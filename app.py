import flet as ft
import requests
import os

GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbygH2yHhw44Lk5Hv8okJDnRBgGw2UzoF1wsZvMGGGr7ZzhSS0Ro6WhSeVFTPM2TpsMv/exec"

def main(page: ft.Page):
    # تنظیمات کلی و فونت
    page.fonts = {"iranyekan": "/fonts/iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    page.padding = 0
    page.rtl = True
    page.theme_mode = "light"
    page.session.logged_in = False

    username = ft.TextField(label="نام کاربری", width=300)
    password = ft.TextField(label="رمز عبور", password=True, width=250)

    # دیالوگ بیومتریک
    def show_biometric_dialog(e):
        def on_select(method_name):
            dlg.open = False
            page.update()
        dlg = ft.AlertDialog(
            title=ft.Text("روش احراز هویت"),
            content=ft.Column([
                ft.ElevatedButton(content=ft.Row([ft.Icon("fingerprint"), ft.Text("اثر انگشت")]), on_click=lambda _: on_select("Fingerprint")),
                ft.ElevatedButton(content=ft.Row([ft.Icon("face"), ft.Text("تشخیص چهره")]), on_click=lambda _: on_select("FaceID")),
            ], tight=True, height=120),
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # دیالوگ ثبت نام
    def show_registration_dialog(e):
        reg_name = ft.TextField(label="نام و نام خانوادگی")
        reg_phone = ft.TextField(label="شماره موبایل")
        reg_pass = ft.TextField(label="رمز عبور جدید", password=True)
        def submit(e):
            dlg.open = False
            page.update()
        dlg = ft.AlertDialog(title=ft.Text("ثبت نام"), content=ft.Column([reg_name, reg_phone, reg_pass], height=200),
                             actions=[ft.ElevatedButton("ارسال", on_click=submit)])
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
                        ft.GestureDetector(content=ft.Image(src="biometric.png", width=40, height=40), on_tap=show_biometric_dialog)
                    ], alignment="center"),
                    ft.ElevatedButton("ورود به TopSUNify", on_click=lambda e: (setattr(page.session, 'logged_in', True), render()), width=300),
                    ft.TextButton("فعال سازی / فراموشی رمز عبور", on_click=show_registration_dialog),
                    # افزودن TopSUN-Powered
                    ft.Container(content=ft.Image(src="TopSUN-Powered.png", width=120), margin=20),
                    ft.Container(expand=True),
                    # افزودن عکس landscape
                    ft.Stack([
                        ft.Image(src="landscape.jpg", width=400, height=200, fit="cover"),
                        ft.Container(width=400, height=200, gradient=ft.LinearGradient(begin=ft.alignment.Alignment(0, 1), end=ft.alignment.Alignment(0, -1), colors=["transparent", "white"]))
                    ], width=400, height=200)
                ], horizontal_alignment="center", expand=True)
            )
        else:
            # صفحات داخلی حفظ شده
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
    ft.app(target=main, port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", assets_dir="assets")
