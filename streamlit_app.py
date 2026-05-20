import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="나만의 챗봇",
    page_icon="💬",
    layout="centered"
)

st.title("💬 나만의 챗봇")
st.write("간단한 질문을 입력하면 AI가 답변합니다.")

# API 키는 코드에 넣지 않습니다.
# Streamlit Cloud의 Secrets에 OPENAI_API_KEY로 따로 저장하세요.
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """
너는 친절하고 쉽게 설명하는 한국어 챗봇이다.
답변은 너무 길지 않게 하고, 초보자도 이해할 수 있게 말한다.
모르는 것은 지어내지 말고 모른다고 말한다.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요. 무엇이든 물어보세요."}
    ]

if st.button("대화 초기화"):
    st.session_state.messages = [
        {"role": "assistant", "content": "대화를 다시 시작합니다. 무엇이든 물어보세요."}
    ]
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_message = st.chat_input("메시지를 입력하세요")

if user_message:
    st.session_state.messages.append(
        {"role": "user", "content": user_message}
    )

    with st.chat_message("user"):
        st.markdown(user_message)

    messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages_for_api += st.session_state.messages

    with st.chat_message("assistant"):
        with st.spinner("답변을 작성하는 중입니다..."):
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages_for_api
            )

            assistant_message = response.choices[0].message.content
            st.markdown(assistant_message)

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_message}
    )
