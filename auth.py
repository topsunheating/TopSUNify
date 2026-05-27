import streamlit as st
import time
import os
import base64

def render_auth_page():
    # دریافت و مدیریت تب انتخاب شده در بیومتریک از طریق URL بدون تداخل با دکمه‌های استریم‌لیت
    query_params = st.query_params
    if "bio_tab" not in st.session_state:
        st.session_state.bio_tab = query_params.get("bio_tab", "fingerprint")

    # --- ۱. تزریق فونت ایران‌یکان و استایل‌های فیکس شده لایه‌های پاپ‌آپ نیتتیو ---
    font_path = "iranyekan.ttf"
    font_base64 = ""

    if os.path.exists(font_path):
        with open(font_path, "rb") as f:
            font_base64 = base64.b64encode(f.read()).decode()

    auth_css = f"""
    <style>
    @font-face {{
        font-family: 'iranyekan';
        src: url(data:font/ttf;base64,{font_base64}) format('truetype');
    }}

    * {{
        font-family: 'iranyekan', Tahoma, sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }}
    
    body, [data-testid="stAppViewContainer"] {{
        background-color: #ffffff !important;
    }}
    
    [data-testid="stHeader"] {{
        display: none !important;
    }}

    /* هدر: چسبیدن کامل لوگو و نوشته */
    .brand-flex-container {{
        display: flex !important;
        flex-direction: row-reverse !important; 
        align-items: center !important;
        justify-content: center !important;
        gap: 2px !important; 
        width: 100% !important;
        max-width: 400px !important;
        margin: 0 auto 30px auto !important;
    }}
    
    .brand-title-text {{
        font-size: 26px !important;
        font-weight: 900 !important;
        color: #000000 !important;
        margin: 0 !important;
        padding-right: 2px !important; 
        line-height: 1 !important;
        letter-spacing: -0.5px !important; 
    }}

    /* فیلدهای ورودی تک‌خطی */
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
    }}
    .stTextInput input:focus {{
        border-bottom: 2px solid #ea580c !important;
        box-shadow: none !important;
    }}

    /* آیکون بیومتریک انتهای فیلد رمز عبور */
    .bio-container {{
        position: relative;
        max-width: 400px;
        margin: 0 auto;
    }}
    
    div.bio-inside-btn {{
        position: absolute;
        left: 45px; 
        top: 36px;
        z-index: 99;
    }}
    
    div.bio-inside-btn button {{
        background: transparent !important;
        border: none !important;
        font-size: 22px !important;
        padding: 0 !important;
        box-shadow: none !important;
        cursor: pointer;
    }}

    /* دکمه اصلی ورود زرد رنگ */
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
        transition: all 0.3s ease;
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

    /* 📌 پیاده‌سازی پاپ‌آپی که دکمه‌ها درون آن قفل و فیکس هستند */
    .custom-overlay-bg {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.5) !important;
        z-index: 999990 !important;
    }}

    .custom-popup-card {{
        position: fixed;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        background: white !important;
        width: 88%;
        max-width: 350px;
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.3);
        z-index: 999999 !important;
        text-align: center;
        direction: rtl !important;
    }}

    /* استایل سگمنت کنترلر بالای پاپ آپ (کاملاً شبیه عکس موبایلت) */
    .segment-tab-container {{
        display: flex;
        background: #f1f5f9;
        padding: 4px;
        border-radius: 30px;
        margin: 10px 0 20px 0;
        direction: ltr !important;
    }}
    
    .segment-btn {{
        flex: 1;
        text-align: center;
        padding: 8px 0;
        font-size: 14px;
        font-weight: bold;
        color: #64748b;
        text-decoration: none !important;
        border-radius: 25px;
        transition: all 0.2s;
    }}
    
    .segment-btn.active {{
        background: #2563eb !important; /* رنگ آبی انتخابی تب فعال مشابه موبایلت */
        color: white !important;
    }}

    /* دکمه انصراف متنی قرمز کاملاً فیکس شده در داخل کادر */
    .html-cancel-link {{
        display: block;
        margin-top: 20px;
        color: #ef4444 !important;
        font-size: 16px;
        font-weight: bold;
        text-decoration: none !important;
        text-align: center;
        width: 100%;
    }}
    </style>
    """
    st.markdown(auth_css, unsafe_allow_html=True)

    # مدیریت استیت باز/بسته بودن پاپ آپ بیومتریک
    if "show_bio_popup" not in st.session_state: st.session_state.show_bio_popup = False

    st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
    
    # --- ۲. هدر: لوگو و متن انگلیسی کاملاً جفت ---
    logo_html = "☀️"
    if os.path.exists("./static/logo.png"):
        with open("./static/logo.png", "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" width="52" style="display: block; margin: 0; padding: 0;">'

    st.markdown(f"""
    <div class="brand-flex-container">
        {logo_html}
        <h2 class="brand-title-text">TopSUNify</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

    # --- ۳. فیلد نام کاربری ---
    username = st.text_input("نام کاربری", value="", placeholder="نام کاربری")

    # --- ۴. فیلد رمز عبور + دکمه بیومتریک ---
    st.markdown('<div class="bio-container">', unsafe_allow_html=True)
    password = st.text_input("رمز ورود", type="password", placeholder="رمز ورود")
    
    st.markdown('<div class="bio-inside-btn">', unsafe_allow_html=True)
    if st.button("🪪", key="trigger_bio_popup_btn", help="انتخاب روش ورود بیومتریک"):
        st.session_state.show_bio_popup = True
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

    # --- ۵. دکمه اصلی ورود (زرد رنگ) ---
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

    # --- ۶. لینک فعال‌سازی / فراموشی رمز ---
    st.markdown('<div class="forgot-link"><a href="#">فعال‌سازی / فراموشی رمز</a></div>', unsafe_allow_html=True)

    # --- ۷. کنترل کلیک‌ها و اکشن‌های پاپ‌آپ از طریق المان مخفی کمکی استریم‌لیت ---
    # این دکمه مخفی دستورات صادر شده از دکمه‌های HTML داخل پاپ آپ را در پایتون پردازش می‌کند
    st.markdown('<div style="display:none;">', unsafe_allow_html=True)
    action_trigger = st.text_input("popup_action_bridge", value="", key="popup_action_bridge")
    st.markdown('</div>', unsafe_allow_html=True)

    # پردازش اکشن کلیک‌های پاپ آپ
    if action_trigger == "switch_to_fingerprint":
        st.session_state.bio_tab = "fingerprint"
        st.query_params["bio_tab"] = "fingerprint"
        st.set_query_params = st.query_params
        st.markdown("<script>window.parent.document.querySelector('input[aria-label=\"popup_action_bridge\"]').value = '';</script>", unsafe_allow_html=True)
        st.rerun()
    elif action_trigger == "switch_to_face":
        st.session_state.bio_tab = "face"
        st.query_params["bio_tab"] = "face"
        st.set_query_params = st.query_params
        st.markdown("<script>window.parent.document.querySelector('input[aria-label=\"popup_action_bridge\"]').value = '';</script>", unsafe_allow_html=True)
        st.rerun()
    elif action_trigger == "close_popup":
        st.session_state.show_bio_popup = False
        st.markdown("<script>window.parent.document.querySelector('input[aria-label=\"popup_action_bridge\"]').value = '';</script>", unsafe_allow_html=True)
        st.rerun()

    # --- ۸. رندر پاپ‌آپ ۱۰۰٪ فیکس و تضمین شده با دکمه‌های داخلی HTML ---
    if st.session_state.show_bio_popup:
        # لایه تاریک پس‌زمینه با قابلیت کلیک برای خروج
        st.markdown('<div class="custom-overlay-bg" onclick="sendPopupAction(\'close_popup\')"></div>', unsafe_allow_html=True)
        
        # کارت سفید اصلی پاپ آپ
        active_f = "active" if st.session_state.bio_tab == "fingerprint" else ""
        active_face = "active" if st.session_state.bio_tab == "face" else ""
        
        # تعیین محتوای متنی و گرافیکی داخلی بر اساس تب فعال
        if st.session_state.bio_tab == "fingerprint":
            inner_content = """
                <h4 style="color: #1e293b; text-align: center; margin:0; font-weight:bold; font-size:18px;">ورود با اثر انگشت</h4>
                <p style="text-align: center; color: #64748b; font-size: 13px; margin: 8px 0 20px 0;">حسگر را لمس کنید</p>
                <h1 style="text-align: center; font-size: 65px; margin: 20px 0; color: #ea580c;">☝️</h1>
            """
        else:
            inner_content = """
                <h4 style="color: #1e293b; text-align: center; margin:0; font-weight:bold; font-size:18px;">ورود با تشخیص چهره</h4>
                <p style="text-align: center; color: #64748b; font-size: 13px; margin: 8px 0 20px 0;">به دوربین جلو نگاه کنید</p>
                <h1 style="text-align: center; font-size: 65px; margin: 20px 0; color: #facc15;">👤</h1>
            """

        st.markdown(f"""
        <div class="custom-popup-card">
            <div style="font-size:13px; color:#94a3b8; margin-bottom:12px; text-align:center; font-weight:bold;">☀️ TopSUNify</div>
            
            <div class="segment-tab-container">
                <a href="#" class="segment-btn {active_face}" onclick="sendPopupAction('switch_to_face'); return false;">Face ID</a>
                <a href="#" class="segment-btn {active_f}" onclick="sendPopupAction('switch_to_fingerprint'); return false;">Fingerprint</a>
            </div>
            
            <div style="min-height: 140px;">
                {inner_content}
            </div>
            
            <a href="#" class="html-cancel-link" onclick="sendPopupAction('close_popup'); return false;">انصراف</a>
        </div>
        
        <script>
        function sendPopupAction(actionName) {{
            var inputs = window.parent.document.getElementsByTagName('input');
            for (var i = 0; i < inputs.length; i++) {{
                if (inputs[i].placeholder === "popup_action_bridge" || inputs[i].ariaLabel === "popup_action_bridge") {{
                    inputs[i].value = actionName;
                    inputs[i].dispatchEvent(new Event('input', {{ bubbles: true }}));
                    inputs[i].dispatchEvent(new Event('change', {{ bubbles: true }}));
                    break;
                }}
            }}
        }}
        </script>
        """, unsafe_allow_html=True)

    # اسکریپت اعمال زرد تاپسان روی دکمه ورود اصلی
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
