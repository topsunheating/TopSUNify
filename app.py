import flet as ft
import os

def main(page: ft.Page):
    page.title = "TopSUNify"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    
    page.session.logged_in = False
    
    username = ft.TextField(label="نام کاربری")
    password = ft.TextField(label="رمز عبور", password=True)

    def login(e):
        if username.value == "admin" and password.value == "1234":
            page.session.logged_in = True
            render()
        else:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("اطلاعات اشتباه است!")))
            page.update()

    def render(tab_index=0):
        page.controls.clear()
        
        if not page.session.logged_in:
            page.add(
                ft.Text("ورود به تاپسانیفای", size=25),
                username,
                password,
                ft.ElevatedButton("ورود", on_click=login)
            )
        else:
            # محتوای تب‌ها
            contents = [
                ft.Text("داشبورد اصلی", size=20),
                ft.Text("لیست فاکتورها", size=20),
                ft.Text("اطلاعات فنی", size=20)
            ]

            # دکمه‌های ناوبری جایگزین
            nav_buttons = ft.Row([
                ft.ElevatedButton("داشبورد", on_click=lambda _: render(0)),
                ft.ElevatedButton("فاکتور", on_click=lambda _: render(1)),
                ft.ElevatedButton("اطلاعات", on_click=lambda _: render(2)),
            ], alignment="center")

            page.add(
                ft.Text("پنل مدیریت", size=30, weight="bold"),
                ft.Divider(),
                contents[tab_index],
                ft.Container(expand=True),
                nav_buttons
            )
        page.update()

    render()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0")
