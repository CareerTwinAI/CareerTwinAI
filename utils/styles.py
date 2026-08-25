# -*- coding: utf-8 -*-
"""Visual identity for CareerTwin AI — توأمك المهني.

White cards, soft shadows, rounded corners, dark navy ink,
light blue / turquoise / orange accents. Full RTL for Arabic.
"""

# pyrefly: ignore [missing-import]
import streamlit as st

COLORS = {
    "ink": "#0B1B33",
    "ink2": "#33456A",
    "muted": "#7488A8",
    "line": "#E3EAF4",
    "surface": "#F6F9FD",
    "white": "#FFFFFF",
    "blue": "#2563EB",
    "turq": "#0FB5B0",
    "violet": "#7C5CFF",
    "amber": "#F0A02A",
    "green": "#12A56E",
    "red": "#E0533D",
}

SHADOW = "0 1px 2px rgba(11,27,51,.04), 0 12px 32px -12px rgba(11,27,51,.14)"
SHADOW_LG = "0 2px 4px rgba(11,27,51,.04), 0 28px 60px -24px rgba(11,27,51,.22)"


def inject_css(lang: str = "ar") -> None:
    """Inject the global stylesheet. RTL when Arabic is active."""
    rtl = lang == "ar"
    direction = "rtl" if rtl else "ltr"
    text_align = "right" if rtl else "left"
    font = "'Tajawal', system-ui, sans-serif" if rtl else "'Plus Jakarta Sans', system-ui, sans-serif"

    st.markdown(
        f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;800&display=swap');

/* ---------- base ---------- */
html, body, .stApp {{
  background: {COLORS['surface']} !important;
  color: {COLORS['ink']};
}}
.stApp, .stApp * {{ font-family: {font}; }}
/* Streamlit renders control icons (sidebar chevron, expander arrows, etc.)
   as Material Symbols ligatures; without their font they show as raw text
   like "keyboard_double_arrow_right". Re-apply the icon font. */
.stApp [data-testid="stIconMaterial"],
.stApp span[class*="material-symbols"] {{
  font-family: 'Material Symbols Rounded' !important;
  font-weight: normal !important;
  letter-spacing: normal !important;
}}
section.main > div {{ direction: {direction}; }}
.block-container {{
  direction: {direction};
  text-align: {text_align};
  max-width: 1080px;
  padding-top: 1.2rem;
  padding-bottom: 4rem;
}}
h1, h2, h3, h4, h5, p, li, label, span, div {{ color: {COLORS['ink']}; }}
[data-testid="stHeader"] {{ background: transparent; }}
#MainMenu, footer {{ visibility: hidden; }}
/* no sidebar content exists — hide the sidebar and its expand control */
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {{ display: none !important; }}

/* ---------- cards ---------- */
.ct-card {{
  background: {COLORS['white']};
  border: 1px solid {COLORS['line']};
  border-radius: 20px;
  padding: 22px 24px;
  box-shadow: {SHADOW};
  margin-bottom: 16px;
}}
.ct-card-lg {{
  background: {COLORS['white']};
  border: 1px solid {COLORS['line']};
  border-radius: 24px;
  padding: 30px 32px;
  box-shadow: {SHADOW_LG};
  margin-bottom: 18px;
}}
.ct-eyebrow {{
  display: inline-block;
  font-size: 12.5px;
  font-weight: 800;
  letter-spacing: .4px;
  color: {COLORS['turq']};
  background: rgba(15,181,176,.10);
  border-radius: 999px;
  padding: 4px 12px;
  margin-bottom: 10px;
}}
.ct-eyebrow.amber {{ color: {COLORS['amber']}; background: rgba(240,160,42,.12); }}
.ct-eyebrow.blue  {{ color: {COLORS['blue']};  background: rgba(37,99,235,.10); }}
.ct-title   {{ font-size: 34px; font-weight: 800; line-height: 1.25; margin: 0 0 6px; }}
.ct-h2      {{ font-size: 24px; font-weight: 800; margin: 0 0 6px; }}
.ct-h3      {{ font-size: 18px; font-weight: 700; margin: 0 0 4px; }}
.ct-lede    {{ font-size: 16.5px; color: {COLORS['ink2']}; line-height: 1.9; }}
.ct-muted   {{ color: {COLORS['muted']}; font-size: 14px; }}
.ct-chip {{
  display: inline-block;
  background: {COLORS['surface']};
  border: 1px solid {COLORS['line']};
  color: {COLORS['ink2']};
  border-radius: 999px;
  padding: 4px 12px;
  margin: 3px 3px;
  font-size: 13px;
  font-weight: 500;
}}
.ct-badge-ready {{
  display: inline-block;
  color: {COLORS['green']};
  background: rgba(18,165,110,.10);
  border-radius: 999px;
  padding: 4px 12px;
  font-size: 12.5px;
  font-weight: 800;
}}
.ct-time {{
  display: inline-block;
  font-weight: 800;
  color: {COLORS['blue']};
  background: rgba(37,99,235,.08);
  border-radius: 10px;
  padding: 4px 12px;
  font-size: 14px;
}}
.ct-persona {{
  color: {COLORS['muted']};
  font-size: 13.5px;
  margin-top: 4px;
}}
.ct-consequence {{
  background: rgba(240,160,42,.08);
  border: 1px solid rgba(240,160,42,.35);
  border-radius: 16px;
  padding: 16px 18px;
  line-height: 1.9;
}}
.ct-feedback {{
  background: rgba(15,181,176,.07);
  border: 1px solid rgba(15,181,176,.35);
  border-radius: 16px;
  padding: 16px 18px;
  line-height: 1.9;
}}
.ct-note {{
  background: rgba(124,92,255,.06);
  border: 1px dashed rgba(124,92,255,.4);
  border-radius: 14px;
  padding: 12px 16px;
  color: {COLORS['ink2']};
  font-size: 14px;
}}
.ct-score-pill {{
  font-size: 44px;
  font-weight: 800;
  color: {COLORS['blue']};
  line-height: 1.1;
}}
.ct-band {{
  display: inline-block;
  font-weight: 800;
  color: {COLORS['turq']};
  background: rgba(15,181,176,.10);
  border-radius: 999px;
  padding: 5px 16px;
  margin-top: 6px;
}}
.ct-accentbar {{
  height: 5px;
  border-radius: 99px;
  margin-bottom: 14px;
}}
.ct-hr {{ border: none; border-top: 1px solid {COLORS['line']}; margin: 14px 0; }}

/* ================= game-mode simulation ================= */
@keyframes ct-fadeup {{
  from {{ opacity: 0; transform: translateY(10px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes ct-pulse {{
  0%, 100% {{ box-shadow: 0 0 0 0 rgba(37,99,235,.45); }}
  50%      {{ box-shadow: 0 0 0 9px rgba(37,99,235,0); }}
}}
@keyframes ct-blink {{
  0%, 80%, 100% {{ opacity: .25; }}
  40% {{ opacity: 1; }}
}}

/* HUD: quest timeline of the 3 missions */
.ct-hud {{
  background: linear-gradient(135deg, {COLORS['ink']} 0%, #13294B 100%);
  border-radius: 20px;
  padding: 18px 22px;
  margin-bottom: 16px;
  box-shadow: {SHADOW_LG};
  animation: ct-fadeup .4s ease both;
}}
.ct-hud-top {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 14px;
}}
.ct-hud-role {{ color: #fff; font-weight: 800; font-size: 16px; }}
.ct-hud-role small {{ color: #9FB4D8; font-weight: 600; font-size: 12px; display: block; }}
.ct-hud-time {{
  color: #fff;
  background: rgba(255,255,255,.10);
  border: 1px solid rgba(255,255,255,.18);
  border-radius: 999px;
  padding: 5px 14px;
  font-weight: 800;
  font-size: 13.5px;
}}
.ct-quest {{
  display: flex;
  align-items: center;
  gap: 0;
}}
.ct-qnode {{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  min-width: 86px;
}}
.ct-qdot {{
  width: 34px; height: 34px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 14px;
  color: #fff;
  background: rgba(255,255,255,.12);
  border: 2px solid rgba(255,255,255,.25);
}}
.ct-qdot.active {{
  background: {COLORS['blue']};
  border-color: {COLORS['blue']};
  animation: ct-pulse 1.8s ease infinite;
}}
.ct-qdot.done {{
  background: {COLORS['green']};
  border-color: {COLORS['green']};
  position: relative;
}}
.ct-qdot.done::after {{
  content: "";
  width: 11px; height: 6px;
  border: 2.5px solid #fff;
  border-top: none; border-right: none;
  transform: rotate(-45deg) translateY(-1px);
}}
.ct-qdot.done span, .ct-qdot.active + span {{ display: none; }}
.ct-qlabel {{ color: #C9D8F2; font-size: 11.5px; font-weight: 700; }}
.ct-qlink {{
  flex: 1;
  height: 3px;
  border-radius: 99px;
  background: rgba(255,255,255,.15);
  margin: 0 4px 22px;
}}
.ct-qlink.done {{ background: {COLORS['green']}; }}

/* chat scene */
.ct-chat-row {{
  display: flex;
  gap: 10px;
  align-items: flex-start;
  margin: 10px 0;
  animation: ct-fadeup .45s ease both;
}}
.ct-avatar {{
  width: 42px; height: 42px;
  flex: 0 0 42px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 16px;
  color: #fff;
}}
.ct-avatar.persona {{ background: linear-gradient(135deg, {COLORS['blue']}, #4E86F7); }}
.ct-avatar.coach   {{ background: linear-gradient(135deg, {COLORS['turq']}, #23C9BE); }}
.ct-avatar.user    {{ background: {COLORS['ink']}; }}
.ct-bubble {{
  background: {COLORS['white']};
  border: 1px solid {COLORS['line']};
  border-radius: 18px;
  padding: 14px 18px;
  max-width: 82%;
  box-shadow: {SHADOW};
  line-height: 1.9;
}}
.ct-bubble.persona {{ border-start-start-radius: 6px; }}
.ct-bubble.user {{
  background: {COLORS['ink']};
  border-color: {COLORS['ink']};
  color: #fff;
  border-start-end-radius: 6px;
}}
.ct-bubble.user * {{ color: #fff; }}
.ct-bubble.coach {{
  background: rgba(15,181,176,.07);
  border-color: rgba(15,181,176,.4);
  border-start-start-radius: 6px;
}}
.ct-bubble-name {{
  font-size: 12px;
  font-weight: 800;
  color: {COLORS['muted']};
  margin-bottom: 4px;
}}
.ct-chat-row.user-row {{ flex-direction: row-reverse; }}
.ct-typing {{
  display: inline-flex;
  gap: 4px;
  align-items: center;
  margin-inline-start: 6px;
}}
.ct-typing i {{
  width: 6px; height: 6px;
  border-radius: 50%;
  background: {COLORS['muted']};
  animation: ct-blink 1.2s infinite;
}}
.ct-typing i:nth-child(2) {{ animation-delay: .2s; }}
.ct-typing i:nth-child(3) {{ animation-delay: .4s; }}

/* scene event (consequence) */
.ct-scene-event {{
  background: rgba(240,160,42,.08);
  border: 1px solid rgba(240,160,42,.4);
  border-radius: 18px;
  padding: 16px 20px;
  margin: 12px 0;
  line-height: 1.9;
  animation: ct-fadeup .5s ease .15s both;
}}
.ct-scene-event b.tag {{
  display: inline-block;
  color: {COLORS['amber']};
  font-size: 12.5px;
  letter-spacing: .3px;
  margin-bottom: 4px;
}}
.ct-skill-chip {{
  display: inline-block;
  background: {COLORS['white']};
  border: 1px solid {COLORS['line']};
  border-radius: 999px;
  padding: 5px 14px;
  margin: 4px 3px;
  font-size: 13px;
  font-weight: 600;
  color: {COLORS['ink2']};
  animation: ct-fadeup .4s ease both;
}}
.ct-skill-chip b {{ color: {COLORS['blue']}; }}
.ct-composer-label {{
  font-size: 13px;
  font-weight: 800;
  color: {COLORS['muted']};
  margin: 10px 0 2px;
}}
/* choice chips: make simulation pills feel like game choices */
.st-key-sim_choices div[data-testid="stPills"] button {{
  border-radius: 16px !important;
  padding: 12px 18px !important;
  font-size: 14px !important;
  min-height: 50px;
  text-align: start;
  background: #FFFFFF !important;
  border: 1.5px solid #D9E3F0 !important;
  color: #0B1B33 !important;
}}

.st-key-sim_choices div[data-testid="stPills"] button * {{
  color: #0B1B33 !important;
}}

.st-key-sim_choices div[data-testid="stPills"] button:hover {{
  background: #F6F9FD !important;
  border-color: #2563EB !important;
}}
/* ---------- header status badge (non-interactive) ---------- */
.ct-status {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 12.5px;
  font-weight: 700;
  color: {COLORS['ink2']};
  background: {COLORS['white']};
  border: 1px solid {COLORS['line']};
  border-radius: 999px;
  padding: 6px 14px;
}}
.ct-status-dot {{
  width: 8px; height: 8px;
  border-radius: 50%;
  background: {COLORS['green']};
  box-shadow: 0 0 0 3px rgba(18,165,110,.15);
}}

/* ---------- brand: hero logo + header mark ---------- */
.ct-hero-landing {{
  text-align: center;
  padding: 18px 12px 6px;
}}
.ct-hero-logo {{
  width: clamp(190px, 32vw, 300px);
  height: auto;
  object-fit: contain;
  display: inline-block;
}}
.ct-hero-logo-fallback {{ padding: 12px 0; }}
.ct-header-brand {{
  display: flex;
  align-items: center;
  gap: 10px;
}}
.ct-header-mark {{
  width: 44px;
  height: 40px;
  object-fit: contain;
  display: inline-block;
}}
.ct-header-mark-fallback {{
  width: 38px; height: 38px;
  border-radius: 12px;
  background: linear-gradient(135deg, {COLORS['blue']}, {COLORS['turq']});
  color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 17px;
}}
@media (max-width: 720px) {{
  .ct-hero-logo {{ width: clamp(160px, 55vw, 230px); }}
  .ct-header-mark {{ width: 36px; height: 33px; }}
}}

/* ---------- equal-height field cards ---------- */
.ct-fieldcard {{ display: flex; flex-direction: column; }}
.ct-field-title {{
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 62px;
}}
.ct-field-title span:last-child {{
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.5;
}}
.ct-field-blurb {{
  height: 76px;
  margin: 4px 0 10px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.75;
}}
@media (max-width: 900px) {{
  .ct-field-blurb {{ height: auto; -webkit-line-clamp: unset; }}
  .ct-field-title {{ min-height: 0; }}
}}

/* ---------- field monogram (professional icon substitute) ---------- */
.ct-monogram {{
  width: 34px; height: 34px;
  flex: 0 0 34px;
  border-radius: 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 15px;
  font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
}}

/* ---------- equal-height position cards ---------- */
.ct-poscard {{ display: flex; flex-direction: column; }}
.ct-pos-title {{
  margin-top: 8px;
  min-height: 56px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.55;
}}
.ct-pos-sub {{
  font-size: 12.5px;
  min-height: 20px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}
.ct-pos-desc {{
  font-size: 14px;
  color: {COLORS['ink2']};
  line-height: 1.8;
  height: 152px;
  margin: 8px 0 10px;
  overflow-y: auto;
  padding-right: 4px;
}}
.ct-pos-skills {{ height: 78px; overflow-y: auto; padding-right: 4px; }}
@media (max-width: 900px) {{
  .ct-pos-desc {{ height: auto; -webkit-line-clamp: unset; }}
  .ct-pos-skills {{ height: auto; }}
  .ct-pos-title {{ min-height: 0; }}
}}

/* ---------- streamlit widgets ---------- */
/* Streamlit >=1.49 tags buttons with data-testid="stBaseButton-<kind>";
   older builds expose kind="...". Target both so styling always applies. */
.stButton > button, .stFormSubmitButton > button {{
  border-radius: 14px !important;
  border: 1px solid {COLORS['line']} !important;
  font-weight: 700 !important;
  padding: .55rem 1.2rem !important;
  box-shadow: {SHADOW};
  transition: transform .12s ease, background .15s ease, box-shadow .15s ease;
}}
.stButton > button:hover {{ transform: translateY(-1px); }}
.stButton > button p {{ color: {COLORS['ink']}; font-weight: 700; }}

button[kind="primary"],
button[data-testid="stBaseButton-primary"],
button[data-testid="baseButton-primary"] {{
  background: {COLORS['ink']} !important;
  color: #ffffff !important;
  border: none !important;
  letter-spacing: .2px;
}}
button[kind="primary"]:hover,
button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="baseButton-primary"]:hover {{
  background: {COLORS['blue']} !important;
  box-shadow: 0 10px 24px -10px rgba(37,99,235,.55);
}}
/* the label may be a p, span, div or bare markdown node depending on the
   Streamlit build — force white on the button AND everything inside it */
button[kind="primary"] *,
button[data-testid="stBaseButton-primary"] *,
button[data-testid="baseButton-primary"] * {{
  color: #ffffff !important;
  fill: #ffffff !important;
}}

button[kind="secondary"],
button[data-testid="stBaseButton-secondary"] {{
  background: {COLORS['white']} !important;
}}
button[kind="secondary"]:hover,
button[data-testid="stBaseButton-secondary"]:hover {{
  border-color: {COLORS['turq']} !important;
}}
button[kind="secondary"] p,
button[data-testid="stBaseButton-secondary"] p {{
  color: {COLORS['ink']} !important;
}}

button[kind="tertiary"],
button[data-testid="stBaseButton-tertiary"] {{
  box-shadow: none !important;
  border: none !important;
  background: transparent !important;
}}
button[kind="tertiary"] p,
button[data-testid="stBaseButton-tertiary"] p {{
  color: {COLORS['muted']} !important;
  font-weight: 600 !important;
}}
button[kind="tertiary"]:hover p,
button[data-testid="stBaseButton-tertiary"]:hover p {{
  color: {COLORS['ink']} !important;
}}
button[kind="tertiary"]:hover,
button[data-testid="stBaseButton-tertiary"]:hover {{ transform: none !important; }}

/* header pill buttons (language / home) */
.st-key-home_wrap .stButton > button,
.st-key-lang_wrap .stButton > button {{
  border-radius: 999px !important;
  border: 1.5px solid {COLORS['line']} !important;
  background: {COLORS['white']} !important;
  padding: .3rem .9rem !important;
  min-height: 36px;
  box-shadow: 0 1px 2px rgba(11,27,51,.05);
  white-space: nowrap !important;
}}
.st-key-home_wrap .stButton > button:hover,
.st-key-lang_wrap .stButton > button:hover {{
  border-color: {COLORS['turq']} !important;
}}
.st-key-home_wrap .stButton > button *,
.st-key-lang_wrap .stButton > button * {{
  color: {COLORS['ink2']} !important;
  font-size: 13.5px !important;
  font-weight: 700 !important;
  white-space: nowrap !important;
}}

/* ---------- option chips (st.pills) ---------- */
div[data-testid="stPills"] {{ direction: {direction}; }}
div[data-testid="stPills"] > div {{ gap: 10px !important; }}
div[data-testid="stPills"] button {{
  border-radius: 999px !important;
  border: 1.5px solid {COLORS['line']} !important;
  background: {COLORS['white']} !important;
  color: {COLORS['ink2']} !important;
  font-weight: 600 !important;
  font-size: 14.5px !important;
  padding: 9px 18px !important;
  min-height: 42px;
  box-shadow: 0 1px 2px rgba(11,27,51,.05);
  transition: border-color .15s ease, box-shadow .15s ease, transform .12s ease,
              background .15s ease, color .15s ease;
}}
div[data-testid="stPills"] button:hover {{
  border-color: {COLORS['turq']} !important;
  color: {COLORS['ink']} !important;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px -8px rgba(15,181,176,.45);
}}
div[data-testid="stPills"] button:focus-visible {{
  outline: 3px solid rgba(124,92,255,.55) !important;
  outline-offset: 2px;
}}
div[data-testid="stPills"] button[data-testid="stBaseButton-pillsActive"],
div[data-testid="stPills"] button[aria-checked="true"],
div[data-testid="stPills"] button[aria-pressed="true"] {{
  background: linear-gradient(135deg, {COLORS['blue']}, {COLORS['turq']}) !important;
  border-color: transparent !important;
  color: #fff !important;
  box-shadow: 0 8px 20px -8px rgba(37,99,235,.55);
}}
div[data-testid="stPills"] button[data-testid="stBaseButton-pillsActive"] p,
div[data-testid="stPills"] button[aria-checked="true"] p,
div[data-testid="stPills"] button[aria-pressed="true"] p {{ color: #fff !important; }}
div[data-testid="stPills"] button p {{ font-size: 14.5px !important; }}

/* ---------- profile page ---------- */
.ct-hero {{
  background:
    radial-gradient(120% 180% at {'100%' if rtl else '0%'} 0%, rgba(37,99,235,.10), transparent 55%),
    radial-gradient(120% 180% at {'0%' if rtl else '100%'} 100%, rgba(15,181,176,.12), transparent 55%),
    {COLORS['white']};
  border: 1px solid {COLORS['line']};
  border-radius: 24px;
  padding: 30px 32px 26px;
  box-shadow: {SHADOW_LG};
  margin-bottom: 20px;
  position: relative;
  overflow: hidden;
}}
.ct-hero::before {{
  content: "";
  position: absolute;
  inset: 0 0 auto 0;
  height: 5px;
  background: linear-gradient(90deg, {COLORS['blue']}, {COLORS['turq']} 55%, {COLORS['amber']});
}}
.ct-tracker {{
  display: flex;
  gap: 7px;
  margin-top: 18px;
  direction: {direction};
}}
.ct-seg {{
  flex: 1;
  height: 7px;
  border-radius: 99px;
  background: {COLORS['line']};
  transition: background .3s ease;
}}
.ct-seg.on {{ background: linear-gradient(90deg, {COLORS['blue']}, {COLORS['turq']}); }}
.ct-tracker-label {{
  margin-top: 9px;
  font-size: 13px;
  font-weight: 700;
  color: {COLORS['muted']};
}}
.ct-tracker-label b {{ color: {COLORS['blue']}; }}
div[data-testid="stVerticalBlockBorderWrapper"] {{
  background: {COLORS['white']};
  border: 1px solid {COLORS['line']} !important;
  border-radius: 18px !important;
  padding: 16px 18px 8px !important;
  box-shadow: {SHADOW};
  margin-bottom: 14px;
  transition: box-shadow .2s ease, border-color .2s ease;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
  border-color: rgba(15,181,176,.45) !important;
  box-shadow: 0 2px 4px rgba(11,27,51,.04), 0 18px 40px -16px rgba(11,27,51,.20);
}}
.ct-qhead {{
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 4px;
}}
.ct-qbadge {{
  width: 34px; height: 34px;
  border-radius: 11px;
  flex: 0 0 34px;
  display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, {COLORS['blue']}, {COLORS['turq']});
  color: #fff;
  font-weight: 800;
  font-size: 15px;
  box-shadow: 0 6px 14px -6px rgba(37,99,235,.5);
}}
.ct-qbadge.done {{ background: linear-gradient(135deg, {COLORS['green']}, {COLORS['turq']}); position: relative; }}
.ct-qbadge.done::after {{
  content: "";
  width: 11px; height: 6px;
  border: 2.5px solid #fff;
  border-top: none; border-right: none;
  transform: rotate(-45deg) translateY(-1px);
  display: block;
}}
.ct-qtitle {{ font-size: 16.5px; font-weight: 800; color: {COLORS['ink']}; line-height: 1.6; }}
.ct-cta-note {{
  text-align: center;
  color: {COLORS['muted']};
  font-size: 13px;
  margin-top: 6px;
}}
.stRadio > div, .stTextArea textarea {{ direction: {direction}; text-align: {text_align}; }}
.stTextArea textarea {{
  border-radius: 14px !important;
  border: 1px solid {COLORS['line']} !important;
  background: {COLORS['white']} !important;
}}
.stTextArea textarea:focus {{ border-color: {COLORS['turq']} !important; }}
.stProgress > div > div > div > div {{
  background: linear-gradient(90deg, {COLORS['blue']}, {COLORS['turq']});
}}
.stRadio label p {{ font-size: 15px; }}
div[data-testid="stMarkdownContainer"] ul {{ padding-{'right' if rtl else 'left'}: 1.2rem; }}

/* ---------- responsive ---------- */
@media (max-width: 720px) {{
  .ct-title {{ font-size: 26px; }}
  .ct-card, .ct-card-lg {{ padding: 18px 16px; }}
  .ct-score-pill {{ font-size: 36px; }}
}}
@media (prefers-reduced-motion: reduce) {{
  .stButton > button {{ transition: none; }}
}}

/* ---------- print: keep only the report content ---------- */
@media print {{
  .stApp, html, body {{ background: #ffffff !important; }}
  [data-testid="stHeader"], [data-testid="stToolbar"],
  .stButton, .stElementToolbar, [data-testid="stElementToolbar"],
  iframe, hr.ct-hr, .ct-status,
  .st-key-home_wrap, .st-key-lang_wrap {{
    display: none !important;
  }}
  .block-container {{
    max-width: 100% !important;
    padding: 0 !important;
  }}
  .ct-card, .ct-card-lg {{
    box-shadow: none !important;
    border: 1px solid {COLORS['line']} !important;
    break-inside: avoid;
  }}
  [data-testid="stExpander"] details {{ break-inside: avoid; }}
}}

</style>
""",
        unsafe_allow_html=True,
    )
