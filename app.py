import streamlit as st

# 🛑 دستور set_page_config حتماً باید در بالاترین خط برنامه باقی بماند
st.set_page_config(
    page_title="TopSUNify | سامانه ریسپانسیو تاپسان",
    page_icon="./static/logo.png",
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

# ====================== ۳. هوشمندسازی CSS برای ریسپانسیو و تب‌های آیکونی ======================
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

    /* --- بهینه‌سازی کانتینر اصلی برای نمایش عالی در تبلت و موبایل --- */
    .main .block-container {{
        max-width: 100% !important;
        padding-left: 15px !important;
        padding-right: 15px !important;
        padding-bottom: 120px !important; /* فضا برای اینکه محتوا زیر منوی پایین نرود */
    }}

    /* --- سیستم نویگیشن چسبیده به پایین (Bottom Navigation) --- */
    div[data-testid="stTabs"] {{
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        background-color: #ffffff !important;
        box-shadow: 0 -5px 15px rgba(0,0,0,0.08) !important;
        z-index: 99999 !important;
        padding: 8px 0px !important;
        border-top: 1px solid #e2e8f0 !important;
        margin: 0 !important;
    }}
    
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {{
        background-color: transparent !important;
        padding: 0 !important;
        border-radius: 0 !important;
        gap: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
    }}

    div[data-testid="stTabs"] button {{
        flex: 1 !important;
        text-align: center !important;
        font-weight: bold !important;
        color: #64748b !important;
        background-color: transparent !important;
        border: none !important;
        padding: 12px 0px !important;
        transition: all 0.2s ease;
    }}
    
    div[data-testid="stTabs"] button[aria-selected="true"] {{
        color: #ea580c !important;
        background-color: transparent !important;
        border-bottom: none !important;
        transform: scale(1.05);
    }}

    /* 📱 استایل‌های اختصاصی موبایل (صفحه‌های کوچک‌تر از 768 پیکسل) */
    @media (max-width: 768px) {{
        /* حذف متون داخل دکمه‌های تب و بزرگ کردن آیکون‌ها/اموجی‌ها */
        div[data-testid="stTabs"] button {{
            font-size: 24px !important; /* سایز بزرگ برای آیکون‌ها جهت لمس راحت */
            color: #94a3b8 !important;
        }}
        /* ترفند مهندسی برای پنهان کردن متن و نگه‌داشتن اموجی اول */
        div[data-testid="stTabs"] button span {{
            font-size: 0px !important;
            color: transparent !important;
        }}
        div[data-testid="stTabs"] button span::first-letter {{
            font-size: 26px !important;
            color: initial !important;
            visibility: visible !important;
        }}
        div[data-testid="stTabs"] button[aria-selected="true"]::after {{
            content: "•";
            display: block;
            font-size: 12px;
            color: #ea580c;
            line-height: 5px;
            text-align: center;
        }}
    }}

    /* 💻 استایل‌های اختصاصی تبلت و دسکتاپ (بزرگ‌تر از 768 پیکسل) */
    @media (min-width: 769px) {{
        div[data-testid="stTabs"] button {{
            font-size: 15px !important;
        }}
        div[data-testid="stTabs"] button[aria-selected="true"] {{
            background-color: #ea580c !important;
            color: white !important;
            border-radius: 12px !important;
        }}
        .main .block-container {{
            max-width: 1100px !important; /* جمع شدن شیک صفحه در مانیتورهای بزرگ */
            margin: 0 auto !important;
        }}
    }}

    /* ================= FILE UPLOAD ================= */
    [data-testid="stFileUploadDropzone"],
    [data-testid="stFileUploaderDropzone"] {{
        border: 2px dashed #ea580c !important;
        border-radius: 24px !important;
        background-color: #f8fafc !important;
        padding: 50px 10px 40px 10px !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

inject_custom_css()

# ====================== ۴. هدر بالایی برنامه ======================
col_logo, col_title = st.columns([0.9, 5])
with col_logo:
    try: st.image("./static/logo.png", width=80)
    except: st.write("☀️")
with col_title:
    st.markdown("<h2 style='margin:0;'>TopSUNify</h2>", unsafe_allow_html=True)
    st.markdown("<h6 style='margin:0; color:#64748b;'>سامانه هوشمند و ریسپانسیو خدمات تاپسان</h6>", unsafe_allow_html=True)

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

# ====================== ۶. ساخت تب‌های اصلی (با اموجی در ابتدا برای حالت موبایل) ======================
# در موبایل متن‌ها به کمک CSS غیب می‌شوند و فقط اموجی (آیکون) می‌ماند.
tab_info, tab_service, tab_warranty, tab_invoice = st.tabs([
    "📚 اطلاعات فنی", 
    "🛠️ خدمات فنی", 
    "🛡️ ثبت گارانتی", 
    "🧾 صدور پیش‌فاکتور"
])

# ==============================================================================
# تب اول: صدور پیش‌فاکتور
# ==============================================================================
with tab_invoice:
    st.subheader("🧾 صدور پیش‌فاکتور هوشمند")
    
    product_type = st.selectbox(
        "نوع سیستم گرمایشی مورد نظر را انتخاب کنید:",
        ["گرمایش کف (سیستم هوشمند)", "زیرفرشی", "رادیاتور", "رستورانی", "عمومی"],
        key="selected_product_type"
    )
    st.write("---")

    if product_type == "گرمایش کف (سیستم هوشمند)":
        tab_file, tab_room_manual, tab_invoice_manual = st.tabs([
            "📂 فایل پلان", 
            "⌨️ ورود دستی ابعاد",
            "✍️ مقادیر مستقیم فاکتور"
        ])

        # --- آپلود فایل اتوکد ---
        with tab_file:
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

        # --- ورود دستی ابعاد اتاق‌ها ---
        with tab_room_manual:
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

        # --- ورود مستقیم اقلام فاکتور ---
        with tab_invoice_manual:
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

        # --- تنظیمات فروش و تاریخ ---
        st.write("### ⚙️ تنظیمات فاکتور")
        col1, col2, col3 = st.columns(3)
        enable_inst = col1.checkbox("هزینه نصب")
        inst_rate = col1.number_input("درصد نصب", value=15) if enable_inst else 15
        enable_tax = col2.checkbox("مالیات")
        tax_rate = col2.number_input("درصد مالیات", value=10) if enable_tax else 10
        enable_disc = col3.checkbox("تخفیف")
        disc = col3.number_input("درصد تخفیف", value=0) if enable_disc else 0

        # خروجی نهایی مالی
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
                
                st.write("### 🧾 پیش‌فاکتور محاسباتی:")
                st.table(pd.DataFrame(table_data, columns=["شرح کالا", "مقدار", "واحد", "مبلغ کل (ریال)"]))
                st.success(f"**مبلغ نهایی: {final_val:,.0f} ریال**")
            except Exception as e:
                st.error(f"خطا در محاسبات: {e}")
    else:
        st.info(f"بخش **{product_type}** به زودی فعال می‌شود.")

# ==============================================================================
# تب دوم: ثبت گارانتی
# ==============================================================================
with tab_warranty:
    st.subheader("🛡️ فرم ثبت گارانتی محصولات")
    with st.form("warranty_form"):
        st.text_input("نام و نام خانوادگی خریدار")
        st.text_input("شماره سریال محصول")
        st.file_uploader("آپلود عکس یا فیلم نصب", type=["jpg", "png", "mp4"])
        if st.form_submit_button("ثبت گارانتی"): st.success("✅ ثبت شد.")

# ==============================================================================
# تب سوم: درخواست خدمات فنی
# ==============================================================================
with tab_service:
    st.subheader("🛠️ ثبت درخواست خدمات فنی")
    st.radio("نوع درخواست:", ["نصب اولیه", "اعلام خرابی", "جابجایی"])
    with st.form("service_form"):
        st.text_area("آدرس")
        if st.form_submit_button("ارسال درخواست"): st.success("📌 ارسال شد.")

# ==============================================================================
# تب چهارم: اطلاعات فنی
# ==============================================================================
with tab_info:
    st.subheader("📚 بانک اطلاعات فنی")
    st.write("کاتالوگ‌ها به زودی آپلود می‌شوند.")
    if st.button("خروج از حساب کاربری"):
        st.session_state.logged_in = False
        st.rerun()
