# -*- coding: utf-8 -*-
"""Support page — redesigned with professional hierarchy."""

import streamlit as st

_TOPICS_AR = ["مشكلة تقنية", "الحساب وكلمة المرور", "اقتراح أو ملاحظة", "سؤال عام"]
_TOPICS_EN = ["Technical issue", "Account & Password", "Suggestion or feedback", "General question"]

_ICON_TECH = (
    "<svg width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='currentColor' "
    "stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
    "<rect x='2' y='3' width='20' height='14' rx='2'/><path d='M8 21h8M12 17v4'/></svg>"
)
_ICON_USER = (
    "<svg width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='currentColor' "
    "stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
    "<circle cx='12' cy='8' r='4'/><path d='M4 20c0-4 3.6-7 8-7s8 3 8 7'/></svg>"
)
_ICON_IDEA = (
    "<svg width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='currentColor' "
    "stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
    "<circle cx='12' cy='12' r='10'/><path d='M12 8v4M12 16h.01'/></svg>"
)


def page_support(data: dict, ui: dict, lang: str) -> None:
    direction = "rtl" if lang == "ar" else "ltr"
    align = "right" if lang == "ar" else "left"

    # Keep all support content and native Streamlit controls in the selected language direction.
    st.markdown(
        f"""
<style>
.ct-support-header, .ct-support-header *,
.ct-support-cats, .ct-support-cats *,
.ct-support-form-card, .ct-support-form-card * {{
    direction: {direction} !important;
    text-align: {align} !important;
}}
[data-testid="stSelectbox"], [data-testid="stTextInput"], [data-testid="stTextArea"] {{
    direction: {direction} !important;
    text-align: {align} !important;
}}
[data-testid="stSelectbox"] label, [data-testid="stTextInput"] label, [data-testid="stTextArea"] label,
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] [data-baseweb="select"],
[data-baseweb="popover"], [data-baseweb="menu"], [role="option"] {{
    direction: {direction} !important;
    text-align: {align} !important;
}}
</style>
""",
        unsafe_allow_html=True,
    )

    # A selectbox keeps its session value across reruns. Remove the previous-language
    # value before rendering so English never shows an Arabic option and vice versa.
    previous_lang = st.session_state.get("support_rendered_lang")
    if previous_lang != lang:
        for key in ("support_type", "support_subject", "support_details"):
            st.session_state.pop(key, None)
        st.session_state.support_rendered_lang = lang

    title = "مركز الدعم" if lang == "ar" else "Support Center"
    subtitle = "نحن هنا لمساعدتك في استخدام منصة توأمك المهني." if lang == "ar" else "We're here to help you use the CareerTwin platform."
    team = "فريق توأمك المهني" if lang == "ar" else "CareerTwin Team"
    team_sub = "متاحون لمساعدتك في أي وقت" if lang == "ar" else "Here to help, any time"

    st.markdown(
        f"<div class='ct-support-header'><div class='ct-dash-greeting' style='font-size:22px'>{title}</div>"
        f"<p class='ct-dash-subtitle'>{subtitle}</p></div>",
        unsafe_allow_html=True,
    )

    cats = [
        (_ICON_TECH, "مشكلة تقنية" if lang == "ar" else "Technical Issue",
         "تحميل الصفحات، خطأ في المحاكاة، توقف المنصة" if lang == "ar" else "Page loading, simulation error, platform freeze"),
        (_ICON_USER, "الحساب والملف" if lang == "ar" else "Account & Profile",
         "تسجيل الدخول، كلمة المرور، بيانات الملف الشخصي" if lang == "ar" else "Sign in, password, profile information"),
        (_ICON_IDEA, "اقتراح أو ملاحظة" if lang == "ar" else "Suggestion or Feedback",
         "تجربة المستخدم، مقترحات جديدة، مشاركة رأيك" if lang == "ar" else "User experience, new ideas, share your feedback"),
    ]

    cats_html = "<div class='ct-support-cats'>"
    for icon, cat_title, cat_items in cats:
        cats_html += (
            f"<div class='ct-support-cat'><div class='ct-support-cat-icon'>{icon}</div>"
            f"<div class='ct-support-cat-title'>{cat_title}</div>"
            f"<div class='ct-support-cat-items'>{cat_items}</div></div>"
        )
    cats_html += "</div>"
    st.markdown(cats_html, unsafe_allow_html=True)

    st.markdown(
        f"<div class='ct-support-form-card'><div class='ct-support-team-row'>"
        f"<div class='ct-support-team-icon'>✦</div><div>"
        f"<div class='ct-support-team-name'>{team}</div>"
        f"<div class='ct-support-team-sub'>{team_sub}</div></div></div></div>",
        unsafe_allow_html=True,
    )

    topics = _TOPICS_AR if lang == "ar" else _TOPICS_EN
    st.selectbox("نوع الطلب" if lang == "ar" else "Request Type", topics, key="support_type")
    st.text_input(
        "الموضوع" if lang == "ar" else "Subject",
        placeholder="مثال: لا تعمل صفحة المحاكاة" if lang == "ar" else "e.g. Simulation page not loading",
        key="support_subject",
    )
    details = st.text_area(
        "التفاصيل" if lang == "ar" else "Details",
        placeholder="اشرح المشكلة أو مقترحك بالتفصيل..." if lang == "ar" else "Describe the issue or suggestion in detail...",
        height=130,
        key="support_details",
    )
    st.text_input(
        "بريدك الإلكتروني (اختياري)" if lang == "ar" else "Your email (optional)",
        value=st.session_state.get("student_profile", {}).get("email", ""),
        placeholder="للرد عليك مباشرة" if lang == "ar" else "So we can reply to you",
        key="support_email",
    )

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    if st.button("إرسال الطلب" if lang == "ar" else "Send Request", type="primary", use_container_width=True, key="support_send_btn"):
        if details and details.strip():
            st.success("✓ " + ("وصلنا طلبك! سيتواصل معك فريق توأمك المهني قريباً." if lang == "ar" else "Request received! The CareerTwin team will get back to you soon."))
        else:
            st.warning("يرجى إضافة تفاصيل قبل الإرسال." if lang == "ar" else "Please add details before sending.")
