"""
Модуль для управления записями о погоде
Содержит логику работы с данными и JSON
"""

import json
import os
import re
from datetime import datetime
from typing import List, Dict, Optional

class WeatherRecord:
    """Класс для представления записи о погоде"""
    
    def __init__(self, date: str, temperature: float, description: str, precipitation: bool):
        self.date = date  # Формат: ГГГГ-ММ-ДД
        self.temperature = temperature
        self.description = description.strip()
        self.precipitation = precipitation
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        """Преобразует запись в словарь для JSON"""
        return {
            'date': self.date,
            'temperature': self.temperature,
            'description': self.description,
            'precipitation': self.precipitation,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Создаёт запись из словаря"""
        record = cls(
            data['date'], 
            data['temperature'], 
            data['description'], 
            data['precipitation']
        )
        record.created_at = data.get('created_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return record

class WeatherManager:
    """Класс для управления дневником погоды"""
    
    def __init__(self, filename: str = "weather.json"):
        self.filename = filename
        self.records: List[WeatherRecord] = []
        self.load_records()
    
    def add_record(self, date: str, temperature: float, description: str, precipitation: bool) -> bool:
        """
        Добавляет новую запись о погоде
        
        Returns:
            bool: True если добавление успешно, False если запись за эту дату уже существует
        """
        # Проверка на дубликат (одна запись на день)
        for record in self.records:
            if record.date == date:
                return False
        
        record = WeatherRecord(date, temperature, description, precipitation)
        self.records.append(record)
        # Сортируем по дате (новые сверху)
        self.records.sort(key=lambda x: x.date, reverse=True)
        self.save_records()
        return True
    
    def remove_record(self, index: int) -> bool:
        """Удаляет запись по индексу"""
        if 0 <= index < len(self.records):
            del self.records[index]
            self.save_records()
            return True
        return False
    
    def get_records(self) -> List[WeatherRecord]:
        """Возвращает список всех записей"""
        return self.records
    
    def filter_by_date(self, date: str) -> List[WeatherRecord]:
        """Фильтрует записи по точной дате"""
        if not date:
            return self.records
        return [record for record in self.records if record.date == date]
    
    def filter_by_temperature(self, min_temp: float) -> List[WeatherRecord]:
        """Фильтрует записи по минимальной температуре"""
        return [record for record in self.records if record.temperature >= min_temp]
    
    def filter_by_precipitation(self, has_precipitation: bool) -> List[WeatherRecord]:
        """Фильтрует записи по наличию осадков"""
        return [record for record in self.records if record.precipitation == has_precipitation]
    
    def get_unique_dates(self) -> List[str]:
        """Возвращает список уникальных дат"""
        dates = sorted(set(record.date for record in self.records), reverse=True)
        return dates
    
    def save_records(self) -> bool:
        """Сохраняет записи в JSON файл"""
        try:
            data = [record.to_dict() for record in self.records]
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
            return False
    
    def load_records(self):
        """Загружает записи из JSON файла"""
        if not os.path.exists(self.filename):
            self.records = []
            self.add_example_data()
            return
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.records = [WeatherRecord.from_dict(item) for item in data]
            # Сортируем по дате
            self.records.sort(key=lambda x: x.date, reverse=True)
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")
            self.records = []
    
    def add_example_data(self):
        """Добавляет примеры записей для демонстрации"""
        example_records = [
            ("2024-06-01", 22.5, "Солнечно, легкий ветерок", False),
            ("2024-06-02", 18.0, "Пасмурно, прохладно", False),
            ("2024-06-03", 15.5, "Дождь, сильный ветер", True),
            ("2024-06-04", 20.0, "Переменная облачность", False),
            ("2024-06-05", 12.0, "Ливень с грозой", True),
            ("2024-06-06", 25.0, "Жарко, солнечно", False),
            ("2024-06-07", 19.5, "Облачно, без осадков", False),
        ]
        for date, temp, desc, precip in example_records:
            self.add_record(date, temp, desc, precip)
    
    def clear_all_records(self):
        """Очищает все записи (для тестирования)"""
        self.records = []
        self.save_records()
    
    def get_statistics(self) -> Dict:
        """Возвращает статистику по записям"""
        if not self.records:
            return {
                'total': 0,
                'avg_temp': 0,
                'max_temp': 0,
                'min_temp': 0,
                'rainy_days': 0
            }
        
        temps = [r.temperature for r in self.records]
        rainy = sum(1 for r in self.records if r.precipitation)
        
        return {
            'total': len(self.records),
            'avg_temp': round(sum(temps) / len(temps), 1),
            'max_temp': max(temps),
            'min_temp': min(temps),
            'rainy_days': rainy
        }
