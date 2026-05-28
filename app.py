import streamlit as st
import os
import base64
import pandas as pd
import tempfile

# 🛑 دستور set_page_config حتماً باید در بالاترین خط برنامه باقی بماند
st.set_page_config(
    page_title="TopSUNify",
    page_icon="./TopSUN-Powered.png", 
    layout="wide"
)

# ====================== ۱. مدیریت وضعیت جهانی سیستم (Session State) ======================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "dashboard" 
if "active_sub_action" not in st.session_state:
    st.session_state.active_sub_action = "file_plan" 

if "manual_rooms" not in st.session_state: st.session_state.manual_rooms = []
if "show_table" not in st.session_state: st.session_state.show_table = False
if "m80" not in st.session_state: st.session_state.m80 = 0.0
if "m40" not in st.session_state: st.session_state.m40 = 0.0
if "xps" not in st.session_state: st.session_state.xps = 0.0
if "thermostat_count" not in st.session_state: st.session_state.thermostat_count = 1
if "panel_count" not in st.session_state: st.session_state.panel_count = 1
if "source_type" not in st.session_state: st.session_state.source_type = ""

# متغیرهای بخش پروفایل کاربری (بروزرسانی شده بر اساس تصویر ارسالی شما)
if "user_display_name" not in st.session_state: st.session_state.user_display_name = "رضا تلچی"
if "user_phone" not in st.session_state: st.session_state.user_phone = "۰۹۱۲۰۱۹۸۲۲۹"
if "user_role" not in st.session_state: st.session_state.user_role = "کاربر عمومی" 
if "profile_pic_base64" not in st.session_state: st.session_state.profile_pic_base64 = ""

# ====================== ۲. بررسی احراز هویت ======================
import auth

if not st.session_state.logged_in:
    auth.render_auth_page()
    st.stop()

# ====================== ۳. ایمپورت کتابخانه‌ها و ماژول‌های مهندسی ======================
import Financial
import main
from Financial import calculate_tosunify_proforma

# ====================== ۴. هوشمندسازی CSS با الهام از طراحی موبایلت ======================
def inject_custom_css():
    font_path = "iranyekan.ttf"
    font_base64 = ""

    if os.path.exists(font_path):
        with open(font_path, "rb") as f:
            font_base64 = base64.b64encode(f.read()).decode()

    css = f"""
    <style>
    @font-face {{
        font-family: 'iranyekan';
        src: url(data:font/ttf;base64,{font_base64}) format('truetype');
    }}

    html, body, [class*="css"], * {{
        font-family: 'iranyekan', Tahoma, sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }}

    [data-testid="stHeader"], [data-testid="stSidebar"] {{
        display: none !important;
    }}

    .main .block-container {{
        max-width: 550px !important;
        margin: 0 auto !important;
        padding-left: 16px !important;
        padding-right: 16px !important;
        padding-bottom: 140px !important; /* فضا برای نوار پایینی مینی‌مال */
        background-color: #f4f6f9 !important;
        min-height: 100vh;
    }}

    .app-main-header-container {{
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        padding: 15px 0 !important;
    }}

    .module-card-box {{
        background: #ffffff !important;
        padding: 22px !important;
        border-radius: 24px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
        margin-bottom: 20px !important;
    }}

    /* استایل کارت هدر پروفایل مشابه موبایلت */
    .profile-header-card {{
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        background: #ffffff !important;
        padding: 20px !important;
        border-radius: 24px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02) !important;
    }}

    .profile-info-block {{
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }}

    .profile-name {{
        font-size: 19px !important;
        font-weight: 800 !important;
        color: #1e293b !important;
        margin-bottom: 6px !important;
    }}

    .profile-phone {{
        font-size: 14px !important;
        color: #64748b !important;
        letter-spacing: 0.5px;
    }}

    .profile-avatar-container {{
        position: relative !important;
        width: 64px !important;
        height: 64px !important;
    }}

    .profile-avatar-img {{
        width: 64px !important;
        height: 64px !important;
        border-radius: 50% !important;
        object-fit: cover !important;
        border: 2px solid #e2e8f0 !important;
    }}

    .profile-menu-item {{
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        padding: 18px 10px !important;
        border-bottom: 1px solid #f1f5f9 !important;
        color: #334155 !important;
    }}

    .profile-menu-item:last-child {{
        border-bottom: none !important;
    }}

    .profile-menu-right {{
        display: flex !important;
        align-items: center !important;
        gap: 14px !important;
        font-size: 15px !important;
    }}

    .profile-menu-icon {{
        font-size: 20px !important;
    }}

    .profile-menu-arrow {{
        color: #cbd5e1 !important;
        font-size: 13px !important;
    }}

    /* 📱 ساختار اختصاصی نوار ناوبری دکمه‌ای پایینی کاملاً فیکس و مشابه موبایلت */
    .fixed-bottom-nav-container {{
        position: fixed !important;
        bottom: 0 !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100% !important;
        max-width: 550px !important;
        background-color: #ffffff !important;
        box-shadow: 0 -8px 25px rgba(0,0,0,0.06) !important;
        z-index: 999999 !important;
        border-top: 1px solid #e2e8f0 !important;
        padding: 10px 14px 14px 14px !important;
    }}

    /* استایل اختصاصی برای دکمه‌های ناوبری پایینی */
    div.stButton > button {{
        border-radius: 16px !important;
        font-weight: bold !important;
        font-size: 12px !important;
        height: 52px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 2px !important;
        line-height: 1.2 !important;
        transition: all 0.2s ease !important;
    }}
    
    /* متمایز کردن دکمه وسط (تاپسان / موبایلت) */
    div.stButton > button[key*="btn_nav_dash"] {{
        background-color: #f0fdf4 !important;
        border: 2px solid #22c55e !important;
        color: #166534 !important;
        transform: scale(1.05);
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

inject_custom_css()

# ====================== ۵. هدر تصویری جدید بر اساس لوگوی ارسالی شما ======================
if os.path.exists("TopSUN-Powered.png"):
    with open("TopSUN-Powered.png", "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode()
    st.markdown(f"""
    <div class="app-main-header-container">
        <img src="data:image/png;base64,{logo_base64}" style="max-width: 200px; height: auto; display: block; margin: 0 auto;">
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<div class="app-main-header-container" style="font-size:24px;">☀️ TopSUN</div>', unsafe_allow_html=True)

