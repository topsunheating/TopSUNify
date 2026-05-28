import streamlit as st
import os
import base64
import jdatetime  
import ezdxf
import tempfile
import pandas as pd
from PIL import Image
import auth
import Financial
import main
from Financial import calculate_tosunify_proforma, generate_proforma_pdf

st.set_page_config(page_title="TopSUNify", layout="wide")

# --- احراز هویت ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if not st.session_state.logged_in:
    auth.render_auth_page()
    st.stop()

# --- CSS نهایی و اصلاح شده برای نویگیشن ثابت موبایل ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] { display: none !important; }
    .main .block-container { padding-bottom: 120px !important; }
    
    /* نوار پایین ثابت که هرگز نمی‌شکند */
    .mobile-footer-nav {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 80px !important;
        background: white !important;
        display: flex !important;
        justify-content: space-around !important;
        align-items: center !important;
        border-top: 1px solid #e2e8f0 !important;
        z-index: 999999 !important;
    }
    
    .nav-btn-wrapper {
        flex: 1 !important;
        text-align: center !important;
    }
    
    /* حذف استایل‌های پیش‌فرض دکمه */
    div[data-testid="stButton"] button {
        background: transparent !important;
        border: none !important;
        width: 100% !important;
        height: 70px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- مدیریت وضعیت‌ها ---
if "active_tab" not in st.session_state: st.session_state.active_tab = "dashboard"

# [در اینجا کدهای منطق و تب‌های شما قرار می‌گیرد...]
if st.session_state.active_tab == "dashboard":
    st.subheader("📊 داشبورد")
elif st.session_state.active_tab == "invoice":
    st.subheader("🧾 پیش‌فاکتور")
# ... سایر تب‌ها ...

# --- نویگیشن پایین (بدون استفاده از st.columns) ---
st.markdown('<div class="mobile-footer-nav">', unsafe_allow_html=True)

tabs = [("dashboard", "📊", "داشبورد"), ("invoice", "🧾", "فاکتور"), ("top_sunify", "✨", "تاپسانیفای"), ("profile", "👤", "پروفایل")]

for tab_id, icon, label in tabs:
    # هر دکمه را در یک div با کلاس nav-btn-wrapper قرار می‌دهیم
    st.markdown(f'<div class="nav-btn-wrapper">', unsafe_allow_html=True)
    if st.button(f"{icon}\n{label}", key=f"nav_{tab_id}"):
        st.session_state.active_tab = tab_id
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
