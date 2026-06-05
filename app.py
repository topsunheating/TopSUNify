import flet as ft
import os
import datetime
import time

FLOOR_PRODUCTS = {
    "طول 1/2 متر": 1250000,
    "طول 1/5 متر": 1850000,
    "طول 2 متر": 2450000,
    "طول 3 متر": 3050000,
    "2 ردیف بطول 2 متر": 4250000,
    "2 ردیف بطول 3 متر": 4850000,
    "3 ردیف بطول 3 متر": 5450000,
    "3 ردیف بطول 3/5 متر": 6650000,
    "3 ردیف بطول 4 متر": 6650000,
}

DIMMERS = {
    "دیمر 600 وات": 950000,
    "دیمر 900 وات": 1450000,
    "دیمر 1500 وات": 2450000,
}

def main(page: ft.Page):
    page.fonts = {"iranyekan": "fonts/iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    page.padding = 0
    page.rtl = True
    page.theme_mode = "light"
    page.bgcolor = "#f5f5f5"

    if not hasattr(page.session, "logged_in"):
        page.session.logged_in = False
        page.session.user_role = "عمومی"
        page.session.username = "رضا تلچی"

    def show_message(text: str, color="green"):
        snack = ft.SnackBar(content=ft.Text(text), bgcolor=color, action="بستن", duration=3000)
        page.snack_bar = snack
        snack.open = True
        page.update()

    # ==================== صفحه پیش فاکتور رادیاتور ====================
    def radiator_manual_invoice_page():
        RADIATOR_PRODUCTS = {
            "50×50 سانت": 12500000, "60×60 سانت": 15800000, "90×90 سانت": 24500000,
            "50×90 سانت": 16800000, "50×110 سانت": 18500000, "50×150 سانت": 23500000,
            "60×80 سانت": 17500000, "90×110 سانت": 26500000, "90×200 سانت": 39500000,
        }
        RADIATOR_COLORS = ["سفید", "مشکی", "طوسی", "طرح چوب", "طرح مرمر", "سفارشی"]
        square_sizes = ["50×50 سانت", "60×60 سانت", "90×90 سانت"]

        invoice_items = []

        radiator_size = ft.Dropdown(label="ابعاد رادیاتور", width=350, options=[ft.dropdown.Option(x) for x in RADIATOR_PRODUCTS.keys()])
        radiator_color = ft.Dropdown(label="طرح رادیاتور", width=350, options=[ft.dropdown.Option(x) for x in RADIATOR_COLORS])
        radiator_orientation = ft.Dropdown(label="نوع نصب", width=350, options=[ft.dropdown.Option("افقی"), ft.dropdown.Option("عمودی"), ft.dropdown.Option("-")], value="-")
        radiator_qty = ft.TextField(label="تعداد", width=350, value="1", keyboard_type=ft.KeyboardType.NUMBER)

        table = ft.DataTable(
            column_spacing=10,
            columns=[
                ft.DataColumn(ft.Text("شرح")),
                ft.DataColumn(ft.Text("تعداد")),
                ft.DataColumn(ft.Text("جمع (تومان)")), 
                ft.DataColumn(ft.Text("حذف"))
            ],
            rows=[]
        )
        total_text = ft.Text("جمع کل: 0 تومان", size=18, weight="bold", color="green")

        def update_orientation(e=None):
            if radiator_size.value in square_sizes:
                radiator_orientation.disabled = True
                radiator_orientation.value = "-"
            else:
                radiator_orientation.disabled = False
            page.update()
          
        def refresh_table():
            table.rows.clear()
            grand_total = 0
            for item in invoice_items:
                def delete_item(e, item_id=item["id"]):
                    nonlocal invoice_items
                    invoice_items[:] = [x for x in invoice_items if x["id"] != item_id]
                    refresh_table()
                    
                table.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(item["description"], size=10), width=150)),
                    ft.DataCell(ft.Text(str(item["qty"]), size=10),
                    ft.DataCell(ft.Text(f"{item['total']:,}", size=10),
                    ft.DataCell(ft.IconButton(ft.Icons.DELETE, icon_color="red",icon_size=12, on_click=delete_item)
                ]))
                grand_total += item["total"]
            total_text.value = f"جمع کل: {grand_total:,} تومان"
            page.update()

        def add_to_invoice(e):
            if not radiator_size.value:
                show_message("لطفاً ابعاد را انتخاب کنید", "red")
                return
                
            try:
                qty = int(radiator_qty.value or 1)
                unit_price = RADIATOR_PRODUCTS.get(radiator_size.value, 0)
                line_total = qty * unit_price
                
                description = f"{radiator_size.value} | {radiator_color.value or 'سفید'}"
                if not radiator_orientation.disabled and radiator_orientation.value != "-":
                    description += f" | {radiator_orientation.value}"
                
                invoice_items.append({"id": time.time(),"description": description, "qty": qty, "total": line_total})
                
                refresh_table()
                show_message("به لیست اضافه شد", "green")
            
            except Exception as ex:
                show_message(f"خطا: {ex}", "red")

        radiator_size.on_change = update_orientation

        return ft.Container(
            content=ft.Column([
                ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: render(1)), ft.Text("پیش فاکتور رادیاتور", size=20, weight="bold")]),
                ft.Divider(),
                radiator_size, radiator_color, radiator_orientation, radiator_qty,
                ft.FilledButton("افزودن به لیست", on_click=add_to_invoice, width=350, bgcolor="#1565C0"),
                ft.Container(content=table, padding=10),
                total_text,
                ft.FilledButton("صدور PDF نهایی", icon=ft.Icons.PICTURE_AS_PDF, width=350, bgcolor="green", on_click=lambda e: show_message("PDF صادر شد", "green"))
            ], scroll=ft.ScrollMode.AUTO, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20, width=400, expand=True
        )
    # ==================== پیش فاکتور دستی زیرفرشی ====================
    def floor_manual_invoice_page():

        product_size = ft.Dropdown(
            label="سایز زیرفرشی",
            width=350,
            options=[ft.dropdown.Option(x) for x in FLOOR_PRODUCTS.keys()]
        )

        qty = ft.TextField(
            label="تعداد",
            width=150,
            value="1"
        )

        insulation_switch = ft.Switch(
            label="افزودن عایق بازتابشی"
        )

        insulation_area = ft.TextField(
            label="متراژ عایق (متر مربع)",
            width=250,
            visible=False
        )

        dimmer_switch = ft.Switch(
            label="افزودن دیمر"
        )

        dimmer_type = ft.Dropdown(
            label="مدل دیمر",
            width=350,
            visible=False,
            options=[ft.dropdown.Option(x) for x in DIMMERS.keys()]
        )

        dimmer_qty = ft.TextField(
            label="تعداد دیمر",
            width=150,
            value="1",
            visible=False
        )

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("شرح")),
                ft.DataColumn(ft.Text("تعداد")),
                ft.DataColumn(ft.Text("قیمت"))
            ],
            rows=[]
        )

        total_text = ft.Text(
            "جمع کل: 0 تومان",
            size=18,
            weight="bold"
        )

        def toggle_insulation(e):
            insulation_area.visible = insulation_switch.value
            page.update()

        def toggle_dimmer(e):
            dimmer_type.visible = dimmer_switch.value
            dimmer_qty.visible = dimmer_switch.value
            page.update()

        def add_item(e):

            table.rows.clear()

            total = 0

            try:

                if product_size.value:

                    count = int(qty.value or 0)

                    unit_price = FLOOR_PRODUCTS[product_size.value]

                    row_total = count * unit_price

                    total += row_total

                    table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(product_size.value)),
                                ft.DataCell(ft.Text(str(count))),
                                ft.DataCell(ft.Text(f"{row_total:,}"))
                            ]
                        )
                    )

                if insulation_switch.value:

                    area = float(insulation_area.value or 0)

                    insulation_price = int(area * 1450000)

                    total += insulation_price

                    table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("عایق بازتابشی")),
                                ft.DataCell(ft.Text(str(area))),
                                ft.DataCell(ft.Text(f"{insulation_price:,}"))
                            ]
                        )
                    )

                if dimmer_switch.value and dimmer_type.value:

                    dqty = int(dimmer_qty.value or 0)

                    dprice = DIMMERS[dimmer_type.value]

                    dimmer_total = dqty * dprice

                    total += dimmer_total

                    table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(dimmer_type.value)),
                                ft.DataCell(ft.Text(str(dqty))),
                                ft.DataCell(ft.Text(f"{dimmer_total:,}"))
                            ]
                        )
                    )

                total_text.value = f"جمع کل: {total:,} تومان"

                page.update()

            except Exception as ex:
                show_message(f"خطا: {ex}", "red")

        insulation_switch.on_change = toggle_insulation
        dimmer_switch.on_change = toggle_dimmer

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                on_click=lambda e: render(1)
                            ),
                            ft.Text(
                                "پیش فاکتور زیرفرشی",
                                size=20,
                                weight="bold"
                            )
                        ]
                    ),

                    product_size,
                    qty,

                    ft.Divider(),

                    insulation_switch,
                    insulation_area,

                    ft.Divider(),

                    dimmer_switch,
                    dimmer_type,
                    dimmer_qty,

                    ft.Divider(),

                    ft.ElevatedButton(
                        "محاسبه پیش فاکتور",
                        on_click=add_item,
                        bgcolor="green",
                        color="white"
                    ),

                    table,

                    total_text,

                    ft.ElevatedButton(
                        "صدور PDF",
                        bgcolor="#1565C0",
                        color="white",
                        icon=ft.Icons.PICTURE_AS_PDF,
                        on_click=lambda e: show_message(
                            "اتصال PDF در مرحله بعد انجام می‌شود"
                        )
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=15
            ),
            padding=15,
            expand=True
        ) 
    # ==================== صفحه گرمایش از کف ====================
    def floor_heating_page():
        file_picker = ft.FilePicker()
        page.overlay.append(file_picker)

        def on_file_picked(e):
            if e.files:
                file = e.files[0]
                show_message(f"فایل {file.name} در حال پردازش...", "blue")
                process_dwg_file(file)

        file_picker.on_result = on_file_picked

        def process_dwg_file(file):
            try:
                # فقط توابع مورد نیاز را ایمپورت می‌کنیم
                from main import generate_layout_plan
                from Financial import calculate_tosunify_proforma, generate_proforma_pdf

                show_message("در حال تحلیل فایل توسط هسته main.py...", "blue")

                # تولید پلان چیدمان
                layout_pdf_bytes = generate_layout_plan(
                    file.path if hasattr(file, 'path') else file.name
                )

                # محاسبات مالی و صدور پیش‌فاکتور
                res = calculate_tosunify_proforma(
                    width_80_m=45.5,
                    width_40_m=8.2,
                    installation_pct=12,
                    discount_pct=5,
                    tax_pct=9,
                    thermostats_count=3
                )

                financial_pdf_bytes = generate_proforma_pdf(
                    res=res,
                    m80=45.5,
                    m40=8.2,
                    xps=65,
                    thermostats=3,
                    p_count=1,
                    customer_name=page.session.username,
                    doc_number=1001
                )

                # دانلود PDF
                import tempfile
                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
                    f.write(financial_pdf_bytes)
                    temp_path = f.name

                page.download_file(temp_path)
                show_message("✅ پیش‌فاکتور و پلان چیدمان با موفقیت صادر شد", "green")

            except Exception as ex:
                show_message(f"❌ خطا در پردازش: {ex}", "red")

        def method2_manual(e):
            show_message("ورود دستی ابعاد اتاق‌ها (در حال توسعه)", "blue")

        def method3_direct(e):
            show_message("روش مقادیر مستقیم (در حال توسعه)", "blue")

        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(1)),
                        ft.Text("گرمایش از کف (سیستم هوشمند)", size=21, weight="bold")
                    ]),
                    padding=15,
                    bgcolor="#f8f9fa",
                    border_radius=12
                ),

                ft.Text("روش صدور پیش‌فاکتور را انتخاب کنید", 
                       size=18, weight="bold", text_align=ft.TextAlign.CENTER),
                ft.Divider(height=25),

                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row([ft.Icon(ft.Icons.UPLOAD_FILE, color="white"), 
                                      ft.Text("📂 آپلود فایل DWG / DXF", size=16, weight="bold")], 
                                      alignment=ft.MainAxisAlignment.CENTER),
                        width=360, height=75, bgcolor="#1565C0", color="white",
                        on_click=lambda e: file_picker.pick_files(allow_multiple=False, allowed_extensions=["dwg", "dxf"]),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=18))
                    ),
                    margin=ft.margin.Margin(bottom=12)
                ),

                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row([ft.Icon(ft.Icons.EDIT_NOTE, color="white"), 
                                      ft.Text("⌨️ ورود دستی ابعاد اتاق‌ها", size=16, weight="bold")], 
                                      alignment=ft.MainAxisAlignment.CENTER),
                        width=360, height=75, bgcolor="#1565C0", color="white",
                        on_click=method2_manual,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=18))
                    ),
                    margin=ft.margin.Margin(bottom=12)
                ),

                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row([ft.Icon(ft.Icons.CALCULATE, color="white"), 
                                      ft.Text("✍️ مقادیر مستقیم (متراژ)", size=16, weight="bold")], 
                                      alignment=ft.MainAxisAlignment.CENTER),
                        width=360, height=75, bgcolor="#1565C0", color="white",
                        on_click=method3_direct,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=18))
                    )
                ),

                ft.Divider(height=30),
                ft.Text("هسته main.py و Financial.py متصل شد", size=13, color="grey", text_align=ft.TextAlign.CENTER)
            ], scroll=ft.ScrollMode.AUTO, spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400,
            expand=True,
            padding=15
        )
    # ==================== صفحات اضافی ====================
    def account_request_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("فرم درخواست همکاری", size=20, weight="bold")]), padding=10),
                ft.TextField(label="نام و نام خانوادگی", text_align=ft.TextAlign.RIGHT),
                ft.TextField(label="نام پدر", text_align=ft.TextAlign.RIGHT),
                ft.TextField(label="تاریخ تولد", text_align=ft.TextAlign.RIGHT),
                ft.TextField(label="شماره شناسنامه", text_align=ft.TextAlign.RIGHT),
                ft.TextField(label="شماره ملی", text_align=ft.TextAlign.RIGHT),
                ft.Dropdown(label="نوع درخواست", options=[ft.dropdown.Option(i) for i in ["نماینده فروش","عامل فروش","کارشناس فروش","نصاب فنی"]]),
                ft.ElevatedButton("ثبت نهایی درخواست", bgcolor="#1565C0", color="white", on_click=lambda e: show_message("درخواست با موفقیت ثبت شد"))
            ], scroll=ft.ScrollMode.AUTO),
            padding=20, width=400, expand=True
        )

    def inventory_page():
        product_data = {
            "گرمایش زیرفرشی": ["طول 1/2 متر", "طول 1/5 متر", "2 ردیف با طول 2 متر"],
            "رادیاتور": ["سایز 50×50 سانت", "سایز 50×90 سانت", "سایز 50×110 سانت", "سایز 50×150 سانت", "سایز 60×60 سانت", "سایز 60×80 سانت", "سایز 90×90 سانت", "سایز 90×110 سانت", "سایز 90×150 سانت", "سایز 90×200 سانت"],
            "عایق بازتابشی": ["3 مترمربع", "6 متر مربع"]
        }
        product_name = ft.Dropdown(label="نام محصول", width=350, options=[ft.dropdown.Option(k) for k in product_data.keys()])
        product_size = ft.Dropdown(label="ابعاد محصول", width=350, options=[])
        product_qty = ft.TextField(label="تعداد", width=100, keyboard_type=ft.KeyboardType.NUMBER)
       
        table = ft.DataTable(columns=[ft.DataColumn(ft.Text("نام")), ft.DataColumn(ft.Text("ابعاد")), ft.DataColumn(ft.Text("تعداد")), ft.DataColumn(ft.Text("حذف"))], rows=[])

        def load_sizes(e):
            if product_name.value:
                selected = product_name.value
                product_size.options = [ft.dropdown.Option(item) for item in product_data.get(selected, [])]
                product_size.value = None
                page.update()

        def add_to_table(e):
            if not product_name.value or not product_size.value or not product_qty.value:
                show_message("لطفاً همه فیلدها را پر کنید", "red")
                return
            new_row = ft.DataRow(cells=[
                ft.DataCell(ft.Text(product_name.value)),
                ft.DataCell(ft.Text(product_size.value)),
                ft.DataCell(ft.Text(product_qty.value)),
                ft.DataCell(ft.IconButton(ft.Icons.DELETE, icon_color="red", on_click=lambda _: (table.rows.remove(new_row), page.update())))
            ])
            table.rows.append(new_row)
            product_qty.value = ""
            page.update()

        def generate_and_download_pdf(e):
            if not table.rows:
                show_message("ابتدا حداقل یک مورد اضافه کنید", "red")
                return
            show_message("PDF تولید و آماده دانلود شد", "green")
            page.update()

        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("اعلام موجودی انبار", size=20, weight="bold")]), padding=10),
                product_name,
                ft.ElevatedButton("بارگذاری ابعاد", on_click=load_sizes, bgcolor="#1565C0", color="white", width=350),
                product_size,
                product_qty,
                ft.ElevatedButton("افزودن به لیست", on_click=add_to_table, bgcolor="green", color="white", width=350),
                ft.Divider(),
                table,
                ft.ElevatedButton("اعلام کل موجودی و دانلود PDF", on_click=generate_and_download_pdf, bgcolor="blue", color="white", width=350, icon=ft.Icons.DOWNLOAD)
            ], scroll=ft.ScrollMode.AUTO, spacing=15),
            width=400, expand=True, padding=15
        )

    def selected_customers_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("مشتریان منتخب", size=20, weight="bold")]), padding=10),
                ft.DataTable(
                    columns=[ft.DataColumn(ft.Text("کد")), ft.DataColumn(ft.Text("نام")), ft.DataColumn(ft.Text("شماره تماس")), ft.DataColumn(ft.Text("شهر"))],
                    rows=[
                        ft.DataRow(cells=[ft.DataCell(ft.Text("C1001")), ft.DataCell(ft.Text("شرکت آریا تهویه")), ft.DataCell(ft.Text("09123456789")), ft.DataCell(ft.Text("تهران"))]),
                        ft.DataRow(cells=[ft.DataCell(ft.Text("C1002")), ft.DataCell(ft.Text("مهندس رضایی")), ft.DataCell(ft.Text("09129876543")), ft.DataCell(ft.Text("اصفهان"))])
                    ]
                )
            ], scroll=ft.ScrollMode.AUTO),
            width=400, expand=True, padding=15
        )

    def colleagues_page():
        all_colleagues = [
            {"code": "101", "name": "علی علوی", "company": "شرکت آلفا", "phone": "09120000000", "city": "تهران"},
            {"code": "102", "name": "رضا رضایی", "company": "تکنو صنعت", "phone": "09130000000", "city": "اصفهان"}
        ]
        table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("کد")), ft.DataColumn(ft.Text("نام")), ft.DataColumn(ft.Text("مجموعه")), ft.DataColumn(ft.Text("تماس")), ft.DataColumn(ft.Text("شهر"))],
            rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(c["code"])), ft.DataCell(ft.Text(c["name"])), ft.DataCell(ft.Text(c["company"])), ft.DataCell(ft.Text(c["phone"])), ft.DataCell(ft.Text(c["city"]))]) for c in all_colleagues]
        )
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("همکاران منتخب", size=20, weight="bold")]), padding=10),
                table
            ], scroll=ft.ScrollMode.AUTO),
            width=400, expand=True, padding=15
        )

    def purchase_request_page():
        product_data = {
            "گرمایش از کف": ["طول 1 متر", "طول 2 متر", "طول 3 متر"],
            "رادیاتور": ["50×50", "50×90", "60×60", "90×150", "90×200"],
            "حوله خشک کن": ["60×40", "80×50", "100×60"],
            "گرمکن مخزن": ["100 لیتری", "200 لیتری", "500 لیتری"],
            "عایق بازتابشی": ["3 مترمربع", "6 مترمربع", "10 مترمربع"]
        }
        product_name = ft.Dropdown(label="نام محصول", width=350, options=[ft.dropdown.Option(k) for k in product_data.keys()])
        product_size = ft.Dropdown(label="ابعاد / مشخصات", width=350, options=[])
        product_qty = ft.TextField(label="تعداد", width=100, keyboard_type=ft.KeyboardType.NUMBER)
        table = ft.DataTable(columns=[ft.DataColumn(ft.Text("نام محصول")), ft.DataColumn(ft.Text("ابعاد")), ft.DataColumn(ft.Text("تعداد")), ft.DataColumn(ft.Text("حذف"))], rows=[])

        def load_sizes(e):
            if product_name.value:
                selected = product_name.value
                product_size.options = [ft.dropdown.Option(item) for item in product_data.get(selected, [])]
                product_size.value = None
                page.update()

        def add_to_table(e):
            if not product_name.value or not product_size.value or not product_qty.value:
                show_message("لطفاً همه فیلدها را پر کنید", "red")
                return
            new_row = ft.DataRow(cells=[
                ft.DataCell(ft.Text(product_name.value)),
                ft.DataCell(ft.Text(product_size.value)),
                ft.DataCell(ft.Text(product_qty.value)),
                ft.DataCell(ft.IconButton(ft.Icons.DELETE, icon_color="red", on_click=lambda _: (table.rows.remove(new_row), page.update())))
            ])
            table.rows.append(new_row)
            product_qty.value = ""
            page.update()

        def generate_purchase_pdf(e):
            if not table.rows:
                show_message("ابتدا حداقل یک درخواست اضافه کنید", "red")
                return
            show_message("PDF درخواست خرید تولید و آماده دانلود شد", "green")
            page.update()

        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("ثبت درخواست خرید", size=20, weight="bold")]), padding=10),
                product_name,
                ft.ElevatedButton("بارگذاری ابعاد", on_click=load_sizes, bgcolor="#1565C0", color="white", width=350),
                product_size,
                product_qty,
                ft.ElevatedButton("افزودن به لیست", on_click=add_to_table, bgcolor="green", color="white", width=350),
                ft.Divider(),
                table,
                ft.ElevatedButton("ثبت نهایی درخواست خرید و دانلود PDF", on_click=generate_purchase_pdf, bgcolor="#1565C0", color="white", width=350, icon=ft.Icons.DOWNLOAD)
            ], scroll=ft.ScrollMode.AUTO, spacing=15),
            width=400, expand=True, padding=15
        )

    def commission_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("محاسبه درصد همکاری", size=20, weight="bold")]), padding=10),
                ft.Text("فاکتورهای تسویه شده این ماه: ۴۸,۵۰۰,۰۰۰ تومان", size=16),
                ft.Text("درصد همکاری شما: ۱۲٪", size=22, weight="bold", color="blue"),
                ft.Text("مبلغ قابل تسویه: ۵,۸۲۰,۰۰۰ تومان", size=18, weight="bold", color="green"),
                ft.ElevatedButton("درخواست تسویه حساب", bgcolor="#1565C0", color="white", width=350, on_click=lambda e: show_message("درخواست تسویه ارسال شد", "green"))
            ], scroll=ft.ScrollMode.AUTO, spacing=25, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )

    def credit_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("مبلغ اعتبار", size=20, weight="bold")]), padding=10),
                ft.Text("اعتبار فعلی شما: ۱۲۰,۰۰۰,۰۰۰ تومان", size=18, weight="bold", color="green"),
                ft.TextField(label="مبلغ درخواستی افزایش اعتبار", width=350),
                ft.Dropdown(label="نوع تضمین", width=350, options=[ft.dropdown.Option("چک"), ft.dropdown.Option("سفته"), ft.dropdown.Option("واریز نقدی")]),
                ft.ElevatedButton("ارسال درخواست افزایش اعتبار", bgcolor="#1565C0", color="white", width=350, on_click=lambda e: show_message("درخواست افزایش اعتبار ارسال شد", "green"))
            ], scroll=ft.ScrollMode.AUTO, spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )

    def theme_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("نمایش (تم)", size=20, weight="bold")]), padding=10),
                ft.ListTile(leading=ft.Icon(ft.Icons.LIGHT_MODE), title=ft.Text("تم روشن"), on_click=lambda e: (setattr(page, 'theme_mode', 'light'), page.update(), show_message("تم روشن فعال شد", "blue"))),
                ft.ListTile(leading=ft.Icon(ft.Icons.DARK_MODE), title=ft.Text("تم تیره"), on_click=lambda e: (setattr(page, 'theme_mode', 'dark'), page.update(), show_message("تم تیره فعال شد", "blue")))
            ], scroll=ft.ScrollMode.AUTO, spacing=10),
            width=400, expand=True, padding=15
        )

    def update_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("بروزرسانی", size=20, weight="bold")]), padding=10),
                ft.Text("نسخه فعلی: ۱.۴.۳", size=17, weight="bold"),
                ft.Divider(),
                ft.Text("نسخه ۱.۴.۵ - ۱۴۰۴/۰۳/۱۰", size=16, weight="bold"),
                ft.Text("• بهبود سرعت بارگذاری\n• رفع باگ PDF\n• اضافه شدن صفحه درصد همکاری", size=15),
                ft.Divider(),
                ft.Text("نسخه ۱.۴.۴ - ۱۴۰۴/۰۲/۲۵", size=16, weight="bold"),
                ft.Text("• بهینه‌سازی تم تیره", size=15),
                ft.ElevatedButton("شما آخرین نسخه را دارید", bgcolor="green", color="white", width=350, on_click=lambda e: show_message("شما آخرین نسخه را نصب دارید", "green"))
            ], scroll=ft.ScrollMode.AUTO, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )

    def network_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("شبکه فروش و خدمات", size=20, weight="bold")]), padding=10),
                ft.Text("نقشه شبکه فروش و خدمات همکاران\n\n(در نسخه کامل نقشه تعاملی نمایش داده خواهد شد)", size=16, text_align=ft.TextAlign.CENTER)
            ], scroll=ft.ScrollMode.AUTO, spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )

    def rules_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("قوانین همکاری", size=20, weight="bold")]), padding=10),
                ft.Text("متن کامل قوانین و شرایط همکاری\n\nدر نسخه کامل اینجا قرار خواهد گرفت.", size=16, text_align=ft.TextAlign.CENTER)
            ], scroll=ft.ScrollMode.AUTO, spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )

    def about_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("درباره ما", size=20, weight="bold")]), padding=10),
                ft.Text("شرکت تاپسان\nتولیدکننده سیستم‌های گرمایشی پیشرفته\n\nنسخه اپلیکیشن: ۱.۴.۳", size=16, text_align=ft.TextAlign.CENTER)
            ], scroll=ft.ScrollMode.AUTO, spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )

    # ==================== صفحه پروفایل ====================
    def profile_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Column([ft.CircleAvatar(foreground_image_src="https://i.pravatar.cc/150?u=reza", radius=48), ft.Text("نام و نام خانوادگی | نام کاربری", size=20, weight="bold", text_align=ft.TextAlign.CENTER), ft.Text("شماره موبایل", size=16, color="grey", text_align=ft.TextAlign.CENTER), ft.Container(content=ft.Text(f"سطح دسترسی: {page.session.user_role}", size=15, color="blue", text_align=ft.TextAlign.CENTER), bgcolor="#f0f0f0", padding=12, border_radius=12, margin=ft.margin.Margin(top=12, bottom=8))], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=20, bgcolor="#f8f9fa", border_radius=20, margin=ft.margin.Margin(bottom=20), width=380),
                ft.Container(content=ft.Column([
                    ft.ListTile(leading=ft.Icon(ft.Icons.PERSON_ADD, color="blue"), title=ft.Text("درخواست ایجاد حساب"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(6)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.STAR, color="orange"), title=ft.Text("مشتریان منتخب"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(7)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.WAREHOUSE, color="green"), title=ft.Text("اعلام موجودی انبار"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(8)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.SHOPPING_CART, color="orange"), title=ft.Text("ثبت درخواست خرید"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(10)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.GROUP), title=ft.Text("همکاران منتخب"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(9)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.PERCENT, color="purple"), title=ft.Text("محاسبه درصد همکاری"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(11)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, color="green"), title=ft.Text("مبلغ اعتبار"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(12)),
                    ft.Divider(height=25),
                    ft.ListTile(leading=ft.Icon(ft.Icons.PALETTE, color="purple"), title=ft.Text("نمایش (تم روشن/تیره)"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(13)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.UPDATE, color="blue"), title=ft.Text("بروزرسانی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(14)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.MAP, color="green"), title=ft.Text("شبکه فروش و خدمات"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(15)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.GAVEL, color="amber"), title=ft.Text("قوانین"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(16)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.INFO, color="blue"), title=ft.Text("درباره ما"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(17)),
                    ft.Divider(height=25),
                    ft.ListTile(leading=ft.Icon(ft.Icons.SETTINGS, color="grey"), title=ft.Text("تنظیمات"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(5)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.LOGOUT, color="red"), title=ft.Text("خروج", color="red"), on_click=lambda e: (setattr(page.session, 'logged_in', False), render())),
                    ft.Text("نسخه ۱.۴.۳", size=12, color="grey", text_align=ft.TextAlign.CENTER)
                ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=360)
            ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, margin=ft.margin.Margin(left=15, right=15), expand=True
        )

    # ==================== رندر اصلی ====================
    def render(tab_index=0):
        page.controls.clear()
        if not page.session.logged_in:
            page.add(
                ft.Container(
                    content=ft.Column([
                        ft.Container(content=ft.Image(src="TopSUNify.png", width=190), margin=ft.margin.Margin(top=40, bottom=40)),
                        ft.Container(content=ft.TextField(label="نام کاربری", width=340, border_radius=12, prefix_icon=ft.Icons.PERSON, text_align=ft.TextAlign.RIGHT), margin=ft.margin.Margin(bottom=20)),
                        ft.Container(content=ft.Row([ft.Container(content=ft.Icon(ft.Icons.FINGERPRINT, size=42, color="#FFCC00"), on_click=lambda e: show_message("احراز هویت بیومتریک", "orange"), padding=10, border_radius=12), ft.TextField(label="رمز عبور", password=True, width=270, border_radius=12, prefix_icon=ft.Icons.LOCK, text_align=ft.TextAlign.RIGHT)], alignment=ft.MainAxisAlignment.CENTER, spacing=12), margin=ft.margin.Margin(bottom=30)),
                        ft.ElevatedButton("ورود به TopSUNify", width=340, bgcolor="#FFCC00", color="black", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)), on_click=lambda e: (setattr(page.session, 'logged_in', True), render())),
                        ft.TextButton("فعال‌سازی / فراموشی رمز", style=ft.ButtonStyle(color={"": "blue"})),
                        ft.Container(content=ft.Image(src="TopSUN-Powered.png", width=160), margin=ft.margin.Margin(top=50, bottom=30)),
                        ft.Container(content=ft.Image(src="landscape.jpg", width=400, height=220, fit="cover"), expand=True)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
                    width=400, margin=ft.margin.Margin(left=15, right=15), expand=True
                )
            )
        else:
            contents = [
                dashboard_page(), pre_invoice_page(), home_page(), technical_page(),
                profile_page(), settings_page(), account_request_page(),
                selected_customers_page(), inventory_page(), colleagues_page(),
                purchase_request_page(), commission_page(), credit_page(),
                theme_page(), update_page(), network_page(), rules_page(), about_page(), floor_heating_page(), floor_manual_invoice_page(), radiator_manual_invoice_page()
            ]
            main_content = ft.Container(content=contents[tab_index], expand=True, width=400, margin=ft.margin.Margin(left=15, right=15))
            nav_bar = ft.Container(
                content=ft.Row([
                    ft.Container(content=ft.Image(src="dashboard.png", width=32, height=32), on_click=lambda _: render(0), padding=8),
                    ft.Container(content=ft.Image(src="invoice.png", width=32, height=32), on_click=lambda _: render(1), padding=8),
                    ft.Container(content=ft.Image(src="TopSUNify-1.png", width=32, height=32), on_click=lambda _: render(2), padding=8),
                    ft.Container(content=ft.Image(src="technical.png", width=32, height=32), on_click=lambda _: render(3), padding=8),
                    ft.Container(content=ft.Image(src="profile.png", width=32, height=32), on_click=lambda _: render(4), padding=8),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                bgcolor="white", padding=12
            )
            page.add(
                ft.Column([
                    ft.Container(content=ft.Image(src="TopSUNify.png", width=80), margin=ft.margin.Margin(top=10, bottom=10)),
                    ft.Divider(),
                    main_content,
                    nav_bar
                ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
        page.update()

    # ==================== صفحات اصلی ====================
    def dashboard_page():
        selected_ref = ft.Ref[ft.Container]()
        def select_period(e, year, month_num):
            if selected_ref.current:
                selected_ref.current.bgcolor = "#f0f0f0"
                selected_ref.current.update()
            e.control.bgcolor = "#1565C0"
            selected_ref.current = e.control
            e.control.update()
            show_message(f"بازه انتخابی: {year}/{month_num}")

        years = ["1401", "1402", "1403", "1404", "1405", "1406", "1407"]
        months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        period_buttons = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=8, alignment=ft.MainAxisAlignment.CENTER)
        for year in years:
            for month_num in months:
                is_selected = (year == "1405" and month_num == "05")
                container = ft.Container(content=ft.Text(f"{year}/{month_num}", size=14, weight="bold", text_align=ft.TextAlign.CENTER), width=85, height=35, bgcolor="#1565C0" if is_selected else "#f0f0f0", border_radius=30, alignment=ft.Alignment(0, 0), on_click=lambda e, y=year, m=month_num: select_period(e, y, m))
                if is_selected: selected_ref.current = container
                period_buttons.controls.append(container)

        view_button = ft.ElevatedButton("مشاهده اطلاعات این بازه", width=250, bgcolor="#1565C0", color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)), on_click=lambda e: show_message("در حال بارگذاری گزارش‌های مالی و عملیاتی..."))

        report_cards = ft.GridView(runs_count=2, max_extent=120, spacing=10, run_spacing=12, padding=10, expand=True)
        cards_data = [("فاکتورهای تسویه شده", ft.Icons.CHECK_CIRCLE, "#1976D2"), ("فاکتورهای فروش", ft.Icons.SHOPPING_CART, "#388E3C"), ("پیش فاکتورها", ft.Icons.RECEIPT_LONG, "#1565C0"), ("پروژه‌های نصب شده", ft.Icons.HOME_WORK, "#7B1FA2"), ("فاکتورهای باز", ft.Icons.PENDING, "#F57C00")]
        for title, icon, color in cards_data:
            report_cards.controls.append(ft.Container(content=ft.Column([ft.Icon(icon, size=36, color=color), ft.Text(title, size=13.5, weight="bold", text_align=ft.TextAlign.CENTER)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8), bgcolor="white", border_radius=16, padding=14, shadow=ft.BoxShadow(blur_radius=8, color="#e0e0e0"), expand=True, on_click=lambda e, t=title: show_message(f"بخش {t}"), ink=True))

        return ft.Container(content=ft.Column([ft.Container(content=ft.Dropdown(value="رضا تلچی", options=[ft.dropdown.Option("رضا تلچی"), ft.dropdown.Option("زیرمجموعه فروش")], width=320, border_radius=30, bgcolor="white"), margin=ft.margin.Margin(bottom=15)), ft.Text("انتخاب بازه زمانی", size=17, weight="bold", text_align=ft.TextAlign.CENTER), period_buttons, ft.Divider(height=10), view_button, ft.Divider(height=20), ft.Text("گزارش‌های مالی و عملیاتی", size=18, weight="bold", text_align=ft.TextAlign.CENTER), report_cards], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)
    # ==================== صفحات اصلی ====================
    def pre_invoice_page():
        products = [
            ("گرمایش از کف", lambda e: render(18)),
            ("زیرفرشی", lambda e: render(19)),
            ("رادیاتور", lambda e: render(20)),
            ("حوله خشک کن", lambda e: show_message("به زودی فعال می‌شود", "blue")),
            ("یخ زدایی رمپ", lambda e: show_message("به زودی فعال می‌شود", "blue")),
            ("یخ زدایی پله", lambda e: show_message("به زودی فعال می‌شود", "blue")),
            ("گرمکن مخزن", lambda e: show_message("به زودی فعال می‌شود", "blue")),
            ("گرمکن صندلی", lambda e: show_message("به زودی فعال می‌شود", "blue")),
            ("رستورانی", lambda e: show_message("به زودی فعال می‌شود", "blue")),
            ("عایق بازتابشی", lambda e: show_message("به زودی فعال می‌شود", "blue")),
        ]
        
        grid = ft.GridView(
            runs_count=2,
            max_extent=120,
            spacing=10,
            run_spacing=12,
            padding=10,
            expand=True
        )
        
        for name, action in products:
            grid.controls.append(
                ft.Container(
                    content=ft.Text(
                        name,
                        size=15,
                        weight="bold",
                        text_align=ft.TextAlign.CENTER,
                        color="#1565C0"
                    ),
                    width=170,
                    height=70,
                    bgcolor="#ffffff",
                    border_radius=12,
                    alignment=ft.Alignment(0, 0),
                    shadow=ft.BoxShadow(blur_radius=6, color="#e0e0e0"),
                    on_click=action,
                    ink=True
                )
            )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "نوع محصول مورد نظر را انتخاب کنید",
                        size=18,
                        weight="bold",
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Divider(height=10),
                    grid
                ],
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            width=400,
            margin=ft.margin.Margin(left=15, right=15),
            expand=True
        )
    def home_page():
        return ft.Container(content=ft.Column([ft.Container(content=ft.Column([ft.Image(src="TopSUNify-1.png", width=80), ft.Text("خوش آمدید به TopSUNify", size=18, weight="bold", text_align=ft.TextAlign.CENTER), ft.Text("مرکز خدمات و پشتیبانی", size=16, color="grey", text_align=ft.TextAlign.CENTER)], horizontal_alignment=ft.CrossAxisAlignment.CENTER), margin=ft.margin.Margin(top=20, bottom=30)), ft.Container(content=ft.Column([ft.ListTile(leading=ft.Icon(ft.Icons.SHIELD, color="green"), title=ft.Text("ثبت گارانتی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.INSTALL_DESKTOP, color="blue"), title=ft.Text("درخواست نصب اولیه"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.SUPPORT_AGENT, color="orange"), title=ft.Text("درخواست خدمات فنی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.SHOPPING_CART_CHECKOUT, color="purple"), title=ft.Text("ثبت درخواست سفارشی و عمده"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.PRINT, color="red"), title=ft.Text("درخواست چاپ طرح سفارشی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20))], spacing=2), width=380)], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)

    def technical_page():
        return ft.Container(content=ft.Column([ft.Container(content=ft.Text("اطلاعات فنی", size=18, weight="bold", text_align=ft.TextAlign.CENTER), padding=20, margin=ft.margin.Margin(bottom=15)), ft.Container(content=ft.Column([ft.ListTile(leading=ft.Icon(ft.Icons.BOOK, color="blue"), title=ft.Text("کاتالوگ محصولات"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.PRICE_CHANGE, color="green"), title=ft.Text("لیست قیمت"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.WORK_HISTORY, color="purple"), title=ft.Text("رزومه شرکت"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.DESCRIPTION, color="orange"), title=ft.Text("پروپوزال و گزارش فنی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.IMAGE, color="pink"), title=ft.Text("تصاویر و فیلم پروژه‌ها"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.VIDEO_LIBRARY, color="red"), title=ft.Text("فیلم‌های تبلیغاتی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20))], spacing=2), width=380)], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)

    def settings_page():
        return ft.Container(content=ft.Column([ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("تنظیمات", size=24, weight="bold")]), padding=15, bgcolor="#f8f9fa", border_radius=20, margin=ft.margin.Margin(bottom=20)), ft.Column([ft.ListTile(leading=ft.Icon(ft.Icons.PERSON), title=ft.Text("تغییر نام کاربری"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.SAVE), title=ft.Text("ذخیره نام کاربری"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.FINGERPRINT), title=ft.Text("ورود با اثر انگشت"), trailing=ft.Switch(value=False)), ft.ListTile(leading=ft.Icon(ft.Icons.LOCK), title=ft.Text("تغییر رمز ورود"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.PHONE), title=ft.Text("تغییر شماره تلفن همراه"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.DEVICES), title=ft.Text("دستگاه‌های فعال"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.Divider(height=20), ft.ListTile(leading=ft.Icon(ft.Icons.DELETE_FOREVER, color="red"), title=ft.Text("حذف تنظیمات و خروج از نرم‌افزار", color="red"), on_click=lambda e: (setattr(page.session, 'logged_in', False), render()))], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER)]), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)

    render()


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
