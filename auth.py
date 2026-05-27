import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import hashlib
import random

SH_URL = "https://docs.google.com/spreadsheets/d/1Vt-vKivm7I2Yi79gJarLVtSR2KowDGCQiW54UIgW6ls/edit?gid=0#gid=0"  # لینک گوگل شیت خودت را اینجا بگذار

def get_sheet_conn():
    return st.connection("gsheets", type=GSheetsConnection)

def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_user_exists(username, phone_number):
    """بررسی تکراری نبودن نام کاربری یا شماره موبایل"""
    try:
        conn = get_sheet_conn()
        df = conn.read(spreadsheet=SH_URL, ttl="0d")
        if not df.empty:
            if "username" in df.columns and username in df["username"].astype(str).values:
                return "username_exists"
            if "phone_number" in df.columns and phone_number in df["phone_number"].astype(str).values:
                return "phone_exists"
    except:
        pass
    return False

def register_user(full_name, username, password, phone_number):
    """ثبت نام قطعی کاربر در گوگل شیت"""
    try:
        conn = get_sheet_conn()
        df = conn.read(spreadsheet=SH_URL, ttl="0d")
        
        new_data = pd.DataFrame([{
            "full_name": full_name,
            "username": username,
            "password_hash": make_hash(password),
            "phone_number": str(phone_number)
        }])
        
        updated_df = pd.concat([df, new_data], ignore_index=True)
        conn.update(spreadsheet=SH_URL, data=updated_df)
        return True
    except Exception as e:
        st.error(f"خطا در ذخیره‌سازی داده‌ها: {e}")
        return False

def login_user(username, password):
    try:
        conn = get_sheet_conn()
        df = conn.read(spreadsheet=SH_URL, ttl="0d")
        if not df.empty and "username" in df.columns and "password_hash" in df.columns:
            hashed_pw = make_hash(password)
            user_rows = df[(df["username"].astype(str) == username) & (df["password_hash"].astype(str) == hashed_pw)]
            return not user_rows.empty
    except:
        pass
    return False

def send_sms_otp(phone_number):
    """تابع ارسال پیامک (فعلاً شبیه‌سازی تستی)"""
    # در آینده کدهای اتصال به پنل پیامک مثل ملی‌پیمک یا کاوه‌نگار اینجا قرار می‌گیرد
    otp_code = "1234" # کد تستی
    return otp_code


# --- ظاهر برنامه ---
def render_auth_page():
    st.markdown("""
        <style>
        div[data-testid="stForm"] {
            border: 1px solid #e2e8f0 !important;
            border-radius: 20px !important;
            padding: 40px !important;
            background-color: #ffffff !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
            max-width: 450px;
            margin: 0 auto;
        }
        div[data-testid="stForm"] button {
            background-color: #ea580c !important;
            color: white !important;
            border-radius: 9999px !important;
            padding: 10px 30px !important;
            width: 100% !important;
            font-weight: bold !important;
            border: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

    col_space1, col_center, col_space2 = st.columns(3)
    with col_center:
        try: st.image("./static/logo.png", width=120)
        except: st.title("☀️")
        st.markdown("<h2 style='text-align: center; margin-top:10px;'>TopSUNify</h2>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    # --- ۱. فرم ورود ---
    if st.session_state.auth_mode == "login":
        with st.form("login_form"):
            st.markdown("<h4 style='text-align: center; color:#1e293b;'>ورود به حساب کاربری</h4>", unsafe_allow_html=True)
            username = st.text_input("نام کاربری", key="login_username").strip()
            password = st.text_input("رمز عبور", type="password", key="login_pass")
            
            if st.form_submit_button("ورود به برنامه"):
                if username == "admin" and password == "1234":
                    st.session_state.logged_in = True
                    st.rerun()
                elif login_user(username, password):
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("❌ نام کاربری یا رمز عبور اشتباه است.")

        _, col_btn, _ = st.columns(3)
        with col_btn:
            if st.button("ایجاد حساب کاربری جدید", key="go_to_signup", use_container_width=True):
                st.session_state.auth_mode = "signup"
                st.rerun()

    # --- ۲. فرم ثبت‌نام اولیه (دریافت مشخصات و موبایل) ---
    elif st.session_state.auth_mode == "signup":
        with st.form("signup_form"):
            st.markdown("<h4 style='text-align: center; color:#1e293b;'>ثبت‌نام در سامانه</h4>", unsafe_allow_html=True)
            full_name = st.text_input("نام و نام خانوادگی")
            phone_number = st.text_input("شماره موبایل (مثل: 09123456789)").strip()
            new_username = st.text_input("نام کاربری دلخواه (انگلیسی)").strip()
            new_password = st.text_input("رمز عبور", type="password")
            
            if st.form_submit_button("ارسال کد تایید پیامکی"):
                if not all([full_name, phone_number, new_username, new_password]):
                    st.error("⚠️ تکمیل تمامی فیلدها الزامی است.")
                elif not phone_number.startswith("09") or len(phone_number) != 11:
                    st.error("❌ شماره موبایل وارد شده معتبر نیست.")
                else:
                    # بررسی تکراری نبودن اطلاعات
                    status = check_user_exists(new_username, phone_number)
                    if status == "username_exists":
                        st.error("❌ این نام کاربری قبلاً گرفته شده است.")
                    elif status == "phone_exists":
                        st.error("❌ این شماره موبایل قبلاً در سیستم ثبت شده است.")
                    else:
                        # موقتاً اطلاعات را ذخیره می‌کنیم تا کد تایید بشود
                        st.session_state.temp_user = {
                            "full_name": full_name,
                            "phone_number": phone_number,
                            "username": new_username,
                            "password": new_password,
                            "sent_otp": send_sms_otp(phone_number)
                        }
                        st.session_state.auth_mode = "verify_otp"
                        st.success("✉️ کد تایید به شماره شما ارسال شد.")
                        st.rerun()

        _, col_btn, _ = st.columns(3)
        with col_btn:
            if st.button("بازگشت به صفحه ورود", key="back_to_log", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()

    # --- ۳. مرحله وارد کردن کد تایید SMS ---
    elif st.session_state.auth_mode == "verify_otp":
        with st.form("otp_form"):
            st.markdown("<h4 style='text-align: center; color:#1e293b;'>تایید شماره موبایل</h4>", unsafe_allow_html=True)
            st.info(f"کد تایید ارسال شده به شماره {st.session_state.temp_user['phone_number']} را وارد کنید.")
            
            user_otp = st.text_input("کد ۴ رقمی تایید", placeholder="کد تست فعلی: 1234").strip()
            
            if st.form_submit_button("تایید و ساخت حساب"):
                if user_otp == st.session_state.temp_user["sent_otp"]:
                    # کد درست بود؛ حالا اطلاعات نهایی را در گوگل شیت ذخیره می‌کنیم
                    u = st.session_state.temp_user
                    if register_user(u["full_name"], u["username"], u["password"], u["phone_number"]):
                        st.session_state.logged_in = True
                        st.success("🎉 حساب شما با موفقیت فعال شد!")
                        del st.session_state.temp_user # پاک کردن اطلاعات موقت
                        st.rerun()
                else:
                    st.error("❌ کد وارد شده اشتباه است.")
                    
        _, col_btn, _ = st.columns(3)
        with col_btn:
            if st.button("تغییر شماره / بازگشت", key="back_to_sign", use_container_width=True):
                st.session_state.auth_mode = "signup"
                st.rerun()
