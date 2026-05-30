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
    page.bgcolor = "#f5f5f5"
    
    if not hasattr(page.session, "logged_in"):
        page.session.logged_in = False
        page.session.user_role = "عمومی"

    def show_message(text: str, color="green"):
        snack = ft.SnackBar(content=ft.Text(text), bgcolor=color, action="بستن", duration=3000)
        page.snack_bar = snack
        snack.open = True
        page.update()

    # ==================== صفحه پروفایل (وسط چین + محدود) ====================
    def profile_page():
        header = ft.Container(
            content=ft.Column([
                ft.CircleAvatar(foreground_image_src="https://i.pravatar.cc/150?u=reza", radius=48),
                ft.Text("نام و نام خانوادگی | نام کاربری", size=20, weight="bold", text_align="center"),
                ft.Text("شماره موبایل", size=16, color="grey", text_align="center"),
                ft.Container(
                    content=ft.Text(f"سطح دسترسی: {page.session.user_role}", size=15, color="blue", text_align="center"),
                    bgcolor="#f0f0f0", padding=12, border_radius=12, margin=ft.margin.Margin(top=12, bottom=8)
                )
            ], horizontal_alignment="center"),
            padding=20, bgcolor="#f8f9fa", border_radius=20, margin=ft.margin.only(bottom=20)
        )

        menu_items = [
            ft.ListTile(leading=ft.Icon(ft.Icons.PERSON_ADD, color="blue"), title=ft.Text("درخواست ایجاد حساب"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=create_account_request),
            ft.ListTile(leading=ft.Icon(ft.Icons.STAR, color="orange"), title=ft.Text("مشتریان منتخب"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
            ft.ListTile(leading=ft.Icon(ft.Icons.WAREHOUSE, color="green"), title=ft.Text("اعلام موجودی انبار"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
            ft.ListTile(leading=ft.Icon(ft.Icons.SHOPPING_CART), title=ft.Text("ثبت درخواست خرید"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
            ft.ListTile(leading=ft.Icon(ft.Icons.GROUP), title=ft.Text("همکاران منتخب"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
            ft.ListTile(leading=ft.Icon(ft.Icons.PERCENT), title=ft.Text("محاسبه درصد همکاری"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
            ft.ListTile(leading=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET), title=ft.Text("مبلغ اعتبار"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
        ]

        common_items = [
            ft.ListTile(leading=ft.Icon(ft.Icons.PALETTE), title=ft.Text("نمایش (تم روشن/تیره)"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
            ft.ListTile(leading=ft.Icon(ft.Icons.UPDATE), title=ft.Text("بروزرسانی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
            ft.ListTile(leading=ft.Icon(ft.Icons.MAP), title=ft.Text("شبکه فروش و خدمات"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
            ft.ListTile(leading=ft.Icon(ft.Icons.GAVEL), title=ft.Text("قوانین"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
            ft.ListTile(leading=ft.Icon(ft.Icons.INFO), title=ft.Text("درباره ما"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
        ]

        return ft.Container(
            content=ft.Column([
                header,
                *menu_items,
                ft.Divider(height=20),
                *common_items,
                ft.Divider(height=20),
                ft.ListTile(leading=ft.Icon(ft.Icons.SETTINGS), title=ft.Text("تنظیمات"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=open_settings),
                ft.ListTile(leading=ft.Icon(ft.Icons.LOGOUT, color="red"), title=ft.Text("خروج", color="red"), on_click=lambda e: (setattr(page.session, 'logged_in', False), render())),
                ft.Text("نسخه ۱.۴.۳", size=12, color="grey", text_align="center")
            ], scroll=ft.ScrollMode.AUTO, spacing=2, horizontal_alignment="center"),
            width=420,          # عرض محدود (مناسب موبایل و وسط‌چین در لپ‌تاپ)
            margin=ft.margin.symmetric(horizontal=10),
            padding=10
        )

    # ==================== درخواست ایجاد حساب ====================
    def create_account_request(e):
        dlg = ft.AlertDialog(
            title=ft.Text("درخواست ایجاد حساب جدید"),
            content=ft.Column([ ... ]),  # همان کد قبلی
            actions=[ ... ]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # ==================== تنظیمات ====================
    def open_settings(e):
        dlg = ft.AlertDialog(title=ft.Text("تنظیمات"), content=ft.Column([ ... ]))
        page.dialog = dlg
        dlg.open = True
        page.update()

    # ==================== رندر اصلی (وسط چین + محدود) ====================
    def render(tab_index=0):
        page.controls.clear()

        if not page.session.logged_in:
            # صفحه لاگین (وسط چین)
            login_content = ft.Container(
                content=ft.Column([ ... ], horizontal_alignment="center", scroll=ft.ScrollMode.AUTO),  # لاگین قبلی شما
                width=420,
                margin=ft.margin.symmetric(horizontal=10)
            )
            page.add(ft.Container(content=login_content, expand=True, alignment=ft.Alignment(0, 0)))
        else:
            contents = [
                ft.Text("داشبورد مدیریتی", size=25),
                ft.Text("بخش پیش‌فاکتورها", size=25),
                ft.Column([ft.Image(src="TopSUNify-1.png", width=200), ft.Text("خانه اصلی", size=25)], horizontal_alignment="center"),
                ft.Text("اطلاعات فنی سیستم", size=25),
                profile_page()   # پروفایل محدود و وسط‌چین
            ]

            nav_buttons = ft.Row([ ... ])  # ناوبری قبلی

            main_content = ft.Container(
                content=contents[tab_index],
                width=420,                    # عرض محدود
                margin=ft.margin.symmetric(horizontal=10),
                alignment=ft.Alignment(0, 0)
            )

            page.add(
                ft.Column([
                    ft.Text("پنل TopSUNify", size=30, weight="bold"),
                    ft.Divider(),
                    main_content,
                    nav_buttons
                ], horizontal_alignment="center", expand=True)
            )

        page.update()

    render()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
