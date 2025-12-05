class Currency:
    def __init__(self, id: str = None, num_code: str = "", char_code: str = "",
                 name: str = "", value: float = 0.0, nominal: int = 1):
        self.__id = id
        self.__num_code = num_code
        self.__char_code = char_code
        self.__name = name
        self.__value = value
        self.__nominal = nominal

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: str):
        if value is not None and not isinstance(value, str):
            raise ValueError("ID должен быть строкой")
        self.__id = value

    @property
    def num_code(self):
        return self.__num_code

    @num_code.setter
    def num_code(self, value: str):
        if not isinstance(value, str) or not value.isdigit() or len(value) != 3:
            raise ValueError("Цифровой код валюты должен состоять из 3 цифр")
        self.__num_code = value

    @property
    def char_code(self):
        return self.__char_code

    @char_code.setter
    def char_code(self, value: str):
        if not isinstance(value, str) or len(value) != 3:
            raise ValueError("Символьный код валюты должен состоять из 3 символов")
        self.__char_code = value.upper()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or len(value) < 2:
            raise ValueError("Название валюты должно содержать минимум 2 символа")
        self.__name = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: float):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Курс валюты должен быть положительным числом")
        self.__value = float(value)

    @property
    def nominal(self):
        return self.__nominal

    @nominal.setter
    def nominal(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Номинал должен быть положительным целым числом")
        self.__nominal = value

    def to_dict(self) -> dict:
        """Преобразование объекта в словарь для БД"""
        return {
            'num_code': self.__num_code,
            'char_code': self.__char_code,
            'name': self.__name,
            'value': self.__value,
            'nominal': self.__nominal
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Currency':
        """Создание объекта из словаря (из БД)"""
        return cls(
            id=str(data.get('id')) if data.get('id') else None,
            num_code=data.get('num_code', ''),
            char_code=data.get('char_code', ''),
            name=data.get('name', ''),
            value=data.get('value', 0.0),
            nominal=data.get('nominal', 1)
        )

    def __str__(self):
        return f"{self.char_code} ({self.name}): {self.value} за {self.nominal}"