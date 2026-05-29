import flet as ft
import os

def main(page: ft.Page):
    page.title = "TopSUNify"
    page.add(ft.Text("سامانه بدون مشکل بالا آمد!", size=30, color="green"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0")
