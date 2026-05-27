import streamlit as st
import time

def render_auth_page():
    # --- ۱. تزریق CSS پیشرفته برای تراز کردن اجزا، تغییر فونت به ایران‌یکان و پاپ‌آپ ---
    auth_css = """
    <style>
    /* لود مستقیم فونت استاندارد ایران‌یکان (مشابه عکس‌های موبایلت) */
    @import url('https://cdn.jsdelivr.net/gh/rastikerdar/iran-yekan-font@v3.0.0/dist/font-face.css');
    
    * {
        font-family: 'iranyekan', Tahoma, sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    body, [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
    }
    
    /* حذف هدر پیش‌فرض */
    [data-testid="stHeader"] {
        display: none !important;
    }

    /* هدر لوگو و نوشته */
    .brand-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        max-width: 400px;
        margin: 0 auto 40px auto;
        padding: 0 10px;
    }
    .brand-title {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #000000 !important; /* رنگ مشکی طبق درخواست شما */
        margin: 0 !important;
    }

    /* استایل اختصاصی فیلدهای ورودی تک‌خطی (بدون باکس خاکستری) */
    div[data-testid="stTextInput"] {
        max-width: 400px;
        margin: 0 auto !important;
    }
    
    .stTextInput input {
        border-top: none !important;
        border-left: none !important;
        border-right: none !important;
        border-bottom: 1px solid #cbd5e1 !important;
        border-radius: 0px !important;
        background-color: transparent !important;
        padding: 12px 5px !important;
        font-size: 16px !important;
        color: #334155 !important;
    }
    .stTextInput input:focus {
        border-bottom: 2px solid #ea580c !important;
        box-shadow: none !important;
    }

    /* پنهان کردن کادر پیش‌فرض دکمه بیومتریک و نشاندن آن کنار پسورد */
    .bio-container {
        position: relative;
        max-width: 400px;
        margin: 0 auto;
    }
    
    /* موقعیت‌دهی دکمه بیومتریک در سمت چپ داخل فیلد پسورد */
    div.bio-inside-btn {
        position: absolute;
        left: 40px; /* کنار آیکون چشم خود استریم‌لیت */
        top: 36px;
        z-index: 99;
    }
    
    div.bio-inside-btn button {
        background: transparent !important;
        border: none !important;
        font-size: 20px !important;
        padding: 0 !important;
        color: #64748b !important;
        box-shadow: none !important;
    }

    /* ردیف رمز یکبار مصرف */
    .otp-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 400px;
        margin: 20px auto !important;
        padding: 0 5px;
    }
    
    /* دکمه اصلی ورود (نارنجی کامل) */
    div.stButton > button.orange-submit {
        width: 100% !important;
        max-width: 400px;
        display: block;
        margin: 25px auto 0 auto !important;
        background-color: #ea580c !important; /* نارنجی سازمانی */
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 0 !important;
        font-size: 16px !important;
        font-weight: bold !important;
    }
    
    /* لینک فراموشی رمز */
    .forgot-link {
        text-align: center;
        margin-top: 20px;
    }
    .forgot-link a {
        color: #2563eb !important;
        text-decoration: none;
        font-size: 14px;
    }

    /* 📌 استایل پاپ‌آپ بیومتریک بومی (Modal) */
    .bio-modal-overlay {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.4);
        z-index: 99999;
        display: flex;
        justify-content: center;
        align-items: flex-end; /* باز شدن از پایین صفحه مانند موبایل */
    }
    .bio-modal-card {
        background: white;
        width: 100%;
        max-width: 450px;
        border-top-left-radius: 24px;
        border-top-right-radius: 24px;
        padding: 30px 20px;
        box-shadow: 0 -10px 25px rgba(0,0,0,0.1);
        animation: slideUp 0.3s ease-out;
    }
    @keyframes slideUp {
        from { transform: translateY(100%); }
        to { transform: translateY(0); }
    }
    
    .bio-nav {
        display: flex;
        background: #f1f5f9;
        border-radius: 12px;
        padding: 4px;
        margin-bottom: 20px;
    }
    .bio-nav-btn {
        flex: 1;
        text-align: center;
        padding: 10px 0;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
        cursor: pointer;
    }
    .bio-nav-btn.active {
        background: #2563eb;
        color: white;
    }
    </style>
    """
    st.markdown(auth_css, unsafe_allow_html=True)

    # وضعیت‌های سیستم بیومتریک
    if "show_bio" not in st.session_state: st.session_state.show_bio = False
    if "bio_mode" not in st.session_state: st.session_state.bio_mode = "finger"

    # --- ۲. هدر: لوگو سمت راست، نوشته مشکی سمت چپ (کاملاً در یک راستا) ---
    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
    
    # ایجاد هدر هماهنگ با استفاده از سیستم کانتینر سفارشی برای دسکتاپ و موبایل
    h_col1, h_col2 = st.columns()
    with h_col1:
        st.markdown('<h2 style="color: #000000; font-weight: 900; margin: 10px 0 0 0; text-align: left; direction: ltr;">TopSUNify</h2>', unsafe_allow_html=True)
    with h_col2:
        try: st.image("./static/logo.png", width=65)
        except: st.write("☀️")

    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)

    # --- ۳. فیلد نام کاربری (پیش‌فرض خالی طبق درخواست شما) ---
    username = st.text_input("نام کاربری", value="", placeholder="نام کاربری")

    # --- ۴. فیلد رمز عبور + قرار دادن دکمه بیومتریک در کنار آن به صورت ساختار یافته ---
    st.markdown('<div class="bio-container">', unsafe_allow_html=True)
    password = st.text_input("رمز ورود", type="password", placeholder="رمز ورود")
    
    # دکمه کوچک بیومتریک که با زدنش پاپ‌آپ باز می‌شود
    st.markdown('<div class="bio-inside-btn">', unsafe_allow_html=True)
    if st.button("💳", help="ورود بیومتریک"):
        st.session_state.show_bio = True
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

    # --- ۵. ردیف استفاده از رمز یکبار مصرف (سویچ شیک) ---
    st.markdown('<div class="otp-row">', unsafe_allow_html=True)
    st.markdown('<span style="color: #475569; font-size: 15px;">استفاده از رمز یکبار مصرف</span>', unsafe_allow_html=True)
    otp_enabled = st.checkbox("", key="otp_toggle_clean")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ۶. دکمه ورود (نارنجی کامل و عریض) ---
    if st.button("ورود به TopSUNify", key="submit_orange", use_container_width=True):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("ورود با موفقیت انجام شد.")
            time.sleep(0.5)
            st.rerun()
        elif username == "" or password == "":
            st.warning("⚠️ لطفاً نام کاربری و رمز عبور را وارد نمایید.")
        else:
            st.error("❌ نام کاربری یا رمز ورود اشتباه است.")

    # --- ۷. بخش فعال‌سازی / فراموشی رمز ---
    st.markdown('<div class="forgot-link"><a href="#">فعال‌سازی / فراموشی رمز</a></div>', unsafe_allow_html=True)

    # --- ۸. پاپ‌آپ بیومتریک پیشرفته با قابلیت بسته شدن با کلیک روی صفحه (Overlay) ---
    if st.session_state.show_bio:
        # ایجاد یک کانتینر تمام صفحه. اگر کاربر روی دکمه "انصراف/بستن" بزند، پاپ‌آپ بسته می‌شود.
        st.markdown('<div class="bio-modal-overlay">', unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown('<h3 style="text-align: center; color: #1e293b;">ورود امن تاپسان</h3>', unsafe_allow_html=True)
            
            # سوییچ بین اثرانگشت و چهره
            b_col1, b_col2 = st.columns(2)
            if b_col1.button("Fingerprint", use_container_width=True):
                st.session_state.bio_mode = "finger"
                st.rerun()
            if b_col2.button("Face ID", use_container_width=True):
                st.session_state.bio_mode = "face"
                st.rerun()
                
            if st.session_state.bio_mode == "finger":
                st.markdown('<p style="text-align: center; color: #64748b; margin-top: 15px;">ورود با اثر انگشت<br><span style="font-size: 13px;">حسگر را لمس کنید</span></p>', unsafe_allow_html=True)
                st.markdown('<h1 style="text-align: center; font-size: 60px; margin: 10px 0;">☝️</h1>', unsafe_allow_html=True)
            else:
                st.markdown('<p style="text-align: center; color: #64748b; margin-top: 15px;">ورود با تشخیص چهره<br><span style="font-size: 13px;">به دوربین نگاه کنید</span></p>', unsafe_allow_html=True)
                st.markdown('<h1 style="text-align: center; font-size: 60px; margin: 10px 0;">👤</h1>', unsafe_allow_html=True)
            
            # دکمه خروج و بستن لمسی پاپ آپ
            if st.button("انصراف", use_container_width=True, key="exit_modal"):
                st.session_state.show_bio = False
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)
