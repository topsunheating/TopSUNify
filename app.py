import flet as ft
import os

def main(page: ft.Page):
    # تنظیمات ساده و امن برای وب
    page.title = "TopSUNify"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # یک تابع برای تغییر صفحه
    def button_click(e):
        page.add(ft.Text("دکمه کار کرد، برنامه زنده است!", color="red"))
        page.update()

    # محتوای اصلی
    page.add(
        ft.Column([
            ft.Text("سیستم فعال شد!", size=30),
            ft.ElevatedButton("تست دکمه", on_click=button_click)
        ])
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0")
