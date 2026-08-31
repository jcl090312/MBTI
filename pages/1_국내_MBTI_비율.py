import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# 페이지 설정 (메인 app.py와 동일한 설정)
# =========================================================
st.set_page_config(
    page_title="국내 MBTI 비율 | 진로 나침반",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 세션 상태 초기화 (메인과 동일한 기본값)
# 다른 페이지를 거치지 않고 이 페이지로 바로 들어와도
# 오류가 나지 않도록 동일하게 초기화합니다.
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

# 차트에 쓸 색상 (다크모드 여부에 따라 자동 전환)
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
        <h1>🇰🇷 국내 MBTI 유형 비율</h1>
        <p>우리나라에서 알려진 MBTI 16가지 유형별 비율을 그래프로 살펴봅니다.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# 데이터
# 인터넷에 널리 알려진 비공식 참고 통계입니다.
# (정식 MBTI 검사 기관의 공식 인구 통계가 아니며, 표본과 시기에 따라
#  차이가 크므로 '흐름을 살펴보기 위한 참고 자료'로만 활용하세요.)
# =========================================================
data = {
    "ISTJ": 25, "ESTJ": 15, "ISTP": 9, "ISFJ": 8,
    "ISFP": 7, "ESFJ": 6, "ESFP": 5, "ESTP": 5,
    "INTJ": 4, "ENFP": 4, "INTP": 3, "INFP": 3,
    "INFJ": 2, "ENTP": 2, "ENTJ": 2, "ENFJ": 1,
}

group_map = {
    "ISTJ": "SJ", "ISFJ": "SJ", "ESTJ": "SJ", "ESFJ": "SJ",
    "ISTP": "SP", "ISFP": "SP", "ESTP": "SP", "ESFP": "SP",
    "INFJ": "NF", "INFP": "NF", "ENFJ": "NF", "ENFP": "NF",
    "INTJ": "NT", "INTP": "NT", "ENTJ": "NT", "ENTP": "NT",
}
group_color = {"SJ": "#4f46e5", "SP": "#f59e0b", "NF": "#10b981", "NT": "#ef4444"}

df = pd.DataFrame({"유형": list(data.keys()), "비율(%)": list(data.values())})
df["기질"] = df["유형"].map(group_map)
df = df.sort_values("비율(%)", ascending=False).reset_index(drop=True)

st.caption(
    "출처: 온라인에 널리 알려진 국내 MBTI 비율 참고 자료 (비공식 통계, 표본에 따라 수치가 달라질 수 있음)"
)

# =========================================================
# 요약 카드
# =========================================================
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="stat-card"><div class="stat-number">{df.iloc[0]['유형']}</div>
    <div class="stat-label">가장 흔한 유형 ({df.iloc[0]['비율(%)']}%)</div></div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="stat-card"><div class="stat-number">{df.iloc[-1]['유형']}</div>
    <div class="stat-label">가장 희귀한 유형 ({df.iloc[-1]['비율(%)']}%)</div></div>""", unsafe_allow_html=True)
with c3:
    sj_sum = df[df['기질']=='SJ']['비율(%)'].sum()
    st.markdown(f"""<div class="stat-card"><div class="stat-number">{sj_sum}%</div>
    <div class="stat-label">SJ(관리자) 계열 합</div></div>""", unsafe_allow_html=True)
with c4:
    nf_sum = df[df['기질']=='NF']['비율(%)'].sum()
    st.markdown(f"""<div class="stat-card"><div class="stat-number">{nf_sum}%</div>
    <div class="stat-label">NF(외교관) 계열 합</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# =========================================================
# 막대 그래프 (전체 16유형)
# =========================================================
st.markdown('<div class="section-title">📊 16개 유형별 비율</div>', unsafe_allow_html=True)

fig_bar = px.bar(
    df, x="유형", y="비율(%)", color="기질",
    color_discrete_map=group_color, text="비율(%)",
    category_orders={"유형": df["유형"].tolist()},
)
fig_bar.update_traces(texttemplate="%{text}%", textposition="outside")
fig_bar.update_layout(
    yaxis_title="비율 (%)", xaxis_title="MBTI 유형",
    plot_bgcolor=CHART_BG, paper_bgcolor=CHART_BG,
    font_color=CHART_TEXT, height=460, legend_title="기질 그룹",
)
fig_bar.update_xaxes(gridcolor=CHART_GRID)
fig_bar.update_yaxes(gridcolor=CHART_GRID)
st.plotly_chart(fig_bar, use_container_width=True)

# =========================================================
# 기질(temperament) 그룹 도넛 + 순위표
# =========================================================
left, right = st.columns([1, 1])

with left:
    st.markdown('<div class="section-title">🍩 기질 그룹별 비중</div>', unsafe_allow_html=True)
    group_df = df.groupby("기질", as_index=False)["비율(%)"].sum()
    fig_donut = go.Figure(
        data=[go.Pie(
            labels=group_df["기질"], values=group_df["비율(%)"], hole=0.55,
            marker=dict(colors=[group_color[g] for g in group_df["기질"]]),
        )]
    )
    fig_donut.update_layout(
        height=380, showlegend=True,
        paper_bgcolor=CHART_BG, font_color=CHART_TEXT,
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with right:
    st.markdown('<div class="section-title">📋 순위표</div>', unsafe_allow_html=True)
    show_df = df[["유형", "비율(%)", "기질"]].copy()
    show_df.insert(0, "순위", range(1, len(show_df) + 1))
    st.dataframe(show_df, hide_index=True, use_container_width=True, height=420)

st.info(
    "💡 **참고**: 위 수치는 정식 심리검사 기관의 공식 인구 통계가 아니라 온라인에서 "
    "널리 공유되는 비공식 자료입니다. 조사 시점·방식에 따라 실제 비율은 달라질 수 있으니, "
    "'절대적인 사실'이 아니라 '대략적인 경향'으로 이해해 주세요."
)

st.markdown(
    '<div class="footer-note">MBTI 결과는 진로 탐색의 출발점입니다. '
    '관심 직업의 실제 업무, 관련 학과, 필요한 역량을 추가로 조사해 보세요.</div>',
    unsafe_allow_html=True,
)
