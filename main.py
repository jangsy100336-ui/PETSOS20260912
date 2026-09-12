import streamlit as st

# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="PetSOS - 반려동물 응급처치",
    page_icon="🐾",
    layout="centered"
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
        max-width: 700px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #17324D;
    }

    .app-title {
        text-align: center;
        font-size: 2.3rem;
        font-weight: 800;
        color: #167D8D;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        text-align: center;
        color: #64748B;
        margin-bottom: 2rem;
    }

    .emergency-card {
        padding: 1.2rem;
        border-radius: 18px;
        margin: 0.5rem 0;
        background-color: white;
        border: 1px solid #E2E8F0;
    }

    .urgent-box {
        padding: 1.2rem;
        border-radius: 16px;
        margin: 1rem 0;
    }

    .level-1 {
        background-color: #ECFDF5;
        border-left: 6px solid #22C55E;
    }

    .level-2 {
        background-color: #FFF7ED;
        border-left: 6px solid #F97316;
    }

    .level-3 {
        background-color: #FEF2F2;
        border-left: 6px solid #DC2626;
    }

    .action-box {
        background-color: white;
        border-radius: 16px;
        padding: 1.2rem;
        margin: 1rem 0;
        border: 1px solid #E2E8F0;
    }

    .small-text {
        color: #64748B;
        font-size: 0.9rem;
    }

    div.stButton > button {
        width: 100%;
        min-height: 48px;
        border-radius: 12px;
        font-size: 1rem;
        font-weight: 600;
    }

    .progress {
        text-align: center;
        color: #64748B;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# Session State 초기화
# =========================================================

defaults = {
    "page": "pet_info",

    "animal_type": "",
    "weight": "",
    "age": "",
    "disease": "",
    "medication": "",
    "special_note": "",

    "emergency_type": "",
    "other_situation": "",

    "answers": {},

    "urgency_level": None,

    "hospital_selected": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# 페이지 이동 함수
# =========================================================

def go_to(page):
    st.session_state.page = page
    st.rerun()


def back_to(page):
    st.session_state.page = page
    st.rerun()


# =========================================================
# 공통 헤더
# =========================================================

def page_header(title, subtitle=None, back_page=None):

    if back_page:
        if st.button("← 이전", key=f"back_{title}"):
            back_to(back_page)

    st.markdown(f"## {title}")

    if subtitle:
        st.markdown(
            f'<p class="small-text">{subtitle}</p>',
            unsafe_allow_html=True
        )


# =========================================================
# 1. 반려동물 정보
# =========================================================

def pet_info_page():

    st.markdown(
        '<div class="app-title">🐾 PetSOS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">반려동물 응급상황 Quick Guide</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 먼저 반려동물의 정보를 알려주세요.")
    st.caption("응급상황에 맞는 안내를 위해 최소한의 정보만 입력해주세요.")

    animal = st.radio(
        "🐾 반려동물 종류",
        ["🐶 강아지", "🐱 고양이", "🐾 기타"],
        horizontal=True,
        index=None
    )

    weight = st.text_input(
        "⚖️ 몸무게 (kg)",
        value=st.session_state.weight,
        placeholder="예: 8.5"
    )

    age = st.text_input(
        "🎂 나이",
        value=st.session_state.age,
        placeholder="예: 5살"
    )

    with st.expander("추가 정보 입력 (선택사항)"):

        disease = st.text_input(
            "기존 질환",
            value=st.session_state.disease,
            placeholder="예: 심장질환"
        )

        medication = st.text_input(
            "복용 중인 약",
            value=st.session_state.medication,
            placeholder="복용 중인 약이 있다면 입력해주세요."
        )

        special_note = st.text_area(
            "기타 특이사항",
            value=st.session_state.special_note,
            placeholder="알레르기 등 특이사항"
        )

    if st.button("다음 →", type="primary"):

        if not animal:
            st.warning("반려동물의 종류를 선택해주세요.")
            return

        st.session_state.animal_type = animal
        st.session_state.weight = weight
        st.session_state.age = age
        st.session_state.disease = disease
        st.session_state.medication = medication
        st.session_state.special_note = special_note

        go_to("emergency")


# =========================================================
# 2. 응급상황 선택
# =========================================================

def emergency_page():

    page_header(
        "무슨 일이 일어났나요?",
        "현재 반려동물에게 발생한 상황을 선택해주세요.",
        "pet_info"
    )

    emergencies = [
        ("🩸", "출혈", "bleeding"),
        ("😮", "호흡곤란", "breathing"),
        ("🧠", "발작 / 경련", "seizure"),
        ("☠️", "중독", "poisoning"),
        ("🤮", "구토 / 설사", "vomiting"),
        ("🔥", "화상", "burn"),
        ("🦴", "외상 / 골절", "injury"),
        ("🌡️", "열사병", "heatstroke"),
        ("🐝", "물림 / 쏘임", "bite"),
        ("❓", "기타", "other")
    ]

    cols = st.columns(2)

    for i, (icon, name, code) in enumerate(emergencies):

        with cols[i % 2]:

            if st.button(
                f"{icon}\n{name}",
                key=f"emergency_{code}",
                use_container_width=True
            ):

                st.session_state.emergency_type = code

                if code == "other":
                    go_to("other")

                else:
                    st.session_state.answers = {}
                    go_to("questions")


# =========================================================
# 3. 기타 상황 입력
# =========================================================

def other_page():

    page_header(
        "❓ 기타 상황",
        "현재 반려동물에게 어떤 일이 일어났는지 간단하게 적어주세요.",
        "emergency"
    )

    situation = st.text_area(
        "현재 상황",
        value=st.session_state.other_situation,
        placeholder="예: 갑자기 쓰러졌어요.",
        height=150
    )

    if st.button("계속하기 →", type="primary"):

        if not situation.strip():
            st.warning("현재 상황을 입력해주세요.")
            return

        st.session_state.other_situation = situation

        # 기타 상황은 안전을 위해 바로 병원 상담 권고
        st.session_state.urgency_level = 2

        go_to("result")


# =========================================================
# 응급상황별 질문 데이터
# =========================================================

questions = {

    "bleeding": [
        ("heavy", "출혈이 심하거나 계속해서 많이 나오고 있나요?"),
        ("conscious", "반려동물이 의식이 있나요?"),
        ("breathing", "정상적으로 호흡하고 있나요?"),
        ("pale_gums", "잇몸이나 혀가 창백하거나 푸른가요?")
    ],

    "breathing": [
        ("breathing", "정상적으로 호흡하고 있나요?"),
        ("conscious", "반려동물이 의식이 있나요?"),
        ("blue_gums", "잇몸이나 혀가 파랗거나 보라색인가요?"),
        ("collapse", "쓰러지거나 제대로 서지 못하나요?")
    ],

    "seizure": [
        ("seizure_now", "현재 발작이나 경련이 계속되고 있나요?"),
        ("conscious", "발작 후 의식이 돌아왔나요?"),
        ("repeat", "짧은 시간 안에 발작이 반복되었나요?"),
        ("breathing", "정상적으로 호흡하고 있나요?")
    ],

    "poisoning": [
        ("known_poison", "독성 물질이나 약물을 먹었을 가능성이 있나요?"),
        ("conscious", "반려동물이 의식이 있나요?"),
        ("breathing", "정상적으로 호흡하고 있나요?"),
        ("symptoms", "구토, 떨림, 경련 등의 증상이 있나요?")
    ],

    "vomiting": [
        ("repeated", "구토나 설사가 반복되고 있나요?"),
        ("blood", "피가 섞여 있나요?"),
        ("conscious", "반려동물이 의식이 있나요?"),
        ("weak", "심하게 처지거나 힘이 없어 보이나요?")
    ],

    "burn": [
        ("large_burn", "화상 부위가 넓거나 심해 보이나요?"),
        ("face", "얼굴이나 입 주변에 화상을 입었나요?"),
        ("breathing", "정상적으로 호흡하고 있나요?"),
        ("conscious", "반려동물이 의식이 있나요?")
    ],

    "injury": [
        ("heavy_bleeding", "심한 출혈이 있나요?"),
        ("cannot_stand", "일어서거나 걷지 못하나요?"),
        ("conscious", "반려동물이 의식이 있나요?"),
        ("breathing", "정상적으로 호흡하고 있나요?")
    ],

    "heatstroke": [
        ("collapse", "쓰러졌거나 의식이 떨어졌나요?"),
        ("breathing", "정상적으로 호흡하고 있나요?"),
        ("heavy_panting", "심하게 헐떡이고 있나요?"),
        ("vomiting", "구토나 설사가 있나요?")
    ],

    "bite": [
        ("heavy_bleeding", "심한 출혈이 있나요?"),
        ("face", "얼굴이나 목 주변을 물렸나요?"),
        ("breathing", "정상적으로 호흡하고 있나요?"),
        ("swelling", "얼굴이나 목이 빠르게 붓고 있나요?")
    ]
}


# =========================================================
# 4. 현재 상태 확인
# =========================================================

def questions_page():

    emergency_name = {
        "bleeding": "🩸 출혈",
        "breathing": "😮 호흡곤란",
        "seizure": "🧠 발작 / 경련",
        "poisoning": "☠️ 중독",
        "vomiting": "🤮 구토 / 설사",
        "burn": "🔥 화상",
        "injury": "🦴 외상 / 골절",
        "heatstroke": "🌡️ 열사병",
        "bite": "🐝 물림 / 쏘임"
    }

    emergency = st.session_state.emergency_type

    page_header(
        f"{emergency_name.get(emergency, '응급상황')}",
        "현재 반려동물의 상태를 확인해주세요.",
        "emergency"
    )

    qs = questions.get(emergency, [])

    for key, question in qs:

        answer = st.radio(
            question,
            ["예", "아니오", "모르겠어요"],
            horizontal=True,
            index=None,
            key=f"question_{key}"
        )

        if answer:
            st.session_state.answers[key] = answer

    if st.button("응급도 확인하기 →", type="primary"):

        unanswered = [
            key for key, _ in qs
            if key not in st.session_state.answers
        ]

        if unanswered:
            st.warning("모든 질문에 답해주세요.")
            return

        calculate_urgency()
        go_to("result")


# =========================================================
# 응급도 계산
# =========================================================

def calculate_urgency():

    answers = st.session_state.answers
    emergency = st.session_state.emergency_type

    level = 1

    # 명백한 위험 신호
    emergency_signs = [
        "heavy",
        "pale_gums",
        "blue_gums",
        "collapse",
        "seizure_now",
        "heavy_bleeding",
        "cannot_stand",
        "large_burn"
    ]

    for sign in emergency_signs:
        if answers.get(sign) == "예":
            level = 3

    # 호흡 관련 위험
    if answers.get("breathing") == "아니오":
        level = 3

    # 의식 관련 위험
    if answers.get("conscious") == "아니오":
        level = 3

    # 중간 정도 위험 신호
    if level == 1:

        medium_signs = [
            "known_poison",
            "symptoms",
            "repeated",
            "blood",
            "weak",
            "face",
            "swelling",
            "repeat",
            "heavy_panting",
            "vomiting"
        ]

        for sign in medium_signs:
            if answers.get(sign) == "예":
                level = 2

    st.session_state.urgency_level = level


# =========================================================
# 5. 응급도 결과
# =========================================================

def result_page():

    level = st.session_state.urgency_level

    page_header(
        "응급도 확인 결과",
        "현재 입력된 정보를 기준으로 확인한 결과입니다.",
        "questions" if st.session_state.emergency_type != "other" else "other"
    )

    if level == 1:

        st.markdown("""
        <div class="urgent-box level-1">
            <h2>🟢 1단계 · 관찰</h2>
            <p><b>현재 확인된 위험 신호가 적습니다.</b></p>
            <p>상태를 계속 관찰하고 이상이 지속되면 동물병원에 연락하세요.</p>
        </div>
        """, unsafe_allow_html=True)

    elif level == 2:

        st.markdown("""
        <div class="urgent-box level-2">
            <h2>🟠 2단계 · 빠른 진료</h2>
            <p><b>가능한 한 빨리 동물병원에 연락하거나 방문하세요.</b></p>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="urgent-box level-3">
            <h2>🔴 3단계 · 응급</h2>
            <p><b>즉시 동물병원에 연락하고 응급진료를 받으세요.</b></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 확인된 정보")

    st.write(
        f"🐾 **종류:** {st.session_state.animal_type}"
    )

    st.write(
        f"⚖️ **체중:** {st.session_state.weight or '입력하지 않음'} kg"
    )

    st.write(
        f"🎂 **나이:** {st.session_state.age or '입력하지 않음'}"
    )

    if st.session_state.emergency_type == "other":

        st.markdown("### 현재 상황")

        st.info(st.session_state.other_situation)

    if st.button("🚑 응급처치 확인하기", type="primary"):
        go_to("first_aid")

    if st.button("🏥 바로 병원 찾기"):
        go_to("hospitals")


# =========================================================
# 응급처치 데이터
# =========================================================

first_aid_data = {

    "bleeding": {
        "title": "🩸 출혈",
        "do": [
            "깨끗한 거즈나 천으로 출혈 부위를 압박하세요.",
            "가능한 한 반려동물의 움직임을 줄이세요."
        ],
        "dont": [
            "상처에 임의로 약품을 바르지 마세요.",
            "박힌 물체를 억지로 제거하지 마세요."
        ],
        "hospital": [
            "출혈이 심하거나 계속되는 경우",
            "반려동물이 의식을 잃거나 심하게 약해지는 경우",
            "잇몸이나 혀가 창백하거나 푸른 경우"
        ]
    },

    "breathing": {
        "title": "😮 호흡곤란",
        "do": [
            "반려동물을 최대한 안정시키고 움직임을 줄이세요.",
            "호흡을 방해할 수 있는 요소가 있는지 확인하세요."
        ],
        "dont": [
            "억지로 물이나 음식을 먹이지 마세요.",
            "불필요하게 움직이거나 흥분시키지 마세요."
        ],
        "hospital": [
            "호흡이 매우 어렵거나 멈추는 경우",
            "잇몸이나 혀가 파랗거나 보라색인 경우",
            "의식을 잃거나 쓰러지는 경우"
        ]
    },

    "seizure": {
        "title": "🧠 발작 / 경련",
        "do": [
            "주변의 위험한 물건을 치워주세요.",
            "발작이 얼마나 지속되는지 시간을 확인하세요."
        ],
        "dont": [
            "입 안에 손이나 물건을 넣지 마세요.",
            "발작 중인 반려동물을 억지로 붙잡지 마세요."
        ],
        "hospital": [
            "발작이 오래 지속되는 경우",
            "발작이 반복되는 경우",
            "발작 후 의식이 돌아오지 않는 경우"
        ]
    },

    "poisoning": {
        "title": "☠️ 중독",
        "do": [
            "무엇을 먹었는지 확인할 수 있다면 정보를 확보하세요.",
            "가능한 한 빨리 동물병원에 연락하세요."
        ],
        "dont": [
            "수의사의 지시 없이 구토를 유도하지 마세요.",
            "임의로 약이나 음식을 먹이지 마세요."
        ],
        "hospital": [
            "독성 물질을 먹었을 가능성이 있는 경우",
            "경련이나 의식 저하가 있는 경우",
            "호흡이 이상한 경우"
        ]
    },

    "vomiting": {
        "title": "🤮 구토 / 설사",
        "do": [
            "증상의 횟수와 상태를 기록하세요.",
            "상태가 악화되는지 관찰하세요."
        ],
        "dont": [
            "사람용 약을 임의로 먹이지 마세요.",
            "상태가 심각한데 진료를 지연하지 마세요."
        ],
        "hospital": [
            "피가 섞여 있는 경우",
            "반복적으로 구토하거나 설사하는 경우",
            "심하게 처지거나 의식이 이상한 경우"
        ]
    },

    "burn": {
        "title": "🔥 화상",
        "do": [
            "가능하면 화상 부위를 깨끗한 흐르는 물로 식혀주세요.",
            "반려동물을 안정시키고 추가적인 손상을 막으세요."
        ],
        "dont": [
            "얼음을 직접 대지 마세요.",
            "화상 부위에 임의의 연고나 기름을 바르지 마세요."
        ],
        "hospital": [
            "화상 범위가 넓은 경우",
            "얼굴이나 입 주변에 화상이 있는 경우",
            "호흡 이상이 있는 경우"
        ]
    }
}


# =========================================================
# 6. 응급처치
# =========================================================

def first_aid_page():

    emergency = st.session_state.emergency_type

    page_header(
        "응급처치 안내",
        "현재 상황에서 필요한 행동을 확인하세요.",
        "result"
    )

    data = first_aid_data.get(emergency)

    if not data:

        st.warning(
            "현재 상황에 대한 구체적인 응급처치 안내가 준비되지 않았습니다."
        )

        st.info(
            "판단하기 어렵거나 상태가 심각하다면 가까운 동물병원에 연락하세요."
        )

    else:

        st.markdown(f"## {data['title']}")

        st.markdown("""
        <div class="action-box">
            <h3>✅ 지금 하세요</h3>
        """, unsafe_allow_html=True)

        for item in data["do"]:
            st.markdown(f"- **{item}**")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="action-box">
            <h3>❌ 하지 마세요</h3>
        """, unsafe_allow_html=True)

        for item in data["dont"]:
            st.markdown(f"- {item}")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="urgent-box level-3">
            <h3>🚨 바로 병원으로 가야 하는 경우</h3>
        """, unsafe_allow_html=True)

        for item in data["hospital"]:
            st.markdown(f"- **{item}**")

        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🏥 가까운 동물병원 찾기", type="primary"):
        go_to("hospitals")


# =========================================================
# 7. 병원 찾기
# =========================================================

def hospitals_page():

    page_header(
        "🏥 가까운 동물병원",
        "현재 위치 주변의 동물병원을 확인하세요.",
        "first_aid"
    )

    st.info(
        "현재 버전에서는 예시 동물병원 정보를 보여줍니다. "
        "실제 위치 기반 검색은 지도/병원 API를 연결하여 구현할 수 있습니다."
    )

    hospitals = [
        {
            "name": "서울동물병원",
            "distance": "1.2 km",
            "phone": "02-1234-5678",
            "open": "현재 운영 정보 확인 필요"
        },
        {
            "name": "우리동물메디컬센터",
            "distance": "2.1 km",
            "phone": "02-2345-6789",
            "open": "현재 운영 정보 확인 필요"
        },
        {
            "name": "24시 동물의료센터",
            "distance": "3.4 km",
            "phone": "02-3456-7890",
            "open": "응급진료 여부 확인 필요"
        }
    ]

    for hospital in hospitals:

        st.markdown(
            f"""
            <div class="action-box">
                <h3>🏥 {hospital['name']}</h3>
                <p>📍 거리: {hospital['distance']}</p>
                <p>📞 {hospital['phone']}</p>
                <p>🕐 {hospital['open']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "📞 전화하기",
                key=f"call_{hospital['name']}"
            ):
                st.info(
                    f"전화번호: {hospital['phone']}"
                )

        with col2:

            if st.button(
                "📋 정보 전달",
                key=f"send_{hospital['name']}"
            ):

                st.session_state.hospital_selected = hospital
                go_to("hospital_info")


# =========================================================
# 8. 병원 전달 정보
# =========================================================

def hospital_info_page():

    page_header(
        "📋 병원에 전달할 정보",
        "병원에 연락하기 전에 정보를 확인해주세요.",
        "hospitals"
    )

    st.markdown("### 🐾 반려동물")

    st.write(
        f"**종류:** {st.session_state.animal_type}"
    )

    st.write(
        f"**체중:** {st.session_state.weight or '입력하지 않음'} kg"
    )

    st.write(
        f"**나이:** {st.session_state.age or '입력하지 않음'}"
    )

    if st.session_state.disease:
        st.write(
            f"**기존 질환:** {st.session_state.disease}"
        )

    if st.session_state.medication:
        st.write(
            f"**복용 중인 약:** {st.session_state.medication}"
        )

    st.markdown("### 🚨 현재 상황")

    emergency_names = {
        "bleeding": "출혈",
        "breathing": "호흡곤란",
        "seizure": "발작 / 경련",
        "poisoning": "중독",
        "vomiting": "구토 / 설사",
        "burn": "화상",
        "injury": "외상 / 골절",
        "heatstroke": "열사병",
        "bite": "물림 / 쏘임",
        "other": "기타"
    }

    st.write(
        f"**응급상황:** "
        f"{emergency_names.get(st.session_state.emergency_type, '알 수 없음')}"
    )

    if st.session_state.other_situation:
        st.write(
            f"**상황 설명:** {st.session_state.other_situation}"
        )

    level_text = {
        1: "🟢 1단계 - 관찰",
        2: "🟠 2단계 - 빠른 진료",
        3: "🔴 3단계 - 응급"
    }

    st.write(
        f"**현재 응급도:** "
        f"{level_text.get(st.session_state.urgency_level, '확인 필요')}"
    )

    st.markdown("### 📞 병원에 전달하기")

    st.caption(
        "초기 버전에서는 실제 병원 시스템으로 정보가 직접 전송되지 않습니다."
    )

    if st.button("📋 정보 복사하기"):

        text = f"""
PetSOS 응급상황 정보

반려동물
- 종류: {st.session_state.animal_type}
- 체중: {st.session_state.weight}
- 나이: {st.session_state.age}

응급상황
- {emergency_names.get(st.session_state.emergency_type)}

응급도
- {level_text.get(st.session_state.urgency_level)}

기존 질환
- {st.session_state.disease or '없음'}

복용 중인 약
- {st.session_state.medication or '없음'}

특이사항
- {st.session_state.special_note or '없음'}
"""

        st.code(text)

        st.success(
            "위 정보를 복사하여 문자나 메신저 등으로 병원에 전달할 수 있습니다."
        )

    if st.session_state.hospital_selected:

        hospital = st.session_state.hospital_selected

        st.markdown(
            f"### 🏥 {hospital['name']}"
        )

        st.write(
            f"전화번호: {hospital['phone']}"
        )

        # 실제 전화 연결은 모바일 브라우저에서 tel: 링크 등을
        # 사용하는 방식으로 확장 가능
        st.markdown(
            f"""
            <a href="tel:{hospital['phone']}">
                <button style="
                    width:100%;
                    height:50px;
                    border:none;
                    border-radius:12px;
                    background:#167D8D;
                    color:white;
                    font-size:16px;
                    font-weight:bold;
                    cursor:pointer;">
                    📞 병원에 전화하기
                </button>
            </a>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# 페이지 Router
# =========================================================

page = st.session_state.page

if page == "pet_info":
    pet_info_page()

elif page == "emergency":
    emergency_page()

elif page == "other":
    other_page()

elif page == "questions":
    questions_page()

elif page == "result":
    result_page()

elif page == "first_aid":
    first_aid_page()

elif page == "hospitals":
    hospitals_page()

elif page == "hospital_info":
    hospital_info_page()
