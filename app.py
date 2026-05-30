import flet as ft
import requests
import os

def main(page: ft.Page):
    # تنظیم دقیق فونت (بدون اسلش در ابتدای آدرس)
    page.fonts = {
        "iranyekan": "fonts/iranyekan.ttf"
    }
    page.theme = ft.Theme(font_family="iranyekan")
    
    page.padding = 0
    page.rtl = True
    page.theme_mode = "light"
    page.session.logged_in = False

    # تعریف دیالوگ بیومتریک
    def show_biometric_dialog(e):
        dlg = ft.AlertDialog(title=ft.Text("احراز هویت بیومتریک فعال شد"))
        page.dialog = dlg
        dlg.open = True
        page.update()

    # تعریف صفحات داخلی
    def render(tab_index=0):
        page.controls.clear()
        
        if not page.session.logged_in:
            # صفحه لاگین
            page.add(
                ft.Column([
                    ft.Container(height=40),
                    ft.Image(src="TopSUNify.png", width=150),
                    ft.TextField(label="نام کاربری", width=300),
                    ft.Row([
                        ft.TextField(label="رمز عبور", password=True, width=250),
                        # استفاده از Container برای کلیک‌خور کردن عکس بدون خطا
                        ft.Container(
                            content=ft.Image(src="biometric.png", width=40, height=40),
                            on_click=show_biometric_dialog,
                            padding=5
                        )
                    ], alignment="center"),
                    ft.ElevatedButton("ورود به TopSUNify", on_click=lambda e: (setattr(page.session, 'logged_in', True), render()), width=300),
                    ft.Container(content=ft.Image(src="TopSUN-Powered.png", width=120), margin=20),
                    ft.Container(expand=True),
                    ft.Stack([
                        ft.Image(src="landscape.jpg", width=400, height=200, fit="cover"),
                        ft.Container(width=400, height=200, gradient=ft.LinearGradient(begin=ft.alignment.Alignment(0, 1), end=ft.alignment.Alignment(0, -1), colors=["transparent", "white"]))
                    ], width=400, height=200)
                ], horizontal_alignment="center", expand=True)
            )
        else:
            # صفحات داخلی کامل
            contents = [
                ft.Text("داشبورد مدیریتی", size=25),
                ft.Text("بخش پیش‌فاکتورها", size=25),
                ft.Column([ft.Image(src="TopSUNify-1.png", width=200), ft.Text("خانه اصلی", size=25)], horizontal_alignment="center"),
                ft.Text("اطلاعات فنی سیستم", size=25),
                ft.Text("پروفایل کاربری", size=25)
            ]
            
            nav_buttons = ft.Row([
                ft.IconButton(icon="dashboard", on_click=lambda _: render(0)),
                ft.IconButton(icon="edit_document", on_click=lambda _: render(1)),
                ft.IconButton(icon="home", on_click=lambda _: render(2)),
                ft.IconButton(icon="build", on_click=lambda _: render(3)),
                ft.IconButton(icon="person", on_click=lambda _: render(4)),
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

# اجرای برنامه
if __name__ == "__main__":
    ft.app(target=main, port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", assets_dir="assets")
