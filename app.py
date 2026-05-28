import streamlit as st
import os
import sys

# تنظیم مسیر برای ایمپورت ماژول‌ها
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ایمپورت ماژول‌های پروژه
import auth
import Financial
import main

# تنظیمات اصلی صفحه
st.set_page_config(page_title="TopSUNify", layout="wide")

# احراز هویت
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if not st.session_state.logged_in:
    auth.render_auth_page()
    st.stop()

# تزریق CSS برای استایل‌دهی و جلوگیری از بهم‌ریختگی موبایل
st.markdown("""
<style>
    /* مخفی کردن المان‌های پیش‌فرض استریم‌لیت */
    [data-testid="stHeader"], [data-testid="stSidebar"] { display: none !important; }
    
    /* فضای پایین برای اینکه محتوا زیر منو نرود */
    .stApp { padding-bottom: 100px !important; }
    
    /* نوار ناوبری ثابت */
    .nav-container {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 70px !important;
        background: white !important;
        display: flex !important;
        justify-content: space-around !important;
        align-items: center !important;
        border-top: 1px solid #e2e8f0 !important;
        z-index: 999999 !important;
    }
    
    /* استایل دکمه‌های ناوبری */
    div[data-testid="stButton"] button {
        border: none !important;
        background: none !important;
        font-size: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# مدیریت وضعیت تب‌ها
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "dashboard"

# نمایش محتوای اصلی (بر اساس تب انتخابی)
if st.session_state.active_tab == "dashboard":
    st.write("### 📊 داشبورد")
elif st.session_state.active_tab == "invoice":
    st.write("### 🧾 پیش‌فاکتور")
elif st.session_state.active_tab == "top_sunify":
    st.write("### ✨ تاپسان")
elif st.session_state.active_tab == "profile":
    st.write("### 👤 پروفایل")

# رندر نوار ناوبری (بدون استفاده از ستون‌بندی استریم‌لیت برای پایداری در موبایل)
st.markdown('<div class="nav-container">', unsafe_allow_html=True)

tabs = [("dashboard", "📊", "داشبورد"), ("invoice", "🧾", "فاکتور"), ("top_sunify", "✨", "تاپسان"), ("profile", "👤", "پروفایل")]

# ایجاد دکمه‌ها بدون ستون‌بندی
for tab_id, icon, label in tabs:
    if st.button(f"{icon}\n{label}", key=f"nav_{tab_id}"):
        st.session_state.active_tab = tab_id
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
