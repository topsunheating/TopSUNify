import os
from io import BytesIO
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
from num2fawords import words 

# تلاش برای فراخوانی کتابخانه تاریخ شمسی
try:
    import jdatetime
except ImportError:
    jdatetime = None

# ================= تنظیمات پیشرفته فارسی =================
def fa(text):
    if not text:
        return ""
    configuration = {
        'delete_harakat': True,
        'support_zwj': True,
        'shift_harakat_position': True,
        'use_unshaped_instead_of_isolated': True
    }
    reshaper = arabic_reshaper.ArabicReshaper(configuration=configuration)
    reshaped_text = reshaper.reshape(str(text))
    return get_display(reshaped_text)

# ================= مسیرها و فونت =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH_REG = os.path.join(BASE_DIR, "Pinar-Regular.ttf")
FONT_PATH_BLACK = os.path.join(BASE_DIR, "Pinar-DS3-Black.ttf") # فونت اعداد و تیترها
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")

PDF_FONT = "Pinar"
FONT_BOLD = "Pinar-DS3-Black"

# ثبت فونت معمولی
if os.path.exists(FONT_PATH_REG):
    pdfmetrics.registerFont(TTFont(PDF_FONT, FONT_PATH_REG))
else:
    PDF_FONT = "Helvetica"

# ثبت فونت Bold (Pinar-DS3-Black)
if os.path.exists(FONT_PATH_BLACK):
    pdfmetrics.registerFont(TTFont(FONT_BOLD, FONT_PATH_BLACK))
else:
    FONT_BOLD = PDF_FONT # اگر فایل نبود از فونت معمولی استفاده کند

