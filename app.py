import flet as ft
import requests
import os

GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbygH2yHhw44Lk5Hv8okJDnRBgGw2UzoF1wsZvMGGGr7ZzhSS0Ro6WhSeVFTPM2TpsMv/exec"

def main(page: ft.Page):
    page.padding = 0
    page.rtl = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.session.logged_in = False

    username = ft.TextField(label="نام کاربری", width=300)
    password = ft.TextField(label="رمز عبور", password=True, width=250)

    def save_to_sheets(name, phone, password):
        try:
            response = requests.post(GOOGLE_SHEET_URL, data={"name": name, "phone": phone, "password": password})
            return response.status_code == 200
        except:
            return False

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
                        ft.Container(content=ft.Image(src="biometric.png", width=30, height=30), on_click=lambda _: None, padding=5)
                    ], alignment="center"),
                    ft.ElevatedButton("ورود به TopSUNify", on_click=lambda e: (setattr(page.session, 'logged_in', True), render()), width=300),
                    
                    # لوگوی سمت راست بدون استفاده از ماژول‌هایِ حساسِ تراز
                    ft.Row([ft.Container(expand=True), ft.Image(src="TopSUN-Powered.png", width=120)], alignment="end"),
                    
                    ft.Container(expand=True),
                    
                    # عکس با گرادیانتِ ایمن (استفاده از رشته برای رنگ‌ها)
                    ft.Container(
                        content=ft.Image(src="landscape.jpg", width=400, height=200, fit=ft.ImageFit.COVER),
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.Alignment(0, -1),
                            end=ft.alignment.Alignment(0, 1),
                            colors=["transparent", "white"] # استفاده از رشته به جای ft.colors
                        )
                    )
                ], horizontal_alignment="center", expand=True)
            )
        else:
            page.add(ft.Column([ft.Text("پنل کاربری", size=30)], horizontal_alignment="center", expand=True))
        page.update()

    render()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
