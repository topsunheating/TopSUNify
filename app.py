import flet as ft
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def main(page: ft.Page):
    # تنظیمات پایه
    page.padding = 0
    page.rtl = True
    page.fonts = {"iranyekan": "iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    page.theme_mode = ft.ThemeMode.LIGHT
    page.session.logged_in = False

    username = ft.TextField(label="نام کاربری", width=300)
    password = ft.TextField(label="رمز عبور", password=True, width=250)

    # تابع ثبت در گوگل شیت
    def save_to_sheets(name, phone, password):
        try:
            scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets']
            creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
            client = gspread.authorize(creds)
            sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Vt-vKivm7I2Yi79gJarLVtSR2KowDGCQiW54UIgW6ls/edit").sheet1
            sheet.append_row([name, phone, password])
            return True
        except:
            return False

    def show_registration_dialog(e):
        reg_name = ft.TextField(label="نام و نام خانوادگی")
        reg_phone = ft.TextField(label="شماره موبایل")
        reg_pass = ft.TextField(label="رمز عبور جدید", password=True)
        
        def submit(e):
            if save_to_sheets(reg_name.value, reg_phone.value, reg_pass.value):
                dlg.open = False
                page.show_snack_bar(ft.SnackBar(content=ft.Text("با موفقیت ثبت شد")))
                page.update()
        
        dlg = ft.AlertDialog(
            title=ft.Text("ثبت نام / فراموشی رمز"),
            content=ft.Column([reg_name, reg_phone, reg_pass], height=200),
            actions=[ft.ElevatedButton("ارسال", on_click=submit)]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def show_biometric_dialog(e):
        dlg = ft.AlertDialog(
            title=ft.Text("احراز هویت"),
            content=ft.Text("حسگر را لمس کنید..."),
            actions=[ft.TextButton("انصراف", on_click=lambda e: setattr(dlg, 'open', False) or page.update())],
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def login(e):
        if username.value == "admin" and password.value == "1234":
            page.session.logged_in = True
            render()
        else:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("اطلاعات اشتباه است!")))
            page.update()

    def render(tab_index=0):
        page.controls.clear()
        if not page.session.logged_in:
            page.add(
                ft.Column([
                    ft.Container(height=40),
                    ft.Image(src="TopSUNify.png", width=150),
                    username,
                    ft.Row([password, ft.IconButton(icon=ft.icons.FINGERPRINT, on_click=show_biometric_dialog)], alignment="center"),
                    ft.ElevatedButton("ورود به TopSUNify", on_click=login, width=300),
                    ft.TextButton("فعال سازی / فراموشی رمز عبور", on_click=show_registration_dialog),
                    # لوگو در سمت راست (استفاده از رشته برای تراز کردن)
                    ft.Container(content=ft.Image(src="TopSUN-Powered.png", width=120), alignment="center_right", padding=10),
                    ft.Container(expand=True),
                    ft.Image(src="landscape.jpg", width=400, height=200)
                ], horizontal_alignment="center", expand=True)
            )
        else:
            # صفحات داخلی
            nav_buttons = ft.Row([
                ft.IconButton(ft.icons.HOME, on_click=lambda _: render(0)),
                ft.IconButton(ft.icons.LIST, on_click=lambda _: render(1)),
                ft.IconButton(ft.icons.PERSON, on_click=lambda _: render(2))
            ], alignment="center")
            
            page.add(ft.Column([ft.Text("پنل کاربری"), ft.Divider(), ft.Container(expand=True), nav_buttons], horizontal_alignment="center", expand=True))
        page.update()

    render()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
