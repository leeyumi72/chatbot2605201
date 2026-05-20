import streamlit as st
from openai import OpenAI

# =====================================================
# 기본 설정
# =====================================================
st.set_page_config(
    page_title="문장 다듬기 앱",
    page_icon="✍️",
    layout="wide"
)

# =====================================================
# 디자인 CSS
# =====================================================
st.markdown(
    """
    <style>
    .main {
        background-color: #fafafa;
    }

    .title-box {
        padding: 2.5rem 0 1rem 0;
    }

    .main-title {
        font-size: 3rem;
        font-weight: 800;
        color: #2f3340;
        margin-bottom: 0.3rem;
    }

    .sub-title {
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }

    .notice-box {
        background-color: #fff7ed;
        border: 1px solid #fed7aa;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        color: #9a3412;
        margin-bottom: 1.5rem;
    }

    .result-card {
        background-color: white;
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 8px 24px rgba(0,0,0,0.04);
        margin-top: 1rem;
    }

    .small-label {
        font-size: 0.9rem;
        font-weight: 700;
        color: #4b5563;
        margin-bottom: 0.4rem;
    }

    .footer-text {
        font-size: 0.85rem;
        color: #9ca3af;
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# API 연결
# API 키는 코드에 직접 넣지 않습니다.
# Streamlit Cloud의 Secrets에 OPENAI_API_KEY로 저장합니다.
# =====================================================
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    st.error("OPENAI_API_KEY가 설정되지 않았습니다. Streamlit Cloud의 Secrets에 API 키를 등록해 주세요.")
    st.stop()

MODEL = st.secrets.get("OPENAI_MODEL", "gpt-4o-mini")

# =====================================================
# 사이드바
# =====================================================
with st.sidebar:
    st.header("⚙️ 설정")

    tone = st.selectbox(
        "문장 톤",
        [
            "자연스럽게",
            "전문적으로",
            "부드럽게",
            "짧고 간결하게",
            "인스타그램 문구처럼",
            "이메일 문장처럼"
        ]
    )

    length = st.selectbox(
        "길이",
        [
            "원문과 비슷하게",
            "더 짧게",
            "조금 더 풍부하게"
        ]
    )

    st.divider()

    st.caption("API 키는 화면에 표시되지 않습니다.")
    st.caption("GitHub 코드에도 API 키를 넣지 않습니다.")

# =====================================================
# 메인 화면
# =====================================================
left, center, right = st.columns([1, 2.2, 1])

with center:
    st.markdown(
        """
        <div class="title-box">
            <div class="main-title">✍️ 문장 다듬기 앱</div>
            <div class="sub-title">어색한 문장을 자연스럽고 읽기 좋게 바꿔보세요.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="notice-box">
        이 앱은 테스트용입니다. 입력한 문장을 바탕으로 표현을 다듬어 줍니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    user_text = st.text_area(
        "다듬고 싶은 문장",
        placeholder="예: 오늘 너무 힘들었지만 그래도 잘 버틴 것 같아",
        height=180
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        run_button = st.button("문장 다듬기", use_container_width=True)

    with col2:
        clear_button = st.button("비우기", use_container_width=True)

    if clear_button:
        st.rerun()

    if run_button:
        if not user_text.strip():
            st.warning("먼저 다듬고 싶은 문장을 입력해 주세요.")
        else:
            prompt = f"""
너는 한국어 문장을 자연스럽고 읽기 좋게 다듬어주는 글쓰기 도우미다.

사용자가 입력한 문장을 아래 조건에 맞게 고쳐라.

조건:
- 문장 톤: {tone}
- 문장 길이: {length}
- 원문의 의미는 바꾸지 말 것
- 없는 내용을 새로 만들지 말 것
- 너무 과장하지 말 것
- 한국어답고 자연스럽게 고칠 것

사용자 문장:
{user_text}

답변 형식:
### 다듬은 문장
수정된 문장

### 수정 이유
- 이유 1
- 이유 2

### 다른 표현
대안 문장 1개
"""

            with st.spinner("문장을 다듬는 중입니다..."):
                try:
                    response = client.chat.completions.create(
                        model=MODEL,
                        messages=[
                            {
                                "role": "system",
                                "content": "너는 한국어 문장을 자연스럽게 다듬는 글쓰기 도우미다."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )

                    result = response.choices[0].message.content

                    st.markdown(
                        '<div class="result-card">',
                        unsafe_allow_html=True
                    )
                    st.markdown(result)
                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )

                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")

    st.markdown(
        """
        <div class="footer-text">
        GitHub에는 API 키를 올리지 말고, Streamlit Cloud Secrets에만 저장하세요.
        </div>
        """,
        unsafe_allow_html=True
    )
