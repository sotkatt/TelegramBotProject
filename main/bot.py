import requests
import logging
from datetime import datetime

import telebot
from telebot import types

from django.conf import settings

from main.utils import utils, chart
from main.keyboards.inlines import *
from main.keyboards.buttons import menu_button, income_button, expense_button, chart_button 
from main.models import (
    TelegramUser, TelegramUserIncome, 
    TelegramAnswers, TelegramSupport,
    TelegramExpense
)


logging.basicConfig(
    filename='main.log', level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

bot = telebot.TeleBot(settings.TOKEN_KEY, parse_mode="HTML")


@bot.message_handler(commands=['start'])
def start(message):

    t_user: types.User = message.from_user

    model_user, created = TelegramUser.objects.get_or_create(user_id=t_user.id)
    
    if created:
        model_user.user_id = t_user.id
        model_user.username = t_user.username
        model_user.first_name = t_user.first_name
        model_user.last_name = t_user.last_name
        model_user.language_code = t_user.language_code
        model_user.is_bot = t_user.is_bot
        model_user.save()

        logging.info(f'Был создан новый аккаунт {model_user.get_name()}')
    
    bot.send_message(message.chat.id, f"Привет, {model_user.get_name()}!", reply_markup=menu_button())


def get_photo_t_user_profile(message: types.Message):
    t_user: types.User = message.from_user
    photos = bot.get_user_profile_photos(t_user.id, limit=1)

    if photos.photos:
        return photos.photos[0][-1].file_id


@bot.message_handler(func=lambda message: message.text == 'Профиль')
def t_user_profile(message):
    t_user: types.User = message.from_user
    model_user = TelegramUser.objects.get(user_id=t_user.id)

    user_profile = (
        f"<b>ID:</b> <code>{model_user.user_id}</code>\n"
        f"<b>Имя:</b> <code>{model_user.first_name}</code>\n"
        f"<b>Фамилия:</b> <code>{model_user.last_name}</code>\n"
        f"<b>Никнейм:</b> <code>@{model_user.username}</code>\n"
        f"<b>Код языка:</b> <code>{model_user.language_code}</code>\n"
        f"<b>Бот:</b> <code>{'Да' if model_user.is_bot else 'Нет'}</code>\n"
        f"\n"
        f"<b>Ваш баланс:</b> <code>{model_user.balance} ₸</code>"
    )

    logging.info(f"Пользователь {model_user.get_name()} в профиле.") 

    try:
        bot.send_photo(message.chat.id, get_photo_t_user_profile(message), user_profile)

    except Exception as e:
        logging.error(f"Ошибка при отправке фото {model_user.get_name()}: {e}!")
        bot.send_message(message.chat.id, user_profile)


def income_amount(message, name):
    t_user: types.User = message.from_user
    model_user = TelegramUser.objects.get(user_id=t_user.id)

    if message.text.lower() == 'отмена':
        bot.send_message(message.chat.id, "Действие отменено!", reply_markup=menu_button())
        return

    try:
        amount = int(message.text)
    except:
        bot.send_message(message.chat.id, "Некорректный ввод!")
        bot.register_next_step_handler(message, income_amount, name)
        return
    
    if amount < 100:
        bot.send_message(message.chat.id, "Сумма дохода должна быть больше 100!")
        bot.register_next_step_handler(message, income_amount, name)
        return
    
    model_user.balance += amount
    imcome = TelegramUserIncome.objects.create(
        user=model_user, 
        name=name, 
        amount=amount
    )
    imcome.save()
    model_user.save()
    bot.send_message(message.chat.id, f"Доход добавлен!\nВаш баланс: {model_user.balance} ₸", reply_markup=menu_button())


def income_source(message):
    if message.text.lower() == 'отмена':
        bot.send_message(message.chat.id, "Действие отменено!", reply_markup=menu_button())
        return
    
    elif utils.income_name_choice(message.text):
        cancel_button = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            types.KeyboardButton(text="Отмена")
        )
        bot.send_message(message.chat.id, "Введите сумму дохода:", reply_markup=cancel_button)
        bot.register_next_step_handler(message, income_amount, message.text)
    else:
        bot.send_message(message.chat.id, "Некорректный ввод!", reply_markup=income_button())
        bot.register_next_step_handler(message, income_source)


@bot.message_handler(func=lambda message: message.text == 'Доход')
def income(message):
    text = "Выберите источник дохода:"
    bot.send_message(message.chat.id, text, reply_markup=income_button())
    bot.register_next_step_handler(message, income_source)


def support_answer_message(model_user, questions, answer):
    text = (
        f"Привет {model_user.get_name()}!\n"
        f"Администраторы ответили на ваш вопрос \n'{questions}'\n\n"
        f"Ответ: {answer}"
    )
    bot.send_message(model_user.user_id, text=text, reply_markup=menu_button())


