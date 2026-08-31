import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from io import BytesIO
from datetime import datetime


# =========================================================
# 1. 페이지 기본 설정
# =========================================================
st.set_page_config(
    page_title="MBTI 진로 탐색 프로그램",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# 2. 세션 상태 초기화
# =========================================================
if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "custom_jobs" not in st.session_state:
    st.session_state.custom_jobs = []

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if "selected_jobs" not in st.session_state:
    st.session_state.selected_jobs = []


# =========================================================
# 3. 다크 모드 스타일
# =========================================================
def apply_theme():
    if st.session_state.dark_mode:
        st.markdown("""
        <style>
            .stApp {
                background-color: #121212;
                color: #F5F5F5;
            }

            [data-testid="stSidebar"] {
                background-color: #1E1E1E;
            }

            h1, h2, h3, h4, p, span, label {
                color: #F5F5F5 !important;
            }

            .stTabs [data-baseweb="tab-list"] {
                background-color: #1E1E1E;
            }

            .stTabs [data-baseweb="tab"] {
                color: #F5F5F5;
            }

            .stTextInput input,
            .stTextArea textarea,
            .stSelectbox div,
            .stMultiSelect div {
                background-color: #2A2A2A !important;
                color: white !important;
            }

            div[data-testid="stExpander"] {
                background-color: #242424;
                border: 1px solid #555555;
            }
        </style>
        """)
    else:
        st.markdown("""
        <style>
            .stApp {
                background-color: #F8FAFC;
            }

            .career-card {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 15px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            }
        </style>
        """)


apply_theme()


# =========================================================
# 4. 직업 데이터
# =========================================================
career_data = {
    "소프트웨어 개발자": {
        "description": "웹사이트, 앱, 인공지능 서비스 등 다양한 컴퓨터 프로그램을 설계하고 개발합니다.",
        "majors": ["컴퓨터공학과", "소프트웨어학과", "인공지능학과", "정보통신공학과"],
        "subjects": ["정보", "수학", "영어", "물리학"],
        "skills": ["논리적 사고력", "문제 해결력", "프로그래밍 능력", "협업 능력"],
        "certificates": ["정보처리기능사", "정보처리기사", "SQLD", "ADsP"],
        "interests": ["IT·기술", "문제 해결", "창작"],
        "aptitudes": ["논리력", "분석력", "집중력"]
    },

    "데이터 분석가": {
        "description": "숫자와 데이터를 분석하여 의미 있는 정보와 문제 해결 방향을 찾는 직업입니다.",
        "majors": ["데이터사이언스학과", "통계학과", "컴퓨터공학과", "산업공학과"],
        "subjects": ["수학", "확률과 통계", "정보", "영어"],
        "skills": ["통계적 사고력", "분석력", "프로그래밍 능력", "자료 해석 능력"],
        "certificates": ["ADsP", "SQLD", "빅데이터분석기사"],
        "interests": ["IT·기술", "수학", "문제 해결"],
        "aptitudes": ["분석력", "논리력", "꼼꼼함"]
    },

    "인공지능 연구원": {
        "description": "인공지능 기술을 연구하고, 사람들의 생활에 활용할 수 있는 새로운 시스템을 개발합니다.",
        "majors": ["인공지능학과", "컴퓨터공학과", "전자공학과", "수학과"],
        "subjects": ["수학", "정보", "물리학", "영어"],
        "skills": ["수학적 사고력", "연구 능력", "프로그래밍 능력", "창의적 문제 해결력"],
        "certificates": ["정보처리기사", "ADsP", "빅데이터분석기사"],
        "interests": ["IT·기술", "과학", "연구"],
        "aptitudes": ["논리력", "분석력", "창의력"]
    },

    "게임 개발자": {
        "description": "게임의 프로그램, 그래픽, 시스템, 스토리 등을 제작하여 게임을 개발합니다.",
        "majors": ["게임학과", "컴퓨터공학과", "소프트웨어학과", "디지털콘텐츠학과"],
        "subjects": ["정보", "수학", "미술", "영어"],
        "skills": ["프로그래밍 능력", "창의력", "협업 능력", "문제 해결력"],
        "certificates": ["정보처리기능사", "정보처리기사"],
        "interests": ["IT·기술", "창작", "게임"],
        "aptitudes": ["창의력", "논리력", "집중력"]
    },

    "정보보안 전문가": {
        "description": "해킹, 개인정보 유출, 악성코드 등 사이버 위협으로부터 시스템과 정보를 보호합니다.",
        "majors": ["정보보호학과", "컴퓨터공학과", "사이버보안학과"],
        "subjects": ["정보", "수학", "영어", "물리학"],
        "skills": ["분석력", "문제 해결력", "보안 지식", "꼼꼼함"],
        "certificates": ["정보보안기사", "정보처리기사", "네트워크관리사"],
        "interests": ["IT·기술", "문제 해결", "연구"],
        "aptitudes": ["분석력", "논리력", "꼼꼼함"]
    },

    "간호사": {
        "description": "환자의 건강 상태를 확인하고 치료, 회복, 건강 관리를 돕는 의료 전문 직업입니다.",
        "majors": ["간호학과"],
        "subjects": ["생명과학", "화학", "보건", "영어"],
        "skills": ["공감 능력", "책임감", "의사소통 능력", "관찰력"],
        "certificates": ["간호사 국가고시"],
        "interests": ["의료·보건", "사람 돕기", "과학"],
        "aptitudes": ["공감력", "책임감", "관찰력"]
    },

    "의사": {
        "description": "환자를 진단하고 치료하며 질병을 예방하기 위한 의료 활동을 수행합니다.",
        "majors": ["의예과", "의학과"],
        "subjects": ["생명과학", "화학", "수학", "영어"],
        "skills": ["분석력", "책임감", "판단력", "의사소통 능력"],
        "certificates": ["의사 국가고시"],
        "interests": ["의료·보건", "과학", "사람 돕기"],
        "aptitudes": ["분석력", "책임감", "집중력"]
    },

    "심리학 연구원": {
        "description": "사람의 생각, 감정, 행동을 과학적으로 연구하고 분석합니다.",
        "majors": ["심리학과", "상담심리학과", "교육학과"],
        "subjects": ["사회·문화", "생활과 윤리", "생명과학", "영어"],
        "skills": ["공감 능력", "분석력", "관찰력", "연구 능력"],
        "certificates": ["임상심리사", "청소년상담사"],
        "interests": ["사람 돕기", "연구", "사회"],
        "aptitudes": ["공감력", "분석력", "관찰력"]
    },

    "사회복지사": {
        "description": "도움이 필요한 사람에게 복지 서비스와 필요한 정보를 연결하고 지원합니다.",
        "majors": ["사회복지학과", "사회학과", "심리학과"],
        "subjects": ["사회·문화", "생활과 윤리", "정치와 법"],
        "skills": ["공감 능력", "의사소통 능력", "책임감", "문제 해결력"],
        "certificates": ["사회복지사 1급", "사회복지사 2급"],
        "interests": ["사람 돕기", "사회", "교육"],
        "aptitudes": ["공감력", "의사소통", "책임감"]
    },

    "교사": {
        "description": "학생의 학습과 성장을 돕고, 수업과 생활지도를 통해 교육 활동을 수행합니다.",
        "majors": ["교육학과", "국어교육과", "수학교육과", "영어교육과", "과학교육과"],
        "subjects": ["관심 교과", "국어", "영어", "사회·문화"],
        "skills": ["의사소통 능력", "설명 능력", "공감 능력", "책임감"],
        "certificates": ["중등학교 정교사 자격증"],
        "interests": ["교육", "사람 돕기", "사회"],
        "aptitudes": ["의사소통", "공감력", "책임감"]
    },

    "변호사": {
        "description": "법률 지식을 바탕으로 개인과 사회의 다양한 분쟁 및 문제 해결을 돕습니다.",
        "majors": ["법학과", "정치외교학과", "행정학과"],
        "subjects": ["정치와 법", "사회·문화", "국어", "영어"],
        "skills": ["논리적 사고력", "말하기 능력", "문서 작성 능력", "분석력"],
        "certificates": ["변호사 시험"],
        "interests": ["사회", "토론", "문제 해결"],
        "aptitudes": ["논리력", "의사소통", "분석력"]
    },

    "공무원": {
        "description": "국가 또는 지방자치단체에서 시민의 생활과 관련된 행정 업무를 수행합니다.",
        "majors": ["행정학과", "정치외교학과", "법학과", "사회복지학과"],
        "subjects": ["정치와 법", "사회·문화", "한국사", "국어"],
        "skills": ["책임감", "문서 작성 능력", "꼼꼼함", "의사소통 능력"],
        "certificates": ["공무원 공개채용시험"],
        "interests": ["사회", "사람 돕기", "문제 해결"],
        "aptitudes": ["책임감", "꼼꼼함", "의사소통"]
    },

    "회계사": {
        "description": "기업이나 기관의 재무 상태를 분석하고 회계 자료를 검토하는 전문가입니다.",
        "majors": ["회계학과", "경영학과", "경제학과", "세무학과"],
        "subjects": ["수학", "경제", "정치와 법", "영어"],
        "skills": ["계산 능력", "분석력", "꼼꼼함", "책임감"],
        "certificates": ["공인회계사(CPA)", "세무사"],
        "interests": ["수학", "경제", "문제 해결"],
        "aptitudes": ["분석력", "꼼꼼함", "논리력"]
    },

    "경영 컨설턴트": {
        "description": "기업이나 조직의 문제를 분석하고 성장 전략과 개선 방향을 제안합니다.",
        "majors": ["경영학과", "경제학과", "산업공학과", "행정학과"],
        "subjects": ["경제", "수학", "사회·문화", "영어"],
        "skills": ["분석력", "발표 능력", "문제 해결력", "의사소통 능력"],
        "certificates": ["경영지도사", "PMP", "SQLD"],
        "interests": ["경제", "문제 해결", "리더십"],
        "aptitudes": ["분석력", "의사소통", "리더십"]
    },

    "기계공학자": {
        "description": "기계와 장치를 설계하고, 제품의 성능과 안전성을 개선합니다.",
        "majors": ["기계공학과", "로봇공학과", "자동차공학과"],
        "subjects": ["수학", "물리학", "정보", "화학"],
        "skills": ["공간지각력", "문제 해결력", "수학적 사고력", "설계 능력"],
        "certificates": ["일반기계기사", "기계설계기사"],
        "interests": ["과학", "IT·기술", "만들기"],
        "aptitudes": ["논리력", "공간지각력", "문제 해결력"]
    },

    "건축가": {
        "description": "건물과 공간을 안전하고 아름답게 설계하며 건축 과정을 계획합니다.",
        "majors": ["건축학과", "건축공학과", "실내건축학과"],
        "subjects": ["수학", "미술", "물리학", "정보"],
        "skills": ["공간지각력", "창의력", "설계 능력", "문제 해결력"],
        "certificates": ["건축사", "건축기사"],
        "interests": ["미술", "만들기", "과학"],
        "aptitudes": ["창의력", "공간지각력", "집중력"]
    },

    "그래픽 디자이너": {
        "description": "색상, 이미지, 글자 등을 활용해 사람들에게 효과적으로 메시지를 전달하는 시각물을 제작합니다.",
        "majors": ["시각디자인학과", "디자인학과", "디지털콘텐츠학과"],
        "subjects": ["미술", "정보", "국어", "영어"],
        "skills": ["창의력", "미적 감각", "디지털 도구 활용 능력", "의사소통 능력"],
        "certificates": ["GTQ", "컴퓨터그래픽스운용기능사"],
        "interests": ["미술", "창작", "IT·기술"],
        "aptitudes": ["창의력", "관찰력", "집중력"]
    },

    "웹툰 작가": {
        "description": "그림과 이야기를 결합하여 웹툰 콘텐츠를 기획하고 제작합니다.",
        "majors": ["만화애니메이션학과", "웹툰학과", "시각디자인학과"],
        "subjects": ["미술", "국어", "정보", "사회·문화"],
        "skills": ["그림 실력", "스토리텔링", "창의력", "꾸준함"],
        "certificates": ["필수 자격증 없음", "GTQ(활용 가능)"],
        "interests": ["미술", "창작", "글쓰기"],
        "aptitudes": ["창의력", "집중력", "관찰력"]
    },

    "작가": {
        "description": "소설, 에세이, 시나리오, 기사 등 글을 통해 생각과 이야기를 전달합니다.",
        "majors": ["국어국문학과", "문예창작학과", "신문방송학과"],
        "subjects": ["국어", "문학", "사회·문화", "영어"],
        "skills": ["글쓰기 능력", "관찰력", "창의력", "표현력"],
        "certificates": ["필수 자격증 없음"],
        "interests": ["글쓰기", "창작", "사회"],
        "aptitudes": ["창의력", "관찰력", "표현력"]
    },

    "광고기획자": {
        "description": "제품이나 서비스의 장점을 효과적으로 알릴 수 있도록 광고 전략과 콘텐츠를 기획합니다.",
        "majors": ["광고홍보학과", "신문방송학과", "경영학과", "디자인학과"],
        "subjects": ["사회·문화", "국어", "미술", "영어"],
        "skills": ["창의력", "기획력", "의사소통 능력", "트렌드 분석력"],
        "certificates": ["검색광고마케터", "SNS광고마케터"],
        "interests": ["창작", "사회", "경제"],
        "aptitudes": ["창의력", "의사소통", "기획력"]
    },

    "마케팅 전문가": {
        "description": "소비자와 시장을 분석하여 제품과 서비스의 가치를 알리는 전략을 세웁니다.",
        "majors": ["경영학과", "광고홍보학과", "경제학과", "미디어커뮤니케이션학과"],
        "subjects": ["경제", "사회·문화", "수학", "영어"],
        "skills": ["분석력", "기획력", "의사소통 능력", "창의력"],
        "certificates": ["검색광고마케터", "ADsP", "사회조사분석사"],
        "interests": ["경제", "창작", "사회"],
        "aptitudes": ["분석력", "창의력", "의사소통"]
    },

    "행사 기획자": {
        "description": "축제, 공연, 전시, 기업 행사 등 다양한 행사를 기획하고 운영합니다.",
        "majors": ["관광경영학과", "문화콘텐츠학과", "광고홍보학과", "이벤트학과"],
        "subjects": ["사회·문화", "국어", "영어", "미술"],
        "skills": ["기획력", "의사소통 능력", "문제 해결력", "협업 능력"],
        "certificates": ["컨벤션기획사", "국내여행안내사"],
        "interests": ["사람 만나기", "창작", "여행"],
        "aptitudes": ["의사소통", "기획력", "리더십"]
    },

    "스포츠 선수": {
        "description": "운동 종목에서 전문적인 훈련을 하고 경기력을 발전시키며 대회에 참가합니다.",
        "majors": ["체육학과", "스포츠과학과", "사회체육학과"],
        "subjects": ["체육", "생명과학", "보건"],
        "skills": ["운동 능력", "끈기", "자기관리 능력", "협업 능력"],
        "certificates": ["생활스포츠지도사", "전문스포츠지도사"],
        "interests": ["스포츠", "건강", "경쟁"],
        "aptitudes": ["신체운동능력", "끈기", "자기관리"]
    },

    "경찰관": {
        "description": "범죄를 예방하고 시민의 안전을 보호하며 사건과 사고에 대응합니다.",
        "majors": ["경찰행정학과", "법학과", "행정학과"],
        "subjects": ["정치와 법", "사회·문화", "체육", "국어"],
        "skills": ["판단력", "책임감", "체력", "의사소통 능력"],
        "certificates": ["경찰공무원 채용시험", "태권도 등 무도 단증"],
        "interests": ["사회", "사람 돕기", "스포츠"],
        "aptitudes": ["책임감", "판단력", "신체운동능력"]
    },

    "소방관": {
        "description": "화재와 재난 현장에서 사람들의 생명과 안전을 지키는 일을 합니다.",
        "majors": ["소방방재학과", "응급구조학과", "안전공학과"],
        "subjects": ["체육", "생명과학", "화학", "물리학"],
        "skills": ["체력", "위기 대처 능력", "책임감", "협업 능력"],
        "certificates": ["소방공무원 채용시험", "응급구조사"],
        "interests": ["사람 돕기", "스포츠", "과학"],
        "aptitudes": ["신체운동능력", "책임감", "판단력"]
    },

    "항공정비사": {
        "description": "항공기의 안전한 운항을 위해 기체와 엔진, 전자 장비를 점검하고 정비합니다.",
        "majors": ["항공정비학과", "항공운항학과", "기계공학과"],
        "subjects": ["물리학", "수학", "정보", "영어"],
        "skills": ["꼼꼼함", "기계 이해력", "문제 해결력", "책임감"],
        "certificates": ["항공정비사 자격증"],
        "interests": ["과학", "IT·기술", "만들기"],
        "aptitudes": ["꼼꼼함", "공간지각력", "책임감"]
    },

    "환경 연구원": {
        "description": "기후 변화, 대기 오염, 생태계 등 환경 문제를 조사하고 해결 방법을 연구합니다.",
        "majors": ["환경공학과", "환경과학과", "생명과학과", "지구과학과"],
        "subjects": ["지구과학", "생명과학", "화학", "수학"],
        "skills": ["연구 능력", "분석력", "문제 해결력", "관찰력"],
        "certificates": ["환경기사", "대기환경기사", "수질환경기사"],
        "interests": ["환경", "과학", "연구"],
        "aptitudes": ["분석력", "관찰력", "책임감"]
    },

    "여행 기획자": {
        "description": "여행객의 목적과 관심에 맞는 여행 상품과 체험 프로그램을 기획합니다.",
        "majors": ["관광경영학과", "호텔관광학과", "국제학과"],
        "subjects": ["영어", "세계지리", "사회·문화", "국어"],
        "skills": ["기획력", "의사소통 능력", "외국어 능력", "창의력"],
        "certificates": ["국내여행안내사", "관광통역안내사"],
        "interests": ["여행", "사람 만나기", "외국어"],
        "aptitudes": ["의사소통", "기획력", "창의력"]
    },

    "호텔리어": {
        "description": "호텔을 방문한 고객이 편안하게 머물 수 있도록 객실, 예약, 서비스 업무를 수행합니다.",
        "majors": ["호텔경영학과", "관광경영학과", "항공서비스학과"],
        "subjects": ["영어", "중국어", "사회·문화", "국어"],
        "skills": ["서비스 정신", "외국어 능력", "의사소통 능력", "문제 해결력"],
        "certificates": ["호텔서비스사", "호텔관리사"],
        "interests": ["사람 만나기", "여행", "외국어"],
        "aptitudes": ["의사소통", "공감력", "문제 해결력"]
    }
}


# =========================================================
# 5. MBTI별 기본 추천 직업
# =========================================================
mbti_recommendations = {
    "ISTJ": ["회계사", "공무원", "품질관리 전문가"],
    "ISFJ": ["간호사", "사회복지사", "교사"],
    "INFJ": ["심리학 연구원", "작가", "환경 연구원"],
    "INTJ": ["소프트웨어 개발자", "데이터 분석가", "인공지능 연구원"],
    "ISTP": ["기계공학자", "항공정비사", "소방관"],
    "ISFP": ["그래픽 디자이너", "웹툰 작가", "호텔리어"],
    "INFP": ["작가", "웹툰 작가", "사회복지사"],
    "INTP": ["과학자", "게임 개발자", "정보보안 전문가"],
    "ESTP": ["경찰관", "스포츠 선수", "행사 기획자"],
    "ESFP": ["행사 기획자", "호텔리어", "여행 기획자"],
    "ENFP": ["광고기획자", "콘텐츠 크리에이터", "여행 기획자"],
    "ENTP": ["창업가", "변호사", "마케팅 전문가"],
    "ESTJ": ["경영 컨설턴트", "공무원", "회계사"],
    "ESFJ": ["교사", "간호사", "호텔리어"],
    "ENFJ": ["교사", "사회복지사", "광고기획자"],
    "ENTJ": ["경영 컨설턴트", "마케팅 전문가", "소프트웨어 개발자"]
}


# 직업 데이터에 존재하지 않는 직업을 위한 기본 정보
default_career_info = {
    "description": "이 직업에 대한 세부 정보를 추가로 조사해 보세요.",
    "majors": ["관련 학과 탐색 필요"],
    "subjects": ["관련 과목 탐색 필요"],
    "skills": ["문제 해결력", "의사소통 능력", "자기관리 능력"],
    "certificates": ["직업별 자격 정보 탐색 필요"],
    "interests": [],
    "aptitudes": []
}


# =========================================================
# 6. 도우미 함수
# =========================================================
def get_all_careers():
    """기본 직업 데이터와 학생이 추가한 직업 데이터를 합칩니다."""
    all_data = career_data.copy()

    for job in st.session_state.custom_jobs:
        all_data[job["name"]] = {
            "description": job["description"],
            "majors": job["majors"],
            "subjects": job["subjects"],
            "skills": job["skills"],
            "certificates": job["certificates"],
            "interests": job["interests"],
            "aptitudes": job["aptitudes"]
        }

    return all_data


def get_career_info(job_name):
    all_careers = get_all_careers()
    return all_careers.get(job_name, default_career_info)


def create_career_card(job_name, key_prefix="career"):
    """직업 정보를 화면 카드 형태로 보여줍니다."""
    info = get_career_info(job_name)

    with st.expander(f"💼 {job_name}", expanded=False):
        st.write(f"**직업 소개**  \n{info['description']}")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**🏫 관련 학과**")
            st.write(", ".join(info["majors"]))

            st.write("**📚 추천 과목**")
            st.write(", ".join(info["subjects"]))

        with col2:
            st.write("**🧠 필요한 역량**")
            st.write(", ".join(info["skills"]))

            st.write("**📜 관련 자격증·시험**")
            st.write(", ".join(info["certificates"]))

        if job_name in st.session_state.favorites:
            if st.button("⭐ 즐겨찾기 해제", key=f"{key_prefix}_remove_{job_name}"):
                st.session_state.favorites.remove(job_name)
                st.rerun()
        else:
            if st.button("☆ 즐겨찾기에 저장", key=f"{key_prefix}_add_{job_name}"):
                st.session_state.favorites.append(job_name)
                st.success(f"'{job_name}' 직업을 즐겨찾기에 저장했습니다.")
                st.rerun()


def make_recommendation(mbti, interests, aptitudes, subjects):
    """
    MBTI 추천과 흥미/적성/과목 조건을 점수화하여 직업을 추천합니다.
    """
    all_careers = get_all_careers()
    scores = {}

    for job_name, info in all_careers.items():
        score = 0

        # MBTI 기본 추천 직업이면 높은 점수
        if job_name in mbti_recommendations.get(mbti, []):
            score += 5

        # 흥미 점수
        score += len(set(interests) & set(info.get("interests", []))) * 3

        # 적성 점수
        score += len(set(aptitudes) & set(info.get("aptitudes", []))) * 3

        # 좋아하는 과목 점수
        score += len(set(subjects) & set(info.get("subjects", []))) * 2

        scores[job_name] = score

    # 점수 높은 순으로 정렬
    sorted_jobs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # 점수가 있는 직업 우선 6개 선택
    recommended = [job for job, score in sorted_jobs if score > 0][:6]

    # 조건이 부족해 결과가 적을 경우 MBTI 추천을 기본으로 사용
    if len(recommended) < 3:
        for job in mbti_recommendations.get(mbti, []):
            if job not in recommended:
                recommended.append(job)

    return recommended[:6]


def create_text_report(mbti, interests, aptitudes, subjects, jobs):
    """TXT 파일로 저장할 진로 탐색 보고서를 만듭니다."""
    report = []
    report.append("=" * 55)
    report.append("MBTI 진로 탐색 결과 보고서")
    report.append("=" * 55)
    report.append(f"생성 날짜: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("")
    report.append(f"MBTI: {mbti}")
    report.append(f"흥미 분야: {', '.join(interests) if interests else '선택하지 않음'}")
    report.append(f"나의 적성: {', '.join(aptitudes) if aptitudes else '선택하지 않음'}")
    report.append(f"좋아하는 과목: {', '.join(subjects) if subjects else '선택하지 않음'}")
    report.append("")
    report.append("[ 추천 직업 ]")

    for index, job_name in enumerate(jobs, start=1):
        info = get_career_info(job_name)

        report.append("")
        report.append(f"{index}. {job_name}")
        report.append(f"- 직업 소개: {info['description']}")
        report.append(f"- 관련 학과: {', '.join(info['majors'])}")
        report.append(f"- 추천 과목: {', '.join(info['subjects'])}")
        report.append(f"- 필요한 역량: {', '.join(info['skills'])}")
        report.append(f"- 관련 자격증·시험: {', '.join(info['certificates'])}")

    report.append("")
    report.append("=" * 55)
    report.append("진로 탐색 질문")
    report.append("=" * 55)
    report.append("1. 추천 직업 중 내가 가장 관심 있는 직업은 무엇인가?")
    report.append("2. 이 직업을 위해 고등학교에서 어떤 과목을 더 공부하면 좋을까?")
    report.append("3. 이 직업과 연결되는 학과와 대학교를 조사해 보자.")
    report.append("4. 내가 경험해 보고 싶은 활동은 무엇인가?")

    return "\n".join(report)


def create_pdf_report(mbti, interests, aptitudes, subjects, jobs):
    """
    reportlab을 이용해 한글 PDF 보고서를 생성합니다.
    UnicodeCIDFont를 사용하므로 한글 표시가 가능합니다.
    """
    buffer = BytesIO()

    pdfmetrics.registerFont(UnicodeCIDFont("HYSMyeongJo-Medium"))

    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    x = 20 * mm
    y = height - 20 * mm

    pdf.setFont("HYSMyeongJo-Medium", 18)
    pdf.drawString(x, y, "MBTI 진로 탐색 결과 보고서")
    y -= 12 * mm

    pdf.setFont("HYSMyeongJo-Medium", 10)
    pdf.drawString(x, y, f"생성 날짜: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y -= 8 * mm

    basic_lines = [
        f"MBTI: {mbti}",
        f"흥미 분야: {', '.join(interests) if interests else '선택하지 않음'}",
        f"나의 적성: {', '.join(aptitudes) if aptitudes else '선택하지 않음'}",
        f"좋아하는 과목: {', '.join(subjects) if subjects else '선택하지 않음'}"
    ]

    for line in basic_lines:
        pdf.drawString(x, y, line)
        y -= 7 * mm

    y -= 4 * mm

    pdf.setFont("HYSMyeongJo-Medium", 14)
    pdf.drawString(x, y, "추천 직업")
    y -= 9 * mm

    for index, job_name in enumerate(jobs, start=1):
        info = get_career_info(job_name)

        lines = [
            f"{index}. {job_name}",
            f"직업 소개: {info['description']}",
            f"관련 학과: {', '.join(info['majors'])}",
            f"추천 과목: {', '.join(info['subjects'])}",
            f"필요 역량: {', '.join(info['skills'])}",
            f"자격증·시험: {', '.join(info['certificates'])}"
        ]

        for line in lines:
            # 페이지 공간이 부족하면 새 페이지 생성
            if y < 25 * mm:
                pdf.showPage()
                pdf.setFont("HYSMyeongJo-Medium", 10)
                y = height - 20 * mm

            pdf.setFont("HYSMyeongJo-Medium", 10)
            pdf.drawString(x, y, line[:85])
            y -= 6 * mm

        y -= 4 * mm

    if y < 45 * mm:
        pdf.showPage()
        y = height - 20 * mm

    pdf.setFont("HYSMyeongJo-Medium", 13)
    pdf.drawString(x, y, "진로 탐색 질문")
    y -= 8 * mm

    pdf.setFont("HYSMyeongJo-Medium", 10)

    questions = [
        "1. 추천 직업 중 내가 가장 관심 있는 직업은 무엇인가?",
        "2. 이 직업을 위해 어떤 과목과 활동을 더 탐색하면 좋을까?",
        "3. 관련 학과와 진학 방법을 조사해 보자.",
        "4. 직접 체험하거나 인터뷰해 보고 싶은 직업은 무엇인가?"
    ]

    for question in questions:
        pdf.drawString(x, y, question)
        y -= 7 * mm

    pdf.save()
    buffer.seek(0)

    return buffer


# =========================================================
# 7. 사이드바
# =========================================================
with st.sidebar:
    st.title("⚙️ 설정")

    dark_mode_value = st.toggle(
        "🌙 다크 모드",
        value=st.session_state.dark_mode
    )

    if dark_mode_value != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode_value
        st.rerun()

    st.divider()

    st.write("### ⭐ 즐겨찾기")
    st.write(f"저장한 직업 수: **{len(st.session_state.favorites)}개**")

    if st.session_state.favorites:
        for favorite in st.session_state.favorites:
            st.write(f"• {favorite}")

    st.divider()

    st.caption(
        "MBTI는 진로를 결정하는 도구가 아니라 "
        "자신의 흥미와 강점을 탐색하기 위한 참고 자료입니다."
    )


# =========================================================
# 8. 제목
# =========================================================
st.title("🎓 MBTI 진로 탐색 프로그램")
st.write("MBTI, 흥미, 적성, 좋아하는 과목을 바탕으로 다양한 직업을 탐색해 보세요.")

st.info(
    "💡 추천 결과만으로 진로를 결정하지 말고, "
    "관심 직업의 실제 업무, 관련 학과, 필요한 역량을 추가로 조사해 보세요."
)


# =========================================================
# 9. 탭 구성
# =========================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 맞춤 직업 추천",
    "🔎 직업 검색",
    "⭐ 즐겨찾기",
    "➕ 나만의 직업 추가",
    "📄 결과 저장"
])


# =========================================================
# 10. 맞춤 직업 추천 탭
# =========================================================
with tab1:
    st.subheader("나의 성향으로 직업 탐색하기")

    col1, col2 = st.columns(2)

    with col1:
        selected_mbti = st.selectbox(
            "1. 나의 MBTI 선택",
            options=list(mbti_recommendations.keys())
        )

        selected_interests = st.multiselect(
            "2. 관심 있는 분야 선택",
            options=[
                "IT·기술", "과학", "의료·보건", "교육", "사회",
                "경제", "미술", "창작", "글쓰기", "스포츠",
                "환경", "여행", "외국어", "사람 돕기",
                "문제 해결", "만들기", "리더십", "토론", "게임"
            ]
        )

    with col2:
        selected_aptitudes = st.multiselect(
            "3. 내가 잘한다고 생각하는 능력 선택",
            options=[
                "논리력", "분석력", "창의력", "공감력",
                "의사소통", "책임감", "꼼꼼함", "집중력",
                "관찰력", "기획력", "리더십", "판단력",
                "공간지각력", "신체운동능력", "표현력",
                "문제 해결력", "자기관리"
            ]
        )

        selected_subjects = st.multiselect(
            "4. 좋아하거나 관심 있는 과목 선택",
            options=[
                "국어", "문학", "수학", "확률과 통계", "영어",
                "사회·문화", "정치와 법", "생활과 윤리", "경제",
                "한국사", "세계지리", "물리학", "화학",
                "생명과학", "지구과학", "정보", "미술", "체육",
                "보건", "중국어"
            ]
        )

    if st.button("✨ 맞춤 직업 추천받기", use_container_width=True):
        st.session_state.selected_jobs = make_recommendation(
            selected_mbti,
            selected_interests,
            selected_aptitudes,
            selected_subjects
        )

        st.success("나의 선택을 바탕으로 직업을 추천했습니다.")

    if st.session_state.selected_jobs:
        st.divider()
        st.subheader("💼 추천 직업")

        st.write(
            f"**{selected_mbti}** 유형과 선택한 관심 분야, 적성, 과목을 참고하여 "
            f"다음 직업을 탐색해 볼 수 있습니다."
        )

        for job_name in st.session_state.selected_jobs:
            create_career_card(job_name, key_prefix="recommend")

        st.warning(
            "추천 직업은 참고 자료입니다. "
            "직업을 선택하기 전에는 관련 학과, 대학, 실제 업무, 진로 체험 활동을 함께 조사해 보세요."
        )


# =========================================================
# 11. 직업 검색 탭
# =========================================================
with tab2:
    st.subheader("직업 검색")

    search_keyword = st.text_input(
        "직업명 또는 관심 키워드를 입력하세요.",
        placeholder="예: 개발자, 간호, 디자인, 환경, 교육"
    )

    all_careers = get_all_careers()

    if search_keyword:
        search_keyword = search_keyword.lower()

        searched_jobs = []

        for job_name, info in all_careers.items():
            searchable_text = " ".join([
                job_name,
                info["description"],
                " ".join(info["majors"]),
                " ".join(info["subjects"]),
                " ".join(info["skills"]),
                " ".join(info["interests"])
            ]).lower()

            if search_keyword in searchable_text:
                searched_jobs.append(job_name)

        if searched_jobs:
            st.success(f"총 {len(searched_jobs)}개의 직업 정보를 찾았습니다.")

            for job_name in searched_jobs:
                create_career_card(job_name, key_prefix="search")
        else:
            st.warning("검색 결과가 없습니다. 다른 키워드로 다시 검색해 보세요.")

    else:
        st.caption("검색어를 입력하면 직업, 학과, 과목, 역량 등을 기준으로 탐색할 수 있습니다.")


# =========================================================
# 12. 즐겨찾기 탭
# =========================================================
with tab3:
    st.subheader("⭐ 내가 저장한 관심 직업")

    if not st.session_state.favorites:
        st.info("아직 저장한 직업이 없습니다. 추천 결과나 직업 검색에서 관심 직업을 저장해 보세요.")
    else:
        st.write(f"총 **{len(st.session_state.favorites)}개**의 직업을 저장했습니다.")

        for job_name in st.session_state.favorites.copy():
            create_career_card(job_name, key_prefix="favorite")


# =========================================================
# 13. 나만의 직업 추가 탭
# =========================================================
with tab4:
    st.subheader("➕ 직접 직업 정보 추가하기")
    st.write("내가 새롭게 조사한 직업 정보를 직접 추가할 수 있습니다.")

    with st.form("custom_job_form"):
        job_name = st.text_input("직업 이름", placeholder="예: 로봇공학자")
        job_description = st.text_area(
            "직업 소개",
            placeholder="이 직업에서 하는 일을 간단하게 작성하세요."
        )

        col1, col2 = st.columns(2)

        with col1:
            job_majors = st.text_input(
                "관련 학과",
                placeholder="쉼표(,)로 구분하세요. 예: 로봇공학과, 기계공학과"
            )

            job_subjects = st.text_input(
                "추천 과목",
                placeholder="예: 수학, 물리학, 정보"
            )

            job_interests = st.text_input(
                "관련 흥미 분야",
                placeholder="예: IT·기술, 과학, 만들기"
            )

        with col2:
            job_skills = st.text_input(
                "필요한 역량",
                placeholder="예: 논리력, 창의력, 문제 해결력"
            )

            job_certificates = st.text_input(
                "관련 자격증 또는 시험",
                placeholder="예: 정보처리기사, 관련 국가시험"
            )

            job_aptitudes = st.text_input(
                "관련 적성",
                placeholder="예: 분석력, 공간지각력, 집중력"
            )

        submit_custom_job = st.form_submit_button("직업 정보 추가하기")

    if submit_custom_job:
        if not job_name.strip():
            st.error("직업 이름은 반드시 입력해야 합니다.")
        else:
            new_job = {
                "name": job_name.strip(),
                "description": job_description.strip() if job_description.strip() else "직업 소개를 추가해 주세요.",
                "majors": [item.strip() for item in job_majors.split(",") if item.strip()] or ["관련 학과 조사 필요"],
                "subjects": [item.strip() for item in job_subjects.split(",") if item.strip()] or ["관련 과목 조사 필요"],
                "skills": [item.strip() for item in job_skills.split(",") if item.strip()] or ["필요 역량 조사 필요"],
                "certificates": [item.strip() for item in job_certificates.split(",") if item.strip()] or ["관련 자격 정보 조사 필요"],
                "interests": [item.strip() for item in job_interests.split(",") if item.strip()],
                "aptitudes": [item.strip() for item in job_aptitudes.split(",") if item.strip()]
            }

            # 같은 이름의 직업이 있다면 기존 항목을 제거 후 새 정보 저장
            st.session_state.custom_jobs = [
                job for job in st.session_state.custom_jobs
                if job["name"] != job_name.strip()
            ]

            st.session_state.custom_jobs.append(new_job)

            st.success(f"'{job_name}' 직업 정보를 추가했습니다.")

    if st.session_state.custom_jobs:
        st.divider()
        st.write("### 내가 추가한 직업 목록")

        for job in st.session_state.custom_jobs:
            col1, col2 = st.columns([5, 1])

            with col1:
                st.write(f"• **{job['name']}**")

            with col2:
                if st.button("삭제", key=f"delete_{job['name']}"):
                    st.session_state.custom_jobs = [
                        item for item in st.session_state.custom_jobs
                        if item["name"] != job["name"]
                    ]

                    if job["name"] in st.session_state.favorites:
                        st.session_state.favorites.remove(job["name"])

                    st.rerun()


# =========================================================
# 14. 결과 저장 탭
# =========================================================
with tab5:
    st.subheader("📄 진로 탐색 결과 저장")

    save_mbti = st.selectbox(
        "MBTI 선택",
        options=list(mbti_recommendations.keys()),
        key="save_mbti"
    )

    save_interests = st.multiselect(
        "흥미 분야",
        options=[
            "IT·기술", "과학", "의료·보건", "교육", "사회",
            "경제", "미술", "창작", "글쓰기", "스포츠",
            "환경", "여행", "외국어", "사람 돕기",
            "문제 해결", "만들기", "리더십", "토론", "게임"
        ],
        key="save_interests"
    )

    save_aptitudes = st.multiselect(
        "적성",
        options=[
            "논리력", "분석력", "창의력", "공감력",
            "의사소통", "책임감", "꼼꼼함", "집중력",
            "관찰력", "기획력", "리더십", "판단력",
            "공간지각력", "신체운동능력", "표현력",
            "문제 해결력", "자기관리"
        ],
        key="save_aptitudes"
    )

    save_subjects = st.multiselect(
        "좋아하는 과목",
        options=[
            "국어", "문학", "수학", "확률과 통계", "영어",
            "사회·문화", "정치와 법", "생활과 윤리", "경제",
            "한국사", "세계지리", "물리학", "화학",
            "생명과학", "지구과학", "정보", "미술", "체육",
            "보건", "중국어"
        ],
        key="save_subjects"
    )

    job_options = list(get_all_careers().keys())

    save_jobs = st.multiselect(
        "보고서에 포함할 직업을 선택하세요.",
        options=job_options,
        default=st.session_state.favorites if st.session_state.favorites else st.session_state.selected_jobs
    )

    if save_jobs:
        text_report = create_text_report(
            save_mbti,
            save_interests,
            save_aptitudes,
            save_subjects,
            save_jobs
        )

        pdf_report = create_pdf_report(
            save_mbti,
            save_interests,
            save_aptitudes,
            save_subjects,
            save_jobs
        )

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="📝 TXT 파일로 저장",
                data=text_report,
                file_name="mbti_진로탐색_결과.txt",
                mime="text/plain",
                use_container_width=True
            )

        with col2:
            st.download_button(
                label="📄 PDF 파일로 저장",
                data=pdf_report,
                file_name="mbti_진로탐색_결과.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        st.caption("저장한 파일은 진로 활동 기록, 직업 조사 보고서 작성 등에 활용할 수 있습니다.")

    else:
        st.info("보고서에 저장할 직업을 한 가지 이상 선택해 주세요.")


# =========================================================
# 15. 하단 안내
# =========================================================
st.divider()

st.markdown("""
### 💡 진로 탐색을 위한 질문

- 추천 직업 중 내가 가장 흥미를 느끼는 직업은 무엇인가요?
- 그 직업에서는 실제로 어떤 일을 하나요?
- 관련 학과에 진학하려면 어떤 과목을 준비하면 좋을까요?
- 이 직업을 직접 체험하거나 인터뷰할 방법은 있을까요?
- 내가 좋아하는 활동과 이 직업은 어떤 점에서 연결되나요?

> 진로는 한 번에 결정하는 것이 아니라, 다양한 경험과 탐색을 통해 만들어 가는 과정입니다.
""")
