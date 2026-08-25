# -*- coding: utf-8 -*-
"""CareerTwin onboarding: register/sign-in flow and welcome screen."""

import base64
from pathlib import Path
import streamlit as st
from utils.styles import COLORS

BASE_DIR = Path(__file__).resolve().parent.parent
LOGO_PATH = BASE_DIR / "assets" / "logo.png"


@st.cache_data(show_spinner=False)
def _logo_b64() -> str:
    try:
        if LOGO_PATH.exists():
            return base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
    except OSError:
        pass
    return ""


def _go(page: str) -> None:
    st.session_state.current_page = page


def _dir_css(lang: str) -> None:
    direction = "rtl" if lang == "ar" else "ltr"
    align = "right" if lang == "ar" else "left"
    st.markdown(
        f"""
<style>
.ct-onboard-shell, .ct-onboard-shell * {{
    direction: {direction} !important;
    text-align: {align} !important;
}}
[data-testid="stTextInput"], [data-testid="stTextInput"] * {{
    direction: {direction} !important;
}}
[data-testid="stTextInput"] label,
[data-testid="stTextInput"] input {{
    text-align: {align} !important;
}}
</style>
""",
        unsafe_allow_html=True,
    )


def page_welcome(data: dict, ui: dict, lang: str) -> None:
    _dir_css(lang)
    st.markdown(
        """
<style>
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background: transparent !important;
}
.time-tunnel-bg {
    position: fixed; inset: 0; z-index: -9999;
    background-color: #FAFAFA; overflow: hidden; perspective: 800px;
}
.tunnel-ring {
    position: absolute; top: 50%; left: 50%;
    width: 100vw; height: 100vw; margin-left: -50vw; margin-top: -50vw;
    border-radius: 50%; box-sizing: border-box;
    box-shadow: inset 0 0 10vw rgba(15,181,176,.15), 0 0 8vw rgba(37,99,235,.1);
    border: 3vw solid rgba(255,255,255,.6); filter: blur(8px);
    animation: tunnelFly 18s ease-in infinite;
}
.ring-1 { animation-delay: 0s; }
.ring-2 { animation-delay: -3s; }
.ring-3 { animation-delay: -6s; }
.ring-4 { animation-delay: -9s; }
.ring-5 { animation-delay: -12s; }
.ring-6 { animation-delay: -15s; }
@keyframes tunnelFly {
    0% { transform: scale(.01); opacity: 0; }
    20% { opacity: .9; }
    80% { opacity: .2; }
    100% { transform: scale(3.5); opacity: 0; }
}
.ct-hero-landing .ct-title { color:#0B1B33 !important; }
.ct-hero-landing .ct-lede { color:#4A5568 !important; }
</style>
<div class="time-tunnel-bg">
  <div class="tunnel-ring ring-1"></div><div class="tunnel-ring ring-2"></div>
  <div class="tunnel-ring ring-3"></div><div class="tunnel-ring ring-4"></div>
  <div class="tunnel-ring ring-5"></div><div class="tunnel-ring ring-6"></div>
</div>
""",
        unsafe_allow_html=True,
    )
    tagline = "عِش مستقبلك قبل أن تختاره." if lang == "ar" else "Experience your future before choosing it."
    lede = (
        "منصة متكاملة لاستكشاف المسار المهني تجمع بين التوجيه الشخصي وتحليل المهارات وتجارب العمل الواقعية."
        if lang == "ar"
        else "Build career clarity through personalized guidance, skills insights, and realistic job experiences."
    )
    st.markdown(
        f"<div class='ct-hero-landing' style='margin-top:15vh;text-align:center'>"
        f"<div class='ct-title' style='font-size:30px;margin-top:6px'>{tagline}</div>"
        f"<p class='ct-lede' style='max-width:640px;margin:8px auto 0'>{lede}</p>"
        f"</div>",
        unsafe_allow_html=True,
    )
    _, center, _ = st.columns([1.5, 1, 1.5])
    with center:
        st.button(
            "ابدأ رحلتي" if lang == "ar" else "Start My Journey",
            type="primary",
            use_container_width=True,
            on_click=_go,
            args=("onboarding",),
        )
        if st.session_state.get("onboarding_complete"):
            st.button(
                "استكشف لوحتي" if lang == "ar" else "My Dashboard",
                use_container_width=True,
                on_click=_go,
                args=("dashboard",),
            )


def page_onboarding(data: dict, ui: dict, lang: str) -> None:
    _dir_css(lang)
    step = st.session_state.get("onboarding_step", 1)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        dots = []
        for i in range(1, 3):
            cls = "done" if i < step else ("active" if i == step else "")
            dots.append(f"<div class='ct-onboard-dot {cls}'></div>")
        st.markdown(f"<div class='ct-onboard-step'>{''.join(dots)}</div>", unsafe_allow_html=True)
        if step == 1:
            _step_register(lang)
        else:
            _step_ready(lang)


