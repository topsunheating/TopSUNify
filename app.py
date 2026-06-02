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

    # تعریف توابع خالی برای جلوگیری از NameError
    def dashboard_page(): return ft.Container(content=ft.Text("داشبورد"))
    def pre_invoice_page(): return ft.Container(content=ft.Text("پیش فاکتور"))
    def home_page(): return ft.Container(content=ft.Text("خانه"))
    def technical_page(): return ft.Container(content=ft.Text("فنی"))
    def settings_page(): return ft.Container(content=ft.Text("تنظیمات"))

    # ==================== صفحات شما ====================
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

    def commission_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("محاسبه درصد همکاری", size=20, weight="bold")]), padding=10),
                ft.Text("فاکتورهای تسویه شده این ماه: ۴۸,۵۰۰,۰۰۰ تومان", size=16),
                ft.Text("درصد همکاری شما: ۱۲٪", size=22, weight="bold", color="blue"),
                ft.Text("مبلغ قابل تسویه: ۵,۸۲۰,۰۰۰ تومان", size=18, weight="bold", color="green"),
                ft.ElevatedButton("درخواست تسویه حساب", bgcolor="#1565C0", color="white", width=350, on_click=lambda e: show_message("درخواست تسویه به مدیران ارسال شد", "green"))
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
                ft.ElevatedButton("ارسال درخواست افزایش اعتبار", bgcolor="#1565C0", color="white", width=350, on_click=lambda e: show_message("درخواست افزایش اعتبار به مدیران ارسال شد", "green"))
            ], scroll=ft.ScrollMode.AUTO, spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )

    def theme_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("نمایش (تم)", size=20, weight="bold")]), padding=10),
                ft.ListTile(leading=ft.Icon(ft.Icons.LIGHT_MODE), title=ft.Text("تم روشن"), on_click=lambda e: (setattr(page, 'theme_mode', 'light'), page.update(), show_message("تم روشن فعال شد", "blue"))),
                ft.ListTile(leading=ft.Icon(ft.Icons.DARK_MODE), title=ft.Text("تم تیره"), on_click=lambda e: (setattr(page, 'theme_mode', 'dark'), page.bgcolor="#1e1e1e", page.update(), show_message("تم تیره فعال شد", "blue")))
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
                ft.Text("• بهبود سرعت بارگذاری صفحات\n• رفع باگ PDF\n• اضافه شدن صفحه محاسبه درصد همکاری", size=15),
                ft.Divider(),
                ft.Text("نسخه ۱.۴.۴ - ۱۴۰۴/۰۲/۲۵", size=16, weight="bold"),
                ft.Text("• بهینه‌سازی تم تیره", size=15),
                ft.ElevatedButton("شما آخرین نسخه را دارید", bgcolor="green", color="white", width=350, on_click=lambda e: show_message("شما آخرین نسخه اپلیکیشن را نصب دارید", "green"))
            ], scroll=ft.ScrollMode.AUTO, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )

    def network_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("شبکه فروش و خدمات", size=20, weight="bold")]), padding=10),
                ft.Text("نقشه شبکه فروش و خدمات همکاران", size=16, text_align=ft.TextAlign.CENTER)
            ], scroll=ft.ScrollMode.AUTO, spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )

    def rules_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("قوانین همکاری", size=20, weight="bold")]), padding=10),
                ft.Text("متن کامل قوانین و شرایط همکاری", size=16, text_align=ft.TextAlign.CENTER)
            ], scroll=ft.ScrollMode.AUTO, spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )

    def about_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("درباره ما", size=20, weight="bold")]), padding=10),
                ft.Text("شرکت تاپسان\nتولیدکننده سیستم‌های گرمایشی پیشرفته", size=16, text_align=ft.TextAlign.CENTER)
            ], scroll=ft.ScrollMode.AUTO, spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )

    def profile_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Column([ft.CircleAvatar(foreground_image_src="https://i.pravatar.cc/150?u=reza", radius=48), ft.Text("کاربر سیستم", size=20, weight="bold")], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=20, bgcolor="#f8f9fa", border_radius=20, margin=ft.margin.Margin(bottom=20), width=380),
                ft.Container(content=ft.Column([
                    ft.ListTile(leading=ft.Icon(ft.Icons.PERSON_ADD), title=ft.Text("درخواست ایجاد حساب"), on_click=lambda e: render(6)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.STAR), title=ft.Text("مشتریان منتخب"), on_click=lambda e: render(7)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.WAREHOUSE), title=ft.Text("اعلام موجودی انبار"), on_click=lambda e: render(8)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.SHOPPING_CART), title=ft.Text("ثبت درخواست خرید"), on_click=lambda e: render(10)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.GROUP), title=ft.Text("همکاران منتخب"), on_click=lambda e: render(9)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.LOGOUT), title=ft.Text("خروج"), on_click=lambda e: (setattr(page.session, 'logged_in', False), render()))
                ], spacing=2), width=360)
            ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True
        )

    # ==================== رندر اصلی ====================
    def render(tab_index=0):
        page.controls.clear()
        if not page.session.logged_in:
            page.add(ft.Container(content=ft.Column([ft.Text("ورود"), ft.ElevatedButton("ورود", on_click=lambda e: (setattr(page.session, 'logged_in', True), render()))], horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=400))
        else:
            contents = [
                dashboard_page(), pre_invoice_page(), home_page(), technical_page(),
                profile_page(), settings_page(), account_request_page(),
                selected_customers_page(), inventory_page(), colleagues_page(),
                purchase_request_page(), commission_page(), credit_page(),
                theme_page(), update_page(), network_page(), rules_page(), about_page()
            ]
            page.add(ft.Column([
                ft.Container(content=contents[tab_index], expand=True, width=400),
                ft.Row([ft.TextButton("داشبورد", on_click=lambda _: render(0)), ft.TextButton("پروفایل", on_click=lambda _: render(4))], alignment=ft.MainAxisAlignment.CENTER)
            ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        page.update()

    render()

if __name__ == "__main__":
    ft.app(target=main, port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", assets_dir="assets")
