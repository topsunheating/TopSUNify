import flet as ft
import os
import requests

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

    def toggle_theme(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()

    account_dlg = ft.AlertDialog(
        title=ft.Text("درخواست ایجاد حساب همکاری", text_align=ft.TextAlign.CENTER),
        content=ft.Container(
            content=ft.Column([
                ft.TextField(label="نام و نام خانوادگی", text_align=ft.TextAlign.RIGHT),
                ft.TextField(label="نام پدر", text_align=ft.TextAlign.RIGHT),
                ft.TextField(label="تاریخ تولد", text_align=ft.TextAlign.RIGHT),
                ft.TextField(label="شماره شناسنامه", text_align=ft.TextAlign.RIGHT),
                ft.TextField(label="شماره ملی", text_align=ft.TextAlign.RIGHT),
                ft.Dropdown(label="نوع درخواست", options=[
                    ft.dropdown.Option("نماینده فروش"),
                    ft.dropdown.Option("عامل فروش"),
                    ft.dropdown.Option("کارشناس فروش"),
                    ft.dropdown.Option("نصاب فنی"),
                ]),
                ft.Text("اینجانب جهت همکاری طبق قوانین شرکت معرفی می‌کنم.", size=12, italic=True),
                ft.ElevatedButton("تایید درخواست", bgcolor="#1565C0", color="white", on_click=lambda e: show_message("درخواست با موفقیت ثبت شد")),
                ft.OutlinedButton("بازگشت به منوی اصلی", on_click=lambda e: (setattr(account_dlg, 'open', False), page.update())),
            ], scroll=ft.ScrollMode.AUTO, tight=True),
            width=350, height=500
        )
    )

    def open_account_request_dialog(e):
        page.dialog = account_dlg
        account_dlg.open = True
        page.update()

    def pre_invoice_page():
        products = ["گرمایش از کف", "زیرفرشی", "رادیاتور", "حوله خشک کن", "یخ زدایی رمپ", "یخ زدایی پله", "گرمکن مخزن", "گرمکن صندلی", "رستورانی", "عایق بازتابشی"]
        grid = ft.GridView(runs_count=2, max_extent=120, spacing=10, run_spacing=12, padding=10, expand=True)
        for name in products:
            # اصلاح تراز در اینجا
            grid.controls.append(ft.Container(content=ft.Text(name, size=15, weight="bold", text_align=ft.TextAlign.CENTER, color="#1565C0"), width=170, height=70, bgcolor="#ffffff", border_radius=12, alignment=ft.Alignment.CENTER, shadow=ft.BoxShadow(blur_radius=6, color="#e0e0e0"), on_click=lambda e, n=name: show_message(f"پیش‌فاکتور {n}"), ink=True))
        return ft.Container(content=ft.Column([ft.Text("نوع محصول مورد نظر را انتخاب کنید", size=18, weight="bold", text_align=ft.TextAlign.CENTER), ft.Divider(height=10), grid], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)

    def home_page():
        return ft.Container(content=ft.Column([ft.Container(content=ft.Column([ft.Image(src="TopSUNify-1.png", width=80), ft.Text("خوش آمدید به TopSUNify", size=18, weight="bold", text_align=ft.TextAlign.CENTER), ft.Text("مرکز خدمات و پشتیبانی", size=16, color="grey", text_align=ft.TextAlign.CENTER)], horizontal_alignment=ft.CrossAxisAlignment.CENTER), margin=ft.margin.Margin(top=20, bottom=30)), ft.Container(content=ft.Column([ft.ListTile(leading=ft.Icon(ft.Icons.SHIELD, color="green"), title=ft.Text("ثبت گارانتی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.INSTALL_DESKTOP, color="blue"), title=ft.Text("درخواست نصب اولیه"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.SUPPORT_AGENT, color="orange"), title=ft.Text("درخواست خدمات فنی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.SHOPPING_CART_CHECKOUT, color="purple"), title=ft.Text("ثبت درخواست سفارشی و عمده"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.PRINT, color="red"), title=ft.Text("درخواست چاپ طرح سفارشی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20))], spacing=2), width=380)], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)

    def technical_page():
        return ft.Container(content=ft.Column([ft.Container(content=ft.Text("اطلاعات فنی", size=18, weight="bold", text_align=ft.TextAlign.CENTER), padding=20, margin=ft.margin.Margin(bottom=15)), ft.Container(content=ft.Column([ft.ListTile(leading=ft.Icon(ft.Icons.BOOK, color="blue"), title=ft.Text("کاتالوگ محصولات"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.PRICE_CHANGE, color="green"), title=ft.Text("لیست قیمت"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.WORK_HISTORY, color="purple"), title=ft.Text("رزومه شرکت"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.DESCRIPTION, color="orange"), title=ft.Text("پروپوزال و گزارش فنی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.IMAGE, color="pink"), title=ft.Text("تصاویر و فیلم پروژه‌ها"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.VIDEO_LIBRARY, color="red"), title=ft.Text("فیلم‌های تبلیغاتی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20))], spacing=2), width=380)], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)

    def settings_page():
        return ft.Container(content=ft.Column([ft.Container(content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: render(4)), ft.Text("تنظیمات", size=24, weight="bold")]), padding=15, bgcolor="#f8f9fa", border_radius=20, margin=ft.margin.Margin(bottom=20)), ft.Column([ft.ListTile(leading=ft.Icon(ft.Icons.PERSON), title=ft.Text("تغییر نام کاربری"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.SAVE), title=ft.Text("ذخیره نام کاربری"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.FINGERPRINT), title=ft.Text("ورود با اثر انگشت"), trailing=ft.Switch(value=False)), ft.ListTile(leading=ft.Icon(ft.Icons.LOCK), title=ft.Text("تغییر رمز ورود"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.PHONE), title=ft.Text("تغییر شماره تلفن همراه"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.DEVICES), title=ft.Text("دستگاه‌های فعال"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.Divider(height=20), ft.ListTile(leading=ft.Icon(ft.Icons.DELETE_FOREVER, color="red"), title=ft.Text("حذف تنظیمات و خروج از نرم‌افزار", color="red"), on_click=lambda e: (setattr(page.session, 'logged_in', False), render()))], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER)]))

    def profile_page():
        return ft.Container(content=ft.Column([ft.Container(content=ft.Column([ft.CircleAvatar(foreground_image_src="https://i.pravatar.cc/150?u=reza", radius=48), ft.Text("نام و نام خانوادگی | نام کاربری", size=20, weight="bold", text_align=ft.TextAlign.CENTER), ft.Text("شماره موبایل", size=16, color="grey", text_align=ft.TextAlign.CENTER), ft.Container(content=ft.Text(f"سطح دسترسی: {page.session.user_role}", size=15, color="blue", text_align=ft.TextAlign.CENTER), bgcolor="#f0f0f0", padding=12, border_radius=12, margin=ft.margin.Margin(top=12, bottom=8))], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=20, bgcolor="#f8f9fa", border_radius=20, margin=ft.margin.Margin(bottom=20), width=380), ft.Container(content=ft.Column([ft.ListTile(leading=ft.Icon(ft.Icons.PERSON_ADD, color="blue"), title=ft.Text("درخواست ایجاد حساب"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=open_account_request_dialog), ft.ListTile(leading=ft.Icon(ft.Icons.STAR, color="orange"), title=ft.Text("مشتریان منتخب"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.WAREHOUSE, color="green"), title=ft.Text("اعلام موجودی انبار"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.SHOPPING_CART), title=ft.Text("ثبت درخواست خرید"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.GROUP), title=ft.Text("همکاران منتخب"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.PERCENT), title=ft.Text("محاسبه درصد همکاری"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET), title=ft.Text("مبلغ اعتبار"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.Divider(height=25), ft.ListTile(leading=ft.Icon(ft.Icons.PALETTE, color="purple"), title=ft.Text("نمایش (تم روشن/تیره)"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=toggle_theme), ft.ListTile(leading=ft.Icon(ft.Icons.UPDATE, color="blue"), title=ft.Text("بروزرسانی"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.MAP, color="green"), title=ft.Text("شبکه فروش و خدمات"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.GAVEL, color="amber"), title=ft.Text("قوانین"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.ListTile(leading=ft.Icon(ft.Icons.INFO, color="blue"), title=ft.Text("درباره ما"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)), ft.Divider(height=25), ft.ListTile(leading=ft.Icon(ft.Icons.SETTINGS, color="grey"), title=ft.Text("تنظیمات"), trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20), on_click=lambda e: render(5)), ft.ListTile(leading=ft.Icon(ft.Icons.LOGOUT, color="red"), title=ft.Text("خروج", color="red"), on_click=lambda e: (setattr(page.session, 'logged_in', False), render())), ft.Text("نسخه ۱.۴.۳", size=12, color="grey", text_align=ft.TextAlign.CENTER)], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=360)], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)

    def dashboard_page():
        selected_ref = ft.Ref[ft.Container]()
        def select_period(e, year, month_num):
            if selected_ref.current: selected_ref.current.bgcolor = "#f0f0f0"; selected_ref.current.update()
            e.control.bgcolor = "#1565C0"; selected_ref.current = e.control; e.control.update(); show_message(f"بازه انتخابی: {year}/{month_num}")
        years, months = ["1401", "1402", "1403", "1404", "1405", "1406", "1407"], ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        period_buttons = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=8, alignment=ft.MainAxisAlignment.CENTER)
        for year in years:
            for month_num in months:
                is_selected = (year == "1405" and month_num == "05")
                # اصلاح تراز در اینجا
                container = ft.Container(content=ft.Text(f"{year}/{month_num}", size=14, weight="bold", text_align=ft.TextAlign.CENTER), width=85, height=35, bgcolor="#1565C0" if is_selected else "#f0f0f0", border_radius=160, alignment=ft.Alignment.alignment = ft.Alignment.CENTER), on_click=lambda e, y=year, m=month_num: select_period(e, y, m))
                if is_selected: selected_ref.current = container
                period_buttons.controls.append(container)
        view_button = ft.ElevatedButton("مشاهده اطلاعات این بازه", width=250, bgcolor="#1565C0", color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)), on_click=lambda e: show_message("در حال بارگذاری گزارش‌های مالی و عملیاتی..."))
        report_cards = ft.GridView(runs_count=2, max_extent=120, spacing=10, run_spacing=12, padding=10, expand=True)
        cards_data = [("فاکتورهای تسویه شده", ft.Icons.CHECK_CIRCLE, "#1976D2"), ("فاکتورهای فروش", ft.Icons.SHOPPING_CART, "#388E3C"), ("پیش فاکتورها", ft.Icons.RECEIPT_LONG, "#1565C0"), ("پروژه‌های نصب شده", ft.Icons.HOME_WORK, "#7B1FA2"), ("فاکتورهای باز", ft.Icons.PENDING, "#F57C00")]
        for title, icon, color in cards_data: report_cards.controls.append(ft.Container(content=ft.Column([ft.Icon(icon, size=36, color=color), ft.Text(title, size=13.5, weight="bold", text_align=ft.TextAlign.CENTER)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8), bgcolor="white", border_radius=16, padding=14, shadow=ft.BoxShadow(blur_radius=8, color="#e0e0e0"), expand=True, on_click=lambda e, t=title: show_message(f"بخش {t}"), ink=True))
        return ft.Container(content=ft.Column([ft.Container(content=ft.Dropdown(value="رضا تلچی", options=[ft.dropdown.Option("رضا تلچی"), ft.dropdown.Option("زیرمجموعه فروش")], width=320, border_radius=30, bgcolor="white"), margin=ft.margin.Margin(bottom=15)), ft.Text("انتخاب بازه زمانی", size=17, weight="bold", text_align=ft.TextAlign.CENTER), period_buttons, ft.Divider(height=10), view_button, ft.Divider(height=20), ft.Text("گزارش‌های مالی و عملیاتی", size=18, weight="bold", text_align=ft.TextAlign.CENTER), report_cards], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True)

    def render(tab_index=0):
        page.controls.clear()
        if not page.session.logged_in:
            page.add(ft.Container(content=ft.Column([ft.Container(content=ft.Image(src="TopSUNify.png", width=190), margin=ft.margin.Margin(top=40, bottom=40)), ft.Container(content=ft.TextField(label="نام کاربری", width=340, border_radius=12, prefix_icon=ft.Icons.PERSON, text_align=ft.TextAlign.RIGHT), margin=ft.margin.Margin(bottom=20)), ft.Container(content=ft.Row([ft.Container(content=ft.Icon(ft.Icons.FINGERPRINT, size=42, color="#FFCC00"), on_click=lambda e: show_message("احراز هویت بیومتریک", "orange"), padding=10, border_radius=12), ft.TextField(label="رمز عبور", password=True, width=270, border_radius=12, prefix_icon=ft.Icons.LOCK, text_align=ft.TextAlign.RIGHT)], alignment=ft.MainAxisAlignment.CENTER, spacing=12), margin=ft.margin.Margin(bottom=30)), ft.ElevatedButton("ورود به TopSUNify", width=340, bgcolor="#FFCC00", color="black", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)), on_click=lambda e: (setattr(page.session, 'logged_in', True), render())), ft.TextButton("فعال‌سازی / فراموشی رمز", style=ft.ButtonStyle(color={"": "blue"})), ft.Container(content=ft.Image(src="TopSUN-Powered.png", width=160), margin=ft.margin.Margin(top=50, bottom=30)), ft.Container(content=ft.Image(src="landscape.jpg", width=400, height=220, fit="cover"), expand=True)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO), width=400, margin=ft.margin.Margin(left=15, right=15), expand=True))
        else:
            contents = [dashboard_page(), pre_invoice_page(), home_page(), technical_page(), profile_page(), settings_page()]
            page.add(ft.Column([ft.Container(content=ft.Image(src="TopSUNify.png", width=80), margin=ft.margin.Margin(top=10, bottom=10)), ft.Divider(), ft.Container(content=contents[tab_index], expand=True, width=400, margin=ft.margin.Margin(left=15, right=15)), ft.Container(content=ft.Row([ft.Container(content=ft.Image(src="dashboard.png", width=32, height=32), on_click=lambda _: render(0), padding=8), ft.Container(content=ft.Image(src="invoice.png", width=32, height=32), on_click=lambda _: render(1), padding=8), ft.Container(content=ft.Image(src="TopSUNify-1.png", width=32, height=32), on_click=lambda _: render(2), padding=8), ft.Container(content=ft.Image(src="technical.png", width=32, height=32), on_click=lambda _: render(3), padding=8), ft.Container(content=ft.Image(src="profile.png", width=32, height=32), on_click=lambda _: render(4), padding=8)], alignment=ft.MainAxisAlignment.CENTER, spacing=15), bgcolor="white", padding=12)], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        page.update()

    render()

if __name__ == "__main__":
    ft.app(target=main, port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", assets_dir="assets")
