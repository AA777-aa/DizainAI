"""
Главное окно приложения DizainAI - Современный дизайн
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QTabWidget, QMenuBar, QMenu, QAction,
    QToolBar, QStatusBar, QFileDialog, QMessageBox,
    QLabel, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QKeySequence, QFont

from config.settings import Settings
from core.project import Project
from core.room import Room

from .canvas_2d import Canvas2D
from .viewport_3d import Viewport3D
from .panels.properties_panel import PropertiesPanel
from .panels.ai_panel import AIPanel
from .panels.materials_panel import MaterialsPanel
from .dialogs.room_dialog import RoomDialog
from .dialogs.settings_dialog import SettingsDialog


class MainWindow(QMainWindow):
    """Главное окно DizainAI"""

    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.project = Project(name="Новый проект")

        self._setup_ui()
        self._create_menus()
        self._create_toolbar()
        self._create_statusbar()
        self._connect_signals()

    def _setup_ui(self):
        """Настройка интерфейса"""
        self.setWindowTitle("DizainAI - Дизайн интерьера")
        self.setMinimumSize(1280, 800)
        self.resize(1500, 950)

        # Центральный виджет
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # === Главный сплиттер ===
        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)
        main_layout.addWidget(splitter)

        # === ЛЕВАЯ ЧАСТЬ: Рабочая область ===
        workspace = QWidget()
        workspace_layout = QVBoxLayout(workspace)
        workspace_layout.setContentsMargins(10, 10, 5, 10)
        workspace_layout.setSpacing(0)

        # Вкладки 2D/3D
        self.view_tabs = QTabWidget()
        self.view_tabs.setDocumentMode(True)

        # 2D Canvas
        self.canvas_2d = Canvas2D(self.project)
        self.view_tabs.addTab(self.canvas_2d, "📐  2D План")

        # 3D Viewport
        self.viewport_3d = Viewport3D(self.project)
        self.view_tabs.addTab(self.viewport_3d, "🏠  3D Просмотр")

        workspace_layout.addWidget(self.view_tabs)
        splitter.addWidget(workspace)

        # === ПРАВАЯ ЧАСТЬ: Панели инструментов ===
        right_panel = QWidget()
        right_panel.setMaximumWidth(420)
        right_panel.setMinimumWidth(360)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(5, 10, 10, 10)
        right_layout.setSpacing(0)

        # Вкладки инструментов
        self.tool_tabs = QTabWidget()

        # Панель свойств
        self.properties_panel = PropertiesPanel(self.project)
        self.tool_tabs.addTab(self.properties_panel, "📋  Проект")

        # AI панель
        self.ai_panel = AIPanel(self.settings, self.project)
        self.tool_tabs.addTab(self.ai_panel, "🤖  AI Дизайн")

        # Панель материалов
        self.materials_panel = MaterialsPanel(self.project)
        self.tool_tabs.addTab(self.materials_panel, "🧱  Материалы")

        right_layout.addWidget(self.tool_tabs)
        splitter.addWidget(right_panel)

        # Пропорции сплиттера
        splitter.setSizes([1050, 400])

    def _create_menus(self):
        """Создание меню"""
        menubar = self.menuBar()

        # === Файл ===
        file_menu = menubar.addMenu("Файл")

        new_action = QAction("🆕  Новый проект", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self._new_project)
        file_menu.addAction(new_action)

        open_action = QAction("📂  Открыть...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self._open_project)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        save_action = QAction("💾  Сохранить", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self._save_project)
        file_menu.addAction(save_action)

        save_as_action = QAction("💾  Сохранить как...", self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.triggered.connect(self._save_project_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        # Подменю экспорта
        export_menu = file_menu.addMenu("📤  Экспорт")

        export_txt = QAction("📄  Текстовый отчёт...", self)
        export_txt.triggered.connect(self._export_text)
        export_menu.addAction(export_txt)

        export_csv = QAction("📊  Материалы (CSV)...", self)
        export_csv.triggered.connect(self._export_csv)
        export_menu.addAction(export_csv)

        file_menu.addSeparator()

        exit_action = QAction("🚪  Выход", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # === Комната ===
        room_menu = menubar.addMenu("Комната")

        add_room_action = QAction("➕  Добавить комнату...", self)
        add_room_action.setShortcut("Ctrl+R")
        add_room_action.triggered.connect(self._add_rectangular_room)
        room_menu.addAction(add_room_action)

        # === Настройки ===
        settings_menu = menubar.addMenu("Настройки")

        settings_action = QAction("⚙️  Параметры...", self)
        settings_action.triggered.connect(self._show_settings)
        settings_menu.addAction(settings_action)

        # === Справка ===
        help_menu = menubar.addMenu("Справка")

        about_action = QAction("ℹ️  О программе", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _create_toolbar(self):
        """Создание панели инструментов"""
        toolbar = QToolBar("Главная")
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addToolBar(toolbar)

        # Кнопки с понятными текстами
        new_btn = toolbar.addAction("📄 Новый")
        new_btn.triggered.connect(self._new_project)
        new_btn.setToolTip("Создать новый проект (Ctrl+N)")

        open_btn = toolbar.addAction("📂 Открыть")
        open_btn.triggered.connect(self._open_project)
        open_btn.setToolTip("Открыть проект (Ctrl+O)")

        save_btn = toolbar.addAction("💾 Сохранить")
        save_btn.triggered.connect(self._save_project)
        save_btn.setToolTip("Сохранить проект (Ctrl+S)")

        toolbar.addSeparator()

        add_room_btn = toolbar.addAction("🏠 Добавить комнату")
        add_room_btn.triggered.connect(self._add_rectangular_room)
        add_room_btn.setToolTip("Добавить новую комнату (Ctrl+R)")

        toolbar.addSeparator()

        settings_btn = toolbar.addAction("⚙️ Настройки")
        settings_btn.triggered.connect(self._show_settings)
        settings_btn.setToolTip("Открыть настройки")

    def _create_statusbar(self):
        """Создание строки состояния"""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Левая часть - статус
        self.status_label = QLabel("✅ Готов к работе")
        self.statusbar.addWidget(self.status_label)

        # Правая часть - информация о проекте
        self.area_label = QLabel()
        self.area_label.setStyleSheet("font-weight: bold; color: #10b981;")
        self.statusbar.addPermanentWidget(self.area_label)

        self._update_status()

    def _connect_signals(self):
        """Подключение сигналов"""
        self.canvas_2d.room_selected.connect(self._on_room_selected)
        self.properties_panel.project_changed.connect(self._on_project_changed)

    def _update_status(self):
        """Обновить строку состояния"""
        rooms_count = len(self.project.rooms)
        total_area = self.project.total_area

        rooms_text = "комната" if rooms_count == 1 else "комнат"
        self.area_label.setText(
            f"🏠 {rooms_count} {rooms_text}  |  📐 {total_area:.1f} м²"
        )

    def _refresh_all(self):
        """Обновить все виджеты"""
        self.canvas_2d.update_project(self.project)
        self.viewport_3d.update_project(self.project)
        self.properties_panel.update_project(self.project)
        self.materials_panel.update_project(self.project)
        self.ai_panel.update_project(self.project)
        self._update_status()

    # === Слоты ===

    def _on_room_selected(self, room_id: str):
        """Выбрана комната"""
        self.properties_panel.select_room(room_id)

    def _on_project_changed(self):
        """Проект изменён"""
        self._refresh_all()

    def _new_project(self):
        """Новый проект"""
        reply = QMessageBox.question(
            self, "Новый проект",
            "Создать новый проект?\n\nНесохранённые изменения будут потеряны.",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.project = Project(name="Новый проект")
            self._refresh_all()
            self.setWindowTitle("DizainAI - Новый проект")
            self.status_label.setText("🆕 Создан новый проект")

    def _open_project(self):
        """Открыть проект"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть проект", "",
            "DizainAI проекты (*.dizain);;Все файлы (*)"
        )

        if file_path:
            try:
                self.project = Project.load(file_path)
                self._refresh_all()
                self.setWindowTitle(f"DizainAI - {self.project.name}")
                self.status_label.setText(f"📂 Открыт: {self.project.name}")
            except Exception as e:
                QMessageBox.critical(
                    self, "Ошибка",
                    f"Не удалось открыть проект:\n{e}"
                )

    def _save_project(self):
        """Сохранить проект"""
        if self.project.file_path:
            try:
                self.project.save()
                self.status_label.setText("💾 Проект сохранён")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения:\n{e}")
        else:
            self._save_project_as()

    def _save_project_as(self):
        """Сохранить как"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить проект",
            f"{self.project.name}.dizain",
            "DizainAI проекты (*.dizain)"
        )

        if file_path:
            try:
                self.project.save(file_path)
                self.setWindowTitle(f"DizainAI - {self.project.name}")
                self.status_label.setText(f"💾 Сохранено: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения:\n{e}")

    def _export_text(self):
        """Экспорт в текст"""
        from utils.export import ProjectExporter

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт отчёта",
            f"{self.project.name}_отчёт.txt",
            "Текстовые файлы (*.txt)"
        )

        if file_path:
            if ProjectExporter.to_text_report(self.project, file_path):
                self.status_label.setText(f"📤 Экспортировано: {file_path}")

    def _export_csv(self):
        """Экспорт материалов в CSV"""
        from utils.export import ProjectExporter

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт материалов",
            f"{self.project.name}_материалы.csv",
            "CSV файлы (*.csv)"
        )

        if file_path:
            if ProjectExporter.to_csv_materials(self.project, file_path):
                self.status_label.setText(f"📤 Экспортировано: {file_path}")

    def _add_rectangular_room(self):
        """Добавление комнаты"""
        dialog = RoomDialog(self)
        if dialog.exec_():
            room = dialog.get_room()
            if room:
                self.project.add_room(room)
                self._refresh_all()
                self.status_label.setText(f"🏠 Добавлена комната: {room.name}")

    def _show_settings(self):
        """Показать настройки"""
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec_():
            # Обновляем AI панель при изменении настроек
            self.ai_panel._init_ai()

    def _show_about(self):
        """О программе"""
        QMessageBox.about(
            self, "О программе DizainAI",
            """
            <div style="text-align: center;">
            <h2 style="color: #4f46e5;">🏠 DizainAI</h2>
            <p style="font-size: 14px;">Версия 1.0.0</p>
            <hr>
            <p>Программа для дизайна интерьера<br>с AI-ассистентом</p>
            <br>
            <b>Возможности:</b>
            <ul style="text-align: left;">
            <li>📐 Создание 2D планов помещений</li>
            <li>🏠 3D визуализация</li>
            <li>🤖 AI-генерация дизайн-идей</li>
            <li>🧱 Расчёт строительных материалов</li>
            </ul>
            </div>
            """
        )