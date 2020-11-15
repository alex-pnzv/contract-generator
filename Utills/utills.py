import csv
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from num2words import num2words
from Exceptions.exceptions import InvalidSum, InvalidUserName, InvalidDate


def price_from_str(price: str, sep=','):
    if not price:
        price = "0"
    price = price.replace(' ', '')
    try:
        if len(price.split(",")) == 2:
            price = price.replace(',', '.')
            formatted_price = format(float(price), '.2f')
            if sep == ',':
                return formatted_price.replace('.', ',')
            return formatted_price
        else:
            formatted_price = format(float(price), '.2f')
            if sep == ',':
                return formatted_price.replace('.', ',')
        return formatted_price
    except Exception:
        raise InvalidSum


def save_spec(data, edrpou):
    file_name = fd.asksaveasfilename(defaultextension=".csv", filetypes=(("csv", "*.csv"), ("All files", "*")))
    if file_name:
        try:
            with open(file_name, 'w', newline='', encoding='windows-1251') as csvfile:
                fieldnames = ['Найменування товару/роботи/послуги', 'ДК 016:2010 (ДКПП)', 'ДК 021:2015 (ЄЗС)',
                              'Одиниця виміру', 'Кількість', 'Ціна за одиницю']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
                csv_data = []
                csv_row = {}
                for row in data:
                    csv_row.setdefault('Найменування товару/роботи/послуги', row.get('product'))
                    csv_row.setdefault('ДК 016:2010 (ДКПП)', '')
                    csv_row.setdefault('ДК 021:2015 (ЄЗС)', edrpou)
                    csv_row.setdefault('Одиниця виміру', row.get('measurement'))
                    csv_row.setdefault('Кількість', row.get('quantity'))
                    csv_row.setdefault('Ціна за одиницю', row.get('price'))
                    csv_data.append(csv_row)
                    csv_row = {}
                writer.writeheader()
                writer.writerows(csv_data)
        except Exception as e:
            mb.showerror("Помилка", e)


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
    if len(year) == 2:
        try:
            year = int(year) + 2000
        except Exception:
            raise InvalidDate
    return '{} {} {}'.format(day, month, year)
