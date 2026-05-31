import flet as ft
import os
import requests

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

    # ==================== تغییر تم ====================
    def toggle_theme(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()
        show_message(f"تم تغییر کرد به: {page.theme_mode}", "blue")

    # ==================== صفحه پیش‌فاکتورها ====================
    def pre_invoice_page():
        products = [
            ("گرمایش از کف", ft.Icons.HEATING, "#1565C0"),
            ("زیرفرشی", ft.Icons.RUGS, "#2E7D32"),
            ("رادیاتور", ft.Icons.RADIATOR, "#C62828"),
            ("حوله خشک کن", ft.Icons.DRY_CLEAN, "#8E24AA"),
            ("یخ زدایی رمپ", ft.Icons.AC_UNIT, "#455A64"),
            ("یخ زدایی پله", ft.Icons.STAIRS, "#FF8F00"),
            ("گرمکن مخزن", ft.Icons.WATER, "#0277BD"),
            ("گرمکن صندلی", ft.Icons.CHAIR, "#6A1B9A"),
            ("رستورانی", ft.Icons.RESTAURANT, "#D84315"),
        ]

        grid = ft.GridView(
            runs_count=3,
            max_extent=130,
            spacing=15,
            run_spacing=15,
            padding=10,
            expand=True,
        )

        for name, icon, color in products:
            grid.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(icon, size=48, color=color),
                        ft.Text(name, size=13, weight="bold", text_align=ft.TextAlign.CENTER),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    width=110,
                    height=120,
                    bgcolor="#ffffff",
                    border_radius=15,
                    shadow=ft.BoxShadow(blur_radius=8, color="#e0e0e0"),
                    on_click=lambda e, n=name: show_message(f"در حال ورود به پیش‌فاکتور {n}"),
                    ink=True,
                )
            )

        return ft.Container(
            content=ft.Column([
                ft.Text("نوع محصول مورد نظر را انتخاب کنید", size=18, weight="bold", text_align=ft.TextAlign.CENTER),
                ft.Divider(height=10),
                grid
            ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            width=400,
            margin=ft.margin.Margin(left=15, right=15),
            expand=True
        )

    # ==================== صفحات دیگر (خلاصه) ====================
    def home_page():
        return ft.Container(
            content=ft.Column([
                ft.Image(src="TopSUNify-1.png", width=180),
                ft.Text("خوش آمدید به TopSUNify", size=20, weight="bold", text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
            width=400,
            margin=ft.margin.Margin(left=15, right=15),
            expand=True
        )

    def technical_page():
        return ft.Container(
            content=ft.Text("اطلاعات فنی سیستم", size=22, weight="bold", text_align=ft.TextAlign.CENTER),
            width=400,
            margin=ft.margin.Margin(left=15, right=15),
            expand=True,
            alignment=ft.Alignment(0, 0)
        )

    def profile_page():
        return ft.Container(
            content=ft.Text("پروفایل کاربری", size=22, weight="bold", text_align=ft.TextAlign.CENTER),
            width=400,
            margin=ft.margin.Margin(left=15, right=15),
            expand=True,
            alignment=ft.Alignment(0, 0)
        )

    def settings_page():
        return ft.Container(
            content=ft.Text("تنظیمات", size=22, weight="bold", text_align=ft.TextAlign.CENTER),
            width=400,
            margin=ft.margin.Margin(left=15, right=15),
            expand=True,
            alignment=ft.Alignment(0, 0)
        )

    # ==================== رندر اصلی ====================
    def render(tab_index=0):
        page.controls.clear()

        if not page.session.logged_in:
            # صفحه لاگین
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
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
                    width=400,
                    margin=ft.margin.Margin(left=15, right=15),
                    expand=True
                )
            )
        else:
            contents = [
                ft.Text("داشبورد مدیریتی", size=18, weight="bold"),
                pre_invoice_page(),      # تب 1 - پیش فاکتورها
                home_page(),             # تب 2
                technical_page(),        # تب 3
                profile_page(),          # تب 4
                settings_page()          # تب 5
            ]

            main_content = ft.Container(
                content=contents[tab_index],
                expand=True,
                width=400,
                margin=ft.margin.Margin(left=15, right=15)
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
            )

            page.add(
                ft.Column([
                    ft.Container(content=ft.Image(src="TopSUNify.png", width=80), margin=ft.margin.Margin(top=10, bottom=5)),
                    main_content,
                    nav_bar
                ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )

        page.update()

    render()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
