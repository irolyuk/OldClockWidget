import sys
import json
from pathlib import Path
from datetime import datetime

from PySide6.QtCore import Qt, QTimer, QPoint, QSettings
from PySide6.QtGui import QColor, QPainter, QAction, QFont
from PySide6.QtWidgets import QApplication, QWidget, QMenu, QSizeGrip


def resource_path(name: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base / name


class OldClockWidget(QWidget):
    BASE_CLOCK_W = 620
    BASE_DRAW_W = 760
    BASE_H = 165

    DIGIT_SLOT = 28.0
    COLON_SLOT = 8.0
    GAP = 6.0
    LED_DIAMETER = 2.15

    DRAW_GAP = 12.0
    DRAW_WIDTH = 62.0

    # Two inactive LED rows/columns around the content.
    MATRIX_PAD_X = 8.0
    MATRIX_PAD_TOP = 8.0
    MATRIX_PAD_BOTTOM = 8.0

    COLORS = {
        "Green": QColor(35, 255, 105),
        "Red": QColor(255, 55, 45),
        "Blue": QColor(55, 155, 255),
        "Cyan": QColor(40, 245, 255),
        "Yellow": QColor(255, 225, 45),
        "Orange": QColor(255, 145, 35),
        "Pink": QColor(255, 80, 190),
        "Purple": QColor(180, 90, 255),
        "White": QColor(235, 245, 240),
    }

    def __init__(self):
        super().__init__()

        with open(resource_path("clock_font.json"), "r", encoding="utf-8") as f:
            data = json.load(f)

        self.font = data["font"]
        layout = data.get("layout", {})
        self.DIGIT_SLOT = float(layout.get("digit_slot_width", 28.0))
        self.COLON_SLOT = float(layout.get("colon_slot_width", 8.0))
        self.GAP = float(layout.get("slot_gap", 6.0))

        self.current_text = datetime.now().strftime("%H:%M:%S")
        self.dragging = False
        self.drag_offset = QPoint()

        # {(logical_x, logical_y): "Color name"}
        self.user_leds = {}
        self.current_color = "Green"
        self.panel_visible = True
        self.signature_visible = True
        self.draw_mode = False
        self.erase_mode = False
        self.settings = QSettings("IvanRoliuk", "OldClockWidget")

        self.setWindowTitle("Old Clock")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMinimumSize(310, 88)
        self.resize(self.BASE_DRAW_W, self.BASE_H)
        self.load_settings()

        self.grip = QSizeGrip(self)
        self.grip.resize(18, 18)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(200)

    def load_settings(self):
        self.panel_visible = self.settings.value("panel_visible", True, type=bool)
        self.signature_visible = self.settings.value("signature_visible", True, type=bool)
        self.current_color = self.settings.value("current_color", "Green", type=str)
        if self.current_color not in self.COLORS:
            self.current_color = "Green"

        size = self.settings.value("window_size")
        pos = self.settings.value("window_pos")
        if size is not None:
            self.resize(size)
        if pos is not None:
            self.move(pos)

        raw = self.settings.value("drawing", "[]", type=str)
        try:
            saved = json.loads(raw)
            self.user_leds = {
                (float(item["x"]), float(item["y"])): item["color"]
                for item in saved
                if item.get("color") in self.COLORS
            }
        except (json.JSONDecodeError, TypeError, KeyError, ValueError):
            self.user_leds = {}

    def save_settings(self):
        self.settings.setValue("panel_visible", self.panel_visible)
        self.settings.setValue("signature_visible", self.signature_visible)
        self.settings.setValue("current_color", self.current_color)
        self.settings.setValue("window_size", self.size())
        self.settings.setValue("window_pos", self.pos())
        drawing = [
            {"x": x, "y": y, "color": color}
            for (x, y), color in self.user_leds.items()
        ]
        self.settings.setValue("drawing", json.dumps(drawing))
        self.settings.sync()

    def closeEvent(self, event):
        self.save_settings()
        super().closeEvent(event)

    def slot_width(self, ch):
        return self.COLON_SLOT if ch == ":" else self.DIGIT_SLOT

    def clock_width(self):
        text = "00:00:00"
        return sum(self.slot_width(c) for c in text) + self.GAP * (len(text) - 1)

    def content_logical_width(self):
        if self.panel_visible:
            return self.clock_width() + self.DRAW_GAP + self.DRAW_WIDTH
        return self.clock_width()

    def total_logical_width(self):
        return self.content_logical_width() + self.MATRIX_PAD_X * 2

    def layout_values(self):
        logical_w = self.total_logical_width()
        logical_h = 48.0 + self.MATRIX_PAD_TOP + self.MATRIX_PAD_BOTTOM
        side_margin = 30.0
        vertical_margin = 13.0
        usable_w = max(1.0, self.width() - side_margin * 2)
        usable_h = max(1.0, self.height() - vertical_margin * 2)
        scale = min(usable_w / logical_w, usable_h / logical_h)
        draw_w = logical_w * scale
        draw_h = logical_h * scale
        return scale, (self.width()-draw_w)/2.0, (self.height()-draw_h)/2.0

    def resizeEvent(self, event):
        self.grip.move(self.width()-self.grip.width(), self.height()-self.grip.height())
        super().resizeEvent(event)

    def tick(self):
        t = datetime.now().strftime("%H:%M:%S")
        if t != self.current_text:
            self.current_text = t
            self.update()

    def paint_led(self, p, x, y, scale, ox, oy, color=None):
        sx = ox + x * scale
        # oy is the top of the WHOLE padded matrix. Move the original
        # clock coordinate system down by MATRIX_PAD_TOP so top/bottom
        # inactive rows are symmetric.
        sy = oy + self.MATRIX_PAD_TOP * scale + (46.0 - y + 1.0) * scale

        if color is not None:
            diameter = max(1.3, self.LED_DIAMETER * scale)
            r = diameter / 2
            glow = QColor(color)
            glow.setAlpha(48)
            gr = r * 1.65
            p.setBrush(glow)
            p.drawEllipse(sx-gr, sy-gr, gr*2, gr*2)
            p.setBrush(color)
            p.drawEllipse(sx-r, sy-r, diameter, diameter)
        else:
            diameter = max(1.0, self.LED_DIAMETER * scale * .88)
            r = diameter / 2
            p.setBrush(QColor(7, 38, 20, 210))
            p.drawEllipse(sx-r, sy-r, diameter, diameter)
            hr = r * .28
            p.setBrush(QColor(12, 58, 30, 150))
            p.drawEllipse(sx-hr, sy-hr, hr*2, hr*2)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Qt.NoPen)

        p.setBrush(QColor(5, 7, 6, 248))
        radius = max(8.0, min(self.width(), self.height()) * .07)
        p.drawRoundedRect(self.rect(), radius, radius)

        scale, ox, oy = self.layout_values()
        total_w = self.total_logical_width()

        # Entire inactive matrix.
        # Matrix extends exactly two LED rows below and two above the
        # original 0..46 clock glyph area.
        x = 0.0
        col = 0
        min_y = -self.MATRIX_PAD_BOTTOM
        max_y = 46.0 + self.MATRIX_PAD_TOP
        while x <= total_w:
            y0 = 0.0 if col % 2 == 0 else 2.0
            # Walk downward to the first lattice point inside min_y.
            y = y0
            while y - 4.0 >= min_y:
                y -= 4.0
            while y <= max_y:
                self.paint_led(p, x, y, scale, ox, oy, None)
                y += 4.0
            x += 2.0
            col += 1

        # Clock always remains green.
        cursor = self.MATRIX_PAD_X
        clock_green = self.COLORS["Green"]
        for ch in self.current_text:
            glyph = self.font[ch]
            aw = float(glyph["width"])
            slot = self.slot_width(ch)
            gx = cursor + (slot-aw)/2.0
            for px, py in glyph["points"]:
                self.paint_led(p, gx+float(px), float(py), scale, ox, oy, clock_green)
            cursor += slot + self.GAP

        # Independent multicolor drawing.
        if self.panel_visible:
            for (x, y), color_name in self.user_leds.items():
                color = self.COLORS.get(color_name, self.COLORS["Green"])
                self.paint_led(p, x, y, scale, ox, oy, color)

        # Small creator signature under the clock, bottom-left.
        # Kept subtle so it feels like part of the display rather than UI chrome.
        if self.signature_visible:
            signature = "Created by Ivan Roliuk"
            font_size = max(6, int(5.2 * scale))
            sig_font = QFont("Consolas")
            sig_font.setPixelSize(font_size)
            sig_font.setBold(False)
            p.setFont(sig_font)

            sig_color = QColor(35, 255, 105, 145)
            p.setPen(sig_color)

            sig_x = ox + self.MATRIX_PAD_X * scale
            sig_y = min(
                self.height() - 5,
                oy + (self.MATRIX_PAD_TOP + 48.0) * scale + font_size + 2
            )
            p.drawText(int(sig_x), int(sig_y), signature)

            p.setPen(Qt.NoPen)

    def drawing_start(self):
        return self.MATRIX_PAD_X + self.clock_width() + self.DRAW_GAP

    def screen_to_led(self, pos):
        if not self.panel_visible:
            return None
        scale, ox, oy = self.layout_values()
        lx = (pos.x()-ox)/scale
        ly = 46.0 - (((pos.y()-oy-self.MATRIX_PAD_TOP*scale)/scale) - 1.0)
        start = self.drawing_start()
        if lx < start or lx > start+self.DRAW_WIDTH or ly < 0 or ly > 46:
            return None

        col = round(lx/2.0)
        x = col*2.0
        y0 = 0.0 if col % 2 == 0 else 2.0
        row = round((ly-y0)/4.0)
        y = y0 + row*4.0

        if x < start or x > start+self.DRAW_WIDTH or y < 0 or y > 46:
            return None
        return (x, y)

    def apply_draw(self, pos, erase=False):
        led = self.screen_to_led(pos)
        if led is None:
            return False
        if erase:
            self.user_leds.pop(led, None)
        else:
            self.user_leds[led] = self.current_color
        self.save_settings()
        self.update()
        return True

    def set_panel_visible(self, visible):
        if self.panel_visible == visible:
            return
        old_w = self.width()
        self.panel_visible = visible

        # Make hiding/showing feel natural instead of squashing the clock.
        hidden_w = self.clock_width() + self.MATRIX_PAD_X * 2
        shown_w = self.clock_width() + self.DRAW_GAP + self.DRAW_WIDTH + self.MATRIX_PAD_X * 2
        ratio = hidden_w / shown_w
        if visible:
            self.resize(max(self.BASE_DRAW_W, int(old_w / max(ratio, .1))), self.height())
        else:
            self.resize(max(self.minimumWidth(), int(old_w * ratio)), self.height())
        self.save_settings()
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.grip.geometry().contains(event.position().toPoint()):
                return
            if self.apply_draw(event.position(), False):
                self.draw_mode = True
                event.accept()
                return
            self.dragging = True
            self.drag_offset = event.globalPosition().toPoint()-self.frameGeometry().topLeft()
            event.accept()
        elif event.button() == Qt.RightButton:
            if self.apply_draw(event.position(), True):
                self.erase_mode = True
                event.accept()
            else:
                self.show_menu(event.globalPosition().toPoint())
                event.accept()

    def mouseMoveEvent(self, event):
        if self.draw_mode and (event.buttons() & Qt.LeftButton):
            self.apply_draw(event.position(), False)
            return
        if self.erase_mode and (event.buttons() & Qt.RightButton):
            self.apply_draw(event.position(), True)
            return
        if self.dragging and (event.buttons() & Qt.LeftButton):
            self.move(event.globalPosition().toPoint()-self.drag_offset)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = self.draw_mode = self.erase_mode = False

    def show_menu(self, pos):
        menu = QMenu(self)

        panel = QAction("Drawing panel", self)
        panel.setCheckable(True)
        panel.setChecked(self.panel_visible)
        panel.toggled.connect(self.set_panel_visible)
        menu.addAction(panel)

        signature_action = QAction("Created by Ivan Roliuk", self)
        signature_action.setCheckable(True)
        signature_action.setChecked(self.signature_visible)
        def toggle_signature(checked):
            self.signature_visible = checked
            self.save_settings()
            self.update()
        signature_action.toggled.connect(toggle_signature)
        menu.addAction(signature_action)

        color_menu = menu.addMenu("Drawing color")
        for name, color in self.COLORS.items():
            action = QAction(name, self)
            action.setCheckable(True)
            action.setChecked(name == self.current_color)
            def choose_color(checked=False, n=name):
                self.current_color = n
                self.save_settings()
            action.triggered.connect(choose_color)
            color_menu.addAction(action)

        clear = QAction("Clear drawing", self)
        def clear_drawing():
            self.user_leds.clear()
            self.save_settings()
            self.update()
        clear.triggered.connect(clear_drawing)
        menu.addAction(clear)

        menu.addSeparator()

        top = QAction("Always on top", self)
        top.setCheckable(True)
        top.setChecked(bool(self.windowFlags() & Qt.WindowStaysOnTopHint))
        def toggle_top(checked):
            flags = self.windowFlags()
            flags = (flags | Qt.WindowStaysOnTopHint) if checked else (flags & ~Qt.WindowStaysOnTopHint)
            self.setWindowFlags(flags)
            self.show()
        top.toggled.connect(toggle_top)
        menu.addAction(top)

        reset = QAction("Reset size", self)
        reset.triggered.connect(lambda: self.resize(
            self.BASE_DRAW_W if self.panel_visible else self.BASE_CLOCK_W,
            self.BASE_H
        ))
        menu.addAction(reset)

        menu.addSeparator()
        quit_action = QAction("Exit", self)
        def quit_app():
            self.save_settings()
            QApplication.quit()
        quit_action.triggered.connect(quit_app)
        menu.addAction(quit_action)

        menu.exec(pos)


app = QApplication(sys.argv)
clock = OldClockWidget()
clock.show()
sys.exit(app.exec())
