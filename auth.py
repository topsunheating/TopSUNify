import streamlit as st
import time
import os
import base64

def render_auth_page():
    # خواندن وضعیت پاپ‌آ‌پ و تب‌ها از query_params برای پایداری کامل در کلیک‌ها
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

    # تبدیل آیکون biometric.png به base64 جهت استفاده پایدار
    bio_icon_base64 = ""
    if os.path.exists("biometric.png"):
        with open("biometric.png", "rb") as f:
            bio_icon_base64 = base64.b64encode(f.read()).decode()

    # لود کردن تصویر منظره برای پایین صفحه (landscape.jpg یا landscape.png)
    landscape_base64 = ""
    landscape_path = None
    for ext in ["jpg", "jpeg", "png"]:
        if os.path.exists(f"landscape.{ext}"):
            landscape_path = f"landscape.{ext}"
            break
            
    if landscape_path:
        with open(landscape_path, "rb") as f:
            landscape_base64 = base64.b64encode(f.read()).decode()

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
        overflow: hidden !important; /* جلوگیری از اسکرول خوردن کل صفحه */
    }}
   
    [data-testid="stHeader"] {{
        display: none !important;
    }}

    /* =======================================================
       اصلاحیه جدید: قفل کردن و ثابت نگه‌داشتن کل فرم ورود در مرکز صفحه
       ======================================================= */
    .fixed-auth-container {{
        position: fixed !important;
        top: 45% !important; /* تراز عمودی عالی */
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: 100% !important;
        max-width: 400px !important;
        padding: 0 20px !important;
        z-index: 100 !important;
        box-sizing: border-box !important;
    }}

    /* کانتینر هدر اصلی برای لوگوی تصویری */
    .brand-flex-container {{
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        margin: 0 auto 30px auto !important;
    }}
    
    .brand-flex-container img {{
        max-width: 220px !important;
        height: auto !important;
    }}

    /* هماهنگی کامل ابعاد فیلدها */
    div[data-testid="stTextInput"] {{
        width: 100% !important;
        max-width: 400px !important;
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

    /* ایجاد فضای خالی برای جا شدن منظم آیکون چشم و بیومتریک در سمت چپ */
    .stTextInput input[type="password"] {{
        padding-left: 85px !important;
    }}

    /* کانتینر نگهدارنده فیلد رمز ورود */
    .bio-container {{
        position: relative !important;
        width: 100% !important;
        max-width: 400px !important;
        margin: 0 auto !important;
    }}
   
    /* تنظیم دقیق و بردن آیکون به بالاتر جهت تراز شدن با مرکز عمودی چشم */
    .bio-html-btn {{
        position: absolute !important;
        left: 48px !important; 
        bottom: 24px !important; 
        z-index: 9999 !important;
        display: inline-block !important;
        width: 22px !important;
        height: 22px !important;
        background: url(data:image/png;base64,{bio_icon_base64}) no-repeat center !important;
        background-size: contain !important;
        cursor: pointer !important;
        opacity: 0.6 !important;
        transition: opacity 0.2s !important;
        border: none !important;
        text-decoration: none !important;
    }}
    .bio-html-btn:hover {{
        opacity: 1 !important;
    }}

    /* تنظیم و هماهنگی ابعاد دکمه ورود با فیلدها */
    div[data-testid="stElementContainer"] {{
        max-width: 400px !important;
        margin: 0 auto !important;
    }}

    /* استایل دکمه زرد رنگ، Bold و تنظیم سایز فونت روی 22px */
    div.stButton > button {{
        width: 100% !important;
        max-width: 400px !important;
        display: block !important;
        margin: 40px auto 0 auto !important;
        background-color: #ffd60a !important; 
        color: #1e293b !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 0 !important; 
        font-size: 22px !important; 
        font-weight: 900 !important; 
        box-shadow: 0 4px 6px -1px rgba(253, 224, 71, 0.2) !important;
        transition: all 0.2s ease-in-out !important;
    }}
    div.stButton > button p {{
        font-size: 22px !important;  
        font-weight: 900 !important; 
        margin: 0 !important;
        line-height: 1.2 !important;
    }}
    div.stButton > button:hover {{
        background-color: #ffc300 !important; 
        color: #000000 !important;
    }}
   
    .forgot-link {{
        text-align: center !important;
        margin-top: 25px !important;
        width: 100% !important;
        max-width: 400px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }}
    .forgot-link a {{
        color: #2563eb !important;
        text-decoration: none !important;
        font-size: 14px !important;
        font-weight: bold !important;
    }}

    /* =======================================================
       تصویر پس‌زمینه محدود به عرض ۴۰۰ پیکسل همراه با فید نرم به بالا
       ======================================================= */
    .landscape-wrapper {{
        position: fixed !important;
        bottom: 0 !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100% !important;
        max-width: 400px !important;
        height: 25vh !important;
        z-index: 1 !important;
        pointer-events: none !important;
    }}

    .bottom-landscape-bg {{
        width: 100% !important;
        height: 100% !important;
        background: url(data:image/jpeg;base64,{landscape_base64}) no-repeat center bottom !important;
        background-size: cover !important;
        -webkit-mask-image: linear-gradient(to top, rgba(0,0,0,1) 0%, rgba(0,0,0,0) 85%) !important;
        mask-image: linear-gradient(to top, rgba(0,0,0,1) 0%, rgba(0,0,0,0) 85%) !important;
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

    .popup-header-brand {{
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-bottom: 25px !important;
    }}
    
    .popup-header-brand img {{
        max-width: 180px !important;
        height: auto !important;
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
    </style>
    """
    st.markdown(auth_css, unsafe_allow_html=True)
   
    # --- لود لوگو/تایپوگرافی جدید سیستم (TopSUNify.png) ---
    logo_html = "☀️ TopSUNify"
    target_logo_path = "TopSUNify.png" if os.path.exists("TopSUNify.png") else "topsunify.png"
    
    if os.path.exists(target_logo_path):
        with open(target_logo_path, "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="display:block; margin: 0 auto;">'

    # --- شروع کانتینر ثابت و قفل شده‌ی فرم ورود ---
    st.markdown('<div class="fixed-auth-container">', unsafe_allow_html=True)

    # هدر اصلی فرم (لوگو)
    st.markdown(f"""
    <div class="brand-flex-container">
        {logo_html}
    </div>
    """, unsafe_allow_html=True)

    # فیلدهای ورودی نام کاربری و پسورد
    username = st.text_input("نام کاربری", value="", placeholder="نام کاربری")
    
    st.markdown('<div class="bio-container">', unsafe_allow_html=True)
    password = st.text_input("رمز ورود", type="password", placeholder="رمز ورود")
    st.markdown('<a href="?show_bio=true&bio_tab=fingerprint" target="_self" class="bio-html-btn"></a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # دکمه ورود زرد رنگ
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

    st.markdown('</div>', unsafe_allow_html=True)
    # --- پایان کانتینر ثابت فرم ورود ---


    # --- تزریق عکس منظره محدود شده با افکت محوشدگی نرم به بالا ---
    if landscape_base64:
        st.markdown("""
        <div class="landscape-wrapper">
            <div class="bottom-landscape-bg"></div>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================
    # پاپ‌آ‌پ بومی و فیکس شده
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

        popup_html_template = f"""
        <div class="popup-overlay"></div>
        <div class="popup-card-container">
            <div class="popup-header-brand">
                {logo_html}
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
