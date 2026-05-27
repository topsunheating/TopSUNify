import streamlit as st

def render_auth_page():
    # استایل کانتینر اصلی فرم ورود هماهنگ با تم نارنجی تاپ‌سانیفای
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

    # تقسیم صفحه به ۳ ستون مساوی برای قرارگیری فرم در وسط صفحه
    col_space1, col_center, col_space2 = st.columns(3)
    
    with col_center:
        try: st.image("./static/logo.png", width=120)
        except: st.title("☀️")
        st.markdown("<h2 style='text-align: center; margin-top:10px;'>TopSUNify</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color:#64748b;'>سامانه هوشمند تحلیل پلان گرمایشی</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    # --- فرم ورود ---
    if st.session_state.auth_mode == "login":
        with st.form("login_form"):
            st.markdown("<h4 style='text-align: center; color:#1e293b;'>ورود به حساب کاربری</h4>", unsafe_allow_html=True)
            username = st.text_input("نام کاربری", key="login_username", placeholder="نام کاربری را وارد کنید")
            password = st.text_input("رمز عبور", type="password", key="login_pass", placeholder="رمز عبور را وارد کنید")
            
            if st.form_submit_button("ورود به برنامه"):
                if username == "admin" and password == "1234":  # نام کاربری و رمز عبور تست
                    st.session_state.logged_in = True
                    st.success("ورود با موفقیت انجام شد!")
                    st.rerun()
                else:
                    st.error("❌ نام کاربری یا رمز عبور اشتباه است.")

        _, col_btn, _ = st.columns(3)
        with col_btn:
            if st.button("ایجاد حساب کاربری جدید", key="go_to_signup", use_container_width=True):
                st.session_state.auth_mode = "signup"
                st.rerun()

    # --- فرم ثبت نام ---
    elif st.session_state.auth_mode == "signup":
        with st.form("signup_form"):
            st.markdown("<h4 style='text-align: center; color:#1e293b;'>ثبت‌نام و ایجاد حساب</h4>", unsafe_allow_html=True)
            full_name = st.text_input("نام و نام خانوادگی")
            new_username = st.text_input("نام کاربری جدید")
            new_password = st.text_input("رمز عبور", type="password")
            
            if st.form_submit_button("ساخت حساب و ورود"):
                if not new_username or not new_password:
                    st.error("⚠️ تکمیل نام کاربری و رمز عبور الزامی است.")
                else:
                    st.session_state.logged_in = True
                    st.success("🎉 حساب کاربری شما با موفقیت ساخته شد!")
                    st.rerun()

        _, col_btn, _ = st.columns(3)
        with col_btn:
            if st.button("ورود با حساب فعلی", key="go_to_login", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()
