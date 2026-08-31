import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# =========================================================
# 페이지 설정 (메인 app.py와 동일한 설정)
# =========================================================
st.set_page_config(
    page_title="우리 반 MBTI 조사 | 진로 나침반",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 세션 상태 초기화 (메인과 동일한 기본값)
# =========================================================
defaults = {
    "dark_mode": False,
    "favorites": [],
    "custom_jobs": [],
    "recommended_jobs": [],
    "last_profile": {
        "mbti": "INTJ",
        "interests": [],
        "aptitudes": [],
        "subjects": []
    }
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

if "class_counts" not in st.session_state:
    st.session_state.class_counts = {}


# =========================================================
# 디자인 및 다크 모드 CSS (메인 app.py와 동일)
# =========================================================
def apply_custom_css():
    if st.session_state.dark_mode:
        bg = "#111827"
        surface = "#1F2937"
        surface2 = "#273449"
        text = "#F9FAFB"
        subtext = "#CBD5E1"
        border = "#3A4A60"
        primary = "#818CF8"
        primary_dark = "#6366F1"
        input_bg = "#1F2937"
        hero1 = "#312E81"
        hero2 = "#1D4ED8"
    else:
        bg = "#F5F7FB"
        surface = "#FFFFFF"
        surface2 = "#F8FAFC"
        text = "#172033"
        subtext = "#64748B"
        border = "#E2E8F0"
        primary = "#4F46E5"
        primary_dark = "#3730A3"
        input_bg = "#FFFFFF"
        hero1 = "#4338CA"
        hero2 = "#2563EB"

    css = f"""
    <style>
        .stApp {{ background: {bg}; color: {text}; }}
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        header[data-testid="stHeader"] {{ background: transparent; }}
        .block-container {{ max-width: 1250px; padding-top: 2rem; padding-bottom: 3rem; }}
        h1, h2, h3, h4, p, label, span, div {{ color: {text}; }}
        [data-testid="stSidebar"] {{ background: {surface}; border-right: 1px solid {border}; }}
        [data-testid="stSidebar"] .stMarkdown p {{ color: {subtext}; }}
        .stTextInput input, .stTextArea textarea,
        .stSelectbox > div > div, .stMultiSelect > div > div {{
            background-color: {input_bg} !important;
            color: {text} !important;
            border-color: {border} !important;
            border-radius: 10px !important;
        }}
        [data-baseweb="select"] * {{ color: {text}; }}
        .stButton > button, .stDownloadButton > button {{
            border-radius: 10px; border: 1px solid {border};
            font-weight: 700; transition: 0.2s;
        }}
        .stButton > button:hover, .stDownloadButton > button:hover {{
            border-color: {primary}; color: {primary}; transform: translateY(-1px);
        }}
        [data-testid="stExpander"] {{
            background: {surface}; border: 1px solid {border};
            border-radius: 14px; margin-bottom: 12px;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
        }}
        [data-testid="stExpander"] details summary {{ font-size: 1.05rem; font-weight: 700; }}
        [data-testid="stAlert"] {{ border-radius: 12px; }}
        hr {{ border-color: {border}; }}
        .hero {{
            background: linear-gradient(135deg, {hero1}, {hero2});
            border-radius: 22px; padding: 38px 42px; margin-bottom: 26px;
            color: white !important; box-shadow: 0 16px 35px rgba(49, 46, 129, 0.22);
        }}
        .hero h1 {{ color: white !important; font-size: 2.5rem; margin: 0 0 8px 0; }}
        .hero p {{ color: #E0E7FF !important; font-size: 1.05rem; margin: 0; }}
        .section-title {{ font-size: 1.55rem; font-weight: 800; margin: 12px 0 5px; color: {text}; }}
        .section-subtitle {{ color: {subtext} !important; margin-bottom: 20px; }}
        .stat-card {{
            background: {surface}; border: 1px solid {border}; border-radius: 16px;
            padding: 18px 20px; min-height: 110px; box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
        }}
        .stat-number {{ font-size: 1.7rem; font-weight: 800; color: {primary} !important; }}
        .stat-label {{ color: {subtext} !important; font-size: 0.9rem; }}
        .footer-note {{ color: {subtext} !important; font-size: 0.88rem; text-align: center; padding: 30px 0 5px; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


apply_custom_css()

if st.session_state.dark_mode:
    CHART_BG, CHART_TEXT, CHART_GRID = "#1F2937", "#F9FAFB", "#3A4A60"
else:
    CHART_BG, CHART_TEXT, CHART_GRID = "#FFFFFF", "#172033", "#E2E8F0"


# =========================================================
# 사이드바 (메인과 동일)
# =========================================================
with st.sidebar:
    st.markdown("## 🧭 진로 나침반")
    st.caption("나의 성향에서 시작하는 진로 탐색")
    st.divider()

    dark_mode = st.toggle("🌙 다크 모드", value=st.session_state.dark_mode)
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()

    st.divider()
    st.markdown("### ⭐ 즐겨찾기 현황")
    st.metric("저장한 직업", f"{len(st.session_state.favorites)}개")

    st.divider()
    st.markdown("### 학습 안내")
    st.caption(
        "MBTI는 진로를 결정하는 검사 결과가 아닙니다. "
        "흥미, 적성, 가치관, 경험을 함께 고려하며 직업을 탐색해 보세요."
    )


# =========================================================
# 헤더
# =========================================================
st.markdown(
    """
    <div class="hero">
        <h1>🧑‍🤝‍🧑 우리 반 MBTI 조사</h1>
        <p>직접 우리 반(또는 우리 학교) 친구들의 MBTI를 입력하고, 전국 참고 통계와 비교해 보세요.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "3번째 페이지는 제가 하나 골라봤어요. 1·2번 페이지가 '남이 만든 통계'를 보여준다면, "
    "이 페이지는 **우리 반 학생들이 직접 데이터를 모아 스스로 통계를 만들어보는 활동**이에요. "
    "탐구 활동이나 발표 자료로 활용하기 좋습니다."
)
st.markdown("---")

TYPES = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ",
]

