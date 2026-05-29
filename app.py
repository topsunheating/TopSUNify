import flet as ft
import requests
import os

GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbygH2yHhw44Lk5Hv8okJDnRBgGw2UzoF1wsZvMGGGr7ZzhSS0Ro6WhSeVFTPM2TpsMv/exec"

def main(page: ft.Page):
    # تنظیمات پایه
    page.padding = 0
    page.rtl = True
    page.theme_mode = "light"  # استفاده از رشته برای پایداری
    page.session.logged_in = False

    username = ft.TextField(label="نام کاربری", width=300)
    password = ft.TextField(label="رمز عبور", password=True, width=250)

    def save_to_sheets(name, phone, password):
        try:
            response = requests.post(GOOGLE_SHEET_URL, data={"name": name, "phone": phone, "password": password})
            return response.status_code == 200
        except: return False

    def show_registration_dialog(e):
        reg_name = ft.TextField(label="نام و نام خانوادگی")
        reg_phone = ft.TextField(label="شماره موبایل")
        reg_pass = ft.TextField(label="رمز عبور جدید", password=True)
        def submit(e):
            if save_to_sheets(reg_name.value, reg_phone.value, reg_pass.value):
                dlg.open = False
                page.update()
        dlg = ft.AlertDialog(title=ft.Text("ثبت نام / فراموشی رمز"), content=ft.Column([reg_name, reg_phone, reg_pass], height=200),
                             actions=[ft.ElevatedButton("ارسال به دیتابیس", on_click=submit)])
        page.dialog = dlg
        dlg.open = True
        page.update()

    def create_nav_icon(icon_name, index, tooltip):
        return ft.Container(
            content=ft.Image(src=icon_name, width=30, height=30),
            padding=10,
            on_click=lambda _: render(index),
            tooltip=tooltip
        )

    def render(tab_index=0):
        page.controls.clear()
        
        if not page.session.logged_in:
            page.add(
                ft.Column([
                    ft.Container(height=40),
                    ft.Image(src="TopSUNify.png", width=150),
                    username,
                    ft.Row([
                        password, 
                        ft.Container(content=ft.Image(src="biometric.png", width=30, height=30), on_click=lambda e: None, padding=5)
                    ], alignment="center"),
                    ft.ElevatedButton("ورود به TopSUNify", on_click=lambda e: (setattr(page.session, 'logged_in', True), render()), width=300),
                    
                    # لوگوی سمت راست (با Row برای پایداری کامل)
                    ft.Row([ft.Container(expand=True), ft.Image(src="TopSUN-Powered.png", width=120)], alignment="end"),
                    
                    ft.Container(expand=True),
                    
                    # عکس با افکت گرادیانت ایمن
                    ft.Container(
                        content=ft.Image(src="landscape.jpg", width=400, height=200, fit="cover"),
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.Alignment(0, -1),
                            end=ft.alignment.Alignment(0, 1),
                            colors=["transparent", "white"]
                        )
                    )
                ], horizontal_alignment="center", expand=True)
            )
        else:
            # صفحات داخلی
            contents = [
                ft.Text("داشبورد مدیریتی", size=25),
                ft.Text("بخش پیش‌فاکتورها", size=25),
                ft.Column([ft.Image(src="TopSUNify-1.png", width=200), ft.Text("خانه اصلی", size=25)], horizontal_alignment="center"),
                ft.Text("اطلاعات فنی سیستم", size=25),
                ft.Text("پروفایل کاربری", size=25)
            ]
            
            nav_buttons = ft.Row([
                create_nav_icon("dashboard.png", 0, "داشبورد"),
                create_nav_icon("invoice.png", 1, "پیش فاکتور"),
                create_nav_icon("TopSUNify-1.png", 2, "خانه"),
                create_nav_icon("technical.png", 3, "اطلاعات فنی"),
                create_nav_icon("profile.png", 4, "پروفایل"),
            ], alignment="center")

            page.add(
                ft.Column([
                    ft.Text("پنل TopSUNify", size=30, weight="bold"),
                    ft.Divider(),
                    ft.Container(content=contents[tab_index], expand=True, alignment=ft.alignment.center),
                    nav_buttons
                ], horizontal_alignment="center", expand=True)
            )
        page.update()

    render()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
