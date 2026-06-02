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

    def render(tab_index=0):
        # تعریف توابع داخل رندر برای دسترسی کامل به متغیرهای محلی و جلوگیری از خطای Scope
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
                    product_size.options = [ft.dropdown.Option(item) for item in product_data.get(product_name.value, [])]
                    page.update()

            def add_to_table(e):
                new_row = ft.DataRow(cells=[ft.DataCell(ft.Text(product_name.value)), ft.DataCell(ft.Text(product_size.value)), ft.DataCell(ft.Text(product_qty.value)), ft.DataCell(ft.IconButton(ft.Icons.DELETE, icon_color="red", on_click=lambda _: (table.rows.remove(new_row), page.update())))])
                table.rows.append(new_row)
                page.update()

            return ft.Container(content=ft.Column([ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("انبار")]), product_name, ft.ElevatedButton("بارگذاری ابعاد", on_click=load_sizes), product_size, product_qty, ft.ElevatedButton("افزودن", on_click=add_to_table), table]), width=400, expand=True, padding=15)

        # سایر صفحات به همین صورت تعریف می‌شوند تا در لیست contents شناسایی شوند
        def placeholder_page(name): return ft.Container(content=ft.Column([ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text(name)]), ft.Text("در حال توسعه...")]))
        
        # تعریف تمامی صفحات در محدوده رندر
        contents = [
            placeholder_page("داشبورد"), placeholder_page("پیش فاکتور"), placeholder_page("خانه"), placeholder_page("فنی"),
            placeholder_page("پروفایل"), placeholder_page("تنظیمات"), placeholder_page("درخواست همکاری"),
            placeholder_page("مشتریان"), inventory_page(), placeholder_page("همکاران"),
            placeholder_page("درخواست خرید"), placeholder_page("درصد همکاری"), placeholder_page("اعتبار"),
            placeholder_page("تم"), placeholder_page("بروزرسانی"), placeholder_page("شبکه"), placeholder_page("قوانین"), placeholder_page("درباره ما")
        ]

        page.controls.clear()
        if not page.session.logged_in:
            page.add(ft.Container(content=ft.Column([ft.Image(src="TopSUNify.png", width=190), ft.ElevatedButton("ورود به TopSUNify", on_click=lambda e: (setattr(page.session, 'logged_in', True), render()))]), width=400, alignment=ft.Alignment(0, 0)))
        else:
            page.add(ft.Column([ft.Container(content=contents[tab_index], expand=True), ft.Row([ft.IconButton(ft.Icons.HOME, on_click=lambda _: render(2)), ft.IconButton(ft.Icons.PERSON, on_click=lambda _: render(4))], alignment=ft.MainAxisAlignment.CENTER)]))
        page.update()

    render()

if __name__ == "__main__":
    ft.app(target=main, port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", assets_dir="assets")
