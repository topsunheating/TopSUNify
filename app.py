import flet as ft
import os

def main(page: ft.Page):
    # تنظیم فونت
    page.fonts = {"iranyekan": "iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    
    page.title = "TopSUNify"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    page.session.logged_in = False
    
    username = ft.TextField(label="نام کاربری", width=300)
    password = ft.TextField(label="رمز عبور", password=True, width=300)

    def login(e):
        if username.value == "admin" and password.value == "1234":
            page.session.logged_in = True
            render()
        else:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("نام کاربری یا رمز عبور اشتباه است!")))
            page.update()

    def create_nav_icon(icon_path, index, tooltip):
        return ft.Container(
            content=ft.Image(src=icon_path, width=30, height=30),
            padding=10,
            on_click=lambda _: render(index),
            tooltip=tooltip
        )

    def render(tab_index=0):
        page.controls.clear()
        
        if not page.session.logged_in:
            page.add(
                ft.Column([
                    ft.Text("ورود به تاپسانیفای", size=24, weight="bold"),
                    username,
                    password,
                    ft.ElevatedButton("ورود به برنامه", on_click=login, width=300)
                ], horizontal_alignment="center") # استفاده از رشته بجای کلاس برای اطمینان
            )
        else:
            contents = [
                ft.Text("داشبورد مدیریتی", size=20),
                ft.Text("بخش پیش‌فاکتورها", size=20),
                ft.Image(src="TopSUNify-1.png", width=300, height=300),
                ft.Text("اطلاعات فنی سیستم", size=20),
                ft.Text("پروفایل کاربری", size=20)
            ]

            nav_buttons = ft.Row([
                create_nav_icon("dashboard.png", 0, "داشبورد"),
                create_nav_icon("invoice.png", 1, "پیش فاکتور"),
                create_nav_icon("TopSUNify-1.png", 2, "خانه"),
                create_nav_icon("technical.png", 3, "اطلاعات فنی"),
                create_nav_icon("profile.png", 4, "پروفایل"),
            ], alignment="center")

            page.add(
                ft.Text("پنل مدیریت تاپسانیفای", size=25, weight="bold"),
                contents[tab_index],
                nav_buttons
            )
        page.update()

    render()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
