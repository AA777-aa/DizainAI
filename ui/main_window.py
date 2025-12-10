"""
Главное окно приложения DizainAI
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QTabWidget, QMenuBar, QMenu, QAction,
    QToolBar, QStatusBar, QFileDialog, QMessageBox,
    QLabel, QDockWidget
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QKeySequence

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
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)

        # Центральный виджет
        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)

        # Главный сплиттер
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        # Левая панель - 2D/3D вид
        view_tabs = QTabWidget()

        # 2D Canvas
        self.canvas_2d = Canvas2D(self.project)
        view_tabs.addTab(self.canvas_2d, "2D План")

        # 3D Viewport
        self.viewport_3d = Viewport3D(self.project)
        view_tabs.addTab(self.viewport_3d, "3D Вид")

        splitter.addWidget(view_tabs)

        # Правая панель - вкладки инструментов
        right_tabs = QTabWidget()
        right_tabs.setMaximumWidth(400)
        right_tabs.setMinimumWidth(300)

        # Панель свойств
        self.properties_panel = PropertiesPanel(self.project)
        right_tabs.addTab(self.properties_panel, "Свойства")

        # AI панель
        self.ai_panel = AIPanel(self.settings, self.project)
        right_tabs.addTab(self.ai_panel, "AI Дизайнер")

        # Панель материалов
        self.materials_panel = MaterialsPanel(self.project)
        right_tabs.addTab(self.materials_panel, "Материалы")

        splitter.addWidget(right_tabs)

        # Пропорции сплиттера
        splitter.setSizes([900, 350])

    def _create_menus(self):
        """Создание меню"""
        menubar = self.menuBar()

        # Файл
        file_menu = menubar.addMenu("&Файл")

        new_action = QAction("&Новый проект", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self._new_project)
        file_menu.addAction(new_action)

        open_action = QAction("&Открыть...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self._open_project)
        file_menu.addAction(open_action)

        save_action = QAction("&Сохранить", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self._save_project)
        file_menu.addAction(save_action)

        save_as_action = QAction("Сохранить &как...", self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.triggered.connect(self._save_project_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        export_menu = file_menu.addMenu("&Экспорт")
        export_txt = QAction("Текстовый отчёт...", self)
        export_txt.triggered.connect(self._export_text)
        export_menu.addAction(export_txt)

        export_csv = QAction("Материалы (CSV)...", self)
        export_csv.triggered.connect(self._export_csv)
        export_menu.addAction(export_csv)

        file_menu.addSeparator()

        exit_action = QAction("&Выход", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Правка
        edit_menu = menubar.addMenu("&Правка")

        undo_action = QAction("&Отменить", self)
        undo_action.setShortcut(QKeySequence.Undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("&Повторить", self)
        redo_action.setShortcut(QKeySequence.Redo)
        edit_menu.addAction(redo_action)

        # Комната
        room_menu = menubar.addMenu("&Комната")

        add_room_action = QAction("&Добавить комнату...", self)
        add_room_action.setShortcut("Ctrl+R")
        add_room_action.triggered.connect(self._add_room)
        room_menu.addAction(add_room_action)

        add_rect_room = QAction("Добавить &прямоугольную...", self)
        add_rect_room.triggered.connect(self._add_rectangular_room)
        room_menu.addAction(add_rect_room)

        # Настройки
        settings_menu = menubar.addMenu("&Настройки")

        settings_action = QAction("&Параметры...", self)
        settings_action.triggered.connect(self._show_settings)
        settings_menu.addAction(settings_action)

        # Справка
        help_menu = menubar.addMenu("&Справка")

        about_action = QAction("&О программе", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _create_toolbar(self):
        """Создание панели инструментов"""
        toolbar = QToolBar("Основная")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)

        toolbar.addAction("📄 Новый", self._new_project)
        toolbar.addAction("📂 Открыть", self._open_project)
        toolbar.addAction("💾 Сохранить", self._save_project)
        toolbar.addSeparator()
        toolbar.addAction("🏠 Добавить комнату", self._add_rectangular_room)
        toolbar.addSeparator()
        toolbar.addAction("⚙️ Настройки", self._show_settings)

    def _create_statusbar(self):
        """Создание строки состояния"""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.status_label = QLabel("Готов")
        self.statusbar.addWidget(self.status_label)

        self.area_label = QLabel("")
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

        self.area_label.setText(
            f"Комнат: {rooms_count} | Площадь: {total_area:.1f} м²"
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
            "Создать новый проект? Несохранённые изменения будут потеряны.",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.project = Project(name="Новый проект")
            self._refresh_all()
            self.setWindowTitle("DizainAI - Новый проект")

    def _open_project(self):
        """Открыть проект"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть проект",
            "", "DizainAI проекты (*.dizain);;Все файлы (*)"
        )

        if file_path:
            try:
                self.project = Project.load(file_path)
                self._refresh_all()
                self.setWindowTitle(f"DizainAI - {self.project.name}")
                self.statusbar.showMessage(f"Открыт: {file_path}", 3000)
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
                self.statusbar.showMessage("Сохранено", 2000)
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
                self.statusbar.showMessage(f"Сохранено: {file_path}", 3000)
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
                self.statusbar.showMessage(f"Экспортировано: {file_path}", 3000)

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
                self.statusbar.showMessage(f"Экспортировано: {file_path}", 3000)

    def _add_room(self):
        """Добавить комнату через диалог"""
        dialog = RoomDialog(self)
        if dialog.exec_():
            room = dialog.get_room()
            self.project.add_room(room)
            self._refresh_all()

    def _add_rectangular_room(self):
        """Быстрое добавление прямоугольной комнаты"""
        dialog = RoomDialog(self, rectangular=True)
        if dialog.exec_():
            room = dialog.get_room()
            self.project.add_room(room)
            self._refresh_all()

    def _show_settings(self):
        """Показать настройки"""
        dialog = SettingsDialog(self.settings, self)
        dialog.exec_()

    def _show_about(self):
        """О программе"""
        QMessageBox.about(
            self, "О программе DizainAI",
            "<h2>DizainAI</h2>"
            "<p>Версия 1.0.0</p>"
            "<p>Программа для дизайна интерьера с AI-ассистентом.</p>"
            "<p>Возможности:</p>"
            "<ul>"
            "<li>Создание 2D планов помещений</li>"
            "<li>3D визуализация</li>"
            "<li>AI-генерация дизайн-идей</li>"
            "<li>Расчёт строительных материалов</li>"
            "</ul>"
        )