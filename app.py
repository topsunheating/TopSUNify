import flet as ft
import os

def main(page: ft.Page):
    # تنظیمات صفحه
    page.fonts = {"iranyekan": "fonts/iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    page.rtl = True
    
    # تعریف FilePicker داخل main (بسیار مهم)
    file_picker = ft.FilePicker(on_result=lambda e: print("فایل انتخاب شد"))
    page.overlay.append(file_picker)
    page.update()

    # تابع نمایش پیام
    def show_message(text, color="green"):
        page.snack_bar = ft.SnackBar(content=ft.Text(text), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    # تعریف صفحه گرمایش از کف
    def floor_heating_page():
        return ft.Container(
            content=ft.Column([
                ft.Text("گرمایش از کف", size=20, weight="bold"),
                ft.ElevatedButton("آپلود فایل", on_click=lambda e: file_picker.pick_files())
            ])
        )

    page.add(floor_heating_page())

# بخش اجرای وب (حیاتی برای Railway)
if __name__ == "__main__":
    # استفاده از 0.0.0.0 برای اینکه سرور Railway بتواند به آن وصل شود
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, view=ft.AppView.WEB_BROWSER)