# ================= محاسبات مالی هوشمند عایق (رولی و خرده) =================
def calculate_tosunify_proforma(
    width_80_m, 
    width_40_m, 
    installation_pct=0, 
    discount_pct=0, 
    tax_pct=0, 
    thermostats_count=0
):
    # قیمت‌های واحد
    prices = {
        "standard_80": 17900000,
        "slim_40": 13350000,
        "insulation_roll": 142800000,
        "insulation_meter": 1450000,
        "thermostat": 35360000,
        "control_panel": 88950000
    }
   
    # محاسبات عایق
    xps_meters_needed = (width_80_m + width_40_m) * 1.1
    full_rolls = int(xps_meters_needed // 105)
    rem_meters = round(xps_meters_needed % 105, 1)
   
    insulation_roll_total = full_rolls * prices["insulation_roll"]
    insulation_meter_total = rem_meters * prices["insulation_meter"]
    xps_total = insulation_roll_total + insulation_meter_total
   
    # سایر اقلام
    m80_total = width_80_m * prices["standard_80"]
    m40_total = width_40_m * prices["slim_40"]
    thermostat_total = thermostats_count * prices["thermostat"]
    
    # === اصلاح ریشه‌ای باگ تابلو فرمان ===
    # اگر متراژ هر دو فیلم صفر باشد، یعنی تابلویی نیاز نیست و قیمت آن باید ۰ شود
    if width_80_m == 0 and width_40_m == 0:
        panel_total = 0
    else:
        panel_total = prices["control_panel"]
   
    subtotal = m80_total + m40_total + xps_total + thermostat_total + panel_total
   
    install_cost = subtotal * (installation_pct / 100)
    discount_amount = subtotal * (discount_pct / 100)
    before_tax = subtotal + install_cost - discount_amount
    tax_amount = before_tax * (tax_pct / 100)
   
    final_total = before_tax + tax_amount
   
    return {
        "m80_total": m80_total,
        "m40_total": m40_total,
        "xps_total": xps_total,
        "insulation_total": xps_total,
        "insulation_roll_total": insulation_roll_total,
        "insulation_meter_total": insulation_meter_total,
        "thermostat_total": thermostat_total,
        "ControlPanel_Total": panel_total,
        "UnitPrice_m80": prices["standard_80"],
        "UnitPrice_m40": prices["slim_40"],
        "UnitPrice_insulation_meter": prices["insulation_meter"],
        "UnitPrice_insulation_roll": prices["insulation_roll"],
        "UnitPrice_thermostat": prices["thermostat"],
        "UnitPrice_panel": prices["control_panel"],
        "full_rolls_count": full_rolls,
        "rem_meters_count": rem_meters,
        "Installation_Cost": install_cost,
        "Discount_Amount": discount_amount,
        "Tax_Amount": tax_amount,
        "Final_Amount": final_total
    }

# ================= تولید PDF کاملاً پویا، با کادرهای دورگرد، مبالغ BOLD و محاسبات دقیق عایق =================
def generate_proforma_pdf(res, m80, m40, xps, thermostats, p_count=0, customer_name="مشتری گرامی", doc_number=1000, manual_date=None):
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, KeepTogether
    from reportlab.lib.colors import HexColor, white
    
    buffer = BytesIO()
    
    # ۱. محاسبه و همسان‌سازی دقیق مبلغ نهایی (رند کردن کامل برای تطابق عدد و حروف)
    final_amount_raw = res.get('Final_Amount', 0)
    final_amount = int(round(float(final_amount_raw)))
    amount_in_words = words(final_amount) + " ریال"
    
    # ۲. تعریف سند با حاشیه استاندارد و بهینه برای صفحات بعدی
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=35,
        leftMargin=35,
        topMargin=45,
        bottomMargin=45
    )
    
    width, height = A4
    story = []

    # ۳. مدیریت هوشمند تاریخ صدور و تاریخ سررسید از دیکشنری ورودی (res)
    # اگر کلیدها در دیکشنری نبودند، به عنوان فالبک از تاریخ امروز استفاده می‌شود.
    if jdatetime:
        now_sh = jdatetime.datetime.now()
        fallback_date = f"{now_sh.year}/{now_sh.month:02d}/{now_sh.day:02d}"
    else:
        fallback_date = datetime.now().strftime("%Y/%m/%d")

    invoice_date_pdf = res.get('Invoice_Date', manual_date if manual_date else fallback_date)
    due_date_pdf = res.get('Due_Date', fallback_date)

    doc_id = f"TS-{doc_number:05d}"

    # ۴. تابع پس‌زمینه برای رسم المان‌های گرافیکی و کادرهای خریدار/فروشنده
    def draw_page_decorations(canvas_obj, document):
        canvas_obj.saveState()
        
        if document.page == 1:
            # لوگو و هدر اصلی
            if os.path.exists(LOGO_PATH):
                canvas_obj.drawImage(LOGO_PATH, width - 85, height - 75, width=50, height=50, mask='auto')

            canvas_obj.setFont(FONT_BOLD, 18) 
            canvas_obj.drawCentredString(width / 2, height - 45, fa("فروشگاه تاپسان هیتینگ"))

            canvas_obj.setFont(FONT_BOLD, 14)
            canvas_obj.drawCentredString(width / 2, height - 75, fa("پیش‌فاکتور"))
            canvas_obj.line(35, height - 90, width - 35, height - 90)

            # اطلاعات سند (سمت چپ بالا) - اصلاح فیلدهای متنی بر اساس مقادیر تفکیک‌شده
            canvas_obj.setFont(PDF_FONT, 10)
            x_value = 45 
            label_max_w = canvas_obj.stringWidth(fa("تاریخ سررسید:"), PDF_FONT, 10)
            x_label = x_value + label_max_w + 10 
            
            y_info = height - 35 
            canvas_obj.drawString(x_label, y_info, fa("شماره:"))
            canvas_obj.drawString(x_value, y_info, doc_id) 
            
            y_info -= 15
            canvas_obj.drawString(x_label, y_info, fa("تاریخ:"))
            canvas_obj.drawString(x_value, y_info, str(invoice_date_pdf))
            
            y_info -= 15
            canvas_obj.drawString(x_label, y_info, fa("تاریخ سررسید:"))
            canvas_obj.drawString(x_value, y_info, str(due_date_pdf)) # 👈 اعمال مستقیم تاریخ سررسید ۳ روزه

            # === کادرهای خریدار و فروشنده مجزا و لبه گرد ===
            canvas_obj.setStrokeColor(HexColor("#000000"))
            canvas_obj.setLineWidth(0.7)
            box_w = width - 70 
            box_h = 24    
            
            # کادر فروشنده
            y_seller_box = height - 125
            canvas_obj.roundRect(35, y_seller_box, box_w, box_h, 4, fill=0)
            canvas_obj.drawRightString(width - 48, y_seller_box + 7, fa("فروشنده: فروشگاه تاپسان هیتینگ"))

            # کادر خریدار
            y_buyer_box = y_seller_box - box_h - 8
            canvas_obj.roundRect(35, y_buyer_box, box_w, box_h, 4, fill=0)
            canvas_obj.drawRightString(width - 48, y_buyer_box + 7, fa(f"خریدار: {customer_name}"))
            
        else:
            # هدر مختصر برای صفحات دوم به بعد
            canvas_obj.setFont(FONT_BOLD, 10)
            canvas_obj.drawCentredString(width / 2, height - 30, fa("پیش‌فاکتور فروشگاه تاپسان هیتینگ"))
            canvas_obj.setFont(PDF_FONT, 9)
            canvas_obj.drawString(45, height - 30, f"No: {doc_id}")
            canvas_obj.drawRightString(width - 45, height - 30, f"Date: {invoice_date_pdf}")
            canvas_obj.line(35, height - 38, width - 35, height - 38)
            
        # شماره صفحه ثابت در فوتر تمام صفحات
        canvas_obj.setFont(PDF_FONT, 9)
        canvas_obj.drawCentredString(width / 2, 25, fa(f"صفحه {document.page}"))
        canvas_obj.restoreState()

    # ۵. ایجاد فضا برای عبور از هدر صفحه اول و کادرهای خریدار/فروشنده
    story.append(Spacer(1, 125)) 

    # ۶. ساخت ردیف‌های جدول فاکتور (استفاده‌ی مستقیم از مقادیر دیکشنری وب‌سایت جهت حل باگ عایق)
    table_rows = [
        [fa("مبلغ کل (ریال)"), fa("قیمت واحد (ریال)"), fa("مقدار"), fa("واحد"), fa("شرح کالا")]
    ]
    
    if m80 > 0:
        table_rows.append([f"{res.get('m80_total', 0):,.0f}", f"{res.get('UnitPrice_m80', 17900000):,.0f}", f"{m80:.1f}", fa("متر"), fa("گرمایش برقی تاپسان (عرض ۸۰ سانت)")])
    if m40 > 0:
        table_rows.append([f"{res.get('m40_total', 0):,.0f}", f"{res.get('UnitPrice_m40', 13350000):,.0f}", f"{m40:.1f}", fa("متر"), fa("گرمایش برقی تاپسان (عرض ۴۰ سانت)")])
    # ==================== ردیف عایق ====================
    if xps > 0:
        if res.get('full_rolls_count', 0) > 0 and res.get('rem_meters_count', 0) == 0:
            xps_unit = res.get('UnitPrice_insulation_roll', 142800000)
            xps_qty_display = res.get('full_rolls_count')
            xps_unit_text = "رول"
            xps_total = res.get('insulation_roll_total', xps * xps_unit)
        else:
            xps_unit = res.get('UnitPrice_insulation_meter', 1450000)
            xps_qty_display = xps
            xps_unit_text = "مترمربع"
            xps_total = round(xps * xps_unit)
        
        table_rows.append([
            f"{xps_total:,.0f}", 
            f"{xps_unit:,.0f}", 
            f"{xps_qty_display:.1f}" if isinstance(xps_qty_display, float) else str(xps_qty_display),
            fa(xps_unit_text), 
            fa("عایق بازتابشی AlumSUN")
        ])
    if thermostats > 0:
        table_rows.append([f"{res.get('thermostat_total', 0):,.0f}", f"{res.get('UnitPrice_thermostat', 35360000):,.0f}", str(thermostats), fa("عدد"), fa("ترموستات کنترل دمای کف")])
    if p_count > 0:
        panel_title = "تابلو فرمان مرکزی" if thermostats > 1 else "تابلو فرمان"
        table_rows.append([f"{res.get('ControlPanel_Total', 0):,.0f}", f"{res.get('UnitPrice_panel', 88950000):,.0f}", str(p_count), fa("دستگاه"), fa(panel_title)])

    if res.get('Installation_Cost', 0) > 0:
        table_rows.append([f"{res['Installation_Cost']:,.0f}", "", "", "", fa("هزینه نصب و اجرا")])
    if res.get('Discount_Amount', 0) > 0:
        table_rows.append([f"- {res['Discount_Amount']:,.0f}", "", "", "", fa("تخفیف")])
    if res.get('Tax_Amount', 0) > 0:
        table_rows.append([f"{res['Tax_Amount']:,.0f}", "", "", "", fa("مالیات بر ارزش افزوده")])

    # ردیف نهایی جمع کل فاکتور
    table_rows.append([f"{final_amount:,.0f}", "", "", "", fa("مبلغ نهایی")])

    col_widths = [110, 100, 60, 60, 200]
    t = Table(table_rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), PDF_FONT), 
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#f1f5f9")),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#1e293b")),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (-2, -1), 'CENTER'),
        ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#000000")),
        ('BACKGROUND', (0, -1), (-1, -1), HexColor("#e2e8f0")), 
        ('TEXTCOLOR', (0, -1), (-1, -1), HexColor("#000000")), 
        ('FONTNAME', (0, -1), (-1, -1), FONT_BOLD),
    ]))
    
    story.append(t)
    story.append(Spacer(1, 15))

    # ۷. کادر متنی مبلغ نهایی به حروف
    amount_style_bold = ParagraphStyle(name='AmtBold', fontName=FONT_BOLD, fontSize=11, leading=14, alignment=1)
    amount_style_normal = ParagraphStyle(name='AmtNormal', fontName=PDF_FONT, fontSize=9.5, leading=14, alignment=1)
    
    num_p = Paragraph(fa(f"مبلغ نهایی قابل پرداخت: {final_amount:,.0f} ریال"), amount_style_bold)
    word_p = Paragraph(fa(f"({amount_in_words})"), amount_style_normal)
    
    amount_box_table = Table([[num_p], [word_p]], colWidths=[width - 200])
    amount_box_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.8, HexColor("#000000")), 
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    
    story.append(amount_box_table)
    story.append(Spacer(1, 15))

    # ۸. کادر توضیحات رسمی ۱۳ بندی
    desc_header = Paragraph(f"<b>{fa('توضیحات:')}</b>", ParagraphStyle(name='HDesc', fontName=FONT_BOLD, fontSize=11, alignment=2))
    story.append(desc_header)
    story.append(Spacer(1, 5))

    desc_style = ParagraphStyle(
        name='InvoiceDescription', fontName=PDF_FONT, fontSize=9.2, leading=14.5,
        alignment=2, textColor=HexColor("#0f172a")
    )
    
    desc_lines = [
        "– ابعاد گرمایش کف: عرض استاندارد (۸۰ سانت) و ۴۰ سانت سفارشی با طول‌های مشخص (مطابق با پلان چیدمان)",
        "– ابعاد عایق بازتابشی کف: عرض استاندارد ۱/۵ متر بطول ۷۰ متر معادل ۱۰۵ مترمربع",
        "– ترموستات دما و تابلوفرمان براساس شرایط پروژه و جهت هوشمندسازی سیستم گرمایش کف تعبیه شده است.",
        "– همراه با پیش فاکتور، پلان چیدمان جهت مشاهده و تایید ابعادی ارسال می‌گردد.",
        "– با توجه به نوسان قیمتی مواد اولیه، اعتبار پیش فاکتور صرفاً تا تاریخ سررسید می‌باشد.",
        "– تمام هزینه‌های حمل، بیمه، ایاب و ذهاب و ... از محل تحویل شرکت تا محل تحویل خریدار؛ برعهده خریدار می‌باشد.",
        "– تا زمانی که اسناد دریافتی پیش فاکتور حاضر، وصول نقدی نگردد؛ کالا یا وجه آن عندالمطالبه فروشنده می‌باشد.",
        "– شرایط واریزی: واریز ۵۰٪ مبلغ کل بعنوان پیش‌پرداخت و پرداخت ۵۰٪ باقیمانده و تسویه کامل همزمان با صدور برگه خروج",
        "– پرداخت: واریز به کارت: ۹۱۸۹-۳۱۵۵-۸۶۱۰-۶۲۱۹ و یا شبا 820560962180000158097001 بنام آقای رضا تلچی نزد بانک سامان",
        "– زمان تحویل: ۱۰ - ۱۲ روزکاری از تایید واحد مالی شرکت (در صورت امکان تحویل زودتر از موعد اعلامی برحسب شرایط خط تولید وجود دارد)",
        "– هزینه کابل‌کشی، لوله گذاری، سیم‌کشی و سایر تجهیزات مرتبط خارج از پیش فاکتور برعهده خریدار می‌باشد. (با تایید تیم فنی شرکت)",
        "– در حین اجرا، هرگونه افزایش یا کاهش در میزان تجهیزات، مورد توافق طرفین بوده و طرفین متعهد به پرداخت مابه التفاوت می‌باشند.",
        "– پیش فاکتور حاضر، طبق ابعاد و نقشه ارسالی از جانب خریدار صادر گردیده و پرداخت پیش‌پرداخت به معنای تایید پیش‌فاکتور می‌باشد."
    ]

    cleaned_desc_text = "<br/>".join([fa(line) for line in desc_lines])
    wrapped_desc_text = Paragraph(cleaned_desc_text, desc_style)
    
    desc_table = Table([[wrapped_desc_text]], colWidths=[width - 70])
    desc_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.8, HexColor("#000000")),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(desc_table)
    story.append(Spacer(1, 15))

    # ۹. کادر تأیید نهایی و امضا
    approval_header = Paragraph(
        f"<b>{fa('تأیید پیش‌فاکتور')}</b>", 
        ParagraphStyle(name='HApproval', fontName=FONT_BOLD, fontSize=10.5, alignment=2)
    )
    
    line1 = "اینجانب ................................................ مالک / نماینده قانونی  پروژه، پیش فاکتور حاضر را بررسی نموده و کاملا مورد تایید می‌باشد."
    line2 = " "
    
    approval_style = ParagraphStyle(
        name='ApprovalBody', 
        fontName=PDF_FONT, 
        fontSize=9.5, 
        leading=10,
        alignment=2
    )

    approval_text = f"{fa(line1)}<br/>{fa(line2)}"
    approval_p = Paragraph(approval_text, approval_style)

    signature_data = [
        [fa("امضا و مهر/اثر انگشت:"), fa("نام و نام خانوادگی:")],
        ["", ""],
        [fa("تاریخ: "), ""]
    ]

    sig_table = Table(signature_data, colWidths=[(width-110)/2, (width-110)/2])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'RIGHT'),      
        ('FONTNAME', (0,0), (-1,-1), PDF_FONT),
        ('FONTSIZE', (0,0), (-1,-1), 9.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,1), (-1,1), 1),       
        ('RIGHTPADDING', (1,0), (1,-1), 5),     
    ]))

    approval_content = [[approval_p], [Spacer(1, 6)], [sig_table]]
    approval_table = Table(approval_content, colWidths=[width - 70])
    approval_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.0, HexColor("#000000")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
    ]))

    story.append(KeepTogether([approval_header, Spacer(1, 6), approval_table]))

    # ۱۰. کامپایل و ساخت نهایی فایل PDF
    doc.build(story, onFirstPage=draw_page_decorations, onLaterPages=draw_page_decorations)
    
    buffer.seek(0)
    return buffer.getvalue()