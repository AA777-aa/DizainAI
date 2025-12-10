"""
Единая система стилей DizainAI - Тёмная тема
"""

# Цветовая палитра
COLORS = {
    # Основные
    'bg_dark': '#1a1a2e',
    'bg_medium': '#16213e',
    'bg_light': '#1f2937',
    'bg_card': '#252a3d',

    # Акценты
    'accent': '#4f46e5',
    'accent_hover': '#6366f1',
    'accent_light': '#818cf8',

    # Успех/Ошибка
    'success': '#10b981',
    'warning': '#f59e0b',
    'error': '#ef4444',

    # Текст
    'text_primary': '#f8fafc',
    'text_secondary': '#94a3b8',
    'text_muted': '#64748b',

    # Границы
    'border': '#334155',
    'border_light': '#475569',

    # Специальные
    'window': '#87ceeb',
    'door': '#cd853f',
    'wall': '#e2e8f0',
}

# Главная таблица стилей
DARK_THEME = f"""
/* ========== ГЛОБАЛЬНЫЕ СТИЛИ ========== */
QMainWindow, QWidget {{
    background-color: {COLORS['bg_dark']};
    color: {COLORS['text_primary']};
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
}}

/* ========== МЕНЮ ========== */
QMenuBar {{
    background-color: {COLORS['bg_medium']};
    color: {COLORS['text_primary']};
    padding: 5px;
    spacing: 5px;
}}

QMenuBar::item {{
    background: transparent;
    padding: 8px 16px;
    border-radius: 6px;
}}

QMenuBar::item:selected {{
    background-color: {COLORS['accent']};
}}

QMenu {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 5px;
}}

QMenu::item {{
    padding: 10px 30px;
    border-radius: 4px;
}}

QMenu::item:selected {{
    background-color: {COLORS['accent']};
}}

/* ========== ТУЛБАР ========== */
QToolBar {{
    background-color: {COLORS['bg_medium']};
    border: none;
    padding: 8px;
    spacing: 8px;
}}

QToolBar::separator {{
    width: 2px;
    background-color: {COLORS['border']};
    margin: 5px 10px;
}}

QToolButton {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 10px 16px;
    font-weight: 500;
    min-width: 80px;
}}

QToolButton:hover {{
    background-color: {COLORS['accent']};
    border-color: {COLORS['accent']};
}}

QToolButton:pressed {{
    background-color: {COLORS['accent_hover']};
}}

/* ========== КНОПКИ ========== */
QPushButton {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: 600;
    font-size: 13px;
    min-height: 20px;
}}

QPushButton:hover {{
    background-color: {COLORS['accent']};
    border-color: {COLORS['accent']};
}}

QPushButton:pressed {{
    background-color: {COLORS['accent_hover']};
}}

QPushButton:disabled {{
    background-color: {COLORS['bg_light']};
    color: {COLORS['text_muted']};
    border-color: {COLORS['border']};
}}

/* Основная кнопка действия */
QPushButton[class="primary"] {{
    background-color: {COLORS['accent']};
    border-color: {COLORS['accent']};
}}

QPushButton[class="primary"]:hover {{
    background-color: {COLORS['accent_hover']};
}}

/* Кнопка успеха */
QPushButton[class="success"] {{
    background-color: {COLORS['success']};
    border-color: {COLORS['success']};
}}

/* ========== ПОЛЯ ВВОДА ========== */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {COLORS['bg_light']};
    color: {COLORS['text_primary']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
    selection-background-color: {COLORS['accent']};
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border-color: {COLORS['accent']};
}}

QLineEdit:disabled {{
    background-color: {COLORS['bg_dark']};
    color: {COLORS['text_muted']};
}}

/* ========== ВЫПАДАЮЩИЕ СПИСКИ ========== */
QComboBox {{
    background-color: {COLORS['bg_light']};
    color: {COLORS['text_primary']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    padding: 10px 14px;
    min-width: 120px;
}}

QComboBox:hover {{
    border-color: {COLORS['accent']};
}}

QComboBox::drop-down {{
    border: none;
    width: 30px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {COLORS['text_secondary']};
    margin-right: 10px;
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    selection-background-color: {COLORS['accent']};
    padding: 5px;
}}

/* ========== СПИНБОКСЫ ========== */
QSpinBox, QDoubleSpinBox {{
    background-color: {COLORS['bg_light']};
    color: {COLORS['text_primary']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    padding: 10px 14px;
}}

QSpinBox:focus, QDoubleSpinBox:focus {{
    border-color: {COLORS['accent']};
}}

QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
    background-color: {COLORS['bg_card']};
    border: none;
    width: 24px;
    border-radius: 4px;
}}

QSpinBox::up-button:hover, QSpinBox::down-button:hover,
QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {{
    background-color: {COLORS['accent']};
}}

/* ========== ВКЛАДКИ ========== */
QTabWidget::pane {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
    padding: 10px;
}}

QTabBar::tab {{
    background-color: {COLORS['bg_light']};
    color: {COLORS['text_secondary']};
    border: 1px solid {COLORS['border']};
    border-bottom: none;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    padding: 12px 24px;
    margin-right: 4px;
    font-weight: 500;
}}

QTabBar::tab:selected {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text_primary']};
    border-color: {COLORS['accent']};
    border-top: 3px solid {COLORS['accent']};
}}

QTabBar::tab:hover:!selected {{
    background-color: {COLORS['bg_medium']};
    color: {COLORS['text_primary']};
}}

/* ========== ГРУППЫ ========== */
QGroupBox {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
    margin-top: 20px;
    padding: 20px 15px 15px 15px;
    font-weight: 600;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 15px;
    padding: 5px 15px;
    background-color: {COLORS['accent']};
    border-radius: 6px;
    color: {COLORS['text_primary']};
}}

/* ========== СПИСКИ ========== */
QListWidget {{
    background-color: {COLORS['bg_light']};
    border: 2px solid {COLORS['border']};
    border-radius: 10px;
    padding: 8px;
    outline: none;
}}

QListWidget::item {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text_primary']};
    border-radius: 6px;
    padding: 12px;
    margin: 3px 0px;
}}

QListWidget::item:selected {{
    background-color: {COLORS['accent']};
}}

QListWidget::item:hover:!selected {{
    background-color: {COLORS['bg_medium']};
}}

/* ========== ТАБЛИЦЫ ========== */
QTableWidget {{
    background-color: {COLORS['bg_light']};
    color: {COLORS['text_primary']};
    border: 2px solid {COLORS['border']};
    border-radius: 10px;
    gridline-color: {COLORS['border']};
}}

QTableWidget::item {{
    padding: 10px;
}}

QTableWidget::item:selected {{
    background-color: {COLORS['accent']};
}}

QHeaderView::section {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text_primary']};
    border: none;
    padding: 12px;
    font-weight: 600;
}}

/* ========== СКРОЛЛБАРЫ ========== */
QScrollBar:vertical {{
    background-color: {COLORS['bg_light']};
    width: 12px;
    border-radius: 6px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['border_light']};
    border-radius: 6px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS['accent']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background-color: {COLORS['bg_light']};
    height: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:horizontal {{
    background-color: {COLORS['border_light']};
    border-radius: 6px;
    min-width: 30px;
}}

/* ========== ЧЕКБОКСЫ ========== */
QCheckBox {{
    color: {COLORS['text_primary']};
    spacing: 10px;
}}

QCheckBox::indicator {{
    width: 22px;
    height: 22px;
    border-radius: 6px;
    border: 2px solid {COLORS['border']};
    background-color: {COLORS['bg_light']};
}}

QCheckBox::indicator:checked {{
    background-color: {COLORS['accent']};
    border-color: {COLORS['accent']};
}}

QCheckBox::indicator:hover {{
    border-color: {COLORS['accent']};
}}

/* ========== ЛЕЙБЛЫ ========== */
QLabel {{
    color: {COLORS['text_primary']};
}}

QLabel[class="heading"] {{
    font-size: 18px;
    font-weight: 700;
    color: {COLORS['text_primary']};
}}

QLabel[class="subheading"] {{
    font-size: 14px;
    font-weight: 600;
    color: {COLORS['text_secondary']};
}}

QLabel[class="success"] {{
    color: {COLORS['success']};
    font-weight: 600;
}}

QLabel[class="warning"] {{
    color: {COLORS['warning']};
}}

QLabel[class="error"] {{
    color: {COLORS['error']};
}}

/* ========== ПРОГРЕСС БАР ========== */
QProgressBar {{
    background-color: {COLORS['bg_light']};
    border: none;
    border-radius: 8px;
    height: 16px;
    text-align: center;
    color: {COLORS['text_primary']};
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {COLORS['accent']}, stop:1 {COLORS['accent_light']});
    border-radius: 8px;
}}

/* ========== СТАТУСБАР ========== */
QStatusBar {{
    background-color: {COLORS['bg_medium']};
    color: {COLORS['text_secondary']};
    border-top: 1px solid {COLORS['border']};
    padding: 5px;
}}

/* ========== СПЛИТТЕР ========== */
QSplitter::handle {{
    background-color: {COLORS['border']};
}}

QSplitter::handle:horizontal {{
    width: 3px;
}}

QSplitter::handle:vertical {{
    height: 3px;
}}

QSplitter::handle:hover {{
    background-color: {COLORS['accent']};
}}

/* ========== ДИАЛОГИ ========== */
QDialog {{
    background-color: {COLORS['bg_dark']};
}}

QMessageBox {{
    background-color: {COLORS['bg_card']};
}}

QMessageBox QLabel {{
    color: {COLORS['text_primary']};
}}
"""


# Дополнительные утилиты
def apply_theme(app):
    """Применить тему к приложению"""
    app.setStyleSheet(DARK_THEME)


def get_color(name: str) -> str:
    """Получить цвет по имени"""
    return COLORS.get(name, COLORS['text_primary'])