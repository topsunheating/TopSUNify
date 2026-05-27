import streamlit as st

# ====================== ۱. تنظیمات بومی صفحه و هویت بصری ======================
# این بخش باید قطعاً و بدون هیچ استثنایی، اولین خط اجرایی در کل فایل پایتون باشد
st.set_page_config(
    page_title="TopSUNify",
    page_icon="./static/logo.png", # آیکون اختصاصی در تب مرورگر
    layout="wide"
)

# اضافه کردن لوگو به بالای منوی سمت چپ (Sidebar)
st.logo("./static/logo.png", link="https://topsunify-gshdpz3qnjc3itl8ukrxfq.streamlit.app")

# ====================== ۲. ایمپورت سایر کتابخانه‌ها و ماژول‌ها ======================
import Financial
import main
import os
import base64
import jdatetime  # جایگزین شدن کتابخانه تاریخ میلادی با تاریخ شمسی
import ezdxf
import tempfile
from PIL import Image
from Financial import calculate_tosunify_proforma, generate_proforma_pdf

# ====================== ۳. فونت و استایل سفارشی ======================
def inject_custom_css():
    font_path = "pinar-regular.ttf"
    font_base64 = ""

    if os.path.exists(font_path):
        with open(font_path, "rb") as f:
            font_base64 = base64.b64encode(f.read()).decode()

    css = f"""
    <style>
    @font-face {{
        font-family: 'pinar';
        src: url(data:font/ttf;base64,{font_base64}) format('truetype');
    }}

    html, body, [class*="css"], * {{
        font-family: 'pinar', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }}

    /* ================= FILE UPLOAD ================= */
    [data-testid="stFileUploadDropzone"],
    [data-testid="stFileUploaderDropzone"] {{
        border: 2px dashed #e2e8f0 !important;
        border-radius: 24px !important;
        background-color: #f8fafc !important;
        padding: 70px 10px 50px 10px !important;
        position: relative !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    [data-testid="stFileUploadDropzone"] small {{
        display: none !important;
    }}

    [data-testid="stFileUploadDropzone"]::before,
    [data-testid="stFileUploaderDropzone"]::before {{
        content: "فایل DWG یا DXF را انتخاب کنید";
        position: absolute;
        top: 25px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 15px;
        color: #374151;
        font-weight: bold;
        width: 100%;
        text-align: center;
    }}

    [data-testid="stFileUploaderFileName"] ~ section button {{
        display: none !important;
    }}

    [data-testid="stFileUploadDropzone"] button,
    [data-testid="stFileUploaderDropzone"] button {{
        background-color: #ea580c !important;
        border: none !important;
        border-radius: 9999px !important;
        padding: 12px 45px !important;
        position: relative !important;
        font-size: 0px !important;
        color: transparent !important;
        display: block !important;
        margin: 0 auto !important;
    }}

    [data-testid="stFileUploadDropzone"] button::after,
    [data-testid="stFileUploaderDropzone"] button::after {{
        content: "بارگذاری";
        font-size: 14px !important;
        color: white !important;
        font-family: 'pinar', sans-serif !important;
        position: absolute !important;
        left: 50% !important;
        top: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: 100% !important;
        text-align: center !important;
        pointer-events: none;
    }}

    [data-testid="stFileUploaderFileName"] {{
        color: #111827 !important;
        font-size: 13px !important;
        margin-top: 15px !important;
        text-align: center !important;
        display: block !important;
    }}

    [data-testid="stFileUploaderDeleteBtn"] {{
        background: #ef4444 !important;
        color: white !important;
        border-radius: 50% !important;
    }}

    [data-testid="stFileUploadDropzone"] p,
    [data-testid="stFileUploadDropzone"] label {{
        color: transparent !important;
        font-size: 0px !important;
        display: none !important;
    }}

    .stExpander summary {{ display: none !important; }}

    [data-testid="InputInstructions"],
    [class*="StyledInputInstructions"] {{
        display: none !important;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        background-color: #e2e8f0;
        padding: 4px;
        border-radius: 16px;
    }}

    .stTabs [data-baseweb="tab"] {{
        flex: 1;
        background-color: transparent;
        border-radius: 12px;
        color: #4b5563;
        font-weight: bold;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: #ea580c !important;
        color: white !important;
    }}

    [data-testid="column"] {{
        padding: 22px 26px !important;
    }}

    .stColumns {{
        gap: 20px !important;
    }}

    div[data-testid="stCheckbox"] {{
        margin-top: 14px !important;
        margin-bottom: 18px !important;
    }}

    div[data-testid="stCheckbox"] > label {{
        display: flex !important;
        align-items: center !important;
        gap: 14px !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# اجرای استایل‌ها
inject_custom_css()

# هدر برنامه
col_logo, col_title = st.columns([0.9, 5])
with col_logo:
    try: st.image("./static/logo.png", width=90)
    except: st.write("☀️")
with col_title:
    st.markdown("<h1 style='margin:0;'>TopSUNify</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='margin:0; color:#555;'>تحلیل هوشمند پلان و صدور پیش‌فاکتور</h5>", unsafe_allow_html=True)

st.divider()

# مدیریت وضعیت جهانی (Session State)
if "manual_rooms" not in st.session_state: st.session_state.manual_rooms = []
if "show_table" not in st.session_state: st.session_state.show_table = False
if "final_res" not in st.session_state: st.session_state.final_res = {}
if "m80" not in st.session_state: st.session_state.m80 = 0.0
if "m40" not in st.session_state: st.session_state.m40 = 0.0
if "xps" not in st.session_state: st.session_state.xps = 0.0
if "thermostat_count" not in st.session_state: st.session_state.thermostat_count = 1
if "panel_count" not in st.session_state: st.session_state.panel_count = 1
if "source_type" not in st.session_state: st.session_state.source_type = ""

# ==================== تب‌بندی ورودی اطلاعات ====================
tab_file, tab_room_manual, tab_invoice_manual = st.tabs([
    "📂 آپلود فایل پلان (DXF/DWG)", 
    "⌨️ ورود دستی ابعاد اتاق‌ها",
    "✍️ ورود مستقیم اقلام پیش‌فاکتور"
])

# --- سناریو ۱ - تب اول: آپلود فایل اتوکد ---
with tab_file:
    st.markdown("<h4 style='color:#334155; margin-bottom:15px;'>فایل نقشه اتوکد کف (DXF / DWG) را انتخاب کنید:</h4>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(label="", type=['dxf', 'dwg'], key="uploader_main", label_visibility="collapsed")
  
    if uploaded_file is not None:
        file_size_mb = uploaded_file.size / (1024 * 1024)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_file_info, col_file_del = st.columns()
        with col_file_info:
            st.success(f"✅ فایل بارگذاری شد: {uploaded_file.name} ({file_size_mb:.1f} مگابایت)")
        with col_file_del:
            if st.button("🗑️ حذف فایل", key="del_uploader_main", use_container_width=True):
                st.session_state["uploader_main"] = None
                if 'last_processed_file' in st.session_state:
                    del st.session_state['last_processed_file']
                if 'tmp_file_path' in st.session_state:
                    try:
                        if os.path.exists(st.session_state['tmp_file_path']):
                            os.remove(st.session_state['tmp_file_path'])
                    except: pass
                    del st.session_state['tmp_file_path']
                st.session_state.show_table = False
                st.rerun()

        file_id = f"{uploaded_file.name}_{uploaded_file.size}"
       
        if st.session_state.get('last_processed_file') != file_id:
            try:
                with st.spinner("در حال ارسال فایل به موتور تحلیل مهندسی (FastAPI)..."):
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
                  
                    st.success(f"✅ تحلیل موفقیت‌آمیز نقشه اتوکد صورت گرفت.")
                    st.rerun()
            except Exception as e:
                st.error(f"خطا در پردازش فایل مهندسی: {e}")

# --- سناریو ۱ - تب دوم: ورود دستی ابعاد اتاق‌ها ---
with tab_room_manual:
    with st.expander("➕ افزودن اتاق جدید", expanded=True):
        c_name, c_w, c_l = st.columns(3)
        r_name = c_name.text_input("نام فضا", value="پذیرایی", key="manual_r_name")
        r_w = c_w.number_input("عرض (متر)", min_value=0.0, step=0.1, value=4.0, key="manual_r_w")
        r_l = c_l.number_input("طول (متر)", min_value=0.0, step=0.1, value=5.0, key="manual_r_l")
        
        if st.button("➕ اضافه کردن به لیست", key="add_room_action", use_container_width=True):
            if r_w > 0 and r_l > 0:
                st.session_state.manual_rooms.append({
                    "name": r_name or f"فضا {len(st.session_state.manual_rooms)+1}",
                    "w": r_w, 
                    "l": r_l
                })
                st.session_state.source_type = "manual"
                st.session_state.show_table = True
                st.rerun()

    if st.session_state.manual_rooms:
        st.write("### 📋 لیست فضاهای ثبت شده:")
        
        cols = st.columns(3)
        for i, room in enumerate(st.session_state.manual_rooms):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"**{room['name']}**")
                    st.write(f"عرض: **{room['w']}** متر")
                    st.write(f"طول: **{room['l']}** متر")
                    st.write(f"مساحت: **{room['w'] * room['l']:.1f}** مترمربع")
                    
                    if st.button("🗑️ حذف", key=f"delete_room_{i}", use_container_width=True):
                        st.session_state.manual_rooms.pop(i)
                        if not st.session_state.manual_rooms:
                            st.session_state.show_table = False
                        st.rerun()
        
        col_clear = st.columns()
        with col_clear:
            if st.button("🗑️ پاک کردن همه اتاق‌ها", use_container_width=True):
                st.session_state.manual_rooms = []
                st.session_state.show_table = False
                st.rerun()
    else:
        st.info("هنوز هیچ اتاقی اضافه نشده است. از بخش بالا اتاق اضافه کنید.")

# --- سناریو ۲ - تب سوم: ورود مستقیم اقلام پیش‌فاکتور ---
with tab_invoice_manual:
    st.write("### 📝 ورود مستقیم مقادیر فاکتور (بدون تحلیل فنی)")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        m80_dir = st.number_input("متراژ فیلم گرمایشی عرض 80 سانتی‌متر (متر)", min_value=0.0, step=0.5, format="%.2f", key="invoice_m80")
        m40_dir = st.number_input("متراژ فیلم گرمایشی عرض 40 سانتی‌متر (متر)", min_value=0.0, step=0.5, format="%.2f", key="invoice_m40")
        insulation_dir = st.number_input("متراژ عایق (متر مربع)", min_value=0.0, step=0.5, format="%.2f", key="invoice_insulation")
        
    with col_m2:
        thermostat_dir = st.number_input("تعداد ترموستات (عدد)", min_value=0, step=1, key="invoice_thermostat")
        panel_dir = st.number_input("تعداد تابلو فرمان (عدد)", min_value=0, step=1, key="invoice_panel")
        
    if st.button("💾 تایید و ثبت مقادیر دستی فاکتور", key="submit_invoice_manual"):
        if m80_dir == 0 and m40_dir == 0 and insulation_dir == 0 and thermostat_dir == 0 and panel_dir == 0:
            st.warning("⚠️ لطفا حداقل مقدار یکی از اقلام را وارد کنید.")
        else:
            st.session_state.m80 = m80_dir
            st.session_state.m40 = m40_dir
            st.session_state.xps = insulation_dir
            st.session_state.thermostat_count = thermostat_dir
            st.session_state.panel_count = panel_dir
            
            st.session_state.source_type = "direct_invoice"
            st.session_state.show_table = True
            st.success("✅ مقادیر مستقیم با موفقیت ثبت شد. جدول زیر بروزرسانی گردید.")
            st.rerun()


# ====================== تنظیمات فروش، اجرا و تاریخ ======================
st.write("### ⚙️ تنظیمات فروش و زمان‌ب بندی")
col1, col2, col3 = st.columns(3)

with col1:
    enable_inst = st.checkbox("هزینه نصب و اجرا", value=False, key="enable_inst_widget")
    inst_rate = 15
    if enable_inst:
        inst_rate = st.number_input("درصد نصب", min_value=0, max_value=100, value=15, step=1, key="inst_rate_val")

with col2:
    enable_tax = st.checkbox("محاسبه مالیات", value=False, key="enable_tax_widget")
    tax_rate = 10
    if enable_tax:
        tax_rate = st.number_input("درصد مالیات", min_value=0, max_value=100, value=10, step=1, key="tax_rate_val")

with col3:
    enable_disc = st.checkbox("اعمال تخفیف", value=False, key="enable_disc_widget")
    disc = 0
    if enable_disc:
        disc = st.number_input("درصد تخفیف همکاری", min_value=0, max_value=100, value=0, step=1, key="disc_val")


# ====================== تنظیمات زمان‌بندی محاسباتی شمسی ======================
DUE_DAYS_DELTA = 3

col_date1, col_date2 = st.columns(2)
with col_date1:
    invoice_date = jdatetime.date.today()
    invoice_date_str = invoice_date.strftime("%Y/%m/%d")
    st.info(f"🗓️ تاریخ: {invoice_date_str}")

with col_date2:
    due_date = invoice_date + jdatetime.timedelta(days=DUE_DAYS_DELTA)
    due_date_str = due_date.strftime("%Y/%m/%d")
    st.info(f"📅 تاریخ سررسید: {due_date_str}")

st.markdown("<br>", unsafe_allow_html=True)


# ====================== موتور محاسبات مالی نهایی ======================
if st.session_state.get("show_table", False):
    if st.session_state.get("source_type") == "manual":
        total_area = sum(r['w'] * r['l'] for r in st.session_state.get("manual_rooms", []))
        st.session_state.m80 = round(total_area * 0.75, 1)
        st.session_state.m40 = round(total_area * 0.15, 1)
        st.session_state.xps = round(total_area * 1.1, 1)
        st.session_state.thermostat_count = len(st.session_state.get('manual_rooms', [])) or 1
        st.session_state.panel_count = 1

    try:
        final_inst = inst_rate if enable_inst else 0
        final_tax = tax_rate if enable_tax else 0
        final_disc = disc if enable_disc else 0

        current_m80 = st.session_state.get('m80', 0.0)
        current_m40 = st.session_state.get('m40', 0.0)
        current_thermostats = st.session_state.get('thermostat_count', 0)
        
        if st.session_state.get("source_type") == "direct_invoice":
            p_count = st.session_state.get('panel_count', 0)
        else:
            p_count = 1 if (current_m80 > 0 or current_m40 > 0) else 0

        res = calculate_tosunify_proforma(
            current_m80, current_m40, final_inst, final_disc, final_tax, current_thermostats
        )

        res['m80_total'] = current_m80 * res.get('UnitPrice_m80', 17900000)
        res['m40_total'] = current_m40 * res.get('UnitPrice_m40', 13350000)
        res['thermostat_total'] = current_thermostats * res.get('UnitPrice_thermostat', 3536000)
        
        if p_count == 0:
            res['ControlPanel_Total'] = 0
            res['UnitPrice_panel'] = 0
        else:
            res['ControlPanel_Total'] = p_count * res.get('UnitPrice_panel', 88950000)

        if current_m80 == 0 and current_m40 == 0 and st.session_state.get('xps', 0.0) == 0:
            res['insulation_roll_total'] = 0
            res['insulation_meter_total'] = 0
            res['insulation_total'] = 0
            res['xps_total'] = 0
            res['full_rolls_count'] = 0
            res['rem_meters_count'] = 0

        res['Items_Subtotal'] = res['m80_total'] + res['m40_total'] + res['insulation_total'] + res['thermostat_total'] + res['ControlPanel_Total']

        res['Installation_Cost'] = res['Items_Subtotal'] * (final_inst / 100)
        res['Discount_Amount'] = (res['Items_Subtotal'] + res['Installation_Cost']) * (final_disc / 100)
        
        before_tax = res['Items_Subtotal'] + res['Installation_Cost'] - res['Discount_Amount']
        res['Tax_Amount'] = before_tax * (final_tax / 100)
        res['Final_Amount'] = before_tax + res['Tax_Amount']
        
        res['Invoice_Date'] = invoice_date_str
        res['Due_Date'] = due_date_str
        
        st.session_state.final_res = res

    except Exception as e:
        st.error(f"خطا در محاسبات مالی هسته سیستم: {e}")

# ====================== نمایش خروجی پیش‌فاکتور ======================
if st.session_state.get("show_table", False) and "final_res" in st.session_state:
    res = st.session_state.final_res
    st.divider()
    st.subheader("🧾 پیش‌فاکتور نهایی پروژه")
    
    q_m80 = st.session_state.get('m80', 0.0)
    q_m40 = st.session_state.get('m40', 0.0)
    q_xps = st.session_state.get('xps', 0.0)
    t_count = st.session_state.get('thermostat_count', 0)
    
    if st.session_state.get("source_type") == "direct_invoice":
        p_count = st.session_state.get('panel_count', 0)
    else:
        p_count = 1 if (q_m80 > 0 or q_m40 > 0) else 0
    
    thermostat_title = "ترموستات کنترل دمای کف"
    panel_title = "تابلو فرمان" if t_count <= 1 else "تابلو فرمان مرکزی"
    
    table_data = []
    calculated_subtotal = 0

    if q_m80 > 0:
        row_total = q_m80 * res.get('UnitPrice_m80', 17900000)
        calculated_subtotal += row_total
        table_data.append([
            "گرمایش برقی تاپسان (عرض ۸۰ سانت)", f"{q_m80:.1f}", "متر", f"{res.get('UnitPrice_m80', 17900000):,.0f}", f"{row_total:,.0f}"
        ])
    
    if q_m40 > 0:
        row_total = q_m40 * res.get('UnitPrice_m40', 13350000)
        calculated_subtotal += row_total
        table_data.append([
            "گرمایش برقی تاپسان (عرض ۴۰ سانت)", f"{q_m40:.1f}", "متر", f"{res.get('UnitPrice_m40', 13350000):,.0f}", f"{row_total:,.0f}"
        ])
    
    if q_xps > 0:
        xps_unit = res.get('UnitPrice_insulation_meter', 1450000)
        xps_total = q_xps * xps_unit
        calculated_subtotal += xps_total
        table_data.append([
            "عایق بازتابشی AlumSUN", f"{q_xps:.1f}", "مترمربع", f"{xps_unit:,.0f}", f"{xps_total:,.0f}"
        ])
    
    if t_count > 0:
        row_total = t_count * res.get('UnitPrice_thermostat', 3536000)
        calculated_subtotal += row_total
        table_data.append([
            thermostat_title, str(t_count), "عدد", f"{res.get('UnitPrice_thermostat', 3536000):,.0f}", f"{row_total:,.0f}"
        ])
    
    if p_count > 0:
        row_total = p_count * res.get('UnitPrice_panel', 88950000)
        calculated_subtotal += row_total
        table_data.append([
            panel_title, str(p_count), "دستگاه", f"{res.get('UnitPrice_panel', 88950000):,.0f}", f"{row_total:,.0f}"
        ])
    
    f_inst_rate = inst_rate if enable_inst else 0
    f_disc_rate = disc if enable_disc else 0
    f_tax_rate = tax_rate if enable_tax else 0

    inst_val = calculated_subtotal * (f_inst_rate / 100)
    disc_val = (calculated_subtotal + inst_val) * (f_disc_rate / 100)
    before_tax = calculated_subtotal + inst_val - disc_val
    tax_val = before_tax * (f_tax_rate / 100)
    final_val = before_tax + tax_val

    if enable_inst and inst_val > 0:
        table_data.append([f"هزینه نصب و اجرا ({inst_rate}٪)", "&nbsp;", "&nbsp;", "&nbsp;", f"{inst_val:,.0f}"])
    
    if enable_disc and disc_val > 0:
        table_data.append([f"تخفیف همکاری ({disc}٪)", "&nbsp;", "&nbsp;", "&nbsp;", f" {disc_val:,.0f} -"])
    
    if enable_tax and tax_val > 0:
        table_data.append([f"مالیات ارزش افزوده ({tax_rate}٪)", "&nbsp;", "&nbsp;", "&nbsp;", f"{tax_val:,.0f}"])

    res['Items_Subtotal'] = calculated_subtotal
    res['Installation_Cost'] = inst_val
    res['Discount_Amount'] = disc_val
    res['Tax_Amount'] = tax_val
    res['Final_Amount'] = final_val
    st.session_state.final_res = res

    if table_data:
        import pandas as pd
        
        df_display = pd.DataFrame(
            table_data, 
            columns=["شرح کالا", "مقدار", "واحد", "قیمت واحد (ریال)", "مبلغ کل (ریال)"]
        )
                    
        st.markdown("""
            <style>
                div[data-testid="stTable"] {
                    border: 1.5px solid #000000 !important;
                    border-radius: 4px !important;
                    overflow: hidden !important;
                    box-shadow: none !important;
                    background-color: #ffffff !important;
                }
                
                div[data-testid="stBlock"] [data-testid="stElementContainer"],
                div[data-testid="stElementContainer"] {
                    background-color: transparent !important;
                    box-shadow: none !important;
                }

                div[data-testid="stTable"] table {
                    border-collapse: collapse !important;
                    border: none !important;
                    width: 100% !important;
                    background-color: #ffffff !important;
                }
                
                div[data-testid="stTable"] th, div[data-testid="stTable"] td {
                    border: 1px solid #000000 !important;
                    text-align: center !important;
                    vertical-align: middle !important;
                    padding: 0px 6px !important;
                    height: 38px !important;     
                    max-height: 38px !important;
                    line-height: 38px !important;  
                    box-sizing: border-box !important;
                }
                
                div[data-testid="stTable"] td:first-child {
                    text-align: right !important;
                    padding-right: 15px !important;
                }
                
                div[data-testid="stTable"] th {
                    text-align: center !important;
                    background-color: #ffffff !important;
                    line-height: normal !important;
                    padding: 8px 6px !important;
                }
            </style>
        """, unsafe_allow_html=True)
        
        st.table(df_display)
        st.success(f"**مبلغ نهایی قابل پرداخت: {final_val:,.0f} ریال**")
    else:
        st.warning("هیچ مقداری وارد نشده است.")


    # ====================== دکمه‌های دانلود PDF ======================
    st.markdown("<br>", unsafe_allow_html=True)
    col_dl1, col_dl2 = st.columns(2)

    with col_dl1:
        try:
            pdf_res = st.session_state.final_res.copy()
            pdf_res['Invoice_Date'] = invoice_date_str
            pdf_res['Due_Date'] = due_date_str

            pdf_bytes = generate_proforma_pdf(
                pdf_res,
                st.session_state.get("m80", 0.0),
                st.session_state.get("m40", 0.0),
                st.session_state.get("xps", 0.0),
                st.session_state.get('thermostat_count', 0),
                p_count
            )

            st.download_button(
                label="📥 دریافت فایل پیش‌فاکتور",
                data=pdf_bytes,
                file_name="TopSUNify_Official_Proforma.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="download_proforma"
            )
        except Exception as e:
            st.warning(f"دکمه دانلود آماده نیست. دلیل: {e}")
            
    with col_dl2:
        if st.button("🗺️ مشاهده نقشه چیدمان", use_container_width=True):
            source = st.session_state.get("source_type")
            
            if source == "file":
                tmp_path = st.session_state.get('tmp_file_path')
                if not tmp_path or not os.path.exists(tmp_path):
                    st.warning("⚠️ فایل نقشه یافت نشد. لطفا دوباره فایل را آپلود کنید.")
                else:
                    try:
                        with st.spinner("در حال تولید نقشه چیدمان..."):
                            layout_pdf_bytes = main.generate_layout_plan(tmp_path)
                        st.success("✅ نقشه چیدمان کامل تولید شد")
                        st.download_button(
                            label="📥 دانلود PDF نقشه چیدمان تفکیکی",
                            data=layout_pdf_bytes,
                            file_name="TopSUNify_Layout_Plan.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            key="download_layout_file"
                        )
                    except Exception as e:
                        st.error(f"خطا در تولید نقشه: {e}")

            elif source == "manual" and st.session_state.get("manual_rooms"):
                try:
                    with st.spinner("در حال تولید نقشه چیدمان..."):
                        temp_dxf = tempfile.NamedTemporaryFile(delete=False, suffix=".dxf")
                        temp_dxf.close()
                        
                        doc = ezdxf.new('R2010')
                        msp = doc.modelspace()
                        
                        for idx, room in enumerate(st.session_state.manual_rooms):
                            w = float(room['w'])
                            l = float(room['l'])
                            name = room.get('name', f"فضا {idx+1}")
                            
                            pline = msp.add_lwpolyline(
                                [(0,0), (w,0), (w,l), (0,l), (0,0)],
                                format='xy'
                            )
                            pline.dxf.layer = "0"
                            pline.dxf.color = 1
                            pline.closed = True
                            
                            msp.add_text(name, dxfattribs={
                                'insert': (w/2, l + 0.4),
                                'height': 0.25,
                                'layer': 'TEXT'
                            })
                        
                        doc.saveas(temp_dxf.name)
                        layout_pdf_bytes = main.generate_layout_plan(temp_dxf.name, include_overall=False)
                        
                        try: os.remove(temp_dxf.name)
                        except: pass
                        
                    st.success("✅ نقشه چیدمان کامل تولید شد")
                    st.download_button(
                        label="📥 دانلود PDF نقشه چیدمان تفکیکی",
                        data=layout_pdf_bytes,
                        file_name="TopSUNify_Layout_Plan.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        key="download_layout_manual"
                    )
                except Exception as e:
                    st.error(f"خطا در تولید نقشه: {str(e)}")
            else:
                st.warning("⚠️ ابتدا اتاق اضافه کنید یا فایل آپلود کنید.")
