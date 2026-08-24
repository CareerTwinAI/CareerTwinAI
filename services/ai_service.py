
import json
import os
from typing import Dict, List, Optional

from services.scoring import clamp, keys_of

try:  # optional dependency — Demo Mode must not require it at runtime
    # pyrefly: ignore [missing-import]
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


def is_configured() -> bool:
    """True if either OpenAI or Azure OpenAI credentials are present."""
    if os.getenv("OPENAI_API_KEY"):
        return True
    return bool(os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT")
                and os.getenv("AZURE_OPENAI_DEPLOYMENT"))


def _client_and_model():
    """Build the right client lazily; None on any problem."""
    try:
        if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
            # pyrefly: ignore [missing-import]
            from openai import OpenAI
            client = OpenAI(
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                base_url=os.getenv("AZURE_OPENAI_ENDPOINT").rstrip("/") + "/",
            )
            model = os.getenv("AZURE_OPENAI_DEPLOYMENT")
            return client, model
        if os.getenv("OPENAI_API_KEY"):
            # pyrefly: ignore [missing-import]
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            return client, model
    except Exception:
        pass
    return None, None


def _system_prompt(position: dict, lang: str) -> str:
    lang_line = ("اكتب كل النصوص باللغة العربية الفصحى المبسطة."
                 if lang == "ar" else "Write all text in clear, plain English.")
    duties = "\n".join("- " + d["en"] for d in position["duties"])
    return f"""You are the simulation engine of CareerTwin AI, a career-exploration platform for students in the GCC.
You are running a realistic virtual workday for one specific position: {position['title']['en']}.
The situations must reflect this position's own daily responsibilities and nobody else's:
{duties}
Never borrow a situation from a different profession.
{lang_line}

Rules:
- Never tell the user their answer is simply right or wrong. Show the realistic professional consequence instead.
- Consequences must be concrete and plausible (times, numbers, reactions of colleagues), never dramatic or punitive.
- Feedback is supportive, honest and educational — the voice of an experienced mentor, 2 sentences maximum.
- Keep "consequence" under 60 words so the JSON is always complete.

Return ONLY valid JSON, no markdown fences, no commentary, in exactly this shape:
{{"feedback_to_user":"string","consequence":"string","strengths":["string"],"areas_for_improvement":["string"]}}"""


def _validate(raw: dict, fallback_scores: Optional[Dict[str, int]],
              cat_keys: List[str]) -> Optional[dict]:
    """Port of the original validator: scores are directly pulled from the
    local engine rather than AI to enforce deterministic scoring."""
    if not isinstance(raw, dict):
        return None

    def s(x):
        return x.strip() if isinstance(x, str) and x.strip() else None

    consequence, feedback = s(raw.get("consequence")), s(raw.get("feedback_to_user"))
    if not consequence or not feedback:
        return None

    scores = {}
    for k in cat_keys:
        scores[k] = clamp(fallback_scores.get(k, 5)) if fallback_scores else 5

    def arr(x):
        if not isinstance(x, list):
            return []
        return [i.strip() for i in x if isinstance(i, str) and i.strip()][:3]

    return {
        "scores": scores,
        "consequence": consequence,
        "feedback": feedback,
        "strengths": arr(raw.get("strengths")),
        "improvements": arr(raw.get("areas_for_improvement")),
    }


def evaluate_with_ai(position: dict, scenario: dict, step: int, user_text: str,
                     lang: str, history: List[dict],
                     local_scores: Optional[Dict[str, int]] = None) -> Optional[dict]:
    """Evaluate a decision with the live model. Returns None on ANY failure."""
    client, model = _client_and_model()
    if client is None:
        return None

    cat_keys = keys_of(position)
    ctx = "\n\n".join(
        f"Scenario {i + 1}: {h.get('situation', '')}\nUser decision: {h.get('decision', '')}\n"
        f"Outcome: {h.get('consequence', '')}"
        for i, h in enumerate(history)
    )
    user = (
        f"{('Earlier today:' + chr(10) + ctx + chr(10) + chr(10)) if ctx else ''}"
        f"Current situation (scenario {step + 1} of 3, {scenario.get('time', '')}):\n"
        f"{scenario['msg'][lang]}\n\nThe user's decision:\n\"{user_text}\"\n\n"
        f"Evaluate this decision."
    )

    last_content = user
    for attempt in range(2):
        try:
            if attempt == 1:
                last_content = user + ("\n\nIMPORTANT: the previous reply was not valid JSON. "
                                       "Reply with the JSON object only — no prose, no code fences.")
            res = client.chat.completions.create(
                model=model,
                max_tokens=800,
                temperature=0.6,
                messages=[
                    {"role": "system", "content": _system_prompt(position, lang)},
                    {"role": "user", "content": last_content},
                ],
                timeout=25,
            )
            text = (res.choices[0].message.content or "").strip()
            cleaned = text.replace("```json", "").replace("```", "").strip()
            a, b = cleaned.find("{"), cleaned.rfind("}")
            if a < 0 or b < 0:
                continue
            parsed = _validate(json.loads(cleaned[a:b + 1]), local_scores, cat_keys)
            if parsed:
                return parsed
        except Exception:
            continue
    return None
