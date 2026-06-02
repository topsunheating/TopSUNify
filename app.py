import flet as ft
import os
import datetime

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

    def toggle_theme(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()

    # ==================== صفحه گرمایش از کف (سه روش) ====================
    def floor_heating_page():
        tab = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text="📂 آپلود فایل DWG/DXF", content=ft.Column([ft.Text("در حال توسعه... (آپلود فایل اتوکد)", size=16)], horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
                ft.Tab(text="⌨️ ورود دستی ابعاد", content=ft.Column([
                    ft.Text("ابعاد اتاق‌ها را وارد کنید", size=18, weight="bold"),
                    ft.TextField(label="نام فضا", width=350),
                    ft.Row([ft.TextField(label="عرض (متر)", width=170), ft.TextField(label="طول (متر)", width=170)]),
                    ft.ElevatedButton("اضافه کردن اتاق", width=350, bgcolor="#1565C0", color="white"),
                    ft.Divider(),
                    ft.Text("لیست اتاق‌ها", size=16, weight="bold"),
                ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
                ft.Tab(text="✍️ مقادیر مستقیم", content=ft.Column([
                    ft.TextField(label="فیلم عرض ۸۰ متر", width=350),
                    ft.TextField(label="فیلم عرض ۴۰ متر", width=350),
                    ft.TextField(label="عایق (مترمربع)", width=350),
                    ft.TextField(label="تعداد ترموستات", width=350),
                    ft.TextField(label="تعداد تابلو فرمان", width=350),
                    ft.ElevatedButton("صدور پیش‌فاکتور", width=350, bgcolor="#1565C0", color="white", on_click=lambda e: show_message("پیش‌فاکتور صادر شد", "green")),
                ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
            ],
            expand=1
        )

        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(1)),
                        ft.Text("گرمایش از کف (سیستم هوشمند)", size=20, weight="bold")
                    ]),
                    padding=10
                ),
                tab
            ], scroll=ft.ScrollMode.AUTO),
            width=400,
            expand=True,
            padding=15
        )

    # ==================== سایر صفحات (بدون تغییر) ====================
    def dashboard_page():
        return ft.Container(content=ft.Text("داشبورد مدیریتی", size=25, weight="bold"), width=400, expand=True)

    def pre_invoice_page():
        products = [
            ("گرمایش از کف", ft.Icons.FLOOR, lambda e: render(18)),
            ("زیرفرشی", ft.Icons.RUGS, lambda e: show_message("به زودی", "blue")),
            ("رادیاتور", ft.Icons.RADIATOR, lambda e: show_message("به زودی", "blue")),
            ("حوله خشک کن", ft.Icons.DRY_CLEAN, lambda e: show_message("به زودی", "blue")),
            ("یخ زدایی رمپ", ft.Icons.SNOWMOBILE, lambda e: show_message("به زودی", "blue")),
            ("یخ زدایی پله", ft.Icons.STAIRS, lambda e: show_message("به زودی", "blue")),
            ("گرمکن مخزن", ft.Icons.WATER_HEATER, lambda e: show_message("به زودی", "blue")),
            ("گرمکن صندلی", ft.Icons.CHAIR, lambda e: show_message("به زودی", "blue")),
            ("رستورانی", ft.Icons.RESTAURANT, lambda e: show_message("به زودی", "blue")),
            ("عایق بازتابشی", ft.Icons.INSULATION, lambda e: show_message("به زودی", "blue")),
        ]

        grid = ft.GridView(runs_count=2, max_extent=160, spacing=12, run_spacing=12, padding=15, expand=True)
        for name, icon, action in products:
            grid.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(icon, size=48, color="#1565C0"),
                        ft.Text(name, size=15, weight="bold", text_align=ft.TextAlign.CENTER)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    width=170, height=100, bgcolor="#ffffff", border_radius=12,
                    alignment=ft.Alignment(0, 0), shadow=ft.BoxShadow(blur_radius=6, color="#e0e0e0"),
                    on_click=action, ink=True
                )
            )

        return ft.Container(
            content=ft.Column([ft.Text("نوع محصول مورد نظر را انتخاب کنید", size=18, weight="bold", text_align=ft.TextAlign.CENTER), grid], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            width=400, margin=ft.margin.Margin(left=15, right=15), expand=True
        )

    # بقیه صفحات (commission, credit, theme, update, network, rules, about, ...) همان کد قبلی هستند
    # برای کوتاه شدن اینجا فقط profile_page و render را می‌نویسم (بقیه را از کد قبلی کپی کنید)

    def profile_page():
        return ft.Container(
            content=ft.Column([
                # هدر پروفایل (همان قبلی)
                ft.Container(content=ft.Column([ft.CircleAvatar(foreground_image_src="https://i.pravatar.cc/150?u=reza", radius=48), ft.Text("نام و نام خانوادگی | نام کاربری", size=20, weight="bold", text_align=ft.TextAlign.CENTER), ft.Text("شماره موبایل", size=16, color="grey", text_align=ft.TextAlign.CENTER), ft.Container(content=ft.Text(f"سطح دسترسی: {page.session.user_role}", size=15, color="blue", text_align=ft.TextAlign.CENTER), bgcolor="#f0f0f0", padding=12, border_radius=12, margin=ft.margin.Margin(top=12, bottom=8))], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=20, bgcolor="#f8f9fa", border_radius=20, margin=ft.margin.Margin(bottom=20), width=380),
                ft.Container(content=ft.Column([
                    # ... بقیه گزینه‌ها
                    ft.ListTile(leading=ft.Icon(ft.Icons.SHOPPING_CART, color="orange"), title=ft.Text("ثبت درخواست خرید"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(10)),
                    # بقیه گزینه‌ها بدون تغییر
                ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=360)
            ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, margin=ft.margin.Margin(left=15, right=15), expand=True
        )

    # ==================== رندر اصلی ====================
    def render(tab_index=0):
        page.controls.clear()
        if not page.session.logged_in:
            # صفحه لاگین (همان قبلی)
            page.add(...)  # کد لاگین شما
        else:
            contents = [
                dashboard_page(), pre_invoice_page(), home_page(), technical_page(),
                profile_page(), settings_page(), account_request_page(),
                selected_customers_page(), inventory_page(), colleagues_page(),
                purchase_request_page(), commission_page(), credit_page(),
                theme_page(), update_page(), network_page(), rules_page(), about_page(),
                floor_heating_page()   # index 18
            ]
            # ... بقیه کد رندر (nav_bar و غیره) همان قبلی
            main_content = ft.Container(content=contents[tab_index], expand=True, width=400, margin=ft.margin.Margin(left=15, right=15))
            # nav_bar ...
            page.add(...)  # ستون اصلی
        page.update()

    render()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
