import streamlit as st
import time

def render_auth_page():
    # --- ۱. تزریق CSS پیشرفته برای شبیه‌سازی دقیق موبایلت (نسخه تاپسان) ---
    auth_css = """
    <style>
    /* تنظیمات فونت و راست‌چین کلی */
    body, [data-testid="stAppViewContainer"] {
        direction: rtl !important;
        text-align: right !important;
        background-color: #f8fafc !important;
    }
    
    /* مخفی کردن هدر پیش‌فرض استریم‌لیت در صفحه لاگین */
    [data-testid="stHeader"] {
        display: none !important;
    }

    /* استایل اختصاصی فیلدهای ورودی (فقط خط زیرین - مشابه عکس) */
    .stTextInput input {
        border-top: none !important;
        border-left: none !important;
        border-right: none !important;
        border-bottom: 1.5px solid #cbd5e1 !important;
        border-radius: 0px !important;
        background-color: transparent !important;
        padding: 10px 5px !important;
        text-align: right !important;
        font-size: 16px !important;
        transition: border-color 0.3s;
    }
    .stTextInput input:focus {
        border-bottom-color: #ea580c !important; /* رنگ سازمانی نارنجی تاپسان */
        box-shadow: none !important;
    }

    /* زیباسازی دکمه اصلی ورود */
    div.stButton > button:first-child {
        width: 100% !important;
        background-color: #1e3a8a !important; /* سرمه‌ای شیک بانکی */
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 0 !important;
        font-size: 16px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #172554 !important;
    }

    /* پاپ آپ شبیه‌سازی شده بیومتریک (اثرانگشت / تشخیص چهره) */
    .biometric-modal {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0,0,0,0.4);
        z-index: 999999;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .biometric-card {
        background: white;
        border-radius: 24px;
        padding: 30px;
        width: 85%;
        max-width: 360px;
        text-align: center;
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
    }
    .bio-tabs {
        display: flex;
        background: #f1f5f9;
        border-radius: 999px;
        padding: 4px;
        margin-bottom: 25px;
    }
    .bio-tab {
        flex: 1;
        padding: 8px 0;
        font-size: 14px;
        font-weight: bold;
        border-radius: 999px;
        cursor: pointer;
    }
    .bio-tab.active {
        background: #2563eb;
        color: white;
    }
    .bio-tab.inactive {
        color: #64748b;
    }

    /* تصویر و وکتور پایینی صفحه لاگین */
    .login-footer-bg {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        height: 160px;
        background-image: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=600&q=80');
        background-size: cover;
        background-position: center;
        opacity: 0.85;
        z-index: -1;
        border-top-left-radius: 20px;
        border-top-right-radius: 20px;
    }
    </style>
    """
    st.markdown(auth_css, unsafe_allow_html=True)

    # مدیریت وضعیت باز شدن پاپ‌آپ بیومتریک
    if "show_bio" not in st.session_state: st.session_state.show_bio = False
    if "bio_mode" not in st.session_state: st.session_state.bio_mode = "finger" # یا face

    # --- ۲. هدر: آیکون تاپسان و عبارت TopSUNify در یک راستا ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        try: st.image("./static/logo.png", width=55)
        except: st.write("☀️")
    with col_title:
        st.markdown("<h2 style='margin-top:5px; color:#1e3a8a; font-weight:900;'>TopSUNify</h2>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- ۳. فیلد نام کاربری ---
    username = st.text_input("نام کاربری", value="rt_2026", placeholder="نام کاربری خود را وارد کنید")

    # --- ۴. فیلد رمز عبور + دکمه بیومتریک در کنار آن ---
    col_pass, col_bio_btn = st.columns([5, 1])
    with col_pass:
        password = st.text_input("رمز ورود", type="password", placeholder="••••••••")
    with col_bio_btn:
        st.markdown("<p style='margin:0;font-size:12px;color:transparent;'>.</p>", unsafe_allow_html=True) # همترازی
        # دکمه با اموجی اسکنر احراز هویت هوشمند
        if st.button("🪪", help="ورود با اثر انگشت / تشخیص چهره", use_container_width=True):
            st.session_state.show_bio = True
            st.rerun()

    # --- ۵. ردیف رمز یکبار مصرف (سویچ/کلید بغل) ---
    st.markdown("<br>", unsafe_allow_html=True)
    col_otp_text, col_otp_trigger = st.columns([4, 1])
    with col_otp_text:
        st.markdown("<p style='font-size: 15px; color:#475569; margin-top:5px;'>استفاده از رمز یکبار مصرف</p>", unsafe_allow_html=True)
    with col_otp_trigger:
        otp_enabled = st.checkbox("", key="otp_toggle", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ۶. دکمه اصلی ورود به TopSUNify ---
    if st.button("ورود به TopSUNify", use_container_width=True):
        # بررسی منطق ورود (رمز عادی یا حالت OTP)
        if otp_enabled:
            st.info("📟 کد یکبار مصرف به شماره همراه شما پیامک شد.")
        else:
            if username == "rt_2026" and password == "1234":
                st.session_state.logged_in = True
                st.success("ورود موفقیت‌آمیز بود!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ نام کاربری یا رمز ورود اشتباه است.")

    # --- ۷. عبارت فعال‌سازی / فراموشی رمز ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'><a href='#' style='color: #2563eb; text-decoration: none; font-weight: bold; font-size: 14px;'>فعال‌سازی / فراموشی رمز</a></p>", unsafe_allow_html=True)

    # --- ۸. پاپ‌آپ هوشمند اثر انگشت و تشخیص چهره (عکس اول شما) ---
    if st.session_state.show_bio:
        # شبیه‌سازی باکس پاپ‌آپ روی کل صفحه
        st.markdown("""
        <div class="biometric-modal">
            <div class="biometric-card">
                <h3 style="margin-top:0; color:#1e293b;">احراز هویت بیومتریک</h3>
                <p style="color:#64748b; font-size:13px; margin-bottom:20px;">لطفاً روش ورود امن خود را انتخاب کنید</p>
        """, unsafe_allow_html=True)
        
        # دکمه‌های ناوبری بین فیس‌آیدی و فینگرپرینت داخل پاپ‌آپ
        c_tab1, c_tab2 = st.columns(2)
        if c_tab1.button("Fingerprint ☝️", use_container_width=True):
            st.session_state.bio_mode = "finger"
        if c_tab2.button("Face 👤", use_container_width=True):
            st.session_state.bio_mode = "face"

        # نمایش المان متناسب با تب انتخاب شده
        if st.session_state.bio_mode == "finger":
            st.markdown("<h4 style='color:#1e3a8a; margin-top:20px;'>ورود با اثر انگشت</h4>", unsafe_allow_html=True)
            st.markdown("<p style='color:#64748b; font-size:14px;'>حسگر اثر انگشت روی گوشی را لمس کنید</p>", unsafe_allow_html=True)
            st.markdown("<h1 style='text-align:center; font-size:50px; margin:15px 0;'>🌀</h1>", unsafe_allow_html=True)
        else:
            st.markdown("<h4 style='color:#1e3a8a; margin-top:20px;'>ورود با تشخیص چهره</h4>", unsafe_allow_html=True)
            st.markdown("<p style='color:#64748b; font-size:14px;'>به دوربین جلوی گوشی نگاه کنید</p>", unsafe_allow_html=True)
            st.markdown("<h1 style='text-align:center; font-size:50px; margin:15px 0;'>📸</h1>", unsafe_allow_html=True)

        # دکمه انصراف و بستن پاپ آپ
        if st.button("❌ انصراف و بازگشت", key="close_bio"):
            st.session_state.show_bio = False
            st.rerun()
            
        st.markdown("</div></div>", unsafe_allow_html=True)

    # --- ۹. تصویر پس‌زمینه طبیعت در انتهای صفحه (مشابه عکس‌های ارسالی) ---
    st.markdown('<div class="login-footer-bg"></div>', unsafe_allow_html=True)
