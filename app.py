import streamlit as st
import os
import base64
import jdatetime  
import ezdxf
import tempfile
import pandas as pd
from PIL import Image
import auth
from Financial import calculate_tosunify_proforma, generate_proforma_pdf, main # فرض بر اینکه ماژول‌ها در کنار فایل هستند

# --- کانفیگ اصلی ---
st.set_page_config(page_title="TopSUNify", layout="wide")

# --- احراز هویت ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if not st.session_state.logged_in:
    auth.render_auth_page()
    st.stop()

# --- CSS اختصاصی و اصلاح شده برای چیدمان موبایل ---
st.markdown("""
<style>
    /* پاکسازی کامل استایل‌های مزاحم */
    [data-testid="stHeader"], [data-testid="stSidebar"] { display: none !important; }
    
    .stApp { padding-bottom: 90px !important; background-color: #f8fafc !important; }

    /* نوار پایین ثابت که هرگز در موبایل نمی‌شکند */
    .mobile-nav-wrapper {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 80px !important;
        background: white !important;
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-around !important;
        align-items: center !important;
        border-top: 1px solid #e2e8f0 !important;
        z-index: 999999 !important;
        padding: 0 10px !important;
    }
    
    /* دکمه‌های ناوبری */
    .nav-btn-container {
        flex: 1 !important;
        display: flex !important;
        justify-content: center !important;
    }
</style>
""", unsafe_allow_html=True)

# --- مدیریت وضعیت‌ها ---
if "active_tab" not in st.session_state: st.session_state.active_tab = "dashboard"

# [بقیه کدهای منطق برنامه شما که قبلاً داشتید اینجا قرار می‌گیرد...]
# ... (کدهای مربوط به داشبورد، فاکتور، پروفایل و ...)

# --- بخش ناوبری اصلاح شده (جایگزین بخش قبلی) ---
st.markdown('<div class="mobile-nav-wrapper">', unsafe_allow_html=True)

tab_list = [
    ("dashboard", "📊", "داشبورد"),
    ("invoice", "🧾", "فاکتور"),
    ("top_sunify", "✨", "تاپسان"),
    ("profile", "👤", "پروفایل")
]

# نمایش دکمه‌ها بدون استفاده از استون‌بندی استریم‌لیت
# در اینجا از کلیدهای دکمه استفاده می‌کنیم که به صورت افقی چیده می‌شوند
for tab_id, icon, label in tab_list:
    # استفاده از یک کانتینر کوچک برای هر دکمه
    if st.button(f"{icon}\n{label}", key=f"btn_{tab_id}"):
        st.session_state.active_tab = tab_id
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
