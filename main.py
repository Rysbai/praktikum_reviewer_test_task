import datetime as dt
# json не используеться, поэтому не нужно импортировать
# 1 Частые ошибки по стилю кода(PEP8):
# 1.1 Между классами должен быть 2 пустых строк
# 1.2 А между методами класса 1 пустая строка
# 1.3 Вокруг знакаков операци должны быть пробелы. В коде очень много места, где это правило не саблюдаеться
# 1.4 Простая переменная должно состоять из букв нижнего регистра.
# Подробнее: https://www.python.org/dev/peps/pep-0008/


class Record:
    def __init__(self, amount, comment, date=None):  # Обычно если параметр не обязателен, как значение по умаляанию используться None
        self.amount = amount
        self.date = dt.datetime.now().date() if not date else dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []  # Пункт 1.3

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        # Можно писать используя генераторов списков и функцию sum
        # return sum([r.date for r in self.records if r.date == today], 0)

        # sum: https://www.w3schools.com/python/ref_func_sum.asp
        # List comprehensions: https://realpython.com/list-comprehension-python/
        today_stats = 0  # Пункт 1.3
        today = dt.datetime.now().date()  # Лучше обявить дату здесь
        for record in self.records:  # Простая переменная должно состоять из букв нижнего регистра.
            if record.date == today:
                today_stats += record.amount  # Надо писать меньше символов, если есть возможность.

        return today_stats

    def get_week_stats(self):
        # Так же как и предидущий метод, функцию можно упростить используя list comprehensions и sum
        week_stats = 0  # Пункт 1.3
        today = dt.datetime.now().date()
        for record in self.records:
            if (today - record.date).days < 7:  # Можно так упростить проверку, так как нет записей в будущем.
                week_stats += record.amount  # Пункт 1.3
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        """Возвращает остаток калорий на сегодня"""  # Если хочешь описать что делает, его лучше писать в док, потом его можно получить через __dict__
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {x} кКал'
        else:  # Здесь можно впринципе else не писать, потому код сюда спуститься если x > 0 блогодаря return
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Тут можно убрать комментарии, по названию переменной понятно что там храниться
    EURO_RATE = float(70)  # и тут тоже

    def get_today_cash_remained(self, currency, usd_rate=USD_RATE, euro_rate=EURO_RATE):  # параметры должны быть в нижнем регистре
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':  # Пункт 1.3
            cash_remained /= usd_rate
            currency_type = 'USD'
        elif currency_type == 'eur':  # Пункт 1.3
            cash_remained /= euro_rate
            currency_type = 'Euro'  # Пункт 1.3
        elif currency_type == 'rub':   # Пункт 1.3
            cash_remained == 1.00  # Это строка ничего не делает
            currency_type = 'руб'  # Должно быть пробелы вокруг знака операции по PEP8

        if cash_remained > 0:
            return f'На сегодня осталось {round(cash_remained, 2)} {currency_type}'
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:  # Лучше просто писать else, и намного лучше было бы ничего не писать
            return 'Денег нет, держись: твой долг - {0:.2f} {1}'.format(-cash_remained, currency_type)

#  А тут уже три проблемы:
#  1) Не соотвествует заданию, так как возвращает None.
#  2) Не нужно было перегружать метод, по умалчанию python вызвал бы этот метод у родительского класса.
