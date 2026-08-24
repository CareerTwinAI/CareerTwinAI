# -*- coding: utf-8 -*-
"""My Progress — meaningful metrics from actual user activity.

All values are derived from st.session_state, never fabricated.
"""

# pyrefly: ignore [missing-import]
import streamlit as st

from utils.styles import COLORS


def page_my_progress(data: dict, ui: dict, lang: str) -> None:
    """Render the My Progress page."""
    title = "تقدّمي" if lang == "ar" else "My Progress"
    subtitle = ("شاهد ما أكملته وكيف تتطور مهاراتك مع كل تجربة."
                if lang == "ar"
                else "See what you've completed and how your skills develop with every experience.")

    st.markdown(
        f"<div class='ct-h2'>{title}</div>"
        f"<p class='ct-muted' style='margin-bottom:16px'>{subtitle}</p>",
        unsafe_allow_html=True,
    )

    history = st.session_state.get("experience_history", [])
    completed = list({e["position_id"] for e in history if e.get("position_id")})
    fields_explored = list({e["field_id"] for e in history if e.get("field_id")})

    if not history:
        # Empty state
        st.markdown(
            f"<div class='ct-dash-empty'>"
            f"<div class='ct-dash-empty-icon'>📊</div>"
            f"<div class='ct-dash-empty-msg'>"
            f"{'رحلتك المهنية تبدأ بأول تجربة.' if lang == 'ar' else 'Your career journey starts with your first experience.'}"
            f"</div></div>",
            unsafe_allow_html=True,
        )
        st.button(
            "استكشف المجالات" if lang == "ar" else "Explore Careers",
            type="primary", width="stretch",
            on_click=lambda: _go("fields"),
        )
        return

    # Summary metrics
    total_positions = sum(len(f.get("positions", [])) for f in data.get("fields", []))
    total_fields = len(data.get("fields", []))

    scores = [e.get("score") for e in history if e.get("score") is not None]
    avg_score = round(sum(scores) / len(scores)) if scores else 0
    best_score = max(scores) if scores else 0

    cards_html = "<div class='ct-prog-grid'>"

    # Experiences completed
    cards_html += _metric_card(
        "التجارب المكتملة" if lang == "ar" else "Experiences Completed",
        f"{len(completed)}" + (f" {'من' if lang == 'ar' else 'of'} {total_positions}" if total_positions else ""),
        min(100, round(len(completed) / max(1, total_positions) * 100)),
        "من إجمالي الوظائف المتاحة" if lang == "ar" else "of total available positions",
    )

    # Fields explored
    cards_html += _metric_card(
        "المجالات المُستكشفة" if lang == "ar" else "Fields Explored",
        f"{len(fields_explored)}" + (f" {'من' if lang == 'ar' else 'of'} {total_fields}" if total_fields else ""),
        min(100, round(len(fields_explored) / max(1, total_fields) * 100)),
        "من إجمالي المجالات المتاحة" if lang == "ar" else "of total available fields",
    )

    # Average compatibility
    cards_html += _metric_card(
        "متوسط التوافق" if lang == "ar" else "Average Compatibility",
        f"{avg_score}٪",
        avg_score,
        "متوسط نتائج جميع التجارب" if lang == "ar" else "average across all experiences",
    )

    # Best result
    cards_html += _metric_card(
        "أفضل نتيجة" if lang == "ar" else "Best Result",
        f"{best_score}٪",
        best_score,
        "أعلى مؤشر توافق حققته" if lang == "ar" else "highest compatibility score achieved",
    )

    cards_html += "</div>"
    st.markdown(cards_html, unsafe_allow_html=True)

    # Detailed experience history
    st.markdown(
        f"<div class='ct-h3' style='margin-top:22px'>"
        f"{'سجل التجارب' if lang == 'ar' else 'Experience History'}</div>",
        unsafe_allow_html=True,
    )

    for exp in reversed(history):
        fld = next((f for f in data["fields"] if f["id"] == exp.get("field_id")), None)
        pos = None
        if fld:
            pos = next((p for p in fld["positions"] if p["id"] == exp.get("position_id")), None)
        if not pos:
            continue

        score = exp.get("score", 0)
        skills = exp.get("top_skills", [])
        skills_html = "".join(f"<span class='ct-chip'>{s}</span>" for s in skills[:3])

        st.markdown(
            f"<div class='ct-card' style='margin-bottom:10px'>"
            f"<div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px'>"
            f"<div>"
            f"<div class='ct-h3' style='margin:0'>{pos['title'][lang]}</div>"
            f"<div class='ct-muted' style='font-size:12px'>{fld['name'][lang]}</div>"
            f"</div>"
            f"<div class='ct-band' style='font-size:14px'>{score}٪</div>"
            f"</div>"
            f"<div style='margin-top:8px'>{skills_html}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # How metrics are calculated
    with st.expander("كيف تُحسب هذه المقاييس؟" if lang == "ar" else "How are these metrics calculated?"):
        explanation = (
            "كل مقياس مبني على بياناتك الفعلية في المنصة:\n\n"
            "• **التجارب المكتملة**: عدد التجارب المهنية التي أكملت فيها المواقف الثلاثة.\n"
            "• **المجالات المُستكشفة**: عدد المجالات التي جربت فيها وظيفة واحدة على الأقل.\n"
            "• **متوسط التوافق**: المتوسط الحسابي لنتائج جميع تجاربك.\n"
            "• **أفضل نتيجة**: أعلى مؤشر توافق حققته في أي تجربة."
            if lang == "ar" else
            "Every metric is built from your actual platform data:\n\n"
            "• **Experiences Completed**: Number of career experiences where you completed all three scenarios.\n"
            "• **Fields Explored**: Number of fields where you tried at least one position.\n"
            "• **Average Compatibility**: Arithmetic mean of all your experience scores.\n"
            "• **Best Result**: Highest compatibility score achieved in any experience."
        )
        st.markdown(explanation)


def _metric_card(title: str, value: str, pct: int, hint: str) -> str:
    return (
        f"<div class='ct-prog-card'>"
        f"<div class='ct-prog-card-title'>{title}</div>"
        f"<div style='font-size:24px;font-weight:800;color:{COLORS['ink']};margin:6px 0'>{value}</div>"
        f"<div class='ct-prog-bar'>"
        f"<div class='ct-prog-bar-fill' style='width:{min(100, max(0, pct))}%'></div>"
        f"</div>"
        f"<div class='ct-prog-card-sub'>{hint}</div>"
        f"</div>"
    )


def _go(page: str) -> None:
    st.session_state.current_page = page
