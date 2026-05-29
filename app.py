import flet as ft
import os

def main(page: ft.Page):
    # تنظیمات اولیه برای ظاهر اپلیکیشن
    page.title = "TopSUNify"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    page.padding = 0
    # در محیط وب، ابعاد ویندوز را به صورت درصد یا خودکار تنظیم می‌کنیم
    page.window_width = 400
    page.window_height = 800

    # متغیرهای وضعیت برنامه
    page.session.logged_in = False

    # --- تابع رندر صفحه لاگین ---
    def build_login_page():
        logo = ft.Image(src="TopSUNify.png", width=220)
        username = ft.TextField(label="نام کاربری", border=ft.InputBorder.UNDERLINE, prefix_icon=ft.icons.PERSON)
        password = ft.TextField(label="رمز ورود", password=True, can_reveal_password=True, border=ft.InputBorder.UNDERLINE, prefix_icon=ft.icons.LOCK)
        
        def do_login(e):
            if username.value == "admin" and password.value == "1234":
                page.session.logged_in = True
                page.go("/app")
            else:
                page.show_snack_bar(ft.SnackBar(ft.Text("نام کاربری یا رمز اشتباه است!")))

        return ft.View("/", [
            ft.Stack([
                # بک‌گراند منظره
                ft.Container(
                    content=ft.Image(src="landscape.jpg", fit=ft.ImageFit.COVER),
                    height=250, bottom=0, width=400
                ),
                # کارت اصلی ورود
                ft.Container(
                    content=ft.Column([
                        logo,
                        username,
                        password,
                        ft.ElevatedButton("ورود به TopSUNify", on_click=do_login, 
                                          style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                                          height=50, bgcolor="#FFD60A", color="#1e293b")
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    padding=30, top=100
                )
            ])
        ])

    # --- تابع رندر داشبورد اصلی ---
    def build_app_page():
        return ft.View("/app", [
            ft.AppBar(title=ft.Text("داشبورد تاپسانیفای")),
            ft.Container(content=ft.Text("محتوای اصلی برنامه"), expand=True),
            ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(icon=ft.icons.DASHBOARD, label="داشبورد"),
                    ft.NavigationBarDestination(icon=ft.icons.RECEIPT, label="فاکتور"),
                    ft.NavigationBarDestination(icon=ft.icons.INFO, label="تاپسانیفای"),
                    ft.NavigationBarDestination(icon=ft.icons.PERSON, label="پروفایل"),
                ]
            )
        ])

    # مدیریت مسیرها
    def route_change(route):
        page.views.clear()
        if page.session.logged_in:
            page.views.append(build_app_page())
        else:
            page.views.append(build_login_page())
        page.update()

    page.on_route_change = route_change
    page.go("/")

# --- اجرای برنامه با تنظیمات اختصاصی سرور Railway ---
if __name__ == "__main__":
    # خواندن پورت از متغیر محیطی Railway، در صورت عدم وجود، استفاده از پورت 8080
    port = int(os.environ.get("PORT", 8080))
    
    # اجرای اپلیکیشن در حالت وب با هاست آزاد برای دسترسی سرور
    ft.app(
        target=main,
        port=port,
        view=ft.AppView.WEB_BROWSER,
        host="0.0.0.0"
    )
