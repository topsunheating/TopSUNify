import streamlit as st
import time
import os
import base64
import pandas as pd
from PIL import Image
import auth 

# ۱. تنظیمات صفحه
st.set_page_config(
    page_title="TopSUNify",
    page_icon="./topsunify.png",
    layout="wide"
)

# کمی تاخیر برای بازیابی سشن
time.sleep(0.1)

# ۲. پاکسازی پارامترهای اضافه (اصلاح حیاتی برای جلوگیری از تداخل URL)
query_params = st.query_params
if "nav_tab" in query_params:
    selected_tab = query_params["nav_tab"]
    st.query_params.clear()
    st.query_params["nav_tab"] = selected_tab
    # مقدار اولیه تب فعال در سشن آپدیت می‌شود
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = selected_tab
    else:
        st.session_state.active_tab = selected_tab

# ۳. مقداردهی اولیه سشن
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "dashboard"

# ۴. دیباگ وضعیت (می‌توانید بعد از اطمینان کامل آن را کامنت کنید)
st.sidebar.title("دیباگ وضعیت")
st.sidebar.write("وضعیت لاگین:", st.session_state.logged_in)
st.sidebar.write("تب فعال:", st.session_state.active_tab)

# ۵. چک کردن وضعیت ورود
if not st.session_state.logged_in:
    auth.render_auth_page()
    st.stop()

# ==============================================================================
# بخش اصلی برنامه (بعد از تایید لاگین)
# ==============================================================================

st.write(f"شما در تب {st.session_state.active_tab} هستید.")

# اینجا کدهای داشبورد، فاکتور و سایر موارد خود را قرار دهید...

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
# ناوبری نهایی: کاملاً مستقل، افقی، چسبیده به پایین و بدون کد خام
# ==============================================================================

# در انتهای فایل app.py، به جای استفاده از HTML خالص، از این کد استفاده کنید:

st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True) # برای اینکه محتوا زیرِ دکمه‌های ثابت نرود

# کانتینر برای دکمه‌های ناوبری پایین صفحه
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)

def change_tab(tab_name):
    st.query_params["nav_tab"] = tab_name
    st.session_state.active_tab = tab_name
    st.rerun()

with nav_col1:
    if st.button("📊\nداشبورد", use_container_width=True, key="nav_dash"):
        change_tab("dashboard")
with nav_col2:
    if st.button("🧾\nپیش‌فاکتور", use_container_width=True, key="nav_inv"):
        change_tab("invoice")
with nav_col3:
    if st.button("📚\nتاپسان", use_container_width=True, key="nav_info"):
        change_tab("info")
with nav_col4:
    if st.button("👤\nپروفایل", use_container_width=True, key="nav_prof"):
        change_tab("profile")

# استایل CSS برای چسباندن این دکمه‌ها به پایین صفحه
# این بخش را جایگزین کد استایل قبلی در انتهای فایل app.py کنید
st.markdown("""
<style>
    /* تنظیم چیدمان دکمه‌ها در یک ردیف */
    [data-testid="column"] { 
        padding: 0px !important; 
        flex: 1 !important; 
    }
    
    div.row-widget.stButton { 
        position: fixed; 
        bottom: 0; 
        width: 25%; /* هر دکمه دقیقا یک چهارم عرض صفحه */
        margin: 0; 
        padding: 2px;
    }

    /* کوچک کردن متن و آیکون دکمه‌ها برای موبایل */
    button {
        font-size: 10px !important; /* سایز متن کوچکتر */
        padding: 5px 0 !important;
        height: 60px !important;
        white-space: nowrap !important; /* جلوگیری از شکستن خط متن */
    }

    /* برای جلوگیری از هم‌پوشانی محتوا با دکمه‌های پایین */
    .block-container {
        padding-bottom: 80px !important;
    }
</style>
""", unsafe_allow_html=True)
