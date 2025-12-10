"""
Главное окно DizainAI v2.0
Профессиональный интерфейс
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QTabWidget, QMenuBar, QMenu, QAction,
    QStatusBar, QFileDialog, QMessageBox, QLabel, QFrame
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QKeySequence

from config.settings import Settings
from core.project import Project

from .icons import Icons
from .styles import COLORS
from .toolbar import DrawingToolbar, StatusToolbar, EditMode
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
        self._connect_signals()
        self._update_title()

    def _setup_ui(self):
        """Настройка интерфейса"""
        self.setWindowTitle("DizainAI")
        self.setMinimumSize(1280, 800)
        self.resize(1600, 1000)

        # Центральный виджет
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # === Панель инструментов ===
        self.toolbar = DrawingToolbar()
        main_layout.addWidget(self.toolbar)

        # === Основной контент ===
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Сплиттер
        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)

        # === Левая часть: Рабочая область ===
        workspace = QWidget()
        workspace_layout = QVBoxLayout(workspace)
        workspace_layout.setContentsMargins(0, 0, 0, 0)
        workspace_layout.setSpacing(0)

        # Вкладки 2D/3D
        self.view_tabs = QTabWidget()
        self.view_tabs.setDocumentMode(True)
        self.view_tabs.setTabPosition(QTabWidget.North)

        # 2D Canvas
        canvas_container = QWidget()
        canvas_layout = QVBoxLayout(canvas_container)
        canvas_layout.setContentsMargins(0, 0, 0, 0)
        canvas_layout.setSpacing(0)

        self.canvas_2d = Canvas2D(self.project)
        canvas_layout.addWidget(self.canvas_2d, 1)

        # Статус панель
        self.status_toolbar = StatusToolbar()
        self.status_toolbar.setStyleSheet(f"background-color: {COLORS['bg_secondary']};")
        canvas_layout.addWidget(self.status_toolbar)

        self.view_tabs.addTab(canvas_container, "2D План")

        # 3D Viewport
        self.viewport_3d = Viewport3D(self.project)
        self.view_tabs.addTab(self.viewport_3d, "3D Просмотр")

        workspace_layout.addWidget(self.view_tabs)
        splitter.addWidget(workspace)

        # === Правая часть: Панели инструментов ===
        right_panel = QWidget()
        right_panel.setMaximumWidth(380)
        right_panel.setMinimumWidth(320)
        right_panel.setStyleSheet(f"background-color: {COLORS['bg_secondary']};")

        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Вкладки инструментов
        self.tool_tabs = QTabWidget()
        self.tool_tabs.setDocumentMode(True)

        self.properties_panel = PropertiesPanel(self.project)
        self.tool_tabs.addTab(self.properties_panel, "Проект")

        self.ai_panel = AIPanel(self.settings, self.project)
        self.tool_tabs.addTab(self.ai_panel, "AI Дизайн")

        self.materials_panel = MaterialsPanel(self.project)
        self.tool_tabs.addTab(self.materials_panel, "Материалы")

        right_layout.addWidget(self.tool_tabs)
        splitter.addWidget(right_panel)

        # Пропорции сплиттера
        splitter.setSizes([1200, 380])

        content_layout.addWidget(splitter)
        main_layout.addLayout(content_layout)

        # === Статусбар ===
        self._create_statusbar()

    def _create_menus(self):
        """Создание меню"""
        menubar = self.menuBar()

        # === Файл ===
        file_menu = menubar.addMenu("Файл")

        new_action = file_menu.addAction("Новый проект")
        new_action.setShortcut(QKeySequence.New)
        new_action.setIcon(Icons.get_icon(Icons.SVG_NEW))
        new_action.triggered.connect(self._new_project)

        open_action = file_menu.addAction("Открыть...")
        open_action.setShortcut(QKeySequence.Open)
        open_action.setIcon(Icons.get_icon(Icons.SVG_OPEN))
        open_action.triggered.connect(self._open_project)

        file_menu.addSeparator()

        save_action = file_menu.addAction("Сохранить")
        save_action.setShortcut(QKeySequence.Save)
        save_action.setIcon(Icons.get_icon(Icons.SVG_SAVE))
        save_action.triggered.connect(self._save_project)

        save_as_action = file_menu.addAction("Сохранить как...")
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.triggered.connect(self._save_project_as)

        file_menu.addSeparator()

        export_menu = file_menu.addMenu("Экспорт")
        export_menu.setIcon(Icons.get_icon(Icons.SVG_EXPORT))

        export_txt = export_menu.addAction("Текстовый отчёт...")
        export_txt.triggered.connect(self._export_text)

        export_csv = export_menu.addAction("Материалы (CSV)...")
        export_csv.triggered.connect(self._export_csv)

        file_menu.addSeparator()

        exit_action = file_menu.addAction("Выход")
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        # === Правка ===
        edit_menu = menubar.addMenu("Правка")

        undo_action = edit_menu.addAction("Отменить")
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.setIcon(Icons.get_icon(Icons.SVG_UNDO))

        redo_action = edit_menu.addAction("Повторить")
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.setIcon(Icons.get_icon(Icons.SVG_REDO))

        edit_menu.addSeparator()

        delete_action = edit_menu.addAction("Удалить")
        delete_action.setShortcut(QKeySequence.Delete)
        delete_action.setIcon(Icons.get_icon(Icons.SVG_DELETE))

        # === Комната ===
        room_menu = menubar.addMenu("Комната")

        add_room_action = room_menu.addAction("Добавить комнату...")
        add_room_action.setShortcut("Ctrl+R")
        add_room_action.setIcon(Icons.get_icon(Icons.SVG_PLUS))
        add_room_action.triggered.connect(self._add_room)

        # === Вид ===
        view_menu = menubar.addMenu("Вид")

        zoom_in = view_menu.addAction("Увеличить")
        zoom_in.setShortcut(QKeySequence.ZoomIn)
        zoom_in.setIcon(Icons.get_icon(Icons.SVG_ZOOM_IN))

        zoom_out = view_menu.addAction("Уменьшить")
        zoom_out.setShortcut(QKeySequence.ZoomOut)
        zoom_out.setIcon(Icons.get_icon(Icons.SVG_ZOOM_OUT))

        fit_view = view_menu.addAction("Вписать в экран")
        fit_view.setShortcut("Home")
        fit_view.setIcon(Icons.get_icon(Icons.SVG_FIT))
        fit_view.triggered.connect(self.canvas_2d.fit_to_view)

        view_menu.addSeparator()

        toggle_grid = view_menu.addAction("Показать сетку")
        toggle_grid.setCheckable(True)
        toggle_grid.setChecked(True)
        toggle_grid.setShortcut("G")
        toggle_grid.setIcon(Icons.get_icon(Icons.SVG_GRID))

        # === Настройки ===
        settings_menu = menubar.addMenu("Настройки")

        settings_action = settings_menu.addAction("Параметры...")
        settings_action.setIcon(Icons.get_icon(Icons.SVG_SETTINGS))
        settings_action.triggered.connect(self._show_settings)

        # === Справка ===
        help_menu = menubar.addMenu("Справка")

        about_action = help_menu.addAction("О программе")
        about_action.setIcon(Icons.get_icon(Icons.SVG_INFO))
        about_action.triggered.connect(self._show_about)

    def _create_statusbar(self):
        """Создание строки состояния"""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.status_label = QLabel("Готов к работе")
        self.statusbar.addWidget(self.status_label)

        # Информация о проекте
        self.project_info = QLabel()
        self.project_info.setStyleSheet(f"color: {COLORS['text_secondary']};")
        self.statusbar.addPermanentWidget(self.project_info)

        self._update_status()

    def _connect_signals(self):
        """Подключение сигналов"""
        # Тулбар
        self.toolbar.mode_changed.connect(self._on_mode_changed)
        self.toolbar.action_triggered.connect(self._on_toolbar_action)

        # Canvas
        self.canvas_2d.room_selected.connect(self._on_room_selected)

        # Панели
        self.properties_panel.project_changed.connect(self._on_project_changed)

    def _on_mode_changed(self, mode: str):
        """Смена режима редактирования"""
        self.canvas_2d.set_mode(mode)
        self.status_toolbar.set_mode(mode)

    def _on_toolbar_action(self, action: str):
        """Действие из тулбара"""
        if action == "undo":
            pass  # TODO
        elif action == "redo":
            pass  # TODO
        elif action == "delete":
            self.canvas_2d._delete_selected()
        elif action == "zoom_in":
            self.canvas_2d.scale *= 1.2
            self.canvas_2d.update()
        elif action == "zoom_out":
            self.canvas_2d.scale *= 0.8
            self.canvas_2d.update()
        elif action == "fit":
            self.canvas_2d.fit_to_view()
        elif action == "toggle_grid":
            self.canvas_2d.show_grid = not self.canvas_2d.show_grid
            self.canvas_2d.update()

    def _update_title(self):
        """Обновить заголовок окна"""
        title = f"DizainAI — {self.project.name}"
        if self.project.file_path:
            title += f" [{self.project.file_path}]"
        self.setWindowTitle(title)

    def _update_status(self):
        """Обновить строку состояния"""
        rooms = len(self.project.rooms)
        area = self.project.total_area
        self.project_info.setText(f"Комнат: {rooms}  •  Площадь: {area:.1f} м²")

    def _refresh_all(self):
        """Обновить все виджеты"""
        self.canvas_2d.update_project(self.project)
        self.viewport_3d.update_project(self.project)
        self.properties_panel.update_project(self.project)
        self.materials_panel.update_project(self.project)
        self.ai_panel.update_project(self.project)
        self._update_status()
        self._update_title()

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
            self.status_label.setText("Создан новый проект")

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
                self.status_label.setText(f"Открыт: {self.project.name}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть:\n{e}")

    def _save_project(self):
        """Сохранить проект"""
        if self.project.file_path:
            try:
                self.project.save()
                self.status_label.setText("Проект сохранён")
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
                self._update_title()
                self.status_label.setText(f"Сохранено: {file_path}")
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
                self.status_label.setText(f"Экспортировано: {file_path}")

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
                self.status_label.setText(f"Экспортировано: {file_path}")

    def _add_room(self):
        """Добавление комнаты через диалог"""
        dialog = RoomDialog(self)
        if dialog.exec_():
            room = dialog.get_room()
            if room:
                self.project.add_room(room)
                self._refresh_all()
                self.status_label.setText(f"Добавлена комната: {room.name}")

    def _show_settings(self):
        """Показать настройки"""
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec_():
            self.ai_panel._init_ai()

    def _show_about(self):
        """О программе"""
        QMessageBox.about(
            self, "О программе",
            f"""
            <h2>DizainAI</h2>
            <p>Версия 2.0</p>
            <hr>
            <p>Программа для дизайна интерьера с AI-ассистентом</p>
            <br>
            <p><b>Возможности:</b></p>
            <ul>
                <li>Создание 2D планов помещений</li>
                <li>3D визуализация</li>
                <li>AI-генерация дизайн-идей</li>
                <li>Расчёт строительных материалов</li>
            </ul>
            """
        )