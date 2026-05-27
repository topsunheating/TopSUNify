import streamlit as st
import time
import os
import base64

def render_auth_page():
    # مدیریت وضعیت تب انتخاب شده در بیومتریک و پاپ‌آپ
    if "bio_tab" not in st.session_state:
        st.session_state.bio_tab = "fingerprint"
        
    if "show_bio_popup" not in st.session_state:
        st.session_state.show_bio_popup = False
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # --- ۱. تزریق فونت ایران‌یکان و استایل‌های پایه صفحه ---
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

    /* هدر اصلی فرم ورود */
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

    /* ==========================================
       استایل‌های پیشرفته پاپ‌آپ بومی استریم‌لیت
       ========================================== */

    /* لایه بک‌دراپ تاریک */
    .popup-overlay {{
        position: fixed !important;
        top: 0 !important; left: 0 !important;
        width: 100vw !important; height: 100vh !important;
        background: rgba(0, 0, 0, 0.55) !important;
        z-index: 999990 !important;
    }}

    /* کادر سفید اصلی */
    .popup-card-container {{
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
        direction: rtl !important;
    }}

    /* هدر پاپ آپ شامل آیکون و نوشته کاملاً وسط‌چین */
    .popup-header-brand {{
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        font-size: 14px !important;
        color: #94a3b8 !important;
        margin-bottom: 20px !important;
        font-weight: bold !important;
        text-align: center !important;
        width: 100% !important;
    }}

    /* باکس سگمنت کنترلر استریم‌لیت */
    div.segment-tabs-box {{
        background: #f1f5f9 !important;
        padding: 4px !important;
        border-radius: 30px !important;
        margin-bottom: 25px !important;
        width: 100% !important;
    }}
    
    /* استایل دکمه‌های سگمنت پاپ‌آپ */
    div.segment-tabs-box div[data-testid="stHorizontalBlock"] {{
        gap: 4px !important;
    }}
    
    div.segment-tabs-box button {{
        width: 100% !important;
        background: transparent !important;
        border: none !important;
        color: #64748b !important;
        font-size: 14px !important;
        font-weight: bold !important;
        border-radius: 25px !important;
        padding: 8px 0 !important;
        box-shadow: none !important;
        transition: all 0.2s !important;
    }}

    /* دکمه انصراف قرمز پایین پاپ‌آپ */
    div.popup-cancel-box button {{
        width: 100% !important;
        background: transparent !important;
        border: none !important;
        color: #ef4444 !important;
        font-size: 16px !important;
        font-weight: bold !important;
        box-shadow: none !important;
        margin-top: 15px !important;
    }}
    div.popup-cancel-box button:hover {{
        background: #fef2f2 !important;
    }}
    </style>
    """
    st.markdown(auth_css, unsafe_allow_html=True)

    st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
   
    # --- هدر اصلی فرم ---
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

    # --- فیلدهای ورودی نام کاربری و پسورد ---
    username = st.text_input("نام کاربری", value="", placeholder="نام کاربری")
    
    st.markdown('<div class="bio-container">', unsafe_allow_html=True)
    password = st.text_input("رمز ورود", type="password", placeholder="رمز ورود")
   
    st.markdown('<div class="bio-inside-btn">', unsafe_allow_html=True)
    if st.button("🪪", key="trigger_bio_popup_btn", help="انتخاب روش ورود بیومتریک"):
        st.session_state.show_bio_popup = True
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

    # --- پاپ‌آپ کاملاً بومی و عملیاتی بیومتریک ---
    if st.session_state.show_bio_popup:
        # ایجاد لایه تاریک پس‌زمینه
        st.markdown('<div class="popup-overlay"></div>', unsafe_allow_html=True)
        
        # باز کردن کادر پاپ‌آپ
        st.markdown('<div class="popup-card-container">', unsafe_allow_html=True)
        
        # ۱. هدر پاپ‌آپ: آیکون تاپ‌سان + نوشته (کاملاً وسط‌چین)
        st.markdown(f"""
        <div class="popup-header-brand">
            {logo_html}
            <span style="font-size: 15px; color:#475569; font-weight:800; letter-spacing:-0.3px;">TopSUNify</span>
        </div>
        """, unsafe_allow_html=True)
        
        # ۲. سگمنت کنترلر بالای پاپ‌آپ با دکمه‌های واقعی و استایل‌دهی شده پایتون
        st.markdown('<div class="segment-tabs-box">', unsafe_allow_html=True)
        col_tab1, col_tab2 = st.columns(2)
        
        with col_tab1:
            active_face_style = "background: #2563eb !important; color: white !important;" if st.session_state.bio_tab == "face" else ""
            st.markdown(f'<style>div[data-testid="stColumn"]:nth-of-type(1) button {{ {active_face_style} }}</style>', unsafe_allow_html=True)
            if st.button("Face ID", key="tab_btn_face"):
                st.session_state.bio_tab = "face"
                st.rerun()
                
        with col_tab2:
            active_finger_style = "background: #2563eb !important; color: white !important;" if st.session_state.bio_tab == "fingerprint" else ""
            st.markdown(f'<style>div[data-testid="stColumn"]:nth-of-type(2) button {{ {active_finger_style} }}</style>', unsafe_allow_html=True)
            if st.button("Fingerprint", key="tab_btn_finger"):
                st.session_state.bio_tab = "fingerprint"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # ۳. محتوای میانی پاپ‌آپ (کاملاً وسط‌چین شده)
        if st.session_state.bio_tab == "fingerprint":
            st.markdown("""
                <div style="text-align: center; width: 100%; min-height: 70px;">
                    <h4 style="color: #1e293b; text-align: center; margin:0; font-weight:bold; font-size:18px; width:100%;">ورود با اثر انگشت</h4>
                    <p style="text-align: center; color: #64748b; font-size: 13px; margin: 8px 0 0 0; width:100%;">حسگر را لمس کنید</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="text-align: center; width: 100%; min-height: 70px;">
                    <h4 style="color: #1e293b; text-align: center; margin:0; font-weight:bold; font-size:18px; width:100%;">ورود با تشخیص چهره</h4>
                    <p style="text-align: center; color: #64748b; font-size: 13px; margin: 8px 0 0 0; width:100%;">به دوربین جلو نگاه کنید</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)

        # ۴. دکمه انصراف واقعی پایتون با استایل متنی قرمز
        st.markdown('<div class="popup-cancel-box">', unsafe_allow_html=True)
        if st.button("انصراف", key="popup_cancel_action_btn"):
            st.session_state.show_bio_popup = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # بستن کادر پاپ‌آپ
        st.markdown('</div>', unsafe_allow_html=True)

    # اسکریپت زرد کردن دکمه ورود اصلی فرم لودر
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
