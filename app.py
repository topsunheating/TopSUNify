import flet as ft
import os

def main(page: ft.Page):
    # به جای ویو، فقط یک متن ساده اضافه می‌کنیم
    page.add(ft.Text("تست نهایی: اگر این را می‌بینید، سیستم زنده است!", size=30, color="blue"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0")
