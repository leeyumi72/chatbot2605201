import streamlit as st
from openai import OpenAI

st.title("💪 건강 정보 챗봇")
st.write(
    "생활 습관, 운동, 식습관, 건강 관리에 대해 쉽게 안내해주는 챗봇입니다. "
    "단, 이 챗봇은 의사의 진단이나 처방을 대신하지 않습니다."
)

openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("OpenAI API 키를 입력해 주세요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": """
너는 건강 정보 안내 챗봇이다.

역할:
- 사용자의 건강 고민을 친절하고 쉽게 설명한다.
- 식습관, 운동, 수면, 스트레스 관리 등 생활 습관 중심으로 조언한다.
- 어려운 의학 용어는 쉽게 풀어서 설명한다.

주의사항:
- 의사처럼 진단하지 않는다.
- 약 처방이나 복용량을 구체적으로 지시하지 않는다.
- 심한 통증, 호흡 곤란, 가슴 통증, 의식 저하, 갑작스러운 마비,
  고열 지속, 심한 출혈 같은 위험 증상이 있으면 즉시 병원이나 응급실을 안내한다.
- 답변 마지막에는 필요한 경우 전문의 상담을 권한다.

답변 스타일:
- 한국어로 답한다.
- 초보자도 이해하기 쉽게 설명한다.
- 핵심을 먼저 말하고, 실천 방법을 3~5개 정도 제안한다.
"""
            }
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("건강에 대해 궁금한 점을 입력하세요."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
