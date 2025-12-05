from models import Author


class App():
    def __init__(self, name: str, version: str, author: Author):
        self.__name: str = name
        self.__version: str = version
        self.__author: Author = author

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):  # Исправлено: было id
        if type(name) is str and len(name) >= 1:
            self.__name = name  # Исправлено: было id
        else:
            raise ValueError('Ошибка при задании названия приложения')

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, version: str):
        if type(version) is str and len(version) >= 1:
            self.__version = version
        else:
            raise ValueError('Ошибка при задании версии приложения')

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, author: Author):
        if isinstance(author, Author):
            self.__author = author
        else:
            raise ValueError('Ошибка при задании автора приложения')