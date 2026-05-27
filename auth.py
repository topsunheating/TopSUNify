import streamlit as st
import time
import os
import base64

def render_auth_page():
    # مدیریت وضعیت تب انتخاب شده در بیومتریک از طریق Session State
    if "bio_tab" not in st.session_state:
        st.session_state.bio_tab = "fingerprint"

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

    /* دکمه اصلی ورود زرد رنگ تاپسان */
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

    /* پیاده‌سازی پس‌زمینه تاریک پاپ‌آپ */
    .custom-overlay-bg {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.55) !important;
        z-index: 999990 !important;
    }}

    /* کادر سفید اصلی پاپ آپ بیومتریک */
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
    }}

    /* استایل سگمنت کنترلر بالای پاپ آپ (مشابه عکس موبایلت) */
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
        background: #2563eb !important; /* رنگ آبی دکمه فعال مشابه موبایلت */
        color: white !important;
    }}

    /* لینک انصراف متنی قرمز در داخل کادر */
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

    # --- ۷. ردیف کنترل اکشن‌های پاپ‌آپ از طریق المان‌های بومی استریم‌لیت ---
    if st.session_state.show_bio_popup:
        # ایجاد دکمه‌های پنهان استریم‌لیت برای هندل کردن وضعیت دکمه‌های HTML
        col_h1, col_h2, col_h3 = st.columns(3)
        
        with col_h1:
            if st.button("set_finger", key="btn_h_finger", help="hidden"):
                st.session_state.bio_tab = "fingerprint"
                st.rerun()
        with col_h2:
            if st.button("set_face", key="btn_h_face", help="hidden"):
                st.session_state.bio_tab = "face"
                st.rerun()
        with col_h3:
            if st.button("close_bio", key="btn_h_close", help="hidden"):
                st.session_state.show_bio_popup = False
                st.rerun()

        # مخفی کردن دکمه‌های راهبردی بالا از دید کاربر با CSS
        st.markdown("""
            <style>
            div[data-testid="stColumn"] button {
                position: absolute !important;
                width: 0px !important; height: 0px !important;
                padding: 0 !important; border: none !important;
                opacity: 0 !important; visibility: hidden !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # تفکیک وضعیت تب‌های فعال و غیرفعال پاپ آپ
        active_face = "active" if st.session_state.bio_tab == "face" else ""
        active_finger = "active" if st.session_state.bio_tab == "fingerprint" else ""
        
        if st.session_state.bio_tab == "fingerprint":
            inner_html_content = """
                <h4 style="color: #1e293b; text-align: center; margin:0; font-weight:bold; font-size:18px;">ورود با اثر انگشت</h4>
                <p style="text-align: center; color: #64748b; font-size: 13px; margin: 8px 0 20px 0;">حسگر را لمس کنید</p>
                <h1 style="text-align: center; font-size: 65px; margin: 20px 0; color: #ea580c;">☝️</h1>
            """
        else:
            inner_html_content = """
                <h4 style="color: #1e293b; text-align: center; margin:0; font-weight:bold; font-size:18px;">ورود با تشخیص چهره</h4>
                <p style="text-align: center; color: #64748b; font-size: 13px; margin: 8px 0 20px 0;">به دوربین جلو نگاه کنید</p>
                <h1 style="text-align: center; font-size: 65px; margin: 20px 0; color: #facc15;">👤</h1>
            """

        # --- ۸. تزریق پاپ‌آپ نهایی کامپایل شده بدون خطای فرمت رشته ---
        st.markdown(f"""
        <div class="custom-overlay-bg" onclick="triggerPythonAction('close_bio')"></div>
        <div class="custom-popup-card">
            <div style="font-size:13px; color:#94a3b8; margin-bottom:12px; text-align:center; font-weight:bold;">☀️ TopSUNify</div>
            
            <div class="segment-tab-container">
                <a href="#" class="segment-btn {active_face}" onclick="triggerPythonAction('set_face'); return false;">Face ID</a>
                <a href="#" class="segment-btn {active_finger}" onclick="triggerPythonAction('set_finger'); return false;">Fingerprint</a>
            </div>
            
            <div style="min-height: 140px; direction: rtl !important;">
                {inner_html_content}
            </div>
            
            <a href="#" class="html-cancel-link" onclick="triggerPythonAction('close_bio'); return false;">انصراف</a>
        </div>

        <script>
        function triggerPythonAction(actionText) {{
            var buttons = window.parent.document.getElementsByTagName('button');
            for (var i = 0; i < buttons.length; i++) {{
                if (buttons[i].innerText === actionText) {{
                    buttons[i].click();
                    break;
                }}
            }}
        }}
        </script>
        """, unsafe_allow_html=True)

    # اسکریپت زرد کردن دکمه ورود اصلی
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
