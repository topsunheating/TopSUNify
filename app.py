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

    # --- صفحه انبار اصلاح شده ---
    def inventory_page():
        product_name = ft.TextField(label="نام محصول", width=350)
        product_size = ft.TextField(label="ابعاد محصول", width=350)
        product_qty = ft.TextField(label="تعداد موجودی", width=350, keyboard_type=ft.KeyboardType.NUMBER)
        
        table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("نام")), ft.DataColumn(ft.Text("ابعاد")), ft.DataColumn(ft.Text("تعداد"))],
            rows=[]
        )

        def add_to_table(e):
            if product_name.value and product_qty.value:
                table.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(product_name.value)),
                    ft.DataCell(ft.Text(product_size.value)),
                    ft.DataCell(ft.Text(product_qty.value))
                ]))
                product_name.value = ""
                product_size.value = ""
                product_qty.value = ""
                page.update()
            else:
                show_message("لطفاً نام و تعداد را وارد کنید", "red")

        # استفاده از ListView به جای SingleChildScrollView برای جلوگیری از خطا
        return ft.Container(content=ft.ListView([
            ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("اعلام موجودی انبار", size=20, weight="bold")]), padding=10),
            product_name, product_size, product_qty,
            ft.ElevatedButton("تایید موجودی", on_click=add_to_table, bgcolor="green", color="white"),
            ft.Divider(),
            table,
            ft.ElevatedButton("اعلام کل موجودی", on_click=lambda e: show_message("ثبت شد"), bgcolor="blue", color="white", width=350)
        ], expand=1, spacing=10, padding=20), width=400, expand=True)

    # --- سایر صفحات (طبق کد دوم شما) ---
    def selected_customers_page():
        return ft.Container(content=ft.Column([
            ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("مشتریان منتخب", size=20, weight="bold")]), padding=10),
            ft.DataTable(columns=[ft.DataColumn(ft.Text("کد")), ft.DataColumn(ft.Text("نام")), ft.DataColumn(ft.Text("تماس")), ft.DataColumn(ft.Text("شهر"))],
                rows=[ft.DataRow(cells=[ft.DataCell(ft.Text("101")), ft.DataCell(ft.Text("رضا احمدی")), ft.DataCell(ft.Text("09121234567")), ft.DataCell(ft.Text("تهران"))])]),
        ], scroll=ft.ScrollMode.AUTO), width=400, expand=True)

    def account_request_page():
        return ft.Container(content=ft.Column([
            ft.Text("فرم درخواست همکاری", size=20, weight="bold"),
            ft.TextField(label="نام و نام خانوادگی", text_align=ft.TextAlign.RIGHT),
            ft.Dropdown(label="نوع درخواست", options=[ft.dropdown.Option("نماینده فروش"), ft.dropdown.Option("نصاب فنی")]),
            ft.ElevatedButton("ثبت نهایی", on_click=lambda e: show_message("ثبت شد")),
            ft.OutlinedButton("بازگشت", on_click=lambda e: render(4))
        ], scroll=ft.ScrollMode.AUTO), padding=20)

    def pre_invoice_page():
        products = ["گرمایش از کف", "زیرفرشی", "رادیاتور"]
        grid = ft.GridView(runs_count=2, max_extent=120, spacing=10, padding=10, expand=True)
        for name in products:
            grid.controls.append(ft.Container(content=ft.Text(name), width=170, height=70, bgcolor="#ffffff", on_click=lambda e, n=name: show_message(f"پیش‌فاکتور {n}"), ink=True))
        return ft.Container(content=ft.Column([ft.Text("نوع محصول", size=18, weight="bold"), grid], scroll=ft.ScrollMode.AUTO), width=400, expand=True)

    def home_page():
        return ft.Container(content=ft.Column([ft.Text("خوش آمدید")], scroll=ft.ScrollMode.AUTO), width=400, expand=True)

    def technical_page():
        return ft.Container(content=ft.Column([ft.Text("اطلاعات فنی")], scroll=ft.ScrollMode.AUTO), width=400, expand=True)

    def settings_page():
        return ft.Container(content=ft.Column([ft.Text("تنظیمات")], scroll=ft.ScrollMode.AUTO))

    def profile_page():
        return ft.Container(content=ft.Column([
            ft.Text("پروفایل کاربری"),
            ft.ListTile(leading=ft.Icon(ft.Icons.WAREHOUSE), title=ft.Text("اعلام موجودی انبار"), on_click=lambda e: render(8)),
            ft.ListTile(leading=ft.Icon(ft.Icons.LOGOUT), title=ft.Text("خروج"), on_click=lambda e: (setattr(page.session, 'logged_in', False), render()))
        ], scroll=ft.ScrollMode.AUTO), width=400, expand=True)

    def dashboard_page():
        return ft.Container(content=ft.Text("داشبورد"), padding=20)

    # --- تابع رندر ---
    def render(tab_index=0):
        page.controls.clear()
        if not page.session.logged_in:
            page.add(ft.ElevatedButton("ورود به TopSUNify", on_click=lambda e: (setattr(page.session, 'logged_in', True), render())))
        else:
            # لیست صفحات (ایندکس 8 مربوط به انبار)
            contents = [dashboard_page(), pre_invoice_page(), home_page(), technical_page(), profile_page(), settings_page(), account_request_page(), selected_customers_page(), inventory_page()]
            page.add(ft.Column([
                ft.Container(content=contents[tab_index], expand=True, width=400, margin=ft.margin.Margin(left=15, right=15)),
                ft.Row([ft.IconButton(ft.Icons.HOME, on_click=lambda _: render(0)), ft.IconButton(ft.Icons.PERSON, on_click=lambda _: render(4))], alignment=ft.MainAxisAlignment.CENTER)
            ], expand=True))
        page.update()

    render()

if __name__ == "__main__":
    ft.app(target=main, port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", assets_dir="assets")
