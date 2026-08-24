# -*- coding: utf-8 -*-

"""Onboarding flow — simplified 2-step: Register → Ready.



Step 1: Name + Email + Password   (no profile fields)

Step 2: Welcome screen → Dashboard



Profile details (education stage, emirate, interests) are collected later

in the separate 'إكمال الملف التعريفي' page.



CRITICAL: This file does NOT inject max-width CSS on .block-container.

That was the root cause of the vertical button-text bug throughout the app.

Instead, content is centered using st.columns().

"""



import base64

from pathlib import Path





# pyrefly: ignore [missing-import]
import streamlit as st

from utils.styles import COLORS



BASE_DIR  = Path(__file__).resolve().parent.parent

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





def _set_step(n: int) -> None:

    st.session_state.onboarding_step = n





# ------------------------------------------------------------------ #

#  Welcome screen                                                     #

# ------------------------------------------------------------------ #



def page_welcome(data: dict, ui: dict, lang: str) -> None:

    """Premium welcome screen — centered CTA."""

    anim_bg_html = """
    <style>
    /* Make Streamlit background transparent */
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: transparent !important;
    }

    .time-tunnel-bg {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -9999;
        background-color: #FAFAFA;
        overflow: hidden;
        perspective: 800px;
    }

    /* Soft light vortex rings for the time-tunnel */
    .tunnel-ring {
        position: absolute;
        top: 50%; left: 50%;
        width: 100vw; height: 100vw;
        margin-left: -50vw; margin-top: -50vw;
        border-radius: 50%;
        box-sizing: border-box;
        box-shadow: inset 0 0 10vw rgba(15, 181, 176, 0.15), 
                    0 0 8vw rgba(37, 99, 235, 0.1);
        border: 3vw solid rgba(255, 255, 255, 0.6);
        filter: blur(8px);
        animation: tunnelFly 18s ease-in infinite;
    }

    /* Staggered rings with slightly different origins for a soft, curved storm effect */
    .ring-1 { animation-delay: -0s; transform-origin: 50% 50%; }
    .ring-2 { animation-delay: -3s; transform-origin: 51% 49%; }
    .ring-3 { animation-delay: -6s; transform-origin: 53% 47%; }
    .ring-4 { animation-delay: -9s; transform-origin: 51% 53%; }
    .ring-5 { animation-delay: -12s; transform-origin: 47% 51%; }
    .ring-6 { animation-delay: -15s; transform-origin: 49% 50%; }

    @keyframes tunnelFly {
        0% { transform: scale(0.01); opacity: 0; }
        20% { opacity: 0.9; }
        80% { opacity: 0.2; }
        100% { transform: scale(3.5); opacity: 0; }
    }

    /* Glowing motion trails flying out from the center */
    .energy-trail {
        position: absolute;
        top: 50%; left: 50%;
        width: 2px; height: 40vh;
        background: linear-gradient(to bottom, transparent, rgba(15, 181, 176, 0.6), transparent);
        animation: trailFly linear infinite;
        transform-origin: top center;
        opacity: 0;
    }

    .trail-1 { --rot: 45deg; animation-delay: -1s; animation-duration: 6s; }
    .trail-2 { --rot: 110deg; animation-delay: -3s; animation-duration: 8s; background: linear-gradient(to bottom, transparent, rgba(37, 99, 235, 0.4), transparent); }
    .trail-3 { --rot: 195deg; animation-delay: -5s; animation-duration: 7s; }
    .trail-4 { --rot: 280deg; animation-delay: -2s; animation-duration: 9s; background: linear-gradient(to bottom, transparent, rgba(37, 99, 235, 0.4), transparent); }
    .trail-5 { --rot: 330deg; animation-delay: -4s; animation-duration: 6.5s; }
    .trail-6 { --rot: 15deg; animation-delay: -6s; animation-duration: 8.5s; background: linear-gradient(to bottom, transparent, rgba(37, 99, 235, 0.4), transparent); }
    .trail-7 { --rot: 150deg; animation-delay: -7s; animation-duration: 7.5s; }
    .trail-8 { --rot: 240deg; animation-delay: -1.5s; animation-duration: 8.2s; }

    @keyframes trailFly {
        0% { transform: rotate(var(--rot)) translateY(20px) scaleY(0.1); opacity: 0; }
        30% { opacity: 0.8; }
        100% { transform: rotate(var(--rot)) translateY(120vh) scaleY(1.5); opacity: 0; }
    }

    /* Light mode text & cards for landing page */
    .ct-hero-landing .ct-title, .ct-h2 { color: #0B1B33 !important; }
    .ct-hero-landing .ct-lede { color: #4A5568 !important; }
    .ct-h3 { color: #0B1B33 !important; }
    .ct-muted { color: #718096 !important; }
    .ct-card {
        background: rgba(255, 255, 255, 0.75) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(15, 181, 176, 0.2) !important;
        box-shadow: 0 8px 32px rgba(11, 27, 51, 0.06) !important;
    }
    .ct-note {
        background: rgba(15, 181, 176, 0.05) !important;
        border: 1px dashed rgba(15, 181, 176, 0.3) !important;
        color: #0B1B33 !important;
    }
    </style>

    <div class="time-tunnel-bg">
        <!-- Tunnel Rings -->
        <div class="tunnel-ring ring-1"></div>
        <div class="tunnel-ring ring-2"></div>
        <div class="tunnel-ring ring-3"></div>
        <div class="tunnel-ring ring-4"></div>
        <div class="tunnel-ring ring-5"></div>
        <div class="tunnel-ring ring-6"></div>

    </div>
    """

    st.markdown(anim_bg_html, unsafe_allow_html=True)



    tagline = (

        "عِش مستقبلك قبل أن تختاره."

        if lang == "ar"

        else "Experience your future before choosing it."

    )

    lede = (

        "منصة متكاملة لاستكشاف المسار المهني تجمع بين التوجيه الشخصي وتحليل المهارات وتجارب العمل الواقعية."

        if lang == "ar"

        else "Build career clarity through personalized guidance, skills insights, and realistic job experiences."

    )



    st.markdown(

        f"<div class='ct-hero-landing' style='margin-top: 15vh;'>"
        f"<div class='ct-title' style='font-size:30px;margin-top:6px'>{tagline}</div>"
        f"<p class='ct-lede' style='max-width:640px;margin:8px auto 0'>{lede}</p>"
        f"</div>",

        unsafe_allow_html=True,

    )



    # Perfectly centered CTA

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

            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

            st.button(

                "استكشف لوحتي" if lang == "ar" else "My Dashboard",

                use_container_width=True,

                on_click=_go,

                args=("dashboard",),

            )





