import flet as ft
import os

def main(page: ft.Page):
    # تنظیم فونت
    page.fonts = {"iranyekan": "iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    
    page.title = "TopSUNify"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.session.logged_in = False
    
    username = ft.TextField(label="نام کاربری", border_radius=10, width=300)
    password = ft.TextField(label="رمز عبور", password=True, can_reveal_password=True, border_radius=10, width=300)

    def login(e):
        if username.value == "admin" and password.value == "1234":
            page.session.logged_in = True
            render()
        else:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("نام کاربری یا رمز عبور اشتباه است!")))
            page.update()

    # تابع ساخت دکمه با آیکون سفارشی
    def create_nav_icon(icon_path, index, tooltip):
        return ft.Container(
            content=ft.Image(src=icon_path, width=30, height=30),
            padding=10,
            on_click=lambda _: render(index),
            tooltip=tooltip,
            border_radius=10,
        )

    def render(tab_index=0):
        page.controls.clear()
        
        if not page.session.logged_in:
            # صفحه ورود به سبک موبایلت
            page.add(
                ft.Container(
                    content=ft.Column([
                        ft.Text("ورود به تاپسانیفای", size=24, weight="bold", color="#005b96"),
                        ft.Container(height=10),
                        username,
                        password,
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            "ورود به برنامه",
                            on_click=login,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                padding=15,
                            ),
                            width=300
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True),
                    padding=30,
                    border=ft.border.all(1, "#e0e0e0"),
                    border_radius=20,
                    bgcolor=ft.colors.WHITE,
                    shadow=ft.BoxShadow(blur_radius=20, color=ft.colors.GREY_300),
                    width=350,
                    alignment=ft.alignment.center
                )
            )
        else:
            # چیدمان اصلی بعد از ورود
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
                ft.Divider(),
                ft.Container(content=contents[tab_index], expand=True, alignment=ft.alignment.center),
                ft.Divider(),
                nav_buttons
            )
        page.update()

    render()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
