# -*- coding: utf-8 -*-
"""Unified navigation bar with language-aware direction and logout."""

import streamlit as st

_NAV = [
    ("dashboard", "الرئيسية", "Home", "dashboard"),
    ("complete_profile", None, None, "complete_profile"),
    ("fields", "المجالات", "Career Fields", "fields"),
    ("my_progress", "تقدّمي", "My Progress", "my_progress"),
    ("my_future", "مستقبلي", "My Future", "my_future"),
    ("support", "الدعم", "Support", "support"),
]


def _profile_label(lang: str) -> str:
    return "ملفي التعريفي" if lang == "ar" else "My Profile"


def _logout() -> None:
    lang = st.session_state.get("language", "ar")
    account = st.session_state.get("registered_account")
    for key in list(st.session_state.keys()):
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
[data-testid="stAppViewContainer"], [data-testid="stMain"], .block-container,
[data-testid="stVerticalBlock"], [data-testid="stMarkdownContainer"],
[data-testid="stForm"], [data-testid="stExpander"], [data-testid="stTabs"] {{
    direction: {direction} !important;
    text-align: {align} !important;
}}
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2, [data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4, [data-testid="stMarkdownContainer"] li,
[data-testid="stTextInput"] label, [data-testid="stTextInput"] input,
[data-testid="stTextArea"] label, [data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] label, [data-testid="stSelectbox"] [data-baseweb="select"],
[data-testid="stMultiSelect"] label, [data-testid="stMultiSelect"] [data-baseweb="select"],
[data-testid="stRadio"] label, [data-baseweb="popover"], [data-baseweb="menu"] {{
    direction: {direction} !important;
    text-align: {align} !important;
}}
.ct-dash-welcome, .ct-dash-welcome *, .ct-dash-metrics, .ct-dash-metrics *,
.ct-card, .ct-card *, .ct-card-lg, .ct-card-lg *, .ct-profile-header, .ct-profile-header *,
.ct-profile-section, .ct-profile-section *, .ct-dash-roadmap, .ct-dash-roadmap *,
.ct-future-card, .ct-future-card *, .ct-progress-card, .ct-progress-card *,
.ct-support-card, .ct-support-card * {{
    direction: {direction} !important;
    text-align: {align} !important;
}}
</style>
""",
        unsafe_allow_html=True,
    )

    # Real Streamlit column placement (no position:fixed): English logout is
    # physically in the left-most column; Arabic logout is in the right-most.
    action_cols = st.columns([1.25, 5.5, 1.25])
    logout_col = action_cols[0] if lang == "en" else action_cols[2]
    with logout_col:
        if st.button(
            "Logout" if lang == "en" else "تسجيل الخروج",
            key=f"nav_logout_{lang}",
            type="secondary",
            use_container_width=True,
        ):
            _logout()
            st.rerun()

    current = st.session_state.get("current_nav", "dashboard")
    cols = st.columns([1.0, 1.4, 1.1, 1.0, 1.0, 0.8])
    for i, (key, ar, en, page_target) in enumerate(_NAV):
        label = _profile_label(lang) if key == "complete_profile" else (ar if lang == "ar" else en)
        btn_type = "primary" if current == key else "secondary"
        with cols[i]:
            if st.button(label, key=f"nav_{key}", type=btn_type, use_container_width=True):
                st.session_state.current_nav = key
                st.session_state.current_page = page_target
                st.rerun()
