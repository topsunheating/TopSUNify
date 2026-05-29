import flet as ft
import os

def main(page: ft.Page):
    page.title = "TopSUNify"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    page.padding = 0

    # متغیرهای سشن
    page.session.logged_in = False

    # فیلدها را اینجا تعریف می‌کنیم تا در همه جا در دسترس باشند
    username_field = ft.TextField(label="نام کاربری", icon="person", width=300)
    password_field = ft.TextField(label="رمز عبور", icon="lock", password=True, can_reveal_password=True, width=300)

    # تابعی برای لاگین
    def login_click(e):
        if username_field.value == "admin" and password_field.value == "1234":
            page.session.logged_in = True
            page.go("/app")
        else:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("خطا: نام کاربری یا رمز اشتباه است!")))
            page.update()

    # تابع تغییر مسیرها (اصلی‌ترین بخش برای جلوگیری از صفحه سفید)
    def route_change(route):
        page.views.clear()
        
        # صفحه ورود
        if page.route == "/":
            page.views.append(
                ft.View("/", [
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
            )
        
        # صفحه اصلی
        elif page.route == "/app":
            if not page.session.logged_in:
                page.go("/")
                return
            
            page.views.append(
                ft.View("/app", [
                    ft.AppBar(title=ft.Text("داشبورد"), bgcolor="blue_grey_100"),
                    ft.Container(content=ft.Text("شما با موفقیت وارد شدید!"), alignment=ft.alignment.center, expand=True),
                    ft.NavigationBar(
                        destinations=[
                            ft.NavigationBarDestination(icon="dashboard", label="داشبورد"),
                            ft.NavigationBarDestination(icon="receipt", label="فاکتور"),
                            ft.NavigationBarDestination(icon="info", label="تاپسان"),
                            ft.NavigationBarDestination(icon="person", label="پروفایل"),
                        ]
                    )
                ])
            )
        page.update()

    page.on_route_change = route_change
    page.go(page.route) # شروع از مسیر فعلی

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0")
