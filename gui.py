"""
Графический интерфейс для Weather Diary
Использует tkinter для создания GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from weather_manager import WeatherManager

class WeatherDiaryGUI:
    """Основной класс GUI приложения"""
    
    def __init__(self, root):
        self.root = root
        self.weather_manager = WeatherManager()
        
        # Настройка главного окна
        self.root.title("Weather Diary - Дневник погоды")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Установка стиля
        self.root.configure(bg='#e8f4f8')
        
        # Создание интерфейса
        self.create_widgets()
        
        # Загрузка данных
        self.refresh_records_list()
        self.update_date_filter()
        self.update_statistics()
    
    def create_widgets(self):
        """Создание всех виджетов интерфейса"""
        
        # Основной контейнер
        main_frame = tk.Frame(self.root, bg='#e8f4f8')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Заголовок
        title_label = tk.Label(main_frame, text="🌤️ Дневник погоды 🌧️", 
                               font=('Arial', 18, 'bold'), bg='#e8f4f8', fg='#2c3e50')
        title_label.pack(pady=10)
        
        # === Форма добавления записи ===
        self.create_input_frame(main_frame)
        
        # === Панель фильтрации ===
        self.create_filter_frame(main_frame)
        
        # === Панель статистики ===
        self.create_stats_frame(main_frame)
        
        # === Таблица с записями ===
        self.create_records_table(main_frame)
        
        # === Статус бар ===
        self.status_var = tk.StringVar()
        self.status_var.set("✅ Готов к работе")
        status_bar = tk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W, bg='#f0f0f0')
        status_bar.pack(fill=tk.X, pady=(5, 0))
    
    def create_input_frame(self, parent):
        """Создание формы ввода новой записи"""
        input_frame = tk.LabelFrame(parent, text="➕ Добавить запись о погоде", 
                                     font=('Arial', 10, 'bold'), bg='#e8f4f8', fg='#2c3e50')
        input_frame.pack(fill=tk.X, pady=5)
        
        # Внутренний контейнер
        inner_frame = tk.Frame(input_frame, bg='#e8f4f8')
        inner_frame.pack(padx=10, pady=10)
        
        # Дата
        tk.Label(inner_frame, text="📅 Дата (ГГГГ-ММ-ДД):", bg='#e8f4f8').grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.date_entry = tk.Entry(inner_frame, width=20)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        # Вставляем сегодняшнюю дату
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Температура
        tk.Label(inner_frame, text="🌡️ Температура (°C):", bg='#e8f4f8').grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.temp_entry = tk.Entry(inner_frame, width=10)
        self.temp_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Осадки
        tk.Label(inner_frame, text="☔ Осадки:", bg='#e8f4f8').grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.precipitation_var = tk.BooleanVar(value=False)
        self.precipitation_check = tk.Checkbutton(inner_frame, variable=self.precipitation_var, 
                                                   bg='#e8f4f8', text="Есть осадки")
        self.precipitation_check.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Описание
        tk.Label(inner_frame, text="📝 Описание погоды:", bg='#e8f4f8').grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.desc_entry = tk.Entry(inner_frame, width=40)
        self.desc_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Кнопка добавления
        add_btn = tk.Button(inner_frame, text="➕ Добавить запись", 
                           command=self.add_record, bg='#4CAF50', fg='white',
                           font=('Arial', 10, 'bold'), padx=10, pady=3)
        add_btn.grid(row=2, column=0, columnspan=4, pady=10)
    
    def create_filter_frame(self, parent):
        """Создание панели фильтрации"""
        filter_frame = tk.LabelFrame(parent, text="🔍 Фильтрация записей", 
                                      font=('Arial', 10, 'bold'), bg='#e8f4f8', fg='#2c3e50')
        filter_frame.pack(fill=tk.X, pady=5)
        
        inner_frame = tk.Frame(filter_frame, bg='#e8f4f8')
        inner_frame.pack(padx=10, pady=10)
        
        # Фильтр по дате
        tk.Label(inner_frame, text="📅 По дате:", bg='#e8f4f8').grid(row=0, column=0, padx=5)
        self.date_filter_var = tk.StringVar(value="Все даты")
        self.date_filter_combo = ttk.Combobox(inner_frame, textvariable=self.date_filter_var, 
                                               width=15, state='readonly')
        self.date_filter_combo.grid(row=0, column=1, padx=5)
        self.date_filter_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        # Фильтр по температуре
        tk.Label(inner_frame, text="🌡️ Температура выше (°C):", bg='#e8f4f8').grid(row=0, column=2, padx=5)
        self.temp_filter_var = tk.StringVar(value="")
        self.temp_filter_entry = tk.Entry(inner_frame, textvariable=self.temp_filter_var, width=8)
        self.temp_filter_entry.grid(row=0, column=3, padx=5)
        
        # Фильтр по осадкам
        tk.Label(inner_frame, text="☔ Осадки:", bg='#e8f4f8').grid(row=0, column=4, padx=5)
        self.precip_filter_var = tk.StringVar(value="Все")
        self.precip_filter_combo = ttk.Combobox(inner_frame, textvariable=self.precip_filter_var, 
                                                 values=["Все", "С осадками", "Без осадков"], 
                                                 width=12, state='readonly')
        self.precip_filter_combo.grid(row=0, column=5, padx=5)
        self.precip_filter_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        # Кнопки
        btn_frame = tk.Frame(inner_frame, bg='#e8f4f8')
        btn_frame.grid(row=1, column=0, columnspan=7, pady=10)
        
        apply_btn = tk.Button(btn_frame, text="🔍 Применить фильтры", 
                             command=self.apply_filters, bg='#2196F3', fg='white', padx=10)
        apply_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = tk.Button(btn_frame, text="🔄 Сбросить фильтры", 
                             command=self.reset_filters, bg='#FF9800', fg='white', padx=10)
        reset_btn.pack(side=tk.LEFT, padx=5)
    
    def create_stats_frame(self, parent):
        """Создание панели статистики"""
        self.stats_frame = tk.LabelFrame(parent, text="📊 Статистика", 
                                          font=('Arial', 10, 'bold'), bg='#e8f4f8', fg='#2c3e50')
        self.stats_frame.pack(fill=tk.X, pady=5)
        
        self.stats_label = tk.Label(self.stats_frame, text="", 
                                     font=('Arial', 9), bg='#e8f4f8')
        self.stats_label.pack(padx=10, pady=5)
    
    def create_records_table(self, parent):
        """Создание таблицы для отображения записей"""
        table_frame = tk.Frame(parent, bg='#e8f4f8')
        table_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Контейнер с прокруткой
        container = tk.Frame(table_frame)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Создание Treeview
        columns = ('date', 'temperature', 'precipitation', 'description', 'created_at')
        self.tree = ttk.Treeview(container, columns=columns, show='headings', height=12)
        
        # Настройка колонок
        self.tree.heading('date', text='📅 Дата')
        self.tree.heading('temperature', text='🌡️ Температура')
        self.tree.heading('precipitation', text='☔ Осадки')
        self.tree.heading('description', text='📝 Описание')
        self.tree.heading('created_at', text='🕐 Добавлено')
        
        self.tree.column('date', width=120, anchor=tk.CENTER)
        self.tree.column('temperature', width=100, anchor=tk.CENTER)
        self.tree.column('precipitation', width=100, anchor=tk.CENTER)
        self.tree.column('description', width=400)
        self.tree.column('created_at', width=150, anchor=tk.CENTER)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопка удаления
        delete_btn = tk.Button(table_frame, text="🗑️ Удалить выбранную запись", 
                               command=self.delete_record, bg='#f44336', fg='white',
                               font=('Arial', 10), padx=10, pady=3)
        delete_btn.pack(pady=5)
    
    def validate_input(self, date: str, temperature: str, description: str) -> tuple:
        """
        Валидация вводимых данных
        
        Returns:
            tuple: (is_valid, error_message)
        """
        # Проверка даты
        if not date.strip():
            return False, "Дата не может быть пустой!"
        
        # Проверка формата даты (ГГГГ-ММ-ДД)
        import re
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, date):
            return False, "Неверный формат даты! Используйте ГГГГ-ММ-ДД (например, 2024-06-15)"
        
        # Проверка корректности даты
        try:
            year, month, day = map(int, date.split('-'))
            datetime(year, month, day)
        except ValueError:
            return False, "Неверная дата! Проверьте год, месяц и день."
        
        # Проверка температуры
        if not temperature.strip():
            return False, "Температура не может быть пустой!"
        
        try:
            temp = float(temperature)
            if temp < -60 or temp > 60:
                return False, "Температура должна быть в диапазоне от -60°C до +60°C!"
        except ValueError:
            return False, "Температура должна быть числом! (например, 15.5)"
        
        # Проверка описания
        if not description.strip():
            return False, "Описание погоды не может быть пустым!"
        
        if len(description) > 200:
            return False, "Описание не должно превышать 200 символов!"
        
        return True, ""
    
    def add_record(self):
        """Добавляет новую запись о погоде"""
        date = self.date_entry.get()
        temperature = self.temp_entry.get()
        description = self.desc_entry.get()
        precipitation = self.precipitation_var.get()
        
        # Валидация
        is_valid, error_msg = self.validate_input(date, temperature, description)
        if not is_valid:
            messagebox.showerror("Ошибка ввода", error_msg)
            return
        
        # Добавление записи
        temp_value = float(temperature)
        if self.weather_manager.add_record(date, temp_value, description, precipitation):
            precip_text = "🌧️ Да" if precipitation else "☀️ Нет"
            messagebox.showinfo("Успех", f"Запись за {date} успешно добавлена!\n🌡️ {temp_value}°C\n{precip_text}")
            self.clear_input_fields()
            self.refresh_records_list()
            self.update_date_filter()
            self.update_statistics()
            self.status_var.set(f"✅ Добавлена запись за {date}")
        else:
            messagebox.showwarning("Предупреждение", f"Запись за дату {date} уже существует!")
    
    def clear_input_fields(self):
        """Очищает поля ввода"""
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precipitation_var.set(False)
    
    def refresh_records_list(self):
        """Обновляет список записей с учётом фильтров"""
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Получаем записи
        records = self.weather_manager.get_records()
        
        # Применяем фильтры
        records = self.apply_filters_to_records(records)
        
        # Отображаем записи
        for record in records:
            precip_text = "🌧️ Да" if record.precipitation else "☀️ Нет"
            self.tree.insert('', tk.END, values=(
                record.date,
                f"{record.temperature}°C",
                precip_text,
                record.description,
                record.created_at
            ))
        
        count = len(records)
        self.status_var.set(f"📊 Найдено записей: {count}")
    
    def apply_filters_to_records(self, records):
        """Применяет фильтры к записям"""
        filtered = records.copy()
        
        # Фильтр по дате
        selected_date = self.date_filter_var.get()
        if selected_date != "Все даты":
            filtered = [r for r in filtered if r.date == selected_date]
        
        # Фильтр по температуре
        temp_filter = self.temp_filter_var.get()
        if temp_filter.strip():
            try:
                min_temp = float(temp_filter)
                filtered = [r for r in filtered if r.temperature >= min_temp]
            except ValueError:
                pass
        
        # Фильтр по осадкам
        precip_filter = self.precip_filter_var.get()
        if precip_filter == "С осадками":
            filtered = [r for r in filtered if r.precipitation]
        elif precip_filter == "Без осадков":
            filtered = [r for r in filtered if not r.precipitation]
        
        return filtered
    
    def apply_filters(self):
        """Применяет фильтры и обновляет таблицу"""
        self.refresh_records_list()
        self.status_var.set("🔍 Фильтры применены")
    
    def reset_filters(self):
        """Сбрасывает все фильтры"""
        self.date_filter_var.set("Все даты")
        self.temp_filter_var.set("")
        self.precip_filter_var.set("Все")
        self.refresh_records_list()
        self.status_var.set("🔄 Фильтры сброшены")
    
    def delete_record(self):
        """Удаляет выбранную запись"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите запись для удаления!")
            return
        
        # Подтверждение удаления
        item = self.tree.item(selected[0])
        record_date = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить запись за {record_date}?"):
            # Находим индекс записи
            for i, record in enumerate(self.weather_manager.get_records()):
                if record.date == record_date:
                    self.weather_manager.remove_record(i)
                    break
            
            self.refresh_records_list()
            self.update_date_filter()
            self.update_statistics()
            self.status_var.set(f"🗑️ Удалена запись за {record_date}")
    
    def update_date_filter(self):
        """Обновляет список дат в фильтре"""
        dates = self.weather_manager.get_unique_dates()
        dates.insert(0, "Все даты")
        self.date_filter_combo['values'] = dates
        if self.date_filter_var.get() not in dates:
            self.date_filter_var.set("Все даты")
    
    def update_statistics(self):
        """Обновляет панель статистики"""
        stats = self.weather_manager.get_statistics()
        
        if stats['total'] == 0:
            stats_text = "📭 Нет записей. Добавьте первую запись о погоде!"
        else:
            stats_text = (f"📈 Записей: {stats['total']} | "
                         f"🌡️ Средняя температура: {stats['avg_temp']}°C | "
                         f"📊 Макс: {stats['max_temp']}°C | "
                         f"📉 Мин: {stats['min_temp']}°C | "
                         f"🌧️ Дождливых дней: {stats['rainy_days']}")
        
        self.stats_label.config(text=stats_text)
