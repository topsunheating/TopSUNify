import flet as ft
import os

def main(page: ft.Page):
    # تنظیمات اولیه صفحه
    page.title = "TopSUNify"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    
    # متغیر سشن برای مدیریت وضعیت ورود
    page.session.logged_in = False
    
    # فیلدهای ورودی
    username = ft.TextField(label="نام کاربری")
    password = ft.TextField(label="رمز عبور", password=True)

    # تابع ورود به سیستم
    def login(e):
        if username.value == "admin" and password.value == "1234":
            page.session.logged_in = True
            render()
        else:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("نام کاربری یا رمز عبور اشتباه است!")))
            page.update()

    # تابع اصلی برای رندر کردن محتوا
    def render(tab_index=0):
        page.controls.clear()
        
        # اگر کاربر وارد نشده باشد، فرم ورود را نشان بده
        if not page.session.logged_in:
            page.add(
                ft.Text("ورود به تاپسانیفای", size=25),
                username,
                password,
                ft.ElevatedButton("ورود", on_click=login)
            )
        else:
            # محتوای مربوط به هر تب
            # توجه: برای نمایش تصویر در سرور، حتما عکس باید در پوشه assets باشد
            contents = [
                ft.Text("داشبورد مدیریتی", size=20),
                ft.Text("بخش پیش‌فاکتورها", size=20),
                ft.Image(src="TopSUNify-1.png", width=300, height=300, fit=ft.ImageFit.CONTAIN),
                ft.Text("اطلاعات فنی سیستم", size=20),
                ft.Text("پروفایل کاربری", size=20)
            ]

            # دکمه‌های ناوبری (ساده و پایدار)
            nav_buttons = ft.Row([
                ft.ElevatedButton("داشبورد", on_click=lambda _: render(0)),
                ft.ElevatedButton("پیش فاکتور", on_click=lambda _: render(1)),
                ft.ElevatedButton("TopSUNify", on_click=lambda _: render(2)),
                ft.ElevatedButton("اطلاعات فنی", on_click=lambda _: render(3)),
                ft.ElevatedButton("پروفایل", on_click=lambda _: render(4)),
            ], alignment="center", wrap=True)

            # افزودن المان‌ها به صفحه
            page.add(
                ft.Text("پنل مدیریت تاپسانیفای", size=30, weight="bold"),
                ft.Divider(),
                contents[tab_index],
                ft.Container(expand=True), # فضای خالی برای چسباندن دکمه‌ها به پایین
                nav_buttons
            )
        page.update()

    # اجرای اولیه
    render()

# اجرای برنامه در سرور
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0")
