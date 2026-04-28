"""
Weather Diary - приложение для ведения дневника погоды
Автор: Яковлев Владислав Константинович
Версия: 1.0
"""

import tkinter as tk
from gui import WeatherDiaryGUI

def main():
    """Запуск приложения"""
    try:
        root = tk.Tk()
        app = WeatherDiaryGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")

if __name__ == "__main__":
    main()
