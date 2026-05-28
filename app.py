import streamlit as st

# 🛑 دستور set_page_config حتماً باید در بالاترین خط برنامه باقی بماند
st.set_page_config(
    page_title="TopSUNify",
    page_icon="./topsunify.png",  # استفاده از لوگوی اصلی تاپسان
    layout="wide"  # این گزینه به همراه CSS باعث ریسپانسیو شدن کامل در تبلت و دسکتاپ می‌شود
)

# ====================== ۱. اضافه کردن ماژول احراز هویت ======================
import auth

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    auth.render_auth_page()
    st.stop()

# ====================== ۲. ایمپورت کتابخانه‌ها و ماژول‌های مهندسی ======================
import Financial
import main
import os
import base64
import jdatetime  
import ezdxf
import tempfile
import pandas as pd
from PIL import Image
from Financial import calculate_tosunify_proforma, generate_proforma_pdf

# ====================== ۳. هوشمندسازی CSS با فونت ایران‌یکان و ظاهر نیتیو ======================
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

    /* حذف هدر و سایدبار پیش‌فرض برای ظاهر کاملاً اپلیکیشنی */
    [data-testid="stHeader"], [data-testid="stSidebar"] {{
        display: none !important;
    }}

    /* --- بهینه‌سازی کانتینر اصلی برای نمایش عالی در تبلت و موبایل --- */
    .main .block-container {{
        max-width: 550px !important; /* جمع شدن شیک و موبایلی در دسکتاپ */
        margin: 0 auto !important;
        padding-left: 16px !important;
        padding-right: 16px !important;
        padding-bottom: 110px !important; /* فضا برای اینکه محتوا زیر منوی پایین نرود */
        background-color: #f8fafc !important;
        min-height: 100vh;
    }}

    /* هدر بالای اپلیکیشن */
    .app-main-header-container {{
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        padding: 10px 0 !important;
        margin-bottom: 5px !important;
    }}

    /* --- استایل گرید آیکون‌ها (منوی دسترسی سریع ماژول‌ها) --- */
    .icon-grid-container {{
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 12px !important;
        background: #ffffff !important;
        padding: 16px 10px !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 20px !important;
    }}
    
    .icon-item-link {{
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        text-decoration: none !important;
        cursor: pointer !important;
    }}
    
    .icon-circle {{
        width: 54px !important;
        height: 54px !important;
        border-radius: 18px !important;
        background-color: #f1f5f9 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 24px !important;
        margin-bottom: 6px !important;
        transition: all 0.15s ease !important;
    }}
    
    .icon-item-link.active-action .icon-circle {{
        background-color: #fef3c7 !important; /* لایت زرد/نارنجی متمایز */
        border: 2px solid #ea580c !important;
        color: #ea580c !important;
    }}
    
    .icon-label {{
        font-size: 11px !important;
        color: #475569 !important;
        font-weight: bold !important;
        text-align: center !important;
        white-space: nowrap !important;
    }}

    /* باکس محتوای داخلی هر بخش */
    .module-card-box {{
        background: #ffffff !important;
        padding: 20px !important;
        border-radius: 24px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04) !important;
        margin-bottom: 20px !important;
    }}

    /* --- استایل‌های اختصاصی بخش پروفایل کاربری --- */
    .profile-header-card {{
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        background: #ffffff !important;
        padding: 15px !important;
        border-radius: 24px !important;
        margin-bottom: 15px !important;
    }}

    .profile-info-block {{
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }}

    .profile-name {{
        font-size: 18px !important;
        font-weight: 800 !important;
        color: #1e293b !important;
        margin-bottom: 4px !important;
    }}

    .profile-phone {{
        font-size: 13px !important;
        color: #64748b !important;
    }}

    .profile-avatar-container {{
        position: relative !important;
        width: 68px !important;
        height: 68px !important;
    }}

    .profile-avatar-img {{
        width: 68px !important;
        height: 68px !important;
        border-radius: 50% !important;
        object-fit: cover !important;
        border: 2px solid #e2e8f0 !important;
    }}

    .profile-role-badge-box {{
        background: #f1f5f9 !important;
        padding: 12px 16px !important;
        border-radius: 16px !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        margin-bottom: 25px !important;
    }}

    .profile-role-title {{
        font-size: 14px !important;
        color: #475569 !important;
        font-weight: bold !important;
    }}

    .profile-role-value {{
        font-size: 14px !important;
        color: #0f172a !important;
        font-weight: 800 !important;
    }}

    /* منوهای خطی لیست ملو */
    .profile-menu-item {{
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        padding: 16px 8px !important;
        border-bottom: 1px solid #f1f5f9 !important;
        text-decoration: none !important;
        color: #334155 !important;
        transition: background 0.2s !important;
    }}

    .profile-menu-item:last-child {{
        border-bottom: none !important;
    }}

    .profile-menu-right {{
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
        font-size: 15px !important;
        font-weight: bold !important;
    }}

    .profile-menu-icon {{
        font-size: 20px !important;
    }}

    .profile-menu-arrow {{
        color: #cbd5e1 !important;
        font-size: 14px !important;
    }}

    /* --- سیستم نویگیشن فیکس شده در پایین (Bottom Navigation) --- */
    .fixed-bottom-nav {{
        position: fixed !important;
        bottom: 0 !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100% !important;
        max-width: 550px !important;
        height: 70px !important;
        background-color: #ffffff !important;
        box-shadow: 0 -5px 15px rgba(0,0,0,0.06) !important;
        z-index: 99999 !important;
        display: flex !important;
        justify-content: space-around !important;
        align-items: center !important;
        border-top: 1px solid #e2e8f0 !important;
        padding-bottom: env(safe-area-inset-bottom) !important;
    }}

    .nav-tab-item {{
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        text-decoration: none !important;
        color: #94a3b8 !important;
        font-size: 10px !important;
        font-weight: bold !important;
        transition: all 0.2s ease !important;
    }}

    .nav-tab-item.active-tab {{
        color: #ea580c !important; /* رنگ نارنجی سازمانی برند تاپسان */
    }}

    .nav-tab-icon {{
        font-size: 20px !important;
        margin-bottom: 3px !important;
    }}

    /* ================= FILE UPLOAD ================= */
    [data-testid="stFileUploadDropzone"],
    [data-testid="stFileUploaderDropzone"] {{
        border: 2px dashed #ea580c !important;
        border-radius: 24px !important;
        background-color: #f8fafc !important;
        padding: 40px 10px !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

inject_custom_css()

# ====================== ۴. هدر بالایی اختصاصی (فقط لوگوی تصویری بدون متن) ======================
header_logo_html = ""
if os.path.exists("topsunify.png"):
    with open("topsunify.png", "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode()
    header_logo_html = f"""
    <div class="app-main-header-container">
        <img src="data:image/png;base64,{logo_base64}" style="max-width: 140px; height: auto; display: block; margin: 0 auto;">
    </div>
    """
else:
    # فال‌بک در صورتی که فایل موقتاً وجود نداشته باشد
    header_logo_html = '<div class="app-main-header-container" style="font-size:24px;">☀️</div>'

st.markdown(header_logo_html, unsafe_allow_html=True)
st.divider()

# ====================== ۵. مدیریت وضعیت جهانی سیستم (Session State) ======================
if "manual_rooms" not in st.session_state: st.session_state.manual_rooms = []
if "show_table" not in st.session_state: st.session_state.show_table = False
if "final_res" not in st.session_state: st.session_state.final_res = {}
if "m80" not in st.session_state: st.session_state.m80 = 0.0
if "m40" not in st.session_state: st.session_state.m40 = 0.0
if "xps" not in st.session_state: st.session_state.xps = 0.0
if "thermostat_count" not in st.session_state: st.session_state.thermostat_count = 1
if "panel_count" not in st.session_state: st.session_state.panel_count = 1
if "source_type" not in st.session_state: st.session_state.source_type = ""

# متغیرهای پیش‌فرض بخش پروفایل کاربری
if "user_display_name" not in st.session_state: st.session_state.user_display_name = "رضا تلچی"
if "user_phone" not in st.session_state: st.session_state.user_phone = "۰۹۱۲۰۱۹۸۲۲۹"
if "user_role" not in st.session_state: st.session_state.user_role = "کاربر عمومی" 
if "profile_pic_base64" not in st.session_state: st.session_state.profile_pic_base64 = ""

# مدیریت تب فعال پایین و آیکون فعال گرید از روی آدرس URL (پایداری کوئری پارامترها)
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "dashboard" 
if "active_sub_action" not in st.session_state:
    st.session_state.active_sub_action = "file_plan" 

query_p = st.query_params
if "nav_tab" in query_p:
    st.session_state.active_tab = query_p["nav_tab"]
if "sub_act" in query_p:
    st.session_state.active_sub_action = query_p["sub_act"]


# ==============================================================================
# رندر کردن محتوا بر اساس تب انتخاب شده در منوی پایین
# ==============================================================================

# ------------------------------------------------------------------------------
# ۱. محتوای تب: داشبورد (صفحه خانگی یا خلاصه پروژه)
# ------------------------------------------------------------------------------
if st.session_state.active_tab == "dashboard":
    st.markdown('<div class="module-card-box">', unsafe_allow_html=True)
    st.subheader("📊 داشبورد مدیریتی پروژه")
    st.write(f"جناب **{st.session_state.user_display_name}**، به سامانه هوشمند تاپسان خوش آمدید.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric(label="متراژ کل فیلم عرض ۸۰ (محاسباتی)", value=f"{st.session_state.m80:.1f} م")
    with c2:
        st.metric(label="متراژ کل فیلم عرض ۴۰ (محاسباتی)", value=f"{st.session_state.m40:.1f} م")
        
    st.info("برای شروع فرآیند مهندسی یا صدور اسناد، از منوی پایین بخش پیش‌فاکتور را انتخاب کنید.")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# ۲. محتوای تب: صدور پیش‌فاکتور (دارای گرید آیکونی اختصاصی در بالا)
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
        act_file = "active-action" if st.session_state.active_sub_action == "file_plan" else ""
        act_manual = "active-action" if st.session_state.active_sub_action == "manual_dim" else ""
        act_direct = "active-action" if st.session_state.active_sub_action == "direct_val" else ""
        
        grid_html = f"""
        <div class="icon-grid-container">
            <a href="?nav_tab=invoice&sub_act=file_plan" target="_self" class="icon-item-link {act_file}">
                <div class="icon-circle">📂</div>
                <div class="icon-label">فایل پلان</div>
            </a>
            <a href="?nav_tab=invoice&sub_act=manual_dim" target="_self" class="icon-item-link {act_manual}">
                <div class="icon-circle">⌨️</div>
                <div class="icon-label">ورود دستی ابعاد</div>
            </a>
            <a href="?nav_tab=invoice&sub_act=direct_val" target="_self" class="icon-item-link {act_direct}">
                <div class="icon-circle">✍️</div>
                <div class="icon-label">مقادیر مستقیم</div>
            </a>
        </div>
        """
        st.markdown(grid_html, unsafe_allow_html=True)

        st.markdown('<div class="module-card-box">', unsafe_allow_html=True)

        # الف) ماژول آپلود فایل نقشه
        if st.session_state.active_sub_action == "file_plan":
            st.markdown("<h5 style='color:#334155; margin-bottom:15px;'>فایل نقشه اتوکد کف (DXF / DWG) را انتخاب کنید:</h5>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader(label="", type=['dxf', 'dwg'], key="uploader_main", label_visibility="collapsed")
          
            if uploaded_file is not None:
                file_size_mb = uploaded_file.size / (1024 * 1024)
                st.success(f"✅ فایل بارگذاری شد: {uploaded_file.name} ({file_size_mb:.1f} مگابایت)")
                
                if st.button("🗑️ حذف فایل", key="del_uploader_main"):
                    st.session_state["uploader_main"] = None
                    if 'last_processed_file' in st.session_state: del st.session_state['last_processed_file']
                    if 'tmp_file_path' in st.session_state:
                        try: os.remove(st.session_state['tmp_file_path'])
                        except: pass
                        del st.session_state['tmp_file_path']
                    st.session_state.show_table = False
                    st.rerun()

                file_id = f"{uploaded_file.name}_{uploaded_file.size}"
               
                if st.session_state.get('last_processed_file') != file_id:
                    try:
                        with st.spinner("در حال ارسال فایل به موتور تحلیل مهندسی تاپسان..."):
                            file_extension = os.path.splitext(uploaded_file.name).lower()
                            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp:
                                tmp.write(uploaded_file.getvalue())
                                st.session_state['tmp_file_path'] = tmp.name

                            m8, m4 = main.get_total_meters_from_file(st.session_state['tmp_file_path'])
                          
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

        # ب) ماژول ورود دستی ابعاد فضاهای پروژه
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
            else:
                st.info("هنوز هیچ اتاقی اضافه نشده است.")

        # ج) ماژول ورود مستقیم مقادیر عددی فاکتور
        elif st.session_state.active_sub_action == "direct_val":
            st.write("### 📝 ورود مستقیم مقادیر فاکتور")
            m80_dir = st.number_input("فیلم عرض 80 (متر)", min_value=0.0, key="invoice_m80")
            m40_dir = st.number_input("فیلم عرض 40 (متر)", min_value=0.0, key="invoice_m40")
            insulation_dir = st.number_input("عایق (متر مربع)", min_value=0.0, key="invoice_insulation")
            thermostat_dir = st.number_input("ترموستات (عدد)", min_value=0, key="invoice_thermostat")
            panel_dir = st.number_input("تابلو فرمان (عدد)", min_value=0, key="invoice_panel")
                
            if st.button("💾 ثبت مقادیر مستقیم", key="submit_invoice_manual"):
                st.session_state.m80 = m80_dir; st.session_state.m40 = m40_dir
                st.session_state.xps = insulation_dir; st.session_state.thermostat_count = thermostat_dir
                st.session_state.panel_count = panel_dir
                st.session_state.source_type = "direct_invoice"
                st.session_state.show_table = True
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        # --- محاسبات، فیلترینگ اقلام صفر و صدور فاکتور نهایی ---
        st.markdown('<div class="module-card-box">', unsafe_allow_html=True)
        st.write("### ⚙️ تنظیمات فاکتور")
        col1, col2, col3 = st.columns(3)
        enable_inst = col1.checkbox("هزینه نصب")
        inst_rate = col1.number_input("درصد نصب", value=15) if enable_inst else 15
        enable_tax = col2.checkbox("مالیات")
        tax_rate = col2.number_input("درصد مالیات", value=10) if enable_tax else 10
        enable_disc = col3.checkbox("تخفیف")
        disc = col3.number_input("درصد تخفیف", value=0) if enable_disc else 0

        if st.session_state.get("show_table", False):
            if st.session_state.get("source_type") == "manual":
                total_area = sum(r['w'] * r['l'] for r in st.session_state.manual_rooms)
                st.session_state.m80 = round(total_area * 0.75, 1)
                st.session_state.m40 = round(total_area * 0.15, 1)
                st.session_state.xps = round(total_area * 1.1, 1)
                st.session_state.thermostat_count = len(st.session_state.manual_rooms) or 1

            try:
                res = calculate_tosunify_proforma(st.session_state.m80, st.session_state.m40, (inst_rate if enable_inst else 0), (disc if enable_disc else 0), (tax_rate if enable_tax else 0), st.session_state.thermostat_count)
                res['m80_total'] = st.session_state.m80 * res.get('UnitPrice_m80', 17900000)
                res['m40_total'] = st.session_state.m40 * res.get('UnitPrice_m40', 13350000)
                res['thermostat_total'] = st.session_state.thermostat_count * res.get('UnitPrice_thermostat', 3536000)
                p_count = st.session_state.panel_count if st.session_state.source_type == "direct_invoice" else (1 if (st.session_state.m80 > 0 or st.session_state.m40 > 0) else 0)
                res['ControlPanel_Total'] = p_count * res.get('UnitPrice_panel', 88950000) if p_count > 0 else 0

                calculated_subtotal = res['m80_total'] + res['m40_total'] + res['thermostat_total'] + res['ControlPanel_Total'] + (st.session_state.xps * res.get('UnitPrice_insulation_meter', 1450000) if st.session_state.xps > 0 else 0)
                inst_val = calculated_subtotal * ((inst_rate if enable_inst else 0) / 100)
                disc_val = (calculated_subtotal + inst_val) * ((disc if enable_disc else 0) / 100)
                final_val = calculated_subtotal + inst_val - disc_val + ((calculated_subtotal + inst_val - disc_val) * ((tax_rate if enable_tax else 0) / 100))

                table_data = []
                if st.session_state.m80 > 0: table_data.append(["فیلم عرض ۸۰", f"{st.session_state.m80:.1f}", "متر", f"{res['m80_total']:,.0f}"])
                if st.session_state.m40 > 0: table_data.append(["فیلم عرض ۴۰", f"{st.session_state.m40:.1f}", "متر", f"{res['m40_total']:,.0f}"])
                if st.session_state.thermostat_count > 0: table_data.append(["ترموستات", str(st.session_state.thermostat_count), "عدد", f"{res['thermostat_total']:,.0f}"])
                if p_count > 0: table_data.append(["تابلو فرمان مرکزی", str(p_count), "عدد", f"{res['ControlPanel_Total']:,.0f}"])
                if st.session_state.xps > 0: table_data.append(["رول عایق تخصصی", f"{st.session_state.xps:.1f}", "مترمربع", f"{(st.session_state.xps * res.get('UnitPrice_insulation_meter', 1450000)):,.0f}"])
                
                st.write("### 🧾 ریز پیش‌فاکتور محاسباتی پروژه:")
                st.table(pd.DataFrame(table_data, columns=["شرح کالا", "مقدار", "واحد", "مبلغ کل (ریال)"]))
                st.success(f"**مبلغ نهایی فاکتور: {final_val:,.0f} ریال**")
            except Exception as e:
                st.error(f"خطا در محاسبات: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info(f"بخش **{product_type}** به زودی فعال می‌شود.")

# ------------------------------------------------------------------------------
# ۳. محتوای تب: ثبت گارانتی
# ------------------------------------------------------------------------------
elif st.session_state.active_tab == "warranty":
    st.markdown('<div class="module-card-box">', unsafe_allow_html=True)
    st.subheader("🛡️ فرم ثبت گارانتی محصولات تاپسان")
    with st.form("warranty_form"):
        st.text_input("نام و نام خانوادگی خریدار")
        st.text_input("شماره سریال محصول")
        st.file_uploader("آپلود عکس یا فیلم نصب", type=["jpg", "png", "mp4"])
        if st.form_submit_button("ثبت گارانتی"): st.success("✅ مشخصات با موفقیت در بانک سامانه ثبت شد.")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# ۴. محتوای تب: درخواست خدمات فنی
# ------------------------------------------------------------------------------
elif st.session_state.active_tab == "services":
    st.markdown('<div class="module-card-box">', unsafe_allow_html=True)
    st.subheader("🛠️ ثبت درخواست خدمات فنی و مهندسی")
    st.radio("نوع درخواست:", ["نصب اولیه سیستم گرمایش", "اعلام خرابی/عیب‌یابی", "جابجایی پدها"])
    with st.form("service_form"):
        st.text_area("آدرس و توضیحات کروکی پروژه")
        if st.form_submit_button("ارسال درخواست"): st.success("📌 درخواست شما به واحد پشتیبانی ارجاع شد.")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# ۵. محتوای تب: اطلاعات فنی
# ------------------------------------------------------------------------------
elif st.session_state.active_tab == "info":
    st.markdown('<div class="module-card-box">', unsafe_allow_html=True)
    st.subheader("📚 بانک اطلاعات فنی و دانشنامه حرارتی")
    st.write("کاتالوگ‌ها، راهنماهای چیدمان فیلم و نقشه‌های ازپیش تحلیل‌شده به زودی بارگذاری می‌شوند.")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# ۶. محتوای تب اختصاصی: پروفایل کاربری (طراحی مینیمال و نیتیو بر اساس الگوی سامان)
# ------------------------------------------------------------------------------
elif st.session_state.active_tab == "profile":
    
    # تعیین تصویر آواتار پیش‌فرض در صورت عدم آپلود تصویر توسط کاربر
    avatar_src = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
    if st.session_state.profile_pic_base64:
        avatar_src = f"data:image/png;base64,{st.session_state.profile_pic_base64}"
        
    # تزریق استایل‌های بومی و اختصاصی کارت‌ها و لیست ملو (دقیقاً مشابه عکس ارسالی)
    st.markdown("""
    <style>
    /* هدر اصلی پروفایل کاربری */
    .sam-profile-card {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        background: #ffffff !important;
        padding: 16px 20px !important;
        border-radius: 24px !important;
        margin-bottom: 12px !important;
    }
    
    .sam-profile-info {
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }
    
    .sam-profile-name {
        font-size: 19px !important;
        font-weight: 800 !important;
        color: #1e293b !important;
        margin-bottom: 4px !important;
    }
    
    .sam-profile-phone {
        font-size: 13px !important;
        color: #64748b !important;
        letter-spacing: 0.5px;
    }
    
    /* کانتینر تصویر آواتار گرد با رینگ ظریف */
    .sam-avatar-box {
        position: relative !important;
        width: 64px !important;
        height: 64px !important;
    }
    
    .sam-avatar-img {
        width: 64px !important;
        height: 64px !important;
        border-radius: 50% !important;
        object-fit: cover !important;
        border: 2px solid #f1f5f9 !important;
    }
    
    /* باکس ملو تعیین سطح دسترسی حساب کاربری */
    .sam-role-badge-container {
        background: #f1f5f9 !important;
        padding: 14px 20px !important;
        border-radius: 18px !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        margin-bottom: 24px !important;
    }
    
    .sam-role-label {
        font-size: 13px !important;
        color: #64748b !important;
        font-weight: 500 !important;
    }
    
    .sam-role-value {
        font-size: 14px !important;
        color: #1e293b !important;
        font-weight: 800 !important;
    }
    
    /* استایل لیست گزینه‌های ملو و خطی همراه با فلش راهنما */
    .sam-menu-list-wrapper {
        background: #ffffff !important;
        border-radius: 24px !important;
        padding: 6px 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02) !important;
        margin-bottom: 20px !important;
    }
    
    .sam-menu-row-item {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        padding: 16px 4px !important;
        border-bottom: 1px solid #f8fafc !important;
        cursor: pointer;
    }
    
    .sam-menu-row-item:last-child {
        border-bottom: none !important;
    }
    
    .sam-menu-row-right {
        display: flex !important;
        align-items: center !important;
        gap: 14px !important;
    }
    
    .sam-menu-row-text {
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #334155 !important;
    }
    
    .sam-menu-row-icon {
        font-size: 18px !important;
        color: #475569 !important;
        display: flex !important;
        align-items: center !important;
    }
    
    .sam-menu-row-arrow {
        color: #cbd5e1 !important;
        font-size: 12px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ۱. بخش هدر کارت کاربری (نمایش نام و شماره تماس کارشناس)
    st.markdown(f"""
    <div class="sam-profile-card">
        <div class="sam-profile-info">
            <div class="sam-profile-name">{st.session_state.user_display_name}</div>
            <div class="sam-profile-phone">{st.session_state.user_phone}</div>
        </div>
        <div class="sam-avatar-box">
            <img class="sam-avatar-img" src="{avatar_src}">
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ۲. بخش نمایش سطح دسترسی جاری (باکس ملو طوسی رنگ بر اساس ساختار سامان)
    st.markdown(f"""
    <div class="sam-role-badge-container">
        <div class="sam-role-label">سطح دسترسی حساب:</div>
        <div class="sam-role-value">{st.session_state.user_role}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # ۳. ابزار پنهان/توسعه‌دهنده برای مدیریت و شبیه‌سازی تغییرات پروفایل بدون خروج از برنامه
    with st.expander("🛠️ تنظیمات شبیه‌سازی حساب (مخصوص مدیر سیستم)"):
        # تغییر عکس کاربری
        uploaded_avatar = st.file_uploader("تغییر تصویر آواتار:", type=["jpg", "png", "jpeg"], key="sam_avatar_uploader")
        if uploaded_avatar is not None:
            import base64
            st.session_state.profile_pic_base64 = base64.b64encode(uploaded_avatar.getvalue()).decode()
            st.toast("📷 تصویر پروفایل با موفقیت به‌روزرسانی شد.", icon="✅")
            st.rerun()
            
        # تغییر پویای سطح دسترسی و تست آن در کامپوننت‌ها
        roles_list = ["کاربر عمومی", "مدیر", "مدیر فروش", "مدیر فنی", "مدیر خدمات", "کارشناس فروش", "نمایندگی", "عاملیت"]
        current_idx = roles_list.index(st.session_state.user_role) if st.session_state.user_role in roles_list else 0
        selected_role_test = st.selectbox("تعیین سطح دسترسی کاربر جهت تست فیلترها:", roles_list, index=current_idx)
        if selected_role_test != st.session_state.user_role:
            st.session_state.user_role = selected_role_test
            st.rerun()

    # ۴. باکس منوهای خطی ظریف (دقیقاً متناظر با نیازهای اعلام شده و گرافیک تصویر اپلیکیشن سامان)
    st.markdown('<div class="sam-menu-list-wrapper">', unsafe_allow_html=True)
    
    sam_items = [
        {"label": "فاکتورهای تکمیل شده", "icon": "✅"},
        {"label": "فاکتورهای باز", "icon": "⏳"},
        {"label": "پیش فاکتورها", "icon": "🧾"},
        {"label": "مشتریان منتخب", "icon": "⭐"},
        {"label": "اعلام موجودی انبار", "icon": "📦"},
        {"label": "تنظیمات", "icon": "⚙️"},
    ]
    
    for item in sam_items:
        st.markdown(f"""
        <div class="sam-menu-row-item">
            <div class="sam-menu-row-right">
                <span class="sam-menu-row-icon">{item['icon']}</span>
                <span class="sam-menu-row-text">{item['label']}</span>
            </div>
            <div class="sam-menu-row-arrow">◀</div>
        </div>
        """, unsafe_allow_html=True)
        
# ==============================================================================
# ناوبری نهایی چسبیده به پایین صفحه (Bottom Navigation) - نسخه پایدار ۴ تب
# ==============================================================================

st.markdown("""
<style>
    .fixed-bottom-nav {
        position: fixed !important;
        bottom: 0 !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100% !important;
        max-width: 550px !important;
        height: 74px !important;
        background-color: #ffffff !important;
        box-shadow: 0 -4px 15px rgba(0,0,0,0.1) !important;
        z-index: 999999 !important;
        display: flex !important;
        justify-content: space-around !important;
        align-items: center !important;
        border-top: 1px solid #e2e8f0 !important;
        direction: ltr !important;
    }
    .nav-tab-item {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-decoration: none !important;
        color: #94a3b8 !important;
        font-size: 10px !important;
        font-weight: 700 !important;
        flex: 1 !important;
        padding: 6px 0 !important;
    }
    .nav-tab-item.active-tab {
        color: #ea580c !important;
    }
    .nav-tab-icon {
        font-size: 23px !important;
        margin-bottom: 4px !important;
    }
</style>
""", unsafe_allow_html=True)

# تغییر تعداد ستون‌ها به ۴ جهت باز شدن فضا در موبایل
cols = st.columns(4)

# لیست جدید با ۴ تب درخواستی شما
tab_list = [
    ("dashboard", "📊", "داشبورد"),
    ("invoice", "🧾", "پیش‌فاکتور"),
    ("top_sunify", "✨", "تاپسانیفای"),
    ("profile", "👤", "پروفایل")
]

for i, (tab_id, icon, label) in enumerate(tab_list):
    with cols[i]:
        is_active = st.session_state.active_tab == tab_id
        
        # در صورتی که این تب فعال باشد، دکمه را داخل کلاس اکتیو می‌گذاریم تا رنگش نارنجی شود
        if is_active:
            st.markdown('<div class="active-tab-button">', unsafe_allow_html=True)
            
        if st.button(f"{icon}\n{label}", key=f"nav_{tab_id}", 
                     use_container_width=True,
                     help=label):
            st.session_state.active_tab = tab_id
            st.query_params["nav_tab"] = tab_id
            st.rerun()
            
        if is_active:
            st.markdown('</div>', unsafe_allow_html=True)

# CSS اضافی برای زیباتر کردن دکمه‌ها و اعمال رنگ نارنجی به تب فعال
st.markdown("""
<style>
    div[data-testid="stButton"] button {
        background: transparent !important;
        border: none !important;
        color: #94a3b8 !important; /* رنگ خاکستری دکمه‌های غیرفعال */
        font-size: 11px !important;
        font-weight: 700 !important;
        height: 68px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 4px 0 !important;
        white-space: pre-line !important;
    }
    div[data-testid="stButton"] button:hover {
        background: rgba(234, 88, 12, 0.08) !important;
        color: #ea580c !important;
    }
    
    /* افکت تغییر رنگ قطعی دکمه‌ی فعال به نارنجی تاپسان */
    div.active-tab-button button {
        color: #ea580c !important;
    }
    div.active-tab-button button p {
        color: #ea580c !important;
        font-weight: 800 !important;
    }
</style>
""", unsafe_allow_html=True)
