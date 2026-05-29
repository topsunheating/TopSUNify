import flet as ft
import os

def main(page: ft.Page):
    page.title = "TopSUNify"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    
    # متغیرهای سشن
    page.session.logged_in = False
    
    # فیلدها
    username = ft.TextField(label="نام کاربری")
    password = ft.TextField(label="رمز عبور", password=True)

    def login(e):
        if username.value == "admin" and password.value == "1234":
            page.session.logged_in = True
            render()
        else:
            page.add(ft.Text("خطا در ورود"))
            page.update()

    def render():
        page.controls.clear()
        if not page.session.logged_in:
            page.add(
                ft.Text("ورود به سیستم", size=20),
                username,
                password,
                ft.ElevatedButton("ورود", on_click=login)
            )
        else:
            page.add(
                ft.Text("خوش آمدید به داشبورد", size=20),
                ft.ElevatedButton("خروج", on_click=lambda _: (setattr(page.session, "logged_in", False), render()))
            )
        page.update()

    render()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0")
