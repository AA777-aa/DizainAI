"""
Диалог настроек приложения
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QLabel, QGroupBox,
    QComboBox, QSpinBox, QTabWidget, QWidget,
    QMessageBox, QCheckBox
)
from PyQt5.QtCore import Qt

from config.settings import Settings


class SettingsDialog(QDialog):
    """Диалог настроек"""

    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self.settings = settings

        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        """Настройка интерфейса"""
        self.setWindowTitle("Настройки DizainAI")
        self.setMinimumSize(500, 400)

        layout = QVBoxLayout(self)

        # Вкладки
        tabs = QTabWidget()

        # Вкладка API
        api_tab = QWidget()
        api_layout = QVBoxLayout(api_tab)

        api_group = QGroupBox("OpenAI API")
        api_form = QFormLayout(api_group)

        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.Password)
        self.api_key_edit.setPlaceholderText("sk-...")
        api_form.addRow("API ключ:", self.api_key_edit)

        # Кнопка показать/скрыть
        show_key_btn = QPushButton("👁 Показать")
        show_key_btn.setCheckable(True)
        show_key_btn.toggled.connect(self._toggle_key_visibility)
        api_form.addRow("", show_key_btn)

        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "gpt-4",
            "gpt-3.5-turbo"
        ])
        api_form.addRow("Модель:", self.model_combo)

        api_layout.addWidget(api_group)

        # Информация
        info_label = QLabel(
            "💡 Получите API ключ на <a href='https://platform.openai.com/api-keys'>platform.openai.com</a>"
        )
        info_label.setOpenExternalLinks(True)
        info_label.setWordWrap(True)
        api_layout.addWidget(info_label)

        # Проверка ключа
        test_btn = QPushButton("🔍 Проверить подключение")
        test_btn.clicked.connect(self._test_api)
        api_layout.addWidget(test_btn)

        api_layout.addStretch()
        tabs.addTab(api_tab, "🤖 AI")

        # Вкладка Общие
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)

        defaults_group = QGroupBox("Значения по умолчанию")
        defaults_form = QFormLayout(defaults_group)

        self.wall_height_spin = QSpinBox()
        self.wall_height_spin.setRange(2000, 5000)
        self.wall_height_spin.setSuffix(" мм")
        defaults_form.addRow("Высота стен:", self.wall_height_spin)

        self.wall_thickness_spin = QSpinBox()
        self.wall_thickness_spin.setRange(50, 500)
        self.wall_thickness_spin.setSuffix(" мм")
        defaults_form.addRow("Толщина стен:", self.wall_thickness_spin)

        self.grid_spin = QSpinBox()
        self.grid_spin.setRange(10, 500)
        self.grid_spin.setSuffix(" мм")
        defaults_form.addRow("Шаг сетки:", self.grid_spin)

        general_layout.addWidget(defaults_group)

        # Единицы измерения
        units_group = QGroupBox("Единицы измерения")
        units_layout = QHBoxLayout(units_group)

        self.units_combo = QComboBox()
        self.units_combo.addItems(["Миллиметры (мм)", "Сантиметры (см)"])
        units_layout.addWidget(QLabel("Отображать в:"))
        units_layout.addWidget(self.units_combo)
        units_layout.addStretch()

        general_layout.addWidget(units_group)
        general_layout.addStretch()

        tabs.addTab(general_tab, "⚙️ Общие")

        layout.addWidget(tabs)

        # Кнопки
        buttons_layout = QHBoxLayout()

        reset_btn = QPushButton("Сбросить")
        reset_btn.clicked.connect(self._reset_to_defaults)
        buttons_layout.addWidget(reset_btn)

        buttons_layout.addStretch()

        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Сохранить")
        save_btn.setDefault(True)
        save_btn.clicked.connect(self._save_settings)
        buttons_layout.addWidget(save_btn)

        layout.addLayout(buttons_layout)

    def _load_settings(self):
        """Загрузить текущие настройки"""
        self.api_key_edit.setText(self.settings.get("openai_api_key", ""))

        model = self.settings.get("gpt_model", "gpt-4o")
        index = self.model_combo.findText(model)
        if index >= 0:
            self.model_combo.setCurrentIndex(index)

        self.wall_height_spin.setValue(self.settings.get("default_wall_height", 2700))
        self.wall_thickness_spin.setValue(self.settings.get("default_wall_thickness", 100))
        self.grid_spin.setValue(self.settings.get("grid_size", 100))

        units = self.settings.get("units", "mm")
        self.units_combo.setCurrentIndex(0 if units == "mm" else 1)

    def _toggle_key_visibility(self, show):
        """Показать/скрыть API ключ"""
        self.api_key_edit.setEchoMode(
            QLineEdit.Normal if show else QLineEdit.Password
        )

    def _test_api(self):
        """Проверить подключение к API"""
        api_key = self.api_key_edit.text().strip()

        if not api_key:
            QMessageBox.warning(self, "Ошибка", "Введите API ключ")
            return

        try:
            from ai.gpt_client import GPTClient

            client = GPTClient(api_key, self.model_combo.currentText())
            response = client.send_simple("Привет! Ответь одним словом: работает")

            if response.success:
                QMessageBox.information(
                    self, "Успех",
                    f"✅ Подключение работает!\n\nОтвет: {response.content[:100]}"
                )
            else:
                QMessageBox.warning(
                    self, "Ошибка",
                    f"❌ Ошибка подключения:\n{response.error}"
                )

        except Exception as e:
            QMessageBox.critical(
                self, "Ошибка",
                f"❌ Не удалось проверить:\n{str(e)}"
            )

    def _reset_to_defaults(self):
        """Сбросить к значениям по умолчанию"""
        reply = QMessageBox.question(
            self, "Сброс настроек",
            "Сбросить все настройки к значениям по умолчанию?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.api_key_edit.clear()
            self.model_combo.setCurrentIndex(0)
            self.wall_height_spin.setValue(2700)
            self.wall_thickness_spin.setValue(100)
            self.grid_spin.setValue(100)
            self.units_combo.setCurrentIndex(0)

    def _save_settings(self):
        """Сохранить настройки"""
        self.settings.set("openai_api_key", self.api_key_edit.text().strip())
        self.settings.set("gpt_model", self.model_combo.currentText())
        self.settings.set("default_wall_height", self.wall_height_spin.value())
        self.settings.set("default_wall_thickness", self.wall_thickness_spin.value())
        self.settings.set("grid_size", self.grid_spin.value())
        self.settings.set("units", "mm" if self.units_combo.currentIndex() == 0 else "cm")

        self.settings.save()

        QMessageBox.information(self, "Сохранено", "Настройки сохранены!")
        self.accept()