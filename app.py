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
            ("گرمایش از کف", ft.Icons.FLOORING, "#1565C0"),
            ("زیرفرشی", ft.Icons.RUGS, "#2E7D32"),
            ("رادیاتور", ft.Icons.RADIATOR, "#C62828"),
            ("حوله خشک کن", ft.Icons.DRY_CLEAN, "#8E24AA"),
            ("یخ زدایی رمپ", ft.Icons.SNOWMOBILE, "#455A64"),
            ("یخ زدایی پله", ft.Icons.STAIRS, "#FF8F00"),
            ("گرمکن مخزن", ft.Icons.WATER, "#0277BD"),
            ("گرمکن صندلی", ft.Icons.CHAIR, "#6A1B9A"),
            ("رستورانی", ft.Icons.RESTAURANT_MENU, "#D84315"),
        ]

        def open_pre_invoice(product_name):
            show_message(f"در حال ورود به صدور پیش‌فاکتور {product_name}", "blue")

        grid = ft.GridView(
            expand=True,
            runs_count=3,
            max_extent=130,
            spacing=15,
            run_spacing=15,
            padding=10,
        )

        for name, icon, color in products:
            grid.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(icon, size=48, color=color),
                        ft.Text(name, size=13, weight="bold", text_align=ft.TextAlign.CENTER),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    width=110,
                    height=110,
                    bgcolor="#ffffff",
                    border_radius=15,
                    shadow=ft.BoxShadow(blur_radius=8, color="#e0e0e0"),
                    on_click=lambda e, n=name: open_pre_invoice(n),
                    ink=True,
                    alignment=ft.Alignment(0, 0)
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
        return ft.Container(...)  # همان کد قبلی شما

    def technical_page():
        return ft.Container(...)  # همان کد قبلی

    def profile_page():
        return ft.Container(...)  # همان کد قبلی

    def settings_page():
        return ft.Container(...)  # همان کد قبلی

    # ==================== رندر اصلی ====================
    def render(tab_index=0):
        page.controls.clear()

        if not page.session.logged_in:
            # صفحه لاگین (همان قبلی)
            page.add(
                ft.Container(
                    content=ft.Column([
                        ft.Container(content=ft.Image(src="TopSUNify.png", width=190), margin=ft.margin.Margin(top=40, bottom=40)),
                        # ... بقیه لاگین
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
                    width=400,
                    margin=ft.margin.Margin(left=15, right=15),
                    expand=True
                )
            )
        else:
            contents = [
                ft.Text("داشبورد مدیریتی", size=18, weight="bold"),
                pre_invoice_page(),           # ← تب 1: پیش‌فاکتورها
                home_page(),                  # تب 2: خانه اصلی
                technical_page(),             # تب 3: اطلاعات فنی
                profile_page(),               # تب 4: پروفایل
                settings_page()               # تب 5: تنظیمات
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
                    ft.Container(content=ft.Image(src="TopSUNify.png", width=100), margin=ft.margin.Margin(top=10, bottom=10)),
                    ft.Divider(),
                    main_content,
                    nav_bar
                ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )

        page.update()

    render()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
