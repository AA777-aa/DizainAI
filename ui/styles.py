"""
Единая система стилей DizainAI v2.0
Профессиональный дизайн без эмодзи
"""

COLORS = {
    # Фоны
    'bg_primary': '#0f172a',
    'bg_secondary': '#1e293b',
    'bg_tertiary': '#334155',
    'bg_card': '#1e293b',
    'bg_hover': '#334155',
    'bg_active': '#475569',

    # Акценты
    'accent': '#6366f1',
    'accent_hover': '#818cf8',
    'accent_muted': '#4f46e5',

    # Семантические
    'success': '#10b981',
    'success_muted': '#059669',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#3b82f6',

    # Текст
    'text_primary': '#f8fafc',
    'text_secondary': '#94a3b8',
    'text_muted': '#64748b',
    'text_disabled': '#475569',

    # Границы
    'border': '#334155',
    'border_light': '#475569',
    'border_focus': '#6366f1',

    # Специальные элементы
    'wall': '#e2e8f0',
    'wall_selected': '#6366f1',
    'window': '#38bdf8',
    'door': '#a3e635',
    'furniture': '#f472b6',
    'grid': '#1e293b',
    'grid_major': '#334155',
}


DARK_THEME = f"""
/* ============================================
   ОСНОВНЫЕ СТИЛИ
   ============================================ */

* {{
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}}

QMainWindow, QWidget {{
    background-color: {COLORS['bg_primary']};
    color: {COLORS['text_primary']};
    font-size: 13px;
}}

/* ============================================
   МЕНЮ
   ============================================ */

QMenuBar {{
    background-color: {COLORS['bg_secondary']};
    border-bottom: 1px solid {COLORS['border']};
    padding: 4px 8px;
}}

QMenuBar::item {{
    background: transparent;
    padding: 8px 12px;
    border-radius: 6px;
    color: {COLORS['text_secondary']};
}}

QMenuBar::item:selected,
QMenuBar::item:pressed {{
    background-color: {COLORS['bg_hover']};
    color: {COLORS['text_primary']};
}}

QMenu {{
    background-color: {COLORS['bg_secondary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 4px;
}}

QMenu::item {{
    padding: 8px 32px 8px 12px;
    border-radius: 4px;
    color: {COLORS['text_secondary']};
}}

QMenu::item:selected {{
    background-color: {COLORS['accent']};
    color: {COLORS['text_primary']};
}}

QMenu::separator {{
    height: 1px;
    background-color: {COLORS['border']};
    margin: 4px 8px;
}}

QMenu::icon {{
    margin-left: 8px;
}}

/* ============================================
   ТУЛБАР
   ============================================ */

QToolBar {{
    background-color: {COLORS['bg_secondary']};
    border: none;
    border-bottom: 1px solid {COLORS['border']};
    padding: 8px 12px;
    spacing: 4px;
}}

QToolBar::separator {{
    width: 1px;
    background-color: {COLORS['border']};
    margin: 4px 8px;
}}

QToolButton {{
    background-color: transparent;
    border: none;
    border-radius: 6px;
    padding: 8px;
    color: {COLORS['text_secondary']};
}}

QToolButton:hover {{
    background-color: {COLORS['bg_hover']};
    color: {COLORS['text_primary']};
}}

QToolButton:pressed {{
    background-color: {COLORS['bg_active']};
}}

QToolButton:checked {{
    background-color: {COLORS['accent']};
    color: {COLORS['text_primary']};
}}

/* ============================================
   КНОПКИ
   ============================================ */

QPushButton {{
    background-color: {COLORS['bg_tertiary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 10px 20px;
    color: {COLORS['text_primary']};
    font-weight: 500;
}}

QPushButton:hover {{
    background-color: {COLORS['bg_hover']};
    border-color: {COLORS['border_light']};
}}

QPushButton:pressed {{
    background-color: {COLORS['bg_active']};
}}

QPushButton:disabled {{
    background-color: {COLORS['bg_secondary']};
    color: {COLORS['text_disabled']};
    border-color: {COLORS['border']};
}}

/* ============================================
   ПОЛЯ ВВОДА
   ============================================ */

QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {COLORS['bg_tertiary']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 10px 12px;
    color: {COLORS['text_primary']};
    selection-background-color: {COLORS['accent']};
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border-color: {COLORS['border_focus']};
}}

QLineEdit:disabled {{
    background-color: {COLORS['bg_secondary']};
    color: {COLORS['text_disabled']};
}}

QLineEdit::placeholder {{
    color: {COLORS['text_muted']};
}}

/* ============================================
   ВЫПАДАЮЩИЕ СПИСКИ
   ============================================ */

QComboBox {{
    background-color: {COLORS['bg_tertiary']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 10px 12px;
    padding-right: 30px;
    color: {COLORS['text_primary']};
}}

QComboBox:hover {{
    border-color: {COLORS['border_light']};
}}

QComboBox:focus {{
    border-color: {COLORS['border_focus']};
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

QComboBox::down-arrow {{
    image: none;
    border: none;
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid {COLORS['text_secondary']};
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS['bg_secondary']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 4px;
    selection-background-color: {COLORS['accent']};
}}

/* ============================================
   СПИНБОКСЫ
   ============================================ */

QSpinBox, QDoubleSpinBox {{
    background-color: {COLORS['bg_tertiary']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px 12px;
    color: {COLORS['text_primary']};
}}

QSpinBox:focus, QDoubleSpinBox:focus {{
    border-color: {COLORS['border_focus']};
}}

QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
    background-color: {COLORS['bg_hover']};
    border: none;
    width: 20px;
    border-radius: 3px;
    margin: 2px;
}}

QSpinBox::up-button:hover, QSpinBox::down-button:hover,
QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {{
    background-color: {COLORS['accent']};
}}

/* ============================================
   ВКЛАДКИ
   ============================================ */

QTabWidget::pane {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    margin-top: -1px;
}}

QTabBar {{
    background: transparent;
}}

QTabBar::tab {{
    background-color: transparent;
    border: none;
    padding: 12px 20px;
    color: {COLORS['text_secondary']};
    font-weight: 500;
    border-bottom: 2px solid transparent;
    margin-right: 4px;
}}

QTabBar::tab:hover {{
    color: {COLORS['text_primary']};
    background-color: {COLORS['bg_hover']};
    border-radius: 6px 6px 0 0;
}}

QTabBar::tab:selected {{
    color: {COLORS['accent']};
    border-bottom-color: {COLORS['accent']};
}}

/* ============================================
   ГРУППЫ
   ============================================ */

QGroupBox {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
    margin-top: 16px;
    padding: 16px;
    padding-top: 24px;
}}

    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 16px;
        top: 8px;
        color: {COLORS['text_secondary']};
        font-weight: 600;
        font-size: 12px;
        letter-spacing: 0.5px;
    }}

/* ============================================
   СПИСКИ
   ============================================ */

QListWidget {{
    background-color: {COLORS['bg_tertiary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 4px;
    outline: none;
}}

QListWidget::item {{
    background-color: transparent;
    border-radius: 6px;
    padding: 10px 12px;
    margin: 2px 0;
    color: {COLORS['text_secondary']};
}}

QListWidget::item:hover {{
    background-color: {COLORS['bg_hover']};
    color: {COLORS['text_primary']};
}}

QListWidget::item:selected {{
    background-color: {COLORS['accent']};
    color: white;
}}

/* ============================================
   ТАБЛИЦЫ
   ============================================ */

QTableWidget {{
    background-color: {COLORS['bg_tertiary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    gridline-color: {COLORS['border']};
}}

QTableWidget::item {{
    padding: 8px 12px;
    border: none;
}}

QTableWidget::item:selected {{
    background-color: {COLORS['accent']};
}}

QHeaderView::section {{
    background-color: {COLORS['bg_secondary']};
    border: none;
    border-bottom: 1px solid {COLORS['border']};
    padding: 12px;
    font-weight: 600;
    color: {COLORS['text_secondary']};
}}

/* ============================================
   СКРОЛЛБАРЫ
   ============================================ */

QScrollBar:vertical {{
    background-color: transparent;
    width: 8px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['border']};
    border-radius: 4px;
    min-height: 40px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS['border_light']};
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0;
}}

QScrollBar:horizontal {{
    background-color: transparent;
    height: 8px;
}}

QScrollBar::handle:horizontal {{
    background-color: {COLORS['border']};
    border-radius: 4px;
    min-width: 40px;
}}

/* ============================================
   ЧЕКБОКСЫ И РАДИОКНОПКИ
   ============================================ */

QCheckBox {{
    spacing: 8px;
    color: {COLORS['text_primary']};
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid {COLORS['border']};
    background-color: {COLORS['bg_tertiary']};
}}

QCheckBox::indicator:hover {{
    border-color: {COLORS['border_light']};
}}

QCheckBox::indicator:checked {{
    background-color: {COLORS['accent']};
    border-color: {COLORS['accent']};
}}

/* ============================================
   ПРОГРЕСС БАР
   ============================================ */

QProgressBar {{
    background-color: {COLORS['bg_tertiary']};
    border: none;
    border-radius: 4px;
    height: 8px;
    text-align: center;
}}

QProgressBar::chunk {{
    background-color: {COLORS['accent']};
    border-radius: 4px;
}}

/* ============================================
   СТАТУСБАР
   ============================================ */

QStatusBar {{
    background-color: {COLORS['bg_secondary']};
    border-top: 1px solid {COLORS['border']};
    padding: 4px 12px;
    color: {COLORS['text_secondary']};
}}

QStatusBar::item {{
    border: none;
}}

/* ============================================
   СПЛИТТЕР
   ============================================ */

QSplitter::handle {{
    background-color: {COLORS['border']};
}}

QSplitter::handle:horizontal {{
    width: 1px;
}}

QSplitter::handle:vertical {{
    height: 1px;
}}

QSplitter::handle:hover {{
    background-color: {COLORS['accent']};
}}

/* ============================================
   ДИАЛОГИ
   ============================================ */

QDialog {{
    background-color: {COLORS['bg_primary']};
}}

QMessageBox {{
    background-color: {COLORS['bg_secondary']};
}}

/* ============================================
   КАСТОМНЫЕ КЛАССЫ
   ============================================ */

#card {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
}}

#sectionHeader {{
    font-size: 14px;
    font-weight: 600;
    color: {COLORS['text_primary']};
}}

#propertyLabel {{
    color: {COLORS['text_secondary']};
    font-size: 12px;
}}

#statTitle {{
    color: {COLORS['text_muted']};
    font-size: 11px;
    letter-spacing: 0.5px;
}}

/* ============================================
   ТУЛТИПЫ
   ============================================ */

QToolTip {{
    background-color: {COLORS['bg_secondary']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px 12px;
    color: {COLORS['text_primary']};
    font-size: 12px;
}}
"""


def apply_theme(app):
    """Применить тему к приложению"""
    app.setStyleSheet(DARK_THEME)


def get_color(name: str) -> str:
    """Получить цвет по имени"""
    return COLORS.get(name, COLORS['text_primary'])