import flet as ft
import os
import datetime
import time
import re 

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
        RADIATOR_COLORS = ["سفید", "مشکی", "طوسی", "نوک مدادی", "سفارشی"]
        square_sizes = ["50×50 سانت", "60×60 سانت", "90×90 سانت"]

        invoice_items = []

        radiator_size = ft.Dropdown(label="ابعاد رادیاتور", width=350, options=[ft.dropdown.Option(x) for x in RADIATOR_PRODUCTS.keys()])
        radiator_color = ft.Dropdown(label="طرح رادیاتور", width=350, options=[ft.dropdown.Option(x) for x in RADIATOR_COLORS])
        radiator_orientation = ft.Dropdown(label="نوع نصب", width=350, options=[ft.dropdown.Option("افقی"), ft.dropdown.Option("عمودی"), ft.dropdown.Option("-")], value="-")
        radiator_qty = ft.TextField(label="تعداد", width=350, value="1", keyboard_type=ft.KeyboardType.NUMBER)

        table = ft.DataTable(
            column_spacing=10,
            columns=[
                ft.DataColumn(ft.Text("شرح"), numeric=True),
                ft.DataColumn(ft.Text("تعداد")),
                ft.DataColumn(ft.Text("قیمت")), 
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
            nonlocal invoice_items
            table.rows.clear()
            grand_total = 0
            for item in invoice_items:
                def delete_item(e, item_id=item["id"]):
                    nonlocal invoice_items
                    invoice_items[:] = [x for x in invoice_items if x["id"] != item_id]
                    refresh_table()
                    
                def centered_cell(content):
                    return ft.DataCell(
                        ft.Container(
                            content=content,
                            alignment=ft.alignment.center
                        )
                    )
                    
                table.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(item["description"])),
                    ft.DataCell(ft.Text(str(item["qty"]))),
                    ft.DataCell(ft.Text(f"{item['total']:,}")),
                    ft.DataCell(ft.IconButton(ft.Icons.DELETE, icon_color="red", on_click=delete_item))
                ]))
                grand_total += item["total"]        

                grand_total += item["total"]
            total_text.value = f"جمع کل: {grand_total:,} تومان"
            page.update()

        def add_to_invoice(e):
            nonlocal invoice_items
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
        invoice_items = []
        
        product_size = ft.Dropdown(label="سایز زیرفرشی", width=350, options=[ft.dropdown.Option(x) for x in FLOOR_PRODUCTS.keys()])
        qty = ft.TextField(label="تعداد", width=350, value="1", keyboard_type=ft.KeyboardType.NUMBER)
        insulation_switch = ft.Switch(label="افزودن عایق بازتابشی")
        insulation_area = ft.TextField(label="متراژ عایق (متر مربع)", width=350, visible=False, keyboard_type=ft.KeyboardType.NUMBER)
        dimmer_switch = ft.Switch(label="افزودن دیمر")
        dimmer_type = ft.Dropdown(label="مدل دیمر", width=350, visible=False, options=[ft.dropdown.Option(x) for x in DIMMERS.keys()])
        dimmer_qty = ft.TextField(label="تعداد دیمر", width=350, value="1", visible=False, keyboard_type=ft.KeyboardType.NUMBER)
        
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("شرح")),
                ft.DataColumn(ft.Text("تعداد")),
                ft.DataColumn(ft.Text("قیمت")),
                ft.DataColumn(ft.Text("حذف"))
            ],
            rows=[]
        )
        total_text = ft.Text("جمع کل: 0 تومان", size=18, weight="bold", color="green")
        
        def refresh_table():
            table.rows.clear()
            grand_total = 0
            for item in invoice_items:
                def delete_item(e, item_id=item["id"]):
                    nonlocal invoice_items
                    invoice_items = [x for x in invoice_items if x["id"] != item_id]
                    refresh_table()

                table.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(item["desc"], size=12)),
                    ft.DataCell(ft.Text(str(item["qty"]), size=12)),
                    ft.DataCell(ft.Text(f"{item['total']:,}", size=12)),
                    ft.DataCell(ft.IconButton(ft.Icons.DELETE, icon_color="red", icon_size=18, on_click=delete_item))
                ]))
                grand_total += item["total"]
            
            total_text.value = f"جمع کل: {grand_total:,} تومان"
            page.update()
        def add_item(e):
            try:
                added = False
               
                if product_size.value:
                    count = int(qty.value or 0)
                    if count > 0:
                        price = FLOOR_PRODUCTS[product_size.value]
                        invoice_items.append({
                            "id": len(invoice_items) + 1,
                            "desc": product_size.value,
                            "qty": count,
                            "total": count * price
                        })
                        added = True
                   
                if insulation_switch.value and insulation_area.value:
                    area = float(insulation_area.value or 0)
                    if area > 0:
                        invoice_items.append({
                            "id": len(invoice_items) + 1,
                            "desc": "عایق بازتابشی",
                            "qty": area,
                            "total": int(area * 1450000)
                        })
                        added = True
                   
                if dimmer_switch.value and dimmer_type.value:
                    dqty = int(dimmer_qty.value or 0)
                    if dqty > 0:
                        dprice = DIMMERS[dimmer_type.value]
                        invoice_items.append({
                            "id": len(invoice_items) + 1,
                            "desc": dimmer_type.value,
                            "qty": dqty,
                            "total": dqty * dprice
                        })
                        added = True
                   
                if added:
                    refresh_table()
                    show_message("به لیست اضافه شد", "green")
                    # پاک کردن فیلدها
                    product_size.value = None
                    qty.value = "1"
                    page.update()
                else:
                    show_message("لطفاً یک مورد را انتخاب کنید", "orange")
            except Exception as ex:
                show_message(f"خطا: {ex}", "red")
        insulation_switch.on_change = lambda e: (setattr(insulation_area, "visible", insulation_switch.value), page.update())
        dimmer_switch.on_change = lambda e: (setattr(dimmer_type, "visible", dimmer_switch.value), setattr(dimmer_qty, "visible", dimmer_switch.value), page.update())
        
        return ft.Container(
            content=ft.Column([
                ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: render(1)), ft.Text("پیش فاکتور زیرفرشی", size=20, weight="bold")]),
                product_size, qty, ft.Divider(),
                ft.Row([insulation_switch], alignment=ft.MainAxisAlignment.START),
                insulation_area, ft.Divider(),
                ft.Row([dimmer_switch], alignment=ft.MainAxisAlignment.START),
                dimmer_type, dimmer_qty, ft.Divider(),
                ft.FilledButton("افزودن به لیست", on_click=add_item, bgcolor="#1565C0", width=350),
                table, total_text,
                ft.FilledButton("صدور PDF نهایی", icon=ft.Icons.PICTURE_AS_PDF, bgcolor="green", color="white", width=350, on_click=lambda e: show_message("PDF صادر شد", "green"))
            ], scroll=ft.ScrollMode.AUTO, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=15, width=400, expand=True
        )    
    # ==================== صفحه گرمایش از کف ====================
    def floor_heating_page():
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
                ft.Divider(height=30),

                                # روش ۱: آپلود فایل DWG / DXF
                ft.Container(
                    content=ft.FilledButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.UPLOAD_FILE, color="white"),
                            ft.Text("📂 آپلود فایل DWG / DXF", size=16, weight="bold")
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        width=360, height=75, bgcolor="#1565C0", color="white",
                        on_click=lambda e: render(19),   # ← روش اول
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=18))
                    ),
                    margin=ft.margin.Margin(bottom=15)
                ),

                # روش ۲: ورود دستی ابعاد اتاق‌ها
                ft.Container(
                    content=ft.FilledButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.EDIT_NOTE, color="white"),
                            ft.Text("⌨️ ورود دستی ابعاد اتاق‌ها", size=16, weight="bold")
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        width=360, height=75, bgcolor="#1565C0", color="white",
                        on_click=lambda e: render(24),   # ← روش دوم
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=18))
                    ),
                    margin=ft.margin.Margin(bottom=15)
                ),

                # روش ۳: مقادیر مستقیم
                ft.Container(
                    content=ft.FilledButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CALCULATE, color="white"),
                            ft.Text("✍️ مقادیر مستقیم (متراژ)", size=16, weight="bold")
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        width=360, height=75, bgcolor="#1565C0", color="white",
                        on_click=lambda e: render(21),   # ← روش سوم
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=18))
                    )
                ),

                ft.Divider(height=30),
                ft.Text("هسته main.py و Financial.py آماده اتصال است",
                       size=13, color="grey", text_align=ft.TextAlign.CENTER)
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400,
            expand=True,
            padding=15
        )
        
        # ==================== روش دوم گرمایش از کف: ورود دستی ابعاد اتاق‌ها ====================
    def floor_room_dimensions_page():
        rooms = []

        room_name = ft.TextField(label="نام اتاق", width=350, value="اتاق", text_align=ft.TextAlign.RIGHT)
        room_length = ft.TextField(label="طول اتاق (متر)", width=350, keyboard_type=ft.KeyboardType.NUMBER)
        room_width = ft.TextField(label="عرض اتاق (متر)", width=350, keyboard_type=ft.KeyboardType.NUMBER)

        rooms_list = ft.Column(scroll=ft.ScrollMode.AUTO, height=150)

        layout_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("شرح")), ft.DataColumn(ft.Text("مقدار"))], rows=[])

        # گزینه‌های جانبی
        install_switch = ft.Switch(label="اضافه کردن هزینه نصب", value=False)
        install_pct = ft.Dropdown(label="درصد هزینه نصب", width=350, options=[ft.dropdown.Option(x) for x in ["0","10","15","20","25"]], value="15", visible=False)

        travel_switch = ft.Switch(label="اضافه کردن هزینه ایاب و ذهاب", value=False)
        travel_cost = ft.TextField(label="مبلغ ایاب و ذهاب (تومان)", width=350, value="0", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        tax_switch = ft.Switch(label="اضافه کردن مالیات", value=False)
        tax_pct = ft.TextField(label="درصد مالیات", width=350, value="10", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        discount_switch = ft.Switch(label="اضافه کردن تخفیف", value=False)
        discount_pct = ft.TextField(label="درصد تخفیف", width=350, value="5", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        other_switch = ft.Switch(label="سایر هزینه‌ها", value=False)
        other_cost = ft.TextField(label="مبلغ سایر هزینه‌ها (تومان)", width=350, value="0", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        items_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("شرح کالا")), ft.DataColumn(ft.Text("مقدار")), ft.DataColumn(ft.Text("مبلغ"))], rows=[])
        total_text = ft.Text("جمع کل: 0 تومان", size=20, weight="bold", color="green")
        download_btn = ft.FilledButton("دانلود پیش‌فاکتور PDF", width=350, bgcolor="green", color="white", visible=False, icon=ft.Icons.DOWNLOAD)

        def update_visibility(e=None):
            install_pct.visible = install_switch.value
            travel_cost.visible = travel_switch.value
            tax_pct.visible = tax_switch.value
            discount_pct.visible = discount_switch.value
            other_cost.visible = other_switch.value
            page.update()

        install_switch.on_change = travel_switch.on_change = tax_switch.on_change = discount_switch.on_change = other_switch.on_change = update_visibility

        def add_room(e):
            if not room_length.value or not room_width.value:
                show_message("طول و عرض اتاق را وارد کنید", "red")
                return
            try:
                length = float(room_length.value)
                width = float(room_width.value)
                area = length * width
                name = room_name.value or f"اتاق {len(rooms)+1}"

                rooms.append({"name": name, "length": length, "width": width, "area": area})
                rooms_list.controls.append(ft.Text(f"• {name}: {length} × {width} متر ({area:.1f} م²)"))
                
                room_length.value = ""
                room_width.value = ""
                page.update()
            except:
                show_message("مقادیر نامعتبر است", "red")

        def calculate_layout(e):
            if not rooms:
                show_message("ابتدا حداقل یک اتاق اضافه کنید", "red")
                return

            total_area = sum(r["area"] for r in rooms)
            film80 = total_area * 0.7
            film40 = total_area * 0.3
            insulation = total_area * 1.1
            thermostats = len(rooms) + 1

            if thermostats <= 4:
                panel_text = "تابلو ۴ خروجی - ۱۲,۵۰۰,۰۰۰ تومان"
                panel_price = 12500000
            elif thermostats <= 6:
                panel_text = "تابلو ۶ خروجی - ۱۵,۵۰۰,۰۰۰ تومان"
                panel_price = 15500000
            else:
                panel_text = "تابلو ۱۰ خروجی - ۲۲,۰۰۰,۰۰۰ تومان"
                panel_price = 22000000

            layout_table.rows.clear()
            layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("مساحت کل")), ft.DataCell(ft.Text(f"{total_area:.1f} م²"))]))
            layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("فیلم ۸۰")), ft.DataCell(ft.Text(f"{film80:.1f} متر"))]))
            layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("فیلم ۴۰")), ft.DataCell(ft.Text(f"{film40:.1f} متر"))]))
            layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("عایق")), ft.DataCell(ft.Text(f"{insulation:.1f} م²"))]))
            layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("ترموستات")), ft.DataCell(ft.Text(f"{thermostats} عدد"))]))
            layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("تابلو فرمان")), ft.DataCell(ft.Text(panel_text))]))

            page.update()
            show_message("چیدمان محاسبه شد", "green")

        def calculate_full_invoice(e):
            if not layout_table.rows:
                show_message("ابتدا چیدمان را محاسبه کنید", "red")
                return
            # (کد محاسبه نهایی مثل قبل)
            show_message("ریز فاکتور آماده شد", "green")
            download_btn.visible = True
            page.update()

        return ft.Container(
            content=ft.Column([
                ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(18)), 
                       ft.Text("ورود دستی ابعاد اتاق‌ها", size=20, weight="bold")]),
                ft.Divider(),
                room_name, room_length, room_width,
                ft.FilledButton("اضافه کردن اتاق", width=350, bgcolor="#1565C0", on_click=add_room),
                ft.Divider(),
                ft.Text("اتاق‌های اضافه شده:", size=16, weight="bold"),
                rooms_list,
                ft.FilledButton("محاسبه چیدمان", width=350, bgcolor="#00A651", on_click=calculate_layout),
                ft.Divider(),
                ft.Text("نتایج چیدمان:", size=16, weight="bold"),
                layout_table,
                ft.Divider(),
                ft.Text("گزینه‌های جانبی:", size=16, weight="bold"),
                ft.Row([install_switch], alignment=ft.MainAxisAlignment.START), install_pct,
                ft.Row([travel_switch], alignment=ft.MainAxisAlignment.START), travel_cost,
                ft.Row([tax_switch], alignment=ft.MainAxisAlignment.START), tax_pct,
                ft.Row([discount_switch], alignment=ft.MainAxisAlignment.START), discount_pct,
                ft.Row([other_switch], alignment=ft.MainAxisAlignment.START), other_cost,
                ft.Divider(height=20),
                ft.FilledButton("محاسبه و نمایش ریز فاکتور", width=350, bgcolor="#1565C0", color="white", on_click=calculate_full_invoice),
                download_btn,
                ft.Divider(),
                ft.Text("ریز اقلام فاکتور:", size=16, weight="bold"),
                items_table,
                total_text
            ], scroll=ft.ScrollMode.AUTO, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )
         # ==================== روش اول: آپلود فایل DWG/DXF ====================
    def floor_dwg_upload_page():
        file_picker = ft.FilePicker()
        page.overlay.append(file_picker)

        uploaded_file_info = ft.Text("هیچ فایلی انتخاب نشده", color="grey")
        
        # جدول نتایج چیدمان
        layout_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("شرح")), ft.DataColumn(ft.Text("مقدار"))], rows=[])

        # گزینه‌های جانبی (کاملاً مشابه روش دوم)
        install_switch = ft.Switch(label="اضافه کردن هزینه نصب", value=False)
        install_pct = ft.Dropdown(label="درصد هزینه نصب", width=350, options=[
            ft.dropdown.Option("0"), ft.dropdown.Option("10"), ft.dropdown.Option("15"),
            ft.dropdown.Option("20"), ft.dropdown.Option("25")
        ], value="15", visible=False)

        travel_switch = ft.Switch(label="اضافه کردن هزینه ایاب و ذهاب", value=False)
        travel_cost = ft.TextField(label="مبلغ ایاب و ذهاب (تومان)", width=350, value="0", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        tax_switch = ft.Switch(label="اضافه کردن مالیات", value=False)
        tax_pct = ft.TextField(label="درصد مالیات", width=350, value="10", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        discount_switch = ft.Switch(label="اضافه کردن تخفیف", value=False)
        discount_pct = ft.TextField(label="درصد تخفیف", width=350, value="5", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        other_switch = ft.Switch(label="سایر هزینه‌ها", value=False)
        other_cost = ft.TextField(label="مبلغ سایر هزینه‌ها (تومان)", width=350, value="0", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        # جدول ریز اقلام فاکتور
        items_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("شرح کالا")), ft.DataColumn(ft.Text("مقدار")), ft.DataColumn(ft.Text("مبلغ"))], rows=[])
        total_text = ft.Text("جمع کل: 0 تومان", size=20, weight="bold", color="green")
        download_btn = ft.FilledButton("دانلود پیش‌فاکتور PDF", width=350, bgcolor="green", color="white", visible=False, icon=ft.Icons.DOWNLOAD)

        def update_visibility(e=None):
            install_pct.visible = install_switch.value
            travel_cost.visible = travel_switch.value
            tax_pct.visible = tax_switch.value
            discount_pct.visible = discount_switch.value
            other_cost.visible = other_switch.value
            page.update()

        install_switch.on_change = travel_switch.on_change = tax_switch.on_change = discount_switch.on_change = other_switch.on_change = update_visibility

        def on_file_selected(e):
            if e.files:
                file = e.files[0]
                uploaded_file_info.value = f"فایل انتخاب شد: {file.name}"
                uploaded_file_info.color = "green"
                page.update()

                show_message("فایل در حال پردازش توسط هسته main.py ...", "blue")
                page.update()

                try:
                    # شبیه‌سازی فراخوانی واقعی main.py
                    from main import process_dwg_file
                    result = process_dwg_file(file)

                    film80 = result.get("film_80", 45.5)
                    film40 = result.get("film_40", 12.3)
                    insulation = result.get("insulation", 68.0)
                    thermostats = result.get("thermostats", 5)

                except Exception as ex:
                    show_message(f"خطا در پردازش فایل: {ex}\n(از مقادیر تقریبی استفاده شد)", "orange")
                    film80 = 45.5
                    film40 = 12.3
                    insulation = 68.0
                    thermostats = 5

                # پیشنهاد تابلو فرمان
                if thermostats <= 4:
                    panel_text = "تابلو ۴ خروجی - ۱۲,۵۰۰,۰۰۰ تومان"
                    panel_price = 12500000
                elif thermostats <= 6:
                    panel_text = "تابلو ۶ خروجی - ۱۵,۵۰۰,۰۰۰ تومان"
                    panel_price = 15500000
                else:
                    panel_text = "تابلو ۱۰ خروجی - ۲۲,۰۰۰,۰۰۰ تومان"
                    panel_price = 22000000

                # پر کردن جدول نتایج چیدمان
                layout_table.rows.clear()
                layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("فیلم ۸۰")), ft.DataCell(ft.Text(f"{film80:.1f} متر"))]))
                layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("فیلم ۴۰")), ft.DataCell(ft.Text(f"{film40:.1f} متر"))]))
                layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("عایق")), ft.DataCell(ft.Text(f"{insulation:.1f} م²"))]))
                layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("ترموستات")), ft.DataCell(ft.Text(f"{thermostats} عدد"))]))
                layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("تابلو فرمان")), ft.DataCell(ft.Text(panel_text))]))

                page.update()
                show_message("پردازش فایل با موفقیت انجام شد", "green")

        file_picker.on_result = on_file_selected

        def calculate_full_invoice(e):
            if not layout_table.rows:
                show_message("ابتدا فایل را آپلود و پردازش کنید", "red")
                return

            try:
                # استخراج مقادیر از جدول چیدمان
                film80 = float(layout_table.rows[0].cells[1].content.value.split()[0])
                film40 = float(layout_table.rows[1].cells[1].content.value.split()[0])
                insulation = float(layout_table.rows[2].cells[1].content.value.split()[0])
                thermostats = int(layout_table.rows[3].cells[1].content.value.split()[0])
                panel_price = 15500000

                base = film80*1250000 + film40*950000 + insulation*1450000 + thermostats*1850000 + panel_price
                inst = base * (int(install_pct.value) / 100) if install_switch.value else 0
                travel = float(travel_cost.value or 0) if travel_switch.value else 0
                tax = (base + inst + travel) * (float(tax_pct.value or 10) / 100) if tax_switch.value else 0
                disc = (base + inst + travel) * (float(discount_pct.value or 0) / 100) if discount_switch.value else 0
                other = float(other_cost.value or 0) if other_switch.value else 0

                final_total = base + inst + travel + tax - disc + other

                # پر کردن جدول ریز اقلام
                items_table.rows.clear()
                items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("فیلم ۸۰")), ft.DataCell(ft.Text(f"{film80:.1f} م")), ft.DataCell(ft.Text(f"{film80*1250000:,.0f}"))]))
                items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("فیلم ۴۰")), ft.DataCell(ft.Text(f"{film40:.1f} م")), ft.DataCell(ft.Text(f"{film40*950000:,.0f}"))]))
                items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("عایق")), ft.DataCell(ft.Text(f"{insulation:.1f} م²")), ft.DataCell(ft.Text(f"{insulation*1450000:,.0f}"))]))
                items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("ترموستات")), ft.DataCell(ft.Text(f"{thermostats}")), ft.DataCell(ft.Text(f"{thermostats*1850000:,.0f}"))]))
                items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("تابلو فرمان")), ft.DataCell(ft.Text("۱")), ft.DataCell(ft.Text(f"{panel_price:,.0f}"))]))

                if inst > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("هزینه نصب")), ft.DataCell(ft.Text(f"{install_pct.value}%")), ft.DataCell(ft.Text(f"{inst:,.0f}"))]))
                if travel > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("ایاب و ذهاب")), ft.DataCell(ft.Text("")), ft.DataCell(ft.Text(f"{travel:,.0f}"))]))
                if tax > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("مالیات")), ft.DataCell(ft.Text(f"{tax_pct.value}%")), ft.DataCell(ft.Text(f"{tax:,.0f}"))]))
                if disc > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("تخفیف")), ft.DataCell(ft.Text(f"{discount_pct.value}%")), ft.DataCell(ft.Text(f"-{disc:,.0f}"))]))
                if other > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("سایر")), ft.DataCell(ft.Text("")), ft.DataCell(ft.Text(f"{other:,.0f}"))]))

                total_text.value = f"جمع کل: {final_total:,.0f} تومان"
                download_btn.visible = True
                page.update()
                show_message("ریز فاکتور کامل محاسبه شد", "green")

            except Exception as ex:
                show_message(f"خطا در محاسبه نهایی: {ex}", "red")

        return ft.Container(
            content=ft.Column([
                ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(18)),
                       ft.Text("آپلود فایل DWG / DXF", size=20, weight="bold")]),
                ft.Divider(),
                ft.FilledButton("انتخاب فایل DWG یا DXF", width=350, bgcolor="#1565C0", 
                               on_click=lambda e: file_picker.pick_files(allowed_extensions=["dwg", "dxf"])),
                uploaded_file_info,
                ft.Divider(),
                ft.Text("نتایج پردازش پلان:", size=16, weight="bold"),
                layout_table,
                ft.Divider(),
                ft.Text("گزینه‌های جانبی:", size=16, weight="bold"),
                ft.Row([install_switch], alignment=ft.MainAxisAlignment.START), install_pct,
                ft.Row([travel_switch], alignment=ft.MainAxisAlignment.START), travel_cost,
                ft.Row([tax_switch], alignment=ft.MainAxisAlignment.START), tax_pct,
                ft.Row([discount_switch], alignment=ft.MainAxisAlignment.START), discount_pct,
                ft.Row([other_switch], alignment=ft.MainAxisAlignment.START), other_cost,
                ft.Divider(height=20),
                ft.FilledButton("محاسبه و نمایش ریز فاکتور", width=350, bgcolor="#1565C0", color="white", on_click=calculate_full_invoice),
                download_btn,
                ft.Divider(),
                ft.Text("ریز اقلام فاکتور:", size=16, weight="bold"),
                items_table,
                total_text
            ], scroll=ft.ScrollMode.AUTO, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )
        # ==================== روش مقادیر مستقیم ====================
    def direct_values_page():
        m80 = ft.TextField(label="متراژ فیلم عرض ۸۰ (متر)", width=350, value="0", keyboard_type=ft.KeyboardType.NUMBER)
        m40 = ft.TextField(label="متراژ فیلم عرض ۴۰ (متر)", width=350, value="0", keyboard_type=ft.KeyboardType.NUMBER)
        xps = ft.TextField(label="متراژ عایق (مترمربع)", width=350, value="0", keyboard_type=ft.KeyboardType.NUMBER)
        thermostat = ft.TextField(label="تعداد ترموستات", width=350, value="1", keyboard_type=ft.KeyboardType.NUMBER)

        panel_type = ft.Dropdown(
            label="نوع تابلو فرمان",
            width=350,
            options=[
                ft.dropdown.Option("بدون تابلو - ۱۲,۵۰۰,۰۰۰ تومان"),
                ft.dropdown.Option("تابلو تیپ 1 - ۱۲,۵۰۰,۰۰۰ تومان"),
                ft.dropdown.Option("تابلو تیپ 2 - ۱۵,۵۰۰,۰۰۰ تومان"),
                ft.dropdown.Option("تابلو تیپ 3 - ۱۸,۵۰۰,۰۰۰ تومان"),
                ft.dropdown.Option("تابلو تیپ 4 - ۲۲,۰۰۰,۰۰۰ تومان"),
                ft.dropdown.Option("تابلو تیپ 5 - ۲۲,۰۰۰,۰۰۰ تومان"),
                ft.dropdown.Option("تابلو تیپ 6 - ۲۲,۰۰۰,۰۰۰ تومان"),
                ft.dropdown.Option("تابلو سفارشی - ۲۵,۰۰۰,۰۰۰ تومان"),
            ],
            value="تابلو تیپ 2 - ۱۵,۵۰۰,۰۰۰ تومان"
        )

        # گزینه‌های جانبی با سوئیچ
        install_switch = ft.Switch(label="اضافه کردن هزینه نصب", value=False)
        install_pct = ft.Dropdown(label="درصد هزینه نصب", width=350, options=[
            ft.dropdown.Option("0"), ft.dropdown.Option("10"), ft.dropdown.Option("15"),
            ft.dropdown.Option("20"), ft.dropdown.Option("25")
        ], value="15", visible=True)

        travel_switch = ft.Switch(label="اضافه کردن هزینه ایاب و ذهاب", value=False)
        travel_cost = ft.TextField(label="مبلغ ایاب و ذهاب (تومان)", width=350, value="0", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        tax_switch = ft.Switch(label="اضافه کردن مالیات", value=False)
        tax_pct = ft.TextField(label="درصد مالیات", width=350, value="10", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        discount_switch = ft.Switch(label="اضافه کردن تخفیف", value=False)
        discount_pct = ft.TextField(label="درصد تخفیف", width=350, value="5", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        other_switch = ft.Switch(label="سایر هزینه‌ها", value=False)
        other_cost = ft.TextField(label="مبلغ سایر هزینه‌ها (تومان)", width=350, value="0", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        items_table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("شرح کالا")), ft.DataColumn(ft.Text("مقدار")), ft.DataColumn(ft.Text("مبلغ (تومان)"))],
            rows=[]
        )
        total_text = ft.Text("جمع کل: 0 تومان", size=20, weight="bold", color="green")
        download_btn = ft.FilledButton("دانلود پیش‌فاکتور PDF", width=350, bgcolor="green", color="white", visible=False, icon=ft.Icons.DOWNLOAD)

        def update_visibility(e=None):
            install_pct.visible = install_switch.value
            travel_cost.visible = travel_switch.value
            tax_pct.visible = tax_switch.value
            discount_pct.visible = discount_switch.value
            other_cost.visible = other_switch.value
            page.update()

        # اتصال سوئیچ‌ها
        install_switch.on_change = update_visibility
        travel_switch.on_change = update_visibility
        tax_switch.on_change = update_visibility
        discount_switch.on_change = update_visibility
        other_switch.on_change = update_visibility

        # فراخوانی اولیه
        update_visibility()

        def calculate(e):
            try:
                m80v = float(m80.value or 0)
                m40v = float(m40.value or 0)
                xpsv = float(xps.value or 0)
                thv = int(thermostat.value or 1)

                # قیمت تابلو فرمان
                if "سفارشی" in panel_type.value:
                    panel_price = 25000000
                else:
                    try:
                        panel_price = float(panel_type.value.split("-")[-1].replace(",", "").replace("تومان", "").strip())
                    except:
                        panel_price = 15500000

                film80_total = m80v * 1250000
                film40_total = m40v * 950000
                xps_total = xpsv * 1450000
                thermostat_total = thv * 1850000
                panel_total = panel_price

                base = film80_total + film40_total + xps_total + thermostat_total + panel_total
                inst = base * (int(install_pct.value) / 100) if install_switch.value else 0
                travel = float(travel_cost.value or 0) if travel_switch.value else 0
                tax = (base + inst + travel) * (float(tax_pct.value or 10) / 100) if tax_switch.value else 0
                disc = (base + inst + travel) * (float(discount_pct.value or 0) / 100) if discount_switch.value else 0
                other = float(other_cost.value or 0) if other_switch.value else 0

                final_total = base + inst + travel + tax - disc + other

                # پر کردن جدول
                items_table.rows.clear()
                if m80v > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("فیلم گرمایشی ۸۰")), ft.DataCell(ft.Text(f"{m80v} متر")), ft.DataCell(ft.Text(f"{film80_total:,.0f}"))]))
                if m40v > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("فیلم گرمایشی ۴۰")), ft.DataCell(ft.Text(f"{m40v} متر")), ft.DataCell(ft.Text(f"{film40_total:,.0f}"))]))
                if xpsv > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("عایق بازتابشی")), ft.DataCell(ft.Text(f"{xpsv} مترمربع")), ft.DataCell(ft.Text(f"{xps_total:,.0f}"))]))
                if thv > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("ترموستات")), ft.DataCell(ft.Text(f"{thv} عدد")), ft.DataCell(ft.Text(f"{thermostat_total:,.0f}"))]))
                items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("تابلو فرمان")), ft.DataCell(ft.Text("۱ عدد")), ft.DataCell(ft.Text(f"{panel_total:,.0f}"))]))

                if inst > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("هزینه نصب")), ft.DataCell(ft.Text(f"{install_pct.value}%")), ft.DataCell(ft.Text(f"{inst:,.0f}"))]))
                if travel > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("ایاب و ذهاب")), ft.DataCell(ft.Text("")), ft.DataCell(ft.Text(f"{travel:,.0f}"))]))
                if tax > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("مالیات")), ft.DataCell(ft.Text(f"{tax_pct.value}%")), ft.DataCell(ft.Text(f"{tax:,.0f}"))]))
                if disc > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("تخفیف")), ft.DataCell(ft.Text(f"{discount_pct.value}%")), ft.DataCell(ft.Text(f"-{disc:,.0f}"))]))
                if other > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("سایر هزینه‌ها")), ft.DataCell(ft.Text("")), ft.DataCell(ft.Text(f"{other:,.0f}"))]))

                total_text.value = f"جمع کل: {final_total:,.0f} تومان"
                download_btn.visible = True
                page.update()
                show_message("ریز فاکتور محاسبه شد", "green")

            except Exception as ex:
                show_message(f"خطا: {ex}", "red")

        return ft.Container(
            content=ft.Column([
                ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(18)),
                       ft.Text("مقادیر مستقیم - پیش فاکتور", size=20, weight="bold")]),
                ft.Divider(),
                m80, m40, xps, thermostat, panel_type,
                ft.Divider(),
                ft.Row([install_switch], alignment=ft.MainAxisAlignment.START), install_pct,
                ft.Row([travel_switch], alignment=ft.MainAxisAlignment.START), travel_cost,
                ft.Row([tax_switch], alignment=ft.MainAxisAlignment.START), tax_pct,
                ft.Row([discount_switch], alignment=ft.MainAxisAlignment.START), discount_pct,
                ft.Row([other_switch], alignment=ft.MainAxisAlignment.START), other_cost,
                ft.Divider(height=20),
                ft.FilledButton("محاسبه و نمایش ریز فاکتور", width=350, bgcolor="#1565C0", color="white", on_click=calculate),
                download_btn,
                ft.Divider(),
                ft.Text("ریز اقلام فاکتور:", size=16, weight="bold"),
                items_table,
                total_text
            ], scroll=ft.ScrollMode.AUTO, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )
        # ==================== صفحه یخ زدایی رمپ ====================
    def ramp_deicing_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(1)),
                        ft.Text("یخ زدایی رمپ", size=21, weight="bold")
                    ]),
                    padding=15,
                    bgcolor="#f8f9fa",
                    border_radius=12
                ),
                ft.Text("روش صدور پیش‌فاکتور را انتخاب کنید",
                       size=18, weight="bold", text_align=ft.TextAlign.CENTER),
                ft.Divider(height=30),

                # روش ۱: آپلود فایل
                ft.Container(
                    content=ft.FilledButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.UPLOAD_FILE, color="white"),
                            ft.Text("📂 آپلود فایل DWG / DXF", size=16, weight="bold")
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        width=360, height=75, bgcolor="#1565C0", color="white",
                        on_click=lambda e: render(26),   # ← روش اول رمپ
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=18))
                    ),
                    margin=ft.margin.Margin(bottom=15)
                ),

                # روش ۲: ورود دستی ابعاد
                ft.Container(
                    content=ft.FilledButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.EDIT_NOTE, color="white"),
                            ft.Text("⌨️ ورود دستی ابعاد رمپ", size=16, weight="bold")
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        width=360, height=75, bgcolor="#1565C0", color="white",
                        on_click=lambda e: render(27),   # ← روش دوم رمپ
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=18))
                    ),
                    margin=ft.margin.Margin(bottom=15)
                ),

                # روش ۳: مقادیر مستقیم
                ft.Container(
                    content=ft.FilledButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CALCULATE, color="white"),
                            ft.Text("✍️ مقادیر مستقیم", size=16, weight="bold")
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        width=360, height=75, bgcolor="#1565C0", color="white",
                        on_click=lambda e: render(28),   # ← روش سوم رمپ
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=18))
                    )
                ),

                ft.Divider(height=30),
                ft.Text("هسته main.py و Financial.py آماده اتصال است",
                       size=13, color="grey", text_align=ft.TextAlign.CENTER)
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400,
            expand=True,
            padding=15
        )
        # ==================== یخ زدایی رمپ - روش اول: آپلود فایل ====================
    def ramp_deicing_dwg_page():
        file_picker = ft.FilePicker()
        page.overlay.append(file_picker)
        uploaded_file_info = ft.Text("هیچ فایلی انتخاب نشده", color="grey")

        layout_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("شرح")), ft.DataColumn(ft.Text("مقدار"))], rows=[])
        items_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("شرح کالا")), ft.DataColumn(ft.Text("مقدار")), ft.DataColumn(ft.Text("مبلغ"))], rows=[])
        total_text = ft.Text("جمع کل: 0 تومان", size=20, weight="bold", color="green")
        download_btn = ft.FilledButton("دانلود پیش‌فاکتور PDF", width=350, bgcolor="green", color="white", visible=False, icon=ft.Icons.DOWNLOAD)

        # گزینه‌های جانبی
        install_switch = ft.Switch(label="اضافه کردن هزینه نصب", value=False)
        install_pct = ft.Dropdown(label="درصد هزینه نصب", width=350, options=[ft.dropdown.Option(x) for x in ["0","10","15","20","25"]], value="15", visible=False)
        travel_switch = ft.Switch(label="اضافه کردن هزینه ایاب و ذهاب", value=False)
        travel_cost = ft.TextField(label="مبلغ ایاب و ذهاب (تومان)", width=350, value="0", visible=False, keyboard_type=ft.KeyboardType.NUMBER)
        tax_switch = ft.Switch(label="اضافه کردن مالیات", value=False)
        tax_pct = ft.TextField(label="درصد مالیات", width=350, value="10", visible=False, keyboard_type=ft.KeyboardType.NUMBER)
        discount_switch = ft.Switch(label="اضافه کردن تخفیف", value=False)
        discount_pct = ft.TextField(label="درصد تخفیف", width=350, value="5", visible=False, keyboard_type=ft.KeyboardType.NUMBER)
        other_switch = ft.Switch(label="سایر هزینه‌ها", value=False)
        other_cost = ft.TextField(label="مبلغ سایر هزینه‌ها (تومان)", width=350, value="0", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        def update_visibility(e=None):
            install_pct.visible = install_switch.value
            travel_cost.visible = travel_switch.value
            tax_pct.visible = tax_switch.value
            discount_pct.visible = discount_switch.value
            other_cost.visible = other_switch.value
            page.update()

        install_switch.on_change = travel_switch.on_change = tax_switch.on_change = discount_switch.on_change = other_switch.on_change = update_visibility

        def on_file_selected(e):
            if e.files:
                file = e.files[0]
                uploaded_file_info.value = f"فایل انتخاب شد: {file.name}"
                uploaded_file_info.color = "green"
                page.update()
                show_message("فایل در حال پردازش توسط هسته main.py ...", "blue")
                # شبیه‌سازی پردازش
                layout_table.rows.clear()
                layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("متراژ گرمکن رمپ")), ft.DataCell(ft.Text("۴۸.۵ متر"))]))
                layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("عایق")), ft.DataCell(ft.Text("۵۲ م²"))]))
                page.update()
                show_message("پردازش فایل با موفقیت انجام شد", "green")

        file_picker.on_result = on_file_selected

        def calculate_full_invoice(e):
            if not layout_table.rows:
                show_message("ابتدا فایل را آپلود کنید", "red")
                return
            show_message("ریز فاکتور آماده دانلود است", "green")
            download_btn.visible = True
            page.update()

        return ft.Container(
            content=ft.Column([
                ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(25)),
                       ft.Text("یخ زدایی رمپ - آپلود فایل", size=20, weight="bold")]),
                ft.Divider(),
                ft.FilledButton("انتخاب فایل DWG یا DXF", width=350, bgcolor="#1565C0", on_click=lambda e: file_picker.pick_files(allowed_extensions=["dwg", "dxf"])),
                uploaded_file_info,
                ft.Divider(),
                ft.Text("نتایج پردازش:", size=16, weight="bold"),
                layout_table,
                ft.Divider(),
                ft.Text("گزینه‌های جانبی:", size=16, weight="bold"),
                ft.Row([install_switch], alignment=ft.MainAxisAlignment.START), install_pct,
                ft.Row([travel_switch], alignment=ft.MainAxisAlignment.START), travel_cost,
                ft.Row([tax_switch], alignment=ft.MainAxisAlignment.START), tax_pct,
                ft.Row([discount_switch], alignment=ft.MainAxisAlignment.START), discount_pct,
                ft.Row([other_switch], alignment=ft.MainAxisAlignment.START), other_cost,
                ft.Divider(height=20),
                ft.FilledButton("محاسبه و نمایش ریز فاکتور", width=350, bgcolor="#1565C0", color="white", on_click=calculate_full_invoice),
                download_btn,
                ft.Divider(),
                ft.Text("ریز اقلام فاکتور:", size=16, weight="bold"),
                items_table,
                total_text
            ], scroll=ft.ScrollMode.AUTO, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )
            # ==================== یخ زدایی رمپ - روش دوم: ورود دستی ابعاد ====================
    def ramp_deicing_manual_page():
        rooms = []  # اینجا به جای اتاق، بخش‌های رمپ را ذخیره می‌کنیم

        section_name = ft.TextField(label="نام بخش رمپ", width=350, value="رمپ اصلی", text_align=ft.TextAlign.RIGHT)
        section_length = ft.TextField(label="طول رمپ (متر)", width=350, keyboard_type=ft.KeyboardType.NUMBER)
        section_width = ft.TextField(label="عرض رمپ (متر)", width=350, keyboard_type=ft.KeyboardType.NUMBER)

        sections_list = ft.Column(scroll=ft.ScrollMode.AUTO, height=150)

        layout_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("شرح")), ft.DataColumn(ft.Text("مقدار"))], rows=[])

        # گزینه‌های جانبی
        install_switch = ft.Switch(label="اضافه کردن هزینه نصب", value=False)
        install_pct = ft.Dropdown(label="درصد هزینه نصب", width=350, options=[ft.dropdown.Option(x) for x in ["0","10","15","20","25"]], value="15", visible=False)

        travel_switch = ft.Switch(label="اضافه کردن هزینه ایاب و ذهاب", value=False)
        travel_cost = ft.TextField(label="مبلغ ایاب و ذهاب (تومان)", width=350, value="0", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        tax_switch = ft.Switch(label="اضافه کردن مالیات", value=False)
        tax_pct = ft.TextField(label="درصد مالیات", width=350, value="10", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        discount_switch = ft.Switch(label="اضافه کردن تخفیف", value=False)
        discount_pct = ft.TextField(label="درصد تخفیف", width=350, value="5", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        other_switch = ft.Switch(label="سایر هزینه‌ها", value=False)
        other_cost = ft.TextField(label="مبلغ سایر هزینه‌ها (تومان)", width=350, value="0", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        items_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("شرح کالا")), ft.DataColumn(ft.Text("مقدار")), ft.DataColumn(ft.Text("مبلغ"))], rows=[])
        total_text = ft.Text("جمع کل: 0 تومان", size=20, weight="bold", color="green")
        download_btn = ft.FilledButton("دانلود پیش‌فاکتور PDF", width=350, bgcolor="green", color="white", visible=False, icon=ft.Icons.DOWNLOAD)

        def update_visibility(e=None):
            install_pct.visible = install_switch.value
            travel_cost.visible = travel_switch.value
            tax_pct.visible = tax_switch.value
            discount_pct.visible = discount_switch.value
            other_cost.visible = other_switch.value
            page.update()

        install_switch.on_change = travel_switch.on_change = tax_switch.on_change = discount_switch.on_change = other_switch.on_change = update_visibility

        def add_section(e):
            if not section_length.value or not section_width.value:
                show_message("طول و عرض رمپ را وارد کنید", "red")
                return
            try:
                length = float(section_length.value)
                width = float(section_width.value)
                area = length * width
                name = section_name.value or f"بخش {len(rooms)+1}"

                rooms.append({"name": name, "length": length, "width": width, "area": area})
                sections_list.controls.append(ft.Text(f"• {name}: {length} × {width} متر ({area:.1f} م²)"))
                
                section_length.value = ""
                section_width.value = ""
                page.update()
            except:
                show_message("مقادیر نامعتبر است", "red")

        def calculate_layout(e):
            if not rooms:
                show_message("ابتدا حداقل یک بخش اضافه کنید", "red")
                return

            total_area = sum(r["area"] for r in rooms)
            heating_length = total_area * 0.8   # فرض محاسباتی برای یخ‌زدایی
            insulation = total_area * 1.15

            layout_table.rows.clear()
            layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("مساحت کل رمپ")), ft.DataCell(ft.Text(f"{total_area:.1f} م²"))]))
            layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("متراژ گرمکن")), ft.DataCell(ft.Text(f"{heating_length:.1f} متر"))]))
            layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("عایق")), ft.DataCell(ft.Text(f"{insulation:.1f} م²"))]))
            layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("ترموستات")), ft.DataCell(ft.Text("۲ عدد"))]))

            page.update()
            show_message("چیدمان رمپ محاسبه شد", "green")

        def calculate_full_invoice(e):
            if not layout_table.rows:
                show_message("ابتدا چیدمان را محاسبه کنید", "red")
                return
            show_message("ریز فاکتور آماده شد", "green")
            download_btn.visible = True
            page.update()

        return ft.Container(
            content=ft.Column([
                ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(25)),
                       ft.Text("یخ زدایی رمپ - ابعاد دستی", size=20, weight="bold")]),
                ft.Divider(),
                section_name, section_length, section_width,
                ft.FilledButton("اضافه کردن بخش رمپ", width=350, bgcolor="#1565C0", on_click=add_section),
                ft.Divider(),
                ft.Text("بخش‌های اضافه شده:", size=16, weight="bold"),
                sections_list,
                ft.FilledButton("محاسبه چیدمان", width=350, bgcolor="#00A651", on_click=calculate_layout),
                ft.Divider(),
                ft.Text("نتایج چیدمان:", size=16, weight="bold"),
                layout_table,
                ft.Divider(),
                ft.Text("گزینه‌های جانبی:", size=16, weight="bold"),
                ft.Row([install_switch], alignment=ft.MainAxisAlignment.START), install_pct,
                ft.Row([travel_switch], alignment=ft.MainAxisAlignment.START), travel_cost,
                ft.Row([tax_switch], alignment=ft.MainAxisAlignment.START), tax_pct,
                ft.Row([discount_switch], alignment=ft.MainAxisAlignment.START), discount_pct,
                ft.Row([other_switch], alignment=ft.MainAxisAlignment.START), other_cost,
                ft.Divider(height=20),
                ft.FilledButton("محاسبه و نمایش ریز فاکتور", width=350, bgcolor="#1565C0", color="white", on_click=calculate_full_invoice),
                download_btn,
                ft.Divider(),
                ft.Text("ریز اقلام فاکتور:", size=16, weight="bold"),
                items_table,
                total_text
            ], scroll=ft.ScrollMode.AUTO, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )
            # ==================== یخ زدایی رمپ - روش سوم: مقادیر مستقیم ====================
    def ramp_deicing_direct_page():
        heating_length = ft.TextField(label="متراژ گرمکن رمپ (متر)", width=350, value="0", keyboard_type=ft.KeyboardType.NUMBER)
        insulation_area = ft.TextField(label="متراژ عایق (مترمربع)", width=350, value="0", keyboard_type=ft.KeyboardType.NUMBER)
        control_points = ft.TextField(label="تعداد نقطه کنترل / ترموستات", width=350, value="2", keyboard_type=ft.KeyboardType.NUMBER)

        items_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("شرح کالا")), ft.DataColumn(ft.Text("مقدار")), ft.DataColumn(ft.Text("مبلغ"))], rows=[])
        total_text = ft.Text("جمع کل: 0 تومان", size=20, weight="bold", color="green")
        download_btn = ft.FilledButton("دانلود پیش‌فاکتور PDF", width=350, bgcolor="green", color="white", visible=False, icon=ft.Icons.DOWNLOAD)

        # گزینه‌های جانبی
        install_switch = ft.Switch(label="اضافه کردن هزینه نصب", value=False)
        install_pct = ft.Dropdown(label="درصد هزینه نصب", width=350, options=[ft.dropdown.Option(x) for x in ["0","10","15","20","25"]], value="15", visible=False)
        travel_switch = ft.Switch(label="اضافه کردن هزینه ایاب و ذهاب", value=False)
        travel_cost = ft.TextField(label="مبلغ ایاب و ذهاب (تومان)", width=350, value="0", visible=False, keyboard_type=ft.KeyboardType.NUMBER)
        tax_switch = ft.Switch(label="اضافه کردن مالیات", value=False)
        tax_pct = ft.TextField(label="درصد مالیات", width=350, value="10", visible=False, keyboard_type=ft.KeyboardType.NUMBER)
        discount_switch = ft.Switch(label="اضافه کردن تخفیف", value=False)
        discount_pct = ft.TextField(label="درصد تخفیف", width=350, value="5", visible=False, keyboard_type=ft.KeyboardType.NUMBER)
        other_switch = ft.Switch(label="سایر هزینه‌ها", value=False)
        other_cost = ft.TextField(label="مبلغ سایر هزینه‌ها (تومان)", width=350, value="0", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        def update_visibility(e=None):
            install_pct.visible = install_switch.value
            travel_cost.visible = travel_switch.value
            tax_pct.visible = tax_switch.value
            discount_pct.visible = discount_switch.value
            other_cost.visible = other_switch.value
            page.update()

        install_switch.on_change = travel_switch.on_change = tax_switch.on_change = discount_switch.on_change = other_switch.on_change = update_visibility

        def calculate(e):
            try:
                length = float(heating_length.value or 0)
                insulation = float(insulation_area.value or 0)
                thermostats = int(control_points.value or 2)

                base = length * 1850000 + insulation * 1450000 + thermostats * 1850000
                inst = base * (int(install_pct.value) / 100) if install_switch.value else 0
                travel = float(travel_cost.value or 0) if travel_switch.value else 0
                tax = (base + inst + travel) * (float(tax_pct.value or 10) / 100) if tax_switch.value else 0
                disc = (base + inst + travel) * (float(discount_pct.value or 0) / 100) if discount_switch.value else 0
                other = float(other_cost.value or 0) if other_switch.value else 0

                final_total = base + inst + travel + tax - disc + other

                items_table.rows.clear()
                items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("گرمکن رمپ")), ft.DataCell(ft.Text(f"{length} متر")), ft.DataCell(ft.Text(f"{length*1850000:,.0f}"))]))
                items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("عایق")), ft.DataCell(ft.Text(f"{insulation} م²")), ft.DataCell(ft.Text(f"{insulation*1450000:,.0f}"))]))
                items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("ترموستات")), ft.DataCell(ft.Text(f"{thermostats} عدد")), ft.DataCell(ft.Text(f"{thermostats*1850000:,.0f}"))]))

                if inst > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("هزینه نصب")), ft.DataCell(ft.Text(f"{install_pct.value}%")), ft.DataCell(ft.Text(f"{inst:,.0f}"))]))
                if travel > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("ایاب و ذهاب")), ft.DataCell(ft.Text("")), ft.DataCell(ft.Text(f"{travel:,.0f}"))]))
                if tax > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("مالیات")), ft.DataCell(ft.Text(f"{tax_pct.value}%")), ft.DataCell(ft.Text(f"{tax:,.0f}"))]))
                if disc > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("تخفیف")), ft.DataCell(ft.Text(f"{discount_pct.value}%")), ft.DataCell(ft.Text(f"-{disc:,.0f}"))]))
                if other > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("سایر")), ft.DataCell(ft.Text("")), ft.DataCell(ft.Text(f"{other:,.0f}"))]))

                total_text.value = f"جمع کل: {final_total:,.0f} تومان"
                download_btn.visible = True
                page.update()
                show_message("ریز فاکتور محاسبه شد", "green")

            except Exception as ex:
                show_message(f"خطا: {ex}", "red")

        return ft.Container(
            content=ft.Column([
                ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(25)),
                       ft.Text("یخ زدایی رمپ - مقادیر مستقیم", size=20, weight="bold")]),
                ft.Divider(),
                heating_length, insulation_area, control_points,
                ft.Divider(),
                ft.Text("گزینه‌های جانبی:", size=16, weight="bold"),
                ft.Row([install_switch], alignment=ft.MainAxisAlignment.START), install_pct,
                ft.Row([travel_switch], alignment=ft.MainAxisAlignment.START), travel_cost,
                ft.Row([tax_switch], alignment=ft.MainAxisAlignment.START), tax_pct,
                ft.Row([discount_switch], alignment=ft.MainAxisAlignment.START), discount_pct,
                ft.Row([other_switch], alignment=ft.MainAxisAlignment.START), other_cost,
                ft.Divider(height=20),
                ft.FilledButton("محاسبه و نمایش ریز فاکتور", width=350, bgcolor="#1565C0", color="white", on_click=calculate),
                download_btn,
                ft.Divider(),
                ft.Text("ریز اقلام فاکتور:", size=16, weight="bold"),
                items_table,
                total_text
            ], scroll=ft.ScrollMode.AUTO, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )
    # ==================== صفحه یخ زدایی پله ====================
    def stair_deicing_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(1)),
                        ft.Text("یخ زدایی پله", size=21, weight="bold")
                    ]),
                    padding=15,
                    bgcolor="#f8f9fa",
                    border_radius=12
                ),
                ft.Text("روش صدور پیش‌فاکتور را انتخاب کنید",
                       size=18, weight="bold", text_align=ft.TextAlign.CENTER),
                ft.Divider(height=30),

                # روش ۱: آپلود فایل
                ft.Container(
                    content=ft.FilledButton(
                        content=ft.Row([ft.Icon(ft.Icons.UPLOAD_FILE, color="white"),
                                      ft.Text("📂 آپلود فایل DWG / DXF", size=16, weight="bold")],
                                      alignment=ft.MainAxisAlignment.CENTER),
                        width=360, height=75, bgcolor="#1565C0", color="white",
                        on_click=lambda e: render(30),   # روش اول پله
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=18))
                    ),
                    margin=ft.margin.Margin(bottom=15)
                ),

                # روش ۲: ورود دستی ابعاد
                ft.Container(
                    content=ft.FilledButton(
                        content=ft.Row([ft.Icon(ft.Icons.EDIT_NOTE, color="white"),
                                      ft.Text("⌨️ ورود دستی ابعاد پله", size=16, weight="bold")],
                                      alignment=ft.MainAxisAlignment.CENTER),
                        width=360, height=75, bgcolor="#1565C0", color="white",
                        on_click=lambda e: render(31),   # روش دوم پله
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=18))
                    ),
                    margin=ft.margin.Margin(bottom=15)
                ),

                # روش ۳: مقادیر مستقیم
                ft.Container(
                    content=ft.FilledButton(
                        content=ft.Row([ft.Icon(ft.Icons.CALCULATE, color="white"),
                                      ft.Text("✍️ مقادیر مستقیم", size=16, weight="bold")],
                                      alignment=ft.MainAxisAlignment.CENTER),
                        width=360, height=75, bgcolor="#1565C0", color="white",
                        on_click=lambda e: render(32),   # روش سوم پله
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=18))
                    )
                ),

                ft.Divider(height=30),
                ft.Text("هسته main.py و Financial.py آماده اتصال است",
                       size=13, color="grey", text_align=ft.TextAlign.CENTER)
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400,
            expand=True,
            padding=15
        )
            # ==================== یخ زدایی رمپ - روش اول: آپلود فایل ====================
    def stair_deicing_dwg_page():
        file_picker = ft.FilePicker()
        page.overlay.append(file_picker)
        uploaded_file_info = ft.Text("هیچ فایلی انتخاب نشده", color="grey")

        layout_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("شرح")), ft.DataColumn(ft.Text("مقدار"))], rows=[])
        items_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("شرح کالا")), ft.DataColumn(ft.Text("مقدار")), ft.DataColumn(ft.Text("مبلغ"))], rows=[])
        total_text = ft.Text("جمع کل: 0 تومان", size=20, weight="bold", color="green")
        download_btn = ft.FilledButton("دانلود پیش‌فاکتور PDF", width=350, bgcolor="green", color="white", visible=False, icon=ft.Icons.DOWNLOAD)

        # گزینه‌های جانبی
        install_switch = ft.Switch(label="اضافه کردن هزینه نصب", value=False)
        install_pct = ft.Dropdown(label="درصد هزینه نصب", width=350, options=[ft.dropdown.Option(x) for x in ["0","10","15","20","25"]], value="15", visible=False)
        travel_switch = ft.Switch(label="اضافه کردن هزینه ایاب و ذهاب", value=False)
        travel_cost = ft.TextField(label="مبلغ ایاب و ذهاب (تومان)", width=350, value="0", visible=False, keyboard_type=ft.KeyboardType.NUMBER)
        tax_switch = ft.Switch(label="اضافه کردن مالیات", value=False)
        tax_pct = ft.TextField(label="درصد مالیات", width=350, value="10", visible=False, keyboard_type=ft.KeyboardType.NUMBER)
        discount_switch = ft.Switch(label="اضافه کردن تخفیف", value=False)
        discount_pct = ft.TextField(label="درصد تخفیف", width=350, value="5", visible=False, keyboard_type=ft.KeyboardType.NUMBER)
        other_switch = ft.Switch(label="سایر هزینه‌ها", value=False)
        other_cost = ft.TextField(label="مبلغ سایر هزینه‌ها (تومان)", width=350, value="0", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        def update_visibility(e=None):
            install_pct.visible = install_switch.value
            travel_cost.visible = travel_switch.value
            tax_pct.visible = tax_switch.value
            discount_pct.visible = discount_switch.value
            other_cost.visible = other_switch.value
            page.update()

        install_switch.on_change = travel_switch.on_change = tax_switch.on_change = discount_switch.on_change = other_switch.on_change = update_visibility

        def on_file_selected(e):
            if e.files:
                file = e.files[0]
                uploaded_file_info.value = f"فایل انتخاب شد: {file.name}"
                uploaded_file_info.color = "green"
                page.update()
                show_message("فایل در حال پردازش توسط هسته main.py ...", "blue")
                # شبیه‌سازی پردازش
                layout_table.rows.clear()
                layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("متراژ گرمکن پله")), ft.DataCell(ft.Text("۴۸.۵ متر"))]))
                layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("عایق")), ft.DataCell(ft.Text("۵۲ م²"))]))
                page.update()
                show_message("پردازش فایل با موفقیت انجام شد", "green")

        file_picker.on_result = on_file_selected

        def calculate_full_invoice(e):
            if not layout_table.rows:
                show_message("ابتدا فایل را آپلود کنید", "red")
                return
            show_message("ریز فاکتور آماده دانلود است", "green")
            download_btn.visible = True
            page.update()

        return ft.Container(
            content=ft.Column([
                ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(29)),
                       ft.Text("یخ زدایی پله - آپلود فایل", size=20, weight="bold")]),
                ft.Divider(),
                ft.FilledButton("انتخاب فایل DWG یا DXF", width=350, bgcolor="#1565C0", on_click=lambda e: file_picker.pick_files(allowed_extensions=["dwg", "dxf"])),
                uploaded_file_info,
                ft.Divider(),
                ft.Text("نتایج پردازش:", size=16, weight="bold"),
                layout_table,
                ft.Divider(),
                ft.Text("گزینه‌های جانبی:", size=16, weight="bold"),
                ft.Row([install_switch], alignment=ft.MainAxisAlignment.START), install_pct,
                ft.Row([travel_switch], alignment=ft.MainAxisAlignment.START), travel_cost,
                ft.Row([tax_switch], alignment=ft.MainAxisAlignment.START), tax_pct,
                ft.Row([discount_switch], alignment=ft.MainAxisAlignment.START), discount_pct,
                ft.Row([other_switch], alignment=ft.MainAxisAlignment.START), other_cost,
                ft.Divider(height=20),
                ft.FilledButton("محاسبه و نمایش ریز فاکتور", width=350, bgcolor="#1565C0", color="white", on_click=calculate_full_invoice),
                download_btn,
                ft.Divider(),
                ft.Text("ریز اقلام فاکتور:", size=16, weight="bold"),
                items_table,
                total_text
            ], scroll=ft.ScrollMode.AUTO, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )
            # ==================== یخ زدایی پله - روش دوم: ورود دستی ابعاد ====================
    def stair_deicing_manual_page():
        sections = []   # بخش‌های پله

        stair_name = ft.TextField(label="نام پله / بخش", width=350, value="پله اصلی", text_align=ft.TextAlign.RIGHT)
        stair_length = ft.TextField(label="طول پله (متر)", width=350, keyboard_type=ft.KeyboardType.NUMBER)
        stair_width = ft.TextField(label="عرض پله (متر)", width=350, keyboard_type=ft.KeyboardType.NUMBER)
        num_steps = ft.TextField(label="تعداد پله", width=350, value="1", keyboard_type=ft.KeyboardType.NUMBER)

        sections_list = ft.Column(scroll=ft.ScrollMode.AUTO, height=150)

        layout_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("شرح")), ft.DataColumn(ft.Text("مقدار"))], rows=[])

        # گزینه‌های جانبی
        install_switch = ft.Switch(label="اضافه کردن هزینه نصب", value=False)
        install_pct = ft.Dropdown(label="درصد هزینه نصب", width=350, options=[ft.dropdown.Option(x) for x in ["0","10","15","20","25"]], value="15", visible=False)

        travel_switch = ft.Switch(label="اضافه کردن هزینه ایاب و ذهاب", value=False)
        travel_cost = ft.TextField(label="مبلغ ایاب و ذهاب (تومان)", width=350, value="0", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        tax_switch = ft.Switch(label="اضافه کردن مالیات", value=False)
        tax_pct = ft.TextField(label="درصد مالیات", width=350, value="10", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        discount_switch = ft.Switch(label="اضافه کردن تخفیف", value=False)
        discount_pct = ft.TextField(label="درصد تخفیف", width=350, value="5", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        other_switch = ft.Switch(label="سایر هزینه‌ها", value=False)
        other_cost = ft.TextField(label="مبلغ سایر هزینه‌ها (تومان)", width=350, value="0", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        items_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("شرح کالا")), ft.DataColumn(ft.Text("مقدار")), ft.DataColumn(ft.Text("مبلغ"))], rows=[])
        total_text = ft.Text("جمع کل: 0 تومان", size=20, weight="bold", color="green")
        download_btn = ft.FilledButton("دانلود پیش‌فاکتور PDF", width=350, bgcolor="green", color="white", visible=False, icon=ft.Icons.DOWNLOAD)

        def update_visibility(e=None):
            install_pct.visible = install_switch.value
            travel_cost.visible = travel_switch.value
            tax_pct.visible = tax_switch.value
            discount_pct.visible = discount_switch.value
            other_cost.visible = other_switch.value
            page.update()

        install_switch.on_change = travel_switch.on_change = tax_switch.on_change = discount_switch.on_change = other_switch.on_change = update_visibility

        def add_stair_section(e):
            if not stair_length.value or not stair_width.value:
                show_message("طول و عرض پله را وارد کنید", "red")
                return
            try:
                length = float(stair_length.value)
                width = float(stair_width.value)
                steps = int(num_steps.value or 1)
                area = length * width * steps
                name = stair_name.value or f"پله {len(sections)+1}"

                sections.append({"name": name, "length": length, "width": width, "steps": steps, "area": area})
                sections_list.controls.append(ft.Text(f"• {name}: {length}×{width} متر - {steps} پله ({area:.1f} م²)"))
                
                stair_length.value = ""
                stair_width.value = ""
                page.update()
            except:
                show_message("مقادیر نامعتبر است", "red")

        def calculate_layout(e):
            if not sections:
                show_message("ابتدا حداقل یک بخش پله اضافه کنید", "red")
                return

            total_area = sum(s["area"] for s in sections)
            heating_length = total_area * 0.75
            insulation = total_area * 1.2

            layout_table.rows.clear()
            layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("مساحت کل")), ft.DataCell(ft.Text(f"{total_area:.1f} م²"))]))
            layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("متراژ گرمکن")), ft.DataCell(ft.Text(f"{heating_length:.1f} متر"))]))
            layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("عایق")), ft.DataCell(ft.Text(f"{insulation:.1f} م²"))]))
            layout_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("ترموستات")), ft.DataCell(ft.Text("۳ عدد"))]))

            page.update()
            show_message("چیدمان پله محاسبه شد", "green")

        def calculate_full_invoice(e):
            if not layout_table.rows:
                show_message("ابتدا چیدمان را محاسبه کنید", "red")
                return
            show_message("ریز فاکتور آماده شد", "green")
            download_btn.visible = True
            page.update()

        return ft.Container(
            content=ft.Column([
                ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(29)),
                       ft.Text("یخ زدایی پله - ابعاد دستی", size=20, weight="bold")]),
                ft.Divider(),
                stair_name, stair_length, stair_width, num_steps,
                ft.FilledButton("اضافه کردن بخش پله", width=350, bgcolor="#1565C0", on_click=add_stair_section),
                ft.Divider(),
                ft.Text("بخش‌های اضافه شده:", size=16, weight="bold"),
                sections_list,
                ft.FilledButton("محاسبه چیدمان", width=350, bgcolor="#00A651", on_click=calculate_layout),
                ft.Divider(),
                ft.Text("نتایج چیدمان:", size=16, weight="bold"),
                layout_table,
                ft.Divider(),
                ft.Text("گزینه‌های جانبی:", size=16, weight="bold"),
                ft.Row([install_switch], alignment=ft.MainAxisAlignment.START), install_pct,
                ft.Row([travel_switch], alignment=ft.MainAxisAlignment.START), travel_cost,
                ft.Row([tax_switch], alignment=ft.MainAxisAlignment.START), tax_pct,
                ft.Row([discount_switch], alignment=ft.MainAxisAlignment.START), discount_pct,
                ft.Row([other_switch], alignment=ft.MainAxisAlignment.START), other_cost,
                ft.Divider(height=20),
                ft.FilledButton("محاسبه و نمایش ریز فاکتور", width=350, bgcolor="#1565C0", color="white", on_click=calculate_full_invoice),
                download_btn,
                ft.Divider(),
                ft.Text("ریز اقلام فاکتور:", size=16, weight="bold"),
                items_table,
                total_text
            ], scroll=ft.ScrollMode.AUTO, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )
            # ==================== یخ زدایی پله - روش سوم: مقادیر مستقیم ====================
    def stair_deicing_direct_page():
        heating_length = ft.TextField(label="متراژ گرمکن پله (متر)", width=350, value="0", keyboard_type=ft.KeyboardType.NUMBER)
        insulation_area = ft.TextField(label="متراژ عایق (مترمربع)", width=350, value="0", keyboard_type=ft.KeyboardType.NUMBER)
        num_thermostats = ft.TextField(label="تعداد ترموستات", width=350, value="2", keyboard_type=ft.KeyboardType.NUMBER)

        items_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("شرح کالا")), ft.DataColumn(ft.Text("مقدار")), ft.DataColumn(ft.Text("مبلغ"))], rows=[])
        total_text = ft.Text("جمع کل: 0 تومان", size=20, weight="bold", color="green")
        download_btn = ft.FilledButton("دانلود پیش‌فاکتور PDF", width=350, bgcolor="green", color="white", visible=False, icon=ft.Icons.DOWNLOAD)

        install_switch = ft.Switch(label="اضافه کردن هزینه نصب", value=False)
        install_pct = ft.Dropdown(label="درصد هزینه نصب", width=350, options=[ft.dropdown.Option(x) for x in ["0","10","15","20","25"]], value="15", visible=False)
        travel_switch = ft.Switch(label="اضافه کردن هزینه ایاب و ذهاب", value=False)
        travel_cost = ft.TextField(label="مبلغ ایاب و ذهاب (تومان)", width=350, value="0", visible=False, keyboard_type=ft.KeyboardType.NUMBER)
        tax_switch = ft.Switch(label="اضافه کردن مالیات", value=False)
        tax_pct = ft.TextField(label="درصد مالیات", width=350, value="10", visible=False, keyboard_type=ft.KeyboardType.NUMBER)
        discount_switch = ft.Switch(label="اضافه کردن تخفیف", value=False)
        discount_pct = ft.TextField(label="درصد تخفیف", width=350, value="5", visible=False, keyboard_type=ft.KeyboardType.NUMBER)
        other_switch = ft.Switch(label="سایر هزینه‌ها", value=False)
        other_cost = ft.TextField(label="مبلغ سایر هزینه‌ها (تومان)", width=350, value="0", visible=False, keyboard_type=ft.KeyboardType.NUMBER)

        def update_visibility(e=None):
            install_pct.visible = install_switch.value
            travel_cost.visible = travel_switch.value
            tax_pct.visible = tax_switch.value
            discount_pct.visible = discount_switch.value
            other_cost.visible = other_switch.value
            page.update()

        install_switch.on_change = travel_switch.on_change = tax_switch.on_change = discount_switch.on_change = other_switch.on_change = update_visibility

        def calculate(e):
            try:
                length = float(heating_length.value or 0)
                insulation = float(insulation_area.value or 0)
                thermostats = int(num_thermostats.value or 2)

                base = length * 1850000 + insulation * 1450000 + thermostats * 1850000
                inst = base * (int(install_pct.value) / 100) if install_switch.value else 0
                travel = float(travel_cost.value or 0) if travel_switch.value else 0
                tax = (base + inst + travel) * (float(tax_pct.value or 10) / 100) if tax_switch.value else 0
                disc = (base + inst + travel) * (float(discount_pct.value or 0) / 100) if discount_switch.value else 0
                other = float(other_cost.value or 0) if other_switch.value else 0

                final_total = base + inst + travel + tax - disc + other

                items_table.rows.clear()
                items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("گرمکن پله")), ft.DataCell(ft.Text(f"{length} متر")), ft.DataCell(ft.Text(f"{length*1850000:,.0f}"))]))
                items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("عایق")), ft.DataCell(ft.Text(f"{insulation} م²")), ft.DataCell(ft.Text(f"{insulation*1450000:,.0f}"))]))
                items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("ترموستات")), ft.DataCell(ft.Text(f"{thermostats} عدد")), ft.DataCell(ft.Text(f"{thermostats*1850000:,.0f}"))]))

                if inst > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("هزینه نصب")), ft.DataCell(ft.Text(f"{install_pct.value}%")), ft.DataCell(ft.Text(f"{inst:,.0f}"))]))
                if travel > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("ایاب و ذهاب")), ft.DataCell(ft.Text("")), ft.DataCell(ft.Text(f"{travel:,.0f}"))]))
                if tax > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("مالیات")), ft.DataCell(ft.Text(f"{tax_pct.value}%")), ft.DataCell(ft.Text(f"{tax:,.0f}"))]))
                if disc > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("تخفیف")), ft.DataCell(ft.Text(f"{discount_pct.value}%")), ft.DataCell(ft.Text(f"-{disc:,.0f}"))]))
                if other > 0: items_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("سایر")), ft.DataCell(ft.Text("")), ft.DataCell(ft.Text(f"{other:,.0f}"))]))

                total_text.value = f"جمع کل: {final_total:,.0f} تومان"
                download_btn.visible = True
                page.update()
                show_message("ریز فاکتور محاسبه شد", "green")

            except Exception as ex:
                show_message(f"خطا: {ex}", "red")

        return ft.Container(
            content=ft.Column([
                ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(29)),
                       ft.Text("یخ زدایی پله - مقادیر مستقیم", size=20, weight="bold")]),
                ft.Divider(),
                heating_length, insulation_area, num_thermostats,
                ft.Divider(),
                ft.Text("گزینه‌های جانبی:", size=16, weight="bold"),
                ft.Row([install_switch], alignment=ft.MainAxisAlignment.START), install_pct,
                ft.Row([travel_switch], alignment=ft.MainAxisAlignment.START), travel_cost,
                ft.Row([tax_switch], alignment=ft.MainAxisAlignment.START), tax_pct,
                ft.Row([discount_switch], alignment=ft.MainAxisAlignment.START), discount_pct,
                ft.Row([other_switch], alignment=ft.MainAxisAlignment.START), other_cost,
                ft.Divider(height=20),
                ft.FilledButton("محاسبه و نمایش ریز فاکتور", width=350, bgcolor="#1565C0", color="white", on_click=calculate),
                download_btn,
                ft.Divider(),
                ft.Text("ریز اقلام فاکتور:", size=16, weight="bold"),
                items_table,
                total_text
            ], scroll=ft.ScrollMode.AUTO, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
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
                ft.FilledButton("ثبت نهایی درخواست", bgcolor="#1565C0", color="white", on_click=lambda e: show_message("درخواست با موفقیت ثبت شد"))
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
                ft.FilledButton("بارگذاری ابعاد", on_click=load_sizes, bgcolor="#1565C0", color="white", width=350),
                product_size,
                product_qty,
                ft.FilledButton("افزودن به لیست", on_click=add_to_table, bgcolor="green", color="white", width=350),
                ft.Divider(),
                table,
                ft.FilledButton("اعلام کل موجودی و دانلود PDF", on_click=generate_and_download_pdf, bgcolor="blue", color="white", width=350, icon=ft.Icons.DOWNLOAD)
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
                ft.FilledButton("بارگذاری ابعاد", on_click=load_sizes, bgcolor="#1565C0", color="white", width=350),
                product_size,
                product_qty,
                ft.FilledButton("افزودن به لیست", on_click=add_to_table, bgcolor="green", color="white", width=350),
                ft.Divider(),
                table,
                ft.FilledButton("ثبت نهایی درخواست خرید و دانلود PDF", on_click=generate_purchase_pdf, bgcolor="#1565C0", color="white", width=350, icon=ft.Icons.DOWNLOAD)
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
                ft.FilledButton("درخواست تسویه حساب", bgcolor="#1565C0", color="white", width=350, on_click=lambda e: show_message("درخواست تسویه ارسال شد", "green"))
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
                ft.FilledButton("ارسال درخواست افزایش اعتبار", bgcolor="#1565C0", color="white", width=350, on_click=lambda e: show_message("درخواست افزایش اعتبار ارسال شد", "green"))
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
                ft.FilledButton("شما آخرین نسخه را دارید", bgcolor="green", color="white", width=350, on_click=lambda e: show_message("شما آخرین نسخه را نصب دارید", "green"))
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
                        ft.FilledButton("ورود به TopSUNify", width=340, bgcolor="#FFCC00", color="black", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)), on_click=lambda e: (setattr(page.session, 'logged_in', True), render())),
                        ft.TextButton("فعال‌سازی / فراموشی رمز", style=ft.ButtonStyle(color={"": "blue"})),
                        ft.Container(content=ft.Image(src="TopSUN-Powered.png", width=160), margin=ft.margin.Margin(top=50, bottom=30)),
                        ft.Container(content=ft.Image(src="landscape.jpg", width=400, height=220, fit="cover"), expand=True)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
                    width=400, margin=ft.margin.Margin(left=15, right=15), expand=True
                )
            )
        else:
            contents = [
                dashboard_page(),           # 0
                pre_invoice_page(),         # 1
                home_page(),                # 2
                technical_page(),           # 3
                profile_page(),             # 4
                settings_page(),            # 5
                account_request_page(),     # 6
                selected_customers_page(),  # 7
                inventory_page(),           # 8
                colleagues_page(),          # 9
                purchase_request_page(),    # 10
                commission_page(),          # 11
                credit_page(),              # 12
                theme_page(),               # 13
                update_page(),              # 14
                network_page(),             # 15
                rules_page(),               # 16
                about_page(),               # 17
                floor_heating_page(),       # 18
                floor_dwg_upload_page(),    # 19  ← آپلود فایل
                floor_manual_invoice_page(),# 20  ← زیرفرشی
                direct_values_page(),       # 21  ← مقادیر مستقیم
                radiator_manual_invoice_page(), # 22
                warranty_page(page, render), # 23
                floor_room_dimensions_page(),  # 24
                ramp_deicing_page(),        # 25
                ramp_deicing_dwg_page(),        # 26
                ramp_deicing_manual_page(),     # 27
                ramp_deicing_direct_page(),     # 28
                stair_deicing_page(),     # 29
                stair_deicing_dwg_page(),       # 30
                stair_deicing_manual_page(),    # 31
                stair_deicing_direct_page()     # 32
            
            ]

            main_content = ft.Container(
                content=contents[tab_index], 
                expand=True, 
                width=400, 
                margin=ft.margin.Margin(left=15, right=15)
            )

            nav_bar = ft.Container(
                content=ft.Row([
                    ft.Container(content=ft.Image(src="dashboard.png", width=32, height=32), on_click=lambda _: render(0), padding=8),
                    ft.Container(content=ft.Image(src="invoice.png", width=32, height=32), on_click=lambda _: render(1), padding=8),
                    ft.Container(content=ft.Image(src="TopSUNify-1.png", width=32, height=32), on_click=lambda _: render(2), padding=8),
                    ft.Container(content=ft.Image(src="technical.png", width=32, height=32), on_click=lambda _: render(3), padding=8),
                    ft.Container(content=ft.Image(src="profile.png", width=32, height=32), on_click=lambda _: render(4), padding=8),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                bgcolor="white", 
                padding=12
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

        view_button = ft.FilledButton("مشاهده اطلاعات این بازه", width=250, bgcolor="#1565C0", color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)), on_click=lambda e: show_message("در حال بارگذاری گزارش‌های مالی و عملیاتی..."))

        report_cards = ft.GridView(runs_count=2, max_extent=120, spacing=10, run_spacing=12, padding=10, expand=True)
        cards_data = [("فاکتورهای تسویه شده", ft.Icons.CHECK_CIRCLE, "#1976D2"), ("فاکتورهای فروش", ft.Icons.SHOPPING_CART, "#388E3C"), ("پیش فاکتورها", ft.Icons.RECEIPT_LONG, "#1565C0"), ("پروژه‌های نصب شده", ft.Icons.HOME_WORK, "#7B1FA2"), ("فاکتورهای باز", ft.Icons.PENDING, "#F57C00")]
        for title, icon, color in cards_data:
            report_cards.controls.append(ft.Container(content=ft.Column([ft.Icon(icon, size=36, color=color), ft.Text(title, size=13.5, weight="bold", text_align=ft.TextAlign.CENTER)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8), bgcolor="white", border_radius=16, padding=14, shadow=ft.BoxShadow(blur_radius=8, color="#e0e0e0"), expand=True, on_click=lambda e, t=title: show_message(f"بخش {t}"), ink=True))

        return ft.Container(content=ft.Column([ft.Container(content=ft.Dropdown(value="رضا تلچی", options=[ft.dropdown.Option("رضا تلچی"), ft.dropdown.Option("زیرمجموعه فروش")], width=320, border_radius=30, bgcolor="white"), margin=ft.margin.Margin(bottom=15)), ft.Text("انتخاب بازه زمانی", size=17, weight="bold", text_align=ft.TextAlign.CENTER), period_buttons, ft.Divider(height=10), view_button, ft.Divider(height=20), ft.Text("گزارش‌های مالی و عملیاتی", size=18, weight="bold", text_align=ft.TextAlign.CENTER), report_cards], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)
    # ==================== صفحات اصلی ====================
    def pre_invoice_page():
        products = [
            ("گرمایش از کف", lambda e: render(18)),
            ("زیرفرشی", lambda e: render(20)),
            ("رادیاتور", lambda e: render(22)),
            ("حوله خشک کن", lambda e: show_message("به زودی فعال می‌شود", "blue")),
            ("یخ زدایی رمپ", lambda e: render(25)),
            ("یخ زدایی پله", lambda e: render(29)),
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
        return ft.Container(content=ft.Column([ft.Container(content=ft.Column([ft.Image(src="TopSUNify-1.png", width=80), ft.Text("خوش آمدید به TopSUNify", size=18, weight="bold", text_align=ft.TextAlign.CENTER), ft.Text("مرکز خدمات و پشتیبانی", size=16, color="grey", text_align=ft.TextAlign.CENTER)], horizontal_alignment=ft.CrossAxisAlignment.CENTER), margin=ft.margin.Margin(top=20, bottom=30)), ft.Container(content=ft.Column([ft.ListTile(leading=ft.Icon(ft.Icons.SHIELD, color="green"), title=ft.Text("ثبت گارانتی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(23)), ft.ListTile(leading=ft.Icon(ft.Icons.INSTALL_DESKTOP, color="blue"), title=ft.Text("درخواست نصب اولیه"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.SUPPORT_AGENT, color="orange"), title=ft.Text("درخواست خدمات فنی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.SHOPPING_CART_CHECKOUT, color="purple"), title=ft.Text("ثبت درخواست سفارشی و عمده"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.PRINT, color="red"), title=ft.Text("درخواست چاپ طرح سفارشی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20))], spacing=2), width=380)], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)
    
    def warranty_page(page: ft.Page, render_callback):
        data = {
            "تهران": ["تهران", "شهریار", "ورامین"],
            "اصفهان": ["اصفهان", "کاشان", "خمینی‌شهر"],
            "خراسان رضوی": ["مشهد", "نیشابور"]
        }
        def check_national_id(id):
            if not re.match(r'^\d{10}$', id): return False
            check = int(id)
            s = sum(int(id[i]) * (10 - i) for i in range(9)) % 11
            return (s < 2 and check == s) or (s >= 2 and check == 11 - s)
        name = ft.TextField(label="نام و نام خانوادگی", width=350)
        father_name = ft.TextField(label="نام پدر", width=350)
        phone = ft.TextField(label="شماره موبایل", width=350, keyboard_type=ft.KeyboardType.PHONE)
        
        years = [str(y) for y in range(1300, 1410)]
        months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
                  "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
        
        birth_year = ft.Dropdown(label="سال تولد", width=110, options=[ft.dropdown.Option(y) for y in years], value="1370")
        birth_month = ft.Dropdown(label="ماه", width=110, options=[ft.dropdown.Option(m) for m in months], value="فروردین")
        birth_day = ft.Dropdown(label="روز", width=110, options=[ft.dropdown.Option(str(d)) for d in range(1, 32)], value="1")
        
        def get_birth_date():
            return f"{birth_year.value}/{birth_month.value}/{birth_day.value}"
        
        birth_date_display = ft.TextField(
            label="تاریخ تولد شمسی", 
            width=350, 
            value="1370/فروردین/1",
            read_only=True
        )
        
        def update_birth_display(e):
            birth_date_display.value = get_birth_date()
            birth_date_display.update()
            
            birth_year.on_change = update_birth_display
            birth_month.on_change = update_birth_display
            birth_day.on_change = update_birth_display

        national_id = ft.TextField(label="کد ملی", width=350, keyboard_type=ft.KeyboardType.NUMBER)
        province_label = ft.Text("استان محل صدور: نامشخص", color="blue")
            
        def on_national_id_change(e):
            if check_national_id(national_id.value):
                province_label.value = "استان شناسایی شد: (مثال: تهران)"
            else:
                province_label.value = "کد ملی نامعتبر است"
            province_label.update()
        national_id.on_change = on_national_id_change
            
        id_number = ft.TextField(label="شماره شناسنامه", width=350)
        product_code = ft.TextField(label="کد محصول", width=350)
        postal_code = ft.TextField(label="کد پستی (۱۰ رقم)", width=350, keyboard_type=ft.KeyboardType.NUMBER)
            
        provinces = {"تهران": ["تهران", "شهریار", "کرج"], "اصفهان": ["اصفهان", "کاشان"]} # نمونه
        province_dropdown = ft.Dropdown(label="استان", width=350, options=[ft.dropdown.Option(p) for p in provinces.keys()])
        city_dropdown = ft.Dropdown(label="شهر", width=350, options=[])
        def load_cities(e):
            if province_dropdown.value in data:
                city_dropdown.options = [ft.dropdown.Option(c) for c in data[province_dropdown.value]]
                city_dropdown.update()
        btn_load_cities = ft.OutlinedButton("بارگذاری شهرهای استان", on_click=load_cities)
        
        address = ft.TextField(label="آدرس کامل", width=350, multiline=True)
        
        purchase_place = ft.Dropdown(label="محل خرید", width=350, options=[
            ft.dropdown.Option("سایت شرکت"), ft.dropdown.Option("دفتر مرکزی"), ft.dropdown.Option("فروشگاه یا نمایندگی")
        ])
        shop_name = ft.TextField(label="نام فروشگاه یا نمایندگی", width=350, visible=False)
        
        invoice_number = ft.TextField(label="شماره فاکتور", width=350)
        serial_number = ft.TextField(label="شماره سریال محصول", width=350)
        purchase_date = ft.TextField(label="تاریخ خرید", width=350)  
        
        def on_purchase_change(e):
            shop_name.visible = (purchase_place.value == "فروشگاه یا نمایندگی")
            shop_name.update()
        purchase_place.on_change = on_purchase_change
            
        def submit(e):
            if not birth_date_field.value:
                page.show_snack_bar(ft.SnackBar(ft.Text("لطفاً تاریخ تولد را انتخاب کنید!")))
                return
                
            if not check_national_id(national_id.value):
                page.show_snack_bar(ft.SnackBar(ft.Text("کد ملی نامعتبر است!")))
                return
                
            if len(postal_code.value) != 10:
                page.show_snack_bar(ft.SnackBar(ft.Text("کد پستی باید ۱۰ رقم باشد!")))
                return
                
            page.show_snack_bar(ft.SnackBar(ft.Text("اطلاعات با موفقیت ثبت شد.")))
                
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(2)),
                    ft.Text("ثبت گارانتی", size=20, weight="bold")
                ]),
                name, father_name, birth_date_field, national_id, province_label, id_number,
                province_dropdown, city_dropdown, address, postal_code,
                purchase_place, shop_name, invoice_number, serial_number, purchase_date,
                ft.FilledButton("ثبت نهایی", on_click=submit)
            ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=15
        )
    def technical_page():
        return ft.Container(content=ft.Column([ft.Container(content=ft.Text("اطلاعات فنی", size=18, weight="bold", text_align=ft.TextAlign.CENTER), padding=20, margin=ft.margin.Margin(bottom=15)), ft.Container(content=ft.Column([ft.ListTile(leading=ft.Icon(ft.Icons.BOOK, color="blue"), title=ft.Text("کاتالوگ محصولات"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.PRICE_CHANGE, color="green"), title=ft.Text("لیست قیمت"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.WORK_HISTORY, color="purple"), title=ft.Text("رزومه شرکت"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.DESCRIPTION, color="orange"), title=ft.Text("پروپوزال و گزارش فنی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.IMAGE, color="pink"), title=ft.Text("تصاویر و فیلم پروژه‌ها"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.VIDEO_LIBRARY, color="red"), title=ft.Text("فیلم‌های تبلیغاتی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20))], spacing=2), width=380)], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)

    def settings_page():
        return ft.Container(content=ft.Column([ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("تنظیمات", size=24, weight="bold")]), padding=15, bgcolor="#f8f9fa", border_radius=20, margin=ft.margin.Margin(bottom=20)), ft.Column([ft.ListTile(leading=ft.Icon(ft.Icons.PERSON), title=ft.Text("تغییر نام کاربری"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.SAVE), title=ft.Text("ذخیره نام کاربری"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.FINGERPRINT), title=ft.Text("ورود با اثر انگشت"), trailing=ft.Switch(value=False)), ft.ListTile(leading=ft.Icon(ft.Icons.LOCK), title=ft.Text("تغییر رمز ورود"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.PHONE), title=ft.Text("تغییر شماره تلفن همراه"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.DEVICES), title=ft.Text("دستگاه‌های فعال"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.Divider(height=20), ft.ListTile(leading=ft.Icon(ft.Icons.DELETE_FOREVER, color="red"), title=ft.Text("حذف تنظیمات و خروج از نرم‌افزار", color="red"), on_click=lambda e: (setattr(page.session, 'logged_in', False), render()))], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER)]), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)

    render()


if __name__ == "__main__":
    # دریافت پورت از Render (اگر تنظیم نشده بود، پیش‌فرض 8080)
    port = int(os.environ.get("PORT", 8000))
    
    # اجرای برنامه برای وب
    ft.app(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        port=int(port), # اطمینان حاصل کنید که پورت عدد صحیح است
        host="0.0.0.0"
    )


