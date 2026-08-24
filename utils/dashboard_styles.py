# -*- coding: utf-8 -*-
"""Scoped CSS for CareerTwin AI — dashboard, navigation, coach, progress, future-map, support.

Every class is prefixed with ct- so nothing here can accidentally alter existing
Streamlit widgets or the existing simulation / report UI.

Reuses COLORS, SHADOW, SHADOW_LG from utils.styles.
"""

# pyrefly: ignore [missing-import]
import streamlit as st

from utils.styles import COLORS, SHADOW, SHADOW_LG


def inject_dashboard_css(lang: str = "ar") -> None:
    rtl = lang == "ar"
    direction = "rtl" if rtl else "ltr"
    text_align = "right" if rtl else "left"
    font = (
        "'Tajawal', system-ui, sans-serif"
        if rtl
        else "'Plus Jakarta Sans', system-ui, sans-serif"
    )

    st.markdown(
        f"""
<style>
/* =========================================================
   CareerTwin Dashboard — scoped styles v3
   ========================================================= */

/* ===================================================================
   SECTION 0: GLOBAL BUTTON TEXT SAFETY
   Root cause fix: prevent ALL button text from ever going vertical.
   This targets the text nodes *inside* Streamlit buttons.
   =================================================================== */
.stApp button p,
.stApp button span,
.stApp button div {{
  white-space: nowrap !important;
  word-break: keep-all !important;
  overflow-wrap: normal !important;
}}
.stApp button {{
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}}
/* Streamlit wraps button text in a <p>; force it inline */
[data-testid="stBaseButton-primary"] p,
[data-testid="stBaseButton-secondary"] p,
[data-testid="stBaseButton-tertiary"] p {{
  white-space: nowrap !important;
  margin: 0 !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}}

/* ===================================================================
   SECTION 1: HEADER
   =================================================================== */
.ct-header-brand {{
  display: flex;
  align-items: center;
  gap: 10px;
  direction: {direction};
}}
.ct-header-mark {{
  height: 36px;
  width: auto;
  object-fit: contain;
}}
.ct-header-mark-fallback {{
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, {COLORS['blue']}, {COLORS['turq']});
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 16px;
  flex-shrink: 0;
}}
.ct-hr {{
  border: none;
  border-top: 1px solid {COLORS['line']};
  margin: 0;
}}
.ct-status {{
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: {COLORS['green']};
  font-weight: 700;
  background: rgba(18,165,110,.08);
  border: 1px solid rgba(18,165,110,.2);
  border-radius: 999px;
  padding: 3px 10px;
}}
.ct-status-dot {{
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: {COLORS['green']};
  flex-shrink: 0;
  animation: ct-dash-pulse 2.5s ease infinite;
}}

/* Language toggle buttons — pill style, no box */
.ct-lang-wrap {{
  display: flex;
  gap: 6px;
  align-items: center;
  justify-content: flex-end;
}}
.ct-lang-btn {{
  border-radius: 999px !important;
  padding: 5px 14px !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  border: 1.5px solid {COLORS['line']} !important;
  background: {COLORS['white']} !important;
  color: {COLORS['ink2']} !important;
  cursor: pointer !important;
  transition: all .15s ease !important;
  white-space: nowrap !important;
}}
.ct-lang-btn.active {{
  background: {COLORS['ink']} !important;
  border-color: {COLORS['ink']} !important;
  color: #fff !important;
}}
.ct-lang-btn:hover {{
  border-color: {COLORS['turq']} !important;
}}

/* Home / lang Streamlit buttons inside the header row */
div[data-testid="stHorizontalBlock"] button[data-testid^="stBaseButton"] {{
  white-space: nowrap !important;
}}

/* ===================================================================
   SECTION 2: NAVIGATION BAR
   =================================================================== */

/* Wrapper div — horizontally scrollable, RTL/LTR aware */
.ct-navrow {{
  display: flex;
  gap: 6px;
  flex-wrap: nowrap;
  overflow-x: auto;
  padding: 6px 0 12px;
  direction: {direction};
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}}
.ct-navrow::-webkit-scrollbar {{ display: none; }}

/* Column containers inside navrow — auto-size to content */
.ct-navrow [data-testid="column"] {{
  flex: 0 0 auto !important;
  width: auto !important;
  min-width: min-content !important;
}}

/* All nav buttons */
.ct-navrow button {{
  border-radius: 999px !important;
  border: 1.5px solid {COLORS['line']} !important;
  background: {COLORS['white']} !important;
  color: {COLORS['ink2']} !important;
  font-weight: 700 !important;
  font-size: 13px !important;
  padding: 8px 18px !important;
  white-space: nowrap !important;
  min-width: max-content !important;
  width: auto !important;
  height: 40px !important;
  line-height: 1 !important;
  transition: all .18s ease !important;
  box-shadow: none !important;
}}
.ct-navrow button:hover {{
  border-color: {COLORS['turq']} !important;
  color: {COLORS['ink']} !important;
  transform: translateY(-1px) !important;
}}
/* Active nav pill */
.ct-navrow button[data-testid="stBaseButton-primary"] {{
  background: {COLORS['ink']} !important;
  border-color: {COLORS['ink']} !important;
  color: #fff !important;
}}

/* Profile badge indicator dot */
.ct-nav-profile-dot {{
  display: inline-block;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: {COLORS['amber']};
  margin-inline-start: 4px;
  vertical-align: middle;
  flex-shrink: 0;
}}

/* ===================================================================
   SECTION 3: ONBOARDING
   =================================================================== */
.ct-onboard-step {{
  display: flex;
  justify-content: center;
  gap: 8px;
  margin: 16px 0 24px;
}}
.ct-onboard-dot {{
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: {COLORS['line']};
  transition: all .3s ease;
}}
.ct-onboard-dot.done {{
  background: {COLORS['green']};
}}
.ct-onboard-dot.active {{
  background: {COLORS['blue']};
  transform: scale(1.3);
}}
.ct-onboard-shell {{
  background: {COLORS['white']};
  border: 1px solid {COLORS['line']};
  border-radius: 24px;
  padding: 28px 28px 12px;
  box-shadow: {SHADOW};
  margin-bottom: 18px;
  position: relative;
  overflow: hidden;
}}
.ct-onboard-shell::before {{
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, {COLORS['blue']}, {COLORS['turq']});
}}
.ct-onboard-notice {{
  font-size: 12px;
  color: {COLORS['muted']};
  background: {COLORS['surface']};
  border: 1px solid {COLORS['line']};
  border-radius: 10px;
  padding: 8px 12px;
  margin: 10px 0 0;
  text-align: center;
}}
.ct-onboard-link {{
  font-size: 13px;
  color: {COLORS['blue']};
  text-align: center;
  margin-top: 10px;
}}

/* ===================================================================
   SECTION 4: DASHBOARD
   =================================================================== */

/* Welcome header — compact */
.ct-dash-welcome {{
  padding: 22px 28px 18px;
  background: {COLORS['white']};
  border: 1px solid {COLORS['line']};
  border-radius: 20px;
  box-shadow: {SHADOW};
  margin-bottom: 18px;
  position: relative;
  overflow: hidden;
  direction: {direction};
}}
.ct-dash-welcome::before {{
  content: "";
  position: absolute;
  inset: 0 0 auto 0;
  height: 4px;
  background: linear-gradient(90deg, {COLORS['blue']}, {COLORS['turq']} 55%, {COLORS['amber']});
}}
.ct-dash-greeting {{
  font-size: 24px;
  font-weight: 800;
  margin: 0 0 4px;
  color: {COLORS['ink']};
}}
.ct-dash-subtitle {{
  font-size: 14px;
  color: {COLORS['muted']};
  margin: 0;
  line-height: 1.5;
}}
.ct-dash-welcome-cta {{
  margin-top: 14px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}}

/* Metric cards grid */
.ct-dash-metrics {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-bottom: 18px;
}}
.ct-dash-metric {{
  background: {COLORS['white']};
  border: 1px solid {COLORS['line']};
  border-radius: 18px;
  padding: 18px 20px;
  box-shadow: {SHADOW};
  transition: transform .18s ease, box-shadow .18s ease;
  cursor: default;
  direction: {direction};
}}
.ct-dash-metric:hover {{
  transform: translateY(-2px);
  box-shadow: {SHADOW_LG};
}}
.ct-dash-metric.blue   {{ background: rgba(37,99,235,.05);  border-color: rgba(37,99,235,.18);  }}
.ct-dash-metric.teal   {{ background: rgba(15,181,176,.05); border-color: rgba(15,181,176,.18); }}
.ct-dash-metric.purple {{ background: rgba(124,92,255,.05); border-color: rgba(124,92,255,.18); }}
.ct-dash-metric.amber  {{ background: rgba(240,160,42,.05); border-color: rgba(240,160,42,.18); }}
.ct-dash-metric-label {{
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .5px;
  color: {COLORS['muted']};
  margin-bottom: 8px;
}}
.ct-dash-metric-value {{
  font-size: 28px;
  font-weight: 800;
  color: {COLORS['ink']};
  line-height: 1.2;
}}
.ct-dash-metric-value.text {{
  font-size: 15px;
  font-weight: 700;
  line-height: 1.4;
}}
.ct-dash-metric-hint {{
  font-size: 11px;
  color: {COLORS['muted']};
  margin-top: 5px;
  line-height: 1.5;
}}
.ct-dash-metric-empty {{
  font-size: 13px;
  color: {COLORS['muted']};
  font-style: italic;
  margin-top: 6px;
}}

/* Next Best Action card */
.ct-dash-nba {{
  background: {COLORS['white']};
  border: 1px solid {COLORS['line']};
  border-radius: 20px;
  padding: 24px;
  box-shadow: {SHADOW};
  direction: {direction};
  height: 100%;
}}
.ct-dash-nba-icon {{
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: rgba(37,99,235,.08);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: {COLORS['blue']};
  font-size: 20px;
  margin-bottom: 12px;
}}
.ct-dash-nba-label {{
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .5px;
  color: {COLORS['muted']};
  margin-bottom: 6px;
}}
.ct-dash-nba-title {{
  font-size: 16px;
  font-weight: 800;
  color: {COLORS['ink']};
  margin: 0 0 8px;
  line-height: 1.4;
}}
.ct-dash-nba-desc {{
  font-size: 13px;
  color: {COLORS['muted']};
  line-height: 1.6;
  margin: 0 0 16px;
}}

/* Career roadmap */
.ct-dash-roadmap {{
  display: flex;
  align-items: flex-start;
  gap: 0;
  overflow-x: auto;
  padding: 12px 0 4px;
  direction: {direction};
  scrollbar-width: none;
}}
.ct-dash-roadmap::-webkit-scrollbar {{ display: none; }}
.ct-dash-road-node {{
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 88px;
  text-align: center;
  gap: 6px;
  flex-shrink: 0;
}}
.ct-dash-road-dot {{
  width: 34px;
  height: 34px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 12px;
  border: 2.5px solid {COLORS['line']};
  background: {COLORS['white']};
  color: {COLORS['muted']};
  transition: all .3s ease;
  flex-shrink: 0;
}}
.ct-dash-road-dot.done {{
  background: {COLORS['green']};
  border-color: {COLORS['green']};
  color: #fff;
  font-size: 15px;
}}
.ct-dash-road-dot.active {{
  background: {COLORS['blue']};
  border-color: {COLORS['blue']};
  color: #fff;
  animation: ct-dash-pulse 2s ease infinite;
}}
.ct-dash-road-label {{
  font-size: 10px;
  font-weight: 700;
  color: {COLORS['muted']};
  max-width: 80px;
  line-height: 1.3;
}}
.ct-dash-road-link {{
  flex: 1;
  height: 3px;
  min-width: 16px;
  border-radius: 99px;
  background: {COLORS['line']};
  margin: 15px 2px 0;
  transition: background .3s ease;
  flex-shrink: 0;
}}
.ct-dash-road-link.done {{
  background: {COLORS['green']};
}}

/* Recommended fields grid */
.ct-dash-rec-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  gap: 14px;
  margin-top: 4px;
}}
.ct-dash-rec-card {{
  background: {COLORS['white']};
  border: 1px solid {COLORS['line']};
  border-radius: 18px;
  padding: 20px;
  box-shadow: {SHADOW};
  transition: transform .18s ease, box-shadow .18s ease;
  direction: {direction};
}}
.ct-dash-rec-card:hover {{
  transform: translateY(-2px);
  box-shadow: {SHADOW_LG};
  border-color: rgba(37,99,235,.25);
}}
.ct-dash-rec-name {{
  font-size: 15px;
  font-weight: 800;
  color: {COLORS['ink']};
  margin: 0 0 6px;
}}
.ct-dash-rec-desc {{
  font-size: 12px;
  color: {COLORS['muted']};
  line-height: 1.55;
  margin-bottom: 12px;
}}
.ct-dash-rec-skills {{
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 14px;
}}

/* Experience history grid */
.ct-dash-exp-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 14px;
}}
.ct-dash-exp-card {{
  background: {COLORS['white']};
  border: 1px solid {COLORS['line']};
  border-radius: 16px;
  padding: 16px 18px;
  box-shadow: {SHADOW};
  transition: transform .18s ease;
}}
.ct-dash-exp-card:hover {{ transform: translateY(-2px); }}
.ct-dash-exp-status {{
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .4px;
  margin-bottom: 6px;
}}
.ct-dash-exp-status.completed {{ color: {COLORS['green']}; }}
.ct-dash-exp-field {{
  font-size: 11px;
  color: {COLORS['muted']};
  margin-bottom: 3px;
}}
.ct-dash-exp-title {{
  font-size: 15px;
  font-weight: 800;
  color: {COLORS['ink']};
  margin-bottom: 8px;
}}
.ct-dash-exp-skills {{
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}}

/* ===================================================================
   SECTION 5: PROFILE COMPLETION PAGE
   =================================================================== */
.ct-profile-header {{
  padding: 24px 28px 20px;
  background: {COLORS['white']};
  border: 1px solid {COLORS['line']};
  border-radius: 20px;
  box-shadow: {SHADOW};
  margin-bottom: 20px;
  position: relative;
  overflow: hidden;
  direction: {direction};
}}
.ct-profile-header::before {{
  content: "";
  position: absolute;
  inset: 0 0 auto 0;
  height: 4px;
  background: linear-gradient(90deg, {COLORS['turq']}, {COLORS['blue']});
}}
.ct-profile-progress-bar {{
  height: 6px;
  border-radius: 99px;
  background: {COLORS['line']};
  margin-top: 12px;
  overflow: hidden;
}}
.ct-profile-progress-fill {{
  height: 100%;
  border-radius: 99px;
  background: linear-gradient(90deg, {COLORS['blue']}, {COLORS['turq']});
  transition: width .4s ease;
}}
.ct-profile-section {{
  background: {COLORS['white']};
  border: 1px solid {COLORS['line']};
  border-radius: 18px;
  padding: 22px 24px;
  box-shadow: {SHADOW};
  margin-bottom: 14px;
  direction: {direction};
}}
.ct-profile-section-title {{
  font-size: 14px;
  font-weight: 800;
  color: {COLORS['ink']};
  margin: 0 0 14px;
}}

/* ===================================================================
   SECTION 6: FLOATING AI COACH
   =================================================================== */

/* FAB container — fixed at bottom-right */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ct-fab-wrap-marker) {{
  position: fixed !important;
  right: 24px !important;
  bottom: 24px !important;
  z-index: 10000 !important;
  width: 56px !important;
  height: 56px !important;
  border: none !important;
  background: transparent !important;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ct-fab-wrap-marker) > div {{
  width: 56px !important;
  height: 56px !important;
  padding: 0 !important;
  gap: 0 !important;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ct-fab-wrap-marker) > div > div {{
  width: 56px !important;
  height: 56px !important;
  padding: 0 !important;
  gap: 0 !important;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ct-fab-wrap-marker) button {{
  width: 56px !important;
  height: 56px !important;
  min-width: 56px !important;
  border-radius: 50% !important;
  padding: 0 !important;
  font-size: 22px !important;
  background: linear-gradient(135deg, {COLORS['ink']}, {COLORS['blue']}) !important;
  color: #fff !important;
  border: none !important;
  box-shadow: 0 8px 24px -4px rgba(37,99,235,.5) !important;
  white-space: nowrap !important;
  animation: ct-fab-pulse 3.5s ease-in-out infinite !important;
  cursor: pointer !important;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ct-fab-wrap-marker) button:hover {{
  transform: scale(1.07) !important;
  box-shadow: 0 12px 32px -4px rgba(37,99,235,.65) !important;
}}
@keyframes ct-fab-pulse {{
  0%, 100% {{ box-shadow: 0 8px 24px -4px rgba(37,99,235,.45); }}
  50%       {{ box-shadow: 0 8px 32px -4px rgba(37,99,235,.70); }}
}}

/* Coach panel container — fixed above FAB */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ct-coach-panel-marker) {{
  position: fixed !important;
  right: 24px !important;
  bottom: 92px !important;
  width: 400px !important;
  max-height: 560px !important;
  z-index: 9999 !important;
  background: {COLORS['white']} !important;
  border: 1px solid {COLORS['line']} !important;
  border-radius: 22px !important;
  box-shadow: 0 28px 60px -24px rgba(11,27,51,.28) !important;
  overflow: hidden !important;
  direction: {direction} !important;
  animation: ct-coach-fadein .22s ease both !important;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ct-coach-panel-marker) > div {{
  display: flex !important;
  flex-direction: column !important;
  height: 100% !important;
  max-height: 560px !important;
  padding: 0 !important;
  gap: 0 !important;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ct-coach-panel-marker) > div > div {{
  padding: 0 !important;
  gap: 0 !important;
  display: flex !important;
  flex-direction: column !important;
}}
@keyframes ct-coach-fadein {{
  from {{ opacity: 0; transform: translateY(12px); }}
  to   {{ opacity: 1; transform: translateY(0);    }}
}}

/* Coach panel header */
div[data-testid="stVerticalBlock"]:has(.ct-coach-header-marker) {{
  background: linear-gradient(135deg, {COLORS['ink']}, #13294B) !important;
  border-radius: 22px 22px 0 0 !important;
  padding: 12px 16px !important;
  margin: 0 !important;
  width: 100% !important;
}}
div[data-testid="stVerticalBlock"]:has(.ct-coach-header-marker) [data-testid="stHorizontalBlock"] {{
  align-items: center !important;
  gap: 8px !important;
}}
div[data-testid="stVerticalBlock"]:has(.ct-coach-header-marker) .ct-coach-panel-title {{
  font-size: 14px !important;
  font-weight: 800 !important;
  color: #fff !important;
  margin: 0 !important;
}}
/* Minimize / close buttons inside the panel header */
div[data-testid="stVerticalBlock"]:has(.ct-coach-header-marker) button {{
  background: rgba(255,255,255,0.1) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 6px !important;
  width: 28px !important;
  height: 28px !important;
  min-width: 28px !important;
  font-size: 16px !important;
  line-height: 1 !important;
  padding: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer !important;
}}
div[data-testid="stVerticalBlock"]:has(.ct-coach-header-marker) button:hover {{
  background: rgba(255,255,255,0.25) !important;
}}

/* Scrollable messages area */
.ct-chat-msgs {{
  overflow-y: auto;
  padding: 14px 14px 8px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
  max-height: 340px;
  scrollbar-width: thin;
  scrollbar-color: {COLORS['line']} transparent;
  direction: {direction};
}}
.ct-chat-msgs::-webkit-scrollbar {{ width: 4px; }}
.ct-chat-msgs::-webkit-scrollbar-thumb {{ background: {COLORS['line']}; border-radius: 4px; }}

/* Chat message bubbles */
.ct-chat-bubble-ai {{
  background: {COLORS['surface']};
  border: 1px solid {COLORS['line']};
  border-radius: 14px 14px {'14px 4px' if rtl else '4px 14px'};
  padding: 10px 12px;
  font-size: 13px;
  line-height: 1.55;
  color: {COLORS['ink']};
  max-width: 85%;
  align-self: {'flex-end' if rtl else 'flex-start'};
  direction: {direction};
}}
.ct-chat-bubble-user {{
  background: {COLORS['blue']};
  color: #fff;
  border-radius: 14px 14px {'4px 14px' if rtl else '14px 4px'};
  padding: 10px 12px;
  font-size: 13px;
  line-height: 1.55;
  max-width: 80%;
  align-self: {'flex-start' if rtl else 'flex-end'};
  direction: {direction};
}}

/* Coach quick actions */
div[data-testid="stVerticalBlock"]:has(.ct-coach-quick-actions-marker) {{
  padding: 8px 12px !important;
  border-top: 1px solid {COLORS['line']} !important;
  background: {COLORS['surface']} !important;
  direction: {direction} !important;
}}
div[data-testid="stVerticalBlock"]:has(.ct-coach-quick-actions-marker) [data-testid="stHorizontalBlock"] {{
  gap: 6px !important;
}}
div[data-testid="stVerticalBlock"]:has(.ct-coach-quick-actions-marker) button {{
  font-size: 11px !important;
  font-weight: 700 !important;
  color: {COLORS['ink2']} !important;
  background: {COLORS['white']} !important;
  border: 1px solid {COLORS['line']} !important;
  border-radius: 999px !important;
  padding: 4px 10px !important;
  white-space: nowrap !important;
  min-height: 28px !important;
  height: auto !important;
  transition: all .15s ease !important;
  box-shadow: none !important;
}}
div[data-testid="stVerticalBlock"]:has(.ct-coach-quick-actions-marker) button:hover {{
  border-color: {COLORS['turq']} !important;
  color: {COLORS['ink']} !important;
}}

/* Coach input area — styles for the st.form inside the panel */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ct-coach-panel-marker) [data-testid="stForm"] {{
  border: none !important;
  border-top: 1px solid {COLORS['line']} !important;
  padding: 10px 12px !important;
  background: {COLORS['white']} !important;
  margin: 0 !important;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ct-coach-panel-marker) [data-testid="stFormSubmitButton"] button {{
  background: {COLORS['turq']} !important;
  color: #fff !important;
  border: none !important;
  border-radius: 8px !important;
  height: 40px !important;
  padding: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-size: 20px !important;
  transition: background 0.15s ease !important;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ct-coach-panel-marker) [data-testid="stFormSubmitButton"] button:hover {{
  background: {COLORS['blue']} !important;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ct-coach-panel-marker) [data-testid="stTextInput"] input {{
  border-radius: 8px !important;
  border: 1px solid {COLORS['line']} !important;
  padding: 8px 12px !important;
  height: 40px !important;
}}

/* Full-page coach (legacy, kept as safe fallback) */
.ct-coach-container {{
  background: {COLORS['white']};
  border: 1px solid {COLORS['line']};
  border-radius: 20px;
  padding: 0;
  box-shadow: {SHADOW};
  overflow: hidden;
  margin-bottom: 16px;
}}
.ct-coach-header {{
  background: linear-gradient(135deg, {COLORS['ink']}, #13294B);
  padding: 24px 28px;
}}
.ct-coach-header-title {{
  font-size: 20px;
  font-weight: 800;
  color: #fff;
  margin-bottom: 4px;
}}
.ct-coach-header-sub {{
  font-size: 13px;
  color: rgba(255,255,255,.7);
}}
.ct-coach-messages {{
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  direction: {direction};
}}
.ct-coach-msg {{
  padding: 12px 16px;
  border-radius: 16px;
  font-size: 14px;
  line-height: 1.6;
  max-width: 82%;
  direction: {direction};
}}
.ct-coach-msg.ai {{
  background: {COLORS['surface']};
  border: 1px solid {COLORS['line']};
  align-self: {'flex-end' if rtl else 'flex-start'};
  border-radius: 16px 16px {'16px 4px' if rtl else '4px 16px'};
}}
.ct-coach-msg.user {{
  background: {COLORS['blue']};
  color: #fff;
  align-self: {'flex-start' if rtl else 'flex-end'};
  border-radius: 16px 16px {'4px 16px' if rtl else '16px 4px'};
}}

/* ===================================================================
   SECTION 7: SUPPORT PAGE
   =================================================================== */
.ct-support-header {{
  padding: 22px 28px 18px;
  background: {COLORS['white']};
  border: 1px solid {COLORS['line']};
  border-radius: 20px;
  box-shadow: {SHADOW};
  margin-bottom: 20px;
  position: relative;
  overflow: hidden;
  direction: {direction};
}}
.ct-support-header::before {{
  content: "";
  position: absolute;
  inset: 0 0 auto 0;
  height: 4px;
  background: linear-gradient(90deg, {COLORS['blue']}, {COLORS['turq']});
}}
.ct-support-cats {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  margin-bottom: 20px;
}}
.ct-support-cat {{
  background: {COLORS['white']};
  border: 1px solid {COLORS['line']};
  border-radius: 18px;
  padding: 20px;
  box-shadow: {SHADOW};
  text-align: center;
  transition: transform .18s ease, border-color .18s ease;
  cursor: default;
  direction: {direction};
}}
.ct-support-cat:hover {{
  transform: translateY(-2px);
  border-color: rgba(37,99,235,.25);
}}
.ct-support-cat-icon {{
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: rgba(37,99,235,.07);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: {COLORS['blue']};
  font-size: 20px;
  margin-bottom: 10px;
}}
.ct-support-cat-title {{
  font-size: 14px;
  font-weight: 800;
  color: {COLORS['ink']};
  margin: 0 0 6px;
}}
.ct-support-cat-items {{
  font-size: 12px;
  color: {COLORS['muted']};
  line-height: 1.6;
}}
.ct-support-form-card {{
  background: {COLORS['white']};
  border: 1px solid {COLORS['line']};
  border-radius: 20px;
  padding: 28px;
  box-shadow: {SHADOW};
  direction: {direction};
}}
.ct-support-team-row {{
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 22px;
  direction: {direction};
}}
.ct-support-team-icon {{
  width: 50px;
  height: 50px;
  border-radius: 15px;
  background: linear-gradient(135deg, {COLORS['blue']}, {COLORS['turq']});
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  color: #fff;
  flex-shrink: 0;
}}
.ct-support-team-name {{
  font-size: 16px;
  font-weight: 800;
  color: {COLORS['ink']};
}}
.ct-support-team-sub {{
  font-size: 12px;
  color: {COLORS['muted']};
  margin-top: 2px;
}}

/* ===================================================================
   SECTION 8: FUTURE MAP + PROGRESS (existing — preserved)
   =================================================================== */
.ct-future-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
}}
.ct-future-card {{
  background: {COLORS['white']};
  border: 1px solid {COLORS['line']};
  border-radius: 20px;
  padding: 20px;
  box-shadow: {SHADOW};
  transition: transform .18s ease, box-shadow .18s ease;
  cursor: default;
}}
.ct-future-card:hover {{
  transform: translateY(-3px);
  box-shadow: {SHADOW_LG};
}}
.ct-future-card.preferred {{ background: rgba(37,99,235,.04);  border-color: rgba(37,99,235,.2);  }}
.ct-future-card.probable  {{ background: rgba(15,181,176,.04); border-color: rgba(15,181,176,.2); }}
.ct-future-card.plausible {{ background: rgba(240,160,42,.04); border-color: rgba(240,160,42,.2); }}
.ct-future-card.possible  {{ background: rgba(124,92,255,.04); border-color: rgba(124,92,255,.2); }}
.ct-future-tag {{
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .5px;
  color: {COLORS['muted']};
  margin-bottom: 6px;
}}
.ct-future-title {{
  font-size: 16px;
  font-weight: 800;
  color: {COLORS['ink']};
  margin: 0 0 6px;
}}
.ct-future-match {{
  font-size: 13px;
  color: {COLORS['muted']};
  margin: 0 0 8px;
}}
.ct-future-bar-wrap {{
  height: 8px;
  border-radius: 99px;
  background: {COLORS['line']};
  overflow: hidden;
  margin-bottom: 10px;
}}
.ct-future-bar-fill {{
  height: 100%;
  border-radius: 99px;
  background: linear-gradient(90deg, {COLORS['blue']}, {COLORS['turq']});
}}
.ct-future-skills {{
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}}
.ct-prog-section {{
  margin-bottom: 24px;
}}
.ct-prog-bar-wrap {{
  height: 10px;
  border-radius: 99px;
  background: {COLORS['line']};
  overflow: hidden;
  margin: 6px 0;
}}
.ct-prog-bar-fill {{
  height: 100%;
  border-radius: 99px;
  background: linear-gradient(90deg, {COLORS['blue']}, {COLORS['turq']});
  transition: width .6s ease;
}}

/* ===================================================================
   SECTION 9: SHARED ATOMS
   =================================================================== */
.ct-h2 {{
  font-size: 19px;
  font-weight: 800;
  color: {COLORS['ink']};
  margin: 0 0 14px;
  direction: {direction};
}}
.ct-h3 {{
  font-size: 16px;
  font-weight: 800;
  color: {COLORS['ink']};
  margin: 0 0 8px;
}}
.ct-eyebrow {{
  display: inline-block;
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .6px;
  color: {COLORS['blue']};
  background: rgba(37,99,235,.08);
  border-radius: 999px;
  padding: 3px 10px;
  margin-bottom: 10px;
}}
.ct-title {{
  font-size: 24px;
  font-weight: 800;
  color: {COLORS['ink']};
  line-height: 1.25;
  margin: 0 0 6px;
}}
.ct-lede {{
  font-size: 14px;
  color: {COLORS['muted']};
  line-height: 1.65;
  margin: 0;
}}
.ct-muted {{
  color: {COLORS['muted']};
}}
.ct-note {{
  font-size: 12px;
  color: {COLORS['muted']};
  background: {COLORS['surface']};
  border: 1px solid {COLORS['line']};
  border-radius: 10px;
  padding: 10px 14px;
  line-height: 1.6;
}}
.ct-chip {{
  display: inline-block;
  background: {COLORS['surface']};
  border: 1px solid {COLORS['line']};
  border-radius: 999px;
  padding: 2px 10px;
  font-size: 11px;
  font-weight: 700;
  color: {COLORS['ink2']};
  white-space: nowrap;
}}
.ct-hero-landing {{
  text-align: center;
  padding: 32px 16px 16px;
}}
.ct-hero-logo {{
  height: 72px;
  width: auto;
  object-fit: contain;
  margin: 0 auto 12px;
  display: block;
}}
.ct-hero-logo-fallback {{
  margin: 0 auto 16px;
  text-align: center;
}}

/* ===================================================================
   SECTION 10: ANIMATIONS
   =================================================================== */
@keyframes ct-dash-pulse {{
  0%, 100% {{ opacity: 1; transform: scale(1); }}
  50%       {{ opacity: .8; transform: scale(1.06); }}
}}
@keyframes ct-dash-fadeup {{
  from {{ opacity: 0; transform: translateY(16px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}

/* ===================================================================
   SECTION 11: RESPONSIVE
   =================================================================== */
@media (max-width: 860px) {{
  .ct-dash-metrics {{ grid-template-columns: 1fr 1fr; }}
  .ct-support-cats {{ grid-template-columns: 1fr; }}
  div[data-testid="stVerticalBlockBorderWrapper"]:has(.ct-coach-panel-marker) {{ width: calc(100vw - 48px) !important; right: 16px !important; }}
  div[data-testid="stVerticalBlockBorderWrapper"]:has(.ct-fab-wrap-marker) {{ right: 16px !important; }}
}}
@media (max-width: 600px) {{
  .ct-dash-greeting {{ font-size: 20px; }}
  .ct-dash-metrics {{ grid-template-columns: 1fr 1fr; gap: 10px; }}
  .ct-future-grid  {{ grid-template-columns: 1fr; }}
  .ct-dash-exp-grid {{ grid-template-columns: 1fr; }}
  .ct-dash-rec-grid {{ grid-template-columns: 1fr; }}
  .ct-dash-road-node {{ min-width: 70px; }}
  .ct-navrow {{ padding-bottom: 8px; }}
}}
</style>
""",
        unsafe_allow_html=True,
    )
