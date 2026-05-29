import flet as ft
import os

def main(page: ft.Page):
    # ۱. معرفی فونت به فلت
    page.fonts = {
        "iranyekan": "iranyekan.ttf"  # نام فونت در برنامه : نام فایل در فولدر
    }
    
    # ۲. اعمال فونت به کل تم برنامه
    page.theme = ft.Theme(font_family="iranyekan")
    
    page.title = "TopSUNify"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    
    page.session.logged_in = False
    
    def login(e):
        if username.value == "admin" and password.value == "1234":
            page.session.logged_in = True
            render()
        else:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("اطلاعات اشتباه است!")))
            page.update()

    username = ft.TextField(label="نام کاربری")
    password = ft.TextField(label="رمز عبور", password=True)

    def render(tab_index=0):
        page.controls.clear()
        
        if not page.session.logged_in:
            page.add(
                ft.Text("ورود به تاپسانیفای", size=25, weight="bold"),
                username, password,
                ft.ElevatedButton("ورود", on_click=login)
            )
        else:
            contents = [
                ft.Text("داشبورد مدیریتی", size=20),
                ft.Text("بخش پیش‌فاکتورها", size=20),
                ft.Image(src="https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/TopSUNify-1.png", width=300),
                ft.Text("اطلاعات فنی سیستم", size=20),
                ft.Text("پروفایل کاربری", size=20)
            ]

            nav_buttons = ft.Row([
                ft.ElevatedButton("داشبورد", on_click=lambda _: render(0)),
                ft.ElevatedButton("پیش فاکتور", on_click=lambda _: render(1)),
                ft.ElevatedButton("TopSUNify", on_click=lambda _: render(2)),
                ft.ElevatedButton("اطلاعات فنی", on_click=lambda _: render(3)),
                ft.ElevatedButton("پروفایل", on_click=lambda _: render(4)),
            ], alignment="center", wrap=True)

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
    # دقت کنید: assets_dir="." باعث می‌شود فایل فونت شناسایی شود
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir=".")
