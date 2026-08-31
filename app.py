<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MBTI 진로 탐색 프로그램</title>

  <style>
    :root {
      --primary: #4f46e5;
      --primary-dark: #3730a3;
      --sub: #eef2ff;
      --text: #1f2937;
      --gray: #6b7280;
      --border: #e5e7eb;
      --white: #ffffff;
      --bg: #f8fafc;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      font-family: "Pretendard", "Noto Sans KR", Arial, sans-serif;
      color: var(--text);
      background: var(--bg);
      line-height: 1.6;
    }

    header {
      color: white;
      text-align: center;
      padding: 70px 20px;
      background:
        linear-gradient(135deg, rgba(79, 70, 229, 0.92), rgba(37, 99, 235, 0.78)),
        url("https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1600&q=80")
        center/cover;
    }

    header h1 {
      margin: 0 0 12px;
      font-size: clamp(2rem, 5vw, 3.4rem);
    }

    header p {
      margin: 0 auto;
      max-width: 700px;
      font-size: 1.05rem;
      opacity: 0.95;
    }

    main {
      width: min(1100px, calc(100% - 40px));
      margin: 40px auto 70px;
    }

    .intro-box {
      padding: 24px;
      margin-bottom: 32px;
      background: var(--white);
      border-left: 6px solid var(--primary);
      border-radius: 14px;
      box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
    }

    .intro-box h2 {
      margin-top: 0;
      font-size: 1.35rem;
    }

    .intro-box p {
      margin-bottom: 0;
      color: #4b5563;
    }

    .selection-section {
      padding: 32px;
      background: white;
      border: 1px solid var(--border);
      border-radius: 20px;
      box-shadow: 0 8px 25px rgba(15, 23, 42, 0.06);
    }

    .selection-section h2 {
      margin: 0;
      text-align: center;
      font-size: 1.6rem;
    }

    .selection-section > p {
      margin: 8px 0 28px;
      text-align: center;
      color: var(--gray);
    }

    .mbti-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
    }

    .mbti-btn {
      padding: 15px 8px;
      color: var(--primary-dark);
      font-size: 1rem;
      font-weight: 800;
      cursor: pointer;
      background: var(--sub);
      border: 2px solid transparent;
      border-radius: 12px;
      transition: 0.2s;
    }

    .mbti-btn:hover,
    .mbti-btn.active {
      color: white;
      background: var(--primary);
      border-color: var(--primary-dark);
      transform: translateY(-2px);
      box-shadow: 0 7px 15px rgba(79, 70, 229, 0.25);
    }

    #result {
      display: none;
      margin-top: 40px;
    }

    .result-title {
      margin-bottom: 20px;
      text-align: center;
    }

    .result-title h2 {
      margin: 0;
      font-size: 1.7rem;
    }

    .result-title p {
      margin: 8px 0 0;
      color: var(--gray);
    }

    .career-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 22px;
    }

    .career-card {
      overflow: hidden;
      background: white;
      border: 1px solid var(--border);
      border-radius: 18px;
      box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
      transition: transform 0.2s, box-shadow 0.2s;
    }

    .career-card:hover {
      transform: translateY(-7px);
      box-shadow: 0 15px 30px rgba(15, 23, 42, 0.15);
    }

    .career-card img {
      width: 100%;
      height: 190px;
      object-fit: cover;
      display: block;
    }

    .career-content {
      padding: 20px;
    }

    .career-content h3 {
      margin: 0 0 10px;
      font-size: 1.25rem;
    }

    .career-content p {
      margin: 0;
      color: #4b5563;
      font-size: 0.95rem;
    }

    .question-box {
      padding: 24px;
      margin-top: 35px;
      background: #fffbeb;
      border: 1px solid #fde68a;
      border-radius: 16px;
    }

    .question-box h3 {
      margin-top: 0;
      color: #92400e;
    }

    .question-box ul {
      margin-bottom: 0;
      padding-left: 20px;
      color: #78350f;
    }

    footer {
      padding: 25px 20px;
      color: #6b7280;
      text-align: center;
      font-size: 0.9rem;
      background: white;
      border-top: 1px solid var(--border);
    }

    @media (max-width: 800px) {
      .mbti-grid {
        grid-template-columns: repeat(2, 1fr);
      }

      .career-grid {
        grid-template-columns: 1fr;
      }

      .career-card img {
        height: 220px;
      }
    }

    @media (max-width: 450px) {
      main {
        width: min(100% - 24px, 1100px);
      }

      .selection-section {
        padding: 22px 16px;
      }

      .mbti-grid {
        gap: 8px;
      }
    }
  </style>
