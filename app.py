import flet as ft
import os

def main(page: ft.Page):
    # ... کدهای قبلی شما ...
    page.title = "TopSUNify"
    # ... (بقیه تنظیماتِ داخل main) ...
    # دقت کنید که بقیه توابعِ build_login_page و غیره سر جایشان باشند.

    # مدیریت مسیرها (همان کدی که داشتید)
    def route_change(route):
        page.views.clear()
        if page.session.logged_in:
            page.views.append(build_app_page())
        else:
            page.views.append(build_login_page())
        page.update()

    page.on_route_change = route_change
    page.go("/")

# تغییر کلیدی اینجاست:
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        port=port,
        host="0.0.0.0"
    )
