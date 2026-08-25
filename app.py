# -*- coding: utf-8 -*-
"""توأمك المهني — CareerTwin AI (Streamlit edition).

Run locally with:
    python -m streamlit run app.py

Arabic-first, full RTL, fully offline Demo Mode, optional Live AI Mode.
"""

import base64
import json
import os
from pathlib import Path

# pyrefly: ignore [missing-import]
import plotly.graph_objects as go
# pyrefly: ignore [missing-import]
import streamlit as st
# pyrefly: ignore [missing-import]
import streamlit.components.v1 as components
import tornado.web

# Monkeypatch Tornado to add COOP/COEP headers to Streamlit for Godot 4 SharedArrayBuffer support
if not hasattr(tornado.web.RequestHandler, "_coop_patched"):
    _original_set_default_headers = tornado.web.RequestHandler.set_default_headers
    def _new_set_default_headers(self):
        _original_set_default_headers(self)
        self.set_header("Cross-Origin-Opener-Policy", "same-origin")
        self.set_header("Cross-Origin-Embedder-Policy", "require-corp")
    tornado.web.RequestHandler.set_default_headers = _new_set_default_headers
    tornado.web.RequestHandler._coop_patched = True

from services import ai_service, demo_engine
from services.scoring import (branch_after, build_report, get_scenario,
                              recommend_fields)
from utils.styles import COLORS, inject_css
from utils.dashboard_styles import inject_dashboard_css
from components.onboarding import page_welcome, page_onboarding
from components.dashboard import page_dashboard
from components.future_map import page_my_future
from components.progress import page_my_progress
from components.support import page_support
from components.navigation import render_navigation
from components.profile_completion import page_profile_completion
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = str(BASE_DIR / "data" / "careers.json")
LOGO_PATH = BASE_DIR / "assets" / "logo.png"
LOGO_MARK_PATH = BASE_DIR / "assets" / "logo_mark.png"


@st.cache_data(show_spinner=False)
def _logo_b64(path_str: str) -> str:
    """Base64-embed the logo so it renders reliably in Streamlit HTML,
    locally and after deployment. Empty string when the file is missing."""
    p = Path(path_str)
    try:
        if p.exists():
            return base64.b64encode(p.read_bytes()).decode("ascii")
    except OSError:
        pass
    return ""

AR_ERRORS = {
    "no_data": "تعذّر تحميل بيانات الوظائف. تأكد من وجود الملف data/careers.json ثم أعد تشغيل التطبيق.",
    "bad_field": "لم يتم العثور على هذا المجال. عد إلى قائمة المجالات واختر من جديد.",
    "bad_position": "لم يتم العثور على هذه الوظيفة. عد إلى قائمة الوظائف واختر من جديد.",
    "bad_scenario": "تعذّر تجهيز هذا الموقف. أعد بدء اليوم من صفحة الوظيفة.",
    "empty": "اكتب قرارك أو اختر أحد الاقتراحات للمتابعة.",
}


# Published mini-games connected to specific positions (cosmetic openers on
# the position page — the interactive 3-mission simulation and all scoring
# always run inside the platform). GAME_INTRO_URL in .env remains a generic
# fallback for any position without a dedicated game.
POSITION_GAME_URLS = {
    "soc": "https://tesana.netlify.app/",
}


# ------------------------------------------------------------------ #
#  Data loading                                                       #
# ------------------------------------------------------------------ #

@st.cache_data(show_spinner=False)
def load_data() -> dict:
    with open(DATA_PATH, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not data.get("fields"):
        raise ValueError("careers.json has no fields")
    return data


def field_by_id(data: dict, fid: str):
    return next((f for f in data["fields"] if f["id"] == fid), None)


def position_by_id(data: dict, pid: str):
    for f in data["fields"]:
        for p in f["positions"]:
            if p["id"] == pid:
                return f, p
    return None, None


# ------------------------------------------------------------------ #
#  Session state + navigation                                         #
# ------------------------------------------------------------------ #

STATE_DEFAULTS = {
    "current_page": "welcome",
    "profile_answers": {},
    "recommended_fields": [],
    "selected_field": None,
    "selected_position": None,
    "scenario_index": 0,
    "scenario_history": [],       # branch path, e.g. ["contained", "clean"]
    "user_answers": [],           # raw user inputs per scenario
    "skill_scores": [],           # per-turn score dicts
    "decision_consequences": [],  # per-turn consequence texts
    "turns": [],                  # full evaluated turn records
    "final_score": None,
    "final_report": None,
    "app_mode": "demo",           # "demo" | "live"
    "language": "ar",
    "awaiting_continue": False,   # a decision was just evaluated
    "sim_error": None,
    "used_fallback": False,
    "chat_open": False,
    "chat_messages": [],
    "chat_last_page": None,
    # --- new dashboard state ---
    "student_profile": {},
    "onboarding_complete": False,
    "onboarding_step": 1,
    "experience_history": [],
    "coach_messages": [],
    "coach_open": False,
    "current_nav": "dashboard",
}


def init_state() -> None:
    for k, v in STATE_DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v


def go_to_page(page_name: str) -> None:
    st.session_state.current_page = page_name


def _dashboard_breadcrumb(lang: str) -> None:
    """Show a subtle back-to-dashboard link for onboarded users in journey pages."""
    if not st.session_state.get("onboarding_complete"):
        return
    label = "← لوحتي" if lang == "ar" else "← My Dashboard"

    def _go_dash():
        st.session_state.current_page = "dashboard"
        st.session_state.current_nav = "dashboard"

    st.button(label, key="dash_breadcrumb", on_click=_go_dash)
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)


def select_field(field_id: str) -> None:
    st.session_state.selected_field = field_id
    go_to_page("positions")


def select_position(position_id: str) -> None:
    st.session_state.selected_position = position_id
    go_to_page("position_intro")


