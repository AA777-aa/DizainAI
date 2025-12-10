"""
Панель AI-ассистента для генерации дизайна
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QTextEdit, QPushButton, QGroupBox,
    QLineEdit, QProgressBar, QMessageBox, QScrollArea
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from config.settings import Settings
from core.project import Project
from ai.gpt_client import GPTClient
from ai.design_generator import DesignGenerator


class AIWorker(QThread):
    """Фоновый поток для AI запросов"""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    progress = pyqtSignal(str)

    def __init__(self, generator, room, style, preferences):
        super().__init__()
        self.generator = generator
        self.room = room
        self.style = style
        self.preferences = preferences

    def run(self):
        try:
            self.progress.emit("Генерация дизайна...")
            result = self.generator.generate_design(
                self.room,
                self.style,
                self.preferences,
                callback=lambda msg: self.progress.emit(msg)
            )

            if result:
                self.finished.emit(result.description)
            else:
                self.error.emit("Не удалось получить результат")

        except Exception as e:
            self.error.emit(str(e))


class AIPanel(QWidget):
    """Панель AI дизайнера"""

    STYLES = {
        "scandinavian": "🇸🇪 Скандинавский",
        "minimalist": "⬜ Минимализм",
        "modern": "🏢 Современный",
        "classic": "🏛️ Классический",
        "loft": "🏭 Лофт",
        "japandi": "🎌 Джапанди",
        "provence": "🌻 Прованс",
        "industrial": "⚙️ Индустриальный"
    }

    def __init__(self, settings: Settings, project: Project, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.project = project
        self.gpt_client = None
        self.generator = None
        self.worker = None

        self._setup_ui()
        self._init_ai()

    def _setup_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Статус API
        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        # Генератор дизайна
        gen_group = QGroupBox("🎨 Генератор дизайна")
        gen_layout = QVBoxLayout(gen_group)

        # Выбор комнаты
        room_layout = QHBoxLayout()
        room_layout.addWidget(QLabel("Комната:"))
        self.room_combo = QComboBox()
        room_layout.addWidget(self.room_combo)
        gen_layout.addLayout(room_layout)

        # Выбор стиля
        style_layout = QHBoxLayout()
        style_layout.addWidget(QLabel("Стиль:"))
        self.style_combo = QComboBox()
        for key, name in self.STYLES.items():
            self.style_combo.addItem(name, key)
        style_layout.addWidget(self.style_combo)
        gen_layout.addLayout(style_layout)

        # Пожелания
        gen_layout.addWidget(QLabel("Дополнительные пожелания:"))
        self.preferences_edit = QLineEdit()
        self.preferences_edit.setPlaceholderText("Например: бюджетный вариант, для семьи с детьми...")
        gen_layout.addWidget(self.preferences_edit)

        # Кнопка генерации
        self.generate_btn = QPushButton("✨ Сгенерировать дизайн")
        self.generate_btn.clicked.connect(self._generate_design)
        gen_layout.addWidget(self.generate_btn)

        # Прогресс
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        gen_layout.addWidget(self.progress_bar)

        self.progress_label = QLabel()
        self.progress_label.setVisible(False)
        gen_layout.addWidget(self.progress_label)

        layout.addWidget(gen_group)

        # Результат
        result_group = QGroupBox("📝 Результат")
        result_layout = QVBoxLayout(result_group)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(200)
        self.result_text.setPlaceholderText(
            "Здесь появится сгенерированный дизайн-проект...\n\n"
            "1. Выберите комнату\n"
            "2. Выберите стиль\n"
            "3. Нажмите 'Сгенерировать'"
        )
        result_layout.addWidget(self.result_text)

        layout.addWidget(result_group)

        # Чат
        chat_group = QGroupBox("💬 Чат с AI")
        chat_layout = QVBoxLayout(chat_group)

        chat_input_layout = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Задайте вопрос AI-дизайнеру...")
        self.chat_input.returnPressed.connect(self._send_chat)
        chat_input_layout.addWidget(self.chat_input)

        send_btn = QPushButton("📤")
        send_btn.clicked.connect(self._send_chat)
        chat_input_layout.addWidget(send_btn)

        chat_layout.addLayout(chat_input_layout)

        layout.addWidget(chat_group)

        self._update_room_combo()

    def _init_ai(self):
        """Инициализация AI"""
        api_key = self.settings.api_key

        if api_key:
            self.gpt_client = GPTClient(api_key, self.settings.get("gpt_model", "gpt-4o"))
            self.generator = DesignGenerator(self.gpt_client)
            self.status_label.setText("✅ AI подключен")
            self.status_label.setStyleSheet("color: #4CAF50;")
            self.generate_btn.setEnabled(True)
        else:
            self.status_label.setText(
                "⚠️ API ключ не настроен.\n"
                "Перейдите в Настройки → Параметры → AI"
            )
            self.status_label.setStyleSheet("color: #FF9800;")
            self.generate_btn.setEnabled(False)

    def update_project(self, project: Project):
        """Обновить проект"""
        self.project = project
        self._update_room_combo()

        if self.generator:
            self.generator = DesignGenerator(self.gpt_client)

    def _update_room_combo(self):
        """Обновить список комнат"""
        self.room_combo.clear()
        for room in self.project.rooms:
            self.room_combo.addItem(room.name, room.id)

    def _generate_design(self):
        """Запустить генерацию дизайна"""
        if not self.generator:
            QMessageBox.warning(
                self, "Ошибка",
                "AI не настроен. Укажите API ключ в настройках."
            )
            return

        if self.room_combo.count() == 0:
            QMessageBox.warning(
                self, "Ошибка",
                "Сначала добавьте комнату в проект."
            )
            return

        room_id = self.room_combo.currentData()
        room = self.project.get_room_by_id(room_id)

        if not room:
            return

        style_key = self.style_combo.currentData()
        style = self.STYLES.get(style_key, style_key)
        preferences = self.preferences_edit.text()

        # UI состояние загрузки
        self.generate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Индикатор
        self.progress_label.setVisible(True)
        self.result_text.setText("Генерация...")

        # Запускаем в фоне
        self.worker = AIWorker(self.generator, room, style, preferences)
        self.worker.finished.connect(self._on_generation_finished)
        self.worker.error.connect(self._on_generation_error)
        self.worker.progress.connect(self._on_generation_progress)
        self.worker.start()

    def _on_generation_finished(self, result: str):
        """Генерация завершена"""
        self.result_text.setText(result)
        self._reset_ui()

    def _on_generation_error(self, error: str):
        """Ошибка генерации"""
        self.result_text.setText(f"❌ Ошибка: {error}")
        self._reset_ui()

    def _on_generation_progress(self, message: str):
        """Прогресс генерации"""
        self.progress_label.setText(message)

    def _reset_ui(self):
        """Сбросить UI после генерации"""
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)

    def _send_chat(self):
        """Отправить сообщение в чат"""
        message = self.chat_input.text().strip()
        if not message:
            return

        if not self.generator:
            self.result_text.append("\n❌ AI не настроен")
            return

        self.chat_input.clear()
        self.result_text.append(f"\n👤 Вы: {message}")

        response = self.generator.chat(message, self.project)
        self.result_text.append(f"\n🤖 AI: {response}")