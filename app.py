import flet as ft
import os

def main(page: ft.Page):
    page.title = "TopSUNify"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    
    page.session.logged_in = False
    
    # فیلدها
    username = ft.TextField(label="نام کاربری")
    password = ft.TextField(label="رمز عبور", password=True)

    def login(e):
        if username.value == "admin" and password.value == "1234":
            page.session.logged_in = True
            render()
        else:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("نام کاربری یا رمز عبور اشتباه است!")))
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
            # ایجاد منو برای جابجایی بین بخش‌ها
            def change_tab(e):
                render(e.control.selected_index)

            # محتوای هر بخش
            content = ft.Text("خوش آمدید!")
            if tab_index == 1:
                content = ft.Text("لیست فاکتورها: (در حال ساخت)")
            elif tab_index == 2:
                content = ft.Text("اطلاعات تاپسان: (در حال ساخت)")

            page.add(
                ft.Text("پنل مدیریت", size=20),
                content,
                ft.NavigationBar(
                    selected_index=tab_index,
                    on_change=change_tab,
                    destinations=[
                        ft.NavigationBarDestination(icon="dashboard", label="داشبورد"),
                        ft.NavigationBarDestination(icon="receipt", label="فاکتور"),
                        ft.NavigationBarDestination(icon="info", label="اطلاعات"),
                    ]
                )
            )
        page.update()

    render()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0")
