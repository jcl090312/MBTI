import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# 페이지 설정 (메인 app.py와 동일한 설정)
# =========================================================
st.set_page_config(
    page_title="국가별 MBTI 분포 | 진로 나침반",
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
        <h1>🌍 나라별 MBTI 분포 비교</h1>
        <p>나라마다 성격 유형의 분포가 어떻게 다르게 나타나는지 살펴봅니다.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "출처: 한국교육진흥연구소(KEDPI) 참고자료, 16Personalities 전 세계 참여자 집계 자료 "
    "— 두 자료 모두 특정 표본(자발적 응시자) 기반이라 국가 전체 인구를 완벽히 대표하지는 않습니다."
)
st.markdown("---")

# =========================================================
# 1) ST(감각·사고) 기질 비율 — 한국 / 일본 / 미국
# =========================================================
st.markdown('<div class="section-title">① \'ST(현실적·논리적)\' 기질 비율 비교</div>', unsafe_allow_html=True)
st.markdown(
    "감각(S)과 사고(T)를 함께 선호하는 'ST' 기질은 실용적이고 원칙을 중시하는 "
    "성향으로 알려져 있습니다. 세 나라를 비교하면 문화적 차이가 뚜렷하게 드러납니다."
)

st_ratio = pd.DataFrame({"국가": ["한국", "일본", "미국"], "ST 비율(%)": [71, 37, 29]})

fig1 = px.bar(
    st_ratio, x="국가", y="ST 비율(%)", text="ST 비율(%)", color="국가",
    color_discrete_sequence=["#4f46e5", "#f59e0b", "#10b981"],
)
fig1.update_traces(texttemplate="%{text}%", textposition="outside")
fig1.update_layout(
    showlegend=False, height=380, yaxis_range=[0, 85],
    plot_bgcolor=CHART_BG, paper_bgcolor=CHART_BG, font_color=CHART_TEXT,
)
fig1.update_xaxes(gridcolor=CHART_GRID)
fig1.update_yaxes(gridcolor=CHART_GRID)
st.plotly_chart(fig1, use_container_width=True)

st.caption(
    "한국은 ST 성향이 71%로 매우 높게 나타나는 반면, 일본은 37%, 미국은 29% 수준으로 "
    "상대적으로 낮습니다. 이는 각 사회가 중시하는 가치관(실용성·조직 문화·개인주의 등)의 "
    "차이와 관련이 있는 것으로 해석됩니다."
)
st.markdown("---")

# =========================================================
# 2) 전 세계 평균 지표별 비율 (16Personalities 응시자 집계)
# =========================================================
st.markdown('<div class="section-title">② 전 세계 참여자 평균 — 4가지 선호지표 비율</div>', unsafe_allow_html=True)
st.markdown(
    "16Personalities(NERIS)에 응시한 전 세계 참여자들의 평균 결과입니다. "
    "온라인으로 자발적 응시한 사람들의 데이터라, 내향(I)·직관(N)·감정(F) 성향이 "
    "다소 과대표집될 수 있다는 점을 감안해서 봐주세요."
)

axis_df = pd.DataFrame({
    "지표": ["E 외향", "I 내향", "S 감각", "N 직관", "T 사고", "F 감정", "J 판단", "P 인식"],
    "비율(%)": [48.67, 51.33, 43.87, 56.13, 32.69, 67.31, 43.67, 56.33],
    "축": ["E/I", "E/I", "S/N", "S/N", "T/F", "T/F", "J/P", "J/P"],
})

fig2 = px.bar(
    axis_df, x="지표", y="비율(%)", color="축", text="비율(%)",
    color_discrete_sequence=["#4f46e5", "#f59e0b", "#ef4444", "#10b981"],
)
fig2.update_traces(texttemplate="%{text}%", textposition="outside")
fig2.update_layout(
    height=420, showlegend=False,
    plot_bgcolor=CHART_BG, paper_bgcolor=CHART_BG, font_color=CHART_TEXT,
)
fig2.update_xaxes(gridcolor=CHART_GRID)
fig2.update_yaxes(gridcolor=CHART_GRID)
st.plotly_chart(fig2, use_container_width=True)
st.markdown("---")

# =========================================================
# 3) 나라별 특징 요약 (정성적 설명)
# =========================================================
st.markdown('<div class="section-title">③ 나라별 특징 요약</div>', unsafe_allow_html=True)

country_notes = {
    "🇰🇷 한국": "ISTJ·ESTJ 등 S·T·J 성향이 강하게 나타나는 경향. 최근에는 ISFP·INFP·ENFP 등 "
    "P(인식형) 유형의 인기도 빠르게 높아지는 추세.",
    "🇺🇸 미국": "ISFJ·ESFJ·ISTJ 계열이 상위권을 차지하는 경향이 있으며, INFJ는 세계적으로도 "
    "가장 희귀한 유형 중 하나로 꼽힘.",
    "🇯🇵 일본": "MBTI보다 혈액형 성격론이 오래 쓰여와 확산이 상대적으로 늦었으나, 최근 빠르게 "
    "대중화되는 중. SJ 기질과 함께 다른 기질도 비교적 고르게 분포.",
    "🇨🇳 중국": "2023년 이후 SNS(웨이보·샤오홍슈)를 중심으로 급속히 확산. 안정성과 절차를 "
    "중시하는 사회 분위기와 맞물려 ISTJ·ESTJ 같은 J형이 상대적으로 많이 보고됨.",
    "🇫🇷 🇬🇧 유럽 주요국": "영국·프랑스·네덜란드 등은 외향(E)이 내향(I)보다 상대적으로 높은 편인 "
    "반면, 독일·폴란드·이탈리아는 내향(I)이 두드러지게 높은 편.",
}

for country, note in country_notes.items():
    with st.container(border=True):
        st.markdown(f"**{country}**")
        st.write(note)

st.info(
    "💡 **함께 생각해보기**: MBTI 분포는 타고난 것이라기보다 문화적 환경, 교육 방식, "
    "검사 참여자의 특성(자발적 온라인 응시 등)에 큰 영향을 받습니다. 나라별 순위 차이를 "
    "'절대적 국민성'으로 단정 짓기보다, 사회·문화적 배경을 함께 살펴보는 것이 중요합니다."
)

st.markdown(
    '<div class="footer-note">MBTI 결과는 진로 탐색의 출발점입니다. '
    '관심 직업의 실제 업무, 관련 학과, 필요한 역량을 추가로 조사해 보세요.</div>',
    unsafe_allow_html=True,
)
