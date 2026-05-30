import flet as ft
import os

# ==================== تنظیمات ====================
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbygH2yHhw44Lk5Hv8okJDnRBgGw2UzoF1wsZvMGGGr7ZzhSS0Ro6WhSeVFTPM2TpsMv/exec"


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
        snack = ft.SnackBar(content=ft.Text(text), bgcolor=color, action="بستن", duration=3000)
        page.snack_bar = snack
        snack.open = True
        page.update()

    # ==================== صفحه پروفایل ====================
    def profile_page():
        return ft.Container(
            content=ft.Column([
                # هدر پروفایل
                ft.Container(
                    content=ft.Column([
                        ft.CircleAvatar(
                            foreground_image_src="https://i.pravatar.cc/150?u=reza", 
                            radius=48
                        ),
                        ft.Text(
                            "نام و نام خانوادگی | نام کاربری", 
                            size=20, 
                            weight="bold", 
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Text(
                            "شماره موبایل", 
                            size=16, 
                            color="grey", 
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(
                            content=ft.Text(
                                f"سطح دسترسی: {page.session.user_role}", 
                                size=15, 
                                color="blue", 
                                text_align=ft.TextAlign.CENTER
                            ),
                            bgcolor="#f0f0f0", 
                            padding=12, 
                            border_radius=12, 
                            margin=ft.margin.Margin(top=12, bottom=8)
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20, 
                    bgcolor="#f8f9fa", 
                    border_radius=20, 
                    margin=ft.margin.Margin(bottom=20),
                    width=380
                ),

                # لیست منوها - وسط چین قوی
                ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.PERSON_ADD, color="blue"),
                            title=ft.Text("درخواست ایجاد حساب"),
                            trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20),
                            on_click=create_account_request
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.STAR, color="orange"),
                            title=ft.Text("مشتریان منتخب"),
                            trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.WAREHOUSE, color="green"),
                            title=ft.Text("اعلام موجودی انبار"),
                            trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.SHOPPING_CART),
                            title=ft.Text("ثبت درخواست خرید"),
                            trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.GROUP),
                            title=ft.Text("همکاران منتخب"),
                            trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.PERCENT),
                            title=ft.Text("محاسبه درصد همکاری"),
                            trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET),
                            title=ft.Text("مبلغ اعتبار"),
                            trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)
                        ),
                        ft.Divider(height=25),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.SETTINGS),
                            title=ft.Text("تنظیمات"),
                            trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20),
                            on_click=open_settings
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.LOGOUT, color="red"),
                            title=ft.Text("خروج", color="red"),
                            on_click=lambda e: (setattr(page.session, 'logged_in', False), render())
                        ),
                        ft.Text("نسخه ۱.۴.۳", size=12, color="grey", text_align=ft.TextAlign.CENTER)
                    ], 
                    spacing=2, 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    width=360,                    # عرض کمتر برای وسط‌چین بهتر
                    alignment=ft.alignment.center  # وسط‌چین Container
                )
            ], 
            scroll=ft.ScrollMode.AUTO, 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400,
            margin=ft.margin.Margin(left=15, right=15),
            expand=True,
            alignment=ft.alignment.center
        )

    def create_account_request(e):
        show_message("درخواست ایجاد حساب ارسال شد", "blue")

    def open_settings(e):
        show_message("تنظیمات باز شد", "blue")

    # ==================== رندر اصلی ====================
    def render(tab_index=0):
        page.controls.clear()

        if not page.session.logged_in:
            # ... (بخش لاگین بدون تغییر)
            page.add(
                ft.Container(
                    content=ft.Column([
                        ft.Container(content=ft.Image(src="TopSUNify.png", width=190), margin=ft.margin.Margin(top=40, bottom=40)),
                        ft.Container(content=ft.TextField(label="نام کاربری", width=340, border_radius=12, prefix_icon=ft.Icons.PERSON, text_align=ft.TextAlign.RIGHT), margin=ft.margin.Margin(bottom=20)),
                        ft.Container(
                            content=ft.Row([
                                ft.Container(content=ft.Icon(ft.Icons.FINGERPRINT, size=42, color="#FFCC00"), on_click=lambda e: show_message("احراز هویت بیومتریک", "orange"), padding=10, border_radius=12),
                                ft.TextField(label="رمز عبور", password=True, width=270, border_radius=12, prefix_icon=ft.Icons.LOCK, text_align=ft.TextAlign.RIGHT)
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=12),
                            margin=ft.margin.Margin(bottom=30)
                        ),
                        ft.ElevatedButton("ورود به TopSUNify", width=340, bgcolor="#FFCC00", color="black", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)), on_click=lambda e: (setattr(page.session, 'logged_in', True), render())),
                        ft.TextButton("فعال‌سازی / فراموشی رمز", style=ft.ButtonStyle(color={"": "blue"})),
                        ft.Container(content=ft.Image(src="TopSUN-Powered.png", width=160), margin=ft.margin.Margin(top=50, bottom=30)),
                        ft.Container(content=ft.Image(src="landscape.jpg", width=400, height=220, fit="cover"), expand=True)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
                    width=400,
                    margin=ft.margin.Margin(left=15, right=15),
                    expand=True
                )
            )
        else:
            contents = [
                ft.Text("داشبورد مدیریتی", size=25, weight="bold"),
                ft.Text("بخش پیش‌فاکتورها", size=25, weight="bold"),
                ft.Column([ft.Image(src="TopSUNify-1.png", width=200), ft.Text("خانه اصلی", size=25, weight="bold")], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Text("اطلاعات فنی سیستم", size=25, weight="bold"),
                profile_page()
            ]

            main_content = ft.Container(
                content=contents[tab_index], 
                expand=True, 
                width=400, 
                margin=ft.margin.Margin(left=15, right=15),
                alignment=ft.alignment.center
            )

            nav_bar = ft.Container(
                content=ft.Row([
                    ft.Container(content=ft.Image(src="dashboard.png", width=32, height=32), on_click=lambda _: render(0), padding=8),
                    ft.Container(content=ft.Image(src="invoice.png", width=32, height=32), on_click=lambda _: render(1), padding=8),
                    ft.Container(content=ft.Image(src="TopSUNify-1.png", width=32, height=32), on_click=lambda _: render(2), padding=8),
                    ft.Container(content=ft.Image(src="technical.png", width=32, height=32), on_click=lambda _: render(3), padding=8),
                    ft.Container(content=ft.Image(src="profile.png", width=32, height=32), on_click=lambda _: render(4), padding=8),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                bgcolor="white",
                padding=12,
                border=ft.Border(top=ft.BorderSide(1, "#e0e0e0"), bottom=ft.BorderSide(1, "#e0e0e0"))
            )

            page.add(
                ft.Column([
                    ft.Text("پنل TopSUNify", size=30, weight="bold"),
                    ft.Divider(),
                    main_content,
                    nav_bar
                ], expand=True)
            )

        page.update()

    render()


# ==================== اجرا ====================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
