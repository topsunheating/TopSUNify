import flet as ft
import os

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

    def show_message(text: str, color="green"):
        snack = ft.SnackBar(content=ft.Text(text), bgcolor=color, action="بستن", duration=3000)
        page.snack_bar = snack
        snack.open = True
        page.update()

    def toggle_theme(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()

    # --- صفحات برنامه ---

    def selected_customers_page():
        return ft.Container(content=ft.Column([
            ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("مشتریان منتخب", size=20, weight="bold")]),
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("کد")),
                    ft.DataColumn(ft.Text("نام / مجموعه")),
                    ft.DataColumn(ft.Text("شماره تماس")),
                    ft.DataColumn(ft.Text("شهر")),
                ],
                rows=[
                    ft.DataRow(cells=[ft.DataCell(ft.Text("101")), ft.DataCell(ft.Text("رضا احمدی")), ft.DataCell(ft.Text("09121234567")), ft.DataCell(ft.Text("تهران"))]),
                ],
            )
        ]), padding=20)

    def account_request_page():
        return ft.Container(content=ft.Column([
            ft.Text("فرم درخواست همکاری", size=20, weight="bold"),
            ft.TextField(label="نام و نام خانوادگی", text_align=ft.TextAlign.RIGHT),
            ft.TextField(label="نام پدر", text_align=ft.TextAlign.RIGHT),
            ft.TextField(label="شماره ملی", text_align=ft.TextAlign.RIGHT),
            ft.Dropdown(label="نوع درخواست", options=[
                ft.dropdown.Option("نماینده فروش"),
                ft.dropdown.Option("نصاب فنی"),
            ]),
            ft.ElevatedButton("ثبت نهایی درخواست", bgcolor="#1565C0", color="white", on_click=lambda e: show_message("درخواست با موفقیت ثبت شد")),
            ft.OutlinedButton("بازگشت به پروفایل", on_click=lambda e: render(4))
        ], scroll=ft.ScrollMode.AUTO), padding=20)

    def pre_invoice_page():
        return ft.Container(content=ft.Text("صفحه پیش‌فاکتورها"), padding=20)

    def home_page():
        return ft.Container(content=ft.Text("صفحه اصلی"), padding=20)

    def technical_page():
        return ft.Container(content=ft.Text("اطلاعات فنی"), padding=20)

    def settings_page():
        return ft.Container(content=ft.Column([ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("تنظیمات")]), ft.ElevatedButton("خروج", on_click=lambda e: (setattr(page.session, 'logged_in', False), render()))]))

    def dashboard_page():
        return ft.Container(content=ft.Text("داشبورد مدیریتی"), padding=20)

    def profile_page():
        return ft.Container(content=ft.Column([
            ft.Text("پروفایل کاربری", size=20),
            ft.ListTile(leading=ft.Icon(ft.Icons.PERSON_ADD), title=ft.Text("درخواست ایجاد حساب"), on_click=lambda e: render(6)),
            ft.ListTile(leading=ft.Icon(ft.Icons.STAR), title=ft.Text("مشتریان منتخب"), on_click=lambda e: render(7)),
        ]))

    def render(tab_index=0):
        page.controls.clear()
        if not page.session.logged_in:
            page.add(ft.Column([ft.Text("ورود به سیستم"), ft.ElevatedButton("ورود", on_click=lambda e: (setattr(page.session, 'logged_in', True), render()))]))
        else:
            contents = [dashboard_page(), pre_invoice_page(), home_page(), technical_page(), profile_page(), settings_page(), account_request_page(), selected_customers_page()]
            page.add(ft.Column([
                ft.Container(content=contents[tab_index], expand=True),
                ft.Row([ft.IconButton(ft.Icons.HOME, on_click=lambda _: render(0)), ft.IconButton(ft.Icons.PERSON, on_click=lambda _: render(4))])
            ]))
        page.update()

    render()

if __name__ == "__main__":
    ft.app(target=main, port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", assets_dir="assets")
