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
        page.session.username = "رضا تلچی"

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

    # ==================== داشبورد مدیریتی ====================
    def dashboard_page():
        def select_month(e, month_name, month_num):
            show_message(f"بازه {month_name} انتخاب شد")

        months = [
            ("فروردین", "01"), ("اردیبهشت", "02"), ("خرداد", "03"),
            ("تیر", "04"), ("مرداد", "05"), ("شهریور", "06"),
            ("مهر", "07"), ("آبان", "08"), ("آذر", "09"),
            ("دی", "10"), ("بهمن", "11"), ("اسفند", "12")
        ]

        # نوار ماه‌ها دقیقاً مثل عکس شما
        month_buttons = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text(num, size=22, weight="bold", color="#1565C0" if i == 4 else "#555555"),
                        ft.Text(name, size=14, color="#1565C0" if i == 4 else "#666666"),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                    width=85,
                    height=85,
                    bgcolor="#1565C0" if i == 4 else "white",
                    border_radius=20,
                    alignment=ft.Alignment(0.5, 0.5),
                    shadow=ft.BoxShadow(blur_radius=6, color="#e0e0e0") if i != 4 else None,
                    on_click=lambda e, n=name, num=num: select_month(e, n, num)
                ) for i, (name, num) in enumerate(months)
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
        )

        # دکمه مشاهده اطلاعات
        view_button = ft.ElevatedButton(
            "مشاهده اطلاعات",
            width=320,
            bgcolor="#1565C0",
            color="white",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)),
            on_click=lambda e: show_message("در حال نمایش گزارش‌ها...")
        )

        # کارت‌های گزارش (۳ ستونی)
        report_cards = ft.GridView(
            runs_count=3,
            max_extent=175,
            spacing=12,
            run_spacing=12,
            padding=10,
            expand=True,
        )

        cards_data = [
            ("فاکتورهای تسویه شده", ft.Icons.CHECK_CIRCLE, "#1976D2"),
            ("فاکتورهای فروش", ft.Icons.SHOPPING_CART, "#388E3C"),
            ("پیش فاکتورها", ft.Icons.RECEIPT_LONG, "#1565C0"),
            ("پروژه‌های نصب شده", ft.Icons.HOME_WORK, "#7B1FA2"),
            ("فاکتورهای باز", ft.Icons.PENDING, "#F57C00"),
        ]

        for title, icon, color in cards_data:
            report_cards.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(icon, size=36, color=color),
                        ft.Text(title, size=13.5, weight="bold", text_align=ft.TextAlign.CENTER),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    bgcolor="white",
                    border_radius=16,
                    padding=14,
                    shadow=ft.BoxShadow(blur_radius=8, color="#e0e0e0"),
                    expand=True,
                    on_click=lambda e, t=title: show_message(f"بخش {t}"),
                    ink=True,
                )
            )

        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Image(src="TopSUNify.png", width=155), margin=ft.margin.Margin(top=8, bottom=12)),
                
                ft.Container(
                    content=ft.Dropdown(value="رضا تلچی", options=[ft.dropdown.Option("رضا تلچی"), ft.dropdown.Option("زیرمجموعه فروش")],
                                      width=320, border_radius=30, bgcolor="white"),
                    margin=ft.margin.Margin(bottom=15)
                ),

                ft.Text("انتخاب ماه", size=17, weight="bold", text_align=ft.TextAlign.CENTER),
                month_buttons,
                ft.Divider(height=10),
                view_button,
                ft.Divider(height=20),

                ft.Text("گزارش‌های مالی و عملیاتی", size=18, weight="bold", text_align=ft.TextAlign.CENTER),
                report_cards,
            ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
            width=400,
            margin=ft.margin.Margin(left=15, right=15),
            expand=True
        )

    # ==================== صفحه ورود ====================
    def login_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Image(src="TopSUNify.png", width=190), margin=ft.margin.Margin(top=50, bottom=40)),
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
                ft.Container(content=ft.Image(src="TopSUN-Powered.png", width=160), margin=ft.margin.Margin(top=40, bottom=20)),
                ft.Container(content=ft.Image(src="landscape.jpg", width=400, height=210, fit="cover")),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
            width=400,
            margin=ft.margin.Margin(left=15, right=15),
            expand=True
        )

