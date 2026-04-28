"""
Модульные тесты для Weather Diary
Тестирование позитивных, негативных и граничных случаев
"""

import unittest
import os
import tempfile
from weather_manager import WeatherRecord, WeatherManager

class TestWeatherRecord(unittest.TestCase):
    """Тесты для класса WeatherRecord"""
    
    def setUp(self):
        self.record = WeatherRecord("2024-06-15", 22.5, "Солнечно, тепло", False)
    
    def test_record_creation(self):
        """Тест создания записи (позитивный)"""
        self.assertEqual(self.record.date, "2024-06-15")
        self.assertEqual(self.record.temperature, 22.5)
        self.assertEqual(self.record.description, "Солнечно, тепло")
        self.assertFalse(self.record.precipitation)
    
    def test_record_to_dict(self):
        """Тест преобразования в словарь"""
        data = self.record.to_dict()
        self.assertEqual(data['date'], "2024-06-15")
        self.assertEqual(data['temperature'], 22.5)
    
    def test_record_from_dict(self):
        """Тест создания записи из словаря"""
        data = {
            'date': '2024-06-16',
            'temperature': 18.0,
            'description': 'Пасмурно',
            'precipitation': True
        }
        record = WeatherRecord.from_dict(data)
        self.assertEqual(record.date, '2024-06-16')
        self.assertTrue(record.precipitation)

class TestWeatherManager(unittest.TestCase):
    """Тесты для класса WeatherManager"""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        self.manager = WeatherManager(self.temp_file.name)
        self.manager.clear_all_records()
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_add_record_positive(self):
        """Тест успешного добавления записи (позитивный)"""
        result = self.manager.add_record("2024-06-15", 22.5, "Солнечно", False)
        self.assertTrue(result)
        self.assertEqual(len(self.manager.get_records()), 1)
    
    def test_add_record_duplicate(self):
        """Тест предотвращения дубликатов (негативный)"""
        self.manager.add_record("2024-06-15", 22.5, "Солнечно", False)
        result = self.manager.add_record("2024-06-15", 25.0, "Жарко", False)
        self.assertFalse(result)
        self.assertEqual(len(self.manager.get_records()), 1)
    
    def test_add_record_boundary_temperature(self):
        """Тест граничных значений температуры"""
        # Минимальная допустимая температура
        result = self.manager.add_record("2024-06-15", -60.0, "Экстремальный холод", False)
        self.assertTrue(result)
        
        # Максимальная допустимая температура
        result = self.manager.add_record("2024-06-16", 60.0, "Экстремальная жара", False)
        self.assertTrue(result)
    
    def test_remove_record_positive(self):
        """Тест успешного удаления записи"""
        self.manager.add_record("2024-06-15", 22.5, "Солнечно", False)
        result = self.manager.remove_record(0)
        self.assertTrue(result)
        self.assertEqual(len(self.manager.get_records()), 0)
    
    def test_remove_record_invalid_index(self):
        """Тест удаления с неверным индексом (негативный)"""
        result = self.manager.remove_record(999)
        self.assertFalse(result)
    
    def test_filter_by_date(self):
        """Тест фильтрации по дате (позитивный)"""
        self.manager.add_record("2024-06-15", 22.5, "Солнечно", False)
        self.manager.add_record("2024-06-16", 18.0, "Пасмурно", True)
        
        filtered = self.manager.filter_by_date("2024-06-15")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].date, "2024-06-15")
    
    def test_filter_by_temperature(self):
        """Тест фильтрации по температуре (позитивный)"""
        self.manager.add_record("2024-06-15", 22.5, "Солнечно", False)
        self.manager.add_record("2024-06-16", 18.0, "Пасмурно", True)
        self.manager.add_record("2024-06-17", 25.0, "Жарко", False)
        
        filtered = self.manager.filter_by_temperature(20.0)
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(r.temperature >= 20.0 for r in filtered))
    
    def test_filter_by_precipitation(self):
        """Тест фильтрации по осадкам"""
        self.manager.add_record("2024-06-15", 22.5, "Солнечно", False)
        self.manager.add_record("2024-06-16", 18.0, "Пасмурно", True)
        
        filtered = self.manager.filter_by_precipitation(True)
        self.assertEqual(len(filtered), 1)
        self.assertTrue(filtered[0].precipitation)
    
    def test_save_and_load(self):
        """Тест сохранения и загрузки JSON"""
        self.manager.add_record("2024-06-15", 22.5, "Солнечно", False)
        self.manager.save_records()
        
        new_manager = WeatherManager(self.temp_file.name)
        self.assertEqual(len(new_manager.get_records()), 1)
        self.assertEqual(new_manager.get_records()[0].temperature, 22.5)
    
    def test_get_statistics(self):
        """Тест получения статистики"""
        self.manager.add_record("2024-06-15", 22.5, "Солнечно", False)
        self.manager.add_record("2024-06-16", 18.0, "Пасмурно", True)
        self.manager.add_record("2024-06-17", 25.0, "Жарко", False)
        
        stats = self.manager.get_statistics()
        self.assertEqual(stats['total'], 3)
        self.assertEqual(stats['avg_temp'], 21.8)  # (22.5+18+25)/3 = 21.83
        self.assertEqual(stats['max_temp'], 25.0)
        self.assertEqual(stats['min_temp'], 18.0)
        self.assertEqual(stats['rainy_days'], 1)

class TestValidationBoundaries(unittest.TestCase):
    """Тесты валидации граничных случаев"""
    
    def test_invalid_date_format(self):
        """Тест неверного формата даты"""
        manager = WeatherManager()
        
        # Неверный формат
        result = manager.add_record("15-06-2024", 22.5, "Солнечно", False)
        self.assertFalse(result)
    
    def test_invalid_date_values(self):
        """Тест несуществующей даты"""
        manager = WeatherManager()
        
        # 32-е число
        result = manager.add_record("2024-06-32", 22.5, "Солнечно", False)
        self.assertFalse(result)
        
        # 13-й месяц
        result = manager.add_record("2024-13-15", 22.5, "Солнечно", False)
        self.assertFalse(result)
    
    def test_empty_description(self):
        """Тест пустого описания"""
        manager = WeatherManager()
        
        result = manager.add_record("2024-06-15", 22.5, "", False)
        self.assertFalse(result)
    
    def test_invalid_temperature(self):
        """Тест неверного формата температуры"""
        manager = WeatherManager()
        
        result = manager.add_record("2024-06-15", "двадцать", "Солнечно", False)
        self.assertFalse(result)

def run_tests():
    """Запуск всех тестов"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestWeatherRecord))
    suite.addTests(loader.loadTestsFromTestCase(TestWeatherManager))
    suite.addTests(loader.loadTestsFromTestCase(TestValidationBoundaries))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*50)
    print(f"📊 Результаты тестирования:")
    print(f"✅ Запущено тестов: {result.testsRun}")
    print(f"✅ Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    if result.errors:
        print(f"❌ Ошибок: {len(result.errors)}")
    if result.failures:
        print(f"❌ Провалено: {len(result.failures)}")
    print("="*50)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
