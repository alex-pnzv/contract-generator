from num2words import num2words
from Exceptions.exceptions import InvalidSum, InvalidUserName, InvalidDate


def price_to_words(price: str, upper: bool = None):
    if len(price.split(",")) == 2:
        price = price.replace(',', '.')

    try:
        float(price)
    except Exception:
        raise InvalidSum

    uah = num2words(price, lang='uk', to='currency', currency='UAH', cents=False, separator='')
    if upper:
        uah = num2words(price, lang='uk', to='currency', currency='UAH', cents=False, separator='').capitalize()
    return uah


def initials_end(name):
    fio = name.split(" ")
    try:
        firstname = fio[1][0]
        lastname = fio[0]
        patronymic = fio[2][0]
    except IndexError:
        raise InvalidUserName
    return "{} {}.{}.".format(lastname, firstname, patronymic)


def initials_start(name):
    fio = name.split(" ")
    try:
        firstname = fio[1][0]
        lastname = fio[0]
        patronymic = fio[2][0]
    except IndexError:
        raise InvalidUserName
    return "{}.{}. {}".format(firstname, patronymic, lastname)


def month_to_text(date):
    month = {'01': 'січня',
             '02': 'лютого',
             '03': 'березня',
             '04': 'квітня',
             '05': 'травня',
             '06': 'червня',
             '07': 'липня',
             '08': 'серпня',
             '09': 'вересня',
             '10': 'жовтня',
             '11': 'листопада',
             '12': 'грудня'
             }

    if len(date.split(".")) >= 3:
        date = date.split(".")
    elif len(date.split(",")) >= 3:
        date = date.split(",")
    else:
        raise InvalidDate

    if int(date[1]) > 12:
        raise InvalidDate
    day = date[0]
    month = month[date[1]]
    year = date[2]
    return '{} {} {}'.format(day, month, year)
