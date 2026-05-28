import streamlit as st
import os
import sys

# تنظیم مسیر برای ایمپورت ماژول‌ها
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ایمپورت ماژول‌های پروژه
import auth
import Financial
import main

st.set_page_config(page_title="TopSUNify", layout="wide")

# احراز هویت
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if not st.session_state.logged_in:
    auth.render_auth_page()
    st.stop()

# --- CSS حرفه‌ای برای منوی پایین شبیه به اپلیکیشن‌های بانکی ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] { display: none !important; }
    .stApp { padding-bottom: 110px !important; }

    /* کانتینر اصلی منوی پایین */
    .mobile-menu-container {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 90px !important;
        background: white !important;
        display: flex !important;
        justify-content: space-around !important;
        align-items: center !important;
        border-top: 1px solid #e2e8f0 !important;
        z-index: 999999 !important;
        padding: 10px 0 !important;
    }

    /* دکمه‌های آیکون‌دار */
    .menu-item-button {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        width: 70px !important;
        text-decoration: none !important;
        color: #475569 !important;
        font-size: 11px !important;
        font-weight: 600 !important;
    }

    /* دایره آیکون */
    .icon-circle {
        width: 45px !important;
        height: 45px !important;
        background-color: #f1f5f9 !important;
        border-radius: 12px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 20px !important;
        margin-bottom: 5px !important;
        transition: 0.3s !important;
    }

    /* استایل وقتی دکمه فعال است */
    .active-circle { background-color: #ea580c !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# مدیریت وضعیت
if "active_tab" not in st.session_state: st.session_state.active_tab = "dashboard"

# نمایش محتوا
if st.session_state.active_tab == "dashboard": st.write("### 📊 داشبورد")
elif st.session_state.active_tab == "invoice": st.write("### 🧾 پیش‌فاکتور")
elif st.session_state.active_tab == "top_sunify": st.write("### ✨ تاپسان")
elif st.session_state.active_tab == "profile": st.write("### 👤 پروفایل")

# --- رندر کردن نویگیشن بار (ترکیبی از فرم و HTML برای عملکرد عالی) ---
st.markdown('<div class="mobile-menu-container">', unsafe_allow_html=True)

tabs = [("dashboard", "📊", "داشبورد"), ("invoice", "🧾", "فاکتور"), ("top_sunify", "✨", "تاپسان"), ("profile", "👤", "پروفایل")]

for tab_id, icon, label in tabs:
    active_class = "active-circle" if st.session_state.active_tab == tab_id else ""
    
    # برای اینکه دکمه کار کند، از دکمه استریم‌لیت با استایل مخفی استفاده می‌کنیم
    if st.button(f'<div class="icon-circle {active_class}">{icon}</div><div style="font-size:10px">{label}</div>', key=f"nav_{tab_id}"):
        st.session_state.active_tab = tab_id
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
