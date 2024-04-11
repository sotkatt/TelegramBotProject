from telebot import types


def menu_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    k1 = types.KeyboardButton(text="Профиль")
    k2 = types.KeyboardButton(text="Доход")
    k3 = types.KeyboardButton(text="Расход")
    k4 = types.KeyboardButton(text="График")
    k5 = types.KeyboardButton(text="Поддержка")

    markup.row(k1)
    markup.row(k2, k3)
    markup.row(k4)
    markup.row(k5)

    return markup


def income_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    k1 = types.KeyboardButton(text="Зарплата")
    k2 = types.KeyboardButton(text="Родственники")
    k3 = types.KeyboardButton(text="Пассивный доход")
    k4 = types.KeyboardButton(text="Аренда недвижимости")
    k5 = types.KeyboardButton(text="Инвестиции")
    k6 = types.KeyboardButton(text="Фриланс")
    k7 = types.KeyboardButton(text="Бизнес")
    k8 = types.KeyboardButton(text="Пенсия")
    k9 = types.KeyboardButton(text="Стипендия")
    k10 = types.KeyboardButton(text="Другое")
    k11 = types.KeyboardButton(text="Отмена")
    
    markup.row(k1, k2)
    markup.row(k3, k4)
    markup.row(k5, k6)
    markup.row(k7, k8)
    markup.row(k9, k10)
    markup.row(k11)

    return markup


def expense_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    k1 = types.KeyboardButton(text="Еда и напитки")
    k2 = types.KeyboardButton(text="Жилье и коммунальные услуги")
    k3 = types.KeyboardButton(text="Транспорт и топливо")
    k4 = types.KeyboardButton(text="Одежда и обувь")
    k5 = types.KeyboardButton(text="Здоровье и медицинские услуги")
    k6 = types.KeyboardButton(text="Развлечения и отдых")
    k7 = types.KeyboardButton(text="Образование и курсы")
    k8 = types.KeyboardButton(text="Путешествия и отпуск")
    k9 = types.KeyboardButton(text="Подарки и праздники")
    k10 = types.KeyboardButton(text="Сбережения и инвестиции")
    k11 = types.KeyboardButton(text="Другие расходы")
    k12 = types.KeyboardButton(text="Отмена")

    markup.row(k1, k2)
    markup.row(k3, k4)
    markup.row(k5, k6)
    markup.row(k7, k8)
    markup.row(k9, k10)
    markup.row(k11)
    markup.row(k12)

    return markup


def chart_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    k1 = types.KeyboardButton(text="График дохода")
    k2 = types.KeyboardButton(text="График расхода")
    k3 = types.KeyboardButton(text="Отмена")

    markup.row(k1)
    markup.row(k2)
    markup.row(k3)

    return markup
