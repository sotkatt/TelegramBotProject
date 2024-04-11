def income_name_choice(name):
    income_choice = ['Зарплата', 'Родственники', 'Пассивный доход', 'Аренда недвижимости', 'Инвестиции', 'Фриланс', 'Бизнес', 'Пенсия', 'Стипендия', 'Другое']

    if name in income_choice:
        return True

    else:
        return False
    

def expenses_name_choice(name):
    expenses_choice = ['Еда и напитки','Жилье и коммунальные услуги','Транспорт и топливо','Одежда и обувь','Здоровье и медицинские услуги','Развлечения и отдых','Образование и курсы','Путешествия и отпуск','Подарки и праздники','Сбережения и инвестиции','Другие расходы']

    if name in expenses_choice:
        return True
    
    else:
        return False