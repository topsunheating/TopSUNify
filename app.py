import flet as ft
import os

def main(page: ft.Page):
    # یک المان ساده برای تست رندر
    page.add(ft.Text("سیستم فعال شد!", size=40, color="red"))
    page.update()

# این تنظیمات برای Railway حیاتی است
if __name__ == "__main__":
    # دریافت پورت از Railway
    port = int(os.environ.get("PORT", 8080))
    
    # اجرای بدون view برای جلوگیری از تداخل مرورگر
    ft.app(
        target=main,
        port=port,
        host="0.0.0.0"
    )
