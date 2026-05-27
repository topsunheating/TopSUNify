import streamlit as st
import time
import os
import base64

def render_auth_page():
    # وضعیت‌های اولیه
    if "bio_tab" not in st.session_state:
        st.session_state.bio_tab = "fingerprint"
    if "show_bio_popup" not in st.session_state:
        st.session_state.show_bio_popup = False
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # ====================== CSS ======================
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
    [data-testid="stHeader"] {{ display: none !important; }}
    body, [data-testid="stAppViewContainer"] {{ background-color: #ffffff !important; }}

    .brand-flex-container {{
        display: flex !important;
        flex-direction: row-reverse !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
        max-width: 400px !important;
        margin: 0 auto 30px auto !important;
    }}
    .brand-title-text {{
        font-size: 28px !important;
        font-weight: 900 !important;
        color: #000000 !important;
    }}

    div[data-testid="stTextInput"] {{ max-width: 400px; margin: 0 auto !important; }}
    .stTextInput input {{
        border: none !important;
        border-bottom: 1px solid #e2e8f0 !important;
        padding: 12px 8px !important;
    }}
    .stTextInput input:focus {{ border-bottom: 2px solid #ea580c !important; }}

    /* دکمه بیومتریک */
    .bio-btn {{
        position: absolute;
        left: 50px;
        top: 12px;
        font-size: 26px;
        background: none;
        border: none;
        cursor: pointer;
        z-index: 100;
    }}

    /* دکمه ورود اصلی */
    div.stButton > button.yellow-submit-btn {{
        width: 100% !important;
        max-width: 400px;
        margin: 35px auto 0 auto !important;
        background-color: #facc15 !important;
        color: #1e293b !important;
        border-radius: 12px !important;
        padding: 14px !important;
        font-weight: bold !important;
    }}
    div.stButton > button.yellow-submit-btn:hover {{
        background-color: #ea580c !important;
        color: white !important;
    }}

    /* پاپ‌آپ */
    .custom-overlay-bg {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.65) !important;
        z-index: 999990 !important;
    }}
    .custom-popup-card {{
        position: fixed;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        width: 90%;
        max-width: 360px;
        border-radius: 24px;
        padding: 25px;
        box-shadow: 0 25px 35px -10px rgba(0,0,0,0.45);
        z-index: 999999 !important;
        text-align: center;
    }}
    .segment-tab-container {{
        display: flex;
        background: #f1f5f9;
        padding: 5px;
        border-radius: 30px;
        margin: 15px 0 25px 0;
    }}
    .segment-btn {{
        flex: 1;
        padding: 11px 0;
        font-size: 15px;
        font-weight: bold;
        color: #64748b;
        border-radius: 25px;
        text-decoration: none;
    }}
    .segment-btn.active {{
        background: #2563eb;
        color: white;
    }}
    .html-cancel-link {{
        color: #ef4444;
        font-weight: bold;
        margin-top: 25px;
        display: block;
        text-decoration: none;
        font-size: 16px;
    }}
    </style>
    """
    st.markdown(auth_css, unsafe_allow_html=True)

    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

    # هدر
    logo_html = "☀️"
    if os.path.exists("./static/logo.png"):
        with open("./static/logo.png", "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" width="55">'

    st.markdown(f"""
    <div class="brand-flex-container">
        {logo_html}
        <h2 class="brand-title-text">TopSUNify</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height: 25px;"></div>', unsafe_allow_html=True)

    # فیلدهای ورودی
    username = st.text_input("نام کاربری", placeholder="نام کاربری", key="username_input")
    
    # فیلد رمز + دکمه بیومتریک
    col_pw = st.columns([1, 0.12])
    with col_pw[0]:
        password = st.text_input("رمز ورود", type="password", placeholder="رمز ورود", key="password_input")
    
    with col_pw[1]:
        if st.button("🪪", key="bio_trigger_btn"):
            st.session_state.show_bio_popup = True
            st.rerun()

    # دکمه ورود اصلی
    if st.button("ورود به TopSUNify", key="main_login_btn", use_container_width=True):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("ورود موفقیت‌آمیز بود")
            time.sleep(0.6)
            st.rerun()
        else:
            st.error("نام کاربری یا رمز عبور اشتباه است")

    st.markdown('<div class="forgot-link"><a href="#">فعال‌سازی / فراموشی رمز</a></div>', unsafe_allow_html=True)

    # ====================== پاپ‌آپ بیومتریک ======================
    if st.session_state.get("show_bio_popup", False):
        
        # دکمه‌های مخفی برای کنترل
        c1, c2, c3 = st.columns([1,1,1])
        with c1:
            if st.button("set_finger", key="hidden_finger"):
                st.session_state.bio_tab = "fingerprint"
                st.rerun()
        with c2:
            if st.button("set_face", key="hidden_face"):
                st.session_state.bio_tab = "face"
                st.rerun()
        with c3:
            if st.button("close_bio", key="hidden_close"):
                st.session_state.show_bio_popup = False
                st.rerun()

        # مخفی کردن دکمه‌های مخفی
        st.markdown("""
        <style>
        div[data-testid="stColumn"] button {visibility: hidden; height:0px !important; margin:0; padding:0;}
        </style>
        """, unsafe_allow_html=True)

        active_face = "active" if st.session_state.bio_tab == "face" else ""
        active_finger = "active" if st.session_state.bio_tab == "fingerprint" else ""

        if st.session_state.bio_tab == "fingerprint":
            content = """
                <h4 style="margin:5px 0 8px 0; font-size:18px;">ورود با اثر انگشت</h4>
                <p style="color:#64748b; margin-bottom:25px;">حسگر را لمس کنید</p>
                <h1 style="font-size:78px; color:#ea580c;">☝️</h1>
            """
        else:
            content = """
                <h4 style="margin:5px 0 8px 0; font-size:18px;">ورود با تشخیص چهره</h4>
                <p style="color:#64748b; margin-bottom:25px;">به دوربین جلو نگاه کنید</p>
                <h1 style="font-size:70px; color:#facc15;">👤</h1>
            """

        popup_code = f"""
        <div class="custom-overlay-bg" onclick="triggerPythonAction('close_bio')"></div>
        <div class="custom-popup-card">
            <div style="font-size:14px; color:#94a3b8; margin-bottom:12px;">☀️ TopSUNify</div>
            
            <div class="segment-tab-container">
                <a href="#" class="segment-btn {active_face}" onclick="triggerPythonAction('set_face'); return false;">Face ID</a>
                <a href="#" class="segment-btn {active_finger}" onclick="triggerPythonAction('set_finger'); return false;">Fingerprint</a>
            </div>
            
            <div style="min-height: 170px;">
                {content}
            </div>
            
            <a href="#" class="html-cancel-link" onclick="triggerPythonAction('close_bio'); return false;">انصراف</a>
        </div>

        <script>
        function triggerPythonAction(action) {{
            var buttons = window.parent.document.querySelectorAll('button');
            for (var i = 0; i < buttons.length; i++) {{
                if (buttons[i].innerText === action) {{
                    buttons[i].click();
                    break;
                }}
            }}
        }}
        </script>
        """

        st.components.v1.html(popup_code, height=600, width=400, scrolling=False)

    # زرد کردن دکمه ورود
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