st.divider()


# ==============================================================================
# رندر کردن محتوای صفحات بر اساس تب فعال
# ==============================================================================

# ------------------------------------------------------------------------------
# ۱. محتوای تب: داشبورد (صفحه اصلی تاپسان)
# ------------------------------------------------------------------------------
if st.session_state.active_tab == "dashboard":
    st.markdown('<div class="module-card-box">', unsafe_allow_html=True)
    st.subheader("📊 داشبورد مدیریتی پروژه")
    st.write(f"جناب **{st.session_state.user_display_name}**، به سامانه هوشمند تاپسان خوش آمدید.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric(label="متراژ کل فیلم عرض ۸۰", value=f"{st.session_state.m80:.1f} م")
    with c2:
        st.metric(label="متراژ کل فیلم عرض ۴۰", value=f"{st.session_state.m40:.1f} م")
        
    st.info("برای محاسبات مهندسی و بارگذاری نقشه، از منوی پایین گزینه «پیش‌فاکتور» را انتخاب کنید.")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# ۲. محتوای تب: صدور پیش‌فاکتور
# ------------------------------------------------------------------------------
elif st.session_state.active_tab == "invoice":
    st.markdown('<div class="module-card-box">', unsafe_allow_html=True)
    st.subheader("🧾 صدور پیش‌فاکتور هوشمند")
    
    product_type = st.selectbox(
        "نوع سیستم گرمایشی مورد نظر را انتخاب کنید:",
        ["گرمایش کف (سیستم هوشمند)", "زیرفرشی", "رادیاتور", "رستورانی", "عمومی"],
        key="selected_product_type"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if product_type == "گرمایش کف (سیستم هوشمند)":
        col_sub1, col_sub2, col_sub3 = st.columns(3)
        if col_sub1.button("📂 فایل پلان", use_container_width=True, type="primary" if st.session_state.active_sub_action == "file_plan" else "secondary"):
            st.session_state.active_sub_action = "file_plan"
            st.rerun()
        if col_sub2.button("⌨️ ورود دستی ابعاد", use_container_width=True, type="primary" if st.session_state.active_sub_action == "manual_dim" else "secondary"):
            st.session_state.active_sub_action = "manual_dim"
            st.rerun()
        if col_sub3.button("✍️ مقادیر مستقیم", use_container_width=True, type="primary" if st.session_state.active_sub_action == "direct_val" else "secondary"):
            st.session_state.active_sub_action = "direct_val"
            st.rerun()

        st.markdown('<div class="module-card-box" style="margin-top:15px;">', unsafe_allow_html=True)

        if st.session_state.active_sub_action == "file_plan":
            st.markdown("<h5 style='color:#334155; margin-bottom:15px;'>فایل نقشه اتوکد کف (DXF / DWG) را انتخاب کنید:</h5>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader(label="", type=['dxf', 'dwg'], key="uploader_main", label_visibility="collapsed")
          
            if uploaded_file is not None:
                file_size_mb = uploaded_file.size / (1024 * 1024)
                st.success(f"✅ فایل بارگذاری شد: {uploaded_file.name} ({file_size_mb:.1f} مگابایت)")
                
                if st.button("🗑️ حذف فایل", key="del_uploader_main"):
                    st.session_state["uploader_main"] = None
                    if 'last_processed_file' in st.session_state: del st.session_state['last_processed_file']
                    st.session_state.show_table = False
                    st.rerun()

                file_id = f"{uploaded_file.name}_{uploaded_file.size}"
                if st.session_state.get('last_processed_file') != file_id:
                    try:
                        with st.spinner("در حال ارسال فایل به موتور تحلیل مهندسی تاپسان..."):
                            file_extension = os.path.splitext(uploaded_file.name).lower()
                            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp:
                                tmp.write(uploaded_file.getvalue())
                                tmp_path = tmp.name

                            m8, m4 = main.get_total_meters_from_file(tmp_path)
                            try: os.remove(tmp_path)
                            except: pass
                          
                            st.session_state.m80 = float(m8)
                            st.session_state.m40 = float(m4)
                            st.session_state.xps = round((m8 + m4) * 1.1, 1)
                            st.session_state.thermostat_count = main.calculate_thermostats([{'w': m8+m4, 'l': 1}])
                            st.session_state.panel_count = 1 if (m8 > 0 or m4 > 0) else 0
                          
                            st.session_state.last_processed_file = file_id
                            st.session_state.source_type = "file"
                            st.session_state.show_table = True
                            st.rerun()
                    except Exception as e:
                        st.error(f"خطا در پردازش فایل: {e}")

        elif st.session_state.active_sub_action == "manual_dim":
            with st.expander("➕ افزودن اتاق جدید", expanded=True):
                c_name, c_w, c_l = st.columns(3)
                r_name = c_name.text_input("نام فضا", value="پذیرایی", key="manual_r_name")
                r_w = c_w.number_input("عرض (متر)", min_value=0.0, step=0.1, value=4.0, key="manual_r_w")
                r_l = c_l.number_input("طول (متر)", min_value=0.0, step=0.1, value=5.0, key="manual_r_l")
                
                if st.button("➕ اضافه کردن به لیست", key="add_room_action", use_container_width=True):
                    if r_w > 0 and r_l > 0:
                        st.session_state.manual_rooms.append({"name": r_name, "w": r_w, "l": r_l})
                        st.session_state.source_type = "manual"
                        st.session_state.show_table = True
                        st.rerun()

            if st.session_state.manual_rooms:
                st.write("### 📋 لیست فضاهای ثبت شده:")
                for i, room in enumerate(st.session_state.manual_rooms):
                    with st.container(border=True):
                        st.markdown(f"**{room['name']}** | مساحت: {room['w'] * room['l']:.1f} مترمربع")
                        if st.button("🗑️ حذف", key=f"delete_room_{i}"):
                            st.session_state.manual_rooms.pop(i)
                            if not st.session_state.manual_rooms: st.session_state.show_table = False
                            st.rerun()

        elif st.session_state.active_sub_action == "direct_val":
            st.write("### 📝 ورود مستقیم مقادیر فاکتور")
            m80_dir = st.number_input("فیلم عرض 80 (متر)", min_value=0.0, value=st.session_state.m80)
            m40_dir = st.number_input("فیلم عرض 40 (متر)", min_value=0.0, value=st.session_state.m40)
            insulation_dir = st.number_input("عایق (متر مربع)", min_value=0.0, value=st.session_state.xps)
            thermostat_dir = st.number_input("ترموستات (عدد)", min_value=0, value=st.session_state.thermostat_count)
            panel_dir = st.number_input("تابلو فرمان (عدد)", min_value=0, value=st.session_state.panel_count)
                
            if st.button("💾 ثبت مقادیر مستقیم", key="submit_invoice_manual"):
                st.session_state.m80 = m80_dir; st.session_state.m40 = m40_dir
                st.session_state.xps = insulation_dir; st.session_state.thermostat_count = thermostat_dir
                st.session_state.panel_count = panel_dir
                st.session_state.source_type = "direct_invoice"
                st.session_state.show_table = True
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.get("show_table", False):
            st.markdown('<div class="module-card-box">', unsafe_allow_html=True)
            if st.session_state.get("source_type") == "manual":
                total_area = sum(r['w'] * r['l'] for r in st.session_state.manual_rooms)
                st.session_state.m80 = round(total_area * 0.75, 1)
                st.session_state.m40 = round(total_area * 0.15, 1)
                st.session_state.xps = round(total_area * 1.1, 1)
                st.session_state.thermostat_count = len(st.session_state.manual_rooms) or 1

            try:
                res = calculate_tosunify_proforma(st.session_state.m80, st.session_state.m40, 0, 0, 0, st.session_state.thermostat_count)
                res['m80_total'] = st.session_state.m80 * res.get('UnitPrice_m80', 17900000)
                res['m40_total'] = st.session_state.m40 * res.get('UnitPrice_m40', 13350000)
                res['thermostat_total'] = st.session_state.thermostat_count * res.get('UnitPrice_thermostat', 3536000)
                p_count = st.session_state.panel_count if st.session_state.source_type == "direct_invoice" else (1 if (st.session_state.m80 > 0 or st.session_state.m40 > 0) else 0)
                res['ControlPanel_Total'] = p_count * res.get('UnitPrice_panel', 88950000) if p_count > 0 else 0

                calculated_subtotal = res['m80_total'] + res['m40_total'] + res['thermostat_total'] + res['ControlPanel_Total'] + (st.session_state.xps * res.get('UnitPrice_insulation_meter', 1450000) if st.session_state.xps > 0 else 0)

                table_data = []
                if st.session_state.m80 > 0: table_data.append(["فیلم عرض ۸۰", f"{st.session_state.m80:.1f}", "متر", f"{res['m80_total']:,.0f}"])
                if st.session_state.m40 > 0: table_data.append(["فیلم عرض ۴۰", f"{st.session_state.m40:.1f}", "متر", f"{res['m40_total']:,.0f}"])
                if st.session_state.thermostat_count > 0: table_data.append(["ترموستات", str(st.session_state.thermostat_count), "عدد", f"{res['thermostat_total']:,.0f}"])
                if p_count > 0: table_data.append(["تابلو فرمان مرکزی", str(p_count), "عدد", f"{res['ControlPanel_Total']:,.0f}"])
                if st.session_state.xps > 0: table_data.append(["رول عایق تخصصی", f"{st.session_state.xps:.1f}", "مترمربع", f"{(st.session_state.xps * res.get('UnitPrice_insulation_meter', 1450000)):,.0f}"])
                
                st.write("### 🧾 ریز پیش‌فاکتور محاسباتی پروژه:")
                st.table(pd.DataFrame(table_data, columns=["شرح کالا", "مقدار", "واحد", "مبلغ کل (ریال)"]))
                st.success(f"**مبلغ نهایی فاکتور: {calculated_subtotal:,.0f} ریال**")
            except Exception as e:
                st.error(f"خطا در محاسبات: {e}")
            st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# ۳. محتوای تب: خدمات فنی
# ------------------------------------------------------------------------------
elif st.session_state.active_tab == "services":
    st.markdown('<div class="module-card-box">', unsafe_allow_html=True)
    st.subheader("🛠️ خدمات فنی و پشتیبانی تاپسان")
    st.radio("نوع درخواست خدمات:", ["نصب اولیه سیستم گرمایش", "اعلام خرابی/عیب‌یابی", "درخواست سرویس دوره‌ای"])
    with st.form("service_form"):
        st.text_area("توضیحات و آدرس دقیق پروژه")
        if st.form_submit_button("ثبت درخواست"): st.success("📌 درخواست شما ثبت و به واحد فنی ارجاع شد.")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# ۴. محتوای تب: کاتالوگ و دانشنامه
# ------------------------------------------------------------------------------
elif st.session_state.active_tab == "info":
    st.markdown('<div class="module-card-box">', unsafe_allow_html=True)
    st.subheader("📚 دانشنامه و اطلاعات فنی")
    st.write("مستندات مهندسی، نقشه‌های استاندارد چیدمان و کاتالوگ‌های سیستم‌های حرارتی در این بخش در دسترس هستند.")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# ۵. محتوای تب اختصاصی: پروفایل کاربری
# ------------------------------------------------------------------------------
elif st.session_state.active_tab == "profile":
    # لود آیکون یا عکس پروفایل پیش‌فرض از تصاویر ارسالی شما
    avatar_src = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
    if st.session_state.profile_pic_base64:
        avatar_src = f"data:image/png;base64,{st.session_state.profile_pic_base64}"
        
    user_header_html = f"""
    <div class="profile-header-card">
        <div class="profile-info-block">
            <div class="profile-name">{st.session_state.user_display_name}</div>
            <div class="profile-phone">{st.session_state.user_phone}</div>
        </div>
        <div class="profile-avatar-container">
            <img class="profile-avatar-img" src="{avatar_src}">
        </div>
    </div>
    """
    st.markdown(user_header_html, unsafe_allow_html=True)
    
    # منوی مینی‌مال گزینه‌ها مشابه لیست حساب کاربری موبایلت
    st.markdown('<div class="module-card-box" style="padding: 5px 15px !important;">', unsafe_allow_html=True)
    menu_items = [
        {"label": "پیش‌فاکتورهای تکمیل شده", "icon": "📝"},
        {"label": "سپرده‌های حرارتی و پروژه‌ها", "icon": "⭐"},
        {"label": "تسهیلات و عاملیت‌ها", "icon": "🏢"},
        {"label": "اعلام موجودی انبار کالا", "icon": "📦"},
        {"label": "تنظیمات سیستمی", "icon": "⚙️"},
    ]
    for item in menu_items:
        st.markdown(f"""
        <div class="profile-menu-item">
            <div class="profile-menu-right">
                <span class="profile-menu-icon">{item['icon']}</span>
                <span style="font-weight: 500; color:#1e293b;">{item['label']}</span>
            </div>
            <div class="profile-menu-arrow">◀</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🚪 خروج از حساب کاربری تاپسان", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()


# ==============================================================================
# 🎛️ هندسه ناوبری ۵ دکمه‌ای پایینی کاملاً منطبق با ساختار اپلیکیشن موبایلت
# چیدمان از راست به چپ: خدمات | پیش‌فاکتور | [دکمه شاخص وسط: تاپسان] | اطلاعات | پروفایل (عکس کاربر)
# ==============================================================================
st.markdown('<div class="fixed-bottom-nav-container">', unsafe_allow_html=True)
col_nav1, col_nav2, col_nav3, col_nav4, col_nav5 = st.columns(5)

# ۱. منتهی‌الیه راست: خدمات
if col_nav1.button("🛠️\nخدمات", key="btn_nav_serv", use_container_width=True, type="primary" if st.session_state.active_tab == "services" else "secondary"):
    st.session_state.active_tab = "services"
    st.rerun()

# ۲. راست وسط: پیش‌فاکتور
if col_nav2.button("🧾\nپیش‌فاکتور", key="btn_nav_inv", use_container_width=True, type="primary" if st.session_state.active_tab == "invoice" else "secondary"):
    st.session_state.active_tab = "invoice"
    st.rerun()

# ۳. دکمه شاخص وسط: داشبورد اصلی (موبایلت)
if col_nav3.button("☀️\nتاپسان", key="btn_nav_dash", use_container_width=True):
    st.session_state.active_tab = "dashboard"
    st.rerun()

# ۴. چپ وسط: اطلاعات
if col_nav4.button("📚\nاطلاعات", key="btn_nav_info", use_container_width=True, type="primary" if st.session_state.active_tab == "info" else "secondary"):
    st.session_state.active_tab = "info"
    st.rerun()

# ۵. منتهی‌الیه چپ: پروفایل کاربری (دقیقا مطابق عکس موبایلت ارسالی)
if col_nav5.button("👤\nپروفایل", key="btn_nav_prof", use_container_width=True, type="primary" if st.session_state.active_tab == "profile" else "secondary"):
    st.session_state.active_tab = "profile"
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
