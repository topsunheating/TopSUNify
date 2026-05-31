import flet as ft
import os

def main(page: ft.Page):
    page.title = "TopSUNify Dashboard"
    page.padding = 0
    page.rtl = True
    page.theme_mode = "light"
    page.bgcolor = "#f5f5f5"

    if not hasattr(page.session, "logged_in"):
        page.session.logged_in = False
        page.session.selected_month = 2

    # --- تابع رندر ---
    def render(index=0):
        page.controls.clear()
        
        if not page.session.logged_in:
            page.add(
                ft.Column([
                    ft.Text("خوش آمدید", size=30),
                    ft.ElevatedButton("ورود به سیستم", on_click=lambda e: (setattr(page.session, 'logged_in', True), render()))
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
            )
        else:
            # منوی دراپ‌داون
            user_dropdown = ft.Dropdown(
                label="انتخاب مجموعه",
                options=[ft.dropdown.Option("مجموعه اصلی من"), ft.dropdown.Option("زیرمجموعه ۱")],
                width=350
            )

            # دکمه‌های گزارش
            reports = ["پیش فاکتورها", "فاکتورهای فروش", "فاکتورهای تسویه شده", "فاکتورهای باز", "پروژه های نصب شده"]
            buttons = ft.Column([ft.ElevatedButton(text=r, width=350) for r in reports], alignment=ft.MainAxisAlignment.CENTER)

            page.add(
                ft.Column([
                    ft.Container(content=ft.Text("TopSUNify", size=20, weight="bold"), padding=10, bgcolor="white"),
                    ft.Container(content=user_dropdown, padding=10),
                    ft.Container(content=buttons, expand=True),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.DASHBOARD), ft.Icon(ft.Icons.PERSON)
                        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                        padding=10, bgcolor="white"
                    )
                ], expand=True)
            )
        page.update()

    render()

if __name__ == "__main__":
    # استفاده از پورت محیط (مثل Heroku/Docker) یا پیش‌فرض 8080
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0")
