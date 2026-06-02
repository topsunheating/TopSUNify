import flet as ft
import os
import datetime

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
        page.session.inventory_list = []

    def show_message(text: str, color="green"):
        snack = ft.SnackBar(content=ft.Text(text), bgcolor=color, action="بستن", duration=3000)
        page.snack_bar = snack
        snack.open = True
        page.update()

    def toggle_theme(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()

    # ==================== صفحات اضافی ====================
    def inventory_page():
        # ... (همان کد قبلی شما - بدون تغییر)
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
        return ft.Container(content=ft.Column([ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("مشتریان منتخب", size=20, weight="bold")]), padding=10), ft.ListView(controls=[ft.ListTile(leading=ft.Icon(ft.Icons.PERSON, color="blue"), title=ft.Text("مشتری نمونه ۱")), ft.ListTile(leading=ft.Icon(ft.Icons.PERSON, color="blue"), title=ft.Text("مشتری نمونه ۲"))], expand=True)], scroll=ft.ScrollMode.AUTO), width=400, expand=True)

    def colleagues_page():
        all_colleagues = [{"code": "101", "name": "علی علوی", "company": "شرکت آلفا", "phone": "09120000000", "city": "تهران"}, {"code": "102", "name": "رضا رضایی", "company": "تکنو صنعت", "phone": "09130000000", "city": "اصفهان"}]
        table = ft.DataTable(columns=[ft.DataColumn(ft.Text("کد")), ft.DataColumn(ft.Text("نام")), ft.DataColumn(ft.Text("مجموعه")), ft.DataColumn(ft.Text("تماس")), ft.DataColumn(ft.Text("شهر"))], rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(c["code"])), ft.DataCell(ft.Text(c["name"])), ft.DataCell(ft.Text(c["company"])), ft.DataCell(ft.Text(c["phone"])), ft.DataCell(ft.Text(c["city"]))]) for c in all_colleagues])
        return ft.Container(content=ft.Column([ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("همکاران منتخب", size=20, weight="bold")]), padding=10), table], scroll=ft.ScrollMode.AUTO), width=400, expand=True)

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
            new_row = ft.DataRow(cells=[ft.DataCell(ft.Text(product_name.value)), ft.DataCell(ft.Text(product_size.value)), ft.DataCell(ft.Text(product_qty.value)), ft.DataCell(ft.IconButton(ft.Icons.DELETE, icon_color="red", on_click=lambda _: (table.rows.remove(new_row), page.update())))])
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

    def account_request_page():
        return ft.Container(content=ft.Column([ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("فرم درخواست همکاری", size=20, weight="bold")]), padding=10), ft.TextField(label="نام و نام خانوادگی", text_align=ft.TextAlign.RIGHT), ft.TextField(label="نام پدر", text_align=ft.TextAlign.RIGHT), ft.TextField(label="تاریخ تولد", text_align=ft.TextAlign.RIGHT), ft.TextField(label="شماره شناسنامه", text_align=ft.TextAlign.RIGHT), ft.TextField(label="شماره ملی", text_align=ft.TextAlign.RIGHT), ft.Dropdown(label="نوع درخواست", options=[ft.dropdown.Option(i) for i in ["نماینده فروش","عامل فروش","کارشناس فروش","نصاب فنی"]]), ft.ElevatedButton("ثبت نهایی درخواست", bgcolor="#1565C0", color="white", on_click=lambda e: show_message("درخواست با موفقیت ثبت شد"))], scroll=ft.ScrollMode.AUTO), padding=20, width=400, expand=True)

    # ==================== صفحات اصلی ====================
    def pre_invoice_page():
        products = ["گرمایش از کف", "زیرفرشی", "رادیاتور", "حوله خشک کن", "یخ زدایی رمپ", "یخ زدایی پله", "گرمکن مخزن", "گرمکن صندلی", "رستورانی", "عایق بازتابشی"]
        grid = ft.GridView(runs_count=2, max_extent=120, spacing=10, run_spacing=12, padding=10, expand=True)
        for name in products:
            grid.controls.append(ft.Container(content=ft.Text(name, size=15, weight="bold", text_align=ft.TextAlign.CENTER, color="#1565C0"), width=170, height=70, bgcolor="#ffffff", border_radius=12, alignment=ft.Alignment(0, 0), shadow=ft.BoxShadow(blur_radius=6, color="#e0e0e0"), on_click=lambda e, n=name: show_message(f"پیش‌فاکتور {n}"), ink=True))
        return ft.Container(content=ft.Column([ft.Text("نوع محصول مورد نظر را انتخاب کنید", size=18, weight="bold", text_align=ft.TextAlign.CENTER), ft.Divider(height=10), grid], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)

    def home_page():
        return ft.Container(content=ft.Column([ft.Container(content=ft.Column([ft.Image(src="TopSUNify-1.png", width=80), ft.Text("خوش آمدید به TopSUNify", size=18, weight="bold", text_align=ft.TextAlign.CENTER), ft.Text("مرکز خدمات و پشتیبانی", size=16, color="grey", text_align=ft.TextAlign.CENTER)], horizontal_alignment=ft.CrossAxisAlignment.CENTER), margin=ft.margin.Margin(top=20, bottom=30)), ft.Container(content=ft.Column([ft.ListTile(leading=ft.Icon(ft.Icons.SHIELD, color="green"), title=ft.Text("ثبت گارانتی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.INSTALL_DESKTOP, color="blue"), title=ft.Text("درخواست نصب اولیه"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.SUPPORT_AGENT, color="orange"), title=ft.Text("درخواست خدمات فنی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.SHOPPING_CART_CHECKOUT, color="purple"), title=ft.Text("ثبت درخواست سفارشی و عمده"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.PRINT, color="red"), title=ft.Text("درخواست چاپ طرح سفارشی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20))], spacing=2), width=380)], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)

    def technical_page():
        return ft.Container(content=ft.Column([ft.Container(content=ft.Text("اطلاعات فنی", size=18, weight="bold", text_align=ft.TextAlign.CENTER), padding=20, margin=ft.margin.Margin(bottom=15)), ft.Container(content=ft.Column([ft.ListTile(leading=ft.Icon(ft.Icons.BOOK, color="blue"), title=ft.Text("کاتالوگ محصولات"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.PRICE_CHANGE, color="green"), title=ft.Text("لیست قیمت"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.WORK_HISTORY, color="purple"), title=ft.Text("رزومه شرکت"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.DESCRIPTION, color="orange"), title=ft.Text("پروپوزال و گزارش فنی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.IMAGE, color="pink"), title=ft.Text("تصاویر و فیلم پروژه‌ها"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.VIDEO_LIBRARY, color="red"), title=ft.Text("فیلم‌های تبلیغاتی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20))], spacing=2), width=380)], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)

    def settings_page():
        return ft.Container(content=ft.Column([ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("تنظیمات", size=24, weight="bold")]), padding=15, bgcolor="#f8f9fa", border_radius=20, margin=ft.margin.Margin(bottom=20)), ft.Column([ft.ListTile(leading=ft.Icon(ft.Icons.PERSON), title=ft.Text("تغییر نام کاربری"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.SAVE), title=ft.Text("ذخیره نام کاربری"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.FINGERPRINT), title=ft.Text("ورود با اثر انگشت"), trailing=ft.Switch(value=False)), ft.ListTile(leading=ft.Icon(ft.Icons.LOCK), title=ft.Text("تغییر رمز ورود"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.PHONE), title=ft.Text("تغییر شماره تلفن همراه"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.DEVICES), title=ft.Text("دستگاه‌های فعال"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.Divider(height=20), ft.ListTile(leading=ft.Icon(ft.Icons.DELETE_FOREVER, color="red"), title=ft.Text("حذف تنظیمات و خروج از نرم‌افزار", color="red"), on_click=lambda e: (setattr(page.session, 'logged_in', False), render()))], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER)]), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)

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
                    ft.ListTile(leading=ft.Icon(ft.Icons.PERCENT), title=ft.Text("محاسبه درصد همکاری"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET), title=ft
