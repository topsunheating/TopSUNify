import flet as ft
import os

def main(page: ft.Page):
    page.fonts = {"iranyekan": "iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    page.padding = 0 # حذف حاشیه صفحه برای تمام‌صفحه شدن
    
    def show_biometric_dialog(e):
        dlg = ft.AlertDialog(title=ft.Text("احراز هویت"), content=ft.Text("در حال اسکن..."))
        page.dialog = dlg
        dlg.open = True
        page.update()

    def render(tab_index=0):
        page.controls.clear()
        
        # لایه اصلی برای چیدمان روی عکس
        page.add(
            ft.Stack([
                # لایه اول: عکس پس‌زمینه که کل صفحه را می‌پوشاند
                ft.Container(
                    content=ft.Image(src="landscape.jpg", fit=ft.ImageFit.COVER),
                    expand=True
                ),
                # لایه دوم: فرم ورود که روی عکس قرار می‌گیرد
                ft.Container(
                    content=ft.Column([
                        ft.Image(src="topsunify.png", width=220),
                        ft.TextField(label="نام کاربری", bgcolor="white"),
                        ft.Row([
                            ft.TextField(label="رمز ورود", bgcolor="white", expand=True),
                            ft.IconButton(icon=ft.icons.FINGERPRINT, on_click=show_biometric_dialog)
                        ]),
                        ft.ElevatedButton("ورود به TopSUNify", width=300),
                        ft.Text("فعال سازی / فراموشی رمز عبور", color="blue")
                    ], horizontal_alignment="center"),
                    padding=20,
                    alignment=ft.alignment.center
                )
            ])
        )
        page.update()
    render()

if __name__ == "__main__":
    ft.app(target=main, port=8080, host="0.0.0.0", assets_dir="assets")
