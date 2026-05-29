import flet as ft
import os

def main(page: ft.Page):
    # تنظیمات صفحه
    page.title = "TopSUNify"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    page.padding = 0
    page.window_width = 400
    page.window_height = 800

    # وضعیت سشن (لاگین و تب فعال)
    page.session.logged_in = False
    page.session.active_tab = "invoice"

    # --- تابع رندر صفحه لاگین ---
    def build_login():
        return ft.View("/", [
            ft.Stack([
                ft.Container(content=ft.Image(src="assets/landscape.jpg", fit=ft.ImageFit.COVER), height=250, bottom=0),
                ft.Container(
                    content=ft.Column([
                        ft.Image(src="assets/TopSUNify.png", width=200),
                        ft.TextField(label="نام کاربری", prefix_icon=ft.icons.PERSON),
                        ft.TextField(label="رمز ورود", password=True, can_reveal_password=True, prefix_icon=ft.icons.LOCK),
                        ft.ElevatedButton("ورود به TopSUNify", bgcolor="#FFD60A", color="#1e293b", height=50, width=400,
                                          on_click=lambda _: setattr(page.session, 'logged_in', True) or page.go("/app"))
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    padding=30, top=100
                )
            ])
        ])

    # --- تابع رندر صفحه اصلی (داشبورد و تب‌ها) ---
    def build_app_page():
        # محتوای تب‌ها
        content = ft.Text(f"شما در تب {page.session.active_tab} هستید")
        
        return ft.View("/app", [
            ft.AppBar(title=ft.Text("سامانه تاپسانیفای"), center_title=True),
            ft.Container(content=content, alignment=ft.alignment.center, expand=True),
            ft.NavigationBar(
                selected_index=0,
                on_change=lambda e: print(f"Tab changed to {e.control.selected_index}"),
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
    page.go("/")

# اجرای برنامه در Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
