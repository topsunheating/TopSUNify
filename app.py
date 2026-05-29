import flet as ft
import os

def main(page: ft.Page):
    page.title = "TopSUNify"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    page.padding = 0

    page.session.logged_in = False

    def build_login():
        return ft.View("/", [
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.SUNNY, size=80, color="#FFD60A"), # جایگزین لوگو
                    ft.Text("TopSUNify", size=30, weight="bold"),
                    ft.TextField(label="نام کاربری", prefix_icon=ft.icons.PERSON),
                    ft.TextField(label="رمز ورود", password=True, prefix_icon=ft.icons.LOCK),
                    ft.ElevatedButton("ورود", bgcolor="#FFD60A", on_click=lambda _: setattr(page.session, 'logged_in', True) or page.go("/app"))
                ], alignment=ft.MainAxisAlignment.CENTER),
                padding=40
            )
        ])

    def build_app_page():
        return ft.View("/app", [
            ft.AppBar(title=ft.Text("داشبورد تاپسانیفای")),
            ft.Container(content=ft.Text("به سیستم خوش آمدید"), alignment=ft.alignment.center),
            ft.NavigationBar(destinations=[
                ft.NavigationBarDestination(icon=ft.icons.DASHBOARD, label="داشبورد"),
                ft.NavigationBarDestination(icon=ft.icons.PERSON, label="پروفایل"),
            ])
        ])

    def route_change(route):
        page.views.clear()
        page.views.append(build_app_page() if page.session.logged_in else build_login())
        page.update()

    page.on_route_change = route_change
    page.go("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # بدون assets_dir برای جلوگیری از خطای لودینگ
    ft.app(target=main, port=port, host="0.0.0.0")
