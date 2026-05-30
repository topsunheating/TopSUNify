import flet as ft
import os
import time

def main(page: ft.Page):
    page.fonts = {"iranyekan": "fonts/iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    page.padding = 0
    page.rtl = True
    page.theme_mode = "light"
    
    if not hasattr(page.session, "logged_in"):
        page.session.logged_in = False

    # ==================== تابع بیومتریک واقعی با WebAuthn ====================
    def show_biometric_dialog(e):
        # نمایش دیالوگ
        dlg = ft.AlertDialog(
            title=ft.Text("احراز هویت بیومتریک", size=18, weight="bold"),
            content=ft.Column([
                ft.Text("در حال استفاده از حسگر دستگاه شما...", text_align="center"),
                ft.ProgressRing(width=65, height=65, stroke_width=7),
                ft.Text("لطفاً اثر انگشت یا چهره خود را تأیید کنید", size=14, color="grey", text_align="center")
            ], horizontal_alignment="center", spacing=20, height=220),
            actions=[
                ft.TextButton("انصراف", on_click=lambda _: (setattr(dlg, 'open', False), page.update()))
            ]
        )
        
        page.dialog = dlg
        dlg.open = True
        page.update()

        # اجرای WebAuthn واقعی از طریق JavaScript
        try:
            result = page.run_js("""
                async function startBiometricAuth() {
                    try {
                        // شبیه‌سازی challenge (در نسخه واقعی باید از سرور بگیرید)
                        const publicKey = {
                            challenge: new Uint8Array(32),
                            rp: { name: "TopSUNify" },
                            user: { 
                                id: new Uint8Array(16), 
                                name: "user@topSunify.com", 
                                displayName: "کاربر TopSUNify" 
                            },
                            pubKeyCredParams: [{ type: "public-key", alg: -7 }],
                            timeout: 60000,
                            authenticatorSelection: {
                                authenticatorAttachment: "platform",
                                userVerification: "required"
                            }
                        };
                        
                        const credential = await navigator.credentials.create({ publicKey });
                        console.log("✅ WebAuthn Success:", credential);
                        return "success";
                    } catch (err) {
                        console.error("WebAuthn Error:", err);
                        return "failed";
                    }
                }
                return await startBiometricAuth();
            """)
            
            if result == "success":
                time.sleep(0.5)
                dlg.open = False
                page.session.logged_in = True
                page.update()
                render()
            else:
                dlg.open = False
                page.show_snack_bar(ft.SnackBar(ft.Text("احراز هویت ناموفق بود. دوباره تلاش کنید."), open=True))
                page.update()
                
        except Exception as ex:
            dlg.open = False
            page.show_snack_bar(ft.SnackBar(ft.Text(f"خطا: {str(ex)}"), open=True))
            page.update()

    # ==================== صفحه لاگین ====================
    def render(tab_index=0):
        page.controls.clear()

        if not page.session.logged_in:
            page.add(
                ft.Column([
                    ft.Container(content=ft.Image(src="TopSUNify.png", width=190), margin=ft.margin.Margin(top=40, bottom=40)),

                    ft.Container(
                        content=ft.TextField(label="نام کاربری", width=340, border_radius=12, prefix_icon=ft.Icons.PERSON, text_align=ft.TextAlign.RIGHT),
                        margin=ft.margin.Margin(bottom=20)
                    ),

                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                content=ft.Icon(ft.Icons.FINGERPRINT, size=42, color="#FFCC00"),
                                on_click=show_biometric_dialog,
                                padding=10,
                                border_radius=12,
                                ink=True,
                                ink_color="#FFCC00"
                            ),
                            ft.TextField(
                                label="رمز عبور",
                                password=True,
                                width=270,
                                border_radius=12,
                                prefix_icon=ft.Icons.LOCK,
                                text_align=ft.TextAlign.RIGHT,
                            )
                        ], alignment="center", spacing=12, vertical_alignment="center"),
                        margin=ft.margin.Margin(bottom=30)
                    ),

                    ft.ElevatedButton(
                        "ورود به TopSUNify",
                        width=340,
                        bgcolor="#FFCC00",
                        color="black",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)),
                        on_click=lambda e: (setattr(page.session, 'logged_in', True), render())
                    ),

                    ft.Text("فعال‌سازی / فراموشی رمز", size=14, color="blue", text_align="center"),

                    ft.Container(content=ft.Image(src="TopSUN-Powered.png", width=160), margin=ft.margin.Margin(top=50, bottom=30)),

                    ft.Container(expand=True, content=ft.Image(src="landscape.jpg", width=400, height=220, fit="cover"))
                ], horizontal_alignment="center", expand=True, scroll=ft.ScrollMode.AUTO)
            )
        else:
            # داشبورد
            contents = [ft.Text(f"صفحه {i}", size=25) for i in range(5)]
            nav_buttons = ft.Row([ft.IconButton(icon=icon, on_click=lambda _, i=i: render(i)) 
                                for i, icon in enumerate(["dashboard", "edit_document", "home", "build", "person"])], alignment="center")

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
