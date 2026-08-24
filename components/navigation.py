# -*- coding: utf-8 -*-
"""Unified navigation bar — 6 items, no My Coach, correct order.

AR (RTL): الرئيسية | الملف التعريفي | المجالات | تقدّمي | مستقبلي | الدعم
EN (LTR): Home | My Profile | Career Fields | My Progress | My Future | Support
"""

# pyrefly: ignore [missing-import]
import streamlit as st
from utils.styles import COLORS

# (key, label_ar, label_en, page_target)
_NAV = [
    ("dashboard",        "الرئيسية",        "Home",           "dashboard"),
    ("complete_profile", None,              None,             "complete_profile"),  # dynamic label
    ("fields",           "المجالات",        "Career Fields",  "fields"),
    ("my_progress",      "تقدّمي",          "My Progress",    "my_progress"),
    ("my_future",        "مستقبلي",         "My Future",      "my_future"),
    ("support",          "الدعم",           "Support",        "support"),
]


def _profile_label(lang: str) -> str:
    """Return shorter label that fits a nav button."""
    profile = st.session_state.get("student_profile", {})
    has_education = bool(profile.get("education_stage"))
    if has_education:
        return "ملفي التعريفي" if lang == "ar" else "My Profile"
    return "الملف التعريفي" if lang == "ar" else "My Profile"


def render_navigation(lang: str) -> None:
    """Single row of pill buttons — one per page, consistent height, no wrapping."""
    current = st.session_state.get("current_nav", "dashboard")

    # Inject the nav-row wrapper class (CSS is already in dashboard_styles.py)
    st.markdown("<div class='ct-navrow'>", unsafe_allow_html=True)

    # Proportional column widths: profile item gets 1.4 (longer label)
    col_ratios = [1.0, 1.4, 1.1, 1.0, 1.0, 0.8]
    cols = st.columns(col_ratios)

    for i, (key, ar, en, page_target) in enumerate(_NAV):
        # Resolve label
        if key == "complete_profile":
            label = _profile_label(lang)
        else:
            label = ar if lang == "ar" else en

        is_active = current == key
        btn_type = "primary" if is_active else "secondary"

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

    st.markdown("</div>", unsafe_allow_html=True)
