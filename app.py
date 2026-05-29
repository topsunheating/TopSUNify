import flet as ft
import os

def main(page: ft.Page):
    page.title = "TopSUNify"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    page.padding = 0

    # متغیر برای کنترل تب‌ها
    page.session.active_tab = 0

    # تابعی برای ساخت محتوای تب‌ها
    def get_content(index):
        if index == 0:
            return ft.Column([ft.Text("📊 داشبورد اصلی", size=20), ft.Text("خوش آمدید!")])
        elif index == 1:
            return ft.Text("🧾 بخش پیش‌فاکتورها")
        elif index == 2:
            return ft.Text("📚 اطلاعات فنی")
        else:
            return ft.Text("👤 پروفایل کاربری")

    # استفاده از Container برای محتوا
    content_area = ft.Container(content=get_content(0), padding=20, expand=True)

    def nav_change(e):
        page.session.active_tab = e.control.selected_index
        content_area.content = get_content(page.session.active_tab)
        page.update()

    # اصلاح: استفاده از نام رنگ‌ها به صورت رشته (String) برای سازگاری کامل
    page.add(
        ft.AppBar(
            title=ft.Text("TopSUNify"), 
            bgcolor="blue_grey_100" # جایگزین ft.colors.SURFACE_VARIANT
        ),
        content_area,
        ft.NavigationBar(
            selected_index=page.session.active_tab,
            on_change=nav_change,
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.DASHBOARD, label="داشبورد"),
                ft.NavigationBarDestination(icon=ft.icons.RECEIPT, label="فاکتور"),
                ft.NavigationBarDestination(icon=ft.icons.INFO, label="تاپسان"),
                ft.NavigationBarDestination(icon=ft.icons.PERSON, label="پروفایل"),
            ]
        )
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0")
