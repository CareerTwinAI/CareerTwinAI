# -*- coding: utf-8 -*-
"""My Future — dynamic future map with four exploratory categories.

Preferred / Probable / Plausible / Possible futures are derived from
actual profile data and completed experiences, not hardcoded values.
"""

# pyrefly: ignore [missing-import]
import streamlit as st

from utils.styles import COLORS


# ------------------------------------------------------------------ #
#  Future data builder                                                #
# ------------------------------------------------------------------ #

def _build_futures(data: dict, lang: str) -> list:
    """Build the four future categories from actual user activity."""
    s = st.session_state
    profile = s.get("student_profile", {})
    interests = profile.get("interests", [])
    history = s.get("experience_history", [])
    rec_fields = s.get("recommended_fields", [])
    selected = s.get("selected_field")

    fields = data.get("fields", [])
    futures = []

    # Preferred: what the student currently wants (selected or first recommended)
    preferred_id = selected or (rec_fields[0] if rec_fields else None)
    if preferred_id:
        fld = next((f for f in fields if f["id"] == preferred_id), None)
        if fld:
            # Calculate proximity from completed positions in this field
            field_exps = [e for e in history if e.get("field_id") == preferred_id]
            pct = max((e.get("score", 0) for e in field_exps), default=0) if field_exps else 0
            futures.append({
                "type": "preferred",
                "title": fld["name"][lang],
                "desc": ("المستقبل الذي تريده الآن. يعكس طموحك واختيارك الشخصي."
                         if lang == "ar"
                         else "The future you want most right now. It reflects your personal ambition."),
                "pct": pct,
                "tooltip": ("يعكس اختيارك الحالي — وليس تنبؤاً." if lang == "ar"
                            else "Reflects your current choice — not a prediction."),
            })

    # Probable: based on current interests and activity
    if rec_fields and len(rec_fields) > 0:
        prob_id = rec_fields[0] if rec_fields[0] != preferred_id else (rec_fields[1] if len(rec_fields) > 1 else None)
        if prob_id:
            fld = next((f for f in fields if f["id"] == prob_id), None)
            if fld:
                field_exps = [e for e in history if e.get("field_id") == prob_id]
                pct = max((e.get("score", 0) for e in field_exps), default=0) if field_exps else 0
                futures.append({
                    "type": "probable",
                    "title": fld["name"][lang],
                    "desc": ("المستقبل الأكثر احتمالاً إذا استمر اتجاهك الحالي."
                             if lang == "ar"
                             else "The future most likely if your current direction continues."),
                    "pct": pct,
                    "tooltip": ("بناء على اهتماماتك وأنشطتك الحالية." if lang == "ar"
                                else "Based on your current interests and activities."),
                })

    # Plausible: realistic adjacent options based on skills
    if len(rec_fields) > 2:
        plaus_id = rec_fields[2]
        fld = next((f for f in fields if f["id"] == plaus_id), None)
        if fld:
            futures.append({
                "type": "plausible",
                "title": fld["name"][lang],
                "desc": ("مستقبل واقعي يناسب مهاراتك ومعرفتك الحالية."
                         if lang == "ar"
                         else "A realistic future that fits your current skills and knowledge."),
                "pct": 0,
                "tooltip": ("خيار واقعي بناء على ما لديك." if lang == "ar"
                            else "A realistic option based on what you have."),
            })

    # Possible: new paths through learning
    # Pick a field not yet recommended
    explored_ids = set(rec_fields) | {selected} if selected else set(rec_fields)
    possible_field = next((f for f in fields if f["id"] not in explored_ids), None)
    if possible_field:
        futures.append({
            "type": "possible",
            "title": possible_field["name"][lang],
            "desc": ("مسار يمكنك فتحه من خلال تعلم مهارات جديدة واكتساب تجارب."
                     if lang == "ar"
                     else "A path you could open by developing new skills and gaining experience."),
            "pct": 0,
            "tooltip": ("مسار استكشافي يمكنك فتحه — وليس تنبؤاً." if lang == "ar"
                        else "An exploratory path you could open — not a prediction."),
        })

    return futures


# ------------------------------------------------------------------ #
#  Page renderer                                                      #
# ------------------------------------------------------------------ #

def page_my_future(data: dict, ui: dict, lang: str) -> None:
    """Render the My Future page."""
    title = "مستقبلي" if lang == "ar" else "My Future"
    subtitle = ("كل مستقبل يمثل علاقة مختلفة بين مكانك اليوم وأين يمكنك أن تصل."
                if lang == "ar"
                else "Each future represents a different relationship between where you are today and where you could go.")

    st.markdown(
        f"<div class='ct-h2'>{title}</div>"
        f"<p class='ct-muted' style='margin-bottom:16px'>{subtitle}</p>",
        unsafe_allow_html=True,
    )

    futures = _build_futures(data, lang)

    if not futures:
        # Empty state
        st.markdown(
            f"<div class='ct-dash-empty'>"
            f"<div class='ct-dash-empty-icon'>◇</div>"
            f"<div class='ct-dash-empty-msg'>"
            f"{'أكمل ملفك السريع حتى يبدأ توأمك المهني في بناء خارطة مستقبلك.' if lang == 'ar' else 'Complete your quick profile so CareerTwin can begin building your future map.'}"
            f"</div></div>",
            unsafe_allow_html=True,
        )
        st.button(
            "أكمل ملفي" if lang == "ar" else "Complete My Profile",
            type="primary", width="stretch",
            on_click=lambda: _go("profile"),
        )
        return

    # Render future cards
    type_icons = {"preferred": "★", "probable": "→", "plausible": "◇", "possible": "✦"}
    type_labels_ar = {"preferred": "المستقبل المفضل", "probable": "المستقبل المرجح",
                      "plausible": "المستقبل الواقعي", "possible": "المستقبل الممكن"}
    type_labels_en = {"preferred": "Preferred Future", "probable": "Probable Future",
                      "plausible": "Plausible Future", "possible": "Possible Future"}
    type_labels = type_labels_ar if lang == "ar" else type_labels_en

    cards_html = "<div class='ct-future-grid'>"
    for future in futures:
        ftype = future["type"]
        icon = type_icons.get(ftype, "◇")
        label = type_labels.get(ftype, "")
        pct = future["pct"]
        pct_str = f"{pct}٪" if pct > 0 else ("—" if lang == "ar" else "—")

        bar_html = ""
        if pct > 0:
            bar_html = (
                f"<div class='ct-future-bar'>"
                f"<div class='ct-future-bar-fill' style='width:{min(100, pct)}%'></div>"
                f"</div>"
            )

        cards_html += (
            f"<div class='ct-future-card {ftype}'>"
            f"<div class='ct-future-tag'>{icon} {label}</div>"
            f"<div class='ct-future-title'>{future['title']}</div>"
            f"<div class='ct-future-desc'>{future['desc']}</div>"
            f"{bar_html}"
            f"<div class='ct-future-tooltip'>{future['tooltip']}</div>"
            f"</div>"
        )
    cards_html += "</div>"
    st.markdown(cards_html, unsafe_allow_html=True)

    # Guidance note
    st.markdown(
        f"<div class='ct-note' style='margin-top:18px'>"
        f"{'هذه الاتجاهات إرشادية وتتطور مع كل تجربة تكملها. لا تمثل تنبؤات مضمونة.' if lang == 'ar' else 'These directions are exploratory guidance that evolve with every experience you complete. They are not guaranteed predictions.'}"
        f"</div>",
        unsafe_allow_html=True,
    )


def _go(page: str) -> None:
    st.session_state.current_page = page
