import streamlit as st
from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas


# =========================================================
# 페이지 설정
# =========================================================
st.set_page_config(
    page_title="진로 나침반 | MBTI 진로 탐색",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 세션 상태 초기화
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
# 기본 직업 데이터
# =========================================================
career_data = {
    "소프트웨어 개발자": {
        "emoji": "💻",
        "description": "웹사이트, 모바일 앱, 인공지능 서비스 등 다양한 디지털 프로그램을 설계하고 개발합니다.",
        "majors": ["컴퓨터공학과", "소프트웨어학과", "인공지능학과"],
        "subjects": ["정보", "수학", "영어", "물리학"],
        "skills": ["논리력", "분석력", "문제 해결력", "집중력"],
        "certificates": ["정보처리기능사", "정보처리기사", "SQLD"],
        "interests": ["IT·기술", "문제 해결", "만들기"],
        "aptitudes": ["논리력", "분석력", "집중력"]
    },
    "데이터 분석가": {
        "emoji": "📊",
        "description": "데이터를 수집하고 분석하여 기업이나 사회 문제 해결에 필요한 정보를 찾습니다.",
        "majors": ["데이터사이언스학과", "통계학과", "산업공학과"],
        "subjects": ["수학", "확률과 통계", "정보", "영어"],
        "skills": ["분석력", "통계적 사고력", "꼼꼼함", "문제 해결력"],
        "certificates": ["ADsP", "SQLD", "빅데이터분석기사"],
        "interests": ["IT·기술", "수학", "문제 해결"],
        "aptitudes": ["분석력", "논리력", "꼼꼼함"]
    },
    "인공지능 연구원": {
        "emoji": "🤖",
        "description": "인공지능 기술을 연구하고 새로운 알고리즘과 서비스를 개발합니다.",
        "majors": ["인공지능학과", "컴퓨터공학과", "전자공학과", "수학과"],
        "subjects": ["수학", "정보", "물리학", "영어"],
        "skills": ["수학적 사고력", "창의력", "분석력", "연구 능력"],
        "certificates": ["정보처리기사", "ADsP"],
        "interests": ["IT·기술", "과학", "연구"],
        "aptitudes": ["논리력", "분석력", "창의력"]
    },
    "게임 개발자": {
        "emoji": "🎮",
        "description": "게임의 프로그램, 그래픽, 스토리, 시스템을 기획하고 제작합니다.",
        "majors": ["게임학과", "컴퓨터공학과", "디지털콘텐츠학과"],
        "subjects": ["정보", "수학", "미술", "영어"],
        "skills": ["창의력", "프로그래밍 능력", "협업 능력", "집중력"],
        "certificates": ["정보처리기능사", "정보처리기사"],
        "interests": ["IT·기술", "창작", "게임"],
        "aptitudes": ["창의력", "논리력", "집중력"]
    },
    "정보보안 전문가": {
        "emoji": "🔐",
        "description": "해킹과 개인정보 유출 등 사이버 위협으로부터 컴퓨터 시스템과 데이터를 보호합니다.",
        "majors": ["정보보호학과", "사이버보안학과", "컴퓨터공학과"],
        "subjects": ["정보", "수학", "영어", "물리학"],
        "skills": ["분석력", "꼼꼼함", "문제 해결력", "논리력"],
        "certificates": ["정보보안기사", "정보처리기사", "네트워크관리사"],
        "interests": ["IT·기술", "문제 해결", "연구"],
        "aptitudes": ["분석력", "논리력", "꼼꼼함"]
    },
    "간호사": {
        "emoji": "🩺",
        "description": "환자의 건강 상태를 관찰하고 치료와 회복, 건강 관리를 돕는 의료 전문 직업입니다.",
        "majors": ["간호학과"],
        "subjects": ["생명과학", "화학", "보건", "영어"],
        "skills": ["공감력", "책임감", "관찰력", "의사소통"],
        "certificates": ["간호사 국가시험"],
        "interests": ["의료·보건", "사람 돕기", "과학"],
        "aptitudes": ["공감력", "책임감", "관찰력"]
    },
    "의사": {
        "emoji": "👨‍⚕️",
        "description": "환자의 질병을 진단하고 치료하며 건강을 관리하는 의료 전문가입니다.",
        "majors": ["의예과", "의학과"],
        "subjects": ["생명과학", "화학", "수학", "영어"],
        "skills": ["책임감", "분석력", "판단력", "집중력"],
        "certificates": ["의사 국가시험"],
        "interests": ["의료·보건", "과학", "사람 돕기"],
        "aptitudes": ["분석력", "책임감", "집중력"]
    },
    "교사": {
        "emoji": "🏫",
        "description": "학생의 학습과 성장을 지원하고 수업 및 생활 교육 활동을 수행합니다.",
        "majors": ["교육학과", "국어교육과", "수학교육과", "영어교육과", "과학교육과"],
        "subjects": ["국어", "영어", "사회·문화", "관심 교과"],
        "skills": ["의사소통", "공감력", "설명 능력", "책임감"],
        "certificates": ["중등학교 정교사 자격"],
        "interests": ["교육", "사람 돕기", "사회"],
        "aptitudes": ["의사소통", "공감력", "책임감"]
    },
    "사회복지사": {
        "emoji": "🤝",
        "description": "도움이 필요한 사람들에게 복지 서비스와 정보를 연결하고 지원합니다.",
        "majors": ["사회복지학과", "사회학과", "심리학과"],
        "subjects": ["사회·문화", "생활과 윤리", "정치와 법"],
        "skills": ["공감력", "의사소통", "책임감", "문제 해결력"],
        "certificates": ["사회복지사 1급", "사회복지사 2급"],
        "interests": ["사람 돕기", "사회", "교육"],
        "aptitudes": ["공감력", "의사소통", "책임감"]
    },
    "심리학 연구원": {
        "emoji": "🧠",
        "description": "사람의 생각, 감정, 행동을 연구하고 분석하는 일을 합니다.",
        "majors": ["심리학과", "상담심리학과", "교육학과"],
        "subjects": ["사회·문화", "생활과 윤리", "생명과학", "영어"],
        "skills": ["공감력", "관찰력", "분석력", "연구 능력"],
        "certificates": ["임상심리사", "청소년상담사"],
        "interests": ["사람 돕기", "연구", "사회"],
        "aptitudes": ["공감력", "분석력", "관찰력"]
    },
    "변호사": {
        "emoji": "⚖️",
        "description": "법률 지식을 바탕으로 사회의 갈등과 분쟁을 해결하고 권리를 보호합니다.",
        "majors": ["법학과", "행정학과", "정치외교학과"],
        "subjects": ["정치와 법", "사회·문화", "국어", "영어"],
        "skills": ["논리력", "의사소통", "분석력", "표현력"],
        "certificates": ["변호사시험"],
        "interests": ["사회", "토론", "문제 해결"],
        "aptitudes": ["논리력", "의사소통", "분석력"]
    },
    "회계사": {
        "emoji": "🧾",
        "description": "기업과 기관의 재무 정보를 검토하고 회계 및 세무 업무를 수행합니다.",
        "majors": ["회계학과", "경영학과", "경제학과", "세무학과"],
        "subjects": ["수학", "경제", "정치와 법", "영어"],
        "skills": ["분석력", "꼼꼼함", "책임감", "계산 능력"],
        "certificates": ["공인회계사(CPA)", "세무사"],
        "interests": ["수학", "경제", "문제 해결"],
        "aptitudes": ["분석력", "꼼꼼함", "논리력"]
    },
    "공무원": {
        "emoji": "🏛️",
        "description": "국가나 지방자치단체에서 시민 생활과 관련된 행정 업무를 수행합니다.",
        "majors": ["행정학과", "법학과", "정치외교학과", "사회복지학과"],
        "subjects": ["정치와 법", "사회·문화", "한국사", "국어"],
        "skills": ["책임감", "꼼꼼함", "의사소통", "문서 작성 능력"],
        "certificates": ["공무원 공개채용시험"],
        "interests": ["사회", "사람 돕기", "문제 해결"],
        "aptitudes": ["책임감", "꼼꼼함", "의사소통"]
    },
    "기계공학자": {
        "emoji": "⚙️",
        "description": "기계와 장치를 설계하고 성능, 안전성, 생산 과정을 개선합니다.",
        "majors": ["기계공학과", "로봇공학과", "자동차공학과"],
        "subjects": ["수학", "물리학", "정보", "화학"],
        "skills": ["논리력", "공간지각력", "문제 해결력", "설계 능력"],
        "certificates": ["일반기계기사", "기계설계기사"],
        "interests": ["과학", "IT·기술", "만들기"],
        "aptitudes": ["논리력", "공간지각력", "문제 해결력"]
    },
    "건축가": {
        "emoji": "🏗️",
        "description": "사람들이 생활하는 건물과 공간을 안전하고 아름답게 설계합니다.",
        "majors": ["건축학과", "건축공학과", "실내건축학과"],
        "subjects": ["수학", "미술", "물리학", "정보"],
        "skills": ["창의력", "공간지각력", "설계 능력", "집중력"],
        "certificates": ["건축사", "건축기사"],
        "interests": ["미술", "만들기", "과학"],
        "aptitudes": ["창의력", "공간지각력", "집중력"]
    },
    "그래픽 디자이너": {
        "emoji": "🎨",
        "description": "이미지, 글자, 색상 등을 활용하여 시각적인 메시지와 디자인을 만듭니다.",
        "majors": ["시각디자인학과", "디자인학과", "디지털콘텐츠학과"],
        "subjects": ["미술", "정보", "국어", "영어"],
        "skills": ["창의력", "관찰력", "미적 감각", "집중력"],
        "certificates": ["GTQ", "컴퓨터그래픽스운용기능사"],
        "interests": ["미술", "창작", "IT·기술"],
        "aptitudes": ["창의력", "관찰력", "집중력"]
    },
    "웹툰 작가": {
        "emoji": "✏️",
        "description": "그림과 이야기를 결합해 독자에게 전달할 웹툰 콘텐츠를 제작합니다.",
        "majors": ["웹툰학과", "만화애니메이션학과", "시각디자인학과"],
        "subjects": ["미술", "국어", "정보", "사회·문화"],
        "skills": ["창의력", "표현력", "관찰력", "꾸준함"],
        "certificates": ["필수 자격증 없음", "GTQ(활용 가능)"],
        "interests": ["미술", "창작", "글쓰기"],
        "aptitudes": ["창의력", "표현력", "집중력"]
    },
    "작가": {
        "emoji": "📚",
        "description": "소설, 에세이, 시나리오, 기사 등 글을 통해 생각과 이야기를 전달합니다.",
        "majors": ["국어국문학과", "문예창작학과", "신문방송학과"],
        "subjects": ["국어", "문학", "사회·문화", "영어"],
        "skills": ["창의력", "표현력", "관찰력", "글쓰기 능력"],
        "certificates": ["필수 자격증 없음"],
        "interests": ["글쓰기", "창작", "사회"],
        "aptitudes": ["창의력", "표현력", "관찰력"]
    },
    "광고기획자": {
        "emoji": "📣",
        "description": "제품과 서비스의 가치를 효과적으로 알릴 수 있는 광고 전략과 콘텐츠를 기획합니다.",
        "majors": ["광고홍보학과", "미디어커뮤니케이션학과", "경영학과"],
        "subjects": ["사회·문화", "국어", "미술", "영어"],
        "skills": ["창의력", "기획력", "의사소통", "분석력"],
        "certificates": ["검색광고마케터", "SNS광고마케터"],
        "interests": ["창작", "사회", "경제"],
        "aptitudes": ["창의력", "기획력", "의사소통"]
    },
    "마케팅 전문가": {
        "emoji": "📈",
        "description": "시장과 소비자를 분석하고 제품 및 서비스의 판매 전략을 세웁니다.",
        "majors": ["경영학과", "광고홍보학과", "경제학과"],
        "subjects": ["경제", "사회·문화", "수학", "영어"],
        "skills": ["분석력", "창의력", "기획력", "의사소통"],
        "certificates": ["ADsP", "검색광고마케터", "사회조사분석사"],
        "interests": ["경제", "창작", "사회"],
        "aptitudes": ["분석력", "창의력", "의사소통"]
    },
    "행사 기획자": {
        "emoji": "🎪",
        "description": "축제, 공연, 전시, 기업 행사 등의 운영 계획을 세우고 진행합니다.",
        "majors": ["관광경영학과", "문화콘텐츠학과", "광고홍보학과"],
        "subjects": ["사회·문화", "국어", "영어", "미술"],
        "skills": ["기획력", "의사소통", "협업 능력", "문제 해결력"],
        "certificates": ["컨벤션기획사", "국내여행안내사"],
        "interests": ["사람 만나기", "창작", "여행"],
        "aptitudes": ["기획력", "의사소통", "리더십"]
    },
    "경찰관": {
        "emoji": "👮",
        "description": "범죄를 예방하고 시민의 안전을 보호하며 사건과 사고에 대응합니다.",
        "majors": ["경찰행정학과", "법학과", "행정학과"],
        "subjects": ["정치와 법", "사회·문화", "체육", "국어"],
        "skills": ["책임감", "판단력", "체력", "의사소통"],
        "certificates": ["경찰공무원 채용시험", "무도 단증"],
        "interests": ["사회", "사람 돕기", "스포츠"],
        "aptitudes": ["책임감", "판단력", "신체운동능력"]
    },
    "소방관": {
        "emoji": "🚒",
        "description": "화재와 재난 현장에서 시민의 생명과 안전을 지키는 일을 합니다.",
        "majors": ["소방방재학과", "응급구조학과", "안전공학과"],
        "subjects": ["체육", "생명과학", "화학", "물리학"],
        "skills": ["책임감", "판단력", "체력", "협업 능력"],
        "certificates": ["소방공무원 채용시험", "응급구조사"],
        "interests": ["사람 돕기", "스포츠", "과학"],
        "aptitudes": ["책임감", "판단력", "신체운동능력"]
    },
    "환경 연구원": {
        "emoji": "🌿",
        "description": "기후 변화, 생태계, 대기와 물 오염 등 환경 문제를 연구하고 해결책을 찾습니다.",
        "majors": ["환경공학과", "환경과학과", "생명과학과", "지구과학과"],
        "subjects": ["지구과학", "생명과학", "화학", "수학"],
        "skills": ["분석력", "관찰력", "연구 능력", "책임감"],
        "certificates": ["환경기사", "대기환경기사", "수질환경기사"],
        "interests": ["환경", "과학", "연구"],
        "aptitudes": ["분석력", "관찰력", "책임감"]
    },
    "여행 기획자": {
        "emoji": "✈️",
        "description": "여행객의 관심과 목적에 맞는 여행 상품과 체험 프로그램을 기획합니다.",
        "majors": ["관광경영학과", "호텔관광학과", "국제학과"],
        "subjects": ["영어", "세계지리", "사회·문화", "국어"],
        "skills": ["기획력", "의사소통", "외국어 능력", "창의력"],
        "certificates": ["국내여행안내사", "관광통역안내사"],
        "interests": ["여행", "사람 만나기", "외국어"],
        "aptitudes": ["기획력", "의사소통", "창의력"]
    },
    "호텔리어": {
        "emoji": "🏨",
        "description": "호텔을 찾은 고객이 안전하고 편안하게 머물 수 있도록 서비스를 제공합니다.",
        "majors": ["호텔경영학과", "관광경영학과", "항공서비스학과"],
        "subjects": ["영어", "중국어", "사회·문화", "국어"],
        "skills": ["의사소통", "공감력", "문제 해결력", "서비스 정신"],
        "certificates": ["호텔서비스사", "호텔관리사"],
        "interests": ["사람 만나기", "여행", "외국어"],
        "aptitudes": ["의사소통", "공감력", "문제 해결력"]
    }
}


# =========================================================
# MBTI별 기본 추천 직업
# =========================================================
mbti_recommendations = {
    "ISTJ": ["회계사", "공무원", "데이터 분석가"],
    "ISFJ": ["간호사", "사회복지사", "교사"],
    "INFJ": ["심리학 연구원", "작가", "환경 연구원"],
    "INTJ": ["소프트웨어 개발자", "데이터 분석가", "인공지능 연구원"],
    "ISTP": ["기계공학자", "정보보안 전문가", "소방관"],
    "ISFP": ["그래픽 디자이너", "웹툰 작가", "호텔리어"],
    "INFP": ["작가", "웹툰 작가", "사회복지사"],
    "INTP": ["인공지능 연구원", "게임 개발자", "정보보안 전문가"],
    "ESTP": ["경찰관", "소방관", "행사 기획자"],
    "ESFP": ["행사 기획자", "호텔리어", "여행 기획자"],
    "ENFP": ["광고기획자", "작가", "여행 기획자"],
    "ENTP": ["변호사", "마케팅 전문가", "광고기획자"],
    "ESTJ": ["경영 컨설턴트", "공무원", "회계사"],
    "ESFJ": ["교사", "간호사", "호텔리어"],
    "ENFJ": ["교사", "사회복지사", "광고기획자"],
    "ENTJ": ["마케팅 전문가", "소프트웨어 개발자", "회계사"]
}


# 경영 컨설턴트 직업 정보 추가
career_data["경영 컨설턴트"] = {
    "emoji": "💼",
    "description": "기업과 조직의 문제를 분석하고 성장 전략 및 개선 방법을 제안합니다.",
    "majors": ["경영학과", "경제학과", "산업공학과", "행정학과"],
    "subjects": ["경제", "수학", "사회·문화", "영어"],
    "skills": ["분석력", "기획력", "의사소통", "리더십"],
    "certificates": ["경영지도사", "PMP", "SQLD"],
    "interests": ["경제", "문제 해결", "리더십"],
    "aptitudes": ["분석력", "기획력", "리더십"]
}


# =========================================================
# 디자인 및 다크 모드 CSS
# 중요: unsafe_allow_html=True를 반드시 사용해야 함
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
        /* 전체 화면 */
        .stApp {{
            background: {bg};
            color: {text};
        }}

        /* 상단 기본 메뉴 숨김 */
        #MainMenu {{
            visibility: hidden;
        }}

        footer {{
            visibility: hidden;
        }}

        header[data-testid="stHeader"] {{
            background: transparent;
        }}

        /* 본문 폭 */
        .block-container {{
            max-width: 1250px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }}

        /* 글자 색상 */
        h1, h2, h3, h4, p, label, span, div {{
            color: {text};
        }}

        /* 사이드바 */
        [data-testid="stSidebar"] {{
            background: {surface};
            border-right: 1px solid {border};
        }}

        [data-testid="stSidebar"] .stMarkdown p {{
            color: {subtext};
        }}

        /* 입력 요소 */
        .stTextInput input,
        .stTextArea textarea,
        .stSelectbox > div > div,
        .stMultiSelect > div > div {{
            background-color: {input_bg} !important;
            color: {text} !important;
            border-color: {border} !important;
            border-radius: 10px !important;
        }}

        /* 멀티셀렉트 내부 글자 */
        [data-baseweb="select"] * {{
            color: {text};
        }}

        /* 탭 */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            border-bottom: 1px solid {border};
        }}

        .stTabs [data-baseweb="tab"] {{
            height: 46px;
            background: transparent;
            color: {subtext};
            border-radius: 10px 10px 0 0;
            padding: 0 14px;
        }}

        .stTabs [aria-selected="true"] {{
            color: {primary} !important;
            font-weight: 700;
            border-bottom: 3px solid {primary};
        }}

        /* 버튼 */
        .stButton > button,
        .stDownloadButton > button {{
            border-radius: 10px;
            border: 1px solid {border};
            font-weight: 700;
            transition: 0.2s;
        }}

        .stButton > button:hover,
        .stDownloadButton > button:hover {{
            border-color: {primary};
            color: {primary};
            transform: translateY(-1px);
        }}

        /* 확장 카드 */
        [data-testid="stExpander"] {{
            background: {surface};
            border: 1px solid {border};
            border-radius: 14px;
            margin-bottom: 12px;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
        }}

        [data-testid="stExpander"] details summary {{
            font-size: 1.05rem;
            font-weight: 700;
        }}

        /* 정보, 성공, 경고 박스 */
        [data-testid="stAlert"] {{
            border-radius: 12px;
        }}

        /* 구분선 */
        hr {{
            border-color: {border};
        }}

        /* 커스텀 디자인 요소 */
        .hero {{
            background: linear-gradient(135deg, {hero1}, {hero2});
            border-radius: 22px;
            padding: 38px 42px;
            margin-bottom: 26px;
            color: white !important;
            box-shadow: 0 16px 35px rgba(49, 46, 129, 0.22);
        }}

        .hero h1 {{
            color: white !important;
            font-size: 2.5rem;
            margin: 0 0 8px 0;
        }}

        .hero p {{
            color: #E0E7FF !important;
            font-size: 1.05rem;
            margin: 0;
        }}

        .section-title {{
            font-size: 1.55rem;
            font-weight: 800;
            margin: 12px 0 5px;
            color: {text};
        }}

        .section-subtitle {{
            color: {subtext} !important;
            margin-bottom: 20px;
        }}

        .stat-card {{
            background: {surface};
            border: 1px solid {border};
            border-radius: 16px;
            padding: 18px 20px;
            min-height: 110px;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
        }}

        .stat-number {{
            font-size: 1.7rem;
            font-weight: 800;
            color: {primary} !important;
        }}

        .stat-label {{
            color: {subtext} !important;
            font-size: 0.9rem;
        }}

        .career-info-box {{
            background: {surface2};
            border: 1px solid {border};
            border-radius: 12px;
            padding: 14px;
            min-height: 110px;
            margin-top: 10px;
        }}

        .career-info-title {{
            font-size: 0.9rem;
            font-weight: 800;
            color: {primary} !important;
            margin-bottom: 7px;
        }}

        .career-info-content {{
            font-size: 0.92rem;
            color: {text} !important;
            line-height: 1.6;
        }}

        .footer-note {{
            color: {subtext} !important;
            font-size: 0.88rem;
            text-align: center;
            padding: 30px 0 5px;
        }}
    </style>
    """

    # 첨부 이미지처럼 CSS가 화면에 글자로 출력되는 문제 해결
    st.markdown(css, unsafe_allow_html=True)


apply_custom_css()


# =========================================================
# 도우미 함수
# =========================================================
def split_text(text):
    """쉼표로 입력한 내용을 리스트로 변환합니다."""
    return [item.strip() for item in text.split(",") if item.strip()]


def get_all_careers():
    """기본 직업 + 학생이 추가한 직업 정보를 합칩니다."""
    jobs = career_data.copy()

    for custom_job in st.session_state.custom_jobs:
        jobs[custom_job["name"]] = custom_job

    return jobs


def get_job_info(job_name):
    return get_all_careers().get(job_name)


def toggle_favorite(job_name):
    if job_name in st.session_state.favorites:
        st.session_state.favorites.remove(job_name)
    else:
        st.session_state.favorites.append(job_name)


def recommend_jobs(mbti, interests, aptitudes, subjects):
    """MBTI, 흥미, 적성, 과목을 점수화해 직업을 추천합니다."""
    all_jobs = get_all_careers()
    score_result = {}

    for job_name, info in all_jobs.items():
        score = 0

        # MBTI 기본 추천 가중치
        if job_name in mbti_recommendations.get(mbti, []):
            score += 6

        # 흥미, 적성, 과목 일치 점수
        score += len(set(interests) & set(info.get("interests", []))) * 3
        score += len(set(aptitudes) & set(info.get("aptitudes", []))) * 3
        score += len(set(subjects) & set(info.get("subjects", []))) * 2

        score_result[job_name] = score

    sorted_jobs = sorted(
        score_result.items(),
        key=lambda item: item[1],
        reverse=True
    )

    results = [job for job, score in sorted_jobs if score > 0][:6]

    # 선택한 조건이 적은 경우 MBTI 기본 추천을 추가
    for job in mbti_recommendations.get(mbti, []):
        if job not in results:
            results.append(job)

    return results[:6]


def render_job_card(job_name, key_prefix):
    """직업 상세 정보를 확장 카드로 출력합니다."""
    info = get_job_info(job_name)

    if not info:
        return

    emoji = info.get("emoji", "💼")
    favorite = job_name in st.session_state.favorites
    button_text = "★ 저장됨" if favorite else "☆ 즐겨찾기"

    with st.expander(f"{emoji}  {job_name}", expanded=False):
        st.write(info["description"])

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="career-info-box">
                <div class="career-info-title">🏫 관련 학과</div>
                <div class="career-info-content">{", ".join(info["majors"])}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="career-info-box">
                <div class="career-info-title">📚 추천 과목</div>
                <div class="career-info-content">{", ".join(info["subjects"])}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="career-info-box">
                <div class="career-info-title">🧠 필요한 역량</div>
                <div class="career-info-content">{", ".join(info["skills"])}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="career-info-box">
                <div class="career-info-title">📜 자격증 · 시험</div>
                <div class="career-info-content">{", ".join(info["certificates"])}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button(button_text, key=f"{key_prefix}_{job_name}"):
            toggle_favorite(job_name)
            st.rerun()


def create_text_report(profile, jobs):
    lines = [
        "=" * 60,
        "MBTI 진로 탐색 결과 보고서",
        "=" * 60,
        f"생성 일시: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"MBTI: {profile['mbti']}",
        f"흥미 분야: {', '.join(profile['interests']) if profile['interests'] else '선택하지 않음'}",
        f"나의 적성: {', '.join(profile['aptitudes']) if profile['aptitudes'] else '선택하지 않음'}",
        f"좋아하는 과목: {', '.join(profile['subjects']) if profile['subjects'] else '선택하지 않음'}",
        "",
        "[ 추천 · 관심 직업 ]"
    ]

    for index, job_name in enumerate(jobs, start=1):
        info = get_job_info(job_name)
        if not info:
            continue

        lines.extend([
            "",
            f"{index}. {job_name}",
            f"직업 소개: {info['description']}",
            f"관련 학과: {', '.join(info['majors'])}",
            f"추천 과목: {', '.join(info['subjects'])}",
            f"필요 역량: {', '.join(info['skills'])}",
            f"자격증 · 시험: {', '.join(info['certificates'])}",
        ])

    lines.extend([
        "",
        "=" * 60,
        "[ 스스로 탐색할 질문 ]",
        "1. 추천 직업 중 가장 흥미로운 직업은 무엇인가?",
        "2. 그 직업과 연결되는 학과와 대학교는 어디일까?",
        "3. 이 직업을 위해 지금부터 키울 수 있는 역량은 무엇일까?",
        "4. 직업 체험, 독서, 인터뷰 등으로 더 알아볼 방법은 무엇일까?"
    ])

    return "\n".join(lines)


def create_pdf_report(profile, jobs):
    """한글 지원 PDF 보고서 생성 함수"""
    pdfmetrics.registerFont(UnicodeCIDFont("HYSMyeongJo-Medium"))

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    x = 18 * mm
    y = height - 20 * mm
    line_height = 6.5 * mm

    def write_line(text, font_size=10):
        nonlocal y

        if y < 22 * mm:
            pdf.showPage()
            y = height - 20 * mm

        pdf.setFont("HYSMyeongJo-Medium", font_size)
        pdf.drawString(x, y, text[:95])
        y -= line_height

    write_line("MBTI 진로 탐색 결과 보고서", 18)
    y -= 4 * mm
    write_line(f"생성 일시: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y -= 3 * mm

    write_line(f"MBTI: {profile['mbti']}")
    write_line(f"흥미 분야: {', '.join(profile['interests']) if profile['interests'] else '선택하지 않음'}")
    write_line(f"나의 적성: {', '.join(profile['aptitudes']) if profile['aptitudes'] else '선택하지 않음'}")
    write_line(f"좋아하는 과목: {', '.join(profile['subjects']) if profile['subjects'] else '선택하지 않음'}")

    y -= 4 * mm
    write_line("추천 · 관심 직업", 14)
    y -= 2 * mm

    for index, job_name in enumerate(jobs, start=1):
        info = get_job_info(job_name)

        if not info:
            continue

        write_line(f"{index}. {job_name}", 12)
        write_line(f"직업 소개: {info['description']}")
        write_line(f"관련 학과: {', '.join(info['majors'])}")
        write_line(f"추천 과목: {', '.join(info['subjects'])}")
        write_line(f"필요 역량: {', '.join(info['skills'])}")
        write_line(f"자격증 · 시험: {', '.join(info['certificates'])}")
        y -= 3 * mm

    y -= 3 * mm
    write_line("스스로 탐색할 질문", 14)
    write_line("1. 추천 직업 중 가장 흥미로운 직업은 무엇인가?")
    write_line("2. 이 직업을 위해 어떤 과목과 활동을 준비하면 좋을까?")
    write_line("3. 관련 학과와 진로 체험 기회를 조사해 보자.")

    pdf.save()
    buffer.seek(0)

    return buffer


# =========================================================
# 사이드바
# =========================================================
with st.sidebar:
    st.markdown("## 🧭 진로 나침반")
    st.caption("나의 성향에서 시작하는 진로 탐색")

    st.divider()

    dark_mode = st.toggle(
        "🌙 다크 모드",
        value=st.session_state.dark_mode
    )

    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()

    st.divider()

    st.markdown("### ⭐ 즐겨찾기 현황")
    st.metric("저장한 직업", f"{len(st.session_state.favorites)}개")

    if st.session_state.favorites:
        for favorite in st.session_state.favorites:
            st.caption(f"• {favorite}")
    else:
        st.caption("관심 직업을 저장해 보세요.")

    st.divider()

    st.markdown("### 학습 안내")
    st.caption(
        "MBTI는 진로를 결정하는 검사 결과가 아닙니다. "
        "흥미, 적성, 가치관, 경험을 함께 고려하며 직업을 탐색해 보세요."
    )


# =========================================================
# 헤더
# =========================================================
st.markdown("""
<div class="hero">
    <h1>🧭 진로 나침반</h1>
    <p>MBTI · 흥미 · 적성 · 좋아하는 과목을 바탕으로 나에게 맞는 진로를 탐색해 보세요.</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{len(get_all_careers())}</div>
        <div class="stat-label">탐색 가능한 직업</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{len(st.session_state.favorites)}</div>
        <div class="stat-label">내가 저장한 관심 직업</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">16</div>
        <div class="stat-label">MBTI 유형 기반 탐색</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# 탭
