import flet as ft
import os

def main(page: ft.Page):
    page.title = "TopSUNify"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    page.padding = 0

    # متغیرهای سشن
    page.session.logged_in = False
    page.session.active_tab = 0

    # --- تابع بررسی ورود ---
    def login_click(e):
        if username_field.value == "admin" and password_field.value == "1234":
            page.session.logged_in = True
            page.go("/app")
        else:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("نام کاربری یا رمز عبور اشتباه است!")))
        page.update()

    # --- المان‌های فرم ورود ---
    username_field = ft.TextField(label="نام کاربری", icon="person", width=300)
    password_field = ft.TextField(label="رمز عبور", icon="lock", password=True, can_reveal_password=True, width=300)

    # --- ساختار صفحات ---
    def build_login_view():
        return ft.View("/", [
            ft.Container(
                content=ft.Column([
                    ft.Icon("sunny", size=60, color="orange"),
                    ft.Text("ورود به تاپسانیفای", size=24, weight="bold"),
                    username_field,
                    password_field,
                    ft.ElevatedButton("ورود", on_click=login_click, width=300, bgcolor="amber")
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                expand=True
            )
        ])

    def build_app_view():
        # محتوای اصلی (داشبورد)
        return ft.View("/app", [
            ft.AppBar(title=ft.Text("داشبورد"), bgcolor="blue_grey_100"),
            ft.Container(content=ft.Text("خوش آمدید! شما وارد شدید."), alignment=ft.alignment.center, expand=True),
            ft.NavigationBar(
                selected_index=0,
                destinations=[
                    ft.NavigationBarDestination(icon="dashboard", label="داشبورد"),
                    ft.NavigationBarDestination(icon="receipt", label="فاکتور"),
                    ft.NavigationBarDestination(icon="info", label="تاپسان"),
                    ft.NavigationBarDestination(icon="person", label="پروفایل"),
                ]
            )
        ])

    # هندلر تغییر مسیر
    def route_change(route):
        page.views.clear()
        if not page.session.logged_in:
            page.views.append(build_login_view())
        else:
            page.views.append(build_app_view())
        page.update()

    page.on_route_change = route_change
    page.go("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0")
