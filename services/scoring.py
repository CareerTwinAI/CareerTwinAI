# -*- coding: utf-8 -*-
"""Position-specific scoring, scenario branching and the final report.

Every position declares its own five criteria and weights. All scoring
runs against those criteria — never against a generic list.
"""

from typing import Dict, List, Optional


def clamp(n) -> int:
    """Clamp any numeric input into the 0–10 integer range."""
    try:
        v = round(float(n))
    except (TypeError, ValueError):
        v = 0
    return max(0, min(10, v))


def keys_of(position: dict) -> List[str]:
    return [c["key"] for c in position.get("criteria", [])]


def arr_to_scores(arr: list, position: dict) -> Dict[str, int]:
    """Authored option arrays are positional: index i is criterion i."""
    keys = keys_of(position)
    out = {}
    for i, k in enumerate(keys):
        out[k] = clamp(arr[i] if i < len(arr) else 5)
    return out


# ------------------------------------------------------------------ #
#  Scenario branching                                                 #
# ------------------------------------------------------------------ #

def branch_after(step_answered: int, tag: str) -> str:
    """Which branch the NEXT scenario takes, given the tag just chosen."""
    if step_answered == 0:
        return "escalated" if tag == "delayed" else "contained"
    return "pressured" if tag in ("delayed", "vague") else "clean"


def get_scenario(position: dict, step: int, path: List[str]) -> Optional[dict]:
    """Return the scenario dict for a step (0..2) along the branch path."""
    s = position.get("scenarios") or {}
    try:
        if step == 0:
            return s["s1"]
        if step == 1:
            return s["s2"].get(path[0] if path else "contained") or s["s2"]["contained"]
        return s["s3"].get(path[1] if len(path) > 1 else "clean") or s["s3"]["clean"]
    except (KeyError, TypeError):
        return None


# ------------------------------------------------------------------ #
#  Field recommendation from the profile answers                      #
# ------------------------------------------------------------------ #

def recommend_fields(answers: dict, data: dict) -> List[str]:
    """Answers are stored as option indices, so this is language-independent."""
    rec = data.get("rec_weights", {})
    score = {f["id"]: 0 for f in data["fields"]}
    for qi in ("2", "3", "4"):
        ans = answers.get(int(qi)) if answers else None
        if ans is None:
            continue
        tables = rec.get(qi) or []
        
        if not isinstance(ans, list):
            ans = [ans]
            
        for idx in ans:
            table = tables[idx] if 0 <= idx < len(tables) else None
            if not table:
                continue
            for k, v in table.items():
                if k in score:
                    score[k] += v
    ranked = sorted(score, key=lambda k: -score[k])
    return [] if score[ranked[0]] == 0 else ranked[:3]


# ------------------------------------------------------------------ #
#  Report                                                             #
# ------------------------------------------------------------------ #

def _strength(crit: dict, key: str, lang: str, phrase_lib: dict) -> str:
    entry = phrase_lib.get(key, {})
    s = (entry.get("s") or {}).get(lang)
    if s:
        return s
    name = entry.get(lang) or key
    return (f"أظهرت قوة واضحة في {name}" if lang == "ar"
            else f"Showed clear strength in {name.lower()}")


def _improve(crit: dict, key: str, lang: str, phrase_lib: dict) -> str:
    entry = phrase_lib.get(key, {})
    i = (entry.get("i") or {}).get(lang)
    if i:
        return i
    name = entry.get(lang) or key
    return (f"طوّر {name} بالتمرّن على مواقف مشابهة" if lang == "ar"
            else f"Develop {name.lower()} by practising similar situations")


