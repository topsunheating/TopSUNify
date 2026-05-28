import streamlit as st
import os
import base64
import sys

# تنظیم مسیر برای ایمپورت ماژول‌ها
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ایمپورت ماژول‌های شما
import auth
import Financial
import main

# تنظیمات صفحه
st.set_page_config(page_title="TopSUNify", layout="wide")

# مدیریت وضعیت ورود
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if not st.session_state.logged_in:
    auth.render_auth_page()
    st.stop()

# تزریق CSS برای کنترل دقیق موبایل
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] { display: none !important; }
    .stApp { padding-bottom: 90px !important; }
    
    /* کانتینر اصلی ناوبری پایین - غیرقابل تغییر توسط استریم‌لیت */
    .fixed-nav-final {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 75px !important;
        background: #ffffff !important;
        display: flex !important;
        justify-content: space-around !important;
        align-items: center !important;
        border-top: 1px solid #e2e8f0 !important;
        z-index: 999999 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* استایل دکمه‌های ناوبری */
    .nav-button-custom {
        flex: 1 !important;
        background: none !important;
        border: none !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 11px !important;
        color: #94a3b8 !important;
        cursor: pointer !important;
    }
</style>
""", unsafe_allow_html=True)

# مدیریت تب‌ها
if "active_tab" not in st.session_state: st.session_state.active_tab = "dashboard"

# منطق نمایش محتوا (بخش‌های اصلی)
if st.session_state.active_tab == "dashboard":
    st.subheader("📊 داشبورد")
elif st.session_state.active_tab == "invoice":
    st.subheader("🧾 پیش‌فاکتور")
elif st.session_state.active_tab == "top_sunify":
    st.subheader("✨ تاپسان")
elif st.session_state.active_tab == "profile":
    st.subheader("👤 پروفایل")

# رندر کردن نوار ناوبری پایین (بدون ستون‌بندی استریم‌لیت)
st.markdown('<div class="fixed-nav-final">', unsafe_allow_html=True)

tabs = [("dashboard", "📊", "داشبورد"), ("invoice", "🧾", "فاکتور"), ("top_sunify", "✨", "تاپسان"), ("profile", "👤", "پروفایل")]

for tab_id, icon, label in tabs:
    # دکمه‌های ناوبری
    if st.button(f"{icon}\n{label}", key=f"nav_{tab_id}"):
        st.session_state.active_tab = tab_id
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
