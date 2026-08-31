import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -------------------------------------------------
# 페이지 설정
# -------------------------------------------------
try:
    st.set_page_config(page_title="우리 반 MBTI 조사", page_icon="🧑‍🤝‍🧑", layout="wide")
except Exception:
    pass

PRIMARY = "#4f46e5"

st.markdown(
    f"""
    <div style="padding:26px 28px;border-radius:16px;
                background:linear-gradient(135deg, #10b981 0%, {PRIMARY} 100%);
                color:white;margin-bottom:22px;">
        <h1 style="margin:0;font-size:1.9rem;">🧑‍🤝‍🧑 우리 반 MBTI 조사</h1>
        <p style="margin:8px 0 0;opacity:.92;">
            직접 우리 반(또는 우리 학교) 친구들의 MBTI를 입력하고, 전국 참고 통계와 비교해 보세요.
        </p>
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

if "class_counts" not in st.session_state:
    st.session_state.class_counts = {t: 0 for t in TYPES}

# -------------------------------------------------
# 입력 방식 선택
# -------------------------------------------------
input_mode = st.radio(
    "입력 방식을 선택하세요",
    ["🔢 유형별 인원 직접 입력", "📋 명단 붙여넣기 (예: ISTJ, ENFP, ...)"],
    horizontal=True,
)

if input_mode == "🔢 유형별 인원 직접 입력":
    st.markdown("#### 유형별 인원 수를 입력하세요")
    cols = st.columns(4)
    for i, t in enumerate(TYPES):
        with cols[i % 4]:
            st.session_state.class_counts[t] = st.number_input(
                t, min_value=0, max_value=200,
                value=st.session_state.class_counts.get(t, 0),
                key=f"num_{t}",
            )
else:
    st.markdown("#### 친구들의 MBTI를 쉼표(,) 또는 줄바꿈으로 구분해 붙여넣으세요")
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
    c1.metric("조사 인원", f"{total}명")
    c2.metric("우리 반 최다 유형", class_df.iloc[0]["유형"], f"{class_df.iloc[0]['우리 반 비율(%)']}%")
    diff_df = class_df.copy()
    diff_df["차이"] = diff_df["우리 반 비율(%)"] - diff_df["전국 참고 비율(%)"]
    biggest_gap = diff_df.reindex(diff_df["차이"].abs().sort_values(ascending=False).index).iloc[0]
    c3.metric("전국 대비 가장 큰 차이", biggest_gap["유형"], f"{biggest_gap['차이']:+.1f}%p")

    st.subheader("📊 우리 반 vs 전국 참고 비율")
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
        barmode="group", plot_bgcolor="white", height=450,
        yaxis_title="비율(%)", xaxis_title="MBTI 유형",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
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
