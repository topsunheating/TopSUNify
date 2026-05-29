import flet as ft
import os

def main(page: ft.Page):
    page.title = "TopSUNify"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    page.padding = 0

    # مقداردهی اولیه سشن
    page.session.logged_in = False
    page.session.active_tab = 0

    # فیلدها
    username = ft.TextField(label="نام کاربری", width=300)
    password = ft.TextField(label="رمز عبور", password=True, width=300)

    # تابع ورود
    def login(e):
        if username.value == "admin" and password.value == "1234":
            page.session.logged_in = True
            update_ui()
        else:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("نام کاربری یا رمز عبور اشتباه است!")))
            page.update()

    # تابع تغییر تب‌ها
    def on_nav_change(e):
        page.session.active_tab = e.control.selected_index
        update_ui()

    # تابع تولید محتوای هر تب
    def get_tab_content(index):
        if index == 0:  # داشبورد
            return ft.Column([
                ft.Card(content=ft.Container(ft.Text("آمار فروش: ۲۰٪ رشد"), padding=20)),
                ft.Card(content=ft.Container(ft.Text("تعداد فاکتورهای جدید: ۵"), padding=20)),
            ])
        elif index == 1:  # فاکتور
            return ft.Text("در اینجا لیست فاکتورها نمایش داده می‌شود.")
        elif index == 2:  # تاپسان
            return ft.Text("اطلاعات فنی تاپسان در این بخش قرار می‌گیرد.")
        else:  # پروفایل
            return ft.Text("تنظیمات پروفایل کاربری.")

    # تابع اصلی رندر
    def update_ui():
        page.controls.clear()
        
        if not page.session.logged_in:
            page.add(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("ورود به تاپسانیفای", size=25, weight="bold"),
                            username, 
                            password,
                            ft.ElevatedButton("ورود", on_click=login)
                        ], 
                        horizontal_alignment="center" # استفاده از متن به جای ماژول
                    ),
                    padding=20, 
                    alignment="center" # استفاده از متن به جای ماژول
                )
            )
        else:
            page.add(
                ft.AppBar(title=ft.Text("پنل مدیریت تاپسانیفای"), bgcolor="blue_grey_50"),
                ft.Container(
                    content=get_tab_content(page.session.active_tab),
                    padding=20
                ),
                ft.NavigationBar(
                    selected_index=page.session.active_tab,
                    on_change=on_nav_change,
                    destinations=[
                        ft.NavigationBarDestination(icon="dashboard", label="داشبورد"),
                        ft.NavigationBarDestination(icon="receipt", label="فاکتور"),
                        ft.NavigationBarDestination(icon="info", label="تاپسان"),
                        ft.NavigationBarDestination(icon="person", label="پروفایل"),
                    ]
                )
            )
        page.update()

    update_ui()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0")
