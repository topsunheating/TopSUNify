import flet as ft
import os

def main(page: ft.Page):
    page.title = "TopSUNify Dashboard"
    page.fonts = {"iranyekan": "fonts/iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    page.padding = 0
    page.rtl = True
    page.theme_mode = "light"
    page.bgcolor = "#f5f5f5"

    if not hasattr(page.session, "logged_in"):
        page.session.logged_in = False
        page.session.selected_month = 2 # خرداد

    def show_message(text: str, color="green"):
        page.snack_bar = ft.SnackBar(content=ft.Text(text), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    # --- صفحات ---
    def dashboard_page():
        # منوی انتخاب زیرمجموعه
        user_dropdown = ft.Dropdown(
            label="انتخاب مجموعه",
            value="مجموعه اصلی من",
            width=350,
            options=[ft.dropdown.Option("مجموعه اصلی من"), ft.dropdown.Option("زیرمجموعه ۱")],
            bgcolor="white"
        )

        # نوار ماه و سال
        months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
        month_selector = ft.Row([
            ft.IconButton(ft.Icons.ARROW_FORWARD, on_click=lambda _: None),
            ft.Container(content=ft.Text(months[page.session.selected_month], weight="bold", color="white"), 
                         bgcolor="#2196F3", padding=10, border_radius=10),
            ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: None),
        ], alignment=ft.MainAxisAlignment.CENTER)

        # دکمه‌های گزارش
        reports = ["پیش فاکتورها", "فاکتورهای فروش", "فاکتورهای تسویه شده", "فاکتورهای باز", "پروژه های نصب شده"]
        report_buttons = ft.Column([
            ft.ElevatedButton(text=r, width=350, height=50) for r in reports
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        return ft.Container(
            content=ft.Column([user_dropdown, month_selector, report_buttons], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
            padding=10
        )

    def render(index=0):
        page.controls.clear()
        if not page.session.logged_in:
            page.add(ft.Column([
                ft.Text("خوش آمدید", size=30),
                ft.ElevatedButton("ورود به سیستم", on_click=lambda e: (setattr(page.session, 'logged_in', True), render()))
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True))
        else:
            # ساختار اصلی
            page.add(
                ft.Column([
                    ft.Container(content=ft.Text("TopSUNify", size=20), padding=15, bgcolor="white", width=400),
                    ft.Container(content=dashboard_page(), expand=True),
                    ft.Container(
                        content=ft.Row([
                            ft.IconButton(ft.Icons.DASHBOARD, on_click=lambda _: render(0)),
                            ft.IconButton(ft.Icons.PERSON, on_click=lambda _: render(0)),
                        ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                        bgcolor="white", padding=10
                    )
                ], expand=True)
            )
        page.update()

    render()

if __name__ == "__main__":
    ft.app(target=main)