def build_report(turns: List[dict], position: dict, lang: str, data: dict,
                 profile_answers: Optional[dict] = None) -> dict:
    """Port of the original report builder — weighted, position-specific."""
    ui = data["ui"][lang]
    sig = data["sig"]
    crit_lib = data["crit"]
    crits = position["criteria"]

    style_idx = (profile_answers or {}).get(4)
    style_answer = None
    if style_idx is not None:
        opts = ui["q"][4]["o"]
        if isinstance(style_idx, list):
            valid_idxs = [i for i in style_idx if 0 <= i < len(opts)]
            if valid_idxs:
                separator = " و " if lang == "ar" else " and "
                style_answer = separator.join(opts[i] for i in valid_idxs)
        elif isinstance(style_idx, int) and 0 <= style_idx < len(opts):
            style_answer = opts[style_idx]


    n = max(1, len(turns))
    avg = {c["key"]: sum(t.get("scores", {}).get(c["key"], 0) for t in turns) / n
           for c in crits}
    weighted = sum(avg[c["key"]] * c["w"] for c in crits)
    pct = round(weighted * 10)

    sorted_crits = sorted(crits, key=lambda c: -avg[c["key"]])
    top = sorted_crits[:2]
    low = list(reversed(sorted_crits[-2:]))

    band = ui["bandHigh"] if pct >= 78 else ui["bandMid"] if pct >= 58 else ui["bandLow"]

    # only reuse AI-written lists produced in the language now on screen,
    # taking at most one per scenario so the last turn can't be crowded out
    def pick(key):
        out = []
        for t in turns:
            if t.get("src_lang") != lang:
                continue
            items = t.get(key) or []
            if items and items[0] not in out:
                out.append(items[0])
        return out

    ai_strengths, ai_improve = pick("strengths"), pick("improvements")
    strengths = (ai_strengths or [_strength(c, c["key"], lang, crit_lib) for c in top])[:3]
    improvements = (ai_improve or [_improve(c, c["key"], lang, crit_lib) for c in low])[:3]

    tags = [t.get("tag") for t in turns]
    fast = tags.count("decisive")
    slow = tags.count("delayed")
    think = sum(1 for x in tags if x in ("analytical", "technical"))
    talk = sum(1 for x in tags if x in ("communicative", "clear"))

    if lang == "ar":
        style = (
            ("تميل إلى الحسم المبكر واحتواء الموقف قبل اكتمال الصورة. " if fast >= 2 else
             "تميل إلى الانتظار وجمع اليقين قبل التحرك، وهو أسلوب يناسب البيئات المستقرة أكثر من البيئات السريعة. " if slow >= 2 else
             "توازن بين التحليل والتحرك، وتقرّر عندما تتضح الملامح الأساسية. ")
            + ("تعتمد على المعطيات قبل الانطباع، " if think >= 2 else "")
            + ("وتُعطي التواصل مع الأطراف المعنية وزناً واضحاً في قرارك."
               if talk >= 2 else "ويمكن أن يستفيد أسلوبك من إشراك الآخرين مبكراً في القرار.")
            + (f" أسلوبك المُعلن ({style_answer}) ظهر فعلاً في طريقة تعاملك مع اليوم." if style_answer else "")
        )
    else:
        style = (
            ("You lean towards early, decisive containment before the picture is complete. " if fast >= 2 else
             "You lean towards waiting for certainty before acting — a style that suits stable environments more than fast-moving ones. " if slow >= 2 else
             "You balance analysis and action, deciding once the main outlines are clear. ")
            + ("You work from evidence rather than impression, " if think >= 2 else "")
            + ("and you give communication with the people involved real weight in your decisions."
               if talk >= 2 else "and your approach would benefit from involving others in the decision earlier.")
            + (f" Your stated preference ({style_answer}) genuinely showed up in how you handled the day." if style_answer else "")
        )

    def sig_avg(signal):
        ks = [c for c in crits if sig.get(c["key"], "analysis") == signal]
        return (sum(avg[c["key"]] for c in ks) / len(ks)) if ks else weighted

    pressure = sig_avg("adapt") + sig_avg("decide")
    title = position["title"][lang]
    if lang == "ar":
        comfort = (
            f"بدوتَ مرتاحاً في إيقاع هذا الدور: القرارات المتتابعة تحت ضغط الوقت لم تُربكك، وهي جوهر {title} اليومي."
            if pressure >= 15 else
            "بدوتَ متماسكاً في معظم اليوم، مع بعض التردد في اللحظات التي تطلبت قراراً بمعلومات ناقصة — وهذا طبيعي في البداية ويتحسّن بالتمرين."
            if pressure >= 11 else
            f"الجانب الأصعب عليك كان اتخاذ القرار قبل اكتمال المعلومات، وهو موقف يتكرر يومياً في {title}. "
            "هذا لا يعني أن الدور غير مناسب، بل أنه يحتاج منك تدريباً على العمل بالمعلومات الناقصة."
        )
        coach = (
            ("طريقتك في التعامل مع هذا اليوم قريبة فعلاً من طريقة العاملين في هذا المجال." if pct >= 78 else
             "لديك أساس واضح، والفجوة بينك وبين هذا الدور فجوة مهارة قابلة للتعلّم لا فجوة استعداد." if pct >= 58 else
             "هذا اليوم كشف لك طبيعة الدور من الداخل، وهذه معلومة أهم من أي نتيجة.")
            + " الخطوة العملية التالية: اختر مهارة واحدة من قائمة التطوير أدناه واعمل عليها أسبوعين، ثم أعد التجربة وقارن."
            + " ولا تنسَ أن تجرّب مهنة أخرى — المقارنة بين تجربتين تكشف أكثر مما تكشفه تجربة واحدة."
        )
    else:
        comfort = (
            f"You looked comfortable with the rhythm of this role: back-to-back decisions under time pressure "
            f"didn't rattle you, and that is the daily core of a {title}."
            if pressure >= 15 else
            "You held together for most of the day, with some hesitation in the moments that demanded a decision "
            "on partial information — normal at the start, and it improves with practice."
            if pressure >= 11 else
            "The hardest part for you was deciding before the information was complete, which happens daily in "
            "this role. That doesn't mean the role is wrong for you — it means this is the specific muscle to train."
        )
        coach = (
            ("The way you handled this day is genuinely close to how people in this field work." if pct >= 78 else
             "You have a clear foundation, and the gap between you and this role is a learnable skill gap, "
             "not a readiness gap." if pct >= 58 else
             "This day showed you the role from the inside, and that's more useful than any score.")
            + " Your practical next step: pick one skill from the development list below, work on it for two weeks,"
            + " then run the experience again and compare. And do try a second career — comparing two experiences"
            + " reveals far more than one."
        )

    return {
        "avg": avg,
        "pct": pct,
        "band": band,
        "top": top,
        "low": low,
        "strengths": strengths,
        "improvements": improvements,
        "style": style,
        "comfort": comfort,
        "coach": coach,
    }