# ------------------------------------------------------------------ #

#  Onboarding — 2 steps                                               #

# ------------------------------------------------------------------ #



def page_onboarding(data: dict, ui: dict, lang: str) -> None:

    """2-step onboarding: Register → Ready.



    Content is centered via columns — no max-width injection on

    .block-container (that was breaking the header button width).

    """

    step = st.session_state.get("onboarding_step", 1)



    # Center the onboarding form

    _, col, _ = st.columns([1, 2, 1])

    with col:

        # Step dots (2 total)

        total = 2

        dot_parts = []

        for i in range(1, total + 1):

            if i < step:

                cls = "done"

            elif i == step:

                cls = "active"

            else:

                cls = ""

            dot_parts.append(f"<div class='ct-onboard-dot {cls}'></div>")

        st.markdown(

            f"<div class='ct-onboard-step'>{''.join(dot_parts)}</div>",

            unsafe_allow_html=True,

        )



        if step == 1:

            _step_register(lang)

        else:

            _step_ready(lang)





# ------------------------------------------------------------------ #

#  Step 1 — Register (Name + Email + Password only)                   #

# ------------------------------------------------------------------ #



def _step_register(lang: str) -> None:

    mode = st.session_state.get("onboarding_mode", "register")

    is_login = (mode == "login")



    if is_login:

        title = "تسجيل الدخول" if lang == "ar" else "Sign In"

        desc  = "أدخل بياناتك للمتابعة." if lang == "ar" else "Enter your details to continue."

    else:

        title = "إنشاء حساب" if lang == "ar" else "Create your account"

        desc  = (

            "أدخل بياناتك للبدء في رحلتك المهنية."

            if lang == "ar"

            else "Enter your details to begin your career journey."

        )



    st.markdown(

        f"<div class='ct-onboard-shell'>"

        f"<span class='ct-eyebrow'>{'الخطوة ١' if lang == 'ar' else 'Step 1'}</span>"

        f"<div class='ct-title' style='font-size:24px;margin:8px 0 4px'>{title}</div>"

        f"<p class='ct-lede' style='margin:0 0 16px;font-size:13px'>{desc}</p>"

        f"</div>",

        unsafe_allow_html=True,

    )



    if not is_login:

        name = st.text_input(

            "الاسم" if lang == "ar" else "Name",

            placeholder="محمد العامري" if lang == "ar" else "John Smith",

            key="ob_name",

        )

    else:

        name = "طالب" if lang == "ar" else "Student"



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



    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)



    def _submit():

        display_name = (name or "").strip() or ("طالب" if lang == "ar" else "Student")

        st.session_state.student_profile = {

            "name": display_name,

            "email": (email or "").strip(),

            # profile details filled later in إكمال الملف التعريفي

            "education_stage": "",

            "emirate": "",

            "interests": [],

        }

        st.session_state.onboarding_step = 2



    def _toggle_mode():

        st.session_state.onboarding_mode = "register" if is_login else "login"



    btn_label = "تسجيل الدخول" if is_login else ("إنشاء الحساب" if lang == "ar" else "Create Account")

    if is_login and lang != "ar":

        btn_label = "Sign In"



    st.button(

        btn_label,

        type="primary",

        use_container_width=True,

        on_click=_submit,

    )



    toggle_text = (

        ("ليس لديك حساب؟ إنشاء حساب" if lang == "ar" else "Don't have an account? Create one")

        if is_login else

        ("لديك حساب؟ تسجيل الدخول" if lang == "ar" else "Already have an account? Sign in")

    )



    st.button(

        toggle_text,

        type="tertiary",

        use_container_width=True,

        on_click=_toggle_mode,

    )



    st.markdown(

        f"<div class='ct-onboard-notice'>"

        f"{'الوضع التجريبي — يمكنك إدخال أي بيانات للمتابعة.' if lang == 'ar' else 'Demo Mode — you can enter any details to continue.'}"

        f"</div>",

        unsafe_allow_html=True,

    )





# ------------------------------------------------------------------ #

#  Step 2 — Ready                                                     #

# ------------------------------------------------------------------ #



def _step_ready(lang: str) -> None:

    profile = st.session_state.get("student_profile", {})

    name    = profile.get("name", "")

    title   = f"أهلاً {name}! 🎉" if lang == "ar" else f"Welcome, {name}! 🎉"

    desc    = (

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



    def _finish():

        st.session_state.onboarding_complete = True

        st.session_state.current_page        = "dashboard"

        st.session_state.current_nav         = "dashboard"



    st.button(

        "ادخل إلى لوحتي" if lang == "ar" else "Go to My Dashboard",

        type="primary",

        use_container_width=True,

        on_click=_finish,

    )

