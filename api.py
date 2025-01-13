import streamlit as st
from openai import OpenAI
import time

# 페이지 설정
st.set_page_config(
    page_title="필로소피 AI EDU 교육팀 챗봇",
    page_icon="🎓",
    layout="wide"
)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "openai_client" not in st.session_state:
    st.session_state.openai_client = None

# 페이지 스타일링
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #2E4053;
    }
    </style>
""", unsafe_allow_html=True)

# 제목과 소개
st.title("🎓 필로소피 AI EDU 교육팀 챗봇")
st.markdown("""
    ### 환영합니다! 
    AI 교육의 전문가 팀이 여러분의 질문에 답변해드립니다.
""")

# 사이드바에 팀 소개
with st.sidebar:
    st.header("🤝 교육팀 소개")
    st.markdown("""
    **Sam - 교육 Needs 평가 및 계획 전문가**
    - 교육 needs 분석
    - 맞춤형 교육 계획 수립
    
    **Peter - AI 교육 전문가**
    - AI Ph.D 보유
    - AI 트레이닝 프로그램 설계
    
    **Jenny - AI in Education 전문가**
    - AI & Education Ph.D 보유
    - EdTech 및 AI 교육 방법론
    
    **William - 교육팀 리더**
    - 교육 프로그램 총괄
    - 전략적 방향 설정
    """)

# API 키 입력 섹션
api_key = st.text_input("OpenAI API 키를 입력하세요:", type="password")

if api_key:
    if st.session_state.openai_client is None:
        st.session_state.openai_client = OpenAI(api_key=api_key)
        
    # Assistant ID 설정
    assistant_id = "asst_afzqzKDfiL5izhDUfkJu54Lo"

    # 초기 웰컴 메시지
    if not st.session_state.messages:
        welcome_message = """안녕하세요! 필로소피 AI EDU 교육팀입니다. 🎓

저희는 AI 교육의 전문가 팀으로, 다음과 같은 도움을 제공해드릴 수 있습니다:

• 교육 needs 분석 및 맞춤형 교육 계획 수립
• AI 기술 및 개념에 대한 전문적인 교육
• AI 기반 교육 방법론 및 EdTech 활용 방안
• 교육 프로그램 설계 및 평가

어떤 분야에 대해 도움이 필요하신가요?"""
        
        st.session_state.messages.append({"role": "assistant", "content": welcome_message})

    # 채팅 인터페이스
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 처리
    if prompt := st.chat_input("질문을 입력해주세요..."):
        # 사용자 메시지 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Assistant 응답 생성
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                # 로딩 메시지 표시
                with st.spinner("답변을 생성하고 있습니다..."):
                    # 스레드 생성
                    thread = st.session_state.openai_client.beta.threads.create()
                    
                    # 메시지 추가
                    st.session_state.openai_client.beta.threads.messages.create(
                        thread_id=thread.id,
                        role="user",
                        content=prompt
                    )
                    
                    # 실행 시작
                    run = st.session_state.openai_client.beta.threads.runs.create(
                        thread_id=thread.id,
                        assistant_id=assistant_id
                    )
                    
                    # 실행 완료 대기
                    while run.status != "completed":
                        time.sleep(1)
                        run = st.session_state.openai_client.beta.threads.runs.retrieve(
                            thread_id=thread.id,
                            run_id=run.id
                        )

                    # 응답 가져오기
                    messages = st.session_state.openai_client.beta.threads.messages.list(
                        thread_id=thread.id
                    )
                    
                    # 최신 응답 표시
                    assistant_response = messages.data[0].content[0].text.value
                    message_placeholder.markdown(assistant_response)
                    
                    # 응답 저장
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

            except Exception as e:
                message_placeholder.error(f"오류가 발생했습니다: {str(e)}")
else:
    st.warning("🔑 계속하려면 OpenAI API 키를 입력해주세요.")

# 페이지 하단 정보
st.markdown("---")
st.markdown("© 2024 필로소피 AI EDU 교육팀 | AI 교육의 미래를 선도합니다.")
