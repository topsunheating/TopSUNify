import streamlit as st

# 🛑 دستور set_page_config حتماً باید در بالاترین خط برنامه باقی بماند
st.set_page_config(
    page_title="TopSUNify",
    page_icon="./topsunify.png",  # استفاده از لوگوی اصلی تاپسان
    layout="wide"
)

# ====================== ۱. مدیریت وضعیت جهانی سیستم (Session State) ======================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "manual_rooms" not in st.session_state: st.session_state.manual_rooms = []
if "show_table" not in st.session_state: st.session_state.show_table = False
if "final_res" not in st.session_state: st.session_state.final_res = {}
if "m80" not in st.session_state: st.session_state.m80 = 0.0
if "m40" not in st.session_state: st.session_state.m40 = 0.0
if "xps" not in st.session_state: st.session_state.xps = 0.0
if "thermostat_count" not in st.session_state: st.session_state.thermostat_count = 1
if "panel_count" not in st.session_state: st.session_state.panel_count = 1
if "source_type" not in st.session_state: st.session_state.source_type = ""

# متغیرهای بخش پروفایل کاربری
if "user_display_name" not in st.session_state: st.session_state.user_display_name = "رضا تلچی"
if "user_phone" not in st.session_state: st.session_state.user_phone = "۰۹۱۲۰۱۹۸۲۲۹"
if "user_role" not in st.session_state: st.session_state.user_role = "کاربر عمومی" 
if "profile_pic_base64" not in st.session_state: st.session_state.profile_pic_base64 = ""

# ====================== ۲. بررسی احراز هویت قوی ======================
import auth

if not st.session_state.logged_in:
    auth.render_auth_page()
    st.stop()

# ====================== ۳. ایمپورت کتابخانه‌ها و ماژول‌های مهندسی ======================
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


# ====================== ۴. هوشمندسازی CSS با فونت ایران‌یکان و ظاهر نیتیو ======================
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

    .main .block-container {{
        max-width: 550px !important;
        margin: 0 auto !important;
        padding-left: 16px !important;
        padding-right: 16px !important;
        padding-bottom: 110px !important;
        background-color: #f8fafc !important;
        min-height: 100vh;
    }}

    .app-main-header-container {{
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        padding: 10px 0 !important;
        margin-bottom: 5px !important;
    }}

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
        background-color: #fef3c7 !important;
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

    .module-card-box {{
        background: #ffffff !important;
        padding: 20px !important;
        border-radius: 24px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04) !important;
        margin-bottom: 20px !important;
    }}

    /* استایل‌های اختصاصی بخش پروفایل کاربری */
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

    .profile-menu-item {{
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        padding: 16px 8px !important;
        border-bottom: 1px solid #f1f5f9 !important;
        text-decoration: none !important;
        color: #334155 !important;
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
        color: #ea580c !important;
    }}

    .nav-tab-icon {{
        font-size: 20px !important;
        margin-bottom: 3px !important;
    }}

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

# ====================== ۵. هدر بالایی اختصاصی (لوگوی تصویری) ======================
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
    header_logo_html = '<div class="app-main-header-container" style="font-size:24px;">☀️</div>'

st.markdown(header_logo_html, unsafe_allow_html=True)
st.divider()


# ==============================================================================
# رندر کردن محتوای صفحات بر اساس تب فعال
# ==============================================================================

