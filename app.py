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

    # --- صفحات برنامه ---

    def inventory_page():
        product_name = ft.TextField(label="نام محصول", width=350)
        product_size = ft.TextField(label="ابعاد محصول", width=350)
        product_qty = ft.TextField(label="تعداد موجودی", width=350, keyboard_type=ft.KeyboardType.NUMBER)
        
        # استفاده از ListView برای رفع خطای قبلی
        lv = ft.ListView(expand=1, spacing=10, padding=20)
        
        table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("نام")), ft.DataColumn(ft.Text("ابعاد")), ft.DataColumn(ft.Text("تعداد"))],
            rows=[]
        )
        lv.controls.append(table)

        def add_to_table(e):
            if product_name.value and product_qty.value:
                new_row = ft.DataRow(cells=[
                    ft.DataCell(ft.Text(product_name.value)),
                    ft.DataCell(ft.Text(product_size.value)),
                    ft.DataCell(ft.Text(product_qty.value))
                ])
                table.rows.append(new_row)
                page.session.inventory_list.append({"name": product_name.value, "qty": product_qty.value})
                product_name.value = ""
                product_size.value = ""
                product_qty.value = ""
                page.update()
            else:
                show_message("لطفاً نام و تعداد را وارد کنید", "red")

        def finalize_inventory(e):
            show_message(f"فایل موجودی با تاریخ {datetime.date.today()} برای مدیر ارسال شد")
            page.session.inventory_list = []
            table.rows = []
            page.update()

        return ft.Container(content=ft.Column([
            ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("اعلام موجودی انبار", size=20, weight="bold")]), padding=10),
            product_name, product_size, product_qty,
            ft.ElevatedButton("تایید موجودی", on_click=add_to_table, bgcolor="green", color="white"),
            ft.Divider(),
            ft.Container(content=lv, height=250),
            ft.ElevatedButton("اعلام کل موجودی", on_click=finalize_inventory, bgcolor="blue", color="white", width=350)
        ], scroll=ft.ScrollMode.AUTO), width=400, expand=True)

    def selected_customers_page():
        return ft.Container(content=ft.Column([
            ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("مشتریان منتخب", size=20, weight="bold")]), padding=10),
            ft.DataTable(columns=[ft.DataColumn(ft.Text("کد")), ft.DataColumn(ft.Text("نام")), ft.DataColumn(ft.Text("تماس")), ft.DataColumn(ft.Text("شهر"))], rows=[ft.DataRow(cells=[ft.DataCell(ft.Text("101")), ft.DataCell(ft.Text("رضا احمدی")), ft.DataCell(ft.Text("09121234567")), ft.DataCell(ft.Text("تهران"))])])
        ], scroll=ft.ScrollMode.AUTO), width=400, expand=True)

    def account_request_page():
        return ft.Container(content=ft.Column([ft.Text("فرم درخواست همکاری", size=20, weight="bold"), ft.TextField(label="نام و نام خانوادگی"), ft.TextField(label="شماره ملی"), ft.ElevatedButton("ثبت", on_click=lambda e: show_message("ثبت شد")), ft.OutlinedButton("بازگشت", on_click=lambda e: render(4))], scroll=ft.ScrollMode.AUTO), padding=20)

    def pre_invoice_page():
        products = ["گرمایش از کف", "زیرفرشی", "رادیاتور", "حوله خشک کن", "یخ زدایی رمپ", "یخ زدایی پله", "گرمکن مخزن", "گرمکن صندلی", "رستورانی", "عایق بازتابشی"]
        grid = ft.GridView(runs_count=2, max_extent=120, spacing=10, run_spacing=12, padding=10, expand=True)
        for name in products:
            grid.controls.append(ft.Container(content=ft.Text(name, size=15, weight="bold", text_align=ft.TextAlign.CENTER, color="#1565C0"), width=170, height=70, bgcolor="#ffffff", border_radius=12, alignment=ft.Alignment(0, 0), on_click=lambda e, n=name: show_message(f"پیش‌فاکتور {n}"), ink=True))
        return ft.Container(content=ft.Column([ft.Text("نوع محصول", size=18, weight="bold"), ft.Divider(), grid], scroll=ft.ScrollMode.AUTO), width=400, expand=True)

    def home_page():
        return ft.Container(content=ft.Column([ft.ListTile(leading=ft.Icon(ft.Icons.SHIELD), title=ft.Text("ثبت گارانتی")), ft.ListTile(leading=ft.Icon(ft.Icons.INSTALL_DESKTOP), title=ft.Text("نصب اولیه"))], scroll=ft.ScrollMode.AUTO), width=400, expand=True)

    def technical_page():
        return ft.Container(content=ft.Column([ft.Text("اطلاعات فنی"), ft.ListTile(leading=ft.Icon(ft.Icons.BOOK), title=ft.Text("کاتالوگ"))], scroll=ft.ScrollMode.AUTO), width=400, expand=True)

    def settings_page():
        return ft.Container(content=ft.Column([ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("تنظیمات")]), ft.ElevatedButton("خروج", on_click=lambda e: (setattr(page.session, 'logged_in', False), render()))]))

    def profile_page():
        return ft.Container(content=ft.Column([
            ft.Text("پروفایل کاربری"),
            ft.ListTile(leading=ft.Icon(ft.Icons.PERSON_ADD), title=ft.Text("درخواست ایجاد حساب"), on_click=lambda e: render(6)), 
            ft.ListTile(leading=ft.Icon(ft.Icons.STAR), title=ft.Text("مشتریان منتخب"), on_click=lambda e: render(7)), 
            ft.ListTile(leading=ft.Icon(ft.Icons.WAREHOUSE), title=ft.Text("اعلام موجودی انبار"), on_click=lambda e: render(8)),
            ft.ListTile(leading=ft.Icon(ft.Icons.SETTINGS), title=ft.Text("تنظیمات"), on_click=lambda e: render(5)),
            ft.ListTile(leading=ft.Icon(ft.Icons.LOGOUT), title=ft.Text("خروج"), on_click=lambda e: (setattr(page.session, 'logged_in', False), render()))
        ]), width=400, expand=True)

    def dashboard_page():
        return ft.Container(content=ft.Text("داشبورد مدیریتی"), padding=20)

    def render(tab_index=0):
        page.controls.clear()
        if not page.session.logged_in:
            page.add(ft.Column([ft.Text("ورود به سیستم"), ft.ElevatedButton("ورود", on_click=lambda e: (setattr(page.session, 'logged_in', True), render()))], horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        else:
            contents = [dashboard_page(), pre_invoice_page(), home_page(), technical_page(), profile_page(), settings_page(), account_request_page(), selected_customers_page(), inventory_page()]
            page.add(ft.Column([ft.Container(content=contents[tab_index], expand=True), ft.Row([ft.IconButton(ft.Icons.HOME, on_click=lambda _: render(0)), ft.IconButton(ft.Icons.PERSON, on_click=lambda _: render(4))])]))
        page.update()

    render()

if __name__ == "__main__":
    ft.app(target=main, port=int(os.environ.get("PORT", 8080)), host="0.0.0.0")
