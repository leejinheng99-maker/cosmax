import pathlib
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="10만원으로 내집마련 — 미국 주식 주간 리포트",
    page_icon="📈",
    layout="wide",
)

# Streamlit 기본 여백/헤더를 최대한 숨겨서 index.html이 전체 화면을 쓰도록 함
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        iframe {
            width: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# app.py와 같은 폴더에 있는 index.html을 읽어서 그대로 렌더링
HTML_PATH = pathlib.Path(__file__).parent / "index.html"
html_content = HTML_PATH.read_text(encoding="utf-8")

# 페이지가 길고(스크롤 필요) 내부에 모달/차트 등 동적 요소가 있으므로
# 넉넉한 높이 + 자체 스크롤 허용
components.html(html_content, height=6000, scrolling=True)
