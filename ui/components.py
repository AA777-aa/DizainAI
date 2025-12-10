"""
Переиспользуемые UI компоненты DizainAI
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QGraphicsDropShadowEffect,
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QFont

from .icons import Icons, IconButton


class Card(QFrame):
    """Карточка с тенью"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self._setup_shadow()

    def _setup_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)


class SectionHeader(QWidget):
    """Заголовок секции с иконкой"""

    def __init__(self, title: str, icon_svg: str = None, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 8)
        layout.setSpacing(8)

        if icon_svg:
            icon_label = QLabel()
            icon_label.setPixmap(Icons.get_pixmap(icon_svg, Icons.COLOR_ACCENT, 18))
            layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setObjectName("sectionHeader")
        layout.addWidget(title_label)

        layout.addStretch()


class PropertyRow(QWidget):
    """Строка свойства: метка + значение"""

    value_changed = pyqtSignal(object)

    def __init__(self, label: str, widget_type: str = "text", parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(12)

        # Метка
        self.label = QLabel(label)
        self.label.setMinimumWidth(80)
        self.label.setObjectName("propertyLabel")
        layout.addWidget(self.label)

        # Виджет значения
        self.value_widget = self._create_widget(widget_type)
        layout.addWidget(self.value_widget, 1)

    def _create_widget(self, widget_type: str) -> QWidget:
        if widget_type == "text":
            widget = QLineEdit()
            widget.textChanged.connect(lambda v: self.value_changed.emit(v))
        elif widget_type == "int":
            widget = QSpinBox()
            widget.setRange(0, 99999)
            widget.valueChanged.connect(lambda v: self.value_changed.emit(v))
        elif widget_type == "float":
            widget = QDoubleSpinBox()
            widget.setRange(0, 99999)
            widget.setDecimals(2)
            widget.valueChanged.connect(lambda v: self.value_changed.emit(v))
        elif widget_type == "combo":
            widget = QComboBox()
            widget.currentTextChanged.connect(lambda v: self.value_changed.emit(v))
        else:
            widget = QLabel()

        return widget

    def set_value(self, value):
        """Установить значение"""
        widget = self.value_widget
        if isinstance(widget, QLineEdit):
            widget.setText(str(value))
        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            widget.setValue(value)
        elif isinstance(widget, QComboBox):
            idx = widget.findText(str(value))
            if idx >= 0:
                widget.setCurrentIndex(idx)
        elif isinstance(widget, QLabel):
            widget.setText(str(value))

    def get_value(self):
        """Получить значение"""
        widget = self.value_widget
        if isinstance(widget, QLineEdit):
            return widget.text()
        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            return widget.value()
        elif isinstance(widget, QComboBox):
            return widget.currentText()
        elif isinstance(widget, QLabel):
            return widget.text()


class StatCard(Card):
    """Карточка со статистикой"""

    def __init__(self, title: str, value: str = "0",
                 icon_svg: str = None, color: str = None, parent=None):
        super().__init__(parent)

        self.color = color or "#818cf8"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        # Верхняя строка с иконкой и значением
        top_row = QHBoxLayout()

        if icon_svg:
            icon_label = QLabel()
            icon_label.setPixmap(Icons.get_pixmap(icon_svg, self.color, 24))
            top_row.addWidget(icon_label)

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"""
            font-size: 28px;
            font-weight: bold;
            color: {self.color};
        """)
        top_row.addWidget(self.value_label)
        top_row.addStretch()

        layout.addLayout(top_row)

        # Подпись
        self.title_label = QLabel(title)
        self.title_label.setObjectName("statTitle")
        layout.addWidget(self.title_label)

    def set_value(self, value: str):
        self.value_label.setText(value)


class ActionButton(QPushButton):
    """Кнопка действия с иконкой и анимацией"""

    def __init__(self, text: str, icon_svg: str = None,
                 variant: str = "default", parent=None):
        super().__init__(text, parent)

        self.variant = variant
        self.setObjectName(f"actionButton_{variant}")

        if icon_svg:
            self.setIcon(Icons.get_icon(icon_svg, self._get_icon_color(), 18))

        self.setMinimumHeight(40)
        self._apply_style()

    def _get_icon_color(self) -> str:
        colors = {
            "default": Icons.COLOR_DEFAULT,
            "primary": "#ffffff",
            "success": "#ffffff",
            "danger": "#ffffff"
        }
        return colors.get(self.variant, Icons.COLOR_DEFAULT)

    def _apply_style(self):
        styles = {
            "default": """
                QPushButton {
                    background-color: #1e293b;
                    border: 1px solid #334155;
                    color: #f8fafc;
                }
                QPushButton:hover {
                    background-color: #334155;
                    border-color: #475569;
                }
            """,
            "primary": """
                QPushButton {
                    background-color: #4f46e5;
                    border: none;
                    color: #ffffff;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #6366f1;
                }
            """,
            "success": """
                QPushButton {
                    background-color: #10b981;
                    border: none;
                    color: #ffffff;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #059669;
                }
            """,
            "danger": """
                QPushButton {
                    background-color: #ef4444;
                    border: none;
                    color: #ffffff;
                }
                QPushButton:hover {
                    background-color: #dc2626;
                }
            """
        }

        base_style = """
            QPushButton {
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 13px;
            }
            QPushButton:pressed {
                padding-top: 10px;
                padding-bottom: 6px;
            }
            QPushButton:disabled {
                opacity: 0.5;
            }
        """

        self.setStyleSheet(base_style + styles.get(self.variant, styles["default"]))


class Separator(QFrame):
    """Разделитель"""

    def __init__(self, orientation: str = "horizontal", parent=None):
        super().__init__(parent)

        if orientation == "horizontal":
            self.setFrameShape(QFrame.HLine)
            self.setFixedHeight(1)
        else:
            self.setFrameShape(QFrame.VLine)
            self.setFixedWidth(1)

        self.setStyleSheet("background-color: #334155;")


class Badge(QLabel):
    """Бейдж/метка"""

    def __init__(self, text: str, variant: str = "default", parent=None):
        super().__init__(text, parent)

        colors = {
            "default": ("#334155", "#94a3b8"),
            "primary": ("#4f46e5", "#ffffff"),
            "success": ("#10b981", "#ffffff"),
            "warning": ("#f59e0b", "#000000"),
            "danger": ("#ef4444", "#ffffff"),
        }

        bg, fg = colors.get(variant, colors["default"])

        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg};
                color: {fg};
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 600;
            }}
        """)


class EmptyState(QWidget):
    """Заглушка для пустого состояния"""

    action_clicked = pyqtSignal()

    def __init__(self, icon_svg: str, title: str,
                 description: str = "", action_text: str = "", parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)

        # Иконка
        icon_label = QLabel()
        icon_label.setPixmap(Icons.get_pixmap(icon_svg, "#475569", 64))
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        # Заголовок
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #94a3b8;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Описание
        if description:
            desc_label = QLabel(description)
            desc_label.setStyleSheet("color: #64748b; font-size: 13px;")
            desc_label.setAlignment(Qt.AlignCenter)
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)

        # Кнопка действия
        if action_text:
            action_btn = ActionButton(action_text, Icons.SVG_PLUS, "primary")
            action_btn.clicked.connect(self.action_clicked.emit)
            layout.addWidget(action_btn, alignment=Qt.AlignCenter)