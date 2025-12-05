class UserCurrency:
    def __init__(self, id: str, user_id: str, currency_id: str):
        self.__id: str = id
        self.__user_id: str = user_id
        self.__currency_id: str = currency_id

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: str):
        if type(id) is str:
            self.__id = id
        else:
            raise ValueError('Ошибка при задании ID подписки')

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id: str):
        if type(user_id) is str:
            self.__user_id = user_id
        else:
            raise ValueError('Ошибка при задании ID пользователя')

    @property
    def currency_id(self):
        return self.__currency_id

    @currency_id.setter
    def currency_id(self, currency_id: str):
        if type(currency_id) is str:
            self.__currency_id = currency_id
        else:
            raise ValueError('Ошибка при задании ID валюты')