# ==================== بقیه صفحات (بدون تغییر) ====================
    def pre_invoice_page():
        products = ["گرمایش از کف", "زیرفرشی", "رادیاتور", "حوله خشک کن", "یخ زدایی رمپ",
                   "یخ زدایی پله", "گرمکن مخزن", "گرمکن صندلی", "رستورانی", "عایق بازتابشی"]
        grid = ft.GridView(runs_count=2, max_extent=170, spacing=12, run_spacing=12, padding=10, expand=True)
        for name in products:
            grid.controls.append(
                ft.Container(
                    content=ft.Text(name, size=15, weight="bold", text_align=ft.TextAlign.CENTER, color="#1565C0"),
                    width=160, height=80, bgcolor="#ffffff", border_radius=12,
                    alignment=ft.Alignment(0, 0), shadow=ft.BoxShadow(blur_radius=6, color="#e0e0e0"),
                    on_click=lambda e, n=name: show_message(f"پیش‌فاکتور {n}"), ink=True,
                )
            )
        return ft.Container(
            content=ft.Column([ft.Text("نوع محصول مورد نظر را انتخاب کنید", size=18, weight="bold", text_align=ft.TextAlign.CENTER), ft.Divider(), grid],
                              scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, margin=ft.margin.Margin(left=15, right=15), expand=True
        )
    def home_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Image(src="TopSUNify-1.png", width=120), margin=ft.margin.Margin(top=30, bottom=20)),
                ft.Text("خوش آمدید به TopSUNify", size=22, weight="bold", text_align=ft.TextAlign.CENTER),
                ft.Text("مرکز خدمات و پشتیبانی", size=16, color="grey", text_align=ft.TextAlign.CENTER),
                ft.Container(
                    content=ft.Column([
                        ft.ListTile(leading=ft.Icon(ft.Icons.SHIELD, color="green"), title=ft.Text("ثبت گارانتی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                        ft.ListTile(leading=ft.Icon(ft.Icons.INSTALL_DESKTOP, color="blue"), title=ft.Text("درخواست نصب اولیه"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                        ft.ListTile(leading=ft.Icon(ft.Icons.SUPPORT_AGENT, color="orange"), title=ft.Text("درخواست خدمات فنی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                        ft.ListTile(leading=ft.Icon(ft.Icons.SHOPPING_CART_CHECKOUT, color="purple"), title=ft.Text("ثبت درخواست سفارشی و عمده"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                        ft.ListTile(leading=ft.Icon(ft.Icons.PRINT, color="red"), title=ft.Text("درخواست چاپ طرح سفارشی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                    ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    width=380
                )
            ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, margin=ft.margin.Margin(left=15, right=15), expand=True
        )
    def technical_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Text("اطلاعات فنی", size=22, weight="bold", text_align=ft.TextAlign.CENTER), padding=20),
                ft.Container(
                    content=ft.Column([
                        ft.ListTile(leading=ft.Icon(ft.Icons.BOOK, color="blue"), title=ft.Text("کاتالوگ محصولات"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                        ft.ListTile(leading=ft.Icon(ft.Icons.PRICE_CHANGE, color="green"), title=ft.Text("لیست قیمت"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                        ft.ListTile(leading=ft.Icon(ft.Icons.WORK_HISTORY, color="purple"), title=ft.Text("رزومه شرکت"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                        ft.ListTile(leading=ft.Icon(ft.Icons.DESCRIPTION, color="orange"), title=ft.Text("پروپوزال و گزارش فنی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                        ft.ListTile(leading=ft.Icon(ft.Icons.IMAGE, color="pink"), title=ft.Text("تصاویر و فیلم پروژه‌ها"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                        ft.ListTile(leading=ft.Icon(ft.Icons.VIDEO_LIBRARY, color="red"), title=ft.Text("فیلم‌های تبلیغاتی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                    ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    width=380
                )
            ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, margin=ft.margin.Margin(left=15, right=15), expand=True
        )
    def settings_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("تنظیمات", size=24, weight="bold")]),
                            padding=15, bgcolor="#f8f9fa", border_radius=20, margin=ft.margin.Margin(bottom=20)),
                ft.Column([
                    ft.ListTile(leading=ft.Icon(ft.Icons.PERSON), title=ft.Text("تغییر نام کاربری"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.SAVE), title=ft.Text("ذخیره نام کاربری"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.FINGERPRINT), title=ft.Text("ورود با اثر انگشت"), trailing=ft.Switch(value=False)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.LOCK), title=ft.Text("تغییر رمز ورود"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.PHONE), title=ft.Text("تغییر شماره تلفن همراه"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.DEVICES), title=ft.Text("دستگاه‌های فعال"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                    ft.Divider(height=20),
                    ft.ListTile(leading=ft.Icon(ft.Icons.DELETE_FOREVER, color="red"), title=ft.Text("حذف تنظیمات و خروج از نرم‌افزار", color="red"), on_click=lambda e: (setattr(page.session, 'logged_in', False), render())),
                ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ], scroll=ft.ScrollMode.AUTO),
            width=400, margin=ft.margin.Margin(left=15, right=15), expand=True
        )
    def profile_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Column([ft.CircleAvatar(foreground_image_src="https://i.pravatar.cc/150?u=reza", radius=48),
                    ft.Text("نام و نام خانوادگی | نام کاربری", size=20, weight="bold", text_align=ft.TextAlign.CENTER),
                    ft.Text("شماره موبایل", size=16, color="grey", text_align=ft.TextAlign.CENTER),
                    ft.Container(content=ft.Text(f"سطح دسترسی: {page.session.user_role}", size=15, color="blue", text_align=ft.TextAlign.CENTER), bgcolor="#f0f0f0", padding=12, border_radius=12, margin=ft.margin.Margin(top=12, bottom=8))
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=20, bgcolor="#f8f9fa", border_radius=20, margin=ft.margin.Margin(bottom=20), width=380),
                ft.Container(content=ft.Column([
                    ft.ListTile(leading=ft.Icon(ft.Icons.PERSON_ADD, color="blue"), title=ft.Text("درخواست ایجاد حساب"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=create_account_request),
                    ft.ListTile(leading=ft.Icon(ft.Icons.STAR, color="orange"), title=ft.Text("مشتریان منتخب"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.WAREHOUSE, color="green"), title=ft.Text("اعلام موجودی انبار"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.SHOPPING_CART), title=ft.Text("ثبت درخواست خرید"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.GROUP), title=ft.Text("همکاران منتخب"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.PERCENT), title=ft.Text("محاسبه درصد همکاری"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET), title=ft.Text("مبلغ اعتبار"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                    ft.Divider(height=25),
                    ft.ListTile(leading=ft.Icon(ft.Icons.PALETTE, color="purple"), title=ft.Text("نمایش (تم روشن/تیره)"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=toggle_theme),
                    ft.ListTile(leading=ft.Icon(ft.Icons.UPDATE, color="blue"), title=ft.Text("بروزرسانی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.MAP, color="green"), title=ft.Text("شبکه فروش و خدمات"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.GAVEL, color="amber"), title=ft.Text("قوانین"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.INFO, color="blue"), title=ft.Text("درباره ما"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                    ft.Divider(height=25),
                    ft.ListTile(leading=ft.Icon(ft.Icons.SETTINGS, color="grey"), title=ft.Text("تنظیمات"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(5)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.LOGOUT, color="red"), title=ft.Text("خروج", color="red"), on_click=lambda e: (setattr(page.session, 'logged_in', False), render())),
                    ft.Text("نسخه ۱.۴.۳", size=12, color="grey", text_align=ft.TextAlign.CENTER)
                ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=360)
            ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, margin=ft.margin.Margin(left=15, right=15), expand=True
        )
    def create_account_request(e):
        show_message("درخواست ایجاد حساب ارسال شد", "blue")
    # ==================== رندر ====================
    def render(tab_index=0):
        page.controls.clear()

        if not page.session.logged_in:
            page.add(login_page())
        else:
            contents = [dashboard_page(), pre_invoice_page(), home_page(), technical_page(), profile_page(), settings_page()]

            main_content = ft.Container(content=contents[tab_index], expand=True, width=400, margin=ft.margin.Margin(left=15, right=15))

            nav_bar = ft.Container(
                content=ft.Row([
                    ft.Container(content=ft.Image(src="dashboard.png", width=32, height=32), on_click=lambda _: render(0), padding=8),
                    ft.Container(content=ft.Image(src="invoice.png", width=32, height=32), on_click=lambda _: render(1), padding=8),
                    ft.Container(content=ft.Image(src="TopSUNify-1.png", width=32, height=32), on_click=lambda _: render(2), padding=8),
                    ft.Container(content=ft.Image(src="technical.png", width=32, height=32), on_click=lambda _: render(3), padding=8),
                    ft.Container(content=ft.Image(src="profile.png", width=32, height=32), on_click=lambda _: render(4), padding=8),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                bgcolor="white", padding=12,
                border=ft.Border(top=ft.BorderSide(1, "#e0e0e0"), bottom=ft.BorderSide(1, "#e0e0e0"))
            )

            page.add(ft.Column([main_content, nav_bar], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER))

        page.update()

    render()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
