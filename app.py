import flet as ft
import os
import datetime

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
        page.session.inventory_list = []

    def show_message(text: str, color="green"):
        snack = ft.SnackBar(content=ft.Text(text), bgcolor=color, action="بستن", duration=3000)
        page.snack_bar = snack
        snack.open = True
        page.update()

    # ==================== صفحه گرمایش از کف ====================
    def floor_heating_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(1)),
                        ft.Text("گرمایش از کف (سیستم هوشمند)", size=20, weight="bold")
                    ]),
                    padding=10
                ),
                ft.Text("نوع روش صدور پیش‌فاکتور را انتخاب کنید:", size=18, weight="bold", text_align=ft.TextAlign.CENTER),
                ft.Divider(height=10),
                
                ft.ElevatedButton("📂 آپلود فایل DWG/DXF", width=350, bgcolor="#1565C0", color="white", 
                                 on_click=lambda e: show_message("در نسخه کامل: فایل آپلود و تحلیل می‌شود", "blue")),
                ft.ElevatedButton("⌨️ ورود دستی ابعاد اتاق‌ها", width=350, bgcolor="#1565C0", color="white", 
                                 on_click=lambda e: show_message("در نسخه کامل: ابعاد دستی وارد می‌شود", "blue")),
                ft.ElevatedButton("✍️ مقادیر مستقیم", width=350, bgcolor="#1565C0", color="white", 
                                 on_click=lambda e: show_message("پیش‌فاکتور مستقیم صادر شد", "green")),
            ], scroll=ft.ScrollMode.AUTO, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400, expand=True, padding=15
        )

    # ==================== صفحات اضافی ====================
    def account_request_page():
        return ft.Container(content=ft.Column([ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("فرم درخواست همکاری", size=20, weight="bold")]), padding=10), ft.TextField(label="نام و نام خانوادگی", text_align=ft.TextAlign.RIGHT), ft.TextField(label="نام پدر", text_align=ft.TextAlign.RIGHT), ft.TextField(label="تاریخ تولد", text_align=ft.TextAlign.RIGHT), ft.TextField(label="شماره شناسنامه", text_align=ft.TextAlign.RIGHT), ft.TextField(label="شماره ملی", text_align=ft.TextAlign.RIGHT), ft.Dropdown(label="نوع درخواست", options=[ft.dropdown.Option(i) for i in ["نماینده فروش","عامل فروش","کارشناس فروش","نصاب فنی"]]), ft.ElevatedButton("ثبت نهایی درخواست", bgcolor="#1565C0", color="white", on_click=lambda e: show_message("درخواست با موفقیت ثبت شد"))], scroll=ft.ScrollMode.AUTO), padding=20, width=400, expand=True)

    def inventory_page():
        # کد کامل شما (کوتاه شده برای خوانایی)
        product_data = {"گرمایش زیرفرشی": ["طول 1/2 متر"], "رادیاتور": ["سایز 50×50 سانت"]}
        # ... (بقیه کد inventory_page شما)
        return ft.Container(content=ft.Text("اعلام موجودی انبار"), width=400, expand=True)  # جایگزین موقتی

    def selected_customers_page():
        return ft.Container(content=ft.Text("مشتریان منتخب"), width=400, expand=True)

    def colleagues_page():
        return ft.Container(content=ft.Text("همکاران منتخب"), width=400, expand=True)

    def purchase_request_page():
        return ft.Container(content=ft.Text("ثبت درخواست خرید"), width=400, expand=True)

    def commission_page():
        return ft.Container(content=ft.Text("محاسبه درصد همکاری"), width=400, expand=True)

    def credit_page():
        return ft.Container(content=ft.Text("مبلغ اعتبار"), width=400, expand=True)

    def theme_page():
        return ft.Container(content=ft.Text("نمایش (تم)"), width=400, expand=True)

    def update_page():
        return ft.Container(content=ft.Text("بروزرسانی"), width=400, expand=True)

    def network_page():
        return ft.Container(content=ft.Text("شبکه فروش"), width=400, expand=True)

    def rules_page():
        return ft.Container(content=ft.Text("قوانین"), width=400, expand=True)

    def about_page():
        return ft.Container(content=ft.Text("درباره ما"), width=400, expand=True)

    def profile_page():
        return ft.Container(
            content=ft.Column([
                ft.Container(content=ft.Column([ft.CircleAvatar(foreground_image_src="https://i.pravatar.cc/150?u=reza", radius=48), ft.Text("نام و نام خانوادگی | نام کاربری", size=20, weight="bold", text_align=ft.TextAlign.CENTER)], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=20, bgcolor="#f8f9fa", border_radius=20),
                ft.Container(content=ft.Column([
                    ft.ListTile(leading=ft.Icon(ft.Icons.SHOPPING_CART, color="orange"), title=ft.Text("گرمایش از کف"), on_click=lambda e: render(18)),  # لینک به صفحه گرمایش
                    # بقیه گزینه‌ها...
                ], spacing=2), width=360)
            ], scroll=ft.ScrollMode.AUTO),
            width=400, expand=True, padding=15
        )

    # ==================== رندر اصلی ====================
    def render(tab_index=0):
        page.controls.clear()
        if not page.session.logged_in:
            # صفحه لاگین شما
            page.add(ft.Container(content=ft.Column([ft.Image(src="TopSUNify.png", width=190), ft.ElevatedButton("ورود به TopSUNify", on_click=lambda e: (setattr(page.session, 'logged_in', True), render()))], horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=400, expand=True))
        else:
            contents = [
                dashboard_page(), pre_invoice_page(), home_page(), technical_page(),
                profile_page(), settings_page(), account_request_page(),
                selected_customers_page(), inventory_page(), colleagues_page(),
                purchase_request_page(), commission_page(), credit_page(),
                theme_page(), update_page(), network_page(), rules_page(), about_page(),
                floor_heating_page()   # index 18
            ]
            main_content = ft.Container(content=contents[tab_index], expand=True, width=400, margin=ft.margin.Margin(left=15, right=15))
            nav_bar = ft.Container(content=ft.Row([ft.Image(src="invoice.png", width=32, on_click=lambda _: render(1))], alignment=ft.MainAxisAlignment.CENTER), bgcolor="white", padding=12)
            page.add(ft.Column([ft.Image(src="TopSUNify.png", width=80), main_content, nav_bar], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        page.update()

    # ==================== صفحات اصلی ====================
    def dashboard_page():
        return ft.Container(content=ft.Text("داشبورد", size=25), width=400, expand=True)

    def pre_invoice_page():
        products = [
            ("گرمایش از کف", lambda e: render(18)),
            ("زیرفرشی", lambda e: show_message("به زودی", "blue")),
            ("رادیاتور", lambda e: show_message("به زودی", "blue")),
        ]
        grid = ft.GridView(runs_count=2, max_extent=160, spacing=12, expand=True)
        for name, action in products:
            grid.controls.append(ft.Container(content=ft.Text(name, size=16, weight="bold"), width=170, height=100, bgcolor="white", border_radius=12, alignment=ft.Alignment(0,0), on_click=action, ink=True))
        return ft.Container(content=ft.Column([ft.Text("نوع محصول را انتخاب کنید", size=19, weight="bold"), grid], horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=400, expand=True, padding=15)

    def home_page():
        return ft.Container(content=ft.Text("خانه اصلی"), width=400, expand=True)

    def technical_page():
        return ft.Container(content=ft.Text("اطلاعات فنی"), width=400, expand=True)

    def settings_page():
        return ft.Container(content=ft.Text("تنظیمات"), width=400, expand=True)

    render()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
