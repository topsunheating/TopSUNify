import flet as ft
import os

def main(page: ft.Page):
    page.title = "TopSUNify"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    page.padding = 0

    page.session.logged_in = False

    # فیلدها
    username = ft.TextField(label="نام کاربری", width=300)
    password = ft.TextField(label="رمز عبور", password=True, width=300)

    # تابع ورود
    def login(e):
        if username.value == "admin" and password.value == "1234":
            page.session.logged_in = True
            update_ui()
        else:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("اطلاعات اشتباه است!")))
            page.update()

    # تابع تغییر تب‌ها
    def on_nav_change(e):
        page.session.active_tab = e.control.selected_index
        update_ui()

    # تابع اصلی رندر
    def update_ui():
        page.controls.clear()
        
        if not page.session.logged_in:
            page.add(
                ft.Container(
                    ft.Column([
                        ft.Text("ورود به تاپسانیفای", size=25),
                        username, password,
                        ft.ElevatedButton("ورود", on_click=login)
                    ], horizontal_alignment="center"),
                    padding=20
                )
            )
        else:
            # اینجا داشبورد رو با المان‌های ساده می‌سازیم
            page.add(
                ft.AppBar(title=ft.Text("داشبورد مدیریتی")),
                ft.Container(
                    ft.Column([
                        ft.Card(content=ft.Container(ft.Text("آمار فروش: ۲۰٪ رشد"), padding=20)),
                        ft.Card(content=ft.Container(ft.Text("تعداد فاکتورهای جدید: ۵"), padding=20)),
                    ]),
                    padding=20
                ),
                ft.NavigationBar(
                    selected_index=getattr(page.session, "active_tab", 0),
                    on_change=on_nav_change,
                    destinations=[
                        ft.NavigationBarDestination(icon="dashboard", label="داشبورد"),
                        ft.NavigationBarDestination(icon="receipt", label="فاکتور"),
                        ft.NavigationBarDestination(icon="info", label="تاپسان"),
                        ft.NavigationBarDestination(icon="person", label="پروفایل"),
                    ]
                )
            )
        page.update()

    update_ui()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0")
