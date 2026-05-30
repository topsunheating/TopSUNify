import flet as ft
import os
import time

def main(page: ft.Page):
    page.fonts = {"iranyekan": "fonts/iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    page.padding = 0
    page.rtl = True
    page.theme_mode = "light"
    
    if not hasattr(page.session, "logged_in"):
        page.session.logged_in = False

    # ==================== دیالوگ بیومتریک (Popup) ====================
    def show_biometric_dialog(e):
        dlg = ft.AlertDialog(
            title=ft.Text("احراز هویت بیومتریک", size=18, weight="bold"),
            content=ft.Column([
                ft.Text("از اثر انگشت یا تشخیص چهره استفاده کنید", text_align="center"),
                ft.ProgressRing(width=60, height=60, stroke_width=6),
                ft.Text("در حال اتصال به حسگر...", size=14, color="grey", text_align="center")
            ], horizontal_alignment="center", spacing=25, height=200),
            actions=[
                ft.TextButton("انصراف", on_click=lambda _: (setattr(dlg, 'open', False), page.update()))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        page.dialog = dlg
        dlg.open = True
        page.update()

        # شبیه‌سازی موفقیت بیومتریک
        time.sleep(2)
        dlg.open = False
        page.session.logged_in = True
        page.update()
        render()

    # ==================== صفحه لاگین (شبیه عکس دوم) ====================
    def render(tab_index=0):
        page.controls.clear()

        if not page.session.logged_in:
            page.add(
                ft.Column([
                    # لوگو TopSUNify
                    ft.Container(
                        content=ft.Image(src="TopSUNify.png", width=190),
                        margin=ft.margin.Margin(top=40, bottom=40)
                    ),

                    # فیلد نام کاربری
                    ft.Container(
                        content=ft.TextField(
                            label="نام کاربری",
                            width=340,
                            border_radius=12,
                            prefix_icon=ft.Icons.PERSON,
                            text_align=ft.TextAlign.RIGHT,
                        ),
                        margin=ft.margin.Margin(bottom=20)
                    ),

                    # فیلد رمز عبور + آیکون بیومتریک (زرد)
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.FINGERPRINT, size=38, color="#FFCC00"),
                            ft.TextField(
                                label="رمز عبور",
                                password=True,
                                width=280,
                                border_radius=12,
                                prefix_icon=ft.Icons.LOCK,
                                text_align=ft.TextAlign.RIGHT,
                            )
                        ], alignment="center", spacing=10),
                        margin=ft.margin.Margin(bottom=30)
                    ),

                    # دکمه ورود زرد بزرگ
                    ft.ElevatedButton(
                        "ورود به TopSUNify",
                        width=340,
                        bgcolor="#FFCC00",
                        color="black",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=30),
                            text_style=ft.TextStyle(size=17, weight="bold")
                        ),
                        on_click=lambda e: (setattr(page.session, 'logged_in', True), render())
                    ),

                    ft.Text(
                        "فعال‌سازی / فراموشی رمز",
                        size=14,
                        color="blue",
                        text_align="center"
                    ),

                    # Powered by - دقیقاً مثل عکس دوم
                    ft.Container(
                        content=ft.Image(src="TopSUN-Powered.png", width=160),
                        margin=ft.margin.Margin(top=50, bottom=30)
                    ),

                    # تصویر پس‌زمینه پایین
                    ft.Container(
                        expand=True,
                        content=ft.Image(
                            src="landscape.jpg",
                            width=400,
                            height=220,
                            fit="cover"
                        ),
                        margin=ft.margin.Margin(top=10)
                    )
                ], 
                horizontal_alignment="center", 
                expand=True,
                scroll=ft.ScrollMode.AUTO
                )
            )
        else:
            # پنل بعد از ورود
            contents = [
                ft.Text("داشبورد مدیریتی", size=25),
                ft.Text("بخش پیش‌فاکتورها", size=25),
                ft.Column([ft.Image(src="TopSUNify-1.png", width=200), ft.Text("خانه اصلی", size=25)], horizontal_alignment="center"),
                ft.Text("اطلاعات فنی سیستم", size=25),
                ft.Text("پروفایل کاربری", size=25)
            ]

            nav_buttons = ft.Row([
                ft.IconButton(icon="dashboard", on_click=lambda _: render(0)),
                ft.IconButton(icon="edit_document", on_click=lambda _: render(1)),
                ft.IconButton(icon="home", on_click=lambda _: render(2)),
                ft.IconButton(icon="build", on_click=lambda _: render(3)),
                ft.IconButton(icon="person", on_click=lambda _: render(4)),
            ], alignment="center")

            page.add(
                ft.Column([
                    ft.Text("پنل TopSUNify", size=30, weight="bold"),
                    ft.Divider(),
                    ft.Container(
                        content=contents[tab_index], 
                        expand=True, 
                        alignment=ft.Alignment(0, 0)
                    ),
                    nav_buttons
                ], horizontal_alignment="center", expand=True)
            )

        page.update()

    render()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