# =========================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "✨ 맞춤 추천",
    "🔎 직업 검색",
    "⭐ 즐겨찾기",
    "➕ 직업 추가",
    "📄 결과 저장"
])


# =========================================================
# 탭 1: 맞춤 추천
# =========================================================
with tab1:
    st.markdown('<div class="section-title">나의 성향으로 직업 탐색하기</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">선택한 조건과 직업 정보의 일치도를 바탕으로 탐색할 직업을 추천합니다.</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    interest_options = [
        "IT·기술", "과학", "의료·보건", "교육", "사회", "경제",
        "미술", "창작", "글쓰기", "스포츠", "환경", "여행",
        "외국어", "사람 돕기", "문제 해결", "만들기",
        "리더십", "토론", "게임", "사람 만나기", "연구", "수학"
    ]

    aptitude_options = [
        "논리력", "분석력", "창의력", "공감력", "의사소통",
        "책임감", "꼼꼼함", "집중력", "관찰력", "기획력",
        "리더십", "판단력", "공간지각력", "신체운동능력",
        "표현력", "문제 해결력", "자기관리"
    ]

    subject_options = [
        "국어", "문학", "수학", "확률과 통계", "영어",
        "사회·문화", "정치와 법", "생활과 윤리", "경제",
        "한국사", "세계지리", "물리학", "화학", "생명과학",
        "지구과학", "정보", "미술", "체육", "보건", "중국어"
    ]

    with left:
        mbti = st.selectbox(
            "1. 나의 MBTI",
            list(mbti_recommendations.keys()),
            index=list(mbti_recommendations.keys()).index(
                st.session_state.last_profile["mbti"]
            )
        )

        interests = st.multiselect(
            "2. 관심 있는 분야",
            interest_options,
            default=st.session_state.last_profile["interests"]
        )

    with right:
        aptitudes = st.multiselect(
            "3. 내가 잘한다고 생각하는 능력",
            aptitude_options,
            default=st.session_state.last_profile["aptitudes"]
        )

        subjects = st.multiselect(
            "4. 좋아하거나 관심 있는 과목",
            subject_options,
            default=st.session_state.last_profile["subjects"]
        )

    if st.button("✨ 나에게 맞는 직업 추천받기", use_container_width=True):
        st.session_state.last_profile = {
            "mbti": mbti,
            "interests": interests,
            "aptitudes": aptitudes,
            "subjects": subjects
        }

        st.session_state.recommended_jobs = recommend_jobs(
            mbti, interests, aptitudes, subjects
        )

    if st.session_state.recommended_jobs:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">추천 직업 목록</div>', unsafe_allow_html=True)
        st.caption("직업 카드를 열면 관련 학과, 추천 과목, 역량, 자격증 정보를 확인할 수 있습니다.")

        for job in st.session_state.recommended_jobs:
            render_job_card(job, "recommend")


