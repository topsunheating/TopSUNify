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
        page.session.user_role = "general"  # مدیر، مدیرفروش، مدیرفنی، نماینده، کارشناس، عمومی

    # ==================== صفحه پروفایل پیشرفته ====================
    def profile_page():
        role = page.session.user_role
        
        # هدر پروفایل
        header = ft.Container(
            content=ft.Column([
                ft.CircleAvatar(foreground_image_src="https://i.pravatar.cc/150?u=reza", radius=48),
                ft.Text("نام و نام خانوادگی | نام کاربری", size=20, weight="bold", text_align="center"),
                ft.Text("شماره موبایل", size=16, color="grey", text_align="center"),
                ft.Container(
                    content=ft.Text(f"سطح دسترسی: {role}", size=15, color="blue", text_align="center"),
                    bgcolor="#f0f0f0",
                    padding=12,
                    border_radius=12,
                    margin=ft.margin.Margin(top=12, bottom=8)
                )
            ], horizontal_alignment="center"),
            padding=20,
            bgcolor="#f8f9fa",
            border_radius=20,
            margin=ft.margin.Margin(bottom=20)
        )

        # لیست منوها
        menu_items = [
            ft.ListTile(leading=ft.Icon(ft.Icons.PERSON_ADD, color="blue"), 
                       title=ft.Text("درخواست ایجاد حساب"), 
                       trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20),
                       on_click=lambda e: create_account_request()),

            ft.ListTile(leading=ft.Icon(ft.Icons.STAR, color="orange"), 
                       title=ft.Text("مشتریان منتخب"), 
                       trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),

            ft.ListTile(leading=ft.Icon(ft.Icons.WAREHOUSE, color="green"), 
                       title=ft.Text("اعلام موجودی انبار"), 
                       trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),

            ft.ListTile(leading=ft.Icon(ft.Icons.SHOPPING_CART), 
                       title=ft.Text("ثبت درخواست خرید"), 
                       trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),

            ft.ListTile(leading=ft.Icon(ft.Icons.GROUP), 
                       title=ft.Text("همکاران منتخب"), 
                       trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),

            ft.ListTile(leading=ft.Icon(ft.Icons.PERCENT), 
                       title=ft.Text("محاسبه درصد همکاری"), 
                       trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),

            ft.ListTile(leading=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET), 
                       title=ft.Text("مبلغ اعتبار"), 
                       trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
        ]

        # منوهای مشترک
        common_items = [
            ft.ListTile(leading=ft.Icon(ft.Icons.PALETTE), title=ft.Text("نمایش (تم روشن/تیره)"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
            ft.ListTile(leading=ft.Icon(ft.Icons.UPDATE), title=ft.Text("بروزرسانی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
            ft.ListTile(leading=ft.Icon(ft.Icons.MAP), title=ft.Text("شبکه فروش و خدمات"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
            ft.ListTile(leading=ft.Icon(ft.Icons.GAVEL), title=ft.Text("قوانین"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
            ft.ListTile(leading=ft.Icon(ft.Icons.INFO), title=ft.Text("درباره ما"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
        ]

        return ft.Column([
            header,
            *menu_items,
            ft.Divider(height=20),
            *common_items,
            ft.Divider(height=20),
            ft.ListTile(leading=ft.Icon(ft.Icons.SETTINGS), title=ft.Text("تنظیمات"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=open_settings),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.LOGOUT, color="red"),
                title=ft.Text("خروج", color="red"),
                on_click=lambda e: (setattr(page.session, 'logged_in', False), render())
            ),
            ft.Text("نسخه ۱.۴.۳", size=12, color="grey", text_align="center")
        ], scroll=ft.ScrollMode.AUTO, spacing=2)

    # ==================== درخواست ایجاد حساب ====================
    def create_account_request(e=None):
        # فرم درخواست ایجاد حساب
        dlg = ft.AlertDialog(
            title=ft.Text("درخواست ایجاد حساب جدید"),
            content=ft.Column([
                ft.TextField(label="نام و نام خانوادگی / نام شرکت", width=340),
                ft.TextField(label="شماره موبایل", width=340, keyboard_type=ft.KeyboardType.NUMBER),
                ft.TextField(label="نام کاربری", width=340),
                ft.Dropdown(
                    label="سطح دسترسی",
                    options=[
                        ft.dropdown.Option("نمایندگی"),
                        ft.dropdown.Option("عامل فروش"),
                        ft.dropdown.Option("کارشناس فروش"),
                        ft.dropdown.Option("کارشناس فنی"),
                    ],
                    width=340
                ),
                ft.TextField(label="توضیحات / دلیل درخواست", width=340, multiline=True, min_lines=2),
            ], scroll=ft.ScrollMode.AUTO, height=420, spacing=15),
            actions=[
                ft.TextButton("انصراف", on_click=lambda _: (setattr(dlg, 'open', False), page.update())),
                ft.ElevatedButton("ارسال درخواست به مدیر", bgcolor="#FFCC00", color="black", on_click=lambda _: (page.show_snack_bar(ft.SnackBar(ft.Text("درخواست ارسال شد"), open=True)), setattr(dlg, 'open', False), page.update()))
            ]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # ==================== تنظیمات ====================
    def open_settings(e):
        dlg = ft.AlertDialog(
            title=ft.Text("تنظیمات"),
            content=ft.Column([
                ft.ListTile(title=ft.Text("تغییر نام کاربری"), leading=ft.Icon(ft.Icons.PERSON)),
                ft.ListTile(title=ft.Text("ذخیره نام کاربری"), leading=ft.Icon(ft.Icons.SAVE)),
                ft.ListTile(title=ft.Text("ورود با اثر انگشت"), leading=ft.Icon(ft.Icons.FINGERPRINT), trailing=ft.Switch(value=True)),
                ft.ListTile(title=ft.Text("تغییر رمز ورود"), leading=ft.Icon(ft.Icons.LOCK)),
                ft.ListTile(title=ft.Text("تغییر شماره تلفن همراه"), leading=ft.Icon(ft.Icons.PHONE)),
                ft.ListTile(title=ft.Text("دستگاه‌های فعال"), leading=ft.Icon(ft.Icons.DEVICES)),
                ft.ListTile(title=ft.Text("حذف تنظیمات و خروج"), leading=ft.Icon(ft.Icons.DELETE, color="red")),
            ], scroll=ft.ScrollMode.AUTO, height=400),
            actions=[ft.TextButton("بستن", on_click=lambda _: (setattr(dlg, 'open', False), page.update()))]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # ==================== رندر اصلی ====================
    def render(tab_index=0):
        page.controls.clear()

        if not page.session.logged_in:
            # صفحه لاگین (بدون تغییر)
            page.add(
                ft.Column([
                    ft.Container(content=ft.Image(src="TopSUNify.png", width=190), margin=ft.margin.Margin(top=40, bottom=40)),

                    ft.Container(content=ft.TextField(label="نام کاربری", width=340, border_radius=12, prefix_icon=ft.Icons.PERSON, text_align=ft.TextAlign.RIGHT), margin=ft.margin.Margin(bottom=20)),

                    ft.Container(
                        content=ft.Row([
                            ft.Container(content=ft.Icon(ft.Icons.FINGERPRINT, size=42, color="#FFCC00"), on_click=show_biometric_dialog, padding=10, border_radius=12, ink=True),
                            ft.TextField(label="رمز عبور", password=True, width=270, border_radius=12, prefix_icon=ft.Icons.LOCK, text_align=ft.TextAlign.RIGHT)
                        ], alignment="center", spacing=12),
                        margin=ft.margin.Margin(bottom=30)
                    ),

                    ft.ElevatedButton("ورود به TopSUNify", width=340, bgcolor="#FFCC00", color="black", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)), on_click=lambda e: (setattr(page.session, 'logged_in', True), render())),
                    ft.TextButton("فعال‌سازی / فراموشی رمز", style=ft.ButtonStyle(color={"": "blue"}), on_click=show_register_dialog),

                    ft.Container(content=ft.Image(src="TopSUN-Powered.png", width=160), margin=ft.margin.Margin(top=50, bottom=30)),
                    ft.Container(expand=True, content=ft.Image(src="landscape.jpg", width=400, height=220, fit="cover"))
                ], horizontal_alignment="center", expand=True, scroll=ft.ScrollMode.AUTO)
            )
        else:
            contents = [
                ft.Text("داشبورد مدیریتی", size=25),
                ft.Text("بخش پیش‌فاکتورها", size=25),
                ft.Column([ft.Image(src="TopSUNify-1.png", width=200), ft.Text("خانه اصلی", size=25)], horizontal_alignment="center"),
                ft.Text("اطلاعات فنی سیستم", size=25),
                profile_page()
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
                    ft.Container(content=contents[tab_index], expand=True, alignment=ft.Alignment(0, 0)),
                    nav_buttons
                ], horizontal_alignment="center", expand=True)
            )

        page.update()

    # توابع کمکی (برای جلوگیری از خطا)
    def show_biometric_dialog(e):
        page.show_snack_bar(ft.SnackBar(ft.Text("احراز هویت بیومتریک فعال شد"), open=True))
        page.session.logged_in = True
        render()

    def show_register_dialog(e):
        page.show_snack_bar(ft.SnackBar(ft.Text("بخش ثبت‌نام / فراموشی رمز"), open=True))

    render()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
