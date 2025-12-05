import unittest
from unittest.mock import patch, Mock
import json



def get_currencies_simple(currency_codes: list, url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> dict:
    """
    Простая версия функции для тестирования
    """
    import requests

    # 1. Делаем запрос к API
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except Exception:
        raise ConnectionError("API недоступен")

    # 2. Пытаемся прочитать JSON
    try:
        data = response.json()
    except ValueError:
        raise ValueError("Некорректный JSON")

    # 3. Проверяем есть ли ключ "Valute"
    if "Valute" not in data:
        raise KeyError('Нет ключа "Valute"')

    result = {}

    # 4. Для каждой запрошенной валюты
    for code in currency_codes:
        # Проверяем есть ли валюта в данных
        if code not in data["Valute"]:
            raise KeyError(f'Валюта "{code}" отсутствует')

        # Получаем значение курса
        value = data["Valute"][code]["Value"]

        # Проверяем тип значения (должно быть числом)
        if not isinstance(value, (int, float)):
            raise TypeError(f'Курс валюты "{code}" имеет неверный тип')

        # Сохраняем результат
        result[code] = float(value)

    return result


class TestGetCurrenciesSimple(unittest.TestCase):

    def test_correct_return(self):
        """Тест корректного возврата курсов"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "Valute": {
                    "USD": {"Value": 90.5},
                    "EUR": {"Value": 98.2}
                }
            }
            mock_get.return_value = mock_response

            result = get_currencies_simple(["USD", "EUR"])
            self.assertEqual(result["USD"], 90.5)
            self.assertEqual(result["EUR"], 98.2)

    def test_connection_error(self):
        """Тест ConnectionError"""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("Connection failed")

            with self.assertRaises(ConnectionError):
                get_currencies_simple(["USD"])

    def test_nonexistent_currency(self):
        """Тест при несуществующей валюте"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "Valute": {
                    "USD": {"Value": 90.5}
                }
            }
            mock_get.return_value = mock_response

            with self.assertRaises(KeyError):
                get_currencies_simple(["XYZ"])

    def test_value_error(self):
        """Тест ValueError при некорректном JSON"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.side_effect = json.JSONDecodeError("Error", "", 0)
            mock_get.return_value = mock_response

            with self.assertRaises(ValueError):
                get_currencies_simple(["USD"])

    def test_key_error_no_valute(self):
        """Тест KeyError при отсутствии ключа Valute"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {}
            mock_get.return_value = mock_response

            with self.assertRaises(KeyError):
                get_currencies_simple(["USD"])

    def test_type_error_invalid_value(self):
        """Тест TypeError при неверном типе курса"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {
                "Valute": {
                    "USD": {"Value": "не число"}
                }
            }
            mock_get.return_value = mock_response

            with self.assertRaises(TypeError):
                get_currencies_simple(["USD"])


if __name__ == "__main__":
    unittest.main()