# =========================================================
# 탭 2: 직업 검색
# =========================================================
with tab2:
    st.markdown('<div class="section-title">관심 직업 검색하기</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">직업명뿐 아니라 학과, 과목, 역량, 흥미 분야로도 검색할 수 있습니다.</div>',
        unsafe_allow_html=True
    )

    keyword = st.text_input(
        "검색어 입력",
        placeholder="예: 개발자, 디자인, 생명과학, 사람 돕기, 수학"
    )

    if keyword:
        keyword = keyword.lower().strip()
        results = []

        for job_name, info in get_all_careers().items():
            search_text = " ".join([
                job_name,
                info["description"],
                " ".join(info["majors"]),
                " ".join(info["subjects"]),
                " ".join(info["skills"]),
                " ".join(info["certificates"]),
                " ".join(info["interests"]),
                " ".join(info["aptitudes"])
            ]).lower()

            if keyword in search_text:
                results.append(job_name)

        if results:
            st.success(f"'{keyword}'와(과) 관련된 직업 {len(results)}개를 찾았습니다.")

            for job in results:
                render_job_card(job, "search")
        else:
            st.warning("검색 결과가 없습니다. 다른 키워드로 다시 검색해 보세요.")
    else:
        st.info("예시: 개발자, 디자인, 환경, 교육, 의료, 영어, 창의력")