def _step_register(lang: str) -> None:
    mode = st.session_state.get("onboarding_mode", "register")
    is_login = mode == "login"

    title = ("تسجيل الدخول" if lang == "ar" else "Sign In") if is_login else (
        "إنشاء حساب" if lang == "ar" else "Create your account"
    )
    desc = (
        ("أدخل بريدك الإلكتروني وكلمة المرور للمتابعة." if lang == "ar" else "Enter your email and password to continue.")
        if is_login
        else ("أدخل بياناتك للبدء في رحلتك المهنية." if lang == "ar" else "Enter your details to begin your career journey.")
    )

    st.markdown(
        f"<div class='ct-onboard-shell'>"
        f"<span class='ct-eyebrow'>{'الخطوة ١' if lang == 'ar' else 'Step 1'}</span>"
        f"<div class='ct-title' style='font-size:24px;margin:8px 0 4px'>{title}</div>"
        f"<p class='ct-lede' style='margin:0 0 16px;font-size:13px'>{desc}</p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    name = ""
    if not is_login:
        name = st.text_input(
            "الاسم" if lang == "ar" else "Name",
            placeholder="محمد العامري" if lang == "ar" else "John Smith",
            key="ob_name",
        )

    email = st.text_input(
        "البريد الإلكتروني" if lang == "ar" else "Email address",
        placeholder="example@email.com",
        key="ob_email",
    )
    password = st.text_input(
        "كلمة المرور" if lang == "ar" else "Password",
        type="password",
        placeholder="••••••••",
        key="ob_password",
    )

    if "auth_error" not in st.session_state:
        st.session_state.auth_error = ""

    def _submit() -> None:
        email_value = (email or "").strip().lower()
        password_value = password or ""
        st.session_state.auth_error = ""

        if not email_value or not password_value:
            st.session_state.auth_error = (
                "يرجى إدخال البريد الإلكتروني وكلمة المرور."
                if lang == "ar"
                else "Please enter your email and password."
            )
            return

        if is_login:
            account = st.session_state.get("registered_account") or {}
            if account:
                if email_value != account.get("email") or password_value != account.get("password"):
                    st.session_state.auth_error = (
                        "البريد الإلكتروني أو كلمة المرور غير صحيحة."
                        if lang == "ar"
                        else "Incorrect email or password."
                    )
                    return
                profile = dict(account.get("profile") or {})
                profile["email"] = email_value
            else:
                fallback_name = email_value.split("@")[0].replace(".", " ").replace("_", " ").strip().title()
                profile = {
                    "name": fallback_name or ("طالب" if lang == "ar" else "Student"),
                    "email": email_value,
                    "education_stage": "",
                    "emirate": "",
                    "interests": [],
                }
        else:
            display_name = (name or "").strip()
            if not display_name:
                st.session_state.auth_error = "يرجى إدخال الاسم." if lang == "ar" else "Please enter your name."
                return
            existing = st.session_state.get("student_profile", {})
            profile = {
                **existing,
                "name": display_name,
                "email": email_value,
                "education_stage": existing.get("education_stage", ""),
                "emirate": existing.get("emirate", ""),
                "interests": existing.get("interests", []),
            }
            st.session_state.registered_account = {
                "email": email_value,
                "password": password_value,
                "profile": dict(profile),
            }

        st.session_state.student_profile = profile
        st.session_state.onboarding_step = 2

    def _toggle_mode() -> None:
        st.session_state.onboarding_mode = "register" if is_login else "login"
        st.session_state.auth_error = ""

    if st.session_state.get("auth_error"):
        st.error(st.session_state.auth_error)

    if is_login:
        submit_label = "تسجيل الدخول" if lang == "ar" else "Sign In"
    else:
        submit_label = "إنشاء الحساب" if lang == "ar" else "Create Account"

    st.button(
        submit_label,
        type="primary",
        use_container_width=True,
        on_click=_submit,
    )

    toggle_label = (
        ("ليس لديك حساب؟ إنشاء حساب" if lang == "ar" else "Don't have an account? Create one")
        if is_login
        else ("لديك حساب؟ تسجيل الدخول" if lang == "ar" else "Already have an account? Sign in")
    )
    st.button(
        toggle_label,
        type="tertiary",
        use_container_width=True,
        on_click=_toggle_mode,
    )

    notice = (
        "الوضع التجريبي — بيانات الحساب محفوظة خلال الجلسة الحالية فقط."
        if lang == "ar"
        else "Demo Mode — account data is kept for the current session only."
    )
    st.markdown(f"<div class='ct-onboard-notice'>{notice}</div>", unsafe_allow_html=True)


def _step_ready(lang: str) -> None:
    profile = st.session_state.get("student_profile", {})
    name = profile.get("name", "")
    title = f"أهلاً {name}! 🎉" if lang == "ar" else f"Welcome, {name}! 🎉"
    desc = (
        "حسابك جاهز. يمكنك إكمال ملفك التعريفي لاحقاً أو البدء باستكشاف المجالات مباشرة."
        if lang == "ar"
        else "Your account is ready. Complete your profile later or start exploring careers now."
    )
    eyebrow = "جاهز!" if lang == "ar" else "You're set!"

    st.markdown(
        f"<div class='ct-onboard-shell'>"
        f"<span class='ct-eyebrow'>{eyebrow}</span>"
        f"<div class='ct-title' style='font-size:24px;margin:8px 0 4px'>{title}</div>"
        f"<p class='ct-lede' style='margin:0 0 16px;font-size:13px'>{desc}</p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    def _finish() -> None:
        st.session_state.onboarding_complete = True
        st.session_state.current_page = "dashboard"
        st.session_state.current_nav = "dashboard"

    st.button(
        "ادخل إلى لوحتي" if lang == "ar" else "Go to My Dashboard",
        type="primary",
        use_container_width=True,
        on_click=_finish,
    )
