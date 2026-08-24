# -*- coding: utf-8 -*-
"""Profile Completion page — إكمال الملف التعريفي.

Collects education stage, school/university, emirate, and interests.
Separated from registration so onboarding stays fast and clean.
All fields are optional — students can skip and return later.
"""

# pyrefly: ignore [missing-import]
import streamlit as st
from utils.styles import COLORS

_EMIRATES_AR  = ["أبوظبي", "دبي", "الشارقة", "عجمان", "أم القيوين", "رأس الخيمة", "الفجيرة"]
_EMIRATES_EN  = ["Abu Dhabi", "Dubai", "Sharjah", "Ajman", "Umm Al Quwain", "Ras Al Khaimah", "Fujairah"]
_STAGES_AR    = ["ثانوية", "جامعة", "خريج حديث", "أستكشف"]
_STAGES_EN    = ["High school", "University", "Fresh graduate", "Exploring"]
_INTERESTS_AR = ["التقنية", "الذكاء الاصطناعي والبيانات", "الأعمال", "الهندسة",
                 "الصحة", "البيئة", "الفنون الإبداعية", "المالية", "الأمن السيبراني"]
_INTERESTS_EN = ["Technology", "AI & Data", "Business", "Engineering",
                 "Health", "Environment", "Creative Arts", "Finance", "Cybersecurity"]


def _completion_pct(profile: dict) -> int:
    """Returns 0-100 profile completion percentage."""
    fields = ["name", "education_stage", "emirate", "interests"]
    filled = sum(1 for f in fields if profile.get(f))
    return int(filled / len(fields) * 100)


def page_profile_completion(data: dict, ui: dict, lang: str) -> None:
    """Profile completion page with progressive, optional fields."""
    profile = st.session_state.get("student_profile", {})
    pct     = _completion_pct(profile)
    is_done = pct >= 75

    # ── Page header ──
    if is_done:
        title    = "ملفي التعريفي" if lang == "ar" else "My Profile"
        subtitle = (
            "يمكنك تحديث معلوماتك في أي وقت."
            if lang == "ar"
            else "You can update your information at any time."
        )
    else:
        title    = "إكمال الملف التعريفي" if lang == "ar" else "Complete Your Profile"
        subtitle = (
            "كلما أكملت ملفك كلما حصلت على توصيات مهنية أدق."
            if lang == "ar"
            else "A complete profile leads to better career recommendations."
        )

    bar_color = COLORS["green"] if is_done else COLORS["blue"]
    st.markdown(
        f"<div class='ct-profile-header'>"
        f"<div class='ct-dash-greeting' style='font-size:22px'>{title}</div>"
        f"<p class='ct-dash-subtitle'>{subtitle}</p>"
        f"<div class='ct-profile-progress-bar'>"
        f"<div class='ct-profile-progress-fill' style='width:{pct}%;background:{bar_color}'></div>"
        f"</div>"
        f"<div style='font-size:11px;color:{COLORS['muted']};margin-top:5px;font-weight:700'>"
        f"{'اكتمال الملف' if lang == 'ar' else 'Profile completion'}: {pct}%</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── Form ──
    stages   = _STAGES_AR   if lang == "ar" else _STAGES_EN
    emirates = _EMIRATES_AR if lang == "ar" else _EMIRATES_EN
    int_list = _INTERESTS_AR if lang == "ar" else _INTERESTS_EN

    current_stage = profile.get("education_stage", "")
    s_def = stages.index(current_stage) if current_stage in stages else 0

    current_emirate = profile.get("emirate", "")
    e_def = emirates.index(current_emirate) if current_emirate in emirates else 0

    # Section 1: Basic
    st.markdown(
        f"<div class='ct-profile-section'>"
        f"<div class='ct-profile-section-title'>"
        f"{'المعلومات الأساسية' if lang == 'ar' else 'Basic Information'}"
        f"</div></div>",
        unsafe_allow_html=True,
    )
    with st.container():
        name = st.text_input(
            "الاسم" if lang == "ar" else "Full Name",
            value=profile.get("name", ""),
            key="pc_name",
        )
        stage = st.selectbox(
            "المرحلة الدراسية" if lang == "ar" else "Education Stage",
            stages,
            index=s_def,
            key="pc_stage",
        )
        school = st.text_input(
            "المدرسة / الجامعة" if lang == "ar" else "School / University",
            value=profile.get("school", ""),
            key="pc_school",
            placeholder="اختياري" if lang == "ar" else "Optional",
        )

    # Section 2: Location
    st.markdown(
        f"<div class='ct-profile-section'>"
        f"<div class='ct-profile-section-title'>"
        f"{'الموقع' if lang == 'ar' else 'Location'}"
        f"</div></div>",
        unsafe_allow_html=True,
    )
    with st.container():
        emirate = st.selectbox(
            "الإمارة" if lang == "ar" else "Emirate",
            emirates,
            index=e_def,
            key="pc_emirate",
        )

    # Section 3: Interests
    st.markdown(
        f"<div class='ct-profile-section'>"
        f"<div class='ct-profile-section-title'>"
        f"{'الاهتمامات المهنية' if lang == 'ar' else 'Career Interests'}"
        f"</div></div>",
        unsafe_allow_html=True,
    )
    with st.container():
        interests = st.multiselect(
            "الاهتمامات" if lang == "ar" else "Interests",
            int_list,
            default=profile.get("interests", []),
            key="pc_interests",
            label_visibility="collapsed",
        )

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    def _save():
        existing = st.session_state.get("student_profile", {})
        st.session_state.student_profile = {
            **existing,
            "name":            (name or "").strip() or existing.get("name", ""),
            "education_stage": stage,
            "school":          school.strip(),
            "emirate":         emirate,
            "interests":       interests,
        }
        st.session_state.current_nav  = "dashboard"
        st.session_state.current_page = "dashboard"

    c1, c2 = st.columns([2, 1])
    with c1:
        st.button(
            "حفظ الملف التعريفي" if lang == "ar" else "Save Profile",
            type="primary",
            use_container_width=True,
            on_click=_save,
            key="pc_save_btn",
        )
    with c2:
        def _skip():
            st.session_state.current_nav  = "dashboard"
            st.session_state.current_page = "dashboard"

        st.button(
            "تخطّ الآن" if lang == "ar" else "Skip for now",
            use_container_width=True,
            on_click=_skip,
            key="pc_skip_btn",
        )
