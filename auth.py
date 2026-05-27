import streamlit as st
import os

def render_auth_page():
    # ۱. مرکز‌چین کردن فرم و استایل‌دهی اختصاصی به دکمه‌ها و کادرها
    st.markdown("""
        <style>
        /* استایل کانتینر اصلی فرم ورود */
        div[data-testid="stForm"] {
            border: 1px solid #e2e8f0 !important;
            border-radius: 20px !important;
            padding: 40px !important;
            background-color: #ffffff !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
            max-width: 450px;
            margin: 0 auto;
        }
        
        /* دکمه اصلی فرم */
        div[data-testid="stForm"] button {
            background-color: #ea580c !important;
            color: white !important;
            border-radius: 9999px !important;
            padding: 10px 30px !important;
            width: 100% !important;
            font-weight: bold !important;
            border: none !important;
        }
        
        /* تغییر رنگ دکمه تعویض حالت (ورود/ثبت‌نام) */
        .toggle-btn button {
            background-color: transparent !important;
            color: #ea580c !important;
            border: 1px solid #ea580c !important;
            border-radius: 9999px !important;
            width: 100% !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # نمایش لوگو و هدر در بالای فرم
    col_space1, col_center, col_space2 = st.columns(3)
    with col_center:
        try:
            st.image("./static/logo.png", width=120)
        except:
            st.title("☀️")
        st.markdown("<h2 style='text-align: center; margin-top:10px;'>TopSUNify</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color:#64748b;'>سامانه هوشمند تحلیل پلان گرمایشی</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # مدیریت وضعیت (که الان کاربر می‌خواهد وارد شود یا ثبت‌نام کند)
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login" # حالت پیش‌فرض: ورود

    # --- سناریو ورود به حساب کاربری ---
    if st.session_state.auth_mode == "login":
        with st.form("login_form"):
            st.markdown("<h4 style='text-align: center; color:#1e293b;'>ورود به حساب کاربری</h4>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            username = st.text_input("نام کاربری (یا ایمیل)", key="login_username", placeholder="نام کاربری خود را وارد کنید")
            password = st.text_input("رمز عبور", type="password", key="login_pass", placeholder="رمز عبور خود را وارد کنید")
            
            submit_login = st.form_submit_button("ورود به برنامه")
            
            if submit_login:
                if username == "admin" and password == "1234": # این یک مثال ساده است، بعداً به دیتابیس وصل می‌شود
                    st.session_state.logged_in = True
                    st.success("ورود با موفقیت انجام شد! در حال انتقال...")
                    st.rerun()
                else:
                    st.error("❌ نام کاربری یا رمز عبور اشتباه است.")

        # دکمه تغییر وضعیت به ثبت‌نام
        st.markdown("<p style='text-align: center; margin-top:20px; color:#64748b;'>هنوز حساب کاربری ندارید؟</p>", unsafe_allow_html=True)
        _, col_btn, _ = st.columns()
        with col_btn:
            if st.button("ایجاد حساب کاربری جدید", key="go_to_signup"):
                st.session_state.auth_mode = "signup"
                st.rerun()

    # --- سناریو ایجاد حساب کاربری جدید ---
    elif st.session_state.auth_mode == "signup":
        with st.form("signup_form"):
            st.markdown("<h4 style='text-align: center; color:#1e293b;'>ثبت‌نام و ایجاد حساب</h4>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            full_name = st.text_input("نام و نام خانوادگی", placeholder="مثال: علی علوی")
            new_username = st.text_input("نام کاربری فرضی", placeholder="فقط حروف انگلیسی یا اعداد")
            email = st.text_input("آدرس ایمیل", placeholder="example@mail.com")
            new_password = st.text_input("رمز عبور جدید", type="password", placeholder="حداقل ۶ کاراکتر")
            
            submit_signup = st.form_submit_button("ساخت حساب و ورود")
            
            if submit_signup:
                if not new_username or not new_password:
                    st.error("⚠️ تکمیل نام کاربری و رمز عبور الزامی است.")
                else:
                    # اینجا در آینده کد ذخیره در دیتابیس قرار می‌گیرد
                    st.session_state.logged_in = True
                    st.success("🎉 حساب کاربری شما با موفقیت ساخته شد!")
                    st.rerun()

        # دکمه تغییر وضعیت به ورود
        st.markdown("<p style='text-align: center; margin-top:20px; color:#64748b;'>قبلاً ثبت‌نام کرده‌اید؟</p>", unsafe_allow_html=True)
        _, col_btn, _ = st.columns()
        with col_btn:
            if st.button("ورود به حساب فعلی", key="go_to_login"):
                st.session_state.auth_mode = "login"
                st.rerun()
