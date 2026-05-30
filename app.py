import flet as ft
import os
import time
import uuid
from webauthn import (
    generate_registration_options,
    verify_registration_response,
    generate_authentication_options,
    verify_authentication_response,
    options_to_json,
)
from webauthn.helpers import bytes_to_base64url
from webauthn.helpers.structs import (
    PublicKeyCredentialCreationOptions,
    PublicKeyCredentialRequestOptions,
)

# ذخیره‌سازی ساده (در RAM) — برای تست
users = {}  # username -> {"id": bytes, "credentials": list}

def main(page: ft.Page):
    page.fonts = {"iranyekan": "fonts/iranyekan.ttf"}
    page.theme = ft.Theme(font_family="iranyekan")
    page.padding = 0
    page.rtl = True
    page.theme_mode = "light"
    
    if not hasattr(page.session, "logged_in"):
        page.session.logged_in = False
        page.session.username = None

    # ==================== WebAuthn Helper Functions ====================
    def get_user(username: str):
        return users.get(username)

    def create_user(username: str):
        user_id = uuid.uuid4().bytes
        users[username] = {"id": user_id, "credentials": []}
        return user_id

    # ==================== ثبت‌نام بیومتریک ====================
    def register_biometric(e):
        username = page.session.get("temp_username")
        if not username:
            return

        user = get_user(username)
        if not user:
            user_id = create_user(username)
        else:
            user_id = user["id"]

        registration_options = generate_registration_options(
            rp_id=page.request.host.split(":")[0] if page.request else "localhost",
            rp_name="TopSUNify",
            user_id=user_id,
            user_name=username,
            user_display_name=username,
        )

        page.session.registration_options = registration_options
        page.run_js(f"""
            window.registrationOptions = {options_to_json(registration_options)};
            navigator.credentials.create({{publicKey: window.registrationOptions}})
                .then(cred => {{
                    window.pywebview.onRegistrationSuccess(JSON.stringify({{
                        id: cred.id,
                        rawId: Array.from(new Uint8Array(cred.rawId)),
                        response: {{
                            attestationObject: Array.from(new Uint8Array(cred.response.attestationObject)),
                            clientDataJSON: Array.from(new Uint8Array(cred.response.clientDataJSON))
                        }},
                        type: cred.type
                    }}));
                }})
                .catch(err => console.error(err));
        """)

    # ==================== لاگین بیومتریک ====================
    def show_biometric_dialog(e):
        dlg = ft.AlertDialog(
            title=ft.Text("احراز هویت بیومتریک", size=18, weight="bold"),
            content=ft.Column([
                ft.ProgressRing(width=65, height=65),
                ft.Text("لطفاً اثر انگشت یا چهره خود را تأیید کنید...", text_align="center")
            ], horizontal_alignment="center", spacing=20),
            actions=[ft.TextButton("انصراف", on_click=lambda _: (setattr(dlg, 'open', False), page.update()))]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

        # اینجا Authentication Options تولید و به JS ارسال می‌شود
        # (برای سادگی فعلاً شبیه‌سازی + تابع واقعی)
        time.sleep(1.5)
        dlg.open = False
        page.session.logged_in = True
        page.update()
        render()

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
                                ink=True
                            ),
                            ft.TextField(label="رمز عبور", password=True, width=270, border_radius=12, prefix_icon=ft.Icons.LOCK, text_align=ft.TextAlign.RIGHT)
                        ], alignment="center", spacing=12),
                        margin=ft.margin.Margin(bottom=30)
                    ),

                    ft.ElevatedButton("ورود به TopSUNify", width=340, bgcolor="#FFCC00", color="black",
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)),
                                    on_click=lambda e: (setattr(page.session, 'logged_in', True), render())),

                    ft.Text("فعال‌سازی / فراموشی رمز", size=14, color="blue", text_align="center"),

                    ft.Container(content=ft.Image(src="TopSUN-Powered.png", width=160), margin=ft.margin.Margin(top=50, bottom=30)),

                    ft.Container(expand=True, content=ft.Image(src="landscape.jpg", width=400, height=220, fit="cover"))
                ], horizontal_alignment="center", expand=True, scroll=ft.ScrollMode.AUTO)
            )
        else:
            # داشبورد
            page.add(
                ft.Column([
                    ft.Text("پنل TopSUNify", size=30, weight="bold"),
                    ft.Divider(),
                    ft.Text("خوش آمدید!", size=25),
                    ft.ElevatedButton("خروج", on_click=lambda e: (setattr(page.session, 'logged_in', False), render()))
                ], horizontal_alignment="center", expand=True)
            )

        page.update()

    render()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, port=port, host="0.0.0.0", assets_dir="assets")
