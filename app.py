import flet as ft
import os
import time
import requests

def main(page: ft.Page):
    page.fonts = {"iranyekan": "fonts/iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    page.padding = 0
    page.rtl = True
    page.theme_mode = "light"
    
    if not hasattr(page.session, "logged_in"):
        page.session.logged_in = False

    GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbygH2yHhw44Lk5Hv8okJDnRBgGw2UzoF1wsZvMGGGr7ZzhSS0Ro6WhSeVFTPM2TpsMv/exec"

    # ==================== ارسال به گوگل شیت ====================
    def send_to_google_sheet(data: dict):
        try:
            response = requests.post(GOOGLE_SCRIPT_URL, json=data, timeout=10)
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

        time.sleep(2.2)
        dlg.open = False
        page.session.logged_in = True
        page.update()
        render()

    # ==================== دیالوگ ثبت‌نام / فراموشی رمز ====================
    def show_register_dialog(e):
        name = ft.TextField(label="نام و نام خانوادگی", width=340, border_radius=10)
        phone = ft.TextField(label="شماره موبایل", width=340, border_radius=10, prefix_text="+98 ", keyboard_type=ft.KeyboardType.NUMBER)
        username = ft.TextField(label="نام کاربری", width=340, border_radius=10)
        password = ft.TextField(label="رمز عبور", password=True, width=340, border_radius=10)
        confirm_password = ft.TextField(label="تأیید رمز عبور", password=True, width=340, border_radius=10)
        verification_code = ft.TextField(label="کد تأیید", width=340, border_radius=10, visible=False)

        def send_verification(e):
            if not phone.value or len(phone.value) < 10:
                page.show_snack_bar(ft.SnackBar(ft.Text("شماره موبایل معتبر وارد کنید"), open=True))
                return
            page.show_snack_bar(ft.SnackBar(ft.Text("✅ کد تأیید ارسال شد"), open=True, bgcolor="green"))
            verification_code.visible = True
            page.update()

        def register_user(e):
            if password.value != confirm_password.value:
                page.show_snack_bar(ft.SnackBar(ft.Text("رمز عبور مطابقت ندارد"), open=True))
                return
            if not verification_code.value:
                page.show_snack_bar(ft.SnackBar(ft.Text("کد تأیید را وارد کنید"), open=True))
                return

            data = {
                "نام_نام_خانوادگی": name.value,
                "شماره_موبایل": phone.value,
                "نام_کاربری": username.value,
                "رمز_عبور": password.value,
                "تاریخ": time.strftime("%Y-%m-%d %H:%M:%S")
            }

            if send_to_google_sheet(data):
                page.show_snack_bar(ft.SnackBar(ft.Text("✅ ثبت‌نام موفق بود"), open=True, bgcolor="green"))
                dlg.open = False
            else:
                page.show_snack_bar(ft.SnackBar(ft.Text("خطا در ثبت اطلاعات"), open=True))
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("ثبت‌نام / بازیابی حساب", size=18, weight="bold"),
            content=ft.Column([
                name, phone, username, password, confirm_password,
                ft.ElevatedButton("ارسال کد تأیید", bgcolor="blue", color="white", on_click=send_verification),
                verification_code,
            ], spacing=15, scroll=ft.ScrollMode.AUTO, height=450),
            actions=[
                ft.TextButton("انصراف", on_click=lambda _: (setattr(dlg, 'open', False), page.update())),
                ft.ElevatedButton("تأیید نهایی", bgcolor="#FFCC00", color="black", on_click=register_user)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        page.dialog = dlg
        dlg.open = True
        page.update()

    # ==================== صفحه لاگین ====================
    def render(tab_index=0):
        page.controls.clear()

        if not page.session.logged_in:
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
                        ], alignment="center", spacing=12, vertical_alignment="center"),
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

                    # لینک فعال‌سازی / فراموشی رمز (اصلاح شده)
                    ft.GestureDetector(
                        content=ft.Text(
                            "فعال‌سازی / فراموشی رمز",
                            size=14,
                            color="blue",
                            text_align="center"
                        ),
                        on_click=show_register_dialog,
                        mouse_cursor=ft.MouseCursor.CLICK
                    ),

                    ft.Container(content=ft.Image(src="TopSUN-Powered.png", width=160), margin=ft.margin.Margin(top=50, bottom=30)),

                    ft.Container(expand=True, content=ft.Image(src="landscape.jpg", width=400, height=220, fit="cover"))
                ], 
                horizontal_alignment="center", 
                expand=True,
                scroll=ft.ScrollMode.AUTO
                )
            )
        else:
            page.add(
                ft.Column([
                    ft.Text("پنل TopSUNify", size=30, weight="bold"),
                    ft.Divider(),
                    ft.Text("خوش آمدید!", size=24),
                    ft.ElevatedButton("خروج", on_click=lambda e: (setattr(page.session, 'logged_in', False), render()))
                ], horizontal_alignment="center", expand=True)
            )

        page.update()

    render()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
