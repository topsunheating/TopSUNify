import flet as ft
import os

def main(page: ft.Page):
    # تنظیمات صفحه
    page.title = "TopSUNify"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    page.padding = 0
    # در محیط وب، ابعاد ثابت ویندوز ممکن است باعث رفتار غیرمنتظره شود
    # بهتر است اجازه دهیم مرورگر مدیریت کند، اما مقادیر پیش‌فرض را حفظ می‌کنیم

    # وضعیت سشن
    page.session.logged_in = False
    page.session.active_tab = 0

    # --- تابع رندر صفحه لاگین ---
    def build_login():
        def login_click(e):
            page.session.logged_in = True
            page.go("/app")
            page.update()

        return ft.View("/", [
            ft.Stack([
                ft.Container(
                    content=ft.Image(src="assets/landscape.jpg", fit=ft.ImageFit.COVER),
                    height=250, bottom=0
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Image(src="assets/TopSUNify.png", width=200),
                        ft.TextField(label="نام کاربری", prefix_icon=ft.icons.PERSON),
                        ft.TextField(label="رمز ورود", password=True, can_reveal_password=True, prefix_icon=ft.icons.LOCK),
                        ft.ElevatedButton(
                            "ورود به TopSUNify", 
                            bgcolor="#FFD60A", 
                            color="#1e293b", 
                            height=50, 
                            width=300,
                            on_click=login_click
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=30, top=50
                )
            ])
        ])

    # --- تابع رندر صفحه اصلی ---
    def build_app_page():
        def nav_change(e):
            page.session.active_tab = e.control.selected_index
            page.update()

        return ft.View("/app", [
            ft.AppBar(title=ft.Text("سامانه تاپسانیفای"), center_title=True, bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Container(
                content=ft.Text(f"محتوای تب شماره {page.session.active_tab}"), 
                alignment=ft.alignment.center, 
                expand=True
            ),
            ft.NavigationBar(
                selected_index=page.session.active_tab,
                on_change=nav_change,
                destinations=[
                    ft.NavigationBarDestination(icon=ft.icons.DASHBOARD, label="داشبورد"),
                    ft.NavigationBarDestination(icon=ft.icons.RECEIPT, label="فاکتور"),
                    ft.NavigationBarDestination(icon=ft.icons.INFO, label="تاپسان"),
                    ft.NavigationBarDestination(icon=ft.icons.PERSON, label="پروفایل"),
                ]
            )
        ])

    # هندل کردن تغییر مسیرها
    def route_change(route):
        page.views.clear()
        if not page.session.logged_in:
            page.views.append(build_login())
        else:
            page.views.append(build_app_page())
        page.update()

    page.on_route_change = route_change
    page.go(page.route if page.route != "/" else "/")

# اجرای برنامه
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
