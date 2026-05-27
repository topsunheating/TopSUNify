import streamlit as st
import time
import os
import base64

def render_auth_page():
    # مدیریت وضعیت تب انتخاب شده در بیومتریک
    if "bio_tab" not in st.session_state:
        st.session_state.bio_tab = "fingerprint"
        
    if "show_bio_popup" not in st.session_state:
        st.session_state.show_bio_popup = False
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # --- ۱. تزریق فونت ایران‌یکان و استایل‌ها ---
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

    /* لایه تاریک پس‌زمینه پاپ‌آپ روی کل صفحه */
    .custom-overlay-bg {{
        position: fixed !important;
        top: 0 !important; left: 0 !important; 
        width: 100vw !important; height: 100vh !important;
        background: rgba(0, 0, 0, 0.55) !important;
        z-index: 999990 !important;
    }}
   
    /* کادر سفید پاپ‌آپ */
    .custom-popup-card {{
        position: fixed !important;
        top: 50% !important; left: 50% !important;
        transform: translate(-50%, -50%) !important;
        background: white !important;
        width: 88% !important;
        max-width: 350px !important;
        border-radius: 24px !important;
        padding: 24px !important;
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.3) !important;
        z-index: 999999 !important;
        text-align: center !important;
    }}

    .segment-tab-container {{
        display: flex !important;
        background: #f1f5f9 !important;
        padding: 4px !important;
        border-radius: 30px !important;
        margin: 10px 0 20px 0 !important;
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
        margin-top: 20px !important;
        color: #ef4444 !important;
        font-size: 16px !important;
        font-weight: bold !important;
        text-decoration: none !important;
        text-align: center !important;
        width: 100% !important;
    }}
    </style>
    """
    st.markdown(auth_css, unsafe_allow_html=True)

    st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
   
    # --- هدر ---
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

    # --- فیلدهای ورودی ---
    username = st.text_input("نام کاربری", value="", placeholder="نام کاربری")
    
    st.markdown('<div class="bio-container">', unsafe_allow_html=True)
    password = st.text_input("رمز ورود", type="password", placeholder="رمز ورود")
   
    st.markdown('<div class="bio-inside-btn">', unsafe_allow_html=True)
    if st.button("🪪", key="trigger_bio_popup_btn", help="انتخاب روش ورود بیومتریک"):
        st.session_state.show_bio_popup = True
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

    # --- دکمه ورود ---
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

    # --- لینک فراموشی ---
    st.markdown('<div class="forgot-link"><a href="#">فعال‌سازی / فراموشی رمز</a></div>', unsafe_allow_html=True)

    # --- پاپ‌آپ بیومتریک بومی ---
    if st.session_state.show_bio_popup:
        
        col_h1, col_h2, col_h3 = st.columns(3)
        with col_h1:
            if st.button("set_finger", key="btn_h_finger"):
                st.session_state.bio_tab = "fingerprint"
                st.rerun()
        with col_h2:
            if st.button("set_face", key="btn_h_face"):
                st.session_state.bio_tab = "face"
                st.rerun()
        with col_h3:
            if st.button("close_bio", key="btn_h_close"):
                st.session_state.show_bio_popup = False
                st.rerun()

        st.markdown("""
            <style>
            div[data-testid="stColumn"] button {
                position: absolute !important;
                width: 0px !important; 
                height: 0px !important;
                padding: 0 !important; 
                border: none !important;
                opacity: 0 !important; 
                visibility: hidden !important;
            }
            </style>
        """, unsafe_allow_html=True)

        active_face = "active" if st.session_state.bio_tab == "face" else ""
        active_finger = "active" if st.session_state.bio_tab == "fingerprint" else ""

        if st.session_state.bio_tab == "fingerprint":
            graphic_content = """
                <h4 style="color: #1e293b; text-align: center; margin:0; font-weight:bold; font-size:18px;">ورود با اثر انگشت</h4>
                <p style="text-align: center; color: #64748b; font-size: 13px; margin: 8px 0 20px 0;">حسگر را لمس کنید</p>
                <div style="height: 30px;"></div>
            """
        else:
            graphic_content = """
                <h4 style="color: #1e293b; text-align: center; margin:0; font-weight:bold; font-size:18px;">ورود با تشخیص چهره</h4>
                <p style="text-align: center; color: #64748b; font-size: 13px; margin: 8px 0 20px 0;">به دوربین جلو نگاه کنید</p>
                <div style="height: 30px;"></div>
            """

        popup_html_template = """
        <div class="custom-overlay-bg" onclick="triggerPythonAction('close_bio')"></div>
        <div class="custom-popup-card">
            <div style="font-size:13px; color:#94a3b8; margin-bottom:12px; text-align:center; font-weight:bold;">☀️ TopSUNify</div>
            
            <div class="segment-tab-container">
                <a href="#" class="segment-btn {ACTIVE_FACE}" onclick="triggerPythonAction('set_face'); return false;">Face ID</a>
                <a href="#" class="segment-btn {ACTIVE_FINGER}" onclick="triggerPythonAction('set_finger'); return false;">Fingerprint</a>
            </div>
            
            <div style="min-height: 100px; direction: rtl !important;">
                {GRAPHIC_CONTENT}
            </div>
            
            <a href="#" class="html-cancel-link" onclick="triggerPythonAction('close_bio'); return false;">انصراف</a>
        </div>

        <script>
        function triggerPythonAction(actionText) {
            var buttons = window.parent.document.getElementsByTagName('button');
            for (var i = 0; i < buttons.length; i++) {
                if (buttons[i].innerText === actionText) {
                    buttons[i].click();
                    break;
                }
            }
        }
        </script>
        """

        # جایگذاری رشته‌ها به صورت خام بدون دخالت دادن f-string
        popup_rendered = popup_html_template.replace("{ACTIVE_FACE}", active_face)\
                                            .replace("{ACTIVE_FINGER}", active_finger)\
                                            .replace("{GRAPHIC_CONTENT}", graphic_content)

        # 📌 استفاده از تابع ایمن و بومی st.html برای رندر کردن ۱۰۰٪ گرافیکی و بدون نقص متن
        st.html(popup_rendered)

    # اسکریپت اعمال کلاس زرد
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
