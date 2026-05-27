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

    /* فیلدهای ورودی */
    div[data-testid="stTextInput"] {{ max-width: 400px; margin: 0 auto !important; }}
    .stTextInput input {{
        border: none !important;
        border-bottom: 1px solid #e2e8f0 !important;
        border-radius: 0 !important;
        padding: 12px 8px !important;
    }}
    .stTextInput input:focus {{ border-bottom: 2px solid #ea580c !important; }}

    /* دکمه بیومتریک */
    .bio-container {{ position: relative; max-width: 400px; margin: 0 auto; }}
    .bio-inside-btn {{
        position: absolute;
        left: 45px;
        top: 36px;
        z-index: 99;
    }}
    .bio-inside-btn button {{ background: transparent; border: none; font-size: 24px; }}

    /* دکمه ورود اصلی */
    div.stButton > button.yellow-submit-btn {{
        width: 100% !important;
        max-width: 400px;
        margin: 40px auto 0 auto !important;
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
        background: rgba(0, 0, 0, 0.6) !important;
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
        padding: 24px;
        box-shadow: 0 20px 30px -10px rgba(0,0,0,0.4);
        z-index: 999999 !important;
        text-align: center;
    }}
    .segment-tab-container {{
        display: flex;
        background: #f1f5f9;
        padding: 4px;
        border-radius: 30px;
        margin: 15px 0 25px 0;
    }}
    .segment-btn {{
        flex: 1;
        padding: 10px 0;
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
        margin-top: 20px;
        display: block;
        text-decoration: none;
    }}
    </style>
    """
    st.markdown(auth_css, unsafe_allow_html=True)

    # ====================== هدر ======================
    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
    
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

    # ====================== ورودی‌ها ======================
    username = st.text_input("نام کاربری", placeholder="نام کاربری")
    
    st.markdown('<div class="bio-container">', unsafe_allow_html=True)
    password = st.text_input("رمز ورود", type="password", placeholder="رمز ورود")
    
    st.markdown('<div class="bio-inside-btn">', unsafe_allow_html=True)
    if st.button("🪪", key="bio_trigger"):
        st.session_state.show_bio_popup = True
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

    # دکمه ورود
    if st.button("ورود به TopSUNify", key="main_login", use_container_width=True):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("ورود موفقیت‌آمیز بود")
            time.sleep(0.6)
            st.rerun()
        else:
            st.error("اطلاعات وارد شده اشتباه است")

    st.markdown('<div class="forgot-link"><a href="#">فعال‌سازی / فراموشی رمز</a></div>', unsafe_allow_html=True)

    # ====================== پاپ‌آپ بیومتریک ======================
    if st.session_state.show_bio_popup:
        # دکمه‌های مخفی
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("set_finger", key="h_finger"):
                st.session_state.bio_tab = "fingerprint"
                st.rerun()
        with c2:
            if st.button("set_face", key="h_face"):
                st.session_state.bio_tab = "face"
                st.rerun()
        with c3:
            if st.button("close_bio", key="h_close"):
                st.session_state.show_bio_popup = False
                st.rerun()

        # مخفی کردن دکمه‌های مخفی
        st.markdown("""<style>
        div[data-testid="stColumn"] button {visibility: hidden; height:0; padding:0; margin:0;}
        </style>""", unsafe_allow_html=True)

        active_finger = "active" if st.session_state.bio_tab == "fingerprint" else ""
        active_face = "active" if st.session_state.bio_tab == "face" else ""

        content = """
            <h4 style="margin:0; font-weight:bold; font-size:18px;">ورود با اثر انگشت</h4>
            <p style="color:#64748b; margin:10px 0 25px 0;">حسگر را لمس کنید</p>
            <h1 style="font-size:72px; margin:20px 0; color:#ea580c;">☝️</h1>
        """ if st.session_state.bio_tab == "fingerprint" else """
            <h4 style="margin:0; font-weight:bold; font-size:18px;">ورود با تشخیص چهره</h4>
            <p style="color:#64748b; margin:10px 0 25px 0;">به دوربین نگاه کنید</p>
            <h1 style="font-size:72px; margin:20px 0; color:#facc15;">👤</h1>
        """

        popup_code = f"""
        <div class="custom-overlay-bg" onclick="triggerPythonAction('close_bio')"></div>
        <div class="custom-popup-card">
            <div style="font-size:14px; color:#94a3b8; margin-bottom:10px;">☀️ TopSUNify</div>
            
            <div class="segment-tab-container">
                <a href="#" class="segment-btn {active_face}" onclick="triggerPythonAction('set_face'); return false;">Face ID</a>
                <a href="#" class="segment-btn {active_finger}" onclick="triggerPythonAction('set_finger'); return false;">Fingerprint</a>
            </div>
            
            <div style="min-height:160px;">
                {content}
            </div>
            
            <a href="#" class="html-cancel-link" onclick="triggerPythonAction('close_bio'); return false;">انصراف</a>
        </div>

        <script>
        function triggerPythonAction(action) {{
            var btns = window.parent.document.getElementsByTagName('button');
            for (var i = 0; i < btns.length; i++) {{
                if (btns[i].innerText === action) {{
                    btns[i].click();
                    break;
                }}
            }}
        }}
        </script>
        """

        st.components.v1.html(popup_code, height=580, width=400, scrolling=False)

    # زرد کردن دکمه ورود
    st.markdown("""
    <script>
    var btns = window.parent.document.getElementsByTagName('button');
    for (var i = 0; i < btns.length; i++) {
        if (btns[i].innerText === "ورود به TopSUNify") {
            btns[i].classList.add("yellow-submit-btn");
        }
    }
    </script>
    """, unsafe_allow_html=True)
