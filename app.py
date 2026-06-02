import flet as ft
import os

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
        page.session.username = "رضا تلچی"
        page.session.inventory_list = []

    def show_message(text: str, color="green"):
        snack = ft.SnackBar(content=ft.Text(text), bgcolor=color, action="بستن", duration=3000)
        page.snack_bar = snack
        snack.open = True
        page.update()

    def toggle_theme(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()
        show_message(f"تم تغییر کرد به: {page.theme_mode}", "blue")

    # ==================== صفحه اعلام موجودی انبار ====================
    def inventory_page():
        product_data = {
            "گرمایش زیرفرشی": ["طول 1/2 متر", "طول 1/5 متر", "2 ردیف با طول 2 متر"],
            "رادیاتور": ["سایز 50×50 سانت", "سایز 50×90 سانت", "سایز 50×110 سانت", "سایز 50×150 سانت",
                         "سایز 60×60 سانت", "سایز 60×80 سانت", "سایز 90×90 سانت", "سایز 90×110 سانت",
                         "سایز 90×150 سانت", "سایز 90×200 سانت"],
            "عایق بازتابشی": ["3 مترمربع", "6 متر مربع"]
        }

        product_name = ft.Dropdown(
            label="نام محصول",
            options=[ft.dropdown.Option(k) for k in product_data.keys()],
            width=350,
        )

        product_size = ft.Dropdown(label="ابعاد محصول", width=350)
        product_qty = ft.TextField(label="تعداد", width=100, keyboard_type=ft.KeyboardType.NUMBER)

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("نام")),
                ft.DataColumn(ft.Text("ابعاد")),
                ft.DataColumn(ft.Text("تعداد")),
                ft.DataColumn(ft.Text("حذف"))
            ],
            rows=[]
        )

        def update_sizes(e):
            if product_name.value:
                selected = product_name.value
                product_size.options = [ft.dropdown.Option(s) for s in product_data.get(selected, [])]
                product_size.value = None
                product_size.update()
            page.update()

        product_name.on_change = update_sizes

        def delete_row(row):
            table.rows.remove(row)
            page.update()

        def add_to_table(e):
            if product_name.value and product_size.value and product_qty.value:
                new_row = ft.DataRow(cells=[
                    ft.DataCell(ft.Text(product_name.value)),
                    ft.DataCell(ft.Text(product_size.value)),
                    ft.DataCell(ft.Text(product_qty.value)),
                    ft.DataCell(ft.IconButton(ft.Icons.DELETE, icon_color="red", 
                                            on_click=lambda _, r=new_row: delete_row(r)))
                ])
                table.rows.append(new_row)
                product_qty.value = ""
                page.update()
            else:
                show_message("لطفاً همه موارد را پر کنید", "red")

        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)),
                        ft.Text("اعلام موجودی انبار", size=20, weight="bold")
                    ]),
                    padding=10
                ),
                product_name,
                product_size,
                product_qty,
                ft.ElevatedButton("افزودن به لیست", on_click=add_to_table, bgcolor="green", color="white", width=350),
                ft.Divider(),
                table,
                ft.ElevatedButton("اعلام کل موجودی", on_click=lambda e: show_message("موجودی با موفقیت اعلام شد"), bgcolor="blue", color="white", width=350)
            ], scroll=ft.ScrollMode.AUTO, spacing=15),
            width=400,
            expand=True,
            padding=15
        )

    # ==================== صفحات دیگر (خلاصه) ====================
    def selected_customers_page():
        return ft.Container(content=ft.Text("مشتریان منتخب", size=24, weight="bold"), expand=True, alignment=ft.Alignment(0.5, 0.5))

    def account_request_page():
        return ft.Container(content=ft.Text("فرم درخواست همکاری", size=24, weight="bold"), expand=True, alignment=ft.Alignment(0.5, 0.5))

    def pre_invoice_page():
        # کد قبلی شما
        products = ["گرمایش از کف", "زیرفرشی", "رادیاتور", "حوله خشک کن", "یخ زدایی رمپ", "یخ زدایی پله", "گرمکن مخزن", "گرمکن صندلی", "رستورانی", "عایق بازتابشی"]
        grid = ft.GridView(runs_count=2, max_extent=120, spacing=10, run_spacing=12, padding=10, expand=True)
        for name in products:
            grid.controls.append(ft.Container(
                content=ft.Text(name, size=15, weight="bold", text_align=ft.TextAlign.CENTER, color="#1565C0"),
                width=170, height=70, bgcolor="#ffffff", border_radius=12,
                alignment=ft.Alignment(0, 0),
                on_click=lambda e, n=name: show_message(f"پیش‌فاکتور {n}"), ink=True
            ))
        return ft.Container(
            content=ft.Column([
                ft.Text("نوع محصول مورد نظر را انتخاب کنید", size=18, weight="bold", text_align=ft.TextAlign.CENTER),
                ft.Divider(height=10), grid
            ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, margin=ft.margin.Margin(left=15, right=15), expand=True
        )

    def home_page():
        return ft.Container(content=ft.Text("خانه اصلی", size=24, weight="bold"), expand=True, alignment=ft.Alignment(0.5, 0.5))

    def technical_page():
        return ft.Container(content=ft.Text("اطلاعات فنی", size=24, weight="bold"), expand=True, alignment=ft.Alignment(0.5, 0.5))

    def settings_page():
        return ft.Container(content=ft.Text("تنظیمات", size=24, weight="bold"), expand=True, alignment=ft.Alignment(0.5, 0.5))

    def profile_page():
        # کد قبلی شما (بدون تغییر)
        return ft.Container(content=ft.Text("پروفایل", size=24, weight="bold"), expand=True, alignment=ft.Alignment(0.5, 0.5))

    def dashboard_page():
        # کد قبلی شما (بدون تغییر)
        return ft.Container(content=ft.Text("داشبورد", size=24, weight="bold"), expand=True, alignment=ft.Alignment(0.5, 0.5))

    # ==================== رندر ====================
    def render(tab_index=0):
        page.controls.clear()

        if not page.session.logged_in:
            # صفحه ورود
            page.add(
                ft.Container(
                    content=ft.Column([
                        ft.Container(content=ft.Image(src="TopSUNify.png", width=190), margin=ft.margin.Margin(top=40, bottom=40)),
                        ft.Container(content=ft.TextField(label="نام کاربری", width=340, border_radius=12, prefix_icon=ft.Icons.PERSON, text_align=ft.TextAlign.RIGHT), margin=ft.margin.Margin(bottom=20)),
                        ft.Container(
                            content=ft.Row([
                                ft.Container(content=ft.Icon(ft.Icons.FINGERPRINT, size=42, color="#FFCC00"), on_click=lambda e: show_message("احراز هویت بیومتریک", "orange"), padding=10, border_radius=12),
                                ft.TextField(label="رمز عبور", password=True, width=270, border_radius=12, prefix_icon=ft.Icons.LOCK, text_align=ft.TextAlign.RIGHT)
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=12),
                            margin=ft.margin.Margin(bottom=30)
                        ),
                        ft.ElevatedButton("ورود به TopSUNify", width=340, bgcolor="#FFCC00", color="black", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)), on_click=lambda e: (setattr(page.session, 'logged_in', True), render())),
                        ft.TextButton("فعال‌سازی / فراموشی رمز", style=ft.ButtonStyle(color={"": "blue"})),
                        ft.Container(content=ft.Image(src="TopSUN-Powered.png", width=160), margin=ft.margin.Margin(top=50, bottom=30)),
                        ft.Container(content=ft.Image(src="landscape.jpg", width=400, height=220, fit="cover"), expand=True)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
                    width=400,
                    margin=ft.margin.Margin(left=15, right=15),
                    expand=True
                )
            )
        else:
            contents = [
                dashboard_page(),
                pre_invoice_page(),
                home_page(),
                technical_page(),
                profile_page(),
                settings_page(),
                account_request_page(),
                selected_customers_page(),
                inventory_page()
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
                bgcolor="white", padding=12,
                border=ft.Border(top=ft.BorderSide(1, "#e0e0e0"), bottom=ft.BorderSide(1, "#e0e0e0"))
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

    render()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
