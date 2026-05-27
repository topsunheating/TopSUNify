import streamlit as st

# 🛑 دستور set_page_config حتماً باید در بالاترین خط برنامه باقی بماند
st.set_page_config(
    page_title="TopSUNify | سامانه جامع خدمات و محاسبات",
    page_icon="./static/logo.png",
    layout="wide"
)

# ====================== ۱. اضافه کردن ماژول احراز هویت ======================
import auth

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# اگر کاربر لاگین نکرده بود، فرم ورود را نشان بده و بقیه کدها را متوقف کن
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

# ====================== ۳. فونت و استایل سفارشی موبایل و تب‌ها ======================
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

    /* ================= BOTTOM TABS NAVIGATION ================= */
    div[data-testid="stTabs"] {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #ffffff;
        box-shadow: 0 -4px 10px rgba(0,0,0,0.05);
        z-index: 99999;
        padding: 5px 10px;
        border-top: 1px solid #e2e8f0;
        direction: rtl !important;
    }}
    div[data-testid="stTabs"] button {{
        flex: 1;
        text-align: center;
        font-weight: bold !important;
        color: #64748b !important;
        font-size: 14px !important;
        padding: 10px 0 !important;
        background-color: transparent !important;
        border-radius: 12px !important;
    }}
    div[data-testid="stTabs"] button[aria-selected="true"] {{
        color: white !important;
        background-color: #ea580c !important;
        border-bottom: none !important;
    }}
    .main .block-container {{
        padding-bottom: 110px !important;
    }}

    /* ================= FILE UPLOAD ================= */
    [data-testid="stFileUploadDropzone"],
    [data-testid="stFileUploaderDropzone"] {{
        border: 2px dashed #ea580c !important;
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
        content: "بارگذاری قالب نقشه";
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

    [data-testid="column"] {{
        padding: 15px 20px !important;
    }}

    .stColumns {{
        gap: 15px !important;
    }}

    /* ================= TABLES ================= */
    div[data-testid="stTable"] {{
        border: 1.5px solid #000000 !important;
        border-radius: 4px !important;
        overflow: hidden !important;
        background-color: #ffffff !important;
    }}
    div[data-testid="stTable"] table {{
        border-collapse: collapse !important;
        border: none !important;
        width: 100% !important;
    }}
    div[data-testid="stTable"] th, div[data-testid="stTable"] td {{
        border: 1px solid #000000 !important;
        text-align: center !important;
        vertical-align: middle !important;
        padding: 0px 6px !important;
        height: 38px !important;     
    }}
    div[data-testid="stTable"] td:first-child {{
        text-align: right !important;
        padding-right: 15px !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

inject_custom_css()

# ====================== ۴. هدر بالایی برنامه ======================
col_logo, col_title = st.columns([0.9, 5])
with col_logo:
    try: st.image("./static/logo.png", width=85)
    except: st.write("☀️")
with col_title:
    st.markdown("<h2 style='margin:0;'>TopSUNify</h2>", unsafe_allow_html=True)
    st.markdown("<h6 style='margin:0; color:#64748b;'>سامانه هوشمند تحلیل پلان و خدمات جامع تاپسان</h6>", unsafe_allow_html=True)

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

# ====================== ۶. ساخت تب‌های اصلی پایین صفحه ======================
tab_info, tab_service, tab_warranty, tab_invoice = st.tabs([
    "📚 اطلاعات فنی", 
    "🛠️ خدمات فنی", 
    "🛡️ ثبت گارانتی", 
    "🧾 صدور پیش‌فاکتور"
])

# ==============================================================================
# تب اول: صدور پیش‌فاکتور (شامل موتور محاسباتی گرمایش کف)
# ==============================================================================
with tab_invoice:
    st.subheader("🧾 صدور پیش‌فاکتور هوشمند")
    
    product_type = st.selectbox(
        "نوع سیستم گرمایشی مورد نظر را انتخاب کنید:",
        ["گرمایش کف (سیستم هوشمند)", "زیرفرشی", "رادیاتور", "رستورانی", "عمومی"],
        key="selected_product_type"
    )
    st.write("---")

    # --- پیاده‌سازی هسته اصلی گرمایش کف در صورت انتخاب ---
    if product_type == "گرمایش کف (سیستم هوشمند)":
        
        # زیرتب‌های ورودی اطلاعات نقشه و فضاها
        tab_file, tab_room_manual, tab_invoice_manual = st.tabs([
            "📂 آپلود فایل پلان (DXF/DWG)", 
            "⌨️ ورود دستی ابعاد اتاق‌ها",
            "✍️ ورود مستقیم اقلام پیش‌فاکتور"
        ])

        # --- سناریو گرمایش کف: آپلود فایل اتوکد ---
        with tab_file:
            st.markdown("<h5 style='color:#334155; margin-bottom:15px;'>فایل نقشه اتوکد کف (DXF / DWG) را انتخاب کنید:</h5>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader(label="", type=['dxf', 'dwg'], key="uploader_main", label_visibility="collapsed")
          
            if uploaded_file is not None:
                file_size_mb = uploaded_file.size / (1024 * 1024)
                st.markdown("<br>", unsafe_allow_html=True)
                col_file_info, col_file_del = st.columns(3)
                with col_file_info:
                    st.success(f"✅ فایل بارگذاری شد: {uploaded_file.name} ({file_size_mb:.1f} مگابایت)")
                with col_file_del:
                    if st.button("🗑️ حذف فایل", key="del_uploader_main", use_container_width=True):
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
                          
                            st.success(f"✅ تحلیل موفقیت‌آمیز نقشه اتوکد صورت گرفت.")
                            st.rerun()
                    except Exception as e:
                        st.error(f"خطا در پردازش فایل مهندسی: {e}")

        # --- سناریو گرمایش کف: ورود دستی ابعاد اتاق‌ها ---
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
                            "w": r_w, "l": r_l
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
                            st.write(f"عرض: **{room['w']}** متر | طول: **{room['l']}** متر")
                            st.write(f"مساحت: **{room['w'] * room['l']:.1f}** مترمربع")
                            
                            if st.button("🗑️ حذف", key=f"delete_room_{i}", use_container_width=True):
                                st.session_state.manual_rooms.pop(i)
                                if not st.session_state.manual_rooms: st.session_state.show_table = False
                                st.rerun()
                
                if st.button("🗑️ پاک کردن همه اتاق‌ها"):
                    st.session_state.manual_rooms = []
                    st.session_state.show_table = False
                    st.rerun()
            else:
                st.info("هنوز هیچ اتاقی اضافه نشده است.")

        # --- سناریو گرمایش کف: ورود مستقیم اقلام فاکتور ---
        with tab_invoice_manual:
            st.write("### 📝 ورود مستقیم مقادیر فاکتور (بدون تحلیل فنی)")
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                m80_dir = st.number_input("متراژ فیلم عرض 80 سانتی‌متر (متر)", min_value=0.0, step=0.5, key="invoice_m80")
                m40_dir = st.number_input("متراژ فیلم عرض 40 سانتی‌متر (متر)", min_value=0.0, step=0.5, key="invoice_m40")
                insulation_dir = st.number_input("متراژ عایق (متر مربع)", min_value=0.0, step=0.5, key="invoice_insulation")
            with col_m2:
                thermostat_dir = st.number_input("تعداد ترموستات (عدد)", min_value=0, step=1, key="invoice_thermostat")
                panel_dir = st.number_input("تعداد تابلو فرمان (عدد)", min_value=0, step=1, key="invoice_panel")
                
            if st.button("💾 تایید و ثبت مقادیر دستی فاکتور", key="submit_invoice_manual"):
                if m80_dir == 0 and m40_dir == 0 and insulation_dir == 0 and thermostat_dir == 0 and panel_dir == 0:
                    st.warning("⚠️ لطفا حداقل مقدار یکی از اقلام را وارد کنید.")
                else:
                    st.session_state.m80 = m80_dir; st.session_state.m40 = m40_dir
                    st.session_state.xps = insulation_dir; st.session_state.thermostat_count = thermostat_dir
                    st.session_state.panel_count = panel_dir
                    st.session_state.source_type = "direct_invoice"
                    st.session_state.show_table = True
                    st.rerun()

        # --- تنظیمات فروش و زمان‌بندی صادر شدن مالی فاکتور گرمایش کف ---
        st.write("### ⚙️ تنظیمات فروش و زمان‌بندی")
        col1, col2, col3 = st.columns(3)
        with col1:
            enable_inst = st.checkbox("هزینه نصب و اجرا", value=False)
            inst_rate = st.number_input("درصد نصب", min_value=0, max_value=100, value=15) if enable_inst else 15
        with col2:
            enable_tax = st.checkbox("محاسبه مالیات", value=False)
            tax_rate = st.number_input("درصد مالیات", min_value=0, max_value=100, value=10) if enable_tax else 10
        with col3:
            enable_disc = st.checkbox("اعمال تخفیف", value=False)
            disc = st.number_input("درصد تخفیف همکاری", min_value=0, max_value=100, value=0) if enable_disc else 0

        # زمان‌بندی شمسی
        col_date1, col_date2 = st.columns(2)
        invoice_date_str = jdatetime.date.today().strftime("%Y/%m/%d")
        due_date_str = (jdatetime.date.today() + jdatetime.timedelta(days=3)).strftime("%Y/%m/%d")
        col_date1.info(f"🗓️ تاریخ: {invoice_date_str}")
        col_date2.info(f"📅 تاریخ سررسید: {due_date_str}")

        # --- پردازش و جدول خروجی محاسبات مالی پروژه گرمایش کف ---
        if st.session_state.get("show_table", False):
            if st.session_state.get("source_type") == "manual":
                total_area = sum(r['w'] * r['l'] for r in st.session_state.manual_rooms)
                st.session_state.m80 = round(total_area * 0.75, 1)
                st.session_state.m40 = round(total_area * 0.15, 1)
                st.session_state.xps = round(total_area * 1.1, 1)
                st.session_state.thermostat_count = len(st.session_state.manual_rooms) or 1
                st.session_state.panel_count = 1

            try:
                res = calculate_tosunify_proforma(
                    st.session_state.m80, st.session_state.m40, 
                    (inst_rate if enable_inst else 0), (disc if enable_disc else 0), 
                    (tax_rate if enable_tax else 0), st.session_state.thermostat_count
                )
                
                # اعمال مقادیر سطرها
                res['m80_total'] = st.session_state.m80 * res.get('UnitPrice_m80', 17900000)
                res['m40_total'] = st.session_state.m40 * res.get('UnitPrice_m40', 13350000)
                res['thermostat_total'] = st.session_state.thermostat_count * res.get('UnitPrice_thermostat', 3536000)
                
                p_count = st.session_state.panel_count if st.session_state.source_type == "direct_invoice" else (1 if (st.session_state.m80 > 0 or st.session_state.m40 > 0) else 0)
                res['ControlPanel_Total'] = p_count * res.get('UnitPrice_panel', 88950000) if p_count > 0 else 0

                calculated_subtotal = res['m80_total'] + res['m40_total'] + res['thermostat_total'] + res['ControlPanel_Total'] + (st.session_state.xps * res.get('UnitPrice_insulation_meter', 1450000) if st.session_state.xps > 0 else 0)
                
                inst_val = calculated_subtotal * ((inst_rate if enable_inst else 0) / 100)
                disc_val = (calculated_subtotal + inst_val) * ((disc if enable_disc else 0) / 100)
                before_tax = calculated_subtotal + inst_val - disc_val
                tax_val = before_tax * ((tax_rate if enable_tax else 0) / 100)
                final_val = before_tax + tax_val

                # ساخت ساختار نمایشی دیتابیس جدول
                table_data = []
                if st.session_state.m80 > 0: table_data.append(["گرمایش برقی تاپسان (عرض ۸۰ سانت)", f"{st.session_state.m80:.1f}", "متر", f"{res.get('UnitPrice_m80', 17900000):,.0f}", f"{res['m80_total']:,.0f}"])
                if st.session_state.m40 > 0: table_data.append(["گرمایش برقی تاپسان (عرض ۴۰ سانت)", f"{st.session_state.m40:.1f}", "متر", f"{res.get('UnitPrice_m40', 13350000):,.0f}", f"{res['m40_total']:,.0f}"])
                if st.session_state.xps > 0: table_data.append(["عایق بازتابشی AlumSUN", f"{st.session_state.xps:.1f}", "مترمربع", f"{res.get('UnitPrice_insulation_meter', 1450000):,.0f}", f"{(st.session_state.xps * res.get('UnitPrice_insulation_meter', 1450000)):,.0f}"])
                if st.session_state.thermostat_count > 0: table_data.append(["ترموستات کنترل دمای کف", str(st.session_state.thermostat_count), "عدد", f"{res.get('UnitPrice_thermostat', 3536000):,.0f}", f"{res['thermostat_total']:,.0f}"])
                if p_count > 0: table_data.append([("تابلو فرمان مرکزی" if st.session_state.thermostat_count > 1 else "تابلو فرمان"), str(p_count), "دستگاه", f"{res.get('UnitPrice_panel', 88950000):,.0f}", f"{res['ControlPanel_Total']:,.0f}"])
                
                if enable_inst and inst_val > 0: table_data.append([f"هزینه نصب و اجرا ({inst_rate}٪)", "&nbsp;", "&nbsp;", "&nbsp;", f"{inst_val:,.0f}"])
                if enable_disc and disc_val > 0: table_data.append([f"تخفیف همکاری ({disc}٪)", "&nbsp;", "&nbsp;", "&nbsp;", f" {disc_val:,.0f} -"])
                if enable_tax and tax_val > 0: table_data.append([f"مالیات ارزش افزوده ({tax_rate}٪)", "&nbsp;", "&nbsp;", "&nbsp;", f"{tax_val:,.0f}"])

                st.write("### 🧾 پیش‌فاکتور محاسباتی مهندسی:")
                st.table(pd.DataFrame(table_data, columns=["شرح کالا", "مقدار", "واحد", "قیمت واحد (ریال)", "مبلغ کل (ریال)"]))
                st.success(f"**مبلغ نهایی قابل پرداخت پروژه: {final_val:,.0f} ریال**")

                # بخش دانلود مستندات و دکمه چیدمان نقشه
                res.update({'Items_Subtotal': calculated_subtotal, 'Installation_Cost': inst_val, 'Discount_Amount': disc_val, 'Tax_Amount': tax_val, 'Final_Amount': final_val, 'Invoice_Date': invoice_date_str, 'Due_Date': due_date_str})
                st.session_state.final_res = res

                col_dl1, col_dl2 = st.columns(2)
                with col_dl1:
                    try:
                        pdf_bytes = generate_proforma_pdf(st.session_state.final_res, st.session_state.m80, st.session_state.m40, st.session_state.xps, st.session_state.thermostat_count, p_count)
                        st.download_button(label="📥 دریافت فایل رسمی PDF پیش‌فاکتور", data=pdf_bytes, file_name="TopSUNify_Official_Proforma.pdf", mime="application/pdf", use_container_width=True)
                    except Exception as e: st.warning(f"آماده‌سازی دکمه دانلود PDF خطایی دارد: {e}")
                
                with col_dl2:
                    if st.button("🗺️ تولید و دانلود نقشه چیدمان", use_container_width=True):
                        source = st.session_state.source_type
                        if source == "file" and st.session_state.get('tmp_file_path'):
                            layout_pdf_bytes = main.generate_layout_plan(st.session_state['tmp_file_path'])
                            st.download_button(label="📥 دانلود نقشه پلان چیدمان تفکیکی", data=layout_pdf_bytes, file_name="TopSUNify_Layout_Plan.pdf", mime="application/pdf", use_container_width=True)
                        elif source == "manual" and st.session_state.manual_rooms:
                            # ساخت فایل موقت DXF برای حالت دستی
                            temp_dxf = tempfile.NamedTemporaryFile(delete=False, suffix=".dxf")
                            temp_dxf.close()
                            doc = ezdxf.new('R2010'); msp = doc.modelspace()
                            for idx, room in enumerate(st.session_state.manual_rooms):
                                w = float(room['w']); l = float(room['l'])
                                pline = msp.add_lwpolyline([(0,0), (w,0), (w,l), (0,l), (0,0)], format='xy')
                                pline.closed = True
                                msp.add_text(room.get('name', f"فضا {idx+1}"), dxfattribs={'insert': (w/2, l + 0.4), 'height': 0.25})
                            doc.saveas(temp_dxf.name)
                            layout_pdf_bytes = main.generate_layout_plan(temp_dxf.name, include_overall=False)
                            try: os.remove(temp_dxf.name)
                            except: pass
                            st.download_button(label="📥 دانلود نقشه پلان چیدمان دستی", data=layout_pdf_bytes, file_name="TopSUNify_Manual_Layout.pdf", mime="application/pdf", use_container_width=True)
            except Exception as e:
                st.error(f"خطا در هسته محاسباتی: {e}")
    else:
        st.info(f"شما بخش **{product_type}** را انتخاب کرده‌اید. فرم‌ها و کاتالوگ‌های اختصاصی این بخش به زودی بارگذاری می‌شوند.")

# ==============================================================================
# تب دوم: ثبت گارانتی
# ==============================================================================
with tab_warranty:
    st.subheader("🛡️ فرم ثبت گارانتی محصولات")
    with st.form("warranty_form"):
        st.text_input("نام و نام خانوادگی خریدار")
        st.text_input("شماره سریال محصول (درج شده روی دستگاه)")
        st.file_uploader("آپلود عکس یا فیلم محصول نصب شده", type=["jpg", "png", "mp4", "mov"])
        st.file_uploader("آپلود عکس فاکتور خرید", type=["jpg", "png", "pdf"])
        if st.form_submit_button("ثبت و فعال‌سازی گارانتی"):
            st.success("✅ اطلاعات گارانتی با موفقیت در صف بررسی سیستم قرار گرفت.")

# ==============================================================================
# تب سوم: درخواست خدمات فنی
# ==============================================================================
with tab_service:
    st.subheader("🛠️ ثبت درخواست خدمات فنی")
    service_type = st.radio("نوع درخواست:", ["درخواست نصب و راه‌اندازی اولیه", "اعلام خرابی / درخواست تعمیرات", "درخواست جابجایی محصول"])
    with st.form("service_form"):
        st.text_area("توضیحات تکمیلی و آدرس محل پروژه")
        st.text_input("شماره تماس هماهنگی")
        if st.form_submit_button("ارسال درخواست به واحد پشتیبانی"):
            st.success(f"📌 درخواست '{service_type}' شما در سیستم ثبت شد.")

# ==============================================================================
# تب چهارم: اطلاعات فنی
# ==============================================================================
with tab_info:
    st.subheader("📚 بانک اطلاعات فنی و کاتالوگ‌ها")
    info_section = st.segmented_control("بخش مورد نظر:", ["کاتالوگ محصول", "عکس و فیلم پروژه‌ها", "فیلم‌های تبلیغاتی", "رزومه شرکت"], default="کاتالوگ محصول")
    st.markdown(f"### 📂 {info_section}")
    st.write("مستندات و فایل‌های دانلود مربوطه به زودی در اینجا قرار می‌گیرند.")
    
    st.write("<br><br>", unsafe_allow_html=True)
    if st.button("خروج از حساب کاربری", key="logout_btn"):
        st.session_state.logged_in = False
        st.rerun()