def start_simulation() -> None:
    for k in [k for k in st.session_state.keys()
              if k.startswith("opt_") or k.startswith("txt_")]:
        del st.session_state[k]
    st.session_state.scenario_index = 0
    st.session_state.scenario_history = []
    st.session_state.user_answers = []
    st.session_state.skill_scores = []
    st.session_state.decision_consequences = []
    st.session_state.turns = []
    st.session_state.final_score = None
    st.session_state.final_report = None
    st.session_state.awaiting_continue = False
    st.session_state.sim_error = None
    st.session_state.used_fallback = False
    go_to_page("simulation")


def reset_experience(keep_field: bool = False) -> None:
    field = st.session_state.selected_field
    start_simulation()
    st.session_state.selected_position = None
    if keep_field and field:
        st.session_state.selected_field = field
        go_to_page("positions")
    else:
        st.session_state.selected_field = None
        go_to_page("fields")


def submit_decision(data: dict, position: dict, scenario: dict,
                    opt_key: str, txt_key: str, lang: str) -> None:
    """Evaluate one decision (once), store the turn, and pause for feedback.

    Reads the radio/text values from widget state inside the callback, so the
    text typed right before the click is never lost to a stale render."""
    if st.session_state.awaiting_continue:
        return  # duplicate submission guard

    step = st.session_state.scenario_index
    text = (st.session_state.get(txt_key) or "").strip()
    picked_label = st.session_state.get(opt_key)
    option = next((o for o in scenario["options"] if o["label"][lang] == picked_label), None)

    if not text and option is None:
        st.session_state.sim_error = AR_ERRORS["empty"] if lang == "ar" else data["ui"]["en"]["empty"]
        return
    st.session_state.sim_error = None

    st.session_state.used_fallback = False
    if text:
        local = demo_engine.evaluate_free_text(text, scenario, lang, position, data)
        result, ai_used = local, False
        if st.session_state.app_mode == "live":
            ai = ai_service.evaluate_with_ai(
                position, scenario, step, text, lang,
                st.session_state.turns, local_scores=local["scores"])
            if ai:
                tag = demo_engine.tag_from_scores(ai["scores"], local["tag"], position, data)
                result = {**ai, "tag": tag, "from_text": True}
                ai_used = True
            else:
                st.session_state.used_fallback = True
        decision_text = text
    else:
        result = demo_engine.evaluate_option(option, lang, position, data)
        ai_used = False
        decision_text = option["label"][lang]

    turn = {
        "step": step,
        "situation": scenario["msg"][lang],
        "decision": decision_text,
        "tag": result["tag"],
        "scores": result["scores"],
        "consequence": result["consequence"],
        "feedback": result["feedback"],
        "ai_used": ai_used,
        "src_lang": lang,
        "strengths": result.get("strengths", []),
        "improvements": result.get("improvements", []),
    }
    st.session_state.turns.append(turn)
    st.session_state.user_answers.append(decision_text)
    st.session_state.skill_scores.append(result["scores"])
    st.session_state.decision_consequences.append(result["consequence"])
    if step < 2:
        st.session_state.scenario_history.append(branch_after(step, result["tag"]))
    st.session_state.awaiting_continue = True


def continue_day() -> None:
    st.session_state.awaiting_continue = False
    if st.session_state.scenario_index >= 2:
        generate_final_report()
    else:
        st.session_state.scenario_index += 1


def generate_final_report() -> None:
    data = load_data()
    _, position = position_by_id(data, st.session_state.selected_position)
    if position is None:
        go_to_page("fields")
        return
    lang = st.session_state.language
    report = build_report(st.session_state.turns, position, lang, data,
                          st.session_state.profile_answers)
    st.session_state.final_report = report
    st.session_state.final_score = report["pct"]
    go_to_page("report")


# ------------------------------------------------------------------ #
#  Shared UI pieces                                                   #
# ------------------------------------------------------------------ #

def resolve_app_mode() -> None:
    """Automatic backend mode selection — never exposed in the UI.

    Live AI is used whenever a valid API configuration exists; otherwise the
    prepared Demo scenarios run. For development/testing only, the mode can
    be forced through the CAREERTWIN_FORCE_MODE environment variable
    ("live" or "demo") — nothing is ever shown to users."""
    override = (os.getenv("CAREERTWIN_FORCE_MODE") or "").strip().lower()
    if override in ("live", "demo"):
        st.session_state.app_mode = override
    else:
        st.session_state.app_mode = "live" if ai_service.is_configured() else "demo"


def header(ui: dict) -> None:
    lang    = st.session_state.language
    live    = st.session_state.app_mode == "live"
    on_home = st.session_state.current_page in ("landing", "welcome", "dashboard")
