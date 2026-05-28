import streamlit as st
import time
import os
import base64

def render_auth_page():
    def render_auth_page():
    # اگر کاربر قبلاً لاگین کرده، اصلاً نیازی به بررسی query_params نیست
    if st.session_state.get("logged_in", False):
        return 

    # حالا بررسی‌های مربوط به فرم ورود
    show_bio = st.query_params.get("show_bio", "false") == "true"
    # ... بقیه کدهای شما
    # خواندن وضعیت پاپ‌آ‌پ، تب‌ها و مقادیر فرم از query_params برای پایداری کامل
    show_bio = st.query_params.get("show_bio", "false") == "true"
    bio_tab = st.query_params.get("bio_tab", "fingerprint")
    
    # دریافت اطلاعات فیلدها از فرم HTML
    form_submitted = st.query_params.get("login_submit", "false") == "true"
    username_val = st.query_params.get("u", "").strip()
    password_val = st.query_params.get("p", "").strip()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # بررسی وضعیت ورود پس از سابمیت فرم HTML
    if form_submitted:
        # st.query_params.update({"login_submit": "false"}) # این خط دیگر لازم نیست
        
        if username_val == "admin" and password_val == "1234":
            st.session_state.logged_in = True
            st.success("ورود موفقیت‌آمیز بود.")
            
            # --- اینجاست که باید پاک‌سازی را انجام دهید ---
            st.query_params.clear()  # پاک کردن تمام پارامترهای URL برای جلوگیری از تداخل
            
            time.sleep(0.5)
            st.rerun()
            
        elif username_val == "" or password_val == "":
            st.warning("⚠️ لطفاً نام کاربری و رمز عبور را وارد کنید.")
        else:
            st.error("❌ نام کاربری یا رمز ورود اشتباه است.")
            # اختیاری: پاک کردن پارامترهای اشتباه برای جلوگیری از گیر کردن در وضعیت خطا
            st.query_params.clear()

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

    # تبدیل لوگوی ترکیبی TopSUN-Powered.png به base64
    powered_logo_base64 = ""
    if os.path.exists("TopSUN-Powered.png"):
        with open("TopSUN-Powered.png", "rb") as f:
            powered_logo_base64 = base64.b64encode(f.read()).decode()

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
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"], .main {{
        background-color: #ffffff !important;
        overflow: hidden !important; 
        height: 100vh !important;
        width: 100vw !important;
        margin: 0 !important;
        padding: 0 !important;
    }}
   
    [data-testid="stHeader"], [data-testid="stSidebar"] {{
        display: none !important;
    }}

    * {{
        font-family: 'iranyekan', Tahoma, sans-serif !important;
        direction: rtl !important;
        box-sizing: border-box !important;
    }}

    .fixed-auth-card {{
        position: fixed !important;
        top: 36% !important; 
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: 100% !important;
        max-width: 400px !important;
        padding: 0 25px !important;
        z-index: 99990 !important;
    }}

    .brand-flex-container {{
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        margin-bottom: 30px !important;
    }}
    
    .brand-flex-container img {{
        max-width: 220px !important;
        height: auto !important;
    }}

    .input-wrapper {{
        width: 100% !important;
        margin-bottom: 18px !important;
        position: relative !important;
    }}

    .input-wrapper label {{
        display: block !important;
        font-size: 14px !important;
        color: #64748b !important;
        margin-bottom: 4px !important;
        font-weight: bold !important;
    }}

    .native-input {{
        width: 100% !important;
        border-top: none !important;
        border-left: none !important;
        border-right: none !important;
        border-bottom: 1px solid #e2e8f0 !important;
        border-radius: 0px !important;
        background-color: transparent !important;
        padding: 10px 5px !important;
        font-size: 16px !important;
        color: #1e293b !important;
        text-align: right !important;
        outline: none !important;
    }}
    
    .native-input:focus {{
        border-bottom: 2px solid #ea580c !important;
    }}

    .password-field {{
        padding-left: 50px !important;
    }}
   
    .bio-html-btn {{
        position: absolute !important;
        left: 10px !important; 
        bottom: 10px !important; 
        z-index: 100000 !important;
        display: inline-block !important;
        width: 24px !important;
        height: 24px !important;
        background: url(data:image/png;base64,{bio_icon_base64}) no-repeat center !important;
        background-size: contain !important;
        cursor: pointer !important;
        opacity: 0.6 !important;
        border: none !important;
    }}
    .bio-html-btn:hover {{
        opacity: 1 !important;
    }}

    .native-submit-btn {{
        width: 100% !important;
        background-color: #ffd60a !important; 
        color: #1e293b !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 0 !important; 
        font-size: 22px !important; 
        font-weight: 900 !important; 
        box-shadow: 0 4px 6px -1px rgba(253, 224, 71, 0.2) !important;
        cursor: pointer !important;
        margin-top: 25px !important;
        text-align: center !important;
    }}
    
    .native-submit-btn:hover {{
        background-color: #ffc300 !important; 
        color: #000000 !important;
    }}
   
    .forgot-link {{
        text-align: center !important;
        margin-top: 14px !important; 
        width: 100% !important;
    }}
    .forgot-link a {{
        color: #2563eb !important;
        text-decoration: none !important;
        font-size: 14px !important;
        font-weight: bold !important;
    }}

    /* =======================================================
       تنظیم ابعاد جدید: سایز لوگو به درخواست شما نصف (78px) شد
       ======================================================= */
    .topsun-powered-footer-container {{
        position: fixed !important;
        bottom: 26.5vh !important; /* مماس و فیکس شده دقیقاً بالای لبه منظره */
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100% !important;
        max-width: 400px !important;
        padding: 0 25px !important; /* هم‌اندازه با حاشیه فیلدها */
        display: flex !important;
        flex-direction: column !important;
        align-items: flex-end !important; /* تراز راست (راست‌نویس واقعی) */
        z-index: 99988 !important;
    }}
    
    .topsun-powered-image-node {{
        max-width: 78px !important; /* سایز نصف شده برای ظرافت و زیبایی بیشتر */
        height: auto !important;
        display: block !important;
        opacity: 0.95 !important;
    }}

    /* =======================================================
       تصویر پس‌زمینه فیکس شده با افکت محوشدگی نرم به بالا
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
       استایل‌های پاپ‌آ‌پ بومی
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
   
    # --- لود لوگو/تایپوگرافی اصلی سیستم (TopSUNify.png) ---
    logo_html = "☀️ TopSUNify"
    target_logo_path = "TopSUNify.png" if os.path.exists("TopSUNify.png") else "topsunify.png"
    
    if os.path.exists(target_logo_path):
        with open(target_logo_path, "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="display:block; margin: 0 auto;">'

    # --- تنظیم ساختار نمایش تصویر یکپارچه TopSUN-Powered.png ---
    powered_layout_html = ""
    if powered_logo_base64:
        powered_layout_html = f'<img src="data:image/png;base64,{powered_logo_base64}" class="topsun-powered-image-node">'

    # تنظیم فیلدها در صورت پر بودن فرم
    curr_u = username_val if form_submitted else ""
    curr_p = password_val if form_submitted else ""

    native_form_html = f"""
    <div class="fixed-auth-card">
        <form method="get" action="">
            <input type="hidden" name="login_submit" value="true">
            <input type="hidden" name="show_bio" value="{str(show_bio).lower()}">
            <input type="hidden" name="bio_tab" value="{bio_tab}">
            
            <div class="brand-flex-container">
                {logo_html}
            </div>
            
            <div class="input-wrapper">
                <label>نام کاربری</label>
                <input type="text" name="u" class="native-input" value="{curr_u}" placeholder="نام کاربری" autocomplete="off" required>
            </div>
            
            <div class="input-wrapper">
                <label>رمز ورود</label>
                <input type="password" name="p" class="native-input password-field" value="{curr_p}" placeholder="رمز ورود" required>
                <a href="?show_bio=true&bio_tab=fingerprint" target="_self" class="bio-html-btn"></a>
            </div>
            
            <button type="submit" class="native-submit-btn">ورود به TopSUNify</button>
            
            <div class="forgot-link">
                <a href="#">فعال‌سازی / فراموشی رمز</a>
            </div>
        </form>
    </div>

    <div class="topsun-powered-footer-container">
        {powered_layout_html}
    </div>
    """
    st.html(native_form_html)

    # --- تزریق عکس منظره محدود شده با افکت محوشدگی نرم به بالا ---
    if landscape_base64:
        st.markdown("""
        <div class="landscape-wrapper">
            <div class="bottom-landscape-bg"></div>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================
    # پاپ‌آ‌پ بومی بیومتریک
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
            
            <a href="?show_bio=false" target="_self" class="html-cancel-link" style="color: #64748b; text-decoration: none; font-size: 14px; font-weight: bold;">انصراف</a>
        </div>
        """
        st.html(popup_html_template)
