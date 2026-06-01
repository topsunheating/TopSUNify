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
        snack = ft.SnackBar(content=ft.Text(text), bgcolor=color, action="بستن")
        page.snack_bar = snack
        snack.open = True
        page.update()

    def toggle_theme(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()

    # تعریف دیالوگ در داخل main تا در دسترس همه توابع باشد
    account_dlg = ft.AlertDialog(
        title=ft.Text("درخواست ایجاد حساب همکاری", text_align=ft.TextAlign.CENTER),
        content=ft.Container(
            content=ft.Column([
                ft.TextField(label="نام و نام خانوادگی", text_align=ft.TextAlign.RIGHT),
                ft.TextField(label="شماره ملی", text_align=ft.TextAlign.RIGHT),
                ft.ElevatedButton("تایید درخواست", bgcolor="#1565C0", color="white", on_click=lambda e: show_message("درخواست با موفقیت ثبت شد")),
                ft.OutlinedButton("بستن", on_click=lambda e: (setattr(account_dlg, 'open', False), page.update())),
            ], scroll=ft.ScrollMode.AUTO, tight=True),
            width=350, height=300
        )
    )

    def dashboard_page():
        return ft.Container(content=ft.Text("صفحه داشبورد"), alignment=ft.alignment.center, expand=True)

    def pre_invoice_page():
        return ft.Container(content=ft.Text("صفحه پیش‌فاکتور"), alignment=ft.alignment.center, expand=True)

    def home_page():
        return ft.Container(content=ft.Text("صفحه اصلی"), alignment=ft.alignment.center, expand=True)

    def technical_page():
        return ft.Container(content=ft.Text("اطلاعات فنی"), alignment=ft.alignment.center, expand=True)

    def settings_page():
        return ft.Container(content=ft.Text("تنظیمات"), alignment=ft.alignment.center, expand=True)

    def profile_page():
        return ft.Container(content=ft.Column([
            ft.Text("پروفایل کاربری", size=20, weight="bold"),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.PERSON_ADD, color="blue"), 
                title=ft.Text("درخواست ایجاد حساب"), 
                on_click=lambda e: (setattr(page, 'dialog', account_dlg), setattr(account_dlg, 'open', True), page.update())
            ),
            ft.ListTile(leading=ft.Icon(ft.Icons.PALETTE), title=ft.Text("تغییر تم"), on_click=toggle_theme),
            ft.ListTile(leading=ft.Icon(ft.Icons.LOGOUT, color="red"), title=ft.Text("خروج"), on_click=lambda e: (setattr(page.session, 'logged_in', False), render()))
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=400, padding=20)

    def render(tab_index=0):
        page.controls.clear()
        if not page.session.logged_in:
            page.add(ft.Column([
                ft.Text("ورود به سیستم", size=24),
                ft.ElevatedButton("ورود", on_click=lambda e: (setattr(page.session, 'logged_in', True), render()))
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        else:
            contents = [dashboard_page(), pre_invoice_page(), home_page(), technical_page(), profile_page(), settings_page()]
            page.add(ft.Column([
                ft.Container(content=contents[tab_index], expand=True),
                ft.Row([
                    ft.IconButton(ft.Icons.HOME, on_click=lambda _: render(0)),
                    ft.IconButton(ft.Icons.PERSON, on_click=lambda _: render(4)),
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], expand=True))
        page.update()

    render()

if __name__ == "__main__":
    ft.app(target=main, port=8080, host="0.0.0.0", assets_dir="assets")