# =========================================================
# 탭 3: 즐겨찾기
# =========================================================
with tab3:
    st.markdown('<div class="section-title">내 관심 직업 보관함</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">관심 있는 직업을 저장하고 나중에 다시 비교해 보세요.</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.favorites:
        st.info("저장된 직업이 없습니다. 맞춤 추천 또는 직업 검색에서 ☆ 즐겨찾기를 눌러 저장하세요.")
    else:
        st.success(f"현재 {len(st.session_state.favorites)}개의 관심 직업을 저장했습니다.")

        for job in st.session_state.favorites.copy():
            render_job_card(job, "favorite")


# =========================================================
# 탭 4: 학생이 직업 정보 추가
# =========================================================
with tab4:
    st.markdown('<div class="section-title">내가 조사한 직업 직접 추가하기</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">진로 조사, 직업인 인터뷰, 독서 활동에서 알게 된 직업 정보를 기록해 보세요.</div>',
        unsafe_allow_html=True
    )

    with st.form("add_job_form", clear_on_submit=True):
        name = st.text_input("직업 이름 *", placeholder="예: UX 디자이너")
        description = st.text_area(
            "직업 소개 *",
            placeholder="이 직업에서 주로 하는 일을 간단하게 작성하세요."
        )

        form_left, form_right = st.columns(2)

        with form_left:
            majors_text = st.text_input(
                "관련 학과",
                placeholder="예: 디자인학과, 산업디자인학과"
            )
            subjects_text = st.text_input(
                "추천 과목",
                placeholder="예: 미술, 정보, 국어"
            )
            interests_text = st.text_input(
                "관련 흥미 분야",
                placeholder="예: 창작, IT·기술, 사람 돕기"
            )

        with form_right:
            skills_text = st.text_input(
                "필요한 역량",
                placeholder="예: 창의력, 의사소통, 관찰력"
            )
            certificates_text = st.text_input(
                "자격증 또는 시험",
                placeholder="예: GTQ, 관련 국가자격"
            )
            aptitudes_text = st.text_input(
                "관련 적성",
                placeholder="예: 창의력, 분석력, 표현력"
            )

        submitted = st.form_submit_button("➕ 직업 정보 저장하기", use_container_width=True)

    if submitted:
        if not name.strip() or not description.strip():
            st.error("직업 이름과 직업 소개는 반드시 입력해야 합니다.")
        else:
            new_job = {
                "emoji": "💼",
                "name": name.strip(),
                "description": description.strip(),
                "majors": split_text(majors_text) or ["추가 조사 필요"],
                "subjects": split_text(subjects_text) or ["추가 조사 필요"],
                "skills": split_text(skills_text) or ["추가 조사 필요"],
                "certificates": split_text(certificates_text) or ["추가 조사 필요"],
                "interests": split_text(interests_text),
                "aptitudes": split_text(aptitudes_text)
            }

            # 같은 이름의 기존 사용자 직업 정보는 교체
            st.session_state.custom_jobs = [
                job for job in st.session_state.custom_jobs
                if job["name"] != new_job["name"]
            ]
            st.session_state.custom_jobs.append(new_job)

            st.success(f"'{new_job['name']}' 직업 정보를 저장했습니다.")

    if st.session_state.custom_jobs:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 내가 추가한 직업")

        for job in st.session_state.custom_jobs.copy():
            col_a, col_b = st.columns([5, 1])

            with col_a:
                st.write(f"💼 **{job['name']}** — {job['description']}")

            with col_b:
                if st.button("삭제", key=f"delete_{job['name']}"):
                    st.session_state.custom_jobs = [
                        item for item in st.session_state.custom_jobs
                        if item["name"] != job["name"]
                    ]

                    if job["name"] in st.session_state.favorites:
                        st.session_state.favorites.remove(job["name"])

                    st.rerun()


# =========================================================
# 탭 5: 결과 저장
# =========================================================
with tab5:
    st.markdown('<div class="section-title">진로 탐색 결과 저장하기</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">관심 직업과 추천 결과를 TXT 또는 PDF 보고서로 내려받을 수 있습니다.</div>',
        unsafe_allow_html=True
    )

    profile = st.session_state.last_profile
    all_job_names = list(get_all_careers().keys())

    default_jobs = st.session_state.favorites or st.session_state.recommended_jobs

    selected_report_jobs = st.multiselect(
        "보고서에 포함할 직업을 선택하세요.",
        options=all_job_names,
        default=[job for job in default_jobs if job in all_job_names]
    )

    if selected_report_jobs:
        text_report = create_text_report(profile, selected_report_jobs)
        pdf_report = create_pdf_report(profile, selected_report_jobs)

        st.markdown("#### 보고서에 저장될 학생 정보")
        info1, info2, info3, info4 = st.columns(4)
        info1.metric("MBTI", profile["mbti"])
        info2.metric("흥미 분야", len(profile["interests"]))
        info3.metric("적성", len(profile["aptitudes"]))
        info4.metric("저장 직업", len(selected_report_jobs))

        download1, download2 = st.columns(2)

        with download1:
            st.download_button(
                label="📝 TXT 보고서 다운로드",
                data=text_report.encode("utf-8"),
                file_name="진로탐색_결과.txt",
                mime="text/plain",
                use_container_width=True
            )

        with download2:
            st.download_button(
                label="📄 PDF 보고서 다운로드",
                data=pdf_report,
                file_name="진로탐색_결과.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        with st.expander("TXT 보고서 미리 보기"):
            st.text(text_report)

    else:
        st.info("보고서에 넣을 직업을 1개 이상 선택하세요.")


# =========================================================
# 하단 안내
# =========================================================
st.markdown("""
<div class="footer-note">
    MBTI 결과는 진로 탐색의 출발점입니다. 관심 직업의 실제 업무, 관련 학과, 필요한 역량을 추가로 조사해 보세요.
</div>
""", unsafe_allow_html=True)
