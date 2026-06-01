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

    # ==================== دیالوگ‌ها ====================
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
                    ft.Dropdown(label="نوع درخواست", options=[ft.dropdown.Option(i) for i in ["نماینده فروش","عامل فروش","کارشناس فروش","نصاب فنی"]], width=340),
                    ft.TextField(label="معرفی نامه", value="اینجانب ....................... آقا/خانم ....................... را جهت همکار طبق قوانین و شرایط شرکت معرفی می کنم", multiline=True, min_lines=3, text_align=ft.TextAlign.RIGHT),
                ], scroll=ft.ScrollMode.AUTO, spacing=12),
                width=380, height=520, padding=10
            ),
            actions=[
                ft.TextButton("بازگشت", on_click=lambda _: (setattr(dlg, 'open', False), page.update())),
                ft.ElevatedButton("تایید و ارسال درخواست", bgcolor="#1565C0", color="white", on_click=lambda _: (show_message("درخواست ارسال شد", "green"), setattr(dlg, 'open', False), page.update()))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def open_selected_customers_dialog(e):
        dlg = ft.AlertDialog(
            title=ft.Text("مشتریان منتخب", size=18, weight="bold"),
            content=ft.Container(
                content=ft.DataTable(
                    columns=[ft.DataColumn(ft.Text("کد مشتری")), ft.DataColumn(ft.Text("نام و نام خانوادگی / مجموعه")), ft.DataColumn(ft.Text("شماره تماس")), ft.DataColumn(ft.Text("شهر"))],
                    rows=[
                        ft.DataRow(cells=[ft.DataCell(ft.Text(x)) for x in ["C1001","شرکت آریا تهویه","09123456789","تهران"]]),
                        ft.DataRow(cells=[ft.DataCell(ft.Text(x)) for x in ["C1002","مهندس رضایی","09129876543","اصفهان"]])
                    ]
                ),
                width=380, height=400, padding=10
            ),
            actions=[ft.TextButton("بازگشت", on_click=lambda _: (setattr(dlg, 'open', False), page.update()))]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def open_inventory_dialog(e):
        items = []
        product = ft.TextField(label="نام محصول", width=340)
        dimension = ft.TextField(label="ابعاد محصول", width=340)
        quantity = ft.TextField(label="تعداد موجودی", width=340, keyboard_type=ft.KeyboardType.NUMBER)
        inventory_list = ft.Column(scroll=ft.ScrollMode.AUTO, height=200)

        def add_item(e):
            if product.value and quantity.value:
                items.append((product.value, dimension.value or "-", quantity.value))
                refresh_list()
                product.value = dimension.value = quantity.value = ""
                page.update()

        def refresh_list():
            inventory_list.controls.clear()
            for p, d, q in items:
                inventory_list.controls.append(ft.ListTile(title=ft.Text(f"{p} | {d} | تعداد: {q}")))

        def submit_inventory(e):
            if items:
                show_message(f"موجودی انبار با {len(items)} ردیف ثبت شد", "green")
                dlg.open = False
            else:
                show_message("حداقل یک محصول اضافه کنید", "red")
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("اعلام موجودی انبار", size=18, weight="bold"),
            content=ft.Container(
                content=ft.Column([product, dimension, quantity, ft.ElevatedButton("اضافه کردن به لیست", on_click=add_item), ft.Divider(), ft.Text("لیست موجودی:"), inventory_list], scroll=ft.ScrollMode.AUTO, spacing=10),
                width=380, height=520, padding=10
            ),
            actions=[
                ft.TextButton("بازگشت", on_click=lambda _: (setattr(dlg, 'open', False), page.update())),
                ft.ElevatedButton("تایید و تولید PDF", bgcolor="#1565C0", color="white", on_click=submit_inventory)
            ]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # ==================== صفحات ====================
    def dashboard_page():
        return ft.Container(content=ft.Text("داشبورد مدیریتی", size=25, weight="bold"), expand=True, width=400)

    def pre_invoice_page():
        products = ["گرمایش از کف", "زیرفرشی", "رادیاتور", "حوله خشک کن", "یخ زدایی رمپ", "یخ زدایی پله", "گرمکن مخزن", "گرمکن صندلی", "رستورانی"]
        grid = ft.GridView(runs_count=2, max_extent=160, spacing=12, run_spacing=12, padding=15, expand=True)
        for name in products:
            grid.controls.append(ft.Container(content=ft.Text(name, size=15, weight="bold", text_align=ft.TextAlign.CENTER, color="#1565C0"), width=170, height=70, bgcolor="#ffffff", border_radius=12, alignment=ft.Alignment(0,0), on_click=lambda e, n=name: show_message(f"پیش‌فاکتور {n}"), ink=True))
        return ft.Container(content=ft.Column([ft.Text("نوع محصول مورد نظر را انتخاب کنید", size=18, weight="bold"), grid], scroll=ft.ScrollMode.AUTO), width=400, expand=True, margin=ft.margin.Margin(left=15, right=15))

    def home_page():
        return ft.Container(content=ft.Text("خانه اصلی", size=25, weight="bold"), expand=True, width=400)

    def technical_page():
        return ft.Container(content=ft.Text("اطلاعات فنی سیستم", size=25, weight="bold"), expand=True, width=400)

    def settings_page():
        return ft.Container(content=ft.Text("تنظیمات", size=25, weight="bold"), expand=True, width=400)

    def profile_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Column([ft.CircleAvatar(foreground_image_src="https://i.pravatar.cc/150?u=reza", radius=48), ft.Text("نام و نام خانوادگی | نام کاربری", size=20, weight="bold", text_align=ft.TextAlign.CENTER), ft.Text("شماره موبایل", size=16, color="grey", text_align=ft.TextAlign.CENTER), ft.Container(content=ft.Text(f"سطح دسترسی: {page.session.user_role}", size=15, color="blue"), bgcolor="#f0f0f0", padding=12, border_radius=12)], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=20, bgcolor="#f8f9fa", border_radius=20, margin=ft.margin.Margin(bottom=20), width=380),
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
            width=400, margin=ft.margin.Margin(left=15, right=15), expand=True
        )

    # ==================== رندر اصلی ====================
    def render(tab_index=0):
        page.controls.clear()

        if not page.session.logged_in:
            # صفحه لاگین
            page.add(
                ft.Container(
                    content=ft.Column([
                        ft.Container(content=ft.Image(src="TopSUNify.png", width=190), margin=ft.margin.Margin(top=40, bottom=40)),
                        ft.Container(content=ft.TextField(label="نام کاربری", width=340, border_radius=12, prefix_icon=ft.Icons.PERSON, text_align=ft.TextAlign.RIGHT), margin=ft.margin.Margin(bottom=20)),
                        ft.Container(content=ft.Row([ft.Container(content=ft.Icon(ft.Icons.FINGERPRINT, size=42, color="#FFCC00"), on_click=lambda e: show_message("احراز هویت بیومتریک", "orange"), padding=10, border_radius=12), ft.TextField(label="رمز عبور", password=True, width=270, border_radius=12, prefix_icon=ft.Icons.LOCK, text_align=ft.TextAlign.RIGHT)], alignment=ft.MainAxisAlignment.CENTER, spacing=12), margin=ft.margin.Margin(bottom=30)),
                        ft.ElevatedButton("ورود به TopSUNify", width=340, bgcolor="#FFCC00", color="black", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)), on_click=lambda e: (setattr(page.session, 'logged_in', True), render())),
                        ft.TextButton("فعال‌سازی / فراموشی رمز", style=ft.ButtonStyle(color={"": "blue"})),
                        ft.Container(content=ft.Image(src="TopSUN-Powered.png", width=160), margin=ft.margin.Margin(top=50, bottom=30)),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
                    width=400, margin=ft.margin.Margin(left=15, right=15), expand=True
                )
            )
        else:
            contents = [
                dashboard_page(),   # 0
                pre_invoice_page(), # 1
                home_page(),        # 2
                technical_page(),   # 3
                profile_page(),     # 4
                settings_page()     # 5
            ]
            main_content = ft.Container(content=contents[tab_index], expand=True, width=400, margin=ft.margin.Margin(left=15, right=15))
            nav_bar = ft.Container(
                content=ft.Row([
                    ft.Container(content=ft.Image(src="dashboard.png", width=32, height=32), on_click=lambda _: render(0), padding=8),
                    ft.Container(content=ft.Image(src="invoice.png", width=32, height=32), on_click=lambda _: render(1), padding=8),
                    ft.Container(content=ft.Image(src="TopSUNify-1.png", width=32, height=32), on_click=lambda _: render(2), padding=8),
                    ft.Container(content=ft.Image(src="technical.png", width=32, height=32), on_click=lambda _: render(3), padding=8),
                    ft.Container(content=ft.Image(src="profile.png", width=32, height=32), on_click=lambda _: render(4), padding=8),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                bgcolor="white", padding=12
            )
            page.add(
                ft.Column([
                    ft.Container(content=ft.Image(src="TopSUNify.png", width=80), margin=ft.margin.Margin(top=10, bottom=10)),
                    ft.Divider(),
                    main_content,
                    nav_bar
                ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
        page.update()

    # ==================== صفحات ساده ====================
    def home_page():
        return ft.Container(content=ft.Text("خانه اصلی", size=25, weight="bold"), expand=True, width=400)

    def technical_page():
        return ft.Container(content=ft.Text("اطلاعات فنی سیستم", size=25, weight="bold"), expand=True, width=400)

    def settings_page():
        return ft.Container(content=ft.Text("تنظیمات", size=25, weight="bold"), expand=True, width=400)

    render()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
