import unittest
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os


class TestJinjaTemplates(unittest.TestCase):
    """Тесты для Jinja2 шаблонов"""

    def setUp(self):
        """Настройка тестового окружения"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(current_dir, '..', 'templates')

        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape()
        )

    def test_index_template_rendering(self):
        """Тест рендеринга главного шаблона"""
        template = self.env.get_template("index.html")

        context = {
            'app_name': 'Тестовое приложение',
            'myapp': 'Тестовое приложение',
            'version': '1.0.0',
            'navigation': [
                {'caption': 'Основная страница', 'href': '/'},
                {'caption': 'Об авторе', 'href': '/author'}
            ],
            'author_name': 'Тестовый автор',
            'author_group': 'Т3124',
            'user_id': '123',
            'user_name': 'Тестовый пользователь',
            'user1_id': '456',
            'user1_name': 'Другой пользователь'
        }

        result = template.render(**context)

        # Проверяем базовую структуру
        self.assertIn('<!doctype html>', result)
        self.assertIn('<html lang="en">', result)

        # Проверяем передачу переменных
        self.assertIn('Тестовое приложение - Главная страница', result)
        self.assertIn('Тестовый автор', result)
        self.assertIn('Т3124', result)
        self.assertIn('Тестовый пользователь', result)
        self.assertIn('Другой пользователь', result)

        # Проверяем навигацию
        self.assertIn('Основная страница', result)
        self.assertIn('/author', result)

    def test_author_template_rendering(self):
        """Тест рендеринга шаблона об авторе"""
        template = self.env.get_template("author.html")

        context = {
            'author_name': 'Тестовый автор',
            'author_group': 'Т3124',
            'app_name': 'Тестовое приложение',
            'app_version': '2.0.0',
            'navigation': [
                {'caption': 'Основная страница', 'href': '/'},
                {'caption': 'Об авторе', 'href': '/author'}
            ]
        }

        result = template.render(**context)

        # Проверяем передачу переменных
        self.assertIn('Об авторе проекта', result)
        self.assertIn('Тестовый автор', result)
        self.assertIn('Т3124', result)
        self.assertIn('Тестовое приложение', result)
        self.assertIn('2.0.0', result)

    def test_users_template_rendering_with_data(self):
        """Тест рендеринга шаблона пользователей с данными"""
        template = self.env.get_template("users.html")

        # Создаем тестовых пользователей
        class MockUser:
            def __init__(self, user_id, name):
                self.id = user_id
                self.name = name

        users = [
            MockUser("123", "Иван"),
            MockUser("456", "Мария")
        ]

        context = {
            'app_name': 'Тестовое приложение',
            'navigation': [
                {'caption': 'Основная страница', 'href': '/'},
                {'caption': 'Пользователи', 'href': '/users'}
            ],
            'users': users
        }

        result = template.render(**context)

        # Проверяем таблицу пользователей
        self.assertIn('Список пользователей', result)
        self.assertIn('Иван', result)
        self.assertIn('Мария', result)
        self.assertIn('/user?id=123', result)
        self.assertIn('/user?id=456', result)

    def test_users_template_rendering_empty(self):
        """Тест рендеринга шаблона пользователей без данных"""
        template = self.env.get_template("users.html")

        context = {
            'app_name': 'Тестовое приложение',
            'navigation': [],
            'users': []  # Пустой список
        }

        result = template.render(**context)

        # Проверяем сообщение об отсутствии пользователей
        self.assertIn('Нет зарегистрированных пользователей', result)
        self.assertIn('text-muted', result)  # CSS класс для серого текста

    def test_user_template_rendering_with_subscriptions(self):
        """Тест рендеринга шаблона пользователя с подписками"""
        template = self.env.get_template("user.html")

        # Создаем тестового пользователя
        class MockUser:
            def __init__(self, user_id, name):
                self.id = user_id
                self.name = name

        # Создаем тестовые валюты
        class MockCurrency:
            def __init__(self, char_code, name, value, nominal):
                self.char_code = char_code
                self.name = name
                self.value = value
                self.nominal = nominal

        user = MockUser("123", "Иван")
        subscriptions = [
            MockCurrency("USD", "Доллар США", 90.5, 1),
            MockCurrency("EUR", "Евро", 98.2, 1)
        ]

        context = {
            'app_name': 'Тестовое приложение',
            'navigation': [
                {'caption': 'Основная страница', 'href': '/'},
                {'caption': 'Пользователи', 'href': '/users'}
            ],
            'user': user,
            'subscriptions': subscriptions
        }

        result = template.render(**context)

        # Проверяем информацию о пользователе
        self.assertIn('Информация о пользователе', result)
        self.assertIn('Иван', result)
        self.assertIn('123', result)

        # Проверяем таблицу подписок
        self.assertIn('Подписки на валюты', result)
        self.assertIn('USD', result)
        self.assertIn('Доллар США', result)
        self.assertIn('90.5', result)
        self.assertIn('EUR', result)
        self.assertIn('Евро', result)
        self.assertIn('98.2', result)

    def test_user_template_rendering_without_subscriptions(self):
        """Тест рендеринга шаблона пользователя без подписок"""
        template = self.env.get_template("user.html")

        class MockUser:
            def __init__(self, user_id, name):
                self.id = user_id
                self.name = name

        user = MockUser("123", "Иван")

        context = {
            'app_name': 'Тестовое приложение',
            'navigation': [],
            'user': user,
            'subscriptions': []  # Пустой список подписок
        }

        result = template.render(**context)

        # Проверяем сообщение об отсутствии подписок
        self.assertIn('Пользователь не подписан ни на одну валюту', result)
        self.assertIn('text-muted', result)

    def test_currencies_template_rendering_with_data(self):
        """Тест рендеринга шаблона валют с данными"""
        template = self.env.get_template("currencies.html")

        # Создаем тестовые валюты
        class MockCurrency:
            def __init__(self, char_code, name, value, nominal, num_code):
                self.char_code = char_code
                self.name = name
                self.value = value
                self.nominal = nominal
                self.num_code = num_code

        currencies = [
            MockCurrency("USD", "Доллар США", 90.5, 1, "840"),
            MockCurrency("EUR", "Евро", 98.2, 1, "978")
        ]

        context = {
            'app_name': 'Тестовое приложение',
            'navigation': [],
            'currencies': currencies,
            'success': True,
            'error': None
        }

        result = template.render(**context)

        # Проверяем таблицу валют
        self.assertIn('Курсы валют', result)
        self.assertIn('Текущие курсы валют', result)
        self.assertIn('USD', result)
        self.assertIn('Доллар США', result)
        self.assertIn('90.5', result)
        self.assertIn('840', result)
        self.assertIn('EUR', result)
        self.assertIn('Евро', result)
        self.assertIn('98.2', result)
        self.assertIn('978', result)

        # Проверяем отсутствие блока ошибки
        self.assertNotIn('Ошибка при получении курсов валют', result)

    def test_currencies_template_rendering_with_error(self):
        """Тест рендеринга шаблона валют с ошибкой"""
        template = self.env.get_template("currencies.html")

        context = {
            'app_name': 'Тестовое приложение',
            'navigation': [],
            'currencies': [],  # Пустой список
            'success': False,
            'error': 'API недоступен'
        }

        result = template.render(**context)

        # Проверяем блок ошибки
        self.assertIn('Ошибка при получении курсов валют', result)
        self.assertIn('API недоступен', result)
        self.assertIn('alert alert-danger', result)  # CSS класс для ошибки
        self.assertIn('Показаны последние сохраненные данные', result)

    def test_template_conditionals(self):
        """Тест условных операторов в шаблонах"""
        template = self.env.get_template("currencies.html")

        # Тест с success=True
        context_success = {
            'success': True,
            'error': None,
            'currencies': [],
            'app_name': 'Test',
            'navigation': []
        }
        result_success = template.render(**context_success)
        self.assertNotIn('alert alert-danger', result_success)

        # Тест с success=False
        context_error = {
            'success': False,
            'error': 'Ошибка',
            'currencies': [],
            'app_name': 'Test',
            'navigation': []
        }
        result_error = template.render(**context_error)
        self.assertIn('alert alert-danger', result_error)

    def test_template_loops(self):
        """Тест циклов в шаблонах"""
        template = self.env.get_template("users.html")

        class MockUser:
            def __init__(self, user_id, name):
                self.id = user_id
                self.name = name

        users = [
            MockUser("1", "Анна"),
            MockUser("2", "Борис"),
            MockUser("3", "Виктория")
        ]

        context = {
            'app_name': 'Test',
            'navigation': [],
            'users': users
        }

        result = template.render(**context)

        # Проверяем, что все пользователи отображены
        self.assertIn('Анна', result)
        self.assertIn('Борис', result)
        self.assertIn('Виктория', result)

        # Проверяем количество строк в таблице (3 пользователя + заголовок)
        self.assertEqual(result.count('<tr>'), 4)  # 3 пользователя + 1 заголовок


if __name__ == '__main__':
    unittest.main()