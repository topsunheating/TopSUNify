import streamlit as st
import os
import base64
import jdatetime  
import ezdxf
import tempfile
import pandas as pd
from PIL import Image

# 🛑 تنظیمات صفحه
st.set_page_config(page_title="TopSUNify", layout="centered")

# ====================== ۱. احراز هویت ======================
import auth
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    auth.render_auth_page()
    st.stop()

# ====================== ۲. ایمپورت ماژول‌های مهندسی ======================
import Financial
import main
from Financial import calculate_tosunify_proforma, generate_proforma_pdf

# ====================== ۳. CSS سراسری و متمرکز (برای موبایل و دسکتاپ) ======================
def inject_custom_css():
    st.markdown("""
    <style>
        /* متمرکز کردن کل بدنه برنامه در دسکتاپ */
        .main > div {
            max-width: 600px !important;
            margin: 0 auto !important;
        }
        
        /* استایل منوی پایین که در مرکز قفل می‌شود */
        .final-bottom-nav {
            position: fixed !important;
            bottom: 0 !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
            width: 100% !important;
            max-width: 600px !important;
            height: 80px !important;
            background-color: #ffffff !important;
            border-top: 1px solid #e2e8f0 !important;
            box-shadow: 0 -4px 15px rgba(0,0,0,0.1) !important;
            z-index: 999999 !important;
            display: flex !important;
            justify-content: space-around !important;
            align-items: center !important;
        }
        
        .nav-item {
            display: flex; flex-direction: column; align-items: center;
            text-decoration: none; color: #64748b; font-size: 10px; font-weight: bold;
        }
        .nav-item.active { color: #ea580c !important; }
        .icon { font-size: 22px; margin-bottom: 4px; }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ====================== ۴. منطق تب‌ها ======================
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "dashboard"

# تغییر تب بر اساس پارامتر URL
query_params = st.query_params
if "nav_tab" in query_params:
    st.session_state.active_tab = query_params["nav_tab"]

# نمایش محتوا
tab = st.session_state.active_tab

if tab == "dashboard":
    st.title("📊 داشبورد")
    main.render_dashboard() # فرض بر اینکه در فایل main تابع رندر دارید
elif tab == "invoice":
    st.title("🧾 پیش‌فاکتور")
    Financial.render_proforma_ui() # فرض بر اینکه در فایل Financial تابع رندر دارید
elif tab == "topsunify":
    st.title("☀️ تاپسانیفای")
elif tab == "profile":
    st.title("👤 پروفایل")

# ====================== ۵. منوی پایین ======================
st.markdown('<div class="final-bottom-nav">', unsafe_allow_html=True)
items = [
    ("dashboard", "📊", "داشبورد"),
    ("invoice", "🧾", "پیش‌فاکتور"),
    ("topsunify", "☀️", "تاپسانیفای"),
    ("profile", "👤", "پروفایل")
]

for tab_id, icon, label in items:
    active_class = "active" if tab == tab_id else ""
    st.markdown(f'''
        <a href="?nav_tab={tab_id}" class="nav-item {active_class}">
            <div class="icon">{icon}</div>
            {label}
        </a>
    ''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
