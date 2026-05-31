import flet as ft
import os

def main(page: ft.Page):
    # تنظیمات صفحه
    page.fonts = {"iranyekan": "fonts/iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    page.padding = 0
    page.rtl = True
    page.theme_mode = "light"
    page.bgcolor = "#f5f5f5"

    # سشن کاربر
    if not hasattr(page.session, "logged_in"):
        page.session.logged_in = False
        page.session.user_name = "۹۶۲۱-۸۰۰-۱۵۸۰۹۷-۱"
        page.session.selected_month_index = 2 # خرداد

    # ==================== داشبورد ====================
    def dashboard_page():
        months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
        
        def change_month(delta):
            page.session.selected_month_index = (page.session.selected_month_index + delta) % 12
            render(0)

        # منوی کشویی کاربر - اصلاح شده برای جلوگیری از خطا
        user_menu = ft.PopupMenuButton(
            content=ft.Row(
                [ft.Text(page.session.user_name, weight="bold", size=16), ft.Icon(ft.Icons.ARROW_DROP_DOWN)],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            items=[ft.PopupMenuItem(text="زیرمجموعه ۱"), ft.PopupMenuItem(text="زیرمجموعه ۲")]
        )

        # نوار ماه و سال - اصلاح شده برای جلوگیری از خطا
        month_slider = ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(ft.Icons.ARROW_LEFT, on_click=lambda _: change_month(1)),
                    ft.Container(
                        content=ft.Text(months[page.session.selected_month_index], size=18, weight="bold", color="white"),
                        bgcolor="#2196F3",
                        padding=ft.padding.symmetric(horizontal=20, vertical=5),
                        border_radius=20
                    ),
                    ft.IconButton(ft.Icons.ARROW_RIGHT, on_click=lambda _: change_month(-1)),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            margin=ft.margin.only(top=10, bottom=20)
        )

        # دکمه‌های گزارش
        report_buttons = ["پیش‌فاکتورها", "فاکتورهای فروش", "فاکتورهای تسویه شده", "فاکتورهای باز", "پروژه‌های نصب شده"]
        buttons_col = ft.Column(
            [
                ft.ElevatedButton(text=btn, width=300, height=50, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))) 
                for btn in report_buttons
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        return ft.Column([user_menu, month_slider, buttons_col], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # رندر نهایی - اصلاح شده برای جلوگیری از خطای alignment
    def render(tab_index=0):
        page.controls.clear()
        if not page.session.logged_in:
            page.add(
                ft.Container(
                    content=ft.ElevatedButton("ورود", on_click=lambda e: (setattr(page.session, 'logged_in', True), render())),
                    alignment=ft.alignment.center, # در اینجا ft.alignment.center صحیح است
                    expand=True
                )
            )
        else:
            page.add(
                ft.Column([
                    ft.Container(content=dashboard_page() if tab_index==0 else ft.Text("سایر صفحات"), expand=True, padding=20),
                    ft.NavigationBar(
                        selected_index=tab_index,
                        on_change=lambda e: render(e.control.selected_index),
                        destinations=[
                            ft.NavigationDestination(icon=ft.Icons.DASHBOARD, label="داشبورد"), 
                            ft.NavigationDestination(icon=ft.Icons.INVOICE, label="فاکتور"), 
                            ft.NavigationDestination(icon=ft.Icons.PERSON, label="پروفایل")
                        ]
                    )
                ], expand=True)
            )
        page.update()

    render()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0")