# 1번 페이지와 같은 참고용 전국 비율 (비공식 참고 자료)
NATIONAL = {
    "ISTJ": 25, "ESTJ": 15, "ISTP": 9, "ISFJ": 8,
    "ISFP": 7, "ESFJ": 6, "ESFP": 5, "ESTP": 5,
    "INTJ": 4, "ENFP": 4, "INTP": 3, "INFP": 3,
    "INFJ": 2, "ENTP": 2, "ENTJ": 2, "ENFJ": 1,
}

if not st.session_state.class_counts:
    st.session_state.class_counts = {t: 0 for t in TYPES}

# =========================================================
# 입력 방식 선택
# =========================================================
input_mode = st.radio(
    "입력 방식을 선택하세요",
    ["🔢 유형별 인원 직접 입력", "📋 명단 붙여넣기 (예: ISTJ, ENFP, ...)"],
    horizontal=True,
)

if input_mode == "🔢 유형별 인원 직접 입력":
    st.markdown('<div class="section-title">유형별 인원 수를 입력하세요</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, t in enumerate(TYPES):
        with cols[i % 4]:
            st.session_state.class_counts[t] = st.number_input(
                t, min_value=0, max_value=200,
                value=st.session_state.class_counts.get(t, 0),
                key=f"num_{t}",
            )
else:
    st.markdown('<div class="section-title">친구들의 MBTI를 쉼표(,) 또는 줄바꿈으로 구분해 붙여넣으세요</div>', unsafe_allow_html=True)
    pasted = st.text_area(
        "예시: ISTJ, ENFP, INFP, ISTJ, ESTJ ...", height=140,
        placeholder="ISTJ, ENFP, INFP, ISTJ, ESTJ",
    )
    if pasted.strip():
        raw = pasted.replace("\n", ",").split(",")
        counts = {t: 0 for t in TYPES}
        unknown = []
        for item in raw:
            token = item.strip().upper()
            if not token:
                continue
            if token in counts:
                counts[token] += 1
            else:
                unknown.append(token)
        st.session_state.class_counts = counts
        if unknown:
            st.warning(f"인식하지 못한 값은 제외했어요: {', '.join(set(unknown))}")

total = sum(st.session_state.class_counts.values())

st.markdown("---")

if total == 0:
    st.info("아직 입력된 데이터가 없어요. 위에서 우리 반 친구들의 MBTI를 입력해 주세요.")
else:
    class_df = pd.DataFrame(
        {"유형": TYPES, "인원수": [st.session_state.class_counts[t] for t in TYPES]}
    )
    class_df["우리 반 비율(%)"] = (class_df["인원수"] / total * 100).round(1)
    class_df["전국 참고 비율(%)"] = class_df["유형"].map(NATIONAL)
    class_df = class_df.sort_values("인원수", ascending=False).reset_index(drop=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="stat-card"><div class="stat-number">{total}명</div>
        <div class="stat-label">조사 인원</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="stat-card"><div class="stat-number">{class_df.iloc[0]['유형']}</div>
        <div class="stat-label">우리 반 최다 유형 ({class_df.iloc[0]['우리 반 비율(%)']}%)</div></div>""", unsafe_allow_html=True)

    diff_df = class_df.copy()
    diff_df["차이"] = diff_df["우리 반 비율(%)"] - diff_df["전국 참고 비율(%)"]
    biggest_gap = diff_df.reindex(diff_df["차이"].abs().sort_values(ascending=False).index).iloc[0]
    with c3:
        st.markdown(f"""<div class="stat-card"><div class="stat-number">{biggest_gap['유형']}</div>
        <div class="stat-label">전국 대비 가장 큰 차이 ({biggest_gap['차이']:+.1f}%p)</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 우리 반 vs 전국 참고 비율</div>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=class_df["유형"], y=class_df["우리 반 비율(%)"],
        name="우리 반", marker_color="#10b981",
    ))
    fig.add_trace(go.Bar(
        x=class_df["유형"], y=class_df["전국 참고 비율(%)"],
        name="전국 참고 비율", marker_color="#4f46e5", opacity=0.55,
    ))
    fig.update_layout(
        barmode="group", height=450,
        yaxis_title="비율(%)", xaxis_title="MBTI 유형",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        plot_bgcolor=CHART_BG, paper_bgcolor=CHART_BG, font_color=CHART_TEXT,
    )
    fig.update_xaxes(gridcolor=CHART_GRID)
    fig.update_yaxes(gridcolor=CHART_GRID)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 표로 자세히 보기"):
        st.dataframe(
            class_df[["유형", "인원수", "우리 반 비율(%)", "전국 참고 비율(%)"]],
            hide_index=True, use_container_width=True,
        )

    csv = class_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "📥 우리 반 조사 결과 CSV로 저장", data=csv,
        file_name="우리반_MBTI_조사결과.csv", mime="text/csv",
    )

    st.info(
        "💡 **탐구 활동 아이디어**: 우리 반 결과가 전국 참고 비율과 크게 다른 유형이 있다면, "
        "그 이유를 친구들과 이야기해 보세요. (예: 표본 크기, 학급 특성, 진로 희망 분야 등)"
    )

st.markdown(
    '<div class="footer-note">MBTI 결과는 진로 탐색의 출발점입니다. '
    '관심 직업의 실제 업무, 관련 학과, 필요한 역량을 추가로 조사해 보세요.</div>',
    unsafe_allow_html=True,
)