def support_message(message):
    if message.text.lower() == 'отмена':
        bot.send_message(message.chat.id, "Действие отменено!", reply_markup=menu_button())
        return

    t_user: types.User = message.from_user
    model_user = TelegramUser.objects.get(user_id=t_user.id)

    model_support = TelegramSupport.objects.create(user=model_user, message=message.text)
    model_support.save()
    bot.send_message(message.chat.id, "Ваше сообщение отправлено!", reply_markup=menu_button())


@bot.message_handler(func=lambda message: message.text.lower() == "поддержка")
def support(message):

    cancel_button = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
        types.KeyboardButton(text="Отмена")
    )

    bot.send_message(message.chat.id, "Введите ваше сообщение:", reply_markup=cancel_button)
    bot.register_next_step_handler(message, support_message)


def expense_amount(message, name):
    t_user: types.User = message.from_user
    model_user = TelegramUser.objects.get(user_id=t_user.id)

    if message.text.lower() == 'отмена':
        bot.send_message(message.chat.id, "Действие отменено!", reply_markup=menu_button())
        return
    
    try:
        amount = int(message.text)
    except:
        bot.send_message(message.chat.id, "Некорректный ввод!")
        bot.register_next_step_handler(message, expense_amount, name)
        return
    
    if amount < 100:
        bot.send_message(message.chat.id, "Сумма расхода должна быть больше 100!")
        bot.register_next_step_handler(message, expense_amount, name)
        return
    
    if amount > model_user.balance:
        bot.send_message(message.chat.id, "Недостаточно средств!")
        bot.register_next_step_handler(message, expense_amount, name)
        return
    
    model_user.balance -= amount
    expense = TelegramExpense.objects.create(
        user=model_user, 
        name=name, 
        amount=amount
    )
    expense.save()
    model_user.save()
    bot.send_message(message.chat.id, f"Расход добавлен!\nВаш баланс: {model_user.balance} ₸", reply_markup=menu_button())


def expense_source(message):
    if message.text.lower() == 'отмена':
        bot.send_message(message.chat.id, "Действие отменено!", reply_markup=menu_button())
        return
    
    elif utils.expenses_name_choice(message.text):
        cancel_button = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            types.KeyboardButton(text="Отмена")
        )
        bot.send_message(message.chat.id, "Введите сумму расхода:", reply_markup=cancel_button)
        bot.register_next_step_handler(message, expense_amount, message.text)
    
    else:
        bot.send_message(message.chat.id, "Некорректный ввод!", reply_markup=expense_button())
        bot.register_next_step_handler(message, expense_source)


@bot.message_handler(func=lambda message: message.text == 'Расход')
def expense(message):
    text = "Выберите источник расхода:"
    bot.send_message(message.chat.id, text, reply_markup=expense_button())
    bot.register_next_step_handler(message, expense_source)


def chart_source(message):
    if message.text.lower() == 'отмена':
        bot.send_message(message.chat.id, "Действие отменено!", reply_markup=menu_button())
        return

    elif message.text == "График расхода":
        
        chart_expense_photo_url = chart.user_chart_expense(message.chat.id)
        r = requests.get(settings.MY_DOMAIN + chart_expense_photo_url)
        if r.status_code == 200:
            bot.send_photo(message.chat.id, r.content, reply_markup=menu_button())
        else:
            bot.send_message(message.chat.id, "График повреждена!", reply_markup=menu_button())
        
        return
    
    elif message.text == "График дохода":
        chart_income_photo_url = chart.user_chart_income(message.chat.id)

        r = requests.get(settings.MY_DOMAIN + chart_income_photo_url)

        if r.status_code == 200:
            bot.send_photo(message.chat.id, r.content, reply_markup=menu_button())
        else:
            bot.send_message(message.chat.id, "График повреждена!", reply_markup=menu_button())
        
        return

    else:
        bot.send_message(message.chat.id, "Некорректный ввод!")
        bot.register_next_step_handler(message, chart_source)


@bot.message_handler(func=lambda message: message.text == 'График')
def chart_1(message):
    text = f"Выберите опцию:"
    bot.send_message(message.chat.id, text, reply_markup=chart_button())
    bot.register_next_step_handler(message, chart_source)


def run_bot():
    try:
        bot_username = bot.get_me().username
        logger = logging.getLogger(f"Был запушен бот {bot_username}.")
        print(f"Был запушен бот {bot_username}.")
        bot.polling(none_stop=True, interval=0)
    
    except KeyboardInterrupt:
        logger.info("Бот остановлен принудительно!")

    except SystemExit:
        logger.info("Бот остановлен ошобка системы!")

    finally:
        logger.info("Завершение работы бота!")
