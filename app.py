import flet as ft
import os

def main(page: ft.Page):
    page.title = "TopSUNify"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    
    # متغیرهای لاگین
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
                username, password,
                ft.ElevatedButton("ورود", on_click=login)
            )
        else:
            # تعریف محتوا برای هر تب
            contents = [
                ft.Text("خوش آمدید! اینجا داشبورد اصلی است.", size=20),
                ft.Text("لیست فاکتورها: (اطلاعات اینجا قرار می‌گیرد)", size=20),
                ft.Text("اطلاعات فنی تاپسان (در حال ساخت)", size=20)
            ]

            def change_tab(e):
                render(e.control.selected_index)

            # افزودن المان‌ها
            page.add(
                ft.Text("پنل مدیریت", size=30, weight="bold"),
                ft.Divider(),
                contents[tab_index],
                # مدیریت بهتر نوار پایین برای جلوگیری از فضای طوسی خالی
            )
            
            # افزودن نوار پایین به صورت مستقل
            page.navigation_bar = ft.NavigationBar(
                selected_index=tab_index,
                on_change=change_tab,
                destinations=[
                    ft.NavigationBarDestination(icon="dashboard", label="داشبورد"),
                    ft.NavigationBarDestination(icon="receipt", label="فاکتور"),
                    ft.NavigationBarDestination(icon="info", label="اطلاعات"),
                ]
            )
            
        page.update()

    render()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0")