# ------------------------------------------------------------------------------
# ۱. محتوای تب: داشبورد
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
# ۶. محتوای تب اختصاصی: پروفایل کاربری
# ------------------------------------------------------------------------------
elif st.session_state.active_tab == "profile":
    
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
    
    role_badge_html = f"""
    <div class="profile-role-badge-box">
        <div class="profile-role-title">سطح دسترسی حساب:</div>
        <div class="profile-role-value">{st.session_state.user_role}</div>
    </div>
    """
    st.markdown(role_badge_html, unsafe_allow_html=True)
    
    # منوی تنظیمات ادمین و تغییرات پروفایل
    with st.expander("⚙️ تنظیمات کاربری و سطح دسترسی حساب"):
        uploaded_avatar = st.file_uploader("انتخاب یا تغییر عکس پروفایل:", type=["jpg", "png", "jpeg"], key="avatar_uploader_input")
        if uploaded_avatar is not None:
            st.session_state.profile_pic_base64 = base64.b64encode(uploaded_avatar.getvalue()).decode()
            st.toast("📷 عکس پروفایل با موفقیت تغییر یافت.")
            st.rerun()
            
        selected_role_test = st.selectbox(
            "تعیین سطح دسترسی حساب:",
            ["کاربر عمومی", "مدیر", "مدیر فروش", "مدیر فنی", "مدیر خدمات", "کارشناس فروش", "نمایندگی", "عاملیت"],
            index=["کاربر عمومی", "مدیر", "مدیر فروش", "مدیر فنی", "مدیر خدمات", "کارشناس فروش", "نمایندگی", "عاملیت"].index(st.session_state.user_role)
        )
        if selected_role_test != st.session_state.user_role:
            st.session_state.user_role = selected_role_test
            st.rerun()

    # گرید لیست گزینه‌های درخواستی شما
    st.markdown('<div class="module-card-box" style="padding: 10px 15px !important;">', unsafe_allow_html=True)
    
    menu_items = [
        {"label": "فاکتورهای تکمیل شده", "icon": "✅"},
        {"label": "فاکتورهای باز", "icon": "⏳"},
        {"label": "پیش فاکتورها", "icon": "🧾"},
        {"label": "مشتریانی منتخب", "icon": "⭐"},
        {"label": "اعلام موجودی انبار", "icon": "📦"},
        {"label": "تنظیمات", "icon": "⚙️"},
    ]
    
    for item in menu_items:
        item_html = f"""
        <div class="profile-menu-item">
            <div class="profile-menu-right">
                <span class="profile-menu-icon">{item['icon']}</span>
                <span>{item['label']}</span>
            </div>
            <div class="profile-menu-arrow">◀</div>
        </div>
        """
        st.markdown(item_html, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🚪 خروج از حساب کاربری تاپسان", use_container_width=True):
        st.session_state.logged_in = False
        st.query_params.clear()
        st.rerun()


# ==============================================================================
# ناوبری نهایی چسبیده به پایین صفحه با ۶ تب متوازن (Bottom Navigation Bar)
# ==============================================================================
active_dashboard = "active-tab" if st.session_state.active_tab == "dashboard" else ""
active_invoice = "active-tab" if st.session_state.active_tab == "invoice" else ""
active_warranty = "active-tab" if st.session_state.active_tab == "warranty" else ""
active_services = "active-tab" if st.session_state.active_tab == "services" else ""
active_info = "active-tab" if st.session_state.active_tab == "info" else ""
active_profile = "active-tab" if st.session_state.active_tab == "profile" else ""

bottom_navigation_html = f"""
<div class="fixed-bottom-nav">
    <a href="?nav_tab=profile" target="_self" class="nav-tab-item {active_profile}">
        <div class="nav-tab-icon">👤</div>
        <div>پروفایل</div>
    </a>
    <a href="?nav_tab=info" target="_self" class="nav-tab-item {active_info}">
        <div class="nav-tab-icon">📚</div>
        <div>اطلاعات</div>
    </a>
    <a href="?nav_tab=services" target="_self" class="nav-tab-item {active_services}">
        <div class="nav-tab-icon">🛠️</div>
        <div>خدمات</div>
    </a>
    <a href="?nav_tab=warranty" target="_self" class="nav-tab-item {active_warranty}">
        <div class="nav-tab-icon">🛡️</div>
        <div>گارانتی</div>
    </a>
    <a href="?nav_tab=invoice" target="_self" class="nav-tab-item {active_invoice}">
        <div class="nav-tab-icon">🧾</div>
        <div>پیش‌فاکتور</div>
    </a>
    <a href="?nav_tab=dashboard" target="_self" class="nav-tab-item {active_dashboard}">
        <div class="nav-tab-icon">📊</div>
        <div>داشبورد</div>
    </a>
</div>
"""
st.html(bottom_navigation_html)
