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
        page.session.inventory_data = [] # برای ذخیره موجودی ها

    def show_message(text: str, color="green"):
        snack = ft.SnackBar(content=ft.Text(text), bgcolor=color, action="بستن", duration=3000)
        page.snack_bar = snack
        snack.open = True
        page.update()

    def toggle_theme(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()

    # --- صفحات جدید اضافه شده ---

    def inventory_page():
        product_name = ft.TextField(label="نام محصول", text_align=ft.TextAlign.RIGHT)
        product_size = ft.TextField(label="ابعاد محصول", text_align=ft.TextAlign.RIGHT)
        product_qty = ft.TextField(label="تعداد موجودی", text_align=ft.TextAlign.RIGHT, keyboard_type=ft.KeyboardType.NUMBER)
        
        table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("نام")), ft.DataColumn(ft.Text("ابعاد")), ft.DataColumn(ft.Text("تعداد"))],
            rows=[]
        )

        def add_item(e):
            table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(product_name.value)), ft.DataCell(ft.Text(product_size.value)), ft.DataCell(ft.Text(product_qty.value))]))
            product_name.value = ""
            product_size.value = ""
            product_qty.value = ""
            page.update()

        def submit_all(e):
            show_message("فایل موجودی با موفقیت ثبت و ارسال شد")
            render(4) # بازگشت به پروفایل

        return ft.Container(content=ft.Column([
            ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("اعلام موجودی انبار", size=20, weight="bold")]), padding=10),
            product_name, product_size, product_qty,
            ft.ElevatedButton("تایید موجودی", on_click=add_item),
            ft.Divider(),
            table,
            ft.ElevatedButton("اعلام کل موجودی (PDF)", on_click=submit_all, bgcolor="green", color="white")
        ], scroll=ft.ScrollMode.AUTO), width=400, expand=True)

    def selected_customers_page():
        return ft.Container(content=ft.Column([
            ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("مشتریان منتخب", size=20, weight="bold")]), padding=10),
            ft.DataTable(columns=[ft.DataColumn(ft.Text("کد")), ft.DataColumn(ft.Text("نام")), ft.DataColumn(ft.Text("تماس")), ft.DataColumn(ft.Text("شهر"))],
                rows=[ft.DataRow(cells=[ft.DataCell(ft.Text("101")), ft.DataCell(ft.Text("رضا احمدی")), ft.DataCell(ft.Text("09121234567")), ft.DataCell(ft.Text("تهران"))])]),
        ], scroll=ft.ScrollMode.AUTO), width=400, expand=True)

    def account_request_page():
        return ft.Container(content=ft.Column([
            ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("فرم درخواست همکاری", size=20, weight="bold")]), padding=10),
            ft.TextField(label="نام و نام خانوادگی", text_align=ft.TextAlign.RIGHT),
            ft.ElevatedButton("ثبت نهایی درخواست", on_click=lambda e: show_message("ثبت شد"))
        ], scroll=ft.ScrollMode.AUTO), width=400, expand=True)

    # --- توابع اصلی شما (بدون تغییر) ---

    def pre_invoice_page():
        products = ["گرمایش از کف", "زیرفرشی", "رادیاتور", "حوله خشک کن", "یخ زدایی رمپ", "یخ زدایی پله", "گرمکن مخزن", "گرمکن صندلی", "رستورانی", "عایق بازتابشی"]
        grid = ft.GridView(runs_count=2, max_extent=120, spacing=10, run_spacing=12, padding=10, expand=True)
        for name in products:
            grid.controls.append(ft.Container(content=ft.Text(name, size=15, weight="bold", text_align=ft.TextAlign.CENTER, color="#1565C0"), width=170, height=70, bgcolor="#ffffff", border_radius=12, alignment=ft.Alignment(0, 0), shadow=ft.BoxShadow(blur_radius=6, color="#e0e0e0"), on_click=lambda e, n=name: show_message(f"پیش‌فاکتور {n}"), ink=True))
        return ft.Container(content=ft.Column([ft.Text("نوع محصول مورد نظر را انتخاب کنید", size=18, weight="bold", text_align=ft.TextAlign.CENTER), ft.Divider(height=10), grid], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)

    def home_page():
        return ft.Container(content=ft.Column([ft.Container(content=ft.Column([ft.Image(src="TopSUNify-1.png", width=80), ft.Text("خوش آمدید به TopSUNify", size=18, weight="bold", text_align=ft.TextAlign.CENTER)], horizontal_alignment=ft.CrossAxisAlignment.CENTER), margin=ft.margin.Margin(top=20, bottom=30))], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)

    def technical_page():
        return ft.Container(content=ft.Column([ft.Container(content=ft.Text("اطلاعات فنی", size=18, weight="bold", text_align=ft.TextAlign.CENTER), padding=20)], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)

    def settings_page():
        return ft.Container(content=ft.Column([ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("تنظیمات", size=24, weight="bold")]), padding=15)], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER))

    def profile_page():
        return ft.Container(content=ft.Column([
            ft.ListTile(leading=ft.Icon(ft.Icons.PERSON_ADD), title=ft.Text("درخواست ایجاد حساب"), on_click=lambda e: render(6)), 
            ft.ListTile(leading=ft.Icon(ft.Icons.STAR), title=ft.Text("مشتریان منتخب"), on_click=lambda e: render(7)), 
            ft.ListTile(leading=ft.Icon(ft.Icons.WAREHOUSE), title=ft.Text("اعلام موجودی انبار"), on_click=lambda e: render(8)), 
            ft.ListTile(leading=ft.Icon(ft.Icons.LOGOUT), title=ft.Text("خروج"), on_click=lambda e: (setattr(page.session, 'logged_in', False), render()))
        ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)

    def dashboard_page():
        return ft.Container(content=ft.Text("داشبورد مدیریتی"), padding=20)

    def render(tab_index=0):
        page.controls.clear()
        if not page.session.logged_in:
            page.add(ft.ElevatedButton("ورود به برنامه", on_click=lambda e: (setattr(page.session, 'logged_in', True), render())))
        else:
            contents = [dashboard_page(), pre_invoice_page(), home_page(), technical_page(), profile_page(), settings_page(), account_request_page(), selected_customers_page(), inventory_page()]
            page.add(ft.Column([ft.Container(content=contents[tab_index], expand=True, width=400, margin=ft.margin.Margin(left=15, right=15))]))
        page.update()

    render()

if __name__ == "__main__":
    ft.app(target=main, port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", assets_dir="assets")