</head>

<body>
  <header>
    <h1>MBTI 진로 탐색</h1>
    <p>
      나의 성향을 바탕으로 흥미를 느낄 수 있는 직업 분야를 탐색해 보세요.
      선택 결과는 진로 탐색을 위한 참고 자료입니다.
    </p>
  </header>

  <main>
    <section class="intro-box">
      <h2>🔎 진로는 스스로 탐색하는 과정입니다</h2>
      <p>
        MBTI 결과만으로 직업을 결정할 수는 없습니다. 좋아하는 과목, 잘하는 활동,
        가치관, 생활 방식 등을 함께 생각하며 다양한 직업을 조사해 보세요.
      </p>
    </section>

    <section class="selection-section">
      <h2>나의 MBTI를 선택하세요</h2>
      <p>선택하면 어울릴 수 있는 직업 3가지를 확인할 수 있습니다.</p>

      <div class="mbti-grid" id="mbtiGrid">
        <button class="mbti-btn" data-mbti="ISTJ">ISTJ</button>
        <button class="mbti-btn" data-mbti="ISFJ">ISFJ</button>
        <button class="mbti-btn" data-mbti="INFJ">INFJ</button>
        <button class="mbti-btn" data-mbti="INTJ">INTJ</button>

        <button class="mbti-btn" data-mbti="ISTP">ISTP</button>
        <button class="mbti-btn" data-mbti="ISFP">ISFP</button>
        <button class="mbti-btn" data-mbti="INFP">INFP</button>
        <button class="mbti-btn" data-mbti="INTP">INTP</button>

        <button class="mbti-btn" data-mbti="ESTP">ESTP</button>
        <button class="mbti-btn" data-mbti="ESFP">ESFP</button>
        <button class="mbti-btn" data-mbti="ENFP">ENFP</button>
        <button class="mbti-btn" data-mbti="ENTP">ENTP</button>

        <button class="mbti-btn" data-mbti="ESTJ">ESTJ</button>
        <button class="mbti-btn" data-mbti="ESFJ">ESFJ</button>
        <button class="mbti-btn" data-mbti="ENFJ">ENFJ</button>
        <button class="mbti-btn" data-mbti="ENTJ">ENTJ</button>
      </div>
    </section>

    <section id="result">
      <div class="result-title">
        <h2 id="resultHeading">추천 직업</h2>
        <p id="resultDescription"></p>
      </div>

      <div class="career-grid" id="careerGrid"></div>

      <div class="question-box">
        <h3>💡 더 깊이 탐색해 볼 질문</h3>
        <ul>
          <li>추천 직업에서 실제로 하는 일은 무엇일까?</li>
          <li>이 직업과 관련된 고등학교 과목, 학과, 자격은 무엇일까?</li>
          <li>내가 좋아하거나 잘했던 경험과 연결되는 부분은 무엇일까?</li>
        </ul>
      </div>
    </section>
  </main>

  <footer>
    MBTI 진로 탐색 프로그램 · 진로 선택 전에는 다양한 직업 정보와 자신의 경험을 함께 살펴보세요.
  </footer>

  <script>
    const mbtiData = {
      ISTJ: {
        description: "체계적이고 책임감 있게 일을 처리하는 성향을 바탕으로 탐색해 볼 수 있습니다.",
        careers: [
          ["회계사", "숫자와 자료를 정확하게 분석하고 재무 정보를 관리하는 직업입니다.", "https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=800&q=80"],
          ["공무원", "공공 서비스를 안정적으로 운영하고 시민의 생활을 돕는 일을 합니다.", "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?auto=format&fit=crop&w=800&q=80"],
          ["품질관리 전문가", "제품이나 서비스가 기준에 맞는지 점검하고 개선합니다.", "https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&w=800&q=80"]
        ]
      },
      ISFJ: {
        description: "세심하게 타인을 돕고 안정적인 환경을 만드는 분야를 탐색해 볼 수 있습니다.",
        careers: [
          ["간호사", "환자의 건강 상태를 살피고 치료와 회복을 돕습니다.", "https://images.unsplash.com/photo-1584982751601-97dcc096659c?auto=format&fit=crop&w=800&q=80"],
          ["사회복지사", "도움이 필요한 사람들에게 복지 서비스와 정보를 연결합니다.", "https://images.unsplash.com/photo-1559027615-cd4628902d4a?auto=format&fit=crop&w=800&q=80"],
          ["초등교사", "학생들의 기초 학습과 학교생활 성장을 지원합니다.", "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=800&q=80"]
        ]
      },
      INFJ: {
        description: "사람과 사회에 대한 깊은 관심을 바탕으로 의미 있는 변화를 만드는 분야를 탐색해 볼 수 있습니다.",
        careers: [
          ["심리학 연구원", "사람의 생각과 행동을 과학적으로 연구합니다.", "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?auto=format&fit=crop&w=800&q=80"],
          ["작가", "글을 통해 생각, 경험, 이야기를 독자에게 전달합니다.", "https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=800&q=80"],
          ["국제기구 활동가", "국제 사회의 인권, 환경, 교육 등의 문제 해결에 참여합니다.", "https://images.unsplash.com/photo-1521295121783-8a321d551ad2?auto=format&fit=crop&w=800&q=80"]
        ]
      },
      INTJ: {
        description: "논리적으로 계획을 세우고 복잡한 문제를 해결하는 분야를 탐색해 볼 수 있습니다.",
        careers: [
          ["소프트웨어 개발자", "컴퓨터 프로그램과 웹·앱 서비스를 설계하고 개발합니다.", "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=800&q=80"],
          ["데이터 분석가", "데이터를 분석해 의미 있는 정보와 해결 방향을 찾습니다.", "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80"],
          ["연구원", "특정 분야의 문제를 탐구하고 새로운 지식이나 기술을 개발합니다.", "https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&w=800&q=80"]
        ]
      },
      ISTP: {
        description: "직접 관찰하고 도구나 기술을 활용해 문제를 해결하는 분야를 탐색해 볼 수 있습니다.",
        careers: [
          ["기계공학자", "기계와 장치를 설계하고 성능을 개선합니다.", "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=800&q=80"],
          ["항공정비사", "항공기의 안전한 운항을 위해 점검과 정비를 합니다.", "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=800&q=80"],
          ["소방관", "화재와 재난 현장에서 사람들의 안전을 지킵니다.", "https://images.unsplash.com/photo-1518005020951-eccb494ad742?auto=format&fit=crop&w=800&q=80"]
        ]
      },
      ISFP: {
        description: "감각과 개성을 살리며 사람들에게 즐거움과 도움을 주는 분야를 탐색해 볼 수 있습니다.",
        careers: [
          ["그래픽 디자이너", "색상, 이미지, 글자를 활용해 시각적인 메시지를 전달합니다.", "https://images.unsplash.com/photo-1561070791-2526d30994b5?auto=format&fit=crop&w=800&q=80"],
          ["사진작가", "사진을 통해 사람, 장소, 순간의 이야기를 기록합니다.", "https://images.unsplash.com/photo-1452780212940-6f5c0d14d848?auto=format&fit=crop&w=800&q=80"],
          ["반려동물 행동전문가", "반려동물의 행동을 이해하고 건강한 생활을 돕습니다.", "https://images.unsplash.com/photo-1450778869180-41d0601e046e?auto=format&fit=crop&w=800&q=80"]
        ]
      },
      INFP: {
        description: "자신의 가치와 창의성을 바탕으로 사람들의 마음을 이해하는 분야를 탐색해 볼 수 있습니다.",
        careers: [
          ["웹툰 작가", "그림과 이야기를 결합해 독자에게 메시지를 전달합니다.", "https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=800&q=80"],
          ["출판 편집자", "글과 책의 내용을 다듬고 독자에게 전달될 과정을 관리합니다.", "https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=800&q=80"],
          ["환경운동가", "환경 문제를 알리고 지속 가능한 변화를 위해 활동합니다.", "https://images.unsplash.com/photo-1473448912268-2022ce9509d8?auto=format&fit=crop&w=800&q=80"]
        ]
      },
      INTP: {
        description: "호기심을 가지고 원리와 구조를 분석하는 분야를 탐색해 볼 수 있습니다.",
        careers: [
          ["과학자", "자연과 사회의 현상을 관찰하고 실험으로 탐구합니다.", "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?auto=format&fit=crop&w=800&q=80"],
          ["게임 개발자", "프로그래밍과 기획을 통해 게임을 제작합니다.", "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=800&q=80"],
          ["정보보안 전문가", "컴퓨터 시스템과 데이터를 사이버 위협으로부터 보호합니다.", "https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=800&q=80"]
        ]
      },
      ESTP: {
        description: "빠르게 상황을 파악하고 활발하게 행동하는 강점을 활용할 수 있는 분야를 탐색해 볼 수 있습니다.",
        careers: [
          ["경찰관", "지역 사회의 안전을 지키고 사건·사고에 대응합니다.", "https://images.unsplash.com/photo-1605089048842-add353d7c7c9?auto=format&fit=crop&w=800&q=80"],
          ["스포츠 선수", "꾸준한 훈련과 경기력을 바탕으로 스포츠 활동을 합니다.", "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=800&q=80"],
          ["영업 전문가", "고객의 필요를 파악하고 제품이나 서비스를 소개합니다.", "https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=800&q=80"]
        ]
      },
      ESFP: {
        description: "사람들과 즐겁게 소통하고 생동감 있는 경험을 만드는 분야를 탐색해 볼 수 있습니다.",
        careers: [
          ["행사 기획자", "공연, 축제, 전시 등 다양한 행사를 기획하고 운영합니다.", "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=800&q=80"],
          ["승무원", "승객의 안전과 편안한 이동을 돕는 서비스를 제공합니다.", "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=800&q=80"],
          ["방송인", "방송과 미디어를 통해 정보와 즐거움을 전달합니다.", "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=800&q=80"]
        ]
      },
      ENFP: {
        description: "새로운 아이디어를 떠올리고 다양한 사람과 연결되는 분야를 탐색해 볼 수 있습니다.",
        careers: [
          ["광고기획자", "상품이나 서비스의 메시지를 효과적으로 전달하는 광고를 기획합니다.", "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=800&q=80"],
          ["콘텐츠 크리에이터", "영상, 글, 이미지 등으로 흥미로운 콘텐츠를 제작합니다.", "https://images.unsplash.com/photo-1611162617474-5b21e879e113?auto=format&fit=crop&w=800&q=80"],
          ["여행 기획자", "여행객에게 맞는 여행 상품과 경험을 설계합니다.", "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=800&q=80"]
        ]
      },
      ENTP: {
        description: "새로운 가능성을 발견하고 토론과 아이디어 발전을 즐기는 분야를 탐색해 볼 수 있습니다.",
        careers: [
          ["창업가", "새로운 문제 해결 방법을 사업 아이디어로 발전시킵니다.", "https://images.unsplash.com/photo-1556761175-4b46a572b786?auto=format&fit=crop&w=800&q=80"],
          ["변호사", "법률을 분석하고 의뢰인의 권리와 문제 해결을 돕습니다.", "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=800&q=80"],
          ["마케팅 전문가", "시장과 소비자를 분석해 제품의 가치를 알리는 전략을 세웁니다.", "https://images.unsplash.com/photo-1533750349088-cd871a92f312?auto=format&fit=crop&w=800&q=80"]
        ]
      },
      ESTJ: {
        description: "목표를 정하고 체계적으로 조직을 운영하는 분야를 탐색해 볼 수 있습니다.",
        careers: [
          ["경영 관리자", "조직의 목표를 세우고 인력과 업무를 효율적으로 관리합니다.", "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=800&q=80"],
          ["프로젝트 매니저", "프로젝트의 일정, 역할, 예산을 조정해 목표 달성을 이끕니다.", "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=800&q=80"],
          ["행정사", "행정 절차와 관련 서류 업무를 전문적으로 돕습니다.", "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?auto=format&fit=crop&w=800&q=80"]
        ]
      },
      ESFJ: {
        description: "사람들의 필요를 살피고 협력적인 환경을 만드는 분야를 탐색해 볼 수 있습니다.",
        careers: [
          ["인사 담당자", "조직 구성원의 채용, 교육, 복지와 관련된 업무를 합니다.", "https://images.unsplash.com/photo-1521737711867-e3b97375f902?auto=format&fit=crop&w=800&q=80"],
          ["호텔리어", "고객이 편안하고 만족스러운 서비스를 경험하도록 돕습니다.", "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80"],
          ["보육교사", "유아의 생활과 놀이, 발달 과정을 지원합니다.", "https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?auto=format&fit=crop&w=800&q=80"]
        ]
      },
      ENFJ: {
        description: "다른 사람의 성장을 돕고 공동의 목표를 이끄는 분야를 탐색해 볼 수 있습니다.",
        careers: [
          ["교사", "학생의 학습과 성장을 돕고 교육 활동을 설계합니다.", "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=800&q=80"],
          ["진로교육 전문가", "학생이 자신의 흥미와 역량을 발견하도록 교육 프로그램을 운영합니다.", "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?auto=format&fit=crop&w=800&q=80"],
          ["홍보 전문가", "조직의 가치와 활동을 대중에게 효과적으로 알립니다.", "https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=800&q=80"]
        ]
      },
      ENTJ: {
        description: "큰 목표를 세우고 전략적으로 실행하는 리더십 분야를 탐색해 볼 수 있습니다.",
        careers: [
          ["경영 컨설턴트", "조직의 문제를 분석하고 성장 전략을 제안합니다.", "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=800&q=80"],
          ["기업가", "아이디어를 바탕으로 조직과 사업을 만들고 운영합니다.", "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=80"],
          ["제품 관리자", "제품의 방향과 기능을 기획하고 개발 과정을 조율합니다.", "https://images.unsplash.com/photo-1553877522-43269d4ea984?auto=format&fit=crop&w=800&q=80"]
        ]
      }
    };

    const buttons = document.querySelectorAll(".mbti-btn");
    const result = document.getElementById("result");
    const resultHeading = document.getElementById("resultHeading");
    const resultDescription = document.getElementById("resultDescription");
    const careerGrid = document.getElementById("careerGrid");

    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        const selectedMbti = button.dataset.mbti;
        const selectedData = mbtiData[selectedMbti];

        buttons.forEach((btn) => btn.classList.remove("active"));
        button.classList.add("active");

        resultHeading.textContent = `${selectedMbti} 유형을 위한 진로 탐색`;
        resultDescription.textContent = selectedData.description;

        careerGrid.innerHTML = selectedData.careers.map((career) => {
          const [title, description, image] = career;

          return `
            <article class="career-card">
              <img src="${image}" alt="${title} 관련 이미지">
              <div class="career-content">
                <h3>${title}</h3>
                <p>${description}</p>
              </div>
            </article>
          `;
        }).join("");

        result.style.display = "block";
        result.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    });
  </script>
</body>
</html>
