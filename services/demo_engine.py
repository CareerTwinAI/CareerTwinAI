# -*- coding: utf-8 -*-
"""Fully offline evaluation engine — Demo Mode.

Evaluates suggested-decision picks and free-text answers with no API key
and no internet connection. Also serves as the automatic fallback when
Live AI Mode fails, so the experience is never blocked.
"""

import re
from typing import Dict, List, Optional

from services.scoring import arr_to_scores, clamp, keys_of


def _is_latin(word: str) -> bool:
    return bool(re.fullmatch(r"[a-z ]+", word))


def _hits(text: str, words: List[str]) -> int:
    """Count keyword matches, capped at 3. Latin keywords match on a word
    boundary (otherwise "know" scores as "now"); Arabic keeps substring
    matching so verb prefixes (سـ، وـ، أـ) still resolve."""
    n = 0
    for w in words:
        if _is_latin(w):
            if re.search(r"\b" + re.escape(w), text):
                n += 1
        elif w in text:
            n += 1
    return min(3, n)


def evaluate_option(option: dict, lang: str, position: dict, data: dict) -> dict:
    """Score a suggested decision from its authored positional score array."""
    feedback_lib = data["feedback"]
    tag = option.get("tag", "analytical")
    fb = feedback_lib.get(tag) or feedback_lib["analytical"]
    return {
        "scores": arr_to_scores(option.get("s", []), position),
        "tag": tag,
        "consequence": option["cons"][lang],
        "feedback": fb[lang],
        "from_text": False,
    }


def evaluate_free_text(text: str, scenario: dict, lang: str,
                       position: dict, data: dict) -> dict:
    """Keyword-signal heuristic mapped onto the position's own criteria."""
    kw = data["kw"]
    sig = data["sig"]
    feedback_lib = data["feedback"]

    t = (text or "").lower()
    words = len([w for w in re.split(r"\s+", t) if w])
    depth = 1.5 if words >= 30 else 1 if words >= 12 else 0.4 if words >= 5 else -0.5 if words >= 2 else -2

    f = _hits(t, kw["fast"])
    a = _hits(t, kw["analyse"])
    c = _hits(t, kw["comm"])
    d = _hits(t, kw["adapt"])
    w = _hits(t, kw["wait"])

    # length alone must not carry a score: a long answer with no professional
    # substance gets only a fraction of the depth bonus
    substance = f + a + c + d
    base = 3.8 + (depth if substance > 0 else depth * 0.3)

    # floor of 2 so a real attempt is never scored as a non-answer
    def g(v):
        return clamp(max(2, v))

    raw = {
        "analysis": g(base + a * 1.3 - w * 0.8),
        "solve": g(base + (a + f) * 0.7 - w * 0.8),
        "decide": g(base + f * 1.3 - w * 1.5),
        "comm": g(base + c * 1.4 - w * 0.5),
        "adapt": g(base + d * 1.1 + f * 0.4 - w * 0.9),
    }
    scores = {k: raw[sig.get(k, "analysis")] for k in keys_of(position)}

    if w > 0 and f == 0:
        tag = "delayed"
    elif f >= a and f > 0:
        tag = "decisive"
    elif c > a and c > f:
        tag = "communicative"
    elif a > 0:
        tag = "analytical"
    else:
        tag = "clear"

    # the nearest suggested option supplies a realistic consequence
    options = scenario.get("options", [])
    near = next((o for o in options if o.get("tag") == tag), options[0] if options else None)
    consequence = near["cons"][lang] if near and near.get("cons") else ""
    fb = feedback_lib.get(tag) or feedback_lib["analytical"]

    return {
        "scores": scores,
        "tag": tag,
        "consequence": consequence,
        "feedback": fb[lang],
        "from_text": True,
    }


def tag_from_scores(scores: Dict[str, int], fallback: str, position: dict,
                    data: dict) -> str:
    """Keep branching consistent with an external (AI) evaluation instead of
    branching on the local heuristic while scoring with the model."""
    sig = data["sig"]
    keys = keys_of(position)

    def by(signal) -> Optional[int]:
        k = next((x for x in keys if sig.get(x, "analysis") == signal), None)
        return scores.get(k) if k else None

    decide, comm, analysis = by("decide"), by("comm"), by("analysis")
    if decide is not None and decide <= 4:
        return "delayed"
    if comm is not None and comm >= 8 and comm >= (analysis or 0):
        return "clear"
    if decide is not None and decide >= 8:
        return "decisive"
    if analysis is not None and analysis >= 8:
        return "analytical"
    return fallback
