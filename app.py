import flet as ft
import os

def main(page: ft.Page):
    page.fonts = {"iranyekan": "iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
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

    # تابعی برای ساخت دکمه‌های آیکونی بدون خطا
    def create_nav_icon(emoji, index, tooltip):
        return ft.Container(
            content=ft.Text(emoji, size=24),
            padding=10,
            on_click=lambda _: render(index),
            tooltip=tooltip,
            border_radius=10,
        )

    def render(tab_index=0):
        page.controls.clear()
        
        if not page.session.logged_in:
            page.add(
                ft.Text("ورود به تاپسانیفای", size=25),
                username, password,
                ft.ElevatedButton("ورود", on_click=login)
            )
        else:
            contents = [
                ft.Text("داشبورد مدیریتی", size=20),
                ft.Text("بخش پیش‌فاکتورها", size=20),
                ft.Image(src="TopSUNify-1.png", width=300, height=300),
                ft.Text("اطلاعات فنی سیستم", size=20),
                ft.Text("پروفایل کاربری", size=20)
            ]

            # استفاده از کانتینرهای کلیک‌خور به جای IconButton
            nav_buttons = ft.Row([
                create_nav_icon("📊", 0, "داشبورد"),
                create_nav_icon("📝", 1, "پیش فاکتور"),
                create_nav_icon("🏠", 2, "خانه"),
                create_nav_icon("⚙️", 3, "اطلاعات فنی"),
                create_nav_icon("👤", 4, "پروفایل"),
            ], alignment="center")

            page.add(
                ft.Text("پنل مدیریت تاپسانیفای", size=30, weight="bold"),
                ft.Divider(),
                contents[tab_index],
                ft.Container(expand=True),
                nav_buttons
            )
        page.update()

    render()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
