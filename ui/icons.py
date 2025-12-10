"""
SVG Иконки для DizainAI
Векторные иконки вместо эмодзи для профессионального вида
"""

from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QSize, QRectF  # ← Изменено: QRect на QRectF
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QPushButton, QToolButton


class Icons:
    """Централизованное хранилище SVG иконок"""

    # Цвета иконок
    COLOR_DEFAULT = "#94a3b8"
    COLOR_ACTIVE = "#f8fafc"
    COLOR_ACCENT = "#818cf8"
    COLOR_SUCCESS = "#10b981"
    COLOR_WARNING = "#f59e0b"
    COLOR_DANGER = "#ef4444"

    _cache = {}

    # === ФАЙЛОВЫЕ ОПЕРАЦИИ ===
    SVG_NEW = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
        <polyline points="14 2 14 8 20 8"/>
        <line x1="12" y1="18" x2="12" y2="12"/>
        <line x1="9" y1="15" x2="15" y2="15"/>
    </svg>'''

    SVG_OPEN = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
    </svg>'''

    SVG_SAVE = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
        <polyline points="17 21 17 13 7 13 7 21"/>
        <polyline points="7 3 7 8 15 8"/>
    </svg>'''

    SVG_EXPORT = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
        <polyline points="17 8 12 3 7 8"/>
        <line x1="12" y1="3" x2="12" y2="15"/>
    </svg>'''

    # === ИНСТРУМЕНТЫ РИСОВАНИЯ ===
    SVG_SELECT = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <path d="M3 3l7.07 16.97 2.51-7.39 7.39-2.51L3 3z"/>
        <path d="M13 13l6 6"/>
    </svg>'''

    SVG_MOVE = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <polyline points="5 9 2 12 5 15"/>
        <polyline points="9 5 12 2 15 5"/>
        <polyline points="15 19 12 22 9 19"/>
        <polyline points="19 9 22 12 19 15"/>
        <line x1="2" y1="12" x2="22" y2="12"/>
        <line x1="12" y1="2" x2="12" y2="22"/>
    </svg>'''

    SVG_DRAW_WALL = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
        <line x1="3" y1="9" x2="21" y2="9"/>
        <line x1="9" y1="21" x2="9" y2="9"/>
    </svg>'''

    SVG_DRAW_LINE = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <line x1="5" y1="19" x2="19" y2="5"/>
        <circle cx="5" cy="19" r="2"/>
        <circle cx="19" cy="5" r="2"/>
    </svg>'''

    SVG_DRAW_RECT = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
    </svg>'''

    SVG_DOOR = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <path d="M18 3H6a2 2 0 0 0-2 2v16h16V5a2 2 0 0 0-2-2z"/>
        <path d="M14 12h.01"/>
        <path d="M8 21V7l8-2v16"/>
    </svg>'''

    SVG_WINDOW = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <rect x="3" y="3" width="18" height="18" rx="2"/>
        <line x1="3" y1="12" x2="21" y2="12"/>
        <line x1="12" y1="3" x2="12" y2="21"/>
    </svg>'''

    # === ДЕЙСТВИЯ ===
    SVG_DELETE = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <polyline points="3 6 5 6 21 6"/>
        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
        <line x1="10" y1="11" x2="10" y2="17"/>
        <line x1="14" y1="11" x2="14" y2="17"/>
    </svg>'''

    SVG_UNDO = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <polyline points="1 4 1 10 7 10"/>
        <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/>
    </svg>'''

    SVG_REDO = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <polyline points="23 4 23 10 17 10"/>
        <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
    </svg>'''

    SVG_ZOOM_IN = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <circle cx="11" cy="11" r="8"/>
        <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        <line x1="11" y1="8" x2="11" y2="14"/>
        <line x1="8" y1="11" x2="14" y2="11"/>
    </svg>'''

    SVG_ZOOM_OUT = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <circle cx="11" cy="11" r="8"/>
        <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        <line x1="8" y1="11" x2="14" y2="11"/>
    </svg>'''

    SVG_FIT = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <polyline points="15 3 21 3 21 9"/>
        <polyline points="9 21 3 21 3 15"/>
        <line x1="21" y1="3" x2="14" y2="10"/>
        <line x1="3" y1="21" x2="10" y2="14"/>
    </svg>'''

    # === НАВИГАЦИЯ И UI ===
    SVG_SETTINGS = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <circle cx="12" cy="12" r="3"/>
        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
    </svg>'''

    SVG_HOME = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
        <polyline points="9 22 9 12 15 12 15 22"/>
    </svg>'''

    SVG_LAYERS = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <polygon points="12 2 2 7 12 12 22 7 12 2"/>
        <polyline points="2 17 12 22 22 17"/>
        <polyline points="2 12 12 17 22 12"/>
    </svg>'''

    SVG_GRID = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <rect x="3" y="3" width="7" height="7"/>
        <rect x="14" y="3" width="7" height="7"/>
        <rect x="14" y="14" width="7" height="7"/>
        <rect x="3" y="14" width="7" height="7"/>
    </svg>'''

    SVG_EYE = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
        <circle cx="12" cy="12" r="3"/>
    </svg>'''

    SVG_EYE_OFF = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
        <line x1="1" y1="1" x2="23" y2="23"/>
    </svg>'''

    # === AI И СПЕЦИАЛЬНЫЕ ===
    SVG_AI = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2z"/>
        <circle cx="8" cy="14" r="1.5" fill="{color}"/>
        <circle cx="16" cy="14" r="1.5" fill="{color}"/>
    </svg>'''

    SVG_MAGIC = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <path d="M15 4V2"/>
        <path d="M15 16v-2"/>
        <path d="M8 9h2"/>
        <path d="M20 9h2"/>
        <path d="M17.8 11.8L19 13"/>
        <path d="M15 9h0"/>
        <path d="M17.8 6.2L19 5"/>
        <path d="M3 21l9-9"/>
        <path d="M12.2 6.2L11 5"/>
    </svg>'''

    SVG_CUBE = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
        <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
        <line x1="12" y1="22.08" x2="12" y2="12"/>
    </svg>'''

    SVG_CALCULATOR = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <rect x="4" y="2" width="16" height="20" rx="2"/>
        <line x1="8" y1="6" x2="16" y2="6"/>
        <line x1="8" y1="10" x2="8" y2="10.01"/>
        <line x1="12" y1="10" x2="12" y2="10.01"/>
        <line x1="16" y1="10" x2="16" y2="10.01"/>
        <line x1="8" y1="14" x2="8" y2="14.01"/>
        <line x1="12" y1="14" x2="12" y2="14.01"/>
        <line x1="16" y1="14" x2="16" y2="14.01"/>
        <line x1="8" y1="18" x2="8" y2="18.01"/>
        <line x1="12" y1="18" x2="12" y2="18.01"/>
        <line x1="16" y1="18" x2="16" y2="18.01"/>
    </svg>'''

    SVG_PLUS = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <line x1="12" y1="5" x2="12" y2="19"/>
        <line x1="5" y1="12" x2="19" y2="12"/>
    </svg>'''

    SVG_MINUS = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <line x1="5" y1="12" x2="19" y2="12"/>
    </svg>'''

    SVG_CHECK = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <polyline points="20 6 9 17 4 12"/>
    </svg>'''

    SVG_CLOSE = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <line x1="18" y1="6" x2="6" y2="18"/>
        <line x1="6" y1="6" x2="18" y2="18"/>
    </svg>'''

    SVG_INFO = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="16" x2="12" y2="12"/>
        <line x1="12" y1="8" x2="12.01" y2="8"/>
    </svg>'''

    SVG_SEND = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <line x1="22" y1="2" x2="11" y2="13"/>
        <polygon points="22 2 15 22 11 13 2 9 22 2"/>
    </svg>'''

    SVG_FURNITURE = '''<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <path d="M20 9V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v3"/>
        <path d="M2 11v5a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-5a2 2 0 0 0-4 0v2H6v-2a2 2 0 0 0-4 0z"/>
        <path d="M4 18v2"/>
        <path d="M20 18v2"/>
    </svg>'''

    @classmethod
    def get_icon(cls, svg_template: str, color: str = None, size: int = 24) -> QIcon:
        """Создать QIcon из SVG шаблона"""
        if color is None:
            color = cls.COLOR_DEFAULT

        cache_key = f"{svg_template[:50]}_{color}_{size}"
        if cache_key in cls._cache:
            return cls._cache[cache_key]

        svg_data = svg_template.format(color=color)

        # Создаём pixmap
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        renderer = QSvgRenderer(bytearray(svg_data, encoding='utf-8'))
        renderer.render(painter, QRectF(0, 0, size, size))  # ← ИСПРАВЛЕНО: QRectF

        painter.end()

        icon = QIcon(pixmap)
        cls._cache[cache_key] = icon

        return icon

    @classmethod
    def get_pixmap(cls, svg_template: str, color: str = None, size: int = 24) -> QPixmap:
        """Создать QPixmap из SVG шаблона"""
        if color is None:
            color = cls.COLOR_DEFAULT

        svg_data = svg_template.format(color=color)

        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        renderer = QSvgRenderer(bytearray(svg_data, encoding='utf-8'))
        renderer.render(painter, QRectF(0, 0, size, size))  # ← ИСПРАВЛЕНО: QRectF

        painter.end()

        return pixmap


class IconButton(QPushButton):
    """Кнопка с SVG иконкой"""

    def __init__(self, svg_template: str, text: str = "", parent=None,
                 size: int = 24, color: str = None, hover_color: str = None):
        super().__init__(text, parent)

        self.svg_template = svg_template
        self.icon_size = size
        self.normal_color = color or Icons.COLOR_DEFAULT
        self.hover_color = hover_color or Icons.COLOR_ACTIVE

        self._update_icon(self.normal_color)
        self.setIconSize(QSize(size, size))

    def _update_icon(self, color: str):
        self.setIcon(Icons.get_icon(self.svg_template, color, self.icon_size))

    def enterEvent(self, event):
        self._update_icon(self.hover_color)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._update_icon(self.normal_color)
        super().leaveEvent(event)


class ToolButton(QToolButton):
    """Кнопка панели инструментов с SVG иконкой"""

    def __init__(self, svg_template: str, tooltip: str = "", parent=None,
                 size: int = 20, checkable: bool = False):
        super().__init__(parent)

        self.svg_template = svg_template
        self.icon_size = size

        self.setIcon(Icons.get_icon(svg_template, Icons.COLOR_DEFAULT, size))
        self.setIconSize(QSize(size, size))
        self.setToolTip(tooltip)
        self.setCheckable(checkable)

        if checkable:
            self.toggled.connect(self._on_toggled)

    def _on_toggled(self, checked: bool):
        color = Icons.COLOR_ACCENT if checked else Icons.COLOR_DEFAULT
        self.setIcon(Icons.get_icon(self.svg_template, color, self.icon_size))