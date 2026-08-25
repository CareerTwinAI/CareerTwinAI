# -*- coding: utf-8 -*-
"""Unified navigation bar with language-aware direction and logout."""

import streamlit as st

_NAV = [
    ("dashboard",        "الرئيسية",        "Home",           "dashboard"),
    ("complete_profile", None,              None,             "complete_profile"),
    ("fields",           "المجالات",        "Career Fields",  "fields"),
    ("my_progress",      "تقدّمي",          "My Progress",    "my_progress"),
    ("my_future",        "مستقبلي",         "My Future",      "my_future"),
    ("support",          "الدعم",           "Support",        "support"),
]


def _profile_label(lang: str) -> str:
    profile = st.session_state.get("student_profile", {})
    if profile.get("education_stage"):
        return "ملفي التعريفي" if lang == "ar" else "My Profile"
    return "الملف التعريفي" if lang == "ar" else "My Profile"


def _logout() -> None:
    lang = st.session_state.get("language", "ar")
    account = st.session_state.get("registered_account")
    keys = list(st.session_state.keys())
    for key in keys:
        del st.session_state[key]

    st.session_state.language = lang
    if account:
        st.session_state.registered_account = account
    st.session_state.current_page = "welcome"
    st.session_state.current_nav = "dashboard"
    st.session_state.onboarding_complete = False
    st.session_state.onboarding_step = 1
    st.session_state.onboarding_mode = "login" if account else "register"
    st.session_state.student_profile = {}


def render_navigation(lang: str) -> None:
    direction = "rtl" if lang == "ar" else "ltr"
    align = "right" if lang == "ar" else "left"
    st.markdown(
        f"""
<style>
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.block-container {{
    direction: {direction} !important;
    text-align: {align} !important;
}}
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] [data-baseweb="select"],
[data-testid="stMultiSelect"] [data-baseweb="select"],
[data-baseweb="popover"],
[data-baseweb="menu"] {{
    direction: {direction} !important;
    text-align: {align} !important;
}}
.ct-dash-welcome, .ct-dash-metrics, .ct-card, .ct-card-lg,
.ct-profile-header, .ct-profile-section, .ct-dash-roadmap {{
    direction: {direction} !important;
    text-align: {align} !important;
}}
</style>
""",
        unsafe_allow_html=True,
    )

    current = st.session_state.get("current_nav", "dashboard")
    col_ratios = [1.0, 1.4, 1.1, 1.0, 1.0, 0.8, 1.0]
    cols = st.columns(col_ratios)

    for i, (key, ar, en, page_target) in enumerate(_NAV):
        label = _profile_label(lang) if key == "complete_profile" else (ar if lang == "ar" else en)
        btn_type = "primary" if current == key else "secondary"

        with cols[i]:
            if st.button(
                label,
                key=f"nav_{key}",
                type=btn_type,
                use_container_width=True,
            ):
                st.session_state.current_nav = key
                st.session_state.current_page = page_target
                st.rerun()

    with cols[-1]:
        if st.button(
            "تسجيل الخروج" if lang == "ar" else "Logout",
            key="nav_logout",
            type="tertiary",
            use_container_width=True,
        ):
            _logout()
            st.rerun()
