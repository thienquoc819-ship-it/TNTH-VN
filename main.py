import json
import os
import urllib.request
import urllib.error

from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

BG = (0.025, 0.04, 0.075, 1)
PANEL = (0.055, 0.09, 0.14, 1)
NEON = (0.0, 0.85, 1, 1)
WHITE = (0.9, 0.96, 1, 1)
MUTED = (0.55, 0.68, 0.78, 1)


class TNTHVN(App):
    def build(self):
        self.title = "TNTH VN"
        Window.clearcolor = BG
        self.page = BoxLayout(orientation="vertical", spacing=dp(10),
                              padding=dp(15))
        self.show_home()
        return self.page

    def label(self, text, size=16, color=WHITE, height=None):
        return Label(
            text=text,
            font_size=sp(size),
            color=color,
            size_hint_y=None if height else 1,
            height=dp(height) if height else None,
            halign="left",
            valign="middle"
        )

    def clear(self):
        self.page.clear_widgets()

    def header(self, subtitle):
        top = BoxLayout(size_hint_y=None, height=dp(65), spacing=dp(8))
        top.add_widget(Label(
            text="[b]TNTH [color=00D9FF]VN[/color][/b]",
            markup=True, font_size=dp(27), color=WHITE,
            halign="left"
        ))
        top.add_widget(Label(
            text=subtitle, font_size=dp(12), color=MUTED
        ))
        self.page.add_widget(top)

    def button(self, text, callback, color=NEON):
        b = Button(
            text=text, size_hint_y=None, height=dp(52),
            background_normal="", background_color=PANEL,
            color=color, font_size=dp(15)
        )
        b.bind(on_press=callback)
        return b

    def content(self):
        scroll = ScrollView()
        self.body = BoxLayout(
            orientation="vertical", spacing=dp(12),
            size_hint_y=None, padding=(0, dp(5))
        )
        self.body.bind(minimum_height=self.body.setter("height"))
        scroll.add_widget(self.body)
        self.page.add_widget(scroll)

    def show_home(self, *args):
        self.clear()
        self.header("YOUR CONTROL CENTER")
        self.content()

        self.body.add_widget(self.label(
            "[b]Xin chào![/b]", 24, NEON, 45
        ))
        self.body.add_widget(self.label(
            "Chào mừng đến với ứng dụng TNTH VN.",
            15, MUTED, 38
        ))
        self.body.add_widget(Widget(size_hint_y=None, height=dp(10)))

        self.body.add_widget(self.button(
            "▣   QUẢN LÝ BOT TELEGRAM", self.show_telegram
        ))
        self.body.add_widget(self.button(
            "◆   MENU CHỨC NĂNG", self.show_menu
        ))
        self.body.add_widget(self.button(
            "ⓘ   THÔNG TIN ỨNG DỤNG", self.show_info
        ))
        self.body.add_widget(Widget(size_hint_y=None, height=dp(20)))
        self.body.add_widget(self.label(
            "TNTH VN  •  VERSION 1.0",
            12, MUTED, 35
        ))

    def show_menu(self, *args):
        self.clear()
        self.header("FUNCTION MENU")
        self.content()
        self.body.add_widget(self.label("MENU CHỨC NĂNG", 22, NEON, 50))
        self.body.add_widget(self.button("Quản lý Telegram", self.show_telegram))
        self.body.add_widget(self.button("Thông tin ứng dụng", self.show_info))
        self.body.add_widget(self.button("Trang chủ", self.show_home))

    def show_info(self, *args):
        self.clear()
        self.header("ABOUT TNTH VN")
        self.content()
        self.body.add_widget(self.label("TNTH VN", 28, NEON, 55))
        self.body.add_widget(self.label("Phiên bản: 1.0.0", 16, WHITE, 40))
        self.body.add_widget(self.label("Nền tảng: Android", 16, WHITE, 40))
        self.body.add_widget(self.label("Giao diện: Dark Neon Blue", 16, WHITE, 40))
        self.body.add_widget(self.label(
            "Ứng dụng quản lý và theo dõi bot Telegram "
            "thông qua máy chủ API riêng.",
            15, MUTED, 90
        ))
        self.body.add_widget(self.button("Về trang chủ", self.show_home))

    def show_telegram(self, *args):
        self.clear()
        self.header("TELEGRAM CONTROL")
        self.content()

        self.body.add_widget(self.label("QUẢN LÝ BOT", 23, NEON, 48))
        self.body.add_widget(self.label(
            "Nhập địa chỉ HTTPS của máy chủ quản lý bot.",
            14, MUTED, 45
        ))

        self.api_input = TextInput(
            hint_text="https://your-server.example",
            multiline=False, size_hint_y=None, height=dp(50),
            background_color=PANEL, foreground_color=WHITE,
            hint_text_color=MUTED, cursor_color=NEON
        )
        self.body.add_widget(self.api_input)

        self.key_input = TextInput(
            hint_text="API key (không phải Telegram Bot Token)",
            multiline=False, password=True,
            size_hint_y=None, height=dp(50),
            background_color=PANEL, foreground_color=WHITE,
            hint_text_color=MUTED, cursor_color=NEON
        )
        self.body.add_widget(self.key_input)

        self.status = self.label(
            "Trạng thái: Chưa kết nối máy chủ",
            14, MUTED, 55
        )
        self.body.add_widget(self.status)

        self.body.add_widget(self.button(
            "KIỂM TRA TRẠNG THÁI",
            lambda x: self.api_call("status")
        ))
        self.body.add_widget(self.button(
            "BẬT BOT",
            lambda x: self.api_call("start")
        ))
        self.body.add_widget(self.button(
            "TẮT BOT",
            lambda x: self.api_call("stop")
        ))
        self.body.add_widget(self.label(
            "Yêu cầu backend hỗ trợ POST /status, /start và /stop. "
            "Các lệnh chỉ hoạt động khi backend đã được triển khai.",
            13, MUTED, 95
        ))
        self.body.add_widget(self.button("Về trang chủ", self.show_home))

    def api_call(self, action):
        base = self.api_input.text.strip().rstrip("/")
        key = self.key_input.text.strip()

        if not base.startswith("https://") or not key:
            self.status.text = "Cần HTTPS và API key hợp lệ."
            return

        try:
            data = json.dumps({}).encode("utf-8")
            req = urllib.request.Request(
                base + "/" + action,
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + key
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                result = response.read().decode("utf-8")
                self.status.text = "Kết quả: " + result[:250]
        except Exception as e:
            self.status.text = "Không kết nối được: " + str(e)[:150]


def sp(value):
    return dp(value)


if __name__ == "__main__":
    TNTHVN().run()
