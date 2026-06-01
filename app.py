import flet as ft
import os
import requests

GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbygH2yHhw44Lk5Hv8okJDnRBgGw2UzoF1wsZvMGGGr7ZzhSS0Ro6WhSeVFTPM2TpsMv/exec"

def main(page: ft.Page):
    page.fonts = {"iranyekan": "fonts/iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    page.padding = 0
    page.rtl = True
    page.theme_mode = "light"
    page.bgcolor = "#f5f5f5"

    if not hasattr(page.session, "logged_in"):
        page.session.logged_in = False
        page.session.user_role = "عمومی"

    def show_message(text: str, color="green"):
        snack = ft.SnackBar(content=ft.Text(text), bgcolor=color, action="بستن", duration=3000)
        page.snack_bar = snack
        snack.open = True
        page.update()

    # ==================== تغییر تم ====================
    def toggle_theme(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()
        show_message(f"تم تغییر کرد به: {page.theme_mode}", "blue")

    # ==================== درخواست ایجاد حساب ====================
    def open_create_account_dialog(e):
        dlg = ft.AlertDialog(
            title=ft.Text("درخواست ایجاد حساب همکار", size=18, weight="bold"),
            content=ft.Container(
                content=ft.Column([
                    ft.TextField(label="نام و نام خانوادگی", text_align=ft.TextAlign.RIGHT),
                    ft.TextField(label="نام پدر", text_align=ft.TextAlign.RIGHT),
                    ft.TextField(label="تاریخ تولد", text_align=ft.TextAlign.RIGHT),
                    ft.TextField(label="شماره شناسنامه", text_align=ft.TextAlign.RIGHT),
                    ft.TextField(label="شماره ملی", text_align=ft.TextAlign.RIGHT),
                    ft.Dropdown(
                        label="نوع درخواست",
                        options=[
                            ft.dropdown.Option("نماینده فروش"),
                            ft.dropdown.Option("عامل فروش"),
                            ft.dropdown.Option("کارشناس فروش"),
                            ft.dropdown.Option("نصاب فنی"),
                        ],
                        width=340
                    ),
                    ft.TextField(
                        label="معرفی نامه",
                        value="اینجانب ....................... آقا/خانم ....................... را جهت همکار طبق قوانین و شرایط شرکت معرفی می کنم",
                        multiline=True,
                        min_lines=3,
                        text_align=ft.TextAlign.RIGHT
                    ),
                ], scroll=ft.ScrollMode.AUTO, spacing=12),
                width=380,
                height=520,
                padding=10
            ),
            actions=[
                ft.TextButton("انصراف", on_click=lambda _: (setattr(dlg, 'open', False), page.update())),
                ft.ElevatedButton("تایید و ارسال درخواست", bgcolor="#1565C0", color="white", on_click=lambda _: (show_message("درخواست با موفقیت ارسال شد", "green"), setattr(dlg, 'open', False), page.update()))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # ==================== مشتریان منتخب ====================
    def open_selected_customers_dialog(e):
        dlg = ft.AlertDialog(
            title=ft.Text("مشتریان منتخب", size=18, weight="bold"),
            content=ft.Container(
                content=ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("کد مشتری")),
                        ft.DataColumn(ft.Text("نام و نام خانوادگی / مجموعه")),
                        ft.DataColumn(ft.Text("شماره تماس")),
                        ft.DataColumn(ft.Text("شهر")),
                    ],
                    rows=[
                        ft.DataRow(cells=[ft.DataCell(ft.Text("C1001")), ft.DataCell(ft.Text("شرکت آریا تهویه")), ft.DataCell(ft.Text("09123456789")), ft.DataCell(ft.Text("تهران"))]),
                        ft.DataRow(cells=[ft.DataCell(ft.Text("C1002")), ft.DataCell(ft.Text("مهندس رضایی")), ft.DataCell(ft.Text("09129876543")), ft.DataCell(ft.Text("اصفهان"))]),
                    ]
                ),
                width=380,
                height=400,
                padding=10
            ),
            actions=[ft.TextButton("بستن", on_click=lambda _: (setattr(dlg, 'open', False), page.update()))]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # ==================== اعلام موجودی انبار ====================
    def open_inventory_dialog(e):
        items = []

        def add_item(e):
            if product.value and quantity.value:
                items.append((product.value, dimension.value or "-", quantity.value))
                refresh_list()
                product.value = ""
                dimension.value = ""
                quantity.value = ""
                page.update()

        def refresh_list():
            inventory_list.controls.clear()
            for p, d, q in items:
                inventory_list.controls.append(
                    ft.ListTile(title=ft.Text(f"{p} | {d} | تعداد: {q}"))
                )

        def submit_inventory(e):
            if items:
                show_message(f"موجودی انبار با {len(items)} ردیف ثبت و PDF تولید شد", "green")
                dlg.open = False
            else:
                show_message("ابتدا حداقل یک محصول اضافه کنید", "red")
            page.update()

        product = ft.TextField(label="نام محصول", width=340)
        dimension = ft.TextField(label="ابعاد محصول", width=340)
        quantity = ft.TextField(label="تعداد موجودی", width=340, keyboard_type=ft.KeyboardType.NUMBER)

        inventory_list = ft.Column(scroll=ft.ScrollMode.AUTO, height=200)

        dlg = ft.AlertDialog(
            title=ft.Text("اعلام موجودی انبار", size=18, weight="bold"),
            content=ft.Container(
                content=ft.Column([
                    product,
                    dimension,
                    quantity,
                    ft.ElevatedButton("اضافه کردن به لیست", on_click=add_item),
                    ft.Divider(),
                    ft.Text("لیست موجودی اعلام شده:"),
                    inventory_list,
                ], scroll=ft.ScrollMode.AUTO, spacing=10),
                width=380,
                height=520,
                padding=10
            ),
            actions=[
                ft.TextButton("انصراف", on_click=lambda _: (setattr(dlg, 'open', False), page.update())),
                ft.ElevatedButton("تایید و تولید PDF", bgcolor="#1565C0", color="white", on_click=submit_inventory)
            ]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # ==================== صفحه پروفایل ====================
    def profile_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.CircleAvatar(foreground_image_src="https://i.pravatar.cc/150?u=reza", radius=48),
                        ft.Text("نام و نام خانوادگی | نام کاربری", size=20, weight="bold", text_align=ft.TextAlign.CENTER),
                        ft.Text("شماره موبایل", size=16, color="grey", text_align=ft.TextAlign.CENTER),
                        ft.Container(
                            content=ft.Text(f"سطح دسترسی: {page.session.user_role}", size=15, color="blue", text_align=ft.TextAlign.CENTER),
                            bgcolor="#f0f0f0", padding=12, border_radius=12, margin=ft.margin.Margin(top=12, bottom=8)
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20, bgcolor="#f8f9fa", border_radius=20, margin=ft.margin.Margin(bottom=20), width=380
                ),
                ft.Container(
                    content=ft.Column([
                        ft.ListTile(leading=ft.Icon(ft.Icons.PERSON_ADD, color="blue"), title=ft.Text("درخواست ایجاد حساب"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=open_create_account_dialog),
                        ft.ListTile(leading=ft.Icon(ft.Icons.STAR, color="orange"), title=ft.Text("مشتریان منتخب"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=open_selected_customers_dialog),
                        ft.ListTile(leading=ft.Icon(ft.Icons.WAREHOUSE, color="green"), title=ft.Text("اعلام موجودی انبار"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=open_inventory_dialog),
                        ft.ListTile(leading=ft.Icon(ft.Icons.SHOPPING_CART), title=ft.Text("ثبت درخواست خرید"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                        ft.ListTile(leading=ft.Icon(ft.Icons.GROUP), title=ft.Text("همکاران منتخب"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                        ft.ListTile(leading=ft.Icon(ft.Icons.PERCENT), title=ft.Text("محاسبه درصد همکاری"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                        ft.ListTile(leading=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET), title=ft.Text("مبلغ اعتبار"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                        ft.Divider(height=25),
                        ft.ListTile(leading=ft.Icon(ft.Icons.PALETTE, color="purple"), title=ft.Text("نمایش (تم روشن/تیره)"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=toggle_theme),
                        ft.ListTile(leading=ft.Icon(ft.Icons.UPDATE, color="blue"), title=ft.Text("بروزرسانی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                        ft.ListTile(leading=ft.Icon(ft.Icons.MAP, color="green"), title=ft.Text("شبکه فروش و خدمات"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                        ft.ListTile(leading=ft.Icon(ft.Icons.GAVEL, color="amber"), title=ft.Text("قوانین"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                        ft.ListTile(leading=ft.Icon(ft.Icons.INFO, color="blue"), title=ft.Text("درباره ما"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)),
                        ft.Divider(height=25),
                        ft.ListTile(leading=ft.Icon(ft.Icons.SETTINGS, color="grey"), title=ft.Text("تنظیمات"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(5)),
                        ft.ListTile(leading=ft.Icon(ft.Icons.LOGOUT, color="red"), title=ft.Text("خروج", color="red"), on_click=lambda e: (setattr(page.session, 'logged_in', False), render())),
                        ft.Text("نسخه ۱.۴.۳", size=12, color="grey", text_align=ft.TextAlign.CENTER)
                    ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    width=360
                )
            ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400,
            margin=ft.margin.Margin(left=15, right=15),
            expand=True
        )

    # ==================== بقیه صفحات (خلاصه) ====================
    def home_page():
        return ft.Container(...)  # همان کد قبلی شما

    def technical_page():
        return ft.Container(...)  # همان کد قبلی شما

    def settings_page():
        return ft.Container(...)  # همان کد قبلی شما

    # ==================== رندر اصلی ====================
    def render(tab_index=0):
        page.controls.clear()
        if not page.session.logged_in:
            # صفحه لاگین شما
            page.add(...)  # همان کد لاگین قبلی
        else:
            contents = [
                ft.Text("داشبورد مدیریتی", size=18, weight="bold"),
                pre_invoice_page(),
                home_page(),
                technical_page(),
                profile_page(),
                settings_page()
            ]
            # ... بقیه کد رندر (همان قبلی)

        page.update()

    render()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