def _logout():
    current_lang = st.session_state.get("language", "ar")
    st.session_state.clear()
    st.session_state.language = current_lang
    st.session_state.current_page = "welcome"
    st.session_state.onboarding_complete = False
    badge = ""
    if live:
        badge_text = "المحاكاة الذكية مفعّلة" if lang == "ar" else "Smart simulation enabled"
        badge = f"<span class='ct-status'><span class='ct-status-dot'></span>{badge_text}</span>"

    mark_b64 = _logo_b64(str(LOGO_MARK_PATH))
    brand_visual = (
        f"<img class='ct-header-mark' src='data:image/png;base64,{mark_b64}' alt='توأمك المهني'/>"
        if mark_b64
        else "<div class='ct-header-mark-fallback'>ت</div>"
    )

    # ── layout: brand | badge | [home] | lang-AR | lang-EN ──
    # Wider columns so buttons always have room — fixes vertical text root cause
    c1, c2, c3, c_logout, c_ar, c_en = st.columns(
        [3.4, 1.6, 1.2, 1.3, 1.1, 1.1],
        vertical_alignment="center"
    )

    with c1:
        st.markdown(
            f"<div class='ct-header-brand'>{brand_visual}"
            f"<div><span style='font-weight:800;font-size:18px'>{ui['brand']}</span> "
            f"<span style='color:{COLORS['turq']};font-weight:800;font-size:18px'>{ui['brandSub']}</span></div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    with c2:
        align = "left" if lang == "ar" else "right"
        st.markdown(f"<div style='text-align:{align}'>{badge}</div>", unsafe_allow_html=True)

    with c3:
        if not on_home:
            home_target = "dashboard" if st.session_state.get("onboarding_complete") else "welcome"
            def _go_home():
                st.session_state.current_page = home_target
                st.session_state.current_nav  = "dashboard"
            st.button(
                "الرئيسية" if lang == "ar" else "Home",
                key="home_btn",
                use_container_width=True,
                on_click=_go_home,
            )

    # Two language buttons — same size, always visible
    ar_type = "primary" if lang == "ar" else "secondary"
    en_type = "primary" if lang == "en" else "secondary"



    with c_logout:
        if st.session_state.get("onboarding_complete"):
            st.button(
                "تسجيل الخروج" if lang == "ar" else "Logout",
                key="logout_btn",
                use_container_width=True,
                on_click=_logout,
            )


    with c_ar:
        if st.button("العربية", key="lang_ar_btn", type=ar_type, use_container_width=True):
            st.session_state.language = "ar"
            st.rerun()
    with c_en:
        if st.button("English", key="lang_en_btn", type=en_type, use_container_width=True):
            st.session_state.language = "en"
            st.rerun()

    st.markdown("<hr class='ct-hr' style='margin-top:4px'/>", unsafe_allow_html=True)



def card(html: str, large: bool = False) -> None:
    st.markdown(f"<div class='{'ct-card-lg' if large else 'ct-card'}'>{html}</div>",
                unsafe_allow_html=True)


def chips(items, lang):
    return "".join(f"<span class='ct-chip'>{x[lang]}</span>" for x in items)


# ------------------------------------------------------------------ #
#  Pages                                                              #
# ------------------------------------------------------------------ #

def page_landing(data: dict, ui: dict, lang: str) -> None:
    anim_bg_html = """
    <style>
    /* Make Streamlit background transparent so our fixed background shows */
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* The animated background container */
    .landing-anim-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -9999;
        background-color: #030a14;
        background-image: radial-gradient(circle at 50% -20%, #0a1930 0%, #030a14 80%);
        overflow: hidden;
    }

    /* Subtle moving digital grid */
    .landing-anim-grid {
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background-image: 
            linear-gradient(rgba(15, 181, 176, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(37, 99, 235, 0.05) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: gridPan 30s linear infinite;
        opacity: 0.8;
    }

    /* Floating Light Orbs for depth and soft glowing waves */
    .landing-glow-1 {
        position: absolute;
        width: 60vw;
        height: 60vw;
        top: -10vh;
        left: -10vw;
        background: radial-gradient(circle, rgba(15, 181, 176, 0.15) 0%, transparent 60%);
        border-radius: 50%;
        filter: blur(60px);
        animation: float1 20s ease-in-out infinite alternate;
    }

    .landing-glow-2 {
        position: absolute;
        width: 70vw;
        height: 70vw;
        bottom: -20vh;
        right: -10vw;
        background: radial-gradient(circle, rgba(37, 99, 235, 0.15) 0%, transparent 60%);
        border-radius: 50%;
        filter: blur(60px);
        animation: float2 25s ease-in-out infinite alternate-reverse;
    }

    /* Light motion trails for forward-looking travel effect */
    .landing-beams {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: repeating-linear-gradient(
            transparent 0%,
            rgba(15, 181, 176, 0.03) 50%,
            transparent 100%
        );
        background-size: 100% 200%;
        animation: beamMove 15s linear infinite;
        opacity: 0.7;
    }

    /* Dark mode overrides for landing page text & cards */
    .ct-hero-landing .ct-title, .ct-h2 { color: #FFFFFF !important; }
    .ct-hero-landing .ct-lede { color: #A0B2C6 !important; }
    .ct-h3 { color: #FFFFFF !important; }
    .ct-muted { color: #8A9BB3 !important; }
    .ct-card {
        background: rgba(11, 27, 51, 0.4) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3) !important;
    }
    .ct-note {
        background: rgba(124, 92, 255, 0.1) !important;
        border: 1px dashed rgba(124, 92, 255, 0.3) !important;
        color: #D3C9F8 !important;
    }

    @keyframes gridPan {
        0% { transform: translateY(0); }
        100% { transform: translateY(50px); }
    }
    @keyframes float1 {
        0% { transform: translate(0, 0) scale(1); }
        100% { transform: translate(8vw, 4vh) scale(1.1); }
    }
    @keyframes float2 {
        0% { transform: translate(0, 0) scale(1); }
        100% { transform: translate(-8vw, -4vh) scale(1.1); }
    }
    @keyframes beamMove {
        0% { background-position: 0% 0%; }
        100% { background-position: 0% 200%; }
    }
    </style>

    <div class="landing-anim-bg">
        <div class="landing-anim-grid"></div>
        <div class="landing-beams"></div>
        <div class="landing-glow-1"></div>
        <div class="landing-glow-2"></div>
    </div>
    """
    st.markdown(anim_bg_html, unsafe_allow_html=True)

    logo_b64 = _logo_b64(str(LOGO_PATH))
    if logo_b64:
        # the platform name (Arabic + English) is part of the logo lockup,
        # so it is not repeated as text — only the tagline is added
        hero_brand = (f"<img class='ct-hero-logo' src='data:image/png;base64,{logo_b64}' "
                      f"alt='توأمك المهني — CareerTwin AI'/>")
    else:
        hero_brand = (f"<div class='ct-hero-logo-fallback'>"
                      f"<div style='font-size:34px;font-weight:800'>توأمك المهني</div>"
                      f"<div style='font-size:19px;font-weight:700;color:{COLORS['turq']}'>CareerTwin AI</div>"
                      f"</div>")
    st.markdown(
        f"<div class='ct-hero-landing'>{hero_brand}"
        f"<div class='ct-title' style='font-size:30px;margin-top:6px'>{ui['tagline']}</div>"
        f"<p class='ct-lede' style='max-width:640px;margin:6px auto 0'>{ui['lede']}</p>"
        f"</div>",
        unsafe_allow_html=True,
    )
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.button(ui["start"], type="primary", width="stretch",
                  on_click=go_to_page, args=("profile",))

    st.markdown(f"<div class='ct-h2' style='margin-top:24px'>{ui['howTitle']}</div>",
                unsafe_allow_html=True)
    cols = st.columns(2)
    for i, step in enumerate(ui["how"]):
        with cols[i % 2]:
            card(f"<div class='ct-h3'>{i + 1}. {step['t']}</div>"
                 f"<p class='ct-muted' style='font-size:14.5px'>{step['d']}</p>")
    st.markdown(f"<div class='ct-note'>{ui['guidance']}</div>", unsafe_allow_html=True)


def _collect_profile_answers(ui: dict) -> dict:
    """Read the five selectors directly from widget state, so callbacks
    always see the answers of the render that was just on screen."""
    answers = {}
    for i, q in enumerate(ui["q"]):
        choice = st.session_state.get(f"profile_q{i}")
        if isinstance(choice, list):
            answers[i] = [q["o"].index(c) for c in choice if c in q["o"]]
        else:
            answers[i] = q["o"].index(choice) if choice in q["o"] else None
    return answers


def page_profile(data: dict, ui: dict, lang: str) -> None:
    # NOTE: Do NOT inject max-width on .block-container — that globally
    # narrows the header columns and causes vertical button text.
    _dashboard_breadcrumb(lang)

    # restore previous answers into widget state (widget keys are dropped by
    # Streamlit when a page isn't rendered, so we seed them back explicitly).
    # After a language switch the stored label belongs to the other language,
    # so remap it from the index-based answers — the source of truth.
    prev_answers = st.session_state.profile_answers or {}
    for i, q in enumerate(ui["q"]):
        key = f"profile_q{i}"
        prev = prev_answers.get(i)
        is_multi = i in [2, 3, 4]
        
        if is_multi:
            valid_prev = isinstance(prev, list) and all(isinstance(p, int) and 0 <= p < len(q["o"]) for p in prev)
            curr = st.session_state.get(key)
            if curr is not None and (not isinstance(curr, list) or any(c not in q["o"] for c in curr)):
                if valid_prev:
                    st.session_state[key] = [q["o"][p] for p in prev]
                else:
                    st.session_state[key] = []
            elif key not in st.session_state and valid_prev:
                st.session_state[key] = [q["o"][p] for p in prev]
        else:
            valid_prev = isinstance(prev, int) and 0 <= prev < len(q["o"])
            curr = st.session_state.get(key)
            if curr is not None and curr not in q["o"]:
                if valid_prev:
                    st.session_state[key] = q["o"][prev]
                else:
                    del st.session_state[key]
            elif key not in st.session_state and valid_prev:
                st.session_state[key] = q["o"][prev]

    answered = []
    for i in range(len(ui["q"])):
        val = st.session_state.get(f"profile_q{i}")
        if isinstance(val, list) and len(val) > 0:
            answered.append(i)
        elif not isinstance(val, list) and val in ui["q"][i]["o"]:
            answered.append(i)
    n_done, n_total = len(answered), len(ui["q"])

    helper = ("إجاباتك تساعدنا على اقتراح المجالات المهنية الأنسب لك — ويمكنك دائماً اختيار أي مجال آخر."
              if lang == "ar" else
              "Your answers help us suggest the career fields that fit you best — you can always pick any other field.")
    step_label = (f"أجبت على <b>{n_done}</b> من {n_total} أسئلة"
                  if lang == "ar" else f"<b>{n_done}</b> of {n_total} questions answered")
    segs = "".join(f"<div class='ct-seg{' on' if i < n_done else ''}'></div>"
                   for i in range(n_total))
    st.markdown(
        f"<div class='ct-hero'>"
        f"<span class='ct-eyebrow'>{'الخطوة الأولى' if lang == 'ar' else 'Step one'} · CareerTwin AI</span>"
        f"<div class='ct-title' style='font-size:30px'>{ui['pTitle']}</div>"
        f"<p class='ct-lede' style='margin:4px 0 0;font-size:15.5px'>{ui['pSub']}</p>"
        f"<p class='ct-muted' style='margin:8px 0 0;font-size:13.5px'>{helper}</p>"
        f"<div class='ct-tracker'>{segs}</div>"
        f"<div class='ct-tracker-label'>{step_label}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    for i, q in enumerate(ui["q"]):
        key = f"profile_q{i}"
        done = i in answered
        with st.container(border=True):
            st.markdown(
                f"<div class='ct-qhead'>"
                f"<div class='ct-qbadge{' done' if done else ''}'>{'' if done else i + 1}</div>"
                f"<div class='ct-qtitle'>{q['q']}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
            st.pills(q["q"], q["o"], selection_mode="multi" if i in [2, 3, 4] else "single",
                     key=key, label_visibility="collapsed")

    st.session_state.profile_answers = _collect_profile_answers(ui)

    st.markdown("<hr class='ct-hr'/>", unsafe_allow_html=True)

    def _next():
        st.session_state.profile_answers = _collect_profile_answers(ui)
        st.session_state.recommended_fields = recommend_fields(
            st.session_state.profile_answers, data)
        go_to_page("fields")

    def _skip():
        st.session_state.recommended_fields = []
        go_to_page("fields")

    cta = (("عرض المجالات المقترحة ←" if lang == "ar" else "Show my suggested fields →")
           if n_done > 0 else
           (ui["next"] + (" ←" if lang == "ar" else " →")))
    st.button(cta, type="primary", width="stretch", on_click=_next)
    c1, c2 = st.columns(2)
    with c1:
        st.button("→ " + ui["back"] if lang == "ar" else "← " + ui["back"],
                  type="tertiary", width="stretch", on_click=go_to_page, args=("landing",))
    with c2:
        st.button(ui["skip"], type="tertiary", width="stretch", on_click=_skip)
    note = ("لا تُحفظ إجاباتك في أي حساب، وتُستخدم فقط لاقتراح المجالات."
            if lang == "ar" else "Answers aren't stored to any account — they're only used to suggest fields.")
    st.markdown(f"<div class='ct-cta-note'>{note}</div>", unsafe_allow_html=True)


def _field_card(f: dict, ui: dict, lang: str, recommended: bool) -> None:
    rec_badge = (f"<span class='ct-eyebrow amber'>{'مقترح لك' if lang == 'ar' else 'Suggested for you'}</span>"
                 if recommended else "")
    monogram = (f"<span class='ct-monogram' "
                f"style='background:{f['tint']};color:{f['accent']}'>"
                f"{f['name']['en'][:1]}</span>")
    # fixed-height sections keep every card identical so the CTA buttons
    # underneath align on the same horizontal baseline
    card(
        f"<div class='ct-fieldcard'>"
        f"<div class='ct-accentbar' style='background:{f['accent']}'></div>"
        f"{rec_badge}"
        f"<div class='ct-h3 ct-field-title'>{monogram}<span>{f['name'][lang]}</span></div>"
        f"<p class='ct-muted ct-field-blurb'>{f['blurb'][lang]}</p>"
        f"<div><span class='ct-chip'>{ui['positionsCount']}</span></div>"
        f"</div>"
    )
    st.button(
        "عِش التجربة" if lang == "ar" else "Live the experience",
        key=f"fld_{f['id']}_{recommended}", type="primary", width="stretch",
        on_click=select_field, args=(f["id"],),
    )


def page_fields(data: dict, ui: dict, lang: str) -> None:
    _dashboard_breadcrumb(lang)
    rec_ids = st.session_state.recommended_fields or []
    if rec_ids:
        card(f"<div class='ct-h2'>{ui['recTitle']}</div><p class='ct-muted'>{ui['recNote']}</p>")
        cols = st.columns(min(3, len(rec_ids)))
        for i, fid in enumerate(rec_ids):
            f = field_by_id(data, fid)
            if f:
                with cols[i % len(cols)]:
                    _field_card(f, ui, lang, recommended=True)
        st.markdown("<hr class='ct-hr'/>", unsafe_allow_html=True)

    card(f"<div class='ct-h2'>{ui['fTitle']}</div><p class='ct-muted'>{ui['fSub']}</p>")
    cols = st.columns(2)
    for i, f in enumerate(data["fields"]):
        with cols[i % 2]:
            _field_card(f, ui, lang, recommended=False)
    st.button(ui["back"], on_click=go_to_page, args=("profile",))


def page_positions(data: dict, ui: dict, lang: str) -> None:
    f = field_by_id(data, st.session_state.selected_field)
    if f is None:
        st.error(AR_ERRORS["bad_field"])
        st.button(ui["backFields"], on_click=go_to_page, args=("fields",))
        return
    card(
        f"<div class='ct-accentbar' style='background:{f['accent']}'></div>"
        f"<div class='ct-h2'>{ui['posTitle'] + ' ' + f['name'][lang] if lang == 'en' else ui['posTitle'] + ' — ' + f['name'][lang]}</div>"
        f"<p class='ct-muted'>{ui['posSub']}</p>",
        large=True,
    )
    cols = st.columns(3)
    for i, p in enumerate(f["positions"]):
        with cols[i]:
            # fixed-height sections keep the three cards identical, so the
            # CTA buttons underneath align on the same horizontal baseline
            card(
                f"<div class='ct-poscard'>"
                f"<div><span class='ct-badge-ready'>{ui['ready']}</span></div>"
                f"<div class='ct-h3 ct-pos-title'>{p['title'][lang]}</div>"
                f"<div class='ct-muted ct-pos-sub'>{p['title']['en'] if lang == 'ar' else p['title']['ar']}</div>"
                f"<p class='ct-pos-desc'>{p['desc'][lang]}</p>"
                f"<div class='ct-muted' style='font-weight:700;margin-bottom:4px'>{ui['skillsLabel']}</div>"
                f"<div class='ct-pos-skills'>{chips(p['skills'][:3], lang)}</div>"
                f"</div>"
            )
            st.button(ui["tryPos"], key=f"pos_{p['id']}",
                      type="primary", width="stretch",
                      on_click=select_position, args=(p["id"],))
    st.button(ui["backFields"], on_click=go_to_page, args=("fields",))


def page_position_intro(data: dict, ui: dict, lang: str) -> None:
    f, p = position_by_id(data, st.session_state.selected_position)
    if p is None:
        st.error(AR_ERRORS["bad_position"])
        st.button(ui["backFields"], on_click=go_to_page, args=("fields",))
        return

    card(
        f"<div class='ct-accentbar' style='background:{f['accent']}'></div>"
        f"<span class='ct-eyebrow blue'>{ui['introTitle']}</span>"
        f"<div class='ct-title' style='font-size:28px'>{p['title'][lang]}</div>"
        f"<div class='ct-muted'>{f['name'][lang]} · {p['title']['en'] if lang == 'ar' else p['title']['ar']}</div>"
        f"<p class='ct-lede' style='margin-top:10px'>{p['desc'][lang]}</p>"
        f"<div class='ct-persona'>{ui['introPersona']}: <b>{p['persona'][lang]}</b></div>",
        large=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        duties = "".join(f"<li style='margin-bottom:6px'>{d[lang]}</li>" for d in p["duties"])
        card(f"<div class='ct-h3'>{ui['dutiesLabel']}</div><ul style='line-height:1.8'>{duties}</ul>")
    with c2:
        card(f"<div class='ct-h3'>{ui['skillsLabel']}</div><div style='margin-top:8px'>{chips(p['skills'], lang)}</div>")

    crit_rows = "".join(
        f"<div style='display:flex;justify-content:space-between;border-bottom:1px solid {COLORS['line']};padding:7px 0'>"
        f"<span>{c[lang]}</span><b style='color:{COLORS['blue']}'>{round(c['w'] * 100)}٪</b></div>"
        for c in p["criteria"]
    )
    card(f"<div class='ct-h3'>{ui['introCrit']}</div>{crit_rows}"
         f"<p class='ct-muted' style='margin-top:10px'>{ui['introNote']}</p>")

    # position-connected mini-game (e.g. the SOC Analyst game on Tesana):
    # shown prominently for mapped positions; GAME_INTRO_URL in .env stays
    # a generic fallback in a collapsed expander. Purely cosmetic — the
    # interactive 3-mission simulation and all scoring run in the platform.
    game_url = POSITION_GAME_URLS.get(p["id"], "")
    if game_url:
        title = ("لعبة محاكاة — عِش التجربة الوظيفية قبل بدء التقييم!"
                 if lang == "ar" else "Simulation Game — Live the job experience before the test!")
        card(f"<div class='ct-h3'>{title}</div>")
        components.iframe(game_url, height=600, scrolling=True)
    else:
        env_url = (os.getenv("GAME_INTRO_URL") or "").strip()
        if env_url.startswith("https://"):
            with st.expander("لعبة محاكاة — عِش التجربة الوظيفية" if lang == "ar" else "Simulation Game — Live the job experience"):
                components.iframe(env_url, height=600, scrolling=True)

    c1, c2 = st.columns([1, 3])
    with c1:
        st.button(ui["prev"], on_click=go_to_page, args=("positions",))
    with c2:
        st.button("ابدأ الرحلة" if lang == "ar" else "Start the journey",
                  type="primary", width="stretch", on_click=start_simulation)


def _quest_hud(p: dict, scenario: dict, step: int, lang: str) -> None:
    """Game HUD: role badge, virtual clock, and the 3-mission quest line."""
    done = step + (1 if st.session_state.awaiting_continue else 0)
    labels = (["المهمة الأولى", "المهمة الثانية", "المهمة الأخيرة"] if lang == "ar"
              else ["Mission 1", "Mission 2", "Final mission"])
    nodes = []
    for i in range(3):
        state = "done" if i < done else ("active" if i == step else "")
        num = "" if i < done else str(i + 1)
        nodes.append(
            f"<div class='ct-qnode'><div class='ct-qdot {state}'>{num}</div>"
            f"<div class='ct-qlabel'>{labels[i]}</div></div>")
        if i < 2:
            nodes.append(f"<div class='ct-qlink{' done' if i < done else ''}'></div>")
    role_small = "يومك الافتراضي في هذه الوظيفة" if lang == "ar" else "Your virtual workday in this role"
    st.markdown(
        f"<div class='ct-hud'>"
        f"<div class='ct-hud-top'>"
        f"<div class='ct-hud-role'>{p['title'][lang]}<small>{role_small}</small></div>"
        f"<span class='ct-hud-time'>{scenario['time']}</span>"
        f"</div>"
        f"<div class='ct-quest'>{''.join(nodes)}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )


def _chat_bubble(kind: str, avatar_letter: str, name: str, body: str,
                 typing: bool = False) -> None:
    row_cls = "ct-chat-row user-row" if kind == "user" else "ct-chat-row"
    dots = ("<span class='ct-typing'><i></i><i></i><i></i></span>" if typing else "")
    st.markdown(
        f"<div class='{row_cls}'>"
        f"<div class='ct-avatar {kind}'>{avatar_letter}</div>"
        f"<div class='ct-bubble {kind}'>"
        f"<div class='ct-bubble-name'>{name}{dots}</div>{body}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )


def page_simulation(data: dict, ui: dict, lang: str) -> None:
    f, p = position_by_id(data, st.session_state.selected_position)
    if p is None:
        st.error(AR_ERRORS["bad_position"])
        st.button(ui["backFields"], on_click=go_to_page, args=("fields",))
        return

    step = st.session_state.scenario_index
    scenario = get_scenario(p, step, st.session_state.scenario_history)
    if scenario is None:
        st.error(AR_ERRORS["bad_scenario"])
        st.button(ui["backFields"], on_click=reset_experience, kwargs={"keep_field": True})
        return

    _quest_hud(p, scenario, step, lang)

    persona = p["persona"][lang]
    coach_name = "مدربك المهني" if lang == "ar" else "Your career coach"

    # opening beat of the day, once, before the first mission
    if step == 0 and not st.session_state.awaiting_continue and not st.session_state.turns:
        brief = ("بدأ يومك. الرسائل الحقيقية ستصلك الآن — قراراتك هي التي تحرك القصة."
                 if lang == "ar" else
                 "Your day begins. Real messages are coming in — your decisions drive the story.")
        _chat_bubble("coach", "م" if lang == "ar" else "C", coach_name, brief)

    # the scenario arrives as an incoming message from the persona
    _chat_bubble("persona", persona[:1], persona, scenario["msg"][lang],
                 typing=not st.session_state.awaiting_continue)

    if not st.session_state.awaiting_continue:
        labels = [o["label"][lang] for o in scenario["options"]]
        opt_key = f"opt_{step}_{'-'.join(st.session_state.scenario_history)}"
        txt_key = f"txt_{step}"

        st.markdown(f"<div class='ct-composer-label'>{ui['suggested']}</div>",
                    unsafe_allow_html=True)
        with st.container(key="sim_choices"):
            st.pills(ui["yourDecision"], labels, selection_mode="single",
                     key=opt_key, label_visibility="collapsed")

        st.markdown(f"<div class='ct-composer-label'>{ui['orWrite']}</div>",
                    unsafe_allow_html=True)
        st.text_area(ui["orWrite"], placeholder=ui["placeholder"],
                     key=txt_key, label_visibility="collapsed", height=100)

        if st.session_state.sim_error:
            st.warning(st.session_state.sim_error)

        st.button(ui["submit"], type="primary", width="stretch",
                  on_click=submit_decision,
                  args=(data, p, scenario, opt_key, txt_key, lang))
    else:
        turn = st.session_state.turns[-1]
        if st.session_state.used_fallback:
            st.info(ui["fallbackNote"])

        # the player's decision echoes back as an outgoing message
        you = "أنت" if lang == "ar" else "You"
        _chat_bubble("user", you[:1], you, turn["decision"])

        # what happened in the scene
        happened = "ماذا حدث" if lang == "ar" else "What happened"
        st.markdown(
            f"<div class='ct-scene-event'><b class='tag'>{happened}</b><br/>{turn['consequence']}</div>",
            unsafe_allow_html=True,
        )

        # coach feedback arrives each step, with the skill readout
        skills_html = "".join(
            f"<span class='ct-skill-chip' style='animation-delay:{0.15 + i * 0.08}s'>"
            f"{c[lang]} <b>{turn['scores'].get(c['key'], 0)}</b>/10</span>"
            for i, c in enumerate(p["criteria"])
        )
        _chat_bubble("coach", "م" if lang == "ar" else "C", coach_name,
                     f"{turn['feedback']}<div style='margin-top:10px'>{skills_html}</div>")

        nxt = (("المهمة التالية" if lang == "ar" else "Next mission")
               if step < 2 else ui["finish"])
        st.button(nxt, type="primary", width="stretch", on_click=continue_day)

    st.button(ui["changeCareer"], type="tertiary", on_click=reset_experience,
              kwargs={"keep_field": True})


def _radar_chart(report: dict, p: dict, lang: str) -> go.Figure:
    crits = p["criteria"]
    labels = [c[lang] for c in crits] + [crits[0][lang]]
    values = [round(report["avg"][c["key"]], 1) for c in crits] + \
             [round(report["avg"][crits[0]["key"]], 1)]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values, theta=labels, fill="toself",
        line=dict(color=COLORS["blue"], width=2),
        fillcolor="rgba(37,99,235,.18)",
        name=p["title"][lang],
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="white",
            radialaxis=dict(range=[0, 10], showticklabels=True, tickfont=dict(size=10),
                            gridcolor=COLORS["line"]),
            angularaxis=dict(tickfont=dict(size=12, color=COLORS["ink"]),
                             gridcolor=COLORS["line"]),
        ),
        showlegend=False, height=380,
        margin=dict(l=60, r=60, t=30, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Tajawal, Plus Jakarta Sans, sans-serif"),
    )
    return fig


def _print_button(lang: str) -> None:
    """Compact outlined print action for the report header area. Browsers only
    allow printing from a user gesture in the page itself, so this renders a
    real HTML button (in a Streamlit frame) calling window.parent.print().
    The @media print stylesheet hides app controls so only the report prints."""
    label = "طباعة التقرير" if lang == "ar" else "Print the report"
    direction = "rtl" if lang == "ar" else "ltr"
    html = f"""
<div style="direction:{direction};text-align:center;margin:0;padding:0">
  <button onclick="window.parent.print()"
    onmouseover="this.style.borderColor='{COLORS['turq']}';this.style.color='{COLORS['ink']}'"
    onmouseout="this.style.borderColor='{COLORS['line']}';this.style.color='{COLORS['ink2']}'"
    style="
      font-family: Tajawal, 'Plus Jakarta Sans', system-ui, sans-serif;
      background: {COLORS['white']};
      color: {COLORS['ink2']};
      border: 1.5px solid {COLORS['line']};
      border-radius: 14px;
      padding: 10px 22px;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: .2px;
      cursor: pointer;
      width: 100%;
      box-shadow: 0 1px 2px rgba(11,27,51,.05);
      transition: border-color .15s ease, color .15s ease;
    ">{label}</button>
</div>
"""
    if hasattr(st, "iframe"):  # Streamlit >= 1.60
        st.iframe(html, height=52)
    else:  # older versions
        components.html(html, height=52)


def page_report(data: dict, ui: dict, lang: str) -> None:
    f, p = position_by_id(data, st.session_state.selected_position)
    report = st.session_state.final_report
    turns = st.session_state.turns

    if p is None or report is None or len(turns) < 3:
        card(f"<div class='ct-h2'>{ui['noReportTitle']}</div><p class='ct-muted'>{ui['noReportBody']}</p>")
        st.button(ui["backFields"], type="primary", on_click=reset_experience)
        return

    # -------- indicator (position-specific title, per the spec) --------
    card(
        f"<div class='ct-accentbar' style='background:{f['accent']}'></div>"
        f"<span class='ct-eyebrow'>{ui['rTitle']}</span>"
        f"<div class='ct-h2'>{ui['indicatorFor']}{p['title'][lang]}</div>"
        f"<div class='ct-muted'>{f['name'][lang]} · {p['title']['en'] if lang == 'ar' else p['title']['ar']}</div>"
        f"<div class='ct-score-pill' style='margin-top:10px'>{report['pct']}٪</div>"
        f"<div class='ct-band'>{report['band']}</div>",
        large=True,
    )
    st.progress(min(100, max(0, report["pct"])) / 100)

    # compact print action right after the summary (renders on the left in
    # RTL, opposite the summary content) — never a full-width bottom button
    _, print_col = st.columns([2.9, 1.1])
    with print_col:
        _print_button(lang)

    # -------- radar chart --------
    st.markdown(f"<div class='ct-h2'>{ui['skillMap']}</div>", unsafe_allow_html=True)
    # no `width` kwarg: full width is the default, and some Streamlit builds
    # route unknown kwargs into deprecated Plotly config (yellow warning)
    st.plotly_chart(_radar_chart(report, p, lang),
                    config={"displayModeBar": False})

    # -------- strengths / improvements --------
    c1, c2 = st.columns(2)
    with c1:
        items = "".join(f"<li style='margin-bottom:8px'>{s}</li>" for s in report["strengths"])
        card(f"<div class='ct-h3' style='color:{COLORS['green']}'>{ui['strongest']}</div>"
             f"<ul style='line-height:1.8;padding:0 1.1rem;margin:6px 0 0'>{items}</ul>")
    with c2:
        items = "".join(f"<li style='margin-bottom:8px'>{s}</li>" for s in report["improvements"])
        card(f"<div class='ct-h3' style='color:{COLORS['amber']}'>{ui['improve']}</div>"
             f"<ul style='line-height:1.8;padding:0 1.1rem;margin:6px 0 0'>{items}</ul>")

    # -------- work style + decision analysis --------
    card(f"<div class='ct-h3'>{ui['styleTitle']}</div><p class='ct-lede'>{report['style']}</p>")
    card(f"<div class='ct-h3'>{ui['comfortTitle']}</div><p class='ct-lede'>{report['comfort']}</p>")

    with st.expander(ui["decisions"]):
        for i, t in enumerate(turns):
            st.markdown(
                f"<div class='ct-card'><b>{i + 1}.</b> {t['decision']}"
                f"<div class='ct-muted' style='margin-top:6px'>{t['consequence']}</div></div>",
                unsafe_allow_html=True)

    # -------- learning path --------
    c1, c2 = st.columns(2)
    with c1:
        items = "".join(f"<li style='margin-bottom:6px'>{x[lang]}</li>" for x in p["learn"])
        card(f"<div class='ct-h3'>{ui['learnTitle']}</div><ul style='line-height:1.8'>{items}</ul>")
    with c2:
        items = "".join(f"<li style='margin-bottom:6px'>{x[lang]}</li>" for x in p["courses"])
        card(f"<div class='ct-h3'>{ui['coursesTitle']}</div><ul style='line-height:1.8'>{items}</ul>")

    # -------- coach message + disclaimer --------
    card(f"<div class='ct-h3'>{ui['coachTitle']}</div><p class='ct-lede'>{report['coach']}</p>")
    st.markdown(f"<div class='ct-note'>{ui['disclaimer']}</div>", unsafe_allow_html=True)

    # -------- save to journey --------
    def _save_to_journey():
        """Save completed experience to the dashboard history."""
        history = st.session_state.get("experience_history", [])
        # Avoid duplicates
        existing_ids = {(e.get("position_id"), e.get("field_id")) for e in history}
        pid = st.session_state.selected_position
        fid = f["id"] if f else None
        if (pid, fid) not in existing_ids:
            top_skills = []
            if report.get("top"):
                top_skills = [c[lang] for c in report["top"][:3]]
            history.append({
                "position_id": pid,
                "field_id": fid,
                "score": report.get("pct", 0),
                "top_skills": top_skills,
                "band": report.get("band", ""),
            })
            st.session_state.experience_history = history
        st.session_state.current_page = "dashboard"
        st.session_state.current_nav = "dashboard"

    # -------- final action row --------
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    if st.session_state.get("onboarding_complete"):
        c1, c2, c3 = st.columns([1.6, 1.2, 1.2])
        with c1:
            st.button(
                "حفظ والعودة للوحة" if lang == "ar" else "Save & Return to Dashboard",
                type="primary", width="stretch",
                key="report_save_btn",
                on_click=_save_to_journey,
            )
        with c2:
            st.button(ui["tryAnother"], width="stretch",
                      key="report_try_btn",
                      on_click=reset_experience, kwargs={"keep_field": True})
        with c3:
            st.button(ui["backFields"], width="stretch",
                      key="report_back_btn",
                      on_click=reset_experience, kwargs={"keep_field": False})
    else:
        _, c1, c2, _ = st.columns([0.9, 1.6, 1.6, 0.9])
        with c1:
            st.button(ui["tryAnother"], type="primary", width="stretch",
                      key="report_try_btn",
                      on_click=reset_experience, kwargs={"keep_field": True})
        with c2:
            st.button(ui["backFields"], width="stretch",
                      key="report_back_btn",
                      on_click=reset_experience, kwargs={"keep_field": False})


# ------------------------------------------------------------------ #
#  Main                                                               #
# ------------------------------------------------------------------ #

PAGES = {
    "welcome":          page_welcome,
    "onboarding":       page_onboarding,
    "dashboard":        page_dashboard,
    "landing":          page_landing,
    "profile":          page_profile,
    "complete_profile": page_profile_completion,
    "fields":           page_fields,
    "positions":        page_positions,
    "position_intro":   page_position_intro,
    "simulation":       page_simulation,
    "report":           page_report,
    "my_future":        page_my_future,
    "my_progress":      page_my_progress,
    "support":          page_support,
    # my_coach removed from nav/PAGES — coach is floating-only now
}

# Pages that should NOT show the unified navigation
_NO_NAV_PAGES = {"welcome", "onboarding"}
# Pages that are part of the existing career journey (keep compact header)
_JOURNEY_PAGES = {"profile", "fields", "positions", "position_intro", "simulation", "report", "landing"}


def main() -> None:
    st.set_page_config(
        page_title="توأمك المهني — CareerTwin AI",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    init_state()
    lang = st.session_state.language
    inject_css(lang)
    inject_dashboard_css(lang)
    resolve_app_mode()

    # ── Migrate stale navigation state ──────────────────────────────
    # If a previous session had my_coach or experiences as current nav/page,
    # redirect them gracefully to the new equivalents.
    if st.session_state.get("current_nav") in ("my_coach", "experiences"):
        nav = st.session_state.current_nav
        st.session_state.current_nav  = "fields" if nav == "experiences" else "dashboard"
        st.session_state.current_page = "fields" if nav == "experiences" else "dashboard"
    if st.session_state.get("current_page") == "my_coach":
        st.session_state.current_page = "dashboard"
        st.session_state.current_nav  = "dashboard"

    try:
        data = load_data()
    except Exception:
        st.error(AR_ERRORS["no_data"])
        st.stop()
        return

    ui      = data["ui"].get(lang) or data["ui"]["ar"]
    current = st.session_state.current_page

    # Always show the brand header
    header(ui)

    # Show unified navigation on all pages except welcome/onboarding
    if current not in _NO_NAV_PAGES and current not in _JOURNEY_PAGES:
        render_navigation(lang)

    page_fn = PAGES.get(current, page_welcome)
    try:
        page_fn(data, ui, lang)
    except Exception as e:
        import traceback
        traceback.print_exc()
        st.error(
            "حدث خطأ غير متوقع. أعدناك إلى قائمة المجالات."
            if lang == "ar"
            else "Something unexpected happened. We took you back to the fields list."
        )
        st.button(ui["backFields"], type="primary", on_click=reset_experience)


if __name__ == "__main__":
    main()
