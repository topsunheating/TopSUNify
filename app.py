import flet as ft
import os

def main(page: ft.Page):
    # تنظیمات عمومی - این‌ها در تمام نسخه‌ها کار می‌کنند
    page.fonts = {"iranyekan": "fonts/iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    page.padding = 0
    page.rtl = True
    page.theme_mode = "light"
    page.session.logged_in = False

    # دیالوگ بیومتریک با استفاده از کانتینر (بسیار ایمن‌تر از AlertDialog)
    biometric_overlay = ft.Container(
        content=ft.Column([
            ft.Text("احراز هویت بیومتریک", size=20, weight="bold"),
            ft.ElevatedButton("اثر انگشت", on_click=lambda e: (setattr(biometric_overlay, 'visible', False), page.update())),
            ft.ElevatedButton("تشخیص چهره", on_click=lambda e: (setattr(biometric_overlay, 'visible', False), page.update())),
        ], alignment="center", horizontal_alignment="center"),
        width=300, height=200, bgcolor="white", border_radius=20,
        padding=20, visible=False, shadow=ft.BoxShadow(blur_radius=10)
    )

    def show_biometric(e):
        biometric_overlay.visible = True
        page.update()

    def render(tab_index=0):
        page.controls.clear()
        
        if not page.session.logged_in:
            # صفحه لاگین
            page.add(
                ft.Stack([
                    ft.Column([
                        ft.Container(height=40),
                        ft.Image(src="TopSUNify.png", width=150),
                        ft.TextField(label="نام کاربری", width=300),
                        ft.Row([
                            ft.TextField(label="رمز عبور", password=True, width=250),
                            # IconButton همیشه در هر نسخه کار می‌کند
                            ft.IconButton(icon="fingerprint", on_click=show_biometric)
                        ], alignment="center"),
                        ft.ElevatedButton("ورود به TopSUNify", on_click=lambda e: (setattr(page.session, 'logged_in', True), render()), width=300),
                        ft.Container(content=ft.Image(src="TopSUN-Powered.png", width=120), margin=20),
                        ft.Container(expand=True),
                        ft.Image(src="landscape.jpg", width=400, height=200, fit="cover")
                    ], horizontal_alignment="center", expand=True),
                    ft.Container(content=biometric_overlay, alignment=ft.alignment.center)
                ], expand=True)
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
                    ft.Container(content=contents[tab_index], expand=True, alignment="center"),
                    nav_buttons
                ], horizontal_alignment="center", expand=True)
            )
        page.update()

    render()

if __name__ == "__main__":
    # اگر روی سرور هستید از پورت متغیر، اگر لوکال هستید از 8080 استفاده کنید
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
