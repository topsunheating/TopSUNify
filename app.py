import flet as ft
import os
import requests

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

    # --- توابع کمکی ---
    def show_message(text: str, color="green"):
        snack = ft.SnackBar(content=ft.Text(text), bgcolor=color, duration=3000)
        page.snack_bar = snack
        snack.open = True
        page.update()

    def toggle_theme(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()
        show_message(f"تم تغییر کرد به: {page.theme_mode}", "blue")

    # --- دیالوگ‌ها ---
    def open_create_account_dialog(e):
        dlg = ft.AlertDialog(
            title=ft.Text("درخواست ایجاد حساب همکار", size=18, weight="bold"),
            content=ft.Container(
                content=ft.Column([
                    ft.TextField(label="نام و نام خانوادگی", text_align=ft.TextAlign.RIGHT),
                    ft.Dropdown(label="نوع درخواست", options=[ft.dropdown.Option("نماینده فروش"), ft.dropdown.Option("نصاب فنی")], width=340),
                ], scroll=ft.ScrollMode.AUTO),
                width=380, height=300
            ),
            actions=[ft.ElevatedButton("ارسال", on_click=lambda e: (setattr(page.dialog, "open", False), page.update(), show_message("ارسال شد")))]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def open_selected_customers_dialog(e):
        dlg = ft.AlertDialog(
            title=ft.Text("مشتریان منتخب"),
            content=ft.Text("لیست مشتریان اینجا نمایش داده می‌شود."),
            actions=[ft.TextButton("بستن", on_click=lambda e: (setattr(page.dialog, "open", False), page.update()))]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def open_inventory_dialog(e):
        dlg = ft.AlertDialog(
            title=ft.Text("اعلام موجودی انبار"),
            content=ft.Text("فرم موجودی در اینجا قرار می‌گیرد."),
            actions=[ft.TextButton("بستن", on_click=lambda e: (setattr(page.dialog, "open", False), page.update()))]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # --- صفحات (همانند ساختار شما) ---
    def dashboard_page():
        return ft.Container(content=ft.Text("داشبورد"), padding=20)

    def pre_invoice_page():
        return ft.Container(content=ft.Text("پیش‌فاکتور"), padding=20)

    def home_page():
        return ft.Container(content=ft.Text("خانه"), padding=20)

    def technical_page():
        return ft.Container(content=ft.Text("اطلاعات فنی"), padding=20)

    def profile_page():
        return ft.Container(
            content=ft.Column([
                ft.ListTile(leading=ft.Icon(ft.Icons.PERSON_ADD), title=ft.Text("درخواست ایجاد حساب"), on_click=open_create_account_dialog),
                ft.ListTile(leading=ft.Icon(ft.Icons.STAR), title=ft.Text("مشتریان منتخب"), on_click=open_selected_customers_dialog),
                ft.ListTile(leading=ft.Icon(ft.Icons.WAREHOUSE), title=ft.Text("اعلام موجودی انبار"), on_click=open_inventory_dialog),
                ft.ListTile(leading=ft.Icon(ft.Icons.PALETTE), title=ft.Text("تغییر تم"), on_click=toggle_theme),
            ])
        )

    def settings_page():
        return ft.Container(content=ft.Text("تنظیمات"), padding=20)

    # --- رندر اصلی ---
    def render(tab_index=0):
        page.controls.clear()
        if not page.session.logged_in:
            page.add(ft.ElevatedButton("ورود", on_click=lambda e: (setattr(page.session, 'logged_in', True), render())))
        else:
            contents = [dashboard_page(), pre_invoice_page(), home_page(), technical_page(), profile_page(), settings_page()]
            page.add(ft.Column([contents[tab_index]]))
        page.update()

    render()

if __name__ == "__main__":
    ft.app(target=main, port=int(os.environ.get("PORT", 8080)), host="0.0.0.0")
