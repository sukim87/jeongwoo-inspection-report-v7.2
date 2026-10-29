from datetime import date
from io import BytesIO
from pathlib import Path
import hashlib

import streamlit as st
from PIL import Image, ImageOps

from modules.application_reader import read_application
from modules.report_text import make_draft
from modules.excel_writer import build_report


BASE = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Jeongwoo AI 검사결과서",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 검사종류 및 검사코드
# =========================================================

INSPECTION_CODES = [
    ("서류검토", "DR"),
    ("열처리", "HT"),
    ("재료검사", "MI"),
    ("조립검사", "AS"),
    ("마킹검사", "MK"),
    ("압력시험", "PR"),
    ("취부검사", "FU"),
    ("성능시험", "PF"),
    ("치수검사", "DI"),
    ("비파괴검사", "NDE"),
    ("외관검사", "VI"),
    ("도장/도금", "PT"),
    ("가공검사", "MA"),
    ("포장/출하", "PK"),
    ("성형검사", "FM"),
    ("용접검사", "WD"),
]


# =========================================================
# 화면 스타일
# =========================================================

st.markdown(
    """
    <style>
    html,
    body,
    [class*="css"],
    [data-testid="stAppViewContainer"],
    [data-testid="stSidebar"] {
        font-family: "Malgun Gothic", "맑은 고딕", Arial, sans-serif !important;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2.7rem !important;
        padding-bottom: 3rem !important;
    }

    section[data-testid="stSidebar"] {
        background: #f1f3f6;
        border-right: 1px solid #d8dce2;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.3rem !important;
    }

    [data-testid="stSidebar"] img {
        background: white;
        border: 1px solid #e0e3e8;
        border-radius: 8px;
        padding: 11px;
    }

    .side-card {
        background: white;
        border: 1px solid #d8dce2;
        border-top: 3px solid #c8102e;
        border-radius: 8px;
        padding: 13px;
        margin-top: 10px;
        line-height: 1.65;
        font-size: 0.84rem;
    }

    .side-footer {
        color: #9299a3;
        font-size: 0.7rem;
        line-height: 1.55;
        margin-top: 17px;
    }

    .hero {
        background: linear-gradient(110deg, #97001c, #d51c3f);
        color: white;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 14px;
        box-shadow: 0 4px 14px rgba(100, 0, 20, 0.15);
    }

    .hero-title {
        font-size: 1.3rem;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .hero-text {
        font-size: 0.94rem;
        line-height: 1.6;
    }

    .sample-guide {
        background: #ffffff;
        border: 1px solid #d8dce2;
        border-left: 5px solid #c8102e;
        border-radius: 8px;
        padding: 12px 15px;
        margin-bottom: 9px;
        color: #333333;
        line-height: 1.55;
    }

    .section-head {
        background: #dedac8;
        border: 1px solid #222222;
        text-align: center;
        font-weight: 800;
        padding: 7px 10px;
        margin-top: 13px;
    }

    .section-box {
        border: 1px solid #222222;
        border-top: 0;
        padding: 13px 14px 7px 14px;
        background: white;
    }

    div[data-testid="stTextInput"] label,
    div[data-testid="stTextArea"] label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stSelectbox"] label,
    div[data-testid="stFileUploader"] label {
        font-weight: 800 !important;
        color: #111111 !important;
        font-size: 0.95rem !important;
    }

    input,
    textarea,
    [data-baseweb="select"] {
        font-weight: 650 !important;
        color: #111111 !important;
    }

    .stButton button,
    .stDownloadButton button {
        font-weight: 800 !important;
        border-radius: 8px !important;
        min-height: 43px;
    }

    .information-note {
        font-size: 0.79rem;
        color: #69727e;
        line-height: 1.55;
        margin: 4px 0 10px 0;
    }

    .download-area {
        border: 2px solid #c8102e
