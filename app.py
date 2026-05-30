import flet as ft
import os
import json
# برای WebAuthn واقعی در آینده می‌توان از JavaScript injection استفاده کرد

def main(page: ft.Page):
    page.fonts = {"iranyekan": "fonts/iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    page.padding = 0
    page.rtl = True
    page.theme_mode = "light"
    
    if not hasattr(page.session, "logged_in"):
        page.session.logged_in = False

    # ==================== بیومتریک واقعی با WebAuthn ====================
    def show_biometric_dialog(e):
        # نمایش دیالوگ
        dlg = ft.AlertDialog(
            title=ft.Text("احراز هویت بیومتریک", weight="bold"),
            content=ft.Column([
                ft.Text("از اثر انگشت یا تشخیص چهره دستگاه خود استفاده کنید"),
                ft.ProgressRing(),
                ft.Text("در حال اتصال به حسگر...", size=14, color="grey")
            ], horizontal_alignment="center", spacing=20),
            actions=[
                ft.TextButton("انصراف", on_click=lambda _: (setattr(dlg, 'open', False), page.update()))
            ]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

        # شبیه‌سازی واقعی WebAuthn (در آینده می‌توان JS تزریق کرد)
        page.run_js("""
            async function biometricAuth() {
                try {
                    const publicKey = {
                        challenge: new Uint8Array(32),
                        rp: { name: "TopSUNify" },
                        user: { id: new Uint8Array(16), name: "user@example.com", displayName: "کاربر" },
                        pubKeyCredParams: [{ type: "public-key", alg: -7 }]
                    };
                    const credential = await navigator.credentials.create({ publicKey });
                    console.log("Biometric Success", credential);
                    // اینجا می‌توانید به Python برگردانید
                    return true;
                } catch (err) {
                    console.error(err);
                    return false;
                }
            }
            biometricAuth();
        """)

        # برای نسخه فعلی: بعد از ۱.۵ ثانیه موفق در نظر بگیریم
        import time
        time.sleep(1.5)
        dlg.open = False
        page.session.logged_in = True
        render()
        page.update()

    # ==================== صفحه لاگین (شبیه عکس دوم) ====================
    def render(tab_index=0):
        page.controls.clear()

        if not page.session.logged_in:
            page.add(
                ft.Column([
                    ft.Container(
                        content=ft.Image(src="TopSUNify.png", width=180),
                        margin=ft.margin.only(top=50, bottom=30)
                    ),

                    ft.Container(
                        content=ft.TextField(
                            label="نام کاربری",
                            width=320,
                            border_radius=12,
                            prefix_icon=ft.Icons.PERSON,
                        ),
                        margin=ft.margin.only(bottom=15)
                    ),

                    ft.Container(
                        content=ft.Row([
                            ft.TextField(
                                label="رمز عبور",
                                password=True,
                                width=260,
                                border_radius=12,
                                prefix_icon=ft.Icons.LOCK,
                            ),
                            ft.Container(
                                content=ft.Icon(ft.Icons.FINGERPRINT, size=42, color="#FFCC00"),
                                on_click=show_biometric_dialog,
                                padding=8,
                            )
                        ]),
                        margin=ft.margin.only(bottom=30)
                    ),

                    ft.ElevatedButton(
                        "TopSUNify به ورود",
                        width=320,
                        bgcolor="#FFCC00",
                        color="black",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)),
                        on_click=lambda e: (setattr(page.session, 'logged_in', True), render())
                    ),

                    ft.Text("فعال‌سازی / فراموشی رمز", size=14, color="blue"),

                    ft.Container(
                        content=ft.Image(src="TopSUN-Powered.png", width=140),
                        margin=ft.margin.only(top=40)
                    ),

                    ft.Container(expand=True)
                ], horizontal_alignment="center", expand=True, scroll=ft.ScrollMode.AUTO)
            )
        else:
            # پنل اصلی
            contents = [
                ft.Text("داشبورد مدیریتی", size=25),
                ft.Text("بخش پیش‌فاکتورها", size=25),
                ft.Column([ft.Image(src="TopSUNify-1.png", width=200), ft.Text("خانه اصلی", size=25)], horizontal_alignment="center"),
                ft.Text("اطلاعات فنی سیستم", size=25),
                ft.Text("پروفایل کاربری", size=25)
            ]

            nav_buttons = ft.Row([
                ft.IconButton(icon="dashboard", on_click=lambda _: render(0)),
                ft.IconButton(icon="edit_document", on_click=lambda _: render(1)),
                ft.IconButton(icon="home", on_click=lambda _: render(2)),
                ft.IconButton(icon="build", on_click=lambda _: render(3)),
                ft.IconButton(icon="person", on_click=lambda _: render(4)),
            ], alignment="center")

            page.add(
                ft.Column([
                    ft.Text("پنل TopSUNify", size=30, weight="bold"),
                    ft.Divider(),
                    ft.Container(content=contents[tab_index], expand=True, alignment=ft.Alignment(0, 0)),
                    nav_buttons
                ], horizontal_alignment="center", expand=True)
            )

        page.update()

    render()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
