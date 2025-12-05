from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader, select_autoescape
from models import Author, User, App, Currency, UserCurrency
from http.server import HTTPServer, BaseHTTPRequestHandler
from lab7 import get_currencies
import os

# Инициализация данных
main_author = Author("Kamila", 'Р3124')
main_user = User('543454', 'Leisan')
main_user1 = User('505032', 'Rashit')
main_app = App("Знаю все валюты", "1.0.0", main_author)

# Примерные данные для демонстрации
currencies_data = [
    Currency("R01235", "840", "USD", "Доллар США", 90.5, 1),
    Currency("R01239", "978", "EUR", "Евро", 98.2, 1),
    Currency("R01035", "826", "GBP", "Фунт стерлингов", 115.0, 1),
    Currency("R01820", "392", "JPY", "Японская иена", 0.61, 100)
]

users_data = [main_user, main_user1]

# Подписки пользователей
subscriptions = [
    UserCurrency("1", main_user.id, "R01235"),  # Leisan подписан на USD
    UserCurrency("2", main_user.id, "R01239"),  # Leisan подписан на EUR
    UserCurrency("3", main_user1.id, "R01035"),  # Rashit подписан на GBP
]

# Определяем путь к директории с шаблонами
current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(current_dir, 'templates')

# Инициализация Jinja2 Environment с FileSystemLoader
env = Environment(
    loader=FileSystemLoader(templates_dir),
    autoescape=select_autoescape()
)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        # Устанавливаем заголовки по умолчанию
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        if parsed_path.path == '/':
            # Главная страница
            template = env.get_template("index.html")
            result = template.render(
                app_name=main_app.name,
                myapp=main_app.name,
                version=main_app.version,
                navigation=[
                    {'caption': 'Основная страница', 'href': '/'},
                    {'caption': 'Об авторе', 'href': '/author'},
                    {'caption': 'Пользователи', 'href': '/users'},
                    {'caption': 'Курсы валют', 'href': '/currencies'}
                ],
                author_name=main_app.author.name,
                author_group=main_author.group,
                user_id=main_user.id,
                user_name=main_user.name,
                user1_id=main_user1.id,
                user1_name=main_user1.name
            )

        elif parsed_path.path == '/author':
            # Страница об авторе
            template = env.get_template("author.html")
            result = template.render(
                author_name=main_author.name,
                author_group=main_author.group,
                app_name=main_app.name,
                app_version=main_app.version,
                navigation=[
                    {'caption': 'Основная страница', 'href': '/'},
                    {'caption': 'Об авторе', 'href': '/author'},
                    {'caption': 'Пользователи', 'href': '/users'},
                    {'caption': 'Курсы валют', 'href': '/currencies'}
                ]
            )

        elif parsed_path.path == '/users':
            # Список пользователей
            template = env.get_template("users.html")
            result = template.render(
                app_name=main_app.name,
                navigation=[
                    {'caption': 'Основная страница', 'href': '/'},
                    {'caption': 'Об авторе', 'href': '/author'},
                    {'caption': 'Пользователи', 'href': '/users'},
                    {'caption': 'Курсы валют', 'href': '/currencies'}
                ],
                users=users_data
            )

        elif parsed_path.path == '/user':
            # Страница пользователя
            user_id = query_params.get('id', [None])[0]

            if not user_id:
                result = "<html><body><h1>400 - Не указан ID пользователя</h1></body></html>"
                self.send_response(400)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
            else:
                # Находим пользователя
                user = next((u for u in users_data if u.id == user_id), None)

                if not user:
                    result = "<html><body><h1>404 - Пользователь не найден</h1></body></html>"
                    self.send_response(404)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.end_headers()
                else:
                    # Находим подписки пользователя
                    user_subscriptions = []
                    for sub in subscriptions:
                        if sub.user_id == user_id:
                            currency = next((c for c in currencies_data if c.id == sub.currency_id), None)
                            if currency:
                                user_subscriptions.append(currency)

                    template = env.get_template("user.html")
                    result = template.render(
                        app_name=main_app.name,
                        navigation=[
                            {'caption': 'Основная страница', 'href': '/'},
                            {'caption': 'Об авторе', 'href': '/author'},
                            {'caption': 'Пользователи', 'href': '/users'},
                            {'caption': 'Курсы валют', 'href': '/currencies'}
                        ],
                        user=user,
                        subscriptions=user_subscriptions
                    )

        elif parsed_path.path == '/currencies':
            # Страница с курсами валют
            template = env.get_template("currencies.html")

            try:
                # Получаем актуальные курсы валют
                actual_rates = get_currencies(["USD", "EUR", "GBP", "JPY"])

                # Обновляем наши данные с актуальными курсами
                updated_currencies = []
                for currency in currencies_data:
                    if currency.char_code in actual_rates:
                        # Обновляем существующий объект
                        currency.value = actual_rates[currency.char_code]
                        updated_currencies.append(currency)
                    else:
                        updated_currencies.append(currency)

                result = template.render(
                    app_name=main_app.name,
                    navigation=[
                        {'caption': 'Основная страница', 'href': '/'},
                        {'caption': 'Об авторе', 'href': '/author'},
                        {'caption': 'Пользователи', 'href': '/users'},
                        {'caption': 'Курсы валют', 'href': '/currencies'}
                    ],
                    currencies=updated_currencies,
                    success=True,
                    error=None
                )
            except Exception as e:
                # Если произошла ошибка при получении курсов, показываем старые данные
                result = template.render(
                    app_name=main_app.name,
                    navigation=[
                        {'caption': 'Основная страница', 'href': '/'},
                        {'caption': 'Об авторе', 'href': '/author'},
                        {'caption': 'Пользователи', 'href': '/users'},
                        {'caption': 'Курсы валют', 'href': '/currencies'}
                    ],
                    currencies=currencies_data,
                    success=False,
                    error=str(e)
                )

        else:
            # 404 для неизвестных путей
            result = "<html><body><h1>404 - Страница не найдена</h1></body></html>"
            self.send_response(404)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()

        self.wfile.write(bytes(result, "utf-8"))


if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    print('Server is running on http://localhost:8080')
    httpd.serve_forever()








