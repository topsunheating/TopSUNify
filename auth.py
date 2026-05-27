import streamlit as st
import time
import os
import base64

def render_auth_page():
    # --- ۱. لود ایمن فونت ایران‌یکان از پوشه محلی و تزریق CSS زرد و نارنجی ---
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

    /* هدر: چیدمان لوگو و متن انگلیسی */
    .brand-container {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        max-width: 400px;
        margin: 0 auto 30px auto;
    }}
    
    /* استایل فیلدهای ورودی تک‌خطی مدرن */
    div[data-testid="stTextInput"] {{
        max-width: 400px;
        margin: 0 auto !important;
    }}
    
    .stTextInput input {{
        border-top: none !important;
        border-left: none !important;
        border-right: none !important;
        border-bottom: 1.5px solid #cbd5e1 !important;
        border-radius: 0px !important;
        background-color: transparent !important;
        padding: 12px 5px !important;
        font-size: 16px !important;
        color: #1e293b !important;
    }}
    .stTextInput input:focus {{
        border-bottom: 2px solid #ea580c !important; /* لاین زیرین نارنجی هنگام فوکوس */
        box-shadow: none !important;
    }}

    /* موقعیت‌دهی آیکون بیومتریک در سمت چپ، داخل فیلد پسورد */
    .bio-container {{
        position: relative;
        max-width: 400px;
        margin: 0 auto;
    }}
    
    div.bio-inside-btn {{
        position: absolute;
        left: 40px;
        top: 38px;
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

    /* دکمه اصلی ورود به TopSUNify (نارنجی با هاور زرد) */
    div.stButton > button.orange-submit-btn {{
        width: 100% !important;
        max-width: 400px;
        display: block;
        margin: 40px auto 0 auto !important;
        background-color: #ea580c !important; /* نارنجی */
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 0 !important;
        font-size: 16px !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
    }}
    div.stButton > button.orange-submit-btn:hover {{
        background-color: #facc15 !important; /* تغییر رنگ به زرد هنگام هاور */
        color: #1e293b !important;
    }}
    
    .forgot-link {{
        text-align: center;
        margin-top: 25px;
    }}
    .forgot-link a {{
        color: #64748b !important;
        text-decoration: none;
        font-size: 14px;
    }}
    .forgot-link a:hover {{
        color: #ea580c !important;
    }}

    /* 📌 استایل پاپ‌آپ انتخابی بیومتریک */
    .custom-modal-overlay {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: 99999;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }}
    
    .custom-modal-card {{
        background: white;
        width: 100%;
        max-width: 380px;
        border-radius: 24px;
        padding: 25px;
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 5px solid #ea580c; /* نوار بالای پاپ آپ نارنجی */
    }}

    /* دکمه‌های انتخاب روش درون پاپ‌آپ */
    .modal-nav-container {{
        display: flex;
        gap: 10px;
        margin: 20px 0;
    }}
    </style>
    """
    st.markdown(auth_css, unsafe_allow_html=True)

    # مدیریت وضعیت پاپ‌آپ احراز هویت هوشمند
    if "show_bio" not in st.session_state: st.session_state.show_bio = False
    if "bio_method" not in st.session_state: st.session_state.bio_method = "fingerprint"

    st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
    
    # --- ۲. هدر: لوگو سمت راست و متن تیره TopSUNify سمت چپ کاملاً هم‌تراز ---
    h_col1, h_col2 = st.columns()
    with h_col1:
        st.markdown('<h2 style="color: #000000; font-weight: 900; margin: 12px 0 0 0; text-align: left; direction: ltr;">TopSUNify</h2>', unsafe_allow_html=True)
    with h_col2:
        try: st.image("./static/logo.png", width=65)
        except: st.write("☀️")

    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

    # --- ۳. فیلد نام کاربری (کاملاً خالی و بدون پیش‌فرض) ---
    username = st.text_input("نام کاربری", value="", placeholder="نام کاربری را وارد کنید")

    # --- ۴. فیلد رمز عبور + آیکون کوچک ورود بیومتریک در کنار چشم ---
    st.markdown('<div class="bio-container">', unsafe_allow_html=True)
    password = st.text_input("رمز ورود", type="password", placeholder="رمز ورود را وارد کنید")
    
    # دکمه ورود بیومتریک (💳) قرار گرفته در موقعیت مناسب تراز شده
    st.markdown('<div class="bio-inside-btn">', unsafe_allow_html=True)
    if st.button("💳", key="trigger_bio_popup", help="انتخاب روش ورود بیومتریک"):
        st.session_state.show_bio = True
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

    # --- ۵. دکمه اصلی ورود (نارنجی یکدست با کلاس سفارشی) ---
    if st.button("ورود به TopSUNify", key="submit_orange", use_container_width=True, type="primary"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("ورود با موفقیت انجام شد.")
            time.sleep(0.5)
            st.rerun()
        elif username == "" or password == "":
            st.warning("⚠️ لطفاً نام کاربری و رمز عبور را وارد کنید.")
        else:
            st.error("❌ نام کاربری یا رمز ورود اشتباه است.")

    # --- ۶. لینک فعال‌سازی / فراموشی رمز عبور ---
    st.markdown('<div class="forgot-link"><a href="#">فعال‌سازی / فراموشی رمز</a></div>', unsafe_allow_html=True)

    # --- ۷. پاپ‌آپ (Modal) تعاملی انتخاب روش بیومتریک ---
    if st.session_state.show_bio:
        st.markdown('<div class="custom-modal-overlay">', unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown('<h3 style="text-align: center; color: #1e293b; margin-bottom: 5px;">روش ورود بیومتریک</h3>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; color: #64748b; font-size: 13px;">لطفاً یکی از دو روش زیر را انتخاب کنید:</p>', unsafe_allow_html=True)
            
            # ردیف انتخاب بین دو حالت اثر انگشت و چهره
            b_col1, b_col2 = st.columns(2)
            
            # دکمه اثر انگشت (تم زرد/نارنجی در صورت انتخاب)
            if b_col1.button("☝️ Fingerprint", use_container_width=True, key="btn_select_finger"):
                st.session_state.bio_method = "fingerprint"
                st.rerun()
                
            # دکمه تشخیص چهره
            if b_col2.button("👤 Face ID", use_container_width=True, key="btn_select_face"):
                st.session_state.bio_method = "face"
                st.rerun()
            
            st.divider()
            
            # نمایش المان گرافیکی مربوط به انتخاب کاربر
            if st.session_state.bio_method == "fingerprint":
                st.markdown('<h4 style="color: #ea580c; text-align: center;">حسگر اثر انگشت</h4>', unsafe_allow_html=True)
                st.markdown('<h1 style="text-align: center; font-size: 55px; margin: 10px 0; color: #ea580c;">🌀</h1>', unsafe_allow_html=True)
                st.markdown('<p style="text-align: center; color: #64748b; font-size: 13px;">لطفاً انگشت خود را روی حسگر بگذارید</p>', unsafe_allow_html=True)
            else:
                st.markdown('<h4 style="color: #ea580c; text-align: center;">تشخیص چهره</h4>', unsafe_allow_html=True)
                st.markdown('<h1 style="text-align: center; font-size: 55px; margin: 10px 0; color: #facc15;">📸</h1>', unsafe_allow_html=True)
                st.markdown('<p style="text-align: center; color: #64748b; font-size: 13px;">لطفاً به دوربین جلوی دستگاه نگاه کنید</p>', unsafe_allow_html=True)
            
            st.markdown('<br>', unsafe_allow_html=True)
            
            # دکمه خروج و انصراف از پاپ آپ
            if st.button("انصراف و بازگشت", use_container_width=True, key="close_modal_view"):
                st.session_state.show_bio = False
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)

    # اعمال کلاس CSS سفارشی دکمه به المان استریم‌لیت جهت اطمینان از اعمال رنگ نارنجی
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
