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

    # --- توابع اصلی ---
    def show_message(text: str, color="green"):
        snack = ft.SnackBar(content=ft.Text(text), bgcolor=color, action="بستن", duration=3000)
        page.snack_bar = snack
        snack.open = True
        page.update()

    def submit_form(e):
        show_message("درخواست با موفقیت ثبت شد", "green")
        dlg.open = False
        page.update()

    dlg = ft.AlertDialog(
        title=ft.Text("فرم درخواست همکاری", text_align=ft.TextAlign.CENTER),
        content=ft.Container(
            content=ft.Column([
                ft.TextField(label="نام و نام خانوادگی", text_align=ft.TextAlign.RIGHT),
                ft.TextField(label="شماره ملی", text_align=ft.TextAlign.RIGHT),
                ft.ElevatedButton("تایید درخواست", bgcolor="#1565C0", color="white", on_click=submit_form)
            ], tight=True),
            width=300, height=250
        )
    )

    def open_dialog(e):
        page.dialog = dlg
        dlg.open = True
        page.update()

    def create_account_request(e):
        show_message("درخواست ایجاد حساب ارسال شد")

    def toggle_theme(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()

    # --- صفحات برنامه ---
    def pre_invoice_page():
        products = ["گرمایش از کف", "زیرفرشی", "رادیاتور", "حوله خشک کن", "یخ زدایی رمپ", "یخ زدایی پله", "گرمکن مخزن", "گرمکن صندلی", "رستورانی", "عایق بازتابشی"]
        grid = ft.GridView(runs_count=2, max_extent=120, spacing=10, run_spacing=12, padding=10, expand=True)
        for name in products:
            grid.controls.append(
                ft.Container(
                    content=ft.Text(name, size=15, weight="bold", text_align=ft.TextAlign.CENTER, color="#1565C0"),
                    width=170, height=70, bgcolor="#ffffff", border_radius=12, alignment=ft.alignment.center,
                    shadow=ft.BoxShadow(blur_radius=6, color="#e0e0e0"),
                    on_click=lambda e, n=name: show_message(f"پیش‌فاکتور {n}"), ink=True,
                )
            )
        return ft.Container(content=ft.Column([ft.Text("نوع محصول مورد نظر را انتخاب کنید", size=18, weight="bold", text_align=ft.TextAlign.CENTER), ft.Divider(height=10), grid], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10), width=400, margin=ft.margin.symmetric(horizontal=15), expand=True)

    def home_page():
        return ft.Container(content=ft.Column([
            ft.Container(content=ft.Column([ft.Image(src="TopSUNify-1.png", width=80), ft.Text("خوش آمدید به TopSUNify", size=18, weight="bold"), ft.Text("مرکز خدمات و پشتیبانی", size=16, color="grey")], horizontal_alignment=ft.CrossAxisAlignment.CENTER), margin=ft.margin.only(top=20, bottom=30)),
            ft.Container(content=ft.Column([ft.ListTile(leading=ft.Icon(ft.Icons.SHIELD, color="green"), title=ft.Text("ثبت گارانتی")), ft.ListTile(leading=ft.Icon(ft.Icons.INSTALL_DESKTOP, color="blue"), title=ft.Text("درخواست نصب اولیه")), ft.ListTile(leading=ft.Icon(ft.Icons.SUPPORT_AGENT, color="orange"), title=ft.Text("درخواست خدمات فنی")), ft.ListTile(leading=ft.Icon(ft.Icons.SHOPPING_CART_CHECKOUT, color="purple"), title=ft.Text("ثبت درخواست سفارشی و عمده")), ft.ListTile(leading=ft.Icon(ft.Icons.PRINT, color="red"), title=ft.Text("درخواست چاپ طرح سفارشی"))], spacing=2), width=380)
        ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=400, margin=ft.margin.symmetric(horizontal=15), expand=True)

    def technical_page():
        return ft.Container(content=ft.Column([ft.Container(content=ft.Text("اطلاعات فنی", size=18, weight="bold"), padding=20), ft.Container(content=ft.Column([ft.ListTile(leading=ft.Icon(ft.Icons.BOOK, color="blue"), title=ft.Text("کاتالوگ محصولات")), ft.ListTile(leading=ft.Icon(ft.Icons.PRICE_CHANGE, color="green"), title=ft.Text("لیست قیمت")), ft.ListTile(leading=ft.Icon(ft.Icons.WORK_HISTORY, color="purple"), title=ft.Text("رزومه شرکت"))], spacing=2), width=380)], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=400, margin=ft.margin.symmetric(horizontal=15), expand=True)

    def settings_page():
        return ft.Container(content=ft.Column([ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("تنظیمات", size=24, weight="bold")]), padding=15), ft.ListTile(leading=ft.Icon(ft.Icons.DELETE_FOREVER, color="red"), title=ft.Text("خروج از نرم‌افزار", color="red"), on_click=lambda e: (setattr(page.session, 'logged_in', False), render()))], spacing=2), width=400, margin=ft.margin.symmetric(horizontal=15), expand=True)

    def profile_page():
        return ft.Container(content=ft.Column([ft.Container(content=ft.Column([ft.CircleAvatar(foreground_image_src="https://i.pravatar.cc/150?u=reza", radius=48), ft.Text("کاربر گرامی", size=20, weight="bold")], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=20), ft.ListTile(leading=ft.Icon(ft.Icons.PERSON_ADD, color="blue"), title=ft.Text("درخواست ایجاد حساب"), on_click=create_account_request), ft.ListTile(leading=ft.Icon(ft.Icons.PALETTE, color="purple"), title=ft.Text("تغییر تم"), on_click=toggle_theme), ft.ListTile(leading=ft.Icon(ft.Icons.SETTINGS, color="grey"), title=ft.Text("تنظیمات"), on_click=lambda e: render(5)), ft.ListTile(leading=ft.Icon(ft.Icons.LOGOUT, color="red"), title=ft.Text("خروج"), on_click=lambda e: (setattr(page.session, 'logged_in', False), render()))], horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=400, expand=True)

    def dashboard_page():
        return ft.Container(content=ft.Column([ft.Text("داشبورد مدیریتی", size=18, weight="bold"), ft.ElevatedButton("مشاهده گزارش‌ها", on_click=lambda e: show_message("در حال بارگذاری..."))], horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=400, expand=True)

    def render(tab_index=0):
        page.controls.clear()
        if not page.session.logged_in:
            page.add(ft.Container(content=ft.Column([ft.Image(src="TopSUNify.png", width=190), ft.TextField(label="نام کاربری", width=340), ft.TextField(label="رمز عبور", password=True, width=340), ft.ElevatedButton("ورود به TopSUNify", width=340, on_click=lambda e: (setattr(page.session, 'logged_in', True), render()))], horizontal_alignment=ft.CrossAxisAlignment.CENTER), alignment=ft.alignment.center, expand=True))
        else:
            contents = [dashboard_page(), pre_invoice_page(), home_page(), technical_page(), profile_page(), settings_page()]
            page.add(ft.Column([ft.Container(content=ft.Image(src="TopSUNify.png", width=80), margin=10), ft.Divider(), ft.Container(content=contents[tab_index], expand=True), ft.Row([ft.IconButton(ft.Icons.DASHBOARD, on_click=lambda _: render(0)), ft.IconButton(ft.Icons.RECEIPT, on_click=lambda _: render(1)), ft.IconButton(ft.Icons.HOME, on_click=lambda _: render(2)), ft.IconButton(ft.Icons.BUILD, on_click=lambda _: render(3)), ft.IconButton(ft.Icons.PERSON, on_click=lambda _: render(4))], alignment=ft.MainAxisAlignment.CENTER)], expand=True))
        page.update()

    render()

if __name__ == "__main__":
    ft.app(target=main, port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", assets_dir="assets")
