import sys
import functools
import logging


# Декоратор для логирования
def logger(func=None, *, handle=sys.stdout):
    if func is None:
        return lambda f: logger(f, handle=handle)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        msg = f"INFO: {func.__name__} called with args={args}, kwargs={kwargs}"
        if isinstance(handle, logging.Logger):
            handle.info(msg)
        else:
            handle.write(msg + "\n")

        try:
            result = func(*args, **kwargs)
            msg = f"INFO: {func.__name__} returned {result}"
            if isinstance(handle, logging.Logger):
                handle.info(msg)
            else:
                handle.write(msg + "\n")
            return result

        except Exception as e:
            msg = f"ERROR: {func.__name__} raised {type(e).__name__}: {e}"
            if isinstance(handle, logging.Logger):
                handle.error(msg)
            else:
                handle.write(msg + "\n")
            raise

    return wrapper


# Настройка файлового логгера
def setup_file_logger():
    """Настраивает логгер для записи в файл"""
    file_logger = logging.getLogger("currency")
    file_logger.setLevel(logging.INFO)  # Уровень логирования

    # Создаём обработчик для записи в файл
    file_handler = logging.FileHandler("currency_log.txt", mode='a', encoding='utf-8')

    # Настраиваем формат сообщений
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    file_logger.addHandler(file_handler)

    return file_logger


# Создаём файловый логгер
file_logger = setup_file_logger()


# Функция для получения курсов валют с файловым логированием

@logger(handle=file_logger)
def get_currencies(currency_codes: list, url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> dict:
    """
    Получает курсы валют от API ЦБ РФ

    Возвращает словарь вида: {"USD": 93.25, "EUR": 101.7}

    Исключения:
    - ConnectionError: API недоступен
    - ValueError: некорректный JSON
    - KeyError: нет ключа "Valute" или валюта отсутствует
    - TypeError: курс валюты имеет неверный тип
    """
    import requests

    # 1. Делаем запрос к API
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException:
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

        # Сохраняем результат как требует задание
        result[code] = float(value)

    return result


# Пример использования (раскомментируйте когда нужно)
if __name__ == "__main__":
    print("Тестируем файловое логирование...")

    try:
        # Вызываем функцию с файловым логированием
        rates = get_currencies(["USD", "EUR"])
        print(f"Полученные курсы: {rates}")
        print("\nЛоги записаны в файл 'currency_log.txt'")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        print("Подробности в лог-файле 'currency_log.txt'")

    # Проверяем логи
    print("\n" + "=" * 50 + "\n")
    print("Содержимое лог-файла 'currency_log.txt':")
    print("-" * 30)
    try:
        with open("currency_log.txt", "r", encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:
        print("Файл логов ещё не создан")


def get_currencies_stdout():
    return None
