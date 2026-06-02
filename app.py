import flet as ft
import os

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

    # ==================== صفحات ساده ====================
    def dashboard_page():
        return ft.Container(content=ft.Text("داشبورد مدیریتی", size=25, weight="bold"), width=400, expand=True)

    def pre_invoice_page():
        return ft.Container(content=ft.Text("بخش پیش‌فاکتورها", size=25, weight="bold"), width=400, expand=True)

    def home_page():
        return ft.Container(content=ft.Text("خانه اصلی", size=25, weight="bold"), width=400, expand=True)

    def technical_page():
        return ft.Container(content=ft.Text("اطلاعات فنی سیستم", size=25, weight="bold"), width=400, expand=True)

    def settings_page():
        return ft.Container(content=ft.Text("تنظیمات", size=25, weight="bold"), width=400, expand=True)

    # ==================== صفحات درخواستی ====================
    def commission_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("محاسبه درصد همکاری", size=20, weight="bold")]), padding=10),
                ft.Text("فاکتورهای تسویه شده این ماه: ۴۸,۵۰۰,۰۰۰ تومان", size=16),
                ft.Text("درصد همکاری شما: ۱۲٪", size=22, weight="bold", color="blue"),
                ft.Text("مبلغ قابل تسویه: ۵,۸۲۰,۰۰۰ تومان", size=18, weight="bold", color="green"),
                ft.ElevatedButton("درخواست تسویه حساب", bgcolor="#1565C0", color="white", width=350, on_click=lambda e: show_message("درخواست تسویه ارسال شد", "green"))
            ], scroll=ft.ScrollMode.AUTO, spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )

    def credit_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("مبلغ اعتبار", size=20, weight="bold")]), padding=10),
                ft.Text("اعتبار فعلی شما: ۱۲۰,۰۰۰,۰۰۰ تومان", size=18, weight="bold", color="green"),
                ft.TextField(label="مبلغ درخواستی افزایش اعتبار", width=350),
                ft.Dropdown(label="نوع تضمین", width=350, options=[ft.dropdown.Option("چک"), ft.dropdown.Option("سفته"), ft.dropdown.Option("واریز نقدی")]),
                ft.ElevatedButton("ارسال درخواست افزایش اعتبار", bgcolor="#1565C0", color="white", width=350, on_click=lambda e: show_message("درخواست افزایش اعتبار ارسال شد", "green"))
            ], scroll=ft.ScrollMode.AUTO, spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )

    def theme_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("نمایش (تم)", size=20, weight="bold")]), padding=10),
                ft.ListTile(leading=ft.Icon(ft.Icons.LIGHT_MODE), title=ft.Text("تم روشن"), on_click=lambda e: (setattr(page, 'theme_mode', 'light'), page.update(), show_message("تم روشن فعال شد", "blue"))),
                ft.ListTile(leading=ft.Icon(ft.Icons.DARK_MODE), title=ft.Text("تم تیره"), on_click=lambda e: (setattr(page, 'theme_mode', 'dark'), page.update(), show_message("تم تیره فعال شد", "blue")))
            ], scroll=ft.ScrollMode.AUTO, spacing=10),
            width=400, expand=True, padding=15
        )

    def update_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("بروزرسانی", size=20, weight="bold")]), padding=10),
                ft.Text("نسخه فعلی: ۱.۴.۳", size=17, weight="bold"),
                ft.Divider(),
                ft.Text("نسخه ۱.۴.۵ - ۱۴۰۴/۰۳/۱۰", size=16, weight="bold"),
                ft.Text("• بهبود سرعت بارگذاری\n• رفع باگ PDF\n• اضافه شدن صفحه درصد همکاری", size=15),
                ft.Divider(),
                ft.Text("نسخه ۱.۴.۴ - ۱۴۰۴/۰۲/۲۵", size=16, weight="bold"),
                ft.Text("• بهینه‌سازی تم تیره", size=15),
                ft.ElevatedButton("شما آخرین نسخه را دارید", bgcolor="green", color="white", width=350, on_click=lambda e: show_message("شما آخرین نسخه را نصب دارید", "green"))
            ], scroll=ft.ScrollMode.AUTO, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )

    def network_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("شبکه فروش و خدمات", size=20, weight="bold")]), padding=10),
                ft.Text("نقشه شبکه فروش و خدمات همکاران\n\n(در نسخه کامل نقشه تعاملی نمایش داده خواهد شد)", size=16, text_align=ft.TextAlign.CENTER)
            ], scroll=ft.ScrollMode.AUTO, spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )

    def rules_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("قوانین همکاری", size=20, weight="bold")]), padding=10),
                ft.Text("متن کامل قوانین و شرایط همکاری\n\nدر نسخه کامل اینجا قرار خواهد گرفت.", size=16, text_align=ft.TextAlign.CENTER)
            ], scroll=ft.ScrollMode.AUTO, spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )

    def about_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("درباره ما", size=20, weight="bold")]), padding=10),
                ft.Text("شرکت تاپسان\nتولیدکننده سیستم‌های گرمایشی پیشرفته\n\nنسخه اپلیکیشن: ۱.۴.۳", size=16, text_align=ft.TextAlign.CENTER)
            ], scroll=ft.ScrollMode.AUTO, spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )

    # ==================== صفحه پروفایل ====================
    def profile_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Column([ft.CircleAvatar(foreground_image_src="https://i.pravatar.cc/150?u=reza", radius=48), ft.Text("نام و نام خانوادگی | نام کاربری", size=20, weight="bold", text_align=ft.TextAlign.CENTER), ft.Text("شماره موبایل", size=16, color="grey", text_align=ft.TextAlign.CENTER), ft.Container(content=ft.Text(f"سطح دسترسی: {page.session.user_role}", size=15, color="blue", text_align=ft.TextAlign.CENTER), bgcolor="#f0f0f0", padding=12, border_radius=12, margin=ft.margin.Margin(top=12, bottom=8))], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=20, bgcolor="#f8f9fa", border_radius=20, margin=ft.margin.Margin(bottom=20), width=380),
                ft.Container(content=ft.Column([
                    ft.ListTile(leading=ft.Icon(ft.Icons.PERSON_ADD, color="blue"), title=ft.Text("درخواست ایجاد حساب"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(6)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.STAR, color="orange"), title=ft.Text("مشتریان منتخب"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(7)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.WAREHOUSE, color="green"), title=ft.Text("اعلام موجودی انبار"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(8)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.SHOPPING_CART, color="orange"), title=ft.Text("ثبت درخواست خرید"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(10)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.GROUP), title=ft.Text("همکاران منتخب"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(9)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.PERCENT, color="purple"), title=ft.Text("محاسبه درصد همکاری"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(11)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, color="green"), title=ft.Text("مبلغ اعتبار"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(12)),
                    ft.Divider(height=25),
                    ft.ListTile(leading=ft.Icon(ft.Icons.PALETTE, color="purple"), title=ft.Text("نمایش (تم روشن/تیره)"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(13)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.UPDATE, color="blue"), title=ft.Text("بروزرسانی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(14)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.MAP, color="green"), title=ft.Text("شبکه فروش و خدمات"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(15)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.GAVEL, color="amber"), title=ft.Text("قوانین"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(16)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.INFO, color="blue"), title=ft.Text("درباره ما"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(17)),
                    ft.Divider(height=25),
                    ft.ListTile(leading=ft.Icon(ft.Icons.SETTINGS, color="grey"), title=ft.Text("تنظیمات"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(5)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.LOGOUT, color="red"), title=ft.Text("خروج", color="red"), on_click=lambda e: (setattr(page.session, 'logged_in', False), render())),
                    ft.Text("نسخه ۱.۴.۳", size=12, color="grey", text_align=ft.TextAlign.CENTER)
                ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=360)
            ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, margin=ft.margin.Margin(left=15, right=15), expand=True
        )

    # ==================== رندر اصلی ====================
    def render(tab_index=0):
        page.controls.clear()
        if not page.session.logged_in:
            page.add(
                ft.Container(
                    content=ft.Column([
                        ft.Container(content=ft.Image(src="TopSUNify.png", width=190), margin=ft.margin.Margin(top=40, bottom=40)),
                        ft.Container(content=ft.TextField(label="نام کاربری", width=340, border_radius=12, prefix_icon=ft.Icons.PERSON, text_align=ft.TextAlign.RIGHT), margin=ft.margin.Margin(bottom=20)),
                        ft.Container(content=ft.Row([ft.Container(content=ft.Icon(ft.Icons.FINGERPRINT, size=42, color="#FFCC00"), on_click=lambda e: show_message("احراز هویت بیومتریک", "orange"), padding=10, border_radius=12), ft.TextField(label="رمز عبور", password=True, width=270, border_radius=12, prefix_icon=ft.Icons.LOCK, text_align=ft.TextAlign.RIGHT)], alignment=ft.MainAxisAlignment.CENTER, spacing=12), margin=ft.margin.Margin(bottom=30)),
                        ft.ElevatedButton("ورود به TopSUNify", width=340, bgcolor="#FFCC00", color="black", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)), on_click=lambda e: (setattr(page.session, 'logged_in', True), render())),
                        ft.TextButton("فعال‌سازی / فراموشی رمز", style=ft.ButtonStyle(color={"": "blue"})),
                        ft.Container(content=ft.Image(src="TopSUN-Powered.png", width=160), margin=ft.margin.Margin(top=50, bottom=30)),
                        ft.Container(content=ft.Image(src="landscape.jpg", width=400, height=220, fit="cover"), expand=True)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
                    width=400, margin=ft.margin.Margin(left=15, right=15), expand=True
                )
            )
        else:
            contents = [
                dashboard_page(), pre_invoice_page(), home_page(), technical_page(),
                profile_page(), settings_page(), account_request_page(),
                selected_customers_page(), inventory_page(), colleagues_page(),
                purchase_request_page(), commission_page(), credit_page(),
                theme_page(), update_page(), network_page(), rules_page(), about_page()
            ]
            main_content = ft.Container(content=contents[tab_index], expand=True, width=400, margin=ft.margin.Margin(left=15, right=15))
            nav_bar = ft.Container(
                content=ft.Row([
                    ft.Container(content=ft.Image(src="dashboard.png", width=32, height=32), on_click=lambda _: render(0), padding=8),
                    ft.Container(content=ft.Image(src="invoice.png", width=32, height=32), on_click=lambda _: render(1), padding=8),
                    ft.Container(content=ft.Image(src="TopSUNify-1.png", width=32, height=32), on_click=lambda _: render(2), padding=8),
                    ft.Container(content=ft.Image(src="technical.png", width=32, height=32), on_click=lambda _: render(3), padding=8),
                    ft.Container(content=ft.Image(src="profile.png", width=32, height=32), on_click=lambda _: render(4), padding=8),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                bgcolor="white", padding=12
            )
            page.add(
                ft.Column([
                    ft.Container(content=ft.Image(src="TopSUNify.png", width=80), margin=ft.margin.Margin(top=10, bottom=10)),
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
