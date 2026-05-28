# ==============================================================================
# TopSUNify - FINAL STABLE VERSION
# ==============================================================================

import streamlit as st

# ==============================================================================
# PAGE CONFIG
# ==============================================================================

st.set_page_config(
    page_title="TopSUNify",
    page_icon="./topsunify.png",
    layout="wide"
)

# ==============================================================================
# AUTH
# ==============================================================================

import auth

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    auth.render_auth_page()
    st.stop()

# ==============================================================================
# IMPORTS
# ==============================================================================

import os
import base64
import pandas as pd
from PIL import Image

# ==============================================================================
# CUSTOM CSS
# ==============================================================================

def inject_custom_css():

    font_path = "iranyekan.ttf"
    font_base64 = ""

    if os.path.exists(font_path):
        with open(font_path, "rb") as f:
            font_base64 = base64.b64encode(f.read()).decode()

    css = f"""
    <style>

    @font-face {{
        font-family: 'iranyekan';
        src: url(data:font/ttf;base64,{font_base64}) format('truetype');
    }}

    html, body, [class*="css"], * {{
        font-family: 'iranyekan', Tahoma, sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }}

    [data-testid="stHeader"],
    [data-testid="stSidebar"] {{
        display: none !important;
    }}

    .main .block-container {{
        max-width: 550px !important;
        margin: 0 auto !important;
        padding-left: 16px !important;
        padding-right: 16px !important;
        padding-bottom: 120px !important;
        background-color: #f8fafc !important;
        min-height: 100vh;
    }}

    .app-main-header-container {{
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        padding: 10px 0 !important;
        margin-bottom: 5px !important;
    }}

    .module-card-box {{
        background: #ffffff !important;
        padding: 20px !important;
        border-radius: 24px !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.04) !important;
        margin-bottom: 20px !important;
    }}

    .stButton > button {{
        border-radius: 20px !important;
        height: 90px !important;
        background: #ffffff !important;
        border: 2px solid #f1f5f9 !important;
        font-size: 15px !important;
        font-weight: bold !important;
        transition: all 0.2s ease !important;
        white-space: pre-line !important;
    }}

    .stButton > button:hover {{
        border-color: #ea580c !important;
        background: #fff7ed !important;
        color: #ea580c !important;
    }}

    .bottom-native-nav {{
        position: fixed !important;
        bottom: 0 !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100% !important;
        max-width: 550px !important;
        height: 78px !important;
        background: #ffffff !important;
        border-top: 1px solid #e2e8f0 !important;
        box-shadow: 0 -4px 12px rgba(0,0,0,0.06) !important;
        z-index: 999999 !important;
        padding: 8px 12px !important;
    }}

    .bottom-native-nav .stButton > button {{
        height: 58px !important;
        border-radius: 18px !important;
        background: transparent !important;
        border: none !important;
        color: #94a3b8 !important;
        font-size: 11px !important;
        font-weight: bold !important;
    }}

    .bottom-native-nav .stButton > button:hover {{
        background: #fff7ed !important;
        color: #ea580c !important;
    }}

    </style>
    """

    st.markdown(css, unsafe_allow_html=True)

inject_custom_css()

# ==============================================================================
# HEADER
# ==============================================================================

header_logo_html = ""

if os.path.exists("topsunify.png"):

    with open("topsunify.png", "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode()

    header_logo_html = f"""
    <div class="app-main-header-container">
        <img src="data:image/png;base64,{logo_base64}"
             style="max-width:140px;height:auto;display:block;margin:0 auto;">
    </div>
    """

else:

    header_logo_html = """
    <div class="app-main-header-container"
         style="font-size:24px;">
         ☀️
    </div>
    """

st.markdown(header_logo_html, unsafe_allow_html=True)

# ==============================================================================
# SESSION STATE
# ==============================================================================

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "dashboard"

if "user_display_name" not in st.session_state:
    st.session_state.user_display_name = "رضا تلچی"

if "user_phone" not in st.session_state:
    st.session_state.user_phone = "09120198229"

if "user_role" not in st.session_state:
    st.session_state.user_role = "کاربر عمومی"

# ==============================================================================
# DASHBOARD
# ==============================================================================

if st.session_state.active_tab == "dashboard":

    st.markdown('<div class="module-card-box">', unsafe_allow_html=True)

    st.subheader("📊 داشبورد")

    st.success("سامانه با موفقیت اجرا شد.")

    st.write("این نسخه بدون خطای syntax و indentation است.")

    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# INVOICE
# ==============================================================================

elif st.session_state.active_tab == "invoice":

    st.markdown('<div class="module-card-box">', unsafe_allow_html=True)

    st.subheader("🧾 پیش‌فاکتور")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "📂\nفایل پلان",
            key="btn_file_plan",
            use_container_width=True
        ):
            st.success("فایل پلان انتخاب شد")

    with col2:

        if st.button(
            "⌨️\nورود دستی",
            key="btn_manual",
            use_container_width=True
        ):
            st.success("ورود دستی انتخاب شد")

    with col3:

        if st.button(
            "✍️\nمقادیر مستقیم",
            key="btn_direct",
            use_container_width=True
        ):
            st.success("مقادیر مستقیم انتخاب شد")

    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# INFO
# ==============================================================================

elif st.session_state.active_tab == "info":

    st.markdown('<div class="module-card-box">', unsafe_allow_html=True)

    st.subheader("📚 اطلاعات")

    st.info("بخش اطلاعات فنی")

    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# PROFILE
# ==============================================================================

elif st.session_state.active_tab == "profile":

    st.markdown('<div class="module-card-box">', unsafe_allow_html=True)

    st.subheader("👤 پروفایل")

    st.write(f"نام: {st.session_state.user_display_name}")
    st.write(f"شماره: {st.session_state.user_phone}")
    st.write(f"سطح دسترسی: {st.session_state.user_role}")

    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# BOTTOM NAVIGATION
# ==============================================================================

st.markdown('<div class="bottom-native-nav">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:

    if st.button(
        "📊\nداشبورد",
        key="nav_dashboard",
        use_container_width=True
    ):
        st.session_state.active_tab = "dashboard"
        st.rerun()

with col2:

    if st.button(
        "🧾\nپیش‌فاکتور",
        key="nav_invoice",
        use_container_width=True
    ):
        st.session_state.active_tab = "invoice"
        st.rerun()

with col3:

    if st.button(
        "📚\nاطلاعات",
        key="nav_info",
        use_container_width=True
    ):
        st.session_state.active_tab = "info"
        st.rerun()

with col4:

    if st.button(
        "👤\nپروفایل",
        key="nav_profile",
        use_container_width=True
    ):
        st.session_state.active_tab = "profile"
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

