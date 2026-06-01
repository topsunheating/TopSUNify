import flet as ft
import os
import requests

def main(page: ft.Page):
    # تنظیمات اولیه
    page.fonts = {"iranyekan": "fonts/iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    page.padding = 0
    page.rtl = True
    page.theme_mode = "light"
    page.bgcolor = "#f5f5f5"

    if not hasattr(page.session, "logged_in"):
        page.session.logged_in = False
        page.session.user_role = "عمومی"

    # ==================== توابع عمومی و دیالوگ‌ها ====================
    def show_message(text: str, color="green"):
        snack = ft.SnackBar(content=ft.Text(text), bgcolor=color, duration=3000)
        page.snack_bar = snack
        snack.open = True
        page.update()

    def toggle_theme(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()

    # --- دیالوگ‌های استاندارد ---
    def open_create_account_dialog(e):
        dlg = ft.AlertDialog(title=ft.Text("درخواست ایجاد حساب"), content=ft.Text("فرم مربوطه..."))
        page.dialog = dlg
        dlg.open = True
        page.update()

    def open_selected_customers_dialog(e):
        dlg = ft.AlertDialog(title=ft.Text("مشتریان منتخب"), content=ft.Text("لیست مشتریان..."))
        page.dialog = dlg
        dlg.open = True
        page.update()

    def open_inventory_dialog(e):
        dlg = ft.AlertDialog(title=ft.Text("موجودی انبار"), content=ft.Text("موجودی..."))
        page.dialog = dlg
        dlg.open = True
        page.update()

    # ==================== صفحات ====================
    def dashboard_page():
        return ft.Container(content=ft.Text("داشبورد"), expand=True)

    def pre_invoice_page():
        # استفاده از Alignment ثابت (بدون خطا)
        return ft.Container(content=ft.Text("پیش فاکتور"), alignment=ft.alignment.center)

    def home_page():
        return ft.Container(content=ft.Text("خانه"), expand=True)

    def technical_page():
        return ft.Container(content=ft.Text("اطلاعات فنی"), expand=True)

    def settings_page():
        return ft.Container(content=ft.Text("تنظیمات"), expand=True)

    def profile_page():
        return ft.Container(
            content=ft.Column([
                ft.ListTile(title=ft.Text("درخواست ایجاد حساب"), on_click=open_create_account_dialog),
                ft.ListTile(title=ft.Text("مشتریان منتخب"), on_click=open_selected_customers_dialog),
                ft.ListTile(title=ft.Text("موجودی انبار"), on_click=open_inventory_dialog),
                ft.ListTile(title=ft.Text("تغییر تم"), on_click=toggle_theme),
            ])
        )

    # ==================== رندر اصلی ====================
    def render(tab_index=0):
        page.controls.clear()
        if not page.session.logged_in:
            page.add(ft.ElevatedButton("ورود", on_click=lambda e: (setattr(page.session, 'logged_in', True), render())))
        else:
            views = [dashboard_page(), pre_invoice_page(), home_page(), technical_page(), profile_page(), settings_page()]
            page.add(views[tab_index])
        page.update()

    render()

if __name__ == "__main__":
    ft.app(target=main, port=int(os.environ.get("PORT", 8080)), host="0.0.0.0")
