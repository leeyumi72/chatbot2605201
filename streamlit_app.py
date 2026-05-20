import streamlit as st
from openai import OpenAI

# =========================
# 화면 설정
# =========================
st.set_page_config(
    page_title="문장 다듬기 챗봇",
    page_icon="✍️",
    layout="centered"
)

st.title("✍️ 문장 다듬기 챗봇")
st.write("문장을 입력하면 더 자연스럽고 읽기 좋게 다듬어줍니다.")

# =========================
# API 키
# GitHub 코드에는 API 키를 넣지 않습니다.
# Streamlit Cloud > Settings > Secrets 에만 넣습니다.
# =========================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 모델명은 필요하면 바꿀 수 있습니다.
MODEL = "gpt-4o-mini"

# =========================
# 문장 다듬기 규칙
# =========================
SYSTEM_PROMPT = """
너는 한국어 문장을 자연스럽게 다듬어주는 글쓰기 도우미다.

사용자가 문장을 입력하면 다음 방식으로 답한다.

1. 다듬은 문장
2. 왜 이렇게 고쳤는지 짧은 설명
3. 다른 표현 1개

규칙:
- 원래 의미를 바꾸지 않는다.
- 없는 내용을 새로 지어내지 않는다.
- 문장을 너무 과장하지 않는다.
- 한국어답고 자연스럽게 고친다.
- 사용자가 짧은 문장을 입력해도 친절하게 다듬어준다.
"""

# =========================
# 대화 기록
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "다듬고 싶은 문장을 입력해 주세요."
        }
    ]

# =========================
# 초기화 버튼
# =========================
if st.button("대화 초기화"):
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "대화를 다시 시작합니다. 다듬고 싶은 문장을 입력해 주세요."
        }
    ]
    st.rerun()

# =========================
# 이전 대화 보여주기
# =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# 사용자 입력
# =========================
user_message = st.chat_input("예: 오늘 너무 힘들었지만 그래도 잘 버틴 것 같아")

if user_message:
    st.session_state.messages.append(
        {"role": "user", "content": user_message}
    )

    with st.chat_message("user"):
        st.markdown(user_message)

    messages_for_api = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    with st.chat_message("assistant"):
        with st.spinner("문장을 다듬는 중입니다..."):
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages_for_api
            )

            assistant_message = response.choices[0].message.content
            st.markdown(assistant_message)

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_message}
    )
