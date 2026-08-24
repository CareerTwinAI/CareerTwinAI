# -*- coding: utf-8 -*-
"""Personalised student dashboard — redesigned 4-row layout.

ROW 1: Compact welcome header (greeting + subtitle + optional CTA)
ROW 2: Four equal metric cards
ROW 3: NBA card (1.4) + Career Roadmap (1)
ROW 4: Recommended career fields from careers.json

All data comes from st.session_state and careers.json.
"""

from datetime import datetime

# pyrefly: ignore [missing-import]
import streamlit as st

from utils.styles import COLORS


# ------------------------------------------------------------------ #
#  Helpers                                                            #
# ------------------------------------------------------------------ #

def _greeting(lang: str) -> str:
    hour = datetime.now().hour
    if lang == "ar":
        return "صباح الخير" if hour < 12 else "مساء الخير"
    return "Good morning" if hour < 12 else ("Good afternoon" if hour < 18 else "Good evening")


def _completed_positions(history: list) -> list:
    return list({e["position_id"] for e in history if e.get("position_id")})


def _fields_explored(history: list) -> set:
    return {e["field_id"] for e in history if e.get("field_id")}


def _roadmap_stage() -> int:
    s       = st.session_state
    history = s.get("experience_history", [])
    n       = len(_completed_positions(history))
    if n >= 3:
        return 5
    if n >= 2:
        return 4
    if n >= 1:
        return 3
    if s.get("selected_field") or s.get("recommended_fields"):
        return 2
    answers = s.get("profile_answers") or {}
    if any(v is not None and v != [] for v in answers.values()):
        return 1
    return 0


# ------------------------------------------------------------------ #
#  Main page                                                          #
# ------------------------------------------------------------------ #

