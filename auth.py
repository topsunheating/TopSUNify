import streamlit as st
import time
import os
import base64

def render_auth_page():
    # --- ۱. لود فونت ایران‌یکان از پوشه محلی و تزریق استایل‌های مدرن تک‌خطی ---
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

    /* 📌 کانتینر هوشمند برای چسبیدن کامل لوگو و نوشته به یکدیگر */
    .brand-flex-container {{
        display: flex !important;
        flex-direction: row-reverse !important; /* لوگو سمت راست، متن سمت چپ */
        align-items: center !important;
        justify-content: center !important;
        gap: 2px !important; /* فاصله‌ی فوق‌العاده کم و مماس */
        width: 100% !important;
        max-width: 400px !important;
        margin: 0 auto 30px auto !important;
    }}
    
    .brand-title-text {{
        font-size: 26px !important;
        font-weight: 900 !important;
        color: #000000 !important;
        margin: 0 !important;
        padding-right: 2px !important; /* حذف هرگونه فاصله کاذب راست */
        line-height: 1 !important;
        font-family: 'iranyekan', sans-serif !important;
        letter-spacing: -0.5px !important; /* نزدیک‌تر کردن حروف انگلیسی به هم */
    }}

    /* کانتینر فیلدهای ورودی تک‌خطی */
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
        transition: border-color 0.2s ease;
    }}
    .stTextInput input:focus {{
        border-bottom: 2px solid #ea580c !important;
        box-shadow: none !important;
    }}

    /* مدیریت موقعیت آیکون بیومتریک در انتهای فیلد رمز عبور */
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

    /* استایل دکمه ورود (نارنجی با هاور زرد گرم تاپسان) */
    div.stButton > button.orange-submit-btn {{
        width: 100% !important;
        max-width: 400px;
        display: block;
        margin: 40px auto 0 auto !important;
        background-color: #ea580c !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 0 !important;
        font-size: 16px !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
    }}
    div.stButton > button.orange-submit-btn:hover {{
        background-color: #facc15 !important;
        color: #1e293b !important;
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

    /* استایل پاپ‌آپ تمام صفحه بیومتریک */
    .custom-modal-overlay {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.45);
        z-index: 99999;
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    </style>
    """
    st.markdown(auth_css, unsafe_allow_html=True)

    if "show_bio" not in st.session_state: st.session_state.show_bio = False
    if "bio_method" not in st.session_state: st.session_state.bio_method = "fingerprint"

    st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
    
    # --- ۲. هدر فوق‌العاده چسبیده و مماس (بدون فاصله کاذب) ---
    logo_html = "☀️"
    if os.path.exists("./static/logo.png"):
        with open("./static/logo.png", "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" width="35" style="display: block; margin: 0; padding: 0;">'

    st.markdown(f"""
    <div class="brand-flex-container">
        {logo_html}
        <h2 class="brand-title-text">TopSUNify</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

    # --- ۳. فیلد نام کاربری ---
    username = st.text_input("نام کاربری", value="", placeholder="نام کاربری")

    # --- ۴. فیلد رمز عبور + دکمه مینی‌مال بیومتریک جفت شده ---
    st.markdown('<div class="bio-container">', unsafe_allow_html=True)
    password = st.text_input("رمز ورود", type="password", placeholder="رمز ورود")
    
    st.markdown('<div class="bio-inside-btn">', unsafe_allow_html=True)
    if st.button("🪪", key="trigger_bio_popup", help="انتخاب روش ورود بیومتریک"):
        st.session_state.show_bio = True
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

    # --- ۵. دکمه اصلی ورود ---
    if st.button("ورود به TopSUNify", key="submit_orange", use_container_width=True):
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

    # --- ۷. پاپ‌آپ (Modal) انتخاب دوگانه روش احراز هویت ---
    if st.session_state.show_bio:
        st.markdown('<div class="custom-modal-overlay">', unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown('<h3 style="text-align: center; color: #1e293b; margin-bottom: 5px;">روش ورود امن</h3>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; color: #64748b; font-size: 13px;">لطفاً روش احراز هویت خود را انتخاب کنید:</p>', unsafe_allow_html=True)
            
            b_col1, b_col2 = st.columns(2)
            if b_col1.button("☝️ Fingerprint", use_container_width=True, key="set_bio_finger"):
                st.session_state.bio_method = "fingerprint"
                st.rerun()
            if b_col2.button("👤 Face ID", use_container_width=True, key="set_bio_face"):
                st.session_state.bio_method = "face"
                st.rerun()
            
            st.divider()
            
            if st.session_state.bio_method == "fingerprint":
                st.markdown('<h4 style="color: #ea580c; text-align: center;">ورود با اثر انگشت</h4>', unsafe_allow_html=True)
                st.markdown('<h1 style="text-align: center; font-size: 55px; margin: 10px 0; color: #ea580c;">🌀</h1>', unsafe_allow_html=True)
                st.markdown('<p style="text-align: center; color: #64748b; font-size: 13px;">حسگر اثر انگشت دستگاه را لمس کنید</p>', unsafe_allow_html=True)
            else:
                st.markdown('<h4 style="color: #ea580c; text-align: center;">ورود با تشخیص چهره</h4>', unsafe_allow_html=True)
                st.markdown('<h1 style="text-align: center; font-size: 55px; margin: 10px 0; color: #facc15;">📸</h1>', unsafe_allow_html=True)
                st.markdown('<p style="text-align: center; color: #64748b; font-size: 13px;">لطفاً به دوربین جلوی دستگاه نگاه کنید</p>', unsafe_allow_html=True)
            
            st.markdown('<br>', unsafe_allow_html=True)
            
            if st.button("انصراف و بازگشت", use_container_width=True, key="close_modal_view"):
                st.session_state.show_bio = False
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)

    # اسکریپت برای چسباندن استایل نارنجی به دکمه ورود
    st.markdown("""
        <script>
        var buttons = window.parent.document.getElementsByTagName('button');
        for (var i = 0; i < buttons.length; i++) {
            if (buttons[i].innerText === "ورود به TopSUNify") {
                buttons[i].classList.add("orange-submit-btn");
            }
        }
        </script>
    """, unsafe_allow_html=True)
