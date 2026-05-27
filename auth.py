import streamlit as st
import time
import os
import base64

def render_auth_page():
    # خواندن وضعیت پاپ‌آپ و تب‌ها از query_params برای پایداری کامل در کلیک‌ها
    show_bio = st.query_params.get("show_bio", "false") == "true"
    bio_tab = st.query_params.get("bio_tab", "fingerprint")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # --- ۱. تزریق فونت ایران‌یکان و استایل‌های پایه ---
    font_path = "iranyekan.ttf"
    font_base64 = ""
    if os.path.exists(font_path):
        with open(font_path, "rb") as f:
            font_base64 = base64.b64encode(f.read()).decode()

    # تبدیل آیکون جدید biometric.png به base64 جهت استفاده پایدار در استریم‌لیت
    bio_icon_base64 = ""
    if os.path.exists("biometric.png"):
        with open("biometric.png", "rb") as f:
            bio_icon_base64 = base64.b64encode(f.read()).decode()

    auth_css = f"""
    <style>
    @font-face {{
        font-family: 'iranyekan';
        src: url(data:font/ttf;base64,{font_base64}) format('truetype');
    }}
    * {{
        font-family: 'iranyekan', Tahoma, sans-serif !important;
        direction: rtl !important;
    }}
   
    body, [data-testid="stAppViewContainer"] {{
        background-color: #ffffff !important;
    }}
   
    [data-testid="stHeader"] {{
        display: none !important;
    }}

    /* هدر اصلی فرم ورود */
    .brand-flex-container {{
        display: flex !important;
        flex-direction: row-reverse !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 10px !important;
        width: 100% !important;
        max-width: 400px !important;
        margin: 0 auto 30px auto !important;
    }}
   
    .brand-title-text {{
        font-size: 26px !important;
        font-weight: 900 !important;
        color: #000000 !important;
        margin: 0 !important;
        line-height: 1 !important;
    }}

    div[data-testid="stTextInput"] {{
        max-width: 400px;
        margin: 0 auto !important;
    }}
   
    .stTextInput input {{
        border-top: none !important;
        border-left: none !important;
        border-right: none !important;
        border-bottom: 1px solid #e2e8f0 !important;
        border-radius: 0px !important;
        background-color: transparent !important;
        padding: 12px 5px !important;
        font-size: 16px !important;
        color: #1e293b !important;
        text-align: right !important;
    }}
    .stTextInput input:focus {{
        border-bottom: 2px solid #ea580c !important;
        box-shadow: none !important;
    }}

    .bio-container {{
        position: relative;
        max-width: 400px;
        margin: 0 auto;
    }}
   
    /* جایگذاری دکمه بیومتریک تصویری جدید در سمت چپ فیلد */
    div.bio-inside-btn {{
        position: absolute;
        left: 10px;
        top: 32px;
        z-index: 99;
    }}
   
    div.bio-inside-btn button {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        box-shadow: none !important;
        width: 28px !important;
        height: 28px !important;
        min-width: 28px !important;
        min-height: 28px !important;
        cursor: pointer !important;
    }}
    
    div.bio-inside-btn button img {{
        width: 100% !important;
        height: 100% !important;
        object-fit: contain !important;
        opacity: 0.7;
        transition: opacity 0.2s;
    }}
    div.bio-inside-btn button:hover img {{
        opacity: 1 !important;
    }}

    div.stButton > button.yellow-submit-btn {{
        width: 100% !important;
        max-width: 400px;
        display: block;
        margin: 40px auto 0 auto !important;
        background-color: #facc15 !important;
        color: #1e293b !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 0 !important;
        font-size: 16px !important;
        font-weight: bold !important;
    }}
    div.stButton > button.yellow-submit-btn:hover {{
        background-color: #ea580c !important;
        color: white !important;
    }}
   
    .forgot-link {{
        text-align: center;
        margin-top: 25px;
    }}
    .forgot-link a {{
        color: #2563eb !important;
        text-decoration: none;
        font-size: 14px;
        font-weight: bold;
    }}

    /* ==========================================
       استایل‌های پاپ‌آپ یکپارچه کاملاً فیکس شده
       ========================================== */

    .popup-overlay {{
        position: fixed !important;
        top: 0 !important; left: 0 !important;
        width: 100vw !important; height: 100vh !important;
        background: rgba(0, 0, 0, 0.55) !important;
        z-index: 999990 !important;
    }}

    .popup-card-container {{
        position: fixed !important;
        top: 50% !important; left: 50% !important;
        transform: translate(-50%, -50%) !important;
        background: white !important;
        width: 90% !important;
        max-width: 340px !important;
        border-radius: 24px !important;
        padding: 24px !important;
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.3) !important;
        z-index: 999995 !important;
        text-align: center !important;
        box-sizing: border-box !important;
    }}

    /* هدر پاپ‌آپ هماهنگ با چیدمان درخواست شده: اول لوگو سپس متن */
    .popup-header-brand {{
        display: flex !important;
        flex-direction: row !important; /* چیدمان افقی از چپ به راست برای ساختار انگلیسی نام برند */
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
        margin-bottom: 20px !important;
    }}

    .segment-tab-container {{
        display: flex !important;
        background: #f1f5f9 !important;
        padding: 4px !important;
        border-radius: 30px !important;
        margin-bottom: 25px !important;
        direction: ltr !important;
    }}
   
    .segment-btn {{
        flex: 1 !important;
        text-align: center !important;
        padding: 8px 0 !important;
        font-size: 14px !important;
        font-weight: bold !important;
        color: #64748b !important;
        text-decoration: none !important;
        border-radius: 25px !important;
        transition: all 0.2s !important;
    }}
   
    .segment-btn.active {{
        background: #2563eb !important;
        color: white !important;
    }}

    .html-cancel-link {{
        display: block !important;
        margin-top: 25px !important;
        color: #64748b !important;
        font-size: 16px !important;
        font-weight: bold !important;
        text-decoration: none !important;
        text-align: center !important;
        width: 100% !important;
    }}
    .html-cancel-link:hover {{
        color: #ef4444 !important;
    }}
    </style>
    """
    st.markdown(auth_css, unsafe_allow_html=True)
    st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
   
    # --- لود لوگو اصلی سیستم ---
    logo_html = "☀️"
    if os.path.exists("./static/logo.png"):
        with open("./static/logo.png", "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" width="45" style="display:inline-block; vertical-align:middle;">'

    # ایجاد تگ تصویر برای دکمه اثر انگشت جدید
    bio_btn_img = "🪪"
    if bio_icon_base64:
        bio_btn_img = f'<img src="data:image/png;base64,{bio_icon_base64}">'

    # --- هدر اصلی فرم ورود صفحه اصلی ---
    st.markdown(f"""
    <div class="brand-flex-container">
        {logo_html}
        <h2 class="brand-title-text">TopSUNify</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

    # --- فیلدهای ورودی نام کاربری و پسورد ---
    username = st.text_input("نام کاربری", value="", placeholder="نام کاربری")
    
    st.markdown('<div class="bio-container">', unsafe_allow_html=True)
    password = st.text_input("رمز ورود", type="password", placeholder="رمز ورود")
   
    st.markdown('<div class="bio-inside-btn">', unsafe_allow_html=True)
    # دکمه استریم‌لیت حاوی تصویر انیمیشنی اثر انگشت جدید شما
    if st.button(bio_btn_img, key="trigger_bio_popup_btn"):
        st.query_params["show_bio"] = "true"
        st.query_params["bio_tab"] = "fingerprint"
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

    # --- دکمه ورود اصلی ---
    if st.button("ورود به TopSUNify", key="submit_yellow_btn", use_container_width=True):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("ورود موفقیت‌آمیز بود.")
            time.sleep(0.5)
            st.rerun()
        elif username == "" or password == "":
            st.warning("⚠️ لطفاً نام کاربری و رمز عبور را وارد کنید.")
        else:
            st.error("❌ نام کاربری یا رمز ورود اشتباه است.")

    st.markdown('<div class="forgot-link"><a href="#">فعال‌سازی / فراموشی رمز</a></div>', unsafe_allow_html=True)

    # ==========================================
    # پاپ‌آ‌پ اصلاح‌شده با ساختار جدید هدر و تقارن لوگو/برند
    # ==========================================
    if show_bio:
        active_face = "active" if bio_tab == "face" else ""
        active_finger = "active" if bio_tab == "fingerprint" else ""

        if bio_tab == "fingerprint":
            graphic_content = """
                <h4 style="color: #1e293b; text-align: center !important; margin:0; font-weight:bold; font-size:18px; width:100%;">ورود با اثر انگشت</h4>
                <p style="text-align: center !important; color: #64748b; font-size: 13px; margin: 8px 0 20px 0; width:100%;">حسگر را لمس کنید</p>
                <div style="height: 20px;"></div>
            """
        else:
            graphic_content = """
                <h4 style="color: #1e293b; text-align: center !important; margin:0; font-weight:bold; font-size:18px; width:100%;">ورود با تشخیص چهره</h4>
                <p style="text-align: center !important; color: #64748b; font-size: 13px; margin: 8px 0 20px 0; width:100%;">به دوربین جلو نگاه کنید</p>
                <div style="height: 20px;"></div>
            """

        # رندر پاپ‌آپ با ترتیب جدید: اول لوگوی تاپ‌سان و سپس عبارت متنی برند
        popup_html_template = f"""
        <div class="popup-overlay"></div>
        <div class="popup-card-container">
            <div class="popup-header-brand">
                {logo_html}
                <span style="font-size: 16px; color:#475569; font-weight:800; direction:ltr;">TopSUNify</span>
            </div>
            
            <div class="segment-tab-container">
                <a href="?show_bio=true&bio_tab=face" target="_self" class="segment-btn {active_face}">Face ID</a>
                <a href="?show_bio=true&bio_tab=fingerprint" target="_self" class="segment-btn {active_finger}">Fingerprint</a>
            </div>
            
            <div style="min-height: 80px; direction: rtl !important; text-align: center !important;">
                {graphic_content}
            </div>
            
            <a href="?show_bio=false" target="_self" class="html-cancel-link">انصراف</a>
        </div>
        """
        st.html(popup_html_template)

    # اسکریپت اعمال کلاس دکمه ورود اصلی
    st.markdown("""
        <script>
        var buttons = window.parent.document.getElementsByTagName('button');
        for (var i = 0; i < buttons.length; i++) {
            if (buttons[i].innerText === "ورود به TopSUNify") {
                buttons[i].classList.add("yellow-submit-btn");
            }
        }
        </script>
    """, unsafe_allow_html=True)
