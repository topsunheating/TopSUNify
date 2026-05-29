import flet as ft
import os

def main(page: ft.Page):
    # یک متن ساده برای تست
    page.add(ft.Text("TopSUNify is working!", size=30, color="blue"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0")