def page_dashboard(data: dict, ui: dict, lang: str) -> None:
    profile   = st.session_state.get("student_profile", {})
    name      = profile.get("name", "")
    history   = st.session_state.get("experience_history", [])
    completed = _completed_positions(history)
    fields_exp = _fields_explored(history)
    stage      = _roadmap_stage()

    # ── ROW 1: Welcome header ──────────────────────────────────────
    greeting = _greeting(lang)
    welcome  = f"{greeting}، {name}" if lang == "ar" and name else (
        f"{greeting}, {name}" if name else greeting
    )
    subtitle = (
        "تابع رحلتك المهنية واكتشف خطوتك التالية."
        if lang == "ar"
        else "Track your career journey and discover your next step."
    )

    # CTA: prompt profile completion if missing
    profile_complete = bool(profile.get("education_stage"))
    cta_html = ""
    if not profile_complete:
        cta_html = (
            f"<div class='ct-dash-welcome-cta'>"
            f"<span style='font-size:12px;color:{COLORS['muted']}'>"
            f"{'أكمل ملفك للحصول على توصيات مخصصة' if lang == 'ar' else 'Complete your profile for personalised recommendations'}"
            f"</span></div>"
        )

    st.markdown(
        f"<div class='ct-dash-welcome'>"
        f"<div class='ct-dash-greeting'>{welcome}</div>"
        f"<p class='ct-dash-subtitle'>{subtitle}</p>"
        f"{cta_html}"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── ROW 2: Four metric cards ────────────────────────────────────
    n_done   = len(completed)
    n_fields = len(fields_exp)
    best_score = (
        max((e["score"] for e in history if e.get("score") is not None), default=None)
        if history
        else None
    )

    # Current direction
    direction_text = ""
    if st.session_state.get("selected_field"):
        fld = next((f for f in data["fields"] if f["id"] == st.session_state["selected_field"]), None)
        if fld:
            direction_text = fld["name"][lang]
    elif st.session_state.get("recommended_fields"):
        fld = next(
            (f for f in data["fields"] if f["id"] == st.session_state["recommended_fields"][0]),
            None,
        )
        if fld:
            direction_text = fld["name"][lang]

    def _metric(color: str, label: str, value: str, hint: str, empty_hint: str = "") -> str:
        val_class = "text" if len(value) > 4 else ""
        is_empty = value == "—"
        hint_html = (
            f"<div class='ct-dash-metric-empty'>{empty_hint}</div>"
            if is_empty and empty_hint
            else f"<div class='ct-dash-metric-hint'>{hint}</div>"
        )
        return (
            f"<div class='ct-dash-metric {color}'>"
            f"<div class='ct-dash-metric-label'>{label}</div>"
            f"<div class='ct-dash-metric-value {val_class}'>{value}</div>"
            f"{hint_html}"
            f"</div>"
        )

    m1 = _metric(
        "blue",
        "التجارب" if lang == "ar" else "Experiences",
        str(n_done) if n_done else "—",
        "تجارب مكتملة" if lang == "ar" else "completed",
        "أكمل أول تجربة" if lang == "ar" else "Complete your first experience",
    )
    m2 = _metric(
        "teal",
        "المجالات" if lang == "ar" else "Fields",
        str(n_fields) if n_fields else "—",
        "تم استكشافها" if lang == "ar" else "explored",
        "اختر مجالاً للبدء" if lang == "ar" else "Pick a field to start",
    )
    m3 = _metric(
        "purple",
        "التوافق" if lang == "ar" else "Match",
        f"{best_score}%" if best_score is not None else "—",
        "أعلى توافق مهني" if lang == "ar" else "highest match",
        "يظهر بعد أول تجربة" if lang == "ar" else "Appears after first experience",
    )
    m4 = _metric(
        "amber",
        "الاتجاه الحالي" if lang == "ar" else "Direction",
        direction_text if direction_text else "—",
        "المجال الأقرب إليك" if lang == "ar" else "your closest field",
        "ابدأ باستكشاف المجالات" if lang == "ar" else "Start exploring fields",
    )

    st.markdown(
        f"<div class='ct-dash-metrics'>{m1}{m2}{m3}{m4}</div>",
        unsafe_allow_html=True,
    )

    # ── ROW 3: Roadmap ──────────────────────────────────────────────
    _, col_road, _ = st.columns([1, 2.5, 1])
    with col_road:
        _render_roadmap(lang, stage)

    # ── Recent experiences (if any) ─────────────────────────────────
    if history:
        st.markdown(
            f"<div class='ct-h2' style='margin-top:24px'>"
            f"{'تجاربك الأخيرة' if lang == 'ar' else 'Recent Experiences'}"
            f"</div>",
            unsafe_allow_html=True,
        )
        _render_recent_experiences(lang, data, history)


# ------------------------------------------------------------------ #
#  Sub-renderers                                                      #
# ------------------------------------------------------------------ #

def _render_roadmap(lang: str, stage: int) -> None:
    labels_ar = ["تعرّف على نفسك", "استكشف المجالات", "جرّب الوظائف", "قارن النتائج", "طوّر مهاراتك", "اختر خطوتك"]
    labels_en = ["Know Yourself", "Explore Fields", "Try Jobs", "Compare Results", "Build Skills", "Choose Path"]
    labels = labels_ar if lang == "ar" else labels_en

    nodes_html = ""
    for i, label in enumerate(labels):
        dot_cls = "done" if i < stage else ("active" if i == stage else "")
        inner   = "✓" if i < stage else str(i + 1)
        nodes_html += (
            f"<div class='ct-dash-road-node'>"
            f"<div class='ct-dash-road-dot {dot_cls}'>{inner}</div>"
            f"<div class='ct-dash-road-label'>{label}</div>"
            f"</div>"
        )
        if i < len(labels) - 1:
            link_cls = "done" if i < stage else ""
            nodes_html += f"<div class='ct-dash-road-link {link_cls}'></div>"

    st.markdown(
        f"<div class='ct-card' style='margin-bottom:0'>"
        f"<div class='ct-h3' style='margin-bottom:10px'>{'خريطة الرحلة' if lang == 'ar' else 'Journey Roadmap'}</div>"
        f"<div class='ct-dash-roadmap'>{nodes_html}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )


def _render_recent_experiences(lang: str, data: dict, history: list) -> None:
    recent    = list(reversed(history))[:3]
    cards_html = "<div class='ct-dash-exp-grid'>"
    for exp in recent:
        fld = next((f for f in data["fields"] if f["id"] == exp.get("field_id")), None)
        if not fld:
            continue
        pos = next((p for p in fld["positions"] if p["id"] == exp.get("position_id")), None)
        if not pos:
            continue
        score      = exp.get("score")
        score_str  = f"{score}%" if score is not None else "—"
        skills_html = "".join(
            f"<span class='ct-chip'>{s[lang]}</span>"
            for s in pos.get("skills", [])[:3]
        )
        cards_html += (
            f"<div class='ct-dash-exp-card'>"
            f"<div class='ct-dash-exp-status completed'>"
            f"{'مكتملة' if lang == 'ar' else 'Completed'} · {score_str}"
            f"</div>"
            f"<div class='ct-dash-exp-field'>{fld['name'][lang]}</div>"
            f"<div class='ct-dash-exp-title'>{pos['title'][lang]}</div>"
            f"<div class='ct-dash-exp-skills'>{skills_html}</div>"
            f"</div>"
        )
    cards_html += "</div>"
    st.markdown(cards_html, unsafe_allow_html=True)
