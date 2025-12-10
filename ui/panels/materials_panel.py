"""
Панель расчёта материалов
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QGroupBox, QTextEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QTabWidget,
    QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt

from core.project import Project
from core.materials_calc import MaterialsCalculator


class MaterialsPanel(QWidget):
    """Панель расчёта материалов"""

    def __init__(self, project: Project, parent=None):
        super().__init__(parent)
        self.project = project

        self._setup_ui()

    def _setup_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Заголовок
        header = QLabel("🧱 Расчёт строительных материалов")
        header.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(header)

        # Информация о проекте
        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)

        # Кнопка расчёта
        calc_btn = QPushButton("📊 Рассчитать материалы")
        calc_btn.clicked.connect(self._calculate)
        layout.addWidget(calc_btn)

        # Вкладки с результатами
        self.tabs = QTabWidget()

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Материал", "Кол-во", "Ед.", "С запасом", "Примечание"
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabs.addTab(self.table, "📋 Таблица")

        # Текстовый отчёт
        self.text_report = QTextEdit()
        self.text_report.setReadOnly(True)
        self.tabs.addTab(self.text_report, "📝 Отчёт")

        layout.addWidget(self.tabs)

        # Кнопки экспорта
        export_layout = QHBoxLayout()

        export_txt_btn = QPushButton("💾 Экспорт TXT")
        export_txt_btn.clicked.connect(self._export_txt)
        export_layout.addWidget(export_txt_btn)

        export_csv_btn = QPushButton("📊 Экспорт CSV")
        export_csv_btn.clicked.connect(self._export_csv)
        export_layout.addWidget(export_csv_btn)

        layout.addLayout(export_layout)

        self._update_info()

    def update_project(self, project: Project):
        """Обновить проект"""
        self.project = project
        self._update_info()
        self._clear_results()

    def _update_info(self):
        """Обновить информацию о проекте"""
        rooms = len(self.project.rooms)
        area = self.project.total_area

        self.info_label.setText(
            f"📁 Проект: {self.project.name}\n"
            f"🏠 Комнат: {rooms}\n"
            f"📐 Общая площадь: {area:.2f} м²"
        )

    def _clear_results(self):
        """Очистить результаты"""
        self.table.setRowCount(0)
        self.text_report.clear()

    def _calculate(self):
        """Рассчитать материалы"""
        if not self.project.rooms:
            QMessageBox.warning(
                self, "Ошибка",
                "Добавьте хотя бы одну комнату для расчёта."
            )
            return

        calc = MaterialsCalculator(self.project)

        # Текстовый отчёт
        self.text_report.setText(calc.get_summary_text())

        # Таблица
        all_materials = calc.calculate_all()

        self.table.setRowCount(0)
        row = 0

        category_names = {
            "walls": "🧱 СТЕНЫ",
            "floor": "🔲 ПОЛ",
            "ceiling": "⬜ ПОТОЛОК",
            "other": "📦 ПРОЧЕЕ"
        }

        for category, materials in all_materials.items():
            # Заголовок категории
            self.table.insertRow(row)
            header_item = QTableWidgetItem(category_names.get(category, category))
            header_item.setBackground(Qt.lightGray)
            font = header_item.font()
            font.setBold(True)
            header_item.setFont(font)
            self.table.setItem(row, 0, header_item)
            self.table.setSpan(row, 0, 1, 5)
            row += 1

            # Материалы
            for mat in materials:
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(mat.name))
                self.table.setItem(row, 1, QTableWidgetItem(f"{mat.quantity}"))
                self.table.setItem(row, 2, QTableWidgetItem(mat.unit))
                self.table.setItem(row, 3, QTableWidgetItem(f"{mat.with_reserve}"))
                self.table.setItem(row, 4, QTableWidgetItem(mat.notes))
                row += 1

        self.tabs.setCurrentIndex(0)

    def _export_txt(self):
        """Экспорт в TXT"""
        from utils.export import ProjectExporter

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт отчёта",
            f"{self.project.name}_материалы.txt",
            "Текстовые файлы (*.txt)"
        )

        if file_path:
            if ProjectExporter.to_text_report(self.project, file_path):
                QMessageBox.information(
                    self, "Успех",
                    f"Отчёт сохранён:\n{file_path}"
                )

    def _export_csv(self):
        """Экспорт в CSV"""
        from utils.export import ProjectExporter

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт CSV",
            f"{self.project.name}_материалы.csv",
            "CSV файлы (*.csv)"
        )

        if file_path:
            if ProjectExporter.to_csv_materials(self.project, file_path):
                QMessageBox.information(
                    self, "Успех",
                    f"CSV сохранён:\n{file_path}"
                )