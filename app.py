import flet as ft
import os

def main(page: ft.Page):
    page.fonts = {"iranyekan": "iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    page.title = "TopSUNify"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    page.session.logged_in = False
    
    username = ft.TextField(label="نام کاربری", width=300)
    password = ft.TextField(label="رمز عبور", password=True, width=250)

    def show_biometric_dialog(e):
        dlg = ft.AlertDialog(
            title=ft.Text("احراز هویت"),
            content=ft.Text("در حال اسکن اثر انگشت..."),
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

    def create_nav_icon(icon_path, index, tooltip):
        return ft.Container(
            content=ft.Image(src=icon_path, width=30, height=30),
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
                    ft.Image(src="TopSUNify.png", width=150, height=150),
                    username,
                    ft.Row([
                        password,
                        ft.Container(ft.Image(src="biometric.png", width=30, height=30), on_click=show_biometric_dialog, padding=5)
                    ], alignment="center"),
                    ft.ElevatedButton("ورود به TopSUNify", on_click=login, width=300),
                    ft.Text("فعال سازی / فراموشی رمز عبور", size=12, color="blue"),
                    
                    ft.Container(height=30),
                    # لوگوی جدید با تراز راست
                    ft.Container(content=ft.Image(src="TopSUN-Powered.png", width=120), alignment=ft.alignment.center_right, padding=10),
                    
                    ft.Container(expand=True),
                    ft.Image(src="landscape.jpg", width=400, height=200)
                ], horizontal_alignment="center", expand=True)
            )
        else:
            # صفحات داخلی کامل
            contents = [
                ft.Column([ft.Text("داشبورد مدیریتی", size=25), ft.Text("خوش آمدید!")], horizontal_alignment="center"),
                ft.Column([ft.Text("بخش پیش‌فاکتورها", size=25), ft.Text("لیست فاکتورهای شما")], horizontal_alignment="center"),
                ft.Column([ft.Image(src="TopSUNify-1.png", width=200), ft.Text("خانه اصلی")], horizontal_alignment="center"),
                ft.Column([ft.Text("اطلاعات فنی سیستم", size=25), ft.Text("پارامترهای فنی...")], horizontal_alignment="center"),
                ft.Column([ft.Text("پروفایل کاربری", size=25), ft.Text("تنظیمات حساب")], horizontal_alignment="center")
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
