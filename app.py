import flet as ft
import os

GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbygH2yHhw44Lk5Hv8okJDnRBgGw2UzoF1wsZvMGGGr7ZzhSS0Ro6WhSeVFTPM2TpsMv/exec"

def main(page: ft.Page):
    page.fonts = {"iranyekan": "fonts/iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    page.padding = 0
    page.rtl = True
    page.theme_mode = "light"
    page.bgcolor = "#f5f5f5"

    # متغیرهای وضعیت برای داشبورد
    if not hasattr(page.session, "logged_in"):
        page.session.logged_in = False
        page.session.user_role = "مدیر ارشد"  # برای تست سطح دسترسی
        page.session.user_name = "مهندس رضایی"
        page.session.selected_month = 3  # خرداد
        page.session.selected_year = 1403

    def show_message(text: str, color="green"):
        snack = ft.SnackBar(content=ft.Text(text), bgcolor=color, action="بستن", duration=3000)
        page.snack_bar = snack
        snack.open = True
        page.update()

    def toggle_theme(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()
        show_message(f"تم تغییر کرد به: {page.theme_mode}", "blue")

    # ==================== صفحه داشبورد مدیریتی (جدید) ====================
    def dashboard_page():
        # لیست ماه‌های شمسی
        months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
        
        def change_date(delta):
            page.session.selected_month += delta
            if page.session.selected_month > 12:
                page.session.selected_month = 1
                page.session.selected_year += 1
            elif page.session.selected_month < 1:
                page.session.selected_month = 12
                page.session.selected_year -= 1
            render(0) # رندر مجدد داشبورد

        # بخش ۱: نام کاربر و منوی زیرمجموعه
        user_menu = ft.PopupMenuButton(
            content=ft.Row([
                ft.Text(page.session.user_name, size=18, weight="bold", color="#1565C0"),
                ft.Icon(ft.Icons.ARROW_DROP_DOWN, color="#1565C0")
            ], alignment=ft.MainAxisAlignment.CENTER),
            items=[
                ft.PopupMenuItem(text="اطلاعات شخصی (خودم)", on_click=lambda _: show_message("نمایش اطلاعات خودتان")),
                ft.PopupMenuItem(text="زیرمجموعه ۱: دفتر تهران", on_click=lambda _: show_message("سوئیچ به دفتر تهران")),
                ft.PopupMenuItem(text="زیرمجموعه ۲: نمایندگی شمال", on_click=lambda _: show_message("سوئیچ به نمایندگی شمال")),
            ]
        )

        # بخش ۲: نوار انتخاب تاریخ (ماه و سال)
        date_picker = ft.Container(
            content=ft.Row([
                ft.IconButton(icon=ft.Icons.ARROW_RIGHT, on_click=lambda _: change_date(-1)),
                ft.Text(f"{months[page.session.selected_month-1]} {page.session.selected_year}", size=16, weight="500"),
                ft.IconButton(icon=ft.Icons.ARROW_LEFT, on_click=lambda _: change_date(1)),
            ], alignment=ft.MainAxisAlignment.CENTER),
            bgcolor="#ffffff",
            border_radius=15,
            padding=5,
            shadow=ft.BoxShadow(blur_radius=4, color="#eeeeee")
        )

        # بخش ۳: دکمه‌های عملیاتی داشبورد (شبیه تب پیش‌فاکتور)
        dash_items = [
            ("پیش‌فاکتورها", ft.Icons.DESCRIPTION_OUTLINED, "#1E88E5"),
            ("فاکتورهای فروش", ft.Icons.RECEIPT_LONG, "#43A047"),
            ("فاکتورهای تسویه شده", ft.Icons.CHECK_CIRCLE, "#2E7D32"),
            ("فاکتورهای باز", ft.Icons.PENDING_ACTIONS, "#FB8C00"),
            ("پروژه‌های نصب شده", ft.Icons.HANDYMAN, "#5E35B1"),
        ]

        grid = ft.Column(spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        for title, icon, color in dash_items:
            grid.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(icon, color=color, size=24),
                        ft.Text(title, size=16, weight="bold", color="#444444"),
                    ], alignment=ft.MainAxisAlignment.START, spacing=20),
                    width=340,
                    height=65,
                    bgcolor="white",
                    border_radius=15,
                    padding=ft.padding.only(left=20, right=20),
                    shadow=ft.BoxShadow(blur_radius=5, color="#dddddd"),
                    on_click=lambda e, t=title: show_message(f"در حال بارگذاری {t}..."),
                    ink=True
                )
            )

        return ft.Container(
            content=ft.Column([
                user_menu,
                ft.Text("دسترسی به گزارشات مدیریتی", size=14, color="grey"),
                date_picker,
                ft.Divider(height=20, color="transparent"),
                grid
            ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
            expand=True
        )

    # ==================== صفحه پیش‌فاکتورها (محصولات) ====================
    def pre_invoice_page():
        products = ["گرمایش از کف", "زیرفرشی", "رادیاتور", "حوله خشک کن", "یخ زدایی رمپ", "یخ زدایی پله", "گرمکن مخزن", "گرمکن صندلی", "رستورانی", "عایق بازتابشی"]
        grid = ft.GridView(runs_count=3, max_extent=160, spacing=12, run_spacing=12, padding=15, expand=True)

        for name in products:
            grid.controls.append(
                ft.Container(
                    content=ft.Text(name, size=14, weight="bold", text_align=ft.TextAlign.CENTER, color="#1565C0"),
                    width=170, height=70, bgcolor="#ffffff", border_radius=12, alignment=ft.Alignment(0, 0),
                    shadow=ft.BoxShadow(blur_radius=6, color="#e0e0e0"),
                    on_click=lambda e, n=name: show_message(f"پیش‌فاکتور {n}"), ink=True,
                )
            )
        return ft.Container(
            content=ft.Column([
                ft.Text("نوع محصول مورد نظر را انتخاب کنید", size=18, weight="bold", text_align=ft.TextAlign.CENTER),
                ft.Divider(height=10),
                grid
            ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True
        )

    # ==================== بقیه صفحات عینا تکرار می‌شود ====================
    def home_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Column([
                    ft.Image(src="TopSUNify-1.png", width=80),
                    ft.Text("خوش آمدید به TopSUNify", size=18, weight="bold"),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER), margin=ft.margin.Margin(top=20, bottom=30)),
                ft.Column([
                    ft.ListTile(leading=ft.Icon(ft.Icons.SHIELD, color="green"), title=ft.Text("ثبت گارانتی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.INSTALL_DESKTOP, color="blue"), title=ft.Text("درخواست نصب اولیه"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.SUPPORT_AGENT, color="orange"), title=ft.Text("درخواست خدمات فنی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                ], spacing=2)
            ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER), expand=True
        )

    def technical_page():
        return ft.Container(
            content=ft.Column([
                ft.Text("اطلاعات فنی", size=18, weight="bold", padding=20),
                ft.Column([
                    ft.ListTile(leading=ft.Icon(ft.Icons.BOOK, color="blue"), title=ft.Text("کاتالوگ محصولات")),
                    ft.ListTile(leading=ft.Icon(ft.Icons.PRICE_CHANGE, color="green"), title=ft.Text("لیست قیمت")),
                ])
            ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER), expand=True
        )

    def settings_page():
        return ft.Container(
            content=ft.Column([
                ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("تنظیمات", size=24, weight="bold")]),
                ft.ListTile(leading=ft.Icon(ft.Icons.LOCK), title=ft.Text("تغییر رمز ورود")),
                ft.ListTile(leading=ft.Icon(ft.Icons.LOGOUT, color="red"), title=ft.Text("خروج", color="red"), on_click=lambda e: logout()),
            ], scroll=ft.ScrollMode.AUTO), expand=True
        )

    def profile_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Column([
                    ft.CircleAvatar(foreground_image_src="https://i.pravatar.cc/150?u=reza", radius=48),
                    ft.Text(page.session.user_name, size=20, weight="bold"),
                    ft.Text(f"سطح دسترسی: {page.session.user_role}", color="blue"),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=20, bgcolor="#f8f9fa", border_radius=20),
                ft.Column([
                    ft.ListTile(leading=ft.Icon(ft.Icons.SETTINGS), title=ft.Text("تنظیمات"), on_click=lambda e: render(5)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.PALETTE), title=ft.Text("تم"), on_click=toggle_theme),
                ])
            ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER), expand=True
        )

    def logout():
        page.session.logged_in = False
        render()

    # ==================== رندر اصلی ====================
    def render(tab_index=0):
        page.controls.clear()
        if not page.session.logged_in:
            # صفحه لاگین ساده شده
            page.add(ft.Container(content=ft.Column([
                ft.Image(src="TopSUNify.png", width=150),
                ft.TextField(label="نام کاربری", width=300),
                ft.ElevatedButton("ورود", on_click=lambda e: (setattr(page.session, 'logged_in', True), render(0)), width=300, bgcolor="#FFCC00")
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER), expand=True))
        else:
            contents = [
                dashboard_page(),  # تب 0
                pre_invoice_page(),# تب 1
                home_page(),       # تب 2
                technical_page(),   # تب 3
                profile_page(),     # تب 4
                settings_page()     # تب 5
            ]
            
            nav_bar = ft.Container(
                content=ft.Row([
                    ft.IconButton(icon=ft.Icons.DASHBOARD, on_click=lambda _: render(0), icon_color="blue" if tab_index==0 else "grey"),
                    ft.IconButton(icon=ft.Icons.INVOICE, on_click=lambda _: render(1), icon_color="blue" if tab_index==1 else "grey"),
                    ft.IconButton(icon=ft.Icons.HOME, on_click=lambda _: render(2), icon_color="blue" if tab_index==2 else "grey"),
                    ft.IconButton(icon=ft.Icons.BUILD, on_click=lambda _: render(3), icon_color="blue" if tab_index==3 else "grey"),
                    ft.IconButton(icon=ft.Icons.PERSON, on_click=lambda _: render(4), icon_color="blue" if tab_index==4 else "grey"),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                bgcolor="white", padding=10
            )

            page.add(ft.Column([
                ft.Container(content=ft.Image(src="TopSUNify.png", width=80), alignment=ft.alignment.center, padding=10),
                ft.Divider(height=1),
                ft.Container(content=contents[tab_index], expand=True, padding=10),
                nav_bar
            ], expand=True))
        page.update()

    render()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
