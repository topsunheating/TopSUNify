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
        page.session.selected_month = 2 # خرداد به عنوان پیش فرض

    def show_message(text: str, color="green"):
        snack = ft.SnackBar(content=ft.Text(text), bgcolor=color, action="بستن", duration=3000)
        page.snack_bar = snack
        snack.open = True
        page.update()

    def toggle_theme(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()

    # ==================== داشبورد مدیریتی جدید ====================
    def dashboard_page():
        months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
        
        def change_month(delta):
            page.session.selected_month = (page.session.selected_month + delta) % 12
            render(0)

        # منوی انتخاب زیرمجموعه
        user_dropdown = ft.Dropdown(
            label="انتخاب مجموعه/زیرمجموعه",
            value="مجموعه اصلی من",
            width=360,
            options=[
                ft.dropdown.Option("مجموعه اصلی من"),
                ft.dropdown.Option("زیرمجموعه ۱"),
                ft.dropdown.Option("زیرمجموعه ۲"),
            ],
            border_radius=15,
            bgcolor="white"
        )

        # نوار ماه و سال
        month_selector = ft.Container(
            content=ft.Row([
                ft.IconButton(ft.Icons.ARROW_FORWARD_IOS, on_click=lambda _: change_month(1)),
                ft.Container(
                    content=ft.Text(months[page.session.selected_month], size=16, weight="bold", color="white"),
                    bgcolor="#007BFF", padding=ft.padding.symmetric(horizontal=30, vertical=10), border_radius=20
                ),
                ft.IconButton(ft.Icons.ARROW_BACK_IOS, on_click=lambda _: change_month(-1)),
            ], alignment=ft.MainAxisAlignment.CENTER),
            margin=ft.margin.only(top=10, bottom=10)
        )

        # دکمه‌های گزارش
        reports = ["پیش فاکتورها", "فاکتورهای فروش", "فاکتورهای تسویه شده", "فاکتورهای باز", "پروژه های نصب شده"]
        buttons = ft.Column([
            ft.ElevatedButton(text=r, width=360, height=50, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15))) 
            for r in reports
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)

        return ft.Container(
            content=ft.Column([user_dropdown, month_selector, buttons], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True
        )

    # سایر صفحات (عینا همان کد شما)
    def pre_invoice_page():
        # ... (کد قبلی شما برای پیش فاکتورها)
        return ft.Container(content=ft.Text("صفحه پیش فاکتورها"), width=400)

    def home_page():
        # ... (کد قبلی شما)
        return ft.Container(content=ft.Text("صفحه اصلی"), width=400)

    def technical_page():
        # ... (کد قبلی شما)
        return ft.Container(content=ft.Text("اطلاعات فنی"), width=400)

    def settings_page():
        # ... (کد قبلی شما)
        return ft.Container(content=ft.Text("تنظیمات"), width=400)

    def profile_page():
        # ... (کد قبلی شما)
        return ft.Container(content=ft.Text("پروفایل"), width=400)

    def create_account_request(e):
        show_message("درخواست ایجاد حساب ارسال شد", "blue")

    # ==================== رندر اصلی ====================
    def render(tab_index=0):
        page.controls.clear()
        if not page.session.logged_in:
            # (صفحه لاگین شما)
            page.add(ft.Container(content=ft.ElevatedButton("ورود", on_click=lambda e: (setattr(page.session, 'logged_in', True), render()))))
        else:
            contents = [dashboard_page(), pre_invoice_page(), home_page(), technical_page(), profile_page(), settings_page()]
            
            nav_bar = ft.Container(
                content=ft.Row([
                    ft.IconButton(ft.Icons.DASHBOARD, on_click=lambda _: render(0)),
                    ft.IconButton(ft.Icons.DESCRIPTION, on_click=lambda _: render(1)),
                    ft.IconButton(ft.Icons.HOME, on_click=lambda _: render(2)),
                    ft.IconButton(ft.Icons.BUILD, on_click=lambda _: render(3)),
                    ft.IconButton(ft.Icons.PERSON, on_click=lambda _: render(4)),
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                bgcolor="white", padding=10
            )

            page.add(ft.Column([
                ft.Container(content=ft.Text("TopSUNify", size=20, weight="bold"), padding=10),
                ft.Divider(),
                ft.Container(content=contents[tab_index], expand=True),
                nav_bar
            ], expand=True))
        page.update()

    render()

if __name__ == "__main__":
    ft.app(target=main, port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", assets_dir="assets")
