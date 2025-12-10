"""
Диалог добавления комнаты - современный дизайн
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QSpinBox, QPushButton, QLabel,
    QGroupBox, QComboBox, QMessageBox, QCheckBox,
    QFrame
)
from PyQt5.QtCore import Qt

from core.room import Room, Wall, Point2D, Window, Door


class RoomDialog(QDialog):
    """Диалог создания комнаты"""

    ROOM_PRESETS = {
        "custom": ("Произвольная", 0, 0),
        "living": ("🛋️ Гостиная", 5000, 6000),
        "bedroom": ("🛏️ Спальня", 4000, 4500),
        "bedroom_small": ("🛏️ Спальня малая", 3000, 3500),
        "kitchen": ("🍳 Кухня", 3500, 4000),
        "bathroom": ("🚿 Ванная", 2000, 2500),
        "toilet": ("🚽 Туалет", 1200, 1800),
        "hallway": ("🚪 Прихожая", 2000, 4000),
        "office": ("💼 Кабинет", 3000, 3500),
        "kids": ("🧸 Детская", 3500, 4000),
    }

    def __init__(self, parent=None, rectangular=False):
        super().__init__(parent)
        self.rectangular = rectangular
        self.room = None

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Настройка интерфейса"""
        self.setWindowTitle("Добавить комнату")
        self.setMinimumWidth(450)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # === ЗАГОЛОВОК ===
        header = QLabel("🏠 Создание новой комнаты")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #f8fafc;")
        layout.addWidget(header)

        # === ОСНОВНЫЕ ПАРАМЕТРЫ ===
        main_group = QGroupBox("Основные параметры")
        main_layout = QVBoxLayout(main_group)
        main_layout.setSpacing(12)

        # Шаблон
        preset_layout = QHBoxLayout()
        preset_label = QLabel("Шаблон:")
        preset_label.setMinimumWidth(100)
        self.preset_combo = QComboBox()
        for key, (name, w, h) in self.ROOM_PRESETS.items():
            self.preset_combo.addItem(name, key)
        preset_layout.addWidget(preset_label)
        preset_layout.addWidget(self.preset_combo, 1)
        main_layout.addLayout(preset_layout)

        # Название
        name_layout = QHBoxLayout()
        name_label = QLabel("Название:")
        name_label.setMinimumWidth(100)
        self.name_edit = QLineEdit("Новая комната")
        self.name_edit.setPlaceholderText("Введите название комнаты")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit, 1)
        main_layout.addLayout(name_layout)

        layout.addWidget(main_group)

        # === РАЗМЕРЫ ===
        size_group = QGroupBox("Размеры")
        size_layout = QVBoxLayout(size_group)
        size_layout.setSpacing(12)

        # Ширина
        width_layout = QHBoxLayout()
        width_label = QLabel("Ширина:")
        width_label.setMinimumWidth(100)
        self.width_spin = QSpinBox()
        self.width_spin.setRange(500, 50000)
        self.width_spin.setValue(4000)
        self.width_spin.setSuffix(" мм")
        self.width_spin.setSingleStep(100)
        width_layout.addWidget(width_label)
        width_layout.addWidget(self.width_spin, 1)
        size_layout.addLayout(width_layout)

        # Длина
        length_layout = QHBoxLayout()
        length_label = QLabel("Длина:")
        length_label.setMinimumWidth(100)
        self.length_spin = QSpinBox()
        self.length_spin.setRange(500, 50000)
        self.length_spin.setValue(5000)
        self.length_spin.setSuffix(" мм")
        self.length_spin.setSingleStep(100)
        length_layout.addWidget(length_label)
        length_layout.addWidget(self.length_spin, 1)
        size_layout.addLayout(length_layout)

        # Высота
        height_layout = QHBoxLayout()
        height_label = QLabel("Высота:")
        height_label.setMinimumWidth(100)
        self.height_spin = QSpinBox()
        self.height_spin.setRange(2000, 5000)
        self.height_spin.setValue(2700)
        self.height_spin.setSuffix(" мм")
        self.height_spin.setSingleStep(50)
        height_layout.addWidget(height_label)
        height_layout.addWidget(self.height_spin, 1)
        size_layout.addLayout(height_layout)

        # Отображение площади
        self.area_frame = QFrame()
        self.area_frame.setStyleSheet("""
            QFrame {
                background-color: #1f2937;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        area_layout = QHBoxLayout(self.area_frame)
        area_layout.addWidget(QLabel("📐 Площадь:"))
        self.area_label = QLabel("20.00 м²")
        self.area_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #10b981;")
        area_layout.addWidget(self.area_label)
        area_layout.addStretch()
        size_layout.addWidget(self.area_frame)

        layout.addWidget(size_group)

        # === ЭЛЕМЕНТЫ ===
        elements_group = QGroupBox("Добавить элементы")
        elements_layout = QVBoxLayout(elements_group)
        elements_layout.setSpacing(10)

        # Окно
        window_layout = QHBoxLayout()
        self.add_window_check = QCheckBox("🪟 Окно")
        self.add_window_check.setChecked(True)
        window_layout.addWidget(self.add_window_check)
        window_layout.addWidget(QLabel("на стене:"))
        self.window_wall_combo = QComboBox()
        self.window_wall_combo.addItems(["Нижняя", "Правая", "Верхняя", "Левая"])
        self.window_wall_combo.setCurrentIndex(2)
        window_layout.addWidget(self.window_wall_combo)
        window_layout.addStretch()
        elements_layout.addLayout(window_layout)

        # Дверь
        door_layout = QHBoxLayout()
        self.add_door_check = QCheckBox("🚪 Дверь")
        self.add_door_check.setChecked(True)
        door_layout.addWidget(self.add_door_check)
        door_layout.addWidget(QLabel("на стене:"))
        self.door_wall_combo = QComboBox()
        self.door_wall_combo.addItems(["Нижняя", "Правая", "Верхняя", "Левая"])
        self.door_wall_combo.setCurrentIndex(0)
        door_layout.addWidget(self.door_wall_combo)
        door_layout.addStretch()
        elements_layout.addLayout(door_layout)

        layout.addWidget(elements_group)

        # === КНОПКИ ===
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        cancel_btn = QPushButton("Отмена")
        cancel_btn.setMinimumHeight(45)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        ok_btn = QPushButton("✅ Создать комнату")
        ok_btn.setMinimumHeight(45)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #4f46e5;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6366f1;
            }
        """)
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(self._create_room)
        buttons_layout.addWidget(ok_btn)

        layout.addLayout(buttons_layout)

        self._update_area()

    def _connect_signals(self):
        """Подключение сигналов"""
        self.preset_combo.currentIndexChanged.connect(self._on_preset_changed)
        self.width_spin.valueChanged.connect(self._update_area)
        self.length_spin.valueChanged.connect(self._update_area)

    def _on_preset_changed(self, index):
        """Выбор пресета"""
        key = self.preset_combo.currentData()
        if key and key != "custom":
            name, width, length = self.ROOM_PRESETS[key]
            # Убираем эмодзи из названия
            clean_name = name.split(" ", 1)[-1] if " " in name else name
            self.name_edit.setText(clean_name)
            self.width_spin.setValue(width)
            self.length_spin.setValue(length)

    def _update_area(self):
        """Обновить отображение площади"""
        width = self.width_spin.value()
        length = self.length_spin.value()
        area = (width * length) / 1_000_000
        self.area_label.setText(f"{area:.2f} м²")

    def _create_room(self):
        """Создать комнату"""
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название комнаты")
            return

        width = self.width_spin.value()
        length = self.length_spin.value()
        height = self.height_spin.value()

        # Создаём прямоугольную комнату
        self.room = Room.create_rectangular(name, width, length, height)

        # Добавляем окно
        if self.add_window_check.isChecked() and len(self.room.walls) >= 4:
            wall_idx = self.window_wall_combo.currentIndex()
            wall = self.room.walls[wall_idx]

            window_width = min(1200, wall.length * 0.6)
            window_pos = (wall.length - window_width) / 2

            window = Window(
                position=window_pos,
                width=window_width,
                height=1400,
                sill_height=900
            )
            wall.windows.append(window)

        # Добавляем дверь
        if self.add_door_check.isChecked() and len(self.room.walls) >= 4:
            wall_idx = self.door_wall_combo.currentIndex()
            wall = self.room.walls[wall_idx]

            door = Door(
                position=200,
                width=900,
                height=2100
            )
            wall.doors.append(door)

        self.accept()

    def get_room(self) -> Room:
        """Получить созданную комнату"""
        return self.room