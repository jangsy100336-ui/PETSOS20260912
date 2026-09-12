import streamlit as st
from urllib.parse import quote

# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="PetSOS",
    page_icon="🐾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>
    .main {
        background-color: #F8FAFC;
    }

    .block-container {
        max-width: 760px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .app-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #0F766E;
        text-align: center;
        margin-bottom: 0.2rem;
    }

    .app-subtitle {
        text-align: center;
        color: #64748B;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0F172A;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .info-card {
        padding: 1.2rem;
        border-radius: 16px;
        background-color: white;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }

    .emergency-card {
        padding: 1.3rem;
        border-radius: 16px;
        margin: 1rem 0;
        font-size: 1.05rem;
    }

    .urgent-1 {
        background-color: #ECFDF5;
        border-left: 6px solid #22C55E;
    }

    .urgent-2 {
        background-color: #FFF7ED;
        border-left: 6px solid #F97316;
    }

    .urgent-3 {
        background-color: #FEF2F2;
        border-left: 6px solid #DC2626;
    }

    .warning-box {
        background-color: #FFF7ED;
        border-radius: 14px;
        padding: 1rem;
        border: 1px solid #FED7AA;
        margin: 1rem 0;
    }

    .danger-box {
        background-color: #FEF2F2;
        border-radius: 14px;
        padding: 1rem;
        border: 1px solid #FECACA;
        margin: 1rem 0;
    }

    .success-box {
        background-color: #F0FDFA;
        border-radius: 14px;
        padding: 1rem;
        border: 1px solid #99F6E4;
        margin: 1rem 0;
    }

    .small-text {
        color: #64748B;
        font-size: 0.85rem;
    }

    div.stButton > button {
        border-radius: 12px;
        min-height: 48px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# Session State
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "pet"

if "pet" not in st.session_state:
    st.session_state.pet = {}

if "situation" not in st.session_state:
    st.session_state.situation = None

if "other_situation" not in st.session_state:
    st.session_state.other_situation = ""

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "urgency" not in st.session_state:
    st.session_state.urgency = None


# =========================================================
# 데이터
# =========================================================

SITUATIONS = {
    "🩸": "출혈",
    "😮": "호흡곤란",
    "🧠": "발작 / 경련",
    "☠️": "중독",
    "🤮": "구토 / 설사",
    "🔥": "화상",
    "🌡️": "열사병 / 저체온",
    "🦴": "외상 / 골절",
    "🐝": "물림 / 벌레",
    "👁️": "눈 이상",
}

# 데모용 질문
QUESTIONS = {
    "출혈": [
        ("heavy", "출혈이 매우 많거나 빠르게 증가하고 있나요?"),
        ("conscious", "반려동물이 의식이 있나요?"),
        ("breathing", "정상적으로 호흡하고 있나요?"),
        ("pale", "잇몸이나 혀가 창백하거나 푸른색인가요?"),
        ("trauma", "큰 사고나 외상이 있었나요?"),
    ],

    "호흡곤란": [
        ("breathing", "호흡이 매우 어렵거나 불규칙한가요?"),
        ("conscious", "반려동물이 의식이 있나요?"),
        ("blue", "잇몸이나 혀가 파랗거나 회색으로 보이나요?"),
        ("collapse", "갑자기 쓰러졌거나 서 있기 어려운가요?"),
    ],

    "발작 / 경련": [
        ("seizure_now", "현재 발작이나 경련이 계속되고 있나요?"),
        ("conscious", "발작 후 의식이 돌아왔나요?"),
        ("repeat", "짧은 시간 안에 반복적으로 발작했나요?"),
        ("injury", "발작 중 다치거나 큰 외상이 발생했나요?"),
    ],

    "중독": [
        ("known_toxin", "독성 물질이나 약물을 섭취했을 가능성이 있나요?"),
        ("symptoms", "구토, 떨림, 침 흘림 등 이상 증상이 있나요?"),
        ("conscious", "반려동물이 의식이 있나요?"),
        ("breathing", "정상적으로 호흡하고 있나요?"),
    ],

    "구토 / 설사": [
        ("blood", "토사물이나 대변에 피가 보이나요?"),
        ("repeat", "구토나 설사가 반복되고 있나요?"),
        ("conscious", "반려동물이 의식이 있고 반응하나요?"),
        ("weak", "심하게 축 처지거나 서 있기 어려운가요?"),
    ],

    "화상": [
        ("large", "화상 부위가 넓거나 심하게 손상되었나요?"),
        ("face", "얼굴이나 입 주변에 화상이 있나요?"),
        ("breathing", "호흡에 이상이 있나요?"),
        ("conscious", "반려동물이 의식이 있나요?"),
    ],

    "열사병 / 저체온": [
        ("conscious", "반려동물이 의식이 있나요?"),
        ("breathing", "정상적으로 호흡하고 있나요?"),
        ("collapse", "쓰러지거나 제대로 움직이지 못하나요?"),
        ("severe", "심한 떨림, 혼란, 경련 등의 증상이 있나요?"),
    ],

    "외상 / 골절": [
        ("bleeding", "심한 출혈이 있나요?"),
        ("conscious", "반려동물이 의식이 있나요?"),
        ("breathing", "정상적으로 호흡하고 있나요?"),
        ("severe", "심한 통증이나 움직이지 못하는 상태인가요?"),
    ],

    "물림 / 벌레": [
        ("breathing", "호흡에 이상이 있나요?"),
        ("face", "얼굴이나 목이 빠르게 붓고 있나요?"),
        ("collapse", "쓰러지거나 심하게 약해졌나요?"),
        ("bleeding", "출혈이 심한가요?"),
    ],

    "눈 이상": [
        ("injury", "눈에 심한 외상이나 이물질이 있나요?"),
        ("vision", "갑자기 시야에 문제가 생긴 것처럼 보이나요?"),
        ("pain", "눈을 심하게 감고 있거나 통증이 심해 보이나요?"),
        ("blood", "눈 안이나 주변에 출혈이 있나요?"),
    ]
}


FIRST_AID = {

    "출혈": {
        "do": [
            "깨끗한 거즈나 천으로 출혈 부위를 부드럽게 압박하세요.",
            "가능한 한 반려동물의 움직임을 줄이세요.",
            "출혈이 시작된 시간과 상태 변화를 기억하세요."
        ],
        "dont": [
            "상처에 임의로 약품을 바르지 마세요.",
            "박힌 물체를 억지로 제거하지 마세요.",
            "심한 출혈을 집에서 계속 관찰하며 병원 방문을 늦추지 마세요."
        ],
        "hospital": [
            "출혈이 심하거나 계속되는 경우",
            "의식이 떨어지는 경우",
            "호흡에 이상이 있는 경우",
            "잇몸이나 혀가 창백하거나 푸른 경우",
            "큰 사고나 외상이 있었던 경우"
        ]
    },

    "호흡곤란": {
        "do": [
            "반려동물을 최대한 안정시키고 움직임을 줄이세요.",
            "기도를 막을 수 있는 물건이 없는지 안전한 범위에서 확인하세요.",
            "즉시 동물병원에 연락할 준비를 하세요."
        ],
        "dont": [
            "억지로 물이나 음식을 먹이지 마세요.",
            "불필요하게 움직이거나 흥분시키지 마세요.",
            "호흡곤란이 심한데 집에서 기다리지 마세요."
        ],
        "hospital": [
            "호흡이 매우 어렵거나 불규칙한 경우",
            "혀나 잇몸이 파랗거나 회색인 경우",
            "의식을 잃거나 쓰러지는 경우"
        ]
    },

    "발작 / 경련": {
        "do": [
            "주변의 위험한 물건을 치워 다치지 않도록 하세요.",
            "발작이 시작된 시간을 확인하세요.",
            "발작이 끝난 후 상태를 확인하고 병원에 연락하세요."
        ],
        "dont": [
            "입 안에 손이나 물건을 넣지 마세요.",
            "발작 중 억지로 움직임을 멈추려고 하지 마세요.",
            "의식이 없는 상태에서 물이나 음식을 먹이지 마세요."
        ],
        "hospital": [
            "발작이 계속되는 경우",
            "짧은 시간 안에 반복되는 경우",
            "발작 후 의식이 돌아오지 않는 경우",
            "큰 외상이 발생한 경우"
        ]
    },

    "중독": {
        "do": [
            "무엇을 먹었는지 가능하면 확인하세요.",
            "섭취한 것으로 의심되는 물질과 시간을 기록하세요.",
            "즉시 동물병원 또는 수의사에게 연락하세요."
        ],
        "dont": [
            "수의사의 지시 없이 임의로 구토를 유도하지 마세요.",
            "사람용 약이나 음식물을 임의로 먹이지 마세요.",
            "증상이 없다는 이유로 장시간 기다리지 마세요."
        ],
        "hospital": [
            "독성 물질 섭취가 의심되는 경우",
            "구토, 떨림, 침 흘림 등의 증상이 나타나는 경우",
            "의식이나 호흡에 이상이 있는 경우"
        ]
    },

    "구토 / 설사": {
        "do": [
            "구토나 설사의 횟수와 시작 시간을 기록하세요.",
            "토사물이나 대변의 상태를 확인하세요.",
            "상태가 심하거나 반복되면 동물병원에 연락하세요."
        ],
        "dont": [
            "사람용 약을 임의로 먹이지 마세요.",
            "심한 증상이 있는데 장시간 집에서 관찰하지 마세요."
        ],
        "hospital": [
            "피가 섞여 있는 경우",
            "반복적인 구토나 설사가 지속되는 경우",
            "심하게 축 처지는 경우",
            "의식이나 호흡에 이상이 있는 경우"
        ]
    },

    "화상": {
        "do": [
            "추가적인 열원에서 반려동물을 안전하게 이동시키세요.",
            "가능하면 깨끗한 시원한 물로 해당 부위를 식혀주세요.",
            "화상의 정도가 심하거나 넓다면 즉시 병원에 연락하세요."
        ],
        "dont": [
            "얼음을 직접 대지 마세요.",
            "화상 부위에 임의의 연고나 기름을 바르지 마세요.",
            "물집이나 손상된 피부를 임의로 제거하지 마세요."
        ],
        "hospital": [
            "화상 범위가 넓은 경우",
            "얼굴이나 입 주변이 손상된 경우",
            "호흡에 이상이 있는 경우",
            "피부가 심하게 손상된 경우"
        ]
    },

    "열사병 / 저체온": {
        "do": [
            "위험한 환경에서 반려동물을 안전한 장소로 이동시키세요.",
            "상태를 확인하면서 즉시 동물병원에 연락하세요.",
            "병원으로 이동할 준비를 하세요."
        ],
        "dont": [
            "의식이 없는 동물에게 물을 억지로 먹이지 마세요.",
            "갑작스럽고 극단적인 체온 변화를 유도하지 마세요.",
            "심각한 증상을 집에서 장시간 관찰하지 마세요."
        ],
        "hospital": [
            "의식이 떨어지는 경우",
            "쓰러지는 경우",
            "호흡 이상이 있는 경우",
            "경련이나 심한 떨림이 있는 경우"
        ]
    },

    "외상 / 골절": {
        "do": [
            "반려동물의 움직임을 최소화하세요.",
            "추가적인 부상을 막을 수 있도록 안전하게 이동하세요.",
            "심한 출혈이 있다면 가능한 범위에서 압박하세요."
        ],
        "dont": [
            "골절이 의심되는 부위를 임의로 맞추지 마세요.",
            "심한 통증이 있는 동물을 억지로 움직이지 마세요.",
            "큰 사고 후 겉으로 괜찮아 보여도 장시간 기다리지 마세요."
        ],
        "hospital": [
            "큰 사고나 추락이 있었던 경우",
            "심한 출혈이 있는 경우",
            "의식이나 호흡에 이상이 있는 경우",
            "걷지 못하거나 심한 통증이 있는 경우"
        ]
    },

    "물림 / 벌레": {
        "do": [
            "추가적인 공격이나 접촉을 피할 수 있는 안전한 장소로 이동하세요.",
            "부종이나 증상의 변화를 관찰하세요.",
            "증상이 심하거나 빠르게 진행되면 즉시 병원에 연락하세요."
        ],
        "dont": [
            "상처를 강하게 문지르지 마세요.",
            "사람용 약이나 연고를 임의로 사용하지 마세요."
        ],
        "hospital": [
            "얼굴이나 목이 빠르게 붓는 경우",
            "호흡에 이상이 있는 경우",
            "쓰러지거나 심하게 약해지는 경우",
            "심한 출혈이 있는 경우"
        ]
    },

    "눈 이상": {
        "do": [
            "눈을 비비거나 긁지 못하게 해주세요.",
            "추가적인 외상을 피하도록 안정시키세요.",
            "통증이나 시력 이상이 의심되면 병원에 연락하세요."
        ],
        "dont": [
            "눈에 박힌 물체를 억지로 제거하지 마세요.",
            "사람용 안약을 임의로 사용하지 마세요.",
            "심한 눈 손상을 집에서 장시간 관찰하지 마세요."
        ],
        "hospital": [
            "심한 외상이 있는 경우",
            "시력 이상이 갑자기 발생한 경우",
            "심한 통증이 있는 경우",
            "눈이나 주변에 출혈이 있는 경우"
        ]
    }
}


# =========================================================
# 응급도 계산
# =========================================================

def calculate_urgency(situation, answers):
    """
    데모용 단순 규칙.
    실제 서비스에서는 수의학 전문가 검토 및 검증된 triage 기준이 필요함.
    """

    # 3단계로 바로 분류해야 하는 위험 신호
    critical_keys = {
        "출혈": ["heavy", "breathing", "pale"],
        "호흡곤란": ["breathing", "blue", "conscious", "collapse"],
        "발작 / 경련": ["seizure_now", "conscious", "repeat"],
        "중독": ["conscious", "breathing"],
        "구토 / 설사": ["blood", "weak"],
        "화상": ["breathing", "conscious", "large"],
        "열사병 / 저체온": ["conscious", "breathing", "collapse", "severe"],
        "외상 / 골절": ["bleeding", "conscious", "breathing", "severe"],
        "물림 / 벌레": ["breathing", "face", "collapse", "bleeding"],
        "눈 이상": ["injury", "vision", "blood"],
    }

    # 예/아니오 질문에서 위험 신호에 해당하는 답변
    for key in critical_keys.get(situation, []):
        if key in answers and answers[key] == "예":
            return 3

    # 2단계 위험 신호
    warning_keywords = {
        "출혈": ["trauma"],
        "호흡곤란": [],
        "발작 / 경련": ["injury"],
        "중독": ["known_toxin", "symptoms"],
        "구토 / 설사": ["repeat"],
        "화상": ["face"],
        "열사병 / 저체온": [],
        "외상 / 골절": ["severe"],
        "물림 / 벌레": [],
        "눈 이상": ["pain"],
    }

    for key in warning_keywords.get(situation, []):
        if key in answers and answers[key] == "예":
            return 2

    return 1


# =========================================================
# 공통 UI
# =========================================================

def header():
    st.markdown('<div class="app-title">🐾 PetSOS</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-subtitle">반려동물 응급상황 Quick Guide</div>',
        unsafe_allow_html=True
    )


def progress(current):
    steps = ["반려동물 정보", "상황 선택", "상태 확인", "응급도", "응급처치", "병원"]

    cols = st.columns(len(steps))

    for i, step in enumerate(steps):
        with cols[i]:
            if i == current:
                st.markdown(
                    f"<div style='text-align:center;color:#0F766E;font-weight:700'>"
                    f"●<br>{step}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='text-align:center;color:#CBD5E1'>"
                    f"○<br><span style='font-size:0.7rem'>{step}</span></div>",
                    unsafe_allow_html=True
                )


# =========================================================
# 1. 반려동물 정보
# =========================================================

def pet_page():

    header()
    progress(0)

    st.markdown(
        '<div class="section-title">🐾 반려동물 정보를 알려주세요</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "응급상황에서 필요한 정보를 빠르게 확인하기 위한 기본 정보입니다."
    )

    col1, col2 = st.columns(2)

    with col1:
        species = st.radio(
            "동물 종류",
            ["🐶 강아지", "🐱 고양이", "🐾 기타"],
            horizontal=True
        )

    with col2:
        weight = st.number_input(
            "몸무게 (kg)",
            min_value=0.0,
            max_value=200.0,
            value=5.0,
            step=0.1
        )

    age = st.number_input(
        "나이",
        min_value=0,
        max_value=40,
        value=5
    )

    st.markdown("**기존 질환이나 특이사항이 있나요?**")

    has_disease = st.radio(
        "기저질환",
        ["없음", "있음"],
        horizontal=True,
        label_visibility="collapsed"
    )

    disease = ""

    if has_disease == "있음":
        disease = st.text_input(
            "질환을 입력해주세요",
            placeholder="예: 심장질환, 당뇨"
        )

    medication = st.text_input(
        "현재 복용 중인 약",
        placeholder="없다면 비워두세요"
    )

    allergy = st.text_input(
        "알레르기 / 기타 특이사항",
        placeholder="없다면 비워두세요"
    )

    st.markdown("---")

    if st.button("다음 →", use_container_width=True, type="primary"):

        st.session_state.pet = {
            "species": species,
            "weight": weight,
            "age": age,
            "disease": disease,
            "medication": medication,
            "allergy": allergy
        }

        st.session_state.page = "situation"
        st.rerun()


# =========================================================
# 2. 상황 선택
# =========================================================

def situation_page():

    header()
    progress(1)

    st.markdown(
        '<div class="section-title">무슨 일이 일어났나요?</div>',
        unsafe_allow_html=True
    )

    st.caption("현재 상황과 가장 가까운 항목을 선택해주세요.")

    items = list(SITUATIONS.items())

    for i in range(0, len(items), 2):

        cols = st.columns(2)

        for j in range(2):

            if i + j < len(items):

                icon, name = items[i + j]

                with cols[j]:

                    if st.button(
                        f"{icon}\n\n{name}",
                        key=f"situation_{name}",
                        use_container_width=True
                    ):

                        st.session_state.situation = name

                        if name == "기타":
                            st.session_state.page = "other"
                        else:
                            st.session_state.page = "questions"

                        st.rerun()

    st.markdown("")

    if st.button(
        "❓ 기타 — 목록에 없는 상황",
        use_container_width=True
    ):
        st.session_state.situation = "기타"
        st.session_state.page = "other"
        st.rerun()


# =========================================================
# 3. 기타 상황
# =========================================================

def other_page():

    header()
    progress(1)

    st.markdown(
        '<div class="section-title">❓ 어떤 상황인가요?</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "반려동물에게 일어난 상황을 간단하게 적어주세요."
    )

    description = st.text_area(
        "상황 설명",
        placeholder="예: 갑자기 쓰러졌어요.",
        height=150
    )

    st.markdown(
        """
        <div class="warning-box">
        ⚠️ 상황이 심각하거나 판단하기 어려운 경우에는
        직접 응급처치를 시도하기보다 동물병원에 연락하세요.
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "가까운 동물병원 찾기 →",
        use_container_width=True,
        type="primary"
    ):
        st.session_state.other_situation = description
        st.session_state.urgency = 3
        st.session_state.page = "hospital"
        st.rerun()


# =========================================================
# 4. 상태 확인
# =========================================================

def questions_page():

    header()
    progress(2)

    situation = st.session_state.situation

    st.markdown(
        f'<div class="section-title">{situation}</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "현재 상태를 확인해주세요. 정확히 모르겠다면 '모르겠어요'를 선택하세요."
    )

    questions = QUESTIONS.get(situation, [])

    for key, question in questions:

        answer = st.radio(
            question,
            ["예", "아니오", "모르겠어요"],
            horizontal=True,
            key=f"answer_{key}"
        )

        st.session_state.answers[key] = answer

        st.markdown("")

    if st.button(
        "응급도 확인하기 →",
        use_container_width=True,
        type="primary"
    ):

        urgency = calculate_urgency(
            situation,
            st.session_state.answers
        )

        st.session_state.urgency = urgency
        st.session_state.page = "result"

        st.rerun()


# =========================================================
# 5. 응급도 결과
# =========================================================

def result_page():

    header()
    progress(3)

    urgency = st.session_state.urgency
    situation = st.session_state.situation

    if urgency == 1:

        icon = "🟢"
        title = "1단계 · 관찰"
        message = (
            "현재 확인된 위험 신호가 적습니다. "
            "상태를 계속 관찰하고 이상이 지속되면 동물병원에 연락하세요."
        )
        css = "urgent-1"

    elif urgency == 2:

        icon = "🟠"
        title = "2단계 · 빠른 진료"
        message = (
            "가능한 한 빨리 동물병원에 연락하거나 방문하세요."
        )
        css = "urgent-2"

    else:

        icon = "🔴"
        title = "3단계 · 응급"
        message = (
            "즉시 동물병원에 연락하고 응급진료를 받으세요."
        )
        css = "urgent-3"

    st.markdown(
        f"""
        <div class="emergency-card {css}">
            <div style="font-size:2.5rem">{icon}</div>
            <h2>{title}</h2>
            <p>{message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 현재 상황")

    st.info(
        f"{situation}에 대한 위험 신호를 확인했습니다."
    )

    if urgency == 3:

        st.markdown(
            """
            <div class="danger-box">
            🚨 <b>응급상황일 가능성이 있습니다.</b><br>
            응급처치 안내를 확인하면서 가능한 한 빨리 동물병원에 연락하세요.
            </div>
            """,
            unsafe_allow_html=True
        )

    if st.button(
        "🚑 응급처치 확인하기",
        use_container_width=True,
        type="primary"
    ):
        st.session_state.page = "first_aid"
        st.rerun()

    if urgency >= 2:

        if st.button(
            "🏥 바로 병원 찾기",
            use_container_width=True
        ):
            st.session_state.page = "hospital"
            st.rerun()


# =========================================================
# 6. 응급처치
# =========================================================

def first_aid_page():

    header()
    progress(4)

    situation = st.session_state.situation
    data = FIRST_AID.get(situation)

    st.markdown(
        f'<div class="section-title">{situation} 응급처치</div>',
        unsafe_allow_html=True
    )

    if not data:
        st.warning(
            "현재 상황에 대한 상세 안내가 준비되지 않았습니다. "
            "동물병원에 연락하세요."
        )

    else:

        st.markdown("### 🟢 지금 하세요")

        for item in data["do"]:
            st.markdown(f"✅ **{item}**")

        st.markdown("---")

        st.markdown("### 🔴 하지 마세요")

        for item in data["dont"]:
            st.markdown(f"❌ **{item}**")

        st.markdown("---")

        st.markdown("### 🚨 바로 병원으로 가세요")

        for item in data["hospital"]:
            st.markdown(f"🚨 {item}")

    st.markdown("")

    if st.button(
        "🏥 가까운 동물병원 찾기",
        use_container_width=True,
        type="primary"
    ):
        st.session_state.page = "hospital"
        st.rerun()


# =========================================================
# 7. 병원 찾기
# =========================================================

def hospital_page():

    header()
    progress(5)

    st.markdown(
        '<div class="section-title">🏥 가까운 동물병원</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "현재 위치 또는 지역을 기준으로 동물병원을 검색할 수 있습니다."
    )

    region = st.text_input(
        "지역 입력",
        placeholder="예: 서울 강남구"
    )

    if region:

        # 실제 병원 API를 붙이기 전 사용할 검색 링크
        search_url = (
            "https://www.google.com/maps/search/"
            + quote(f"{region} 동물병원")
        )

        st.markdown(
            f"""
            <div class="info-card">
                <h3>📍 {region} 주변 동물병원</h3>
                <p class="small-text">
                    지도에서 주변 동물병원을 확인하세요.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.link_button(
            "🗺️ 주변 동물병원 지도에서 찾기",
            search_url,
            use_container_width=True
        )

    st.markdown("---")

    if st.button(
        "📋 병원에 전달할 정보 확인",
        use_container_width=True,
        type="primary"
    ):
        st.session_state.page = "contact"
        st.rerun()


# =========================================================
# 8. 병원 전달 정보
# =========================================================

def contact_page():

    header()

    st.markdown(
        '<div class="section-title">📋 병원에 전달할 정보</div>',
        unsafe_allow_html=True
    )

    pet = st.session_state.pet
    situation = st.session_state.situation

    if situation == "기타":
        situation_text = st.session_state.other_situation
    else:
        situation_text = situation

    st.markdown("### 🐾 반려동물")

    st.markdown(
        f"""
        <div class="info-card">
        <b>동물</b> : {pet.get("species", "-")}<br>
        <b>나이</b> : {pet.get("age", "-")}세<br>
        <b>체중</b> : {pet.get("weight", "-")} kg<br>
        <b>기저질환</b> : {pet.get("disease") or "없음"}<br>
        <b>복용약</b> : {pet.get("medication") or "없음"}<br>
        <b>특이사항</b> : {pet.get("allergy") or "없음"}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🚨 현재 상황")

    st.markdown(
        f"""
        <div class="info-card">
        <b>상황</b><br>
        {situation_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    if situation != "기타":

        st.markdown("### 🔎 확인된 상태")

        for key, answer in st.session_state.answers.items():

            if answer == "예":

                question = next(
                    (
                        q for k, q in QUESTIONS[situation]
                        if k == key
                    ),
                    key
                )

                st.markdown(f"☑ {question}")

    # 전화 전 전달용 텍스트
    summary = f"""
[PetSOS 응급상황 정보]

반려동물
- 동물: {pet.get("species", "-")}
- 나이: {pet.get("age", "-")}세
- 체중: {pet.get("weight", "-")} kg
- 기저질환: {pet.get("disease") or "없음"}
- 복용약: {pet.get("medication") or "없음"}
- 특이사항: {pet.get("allergy") or "없음"}

현재 상황
- {situation_text}

응급도
- {st.session_state.urgency}단계
"""

    st.markdown("---")

    st.markdown("### 📞 병원에 전달하기")

    st.code(summary, language=None)

    st.caption(
        "위 내용을 복사하여 병원에 전달하거나 전화할 때 참고할 수 있습니다."
    )

    st.button(
        "📋 정보 복사하기",
        use_container_width=True
    )

    st.info(
        "초기 버전에서는 실제 동물병원 시스템으로 정보를 직접 전송하지 않습니다."
    )


# =========================================================
# 페이지 라우팅
# =========================================================

if st.session_state.page == "pet":
    pet_page()

elif st.session_state.page == "situation":
    situation_page()

elif st.session_state.page == "other":
    other_page()

elif st.session_state.page == "questions":
    questions_page()

elif st.session_state.page == "result":
    result_page()

elif st.session_state.page == "first_aid":
    first_aid_page()

elif st.session_state.page == "hospital":
    hospital_page()

elif st.session_state.page == "contact":
    contact_page()
