import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------------------------
# 페이지 설정
# -------------------------------------------------
try:
    st.set_page_config(page_title="국내 MBTI 비율", page_icon="🇰🇷", layout="wide")
except Exception:
    pass

PRIMARY = "#4f46e5"

st.markdown(
    f"""
    <div style="padding:26px 28px;border-radius:16px;
                background:linear-gradient(135deg, {PRIMARY} 0%, #7c3aed 100%);
                color:white;margin-bottom:22px;">
        <h1 style="margin:0;font-size:1.9rem;">🇰🇷 국내 MBTI 유형 비율</h1>
        <p style="margin:8px 0 0;opacity:.92;">
            우리나라에서 알려진 MBTI 16가지 유형별 비율을 그래프로 살펴봅니다.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# 데이터
# 인터넷에 널리 알려진 비공식 참고 통계입니다.
# (정식 MBTI 검사 기관의 공식 인구 통계가 아니며, 표본과 시기에 따라
#  차이가 크므로 '흐름을 살펴보기 위한 참고 자료'로만 활용하세요.)
# -------------------------------------------------
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

# -------------------------------------------------
# 요약 카드
# -------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("가장 흔한 유형", df.iloc[0]["유형"], f"{df.iloc[0]['비율(%)']}%")
c2.metric("가장 희귀한 유형", df.iloc[-1]["유형"], f"{df.iloc[-1]['비율(%)']}%")
c3.metric("SJ(관리자) 계열 합", f"{df[df['기질']=='SJ']['비율(%)'].sum()}%")
c4.metric("NF(외교관) 계열 합", f"{df[df['기질']=='NF']['비율(%)'].sum()}%")

st.markdown("---")

# -------------------------------------------------
# 막대 그래프 (전체 16유형)
# -------------------------------------------------
st.subheader("📊 16개 유형별 비율")

fig_bar = px.bar(
    df,
    x="유형",
    y="비율(%)",
    color="기질",
    color_discrete_map=group_color,
    text="비율(%)",
    category_orders={"유형": df["유형"].tolist()},
)
fig_bar.update_traces(texttemplate="%{text}%", textposition="outside")
fig_bar.update_layout(
    yaxis_title="비율 (%)",
    xaxis_title="MBTI 유형",
    plot_bgcolor="white",
    height=460,
    legend_title="기질 그룹",
)
st.plotly_chart(fig_bar, use_container_width=True)

# -------------------------------------------------
# 기질(temperament) 그룹 도넛
# -------------------------------------------------
left, right = st.columns([1, 1])

with left:
    st.subheader("🍩 기질 그룹별 비중")
    group_df = df.groupby("기질", as_index=False)["비율(%)"].sum()
    fig_donut = go.Figure(
        data=[
            go.Pie(
                labels=group_df["기질"],
                values=group_df["비율(%)"],
                hole=0.55,
                marker=dict(colors=[group_color[g] for g in group_df["기질"]]),
            )
        ]
    )
    fig_donut.update_layout(height=380, showlegend=True)
    st.plotly_chart(fig_donut, use_container_width=True)

with right:
    st.subheader("📋 순위표")
    show_df = df[["유형", "비율(%)", "기질"]].copy()
    show_df.insert(0, "순위", range(1, len(show_df) + 1))
    st.dataframe(show_df, hide_index=True, use_container_width=True, height=420)

st.info(
    "💡 **참고**: 위 수치는 정식 심리검사 기관의 공식 인구 통계가 아니라 온라인에서 "
    "널리 공유되는 비공식 자료입니다. 조사 시점·방식에 따라 실제 비율은 달라질 수 있으니, "
    "'절대적인 사실'이 아니라 '대략적인 경향'으로 이해해 주세요."
)
