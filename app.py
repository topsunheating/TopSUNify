import flet as ft
import os
import time
import requests

GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbygH2yHhw44Lk5Hv8okJDnRBgGw2UzoF1wsZvMGGGr7ZzhSS0Ro6WhSeVFTPM2TpsMv/exec"

def main(page: ft.Page):
    page.fonts = {"iranyekan": "fonts/iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    page.padding = 0
    page.rtl = True
    page.theme_mode = "light"
    
    if not hasattr(page.session, "logged_in"):
        page.session.logged_in = False

    def send_to_google_sheet(data: dict):
        try:
            response = requests.post(GOOGLE_SHEET_URL, json=data, timeout=10)
            return response.status_code == 200
        except:
            return False

    # ==================== دیالوگ بیومتریک ====================
    def show_biometric_dialog(e):
        dlg = ft.AlertDialog(
            title=ft.Text("احراز هویت بیومتریک", size=18, weight="bold"),
            content=ft.Column([
                ft.Text("از اثر انگشت یا تشخیص چهره دستگاه استفاده کنید", text_align="center"),
                ft.ProgressRing(width=70, height=70, stroke_width=8),
                ft.Text("در حال اتصال به حسگر...", size=14, color="grey", text_align="center")
            ], horizontal_alignment="center", spacing=25, height=220),
            actions=[ft.TextButton("انصراف", on_click=lambda _: (setattr(dlg, 'open', False), page.update()))]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

        time.sleep(2)
        dlg.open = False
        page.session.logged_in = True
        page.update()
        render()

    # ==================== دیالوگ ثبت‌نام ====================
    def show_register_dialog(e):
        dlg = ft.AlertDialog(title=ft.Text("ثبت‌نام / بازیابی حساب"))
        page.dialog = dlg
        dlg.open = True
        page.update()

    # ==================== صفحه پروفایل (مطابق عکس‌های شما) ====================
    def profile_page():
        return ft.Column([
            # هدر پروفایل
            ft.Container(
                content=ft.Column([
                    ft.CircleAvatar(
                        foreground_image_src="https://i.pravatar.cc/150?u=reza",  # ← اصلاح شده
                        radius=48
                    ),
                    ft.Text("رضا تلجی", size=20, weight="bold", text_align="center"),
                    ft.Text("۰۹۱۲۶۹۸۲۷۹", size=16, color="grey", text_align="center"),
                    ft.Container(
                        content=ft.Text("سامانی ۱۸۹۷", size=15, color="blue", text_align="center"),
                        bgcolor="#f0f0f0",
                        padding=12,
                        border_radius=12,
                        margin=ft.margin.only(top=12, bottom=8)
                    )
                ], horizontal_alignment="center"),
                padding=20,
                bgcolor="#f8f9fa",
                border_radius=20,
                margin=ft.margin.only(bottom=20)
            ),

            # لیست گزینه‌ها
            ft.ListTile(
                leading=ft.Icon(ft.Icons.ACCOUNT_BALANCE, color="blue"),
                title=ft.Text("افتتاح سپرده"),
                trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20),
                on_click=lambda e: page.show_snack_bar(ft.SnackBar(ft.Text("در حال توسعه"), open=True))
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.STAR, color="orange"),
                title=ft.Text("سپرده‌های منتخب"),
                trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.MONEY, color="green"),
                title=ft.Text("تسهیلات بانکی"),
                trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.SIGNATURE),
                title=ft.Text("امضای دیجیتال"),
                trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.SHOP),
                title=ft.Text("پایانه‌های فروشگاهی"),
                trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.CALCULATE),
                title=ft.Text("محاسبه شبا"),
                trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.SAVINGS),
                title=ft.Text("سپرده بلو"),
                trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)
            ),

            ft.Divider(height=20),

            ft.ListTile(
                leading=ft.Icon(ft.Icons.SETTINGS),
                title=ft.Text("تنظیمات"),
                trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20),
                on_click=lambda e: page.show_snack_bar(ft.SnackBar(ft.Text("بخش تنظیمات"), open=True))
            ),

            ft.ListTile(
                leading=ft.Icon(ft.Icons.LOGOUT, color="red"),
                title=ft.Text("خروج", color="red"),
                on_click=lambda e: (setattr(page.session, 'logged_in', False), render(0))
            )
        ], scroll=ft.ScrollMode.AUTO, spacing=4)

    # ==================== رندر اصلی ====================
    def render(tab_index=0):
        page.controls.clear()

        if not page.session.logged_in:
            # صفحه لاگین
            page.add(
                ft.Column([
                    ft.Container(content=ft.Image(src="TopSUNify.png", width=190), margin=ft.margin.Margin(top=40, bottom=40)),

                    ft.Container(
                        content=ft.TextField(label="نام کاربری", width=340, border_radius=12, prefix_icon=ft.Icons.PERSON, text_align=ft.TextAlign.RIGHT),
                        margin=ft.margin.Margin(bottom=20)
                    ),

                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                content=ft.Icon(ft.Icons.FINGERPRINT, size=42, color="#FFCC00"),
                                on_click=show_biometric_dialog,
                                padding=10,
                                border_radius=12,
                                ink=True,
                                ink_color="#FFCC00"
                            ),
                            ft.TextField(
                                label="رمز عبور",
                                password=True,
                                width=270,
                                border_radius=12,
                                prefix_icon=ft.Icons.LOCK,
                                text_align=ft.TextAlign.RIGHT
                            )
                        ], alignment="center", spacing=12),
                        margin=ft.margin.Margin(bottom=30)
                    ),

                    ft.ElevatedButton(
                        "ورود به TopSUNify",
                        width=340,
                        bgcolor="#FFCC00",
                        color="black",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)),
                        on_click=lambda e: (setattr(page.session, 'logged_in', True), render())
                    ),

                    ft.TextButton(
                        "فعال‌سازی / فراموشی رمز",
                        style=ft.ButtonStyle(color={"": "blue"}),
                        on_click=show_register_dialog
                    ),

                    ft.Container(content=ft.Image(src="TopSUN-Powered.png", width=160), margin=ft.margin.Margin(top=50, bottom=30)),

                    ft.Container(expand=True, content=ft.Image(src="landscape.jpg", width=400, height=220, fit="cover"))
                ], horizontal_alignment="center", expand=True, scroll=ft.ScrollMode.AUTO)
            )
        else:
            # صفحات داخلی
            contents = [
                ft.Text("داشبورد مدیریتی", size=25),
                ft.Text("بخش پیش‌فاکتورها", size=25),
                ft.Column([ft.Image(src="TopSUNify-1.png", width=200), ft.Text("خانه اصلی", size=25)], horizontal_alignment="center"),
                ft.Text("اطلاعات فنی سیستم", size=25),
                profile_page()   # پروفایل
            ]

            nav_buttons = ft.Row([
                ft.Container(content=ft.Image(src="dashboard.png", width=32, height=32), on_click=lambda _: render(0), padding=8),
                ft.Container(content=ft.Image(src="invoice.png", width=32, height=32), on_click=lambda _: render(1), padding=8),
                ft.Container(content=ft.Image(src="TopSUNify-1.png", width=32, height=32), on_click=lambda _: render(2), padding=8),
                ft.Container(content=ft.Image(src="technical.png", width=32, height=32), on_click=lambda _: render(3), padding=8),
                ft.Container(content=ft.Image(src="profile.png", width=32, height=32), on_click=lambda _: render(4), padding=8),
            ], alignment="center", spacing=15)

            page.add(
                ft.Column([
                    ft.Text("پنل TopSUNify", size=30, weight="bold"),
                    ft.Divider(),
                    ft.Container(
                        content=contents[tab_index], 
                        expand=True, 
                        alignment=ft.Alignment(0, 0)
                    ),
                    nav_buttons
                ], horizontal_alignment="center", expand=True)
            )

        page.update()

    render()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
