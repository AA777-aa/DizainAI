"""
DizainAI - Программа для дизайна интерьера
Точка входа в приложение
"""

import sys
import os

# Добавляем корневую папку в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window import MainWindow
from config.settings import Settings


def main():
    """Главная функция запуска приложения"""

    # Включаем поддержку высокого DPI
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("DizainAI")
    app.setApplicationVersion("1.0.0")

    # Загружаем настройки
    settings = Settings()

    # Создаём главное окно
    window = MainWindow(settings)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
