import flet as ft
import os

def main(page: ft.Page):
    # تنظیم فونت
    page.fonts = {"iranyekan": "fonts/iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    
    page.padding = 0
    page.rtl = True
    
    # متغیر وضعیت برای باز و بسته شدن دیالوگ
    def close_dlg(e):
        dlg.visible = False
        page.update()

    # دیالوگ سفارشی به جای استفاده از AlertDialog پیش‌فرض که گاهی در برخی نسخه‌ها مشکل دارد
    dlg = ft.Container(
        content=ft.Column([
            ft.Text("احراز هویت بیومتریک", size=20, weight="bold"),
            ft.ElevatedButton("اثر انگشت", on_click=close_dlg),
            ft.ElevatedButton("تشخیص چهره", on_click=close_dlg),
        ], alignment="center", horizontal_alignment="center"),
        width=300, height=200, bgcolor="white", border_radius=20,
        padding=20, visible=False, shadow=ft.BoxShadow(blur_radius=10)
    )

    def show_biometric(e):
        dlg.visible = True
        page.update()

    # صفحه اصلی
    page.add(
        ft.Stack([
            ft.Column([
                ft.Image(src="TopSUNify.png", width=150),
                ft.Row([
                    ft.TextField(label="نام کاربری", width=200),
                    # دکمه‌ای که حتما کار می‌کند
                    ft.IconButton(icon="fingerprint", on_click=show_biometric)
                ], alignment="center"),
            ], horizontal_alignment="center"),
            # قرار دادن دیالوگ در وسط صفحه با استفاده از Alignment
            ft.Container(content=dlg, alignment=ft.alignment.center)
        ])
    )

ft.app(target=main, assets_dir="assets")
