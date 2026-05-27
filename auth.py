import streamlit as st
import time
import os
import base64

def render_auth_page():
    # مدیریت وضعیت تب انتخاب شده در بیومتریک و پاپ‌آ‌پ
    if "bio_tab" not in st.session_state:
        st.session_state.bio_tab = "fingerprint"
        
    if "show_bio_popup" not in st.session_state:
        st.session_state.show_bio_popup = False
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # --- ۱. تزریق فونت ایران‌یکان و استایل‌های اصلی صفحه ---
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

    /* هدر فرم ورود اصلی */
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
       استایل‌های پاپ‌آپ (کاملاً هماهنگ با عکس نمونه موبایل)
       ========================================== */

    /* لایه تاریک کل صفحه */
    .popup-overlay {{
        position: fixed !important;
        top: 0 !important; left: 0 !important;
        width: 100vw !important; height: 100vh !important;
        background: rgba(0, 0, 0, 0.6) !important;
        z-index: 999990 !important;
    }}

    /* کادر سفید اصلی پاپ‌آپ */
    .popup-card-container {{
        position: fixed !important;
        top: 50% !important; left: 50% !important;
        transform: translate(-50%, -50%) !important;
        background: white !important;
        width: 88% !important;
        max-width: 340px !important;
        border-radius: 28px !important;
        padding: 24px !important;
        box-shadow: 0 20px 30px rgba(0,0,0,0.3) !important;
        z-index: 999995 !important;
        direction: rtl !important;
        text-align: center !important;
    }}

    /* باکس نگهدارنده سگمنت تب بومی */
    div.segment-tabs-box {{
        background: #f1f5f9 !important;
        padding: 4px !important;
        border-radius: 30px !important;
        margin-bottom: 20px !important;
        width: 100% !important;
        z-index: 999999 !important;
        position: relative !important;
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
    }}

    /* باکس دکمه انصراف در پاپ‌آپ */
    div.popup-cancel-box {{
        margin-top: 15px !important;
        width: 100% !important;
        text-align: center !important;
        z-index: 999999 !important;
        position: relative !important;
    }}
    div.popup-cancel-box button {{
        width: 100% !important;
        background: transparent !important;
        border: none !important;
        color: #64748b !important; /* رنگ خاکستری شبیه عکس موبایل */
        font-size: 16px !important;
        font-weight: bold !important;
        box-shadow: none !important;
    }}
    div.popup-cancel-box button:hover {{
        color: #ef4444 !important;
        background: #f1f5f9 !important;
    }}
    </style>
    """
    st.markdown(auth_css, unsafe_allow_html=True)

    st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
   
    # --- هدر اصلی فرم ورود ---
    logo_html = "☀️"
    if os.path.exists("./static/logo.png"):
        with open("./static/logo.png", "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" width="52" style="display: block; margin: 0 auto;">'

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

    st.markdown('<div class="forgot-link"><a href="#">فعال‌سازی / فراموشی رمز</a></div>', unsafe_allow_html=True)

    # ==========================================
    # پاپ‌آپ کاملاً بومی، فیکس شده و هماهنگ با ساختار عکس موبایل
    # ==========================================
    if st.session_state.show_bio_popup:
        # ۱. لایه تاریک پشت پاپ‌آپ
        st.markdown('<div class="popup-overlay"></div>', unsafe_allow_html=True)
        
        # ۲. شروع بدنه کادر پاپ‌آپ سفید رنگ
        st.markdown('<div class="popup-card-container">', unsafe_allow_html=True)
        
        # ۳. بخش دکمه‌های تعویض تب (سگمنت بالای پاپ‌آپ)
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
        st.markdown('</div>', unsafe_allow_html=True) # بستن تب باکس

        # ۴. بخش لوگو و نوشته‌های میانی پاپ‌آپ (دقیقاً مشابه عکس نمونه موبایل شما)
        if st.session_state.bio_tab == "fingerprint":
            st.markdown(f"""
                <div style="text-align: center; width: 100%; display: block; margin: 0 auto;">
                    <div style="display: flex; justify-content: center; align-items: center; gap: 8px; margin-bottom: 15px;">
                        {logo_html}
                        <span style="font-size: 15px; color:#475569; font-weight:800; letter-spacing:-0.3px;">TopSUNify</span>
                    </div>
                    <h4 style="color: #1e293b; text-align: center !important; margin: 0 auto; font-weight: bold; font-size: 18px; width: 100%; display: block;">ورود با اثر انگشت</h4>
                    <p style="text-align: center !important; color: #64748b; font-size: 14px; margin: 8px auto 0 auto; width: 100%; display: block;">حسگر را لمس کنید</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="text-align: center; width: 100%; display: block; margin: 0 auto;">
                    <div style="display: flex; justify-content: center; align-items: center; gap: 8px; margin-bottom: 15px;">
                        {logo_html}
                        <span style="font-size: 15px; color:#475569; font-weight:800; letter-spacing:-0.3px;">TopSUNify</span>
                    </div>
                    <h4 style="color: #1e293b; text-align: center !important; margin: 0 auto; font-weight: bold; font-size: 18px; width: 100%; display: block;">ورود با تشخیص چهره</h4>
                    <p style="text-align: center !important; color: #64748b; font-size: 14px; margin: 8px auto 0 auto; width: 100%; display: block;">به دوربین جلو نگاه کنید</p>
                </div>
            """, unsafe_allow_html=True)

        # ۵. باکس انصراف با دکمه بومی استریم‌لیت
        st.markdown('<div class="popup-cancel-box">', unsafe_allow_html=True)
        if st.button("انصراف", key="popup_cancel_action_btn"):
            st.session_state.show_bio_popup = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True) # بستن باکس انصراف
        
        # ۶. پایان قطعی و بستن کادر پاپ‌آپ سفید رنگ
        st.markdown('</div>', unsafe_allow_html=True)

    # اسکریپت اعمال استایل دکمه اصلی ورود
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
