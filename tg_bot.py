from part_with_parser import parser
import telebot
from telebot import types
from db import BotDB
import re

API_KEY = '6137871025:AAFUh6ZxKtSzAZYhviA-_JuYSUb-iNjrop4'

bot = telebot.TeleBot(API_KEY)
user = BotDB('accountant.db')

# Добавить СНИЛС
def add_snils(message):
    find_snils = re.findall(r"\d{3}-\d{3}-\d{3} \d{2}", message.text)
    if len(find_snils) != 0:
        check_position = BotDB.get_snils(user, message.from_user.id)
        if check_position == "NULL":
            BotDB.add_snils(user, message.from_user.id, find_snils[0])
            bot.send_message(message.chat.id, "СНИЛС успешно добавлен")
        else:
            BotDB.add_snils(user, message.from_user.id, find_snils[0])
            bot.send_message(message.chat.id, "СНИЛС успешно обновлен")
    else:
        bot.send_message(message.chat.id, "СНИЛС введен некорректно, попробуйте ещё раз")



@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Описание команды start
    if (message.text == '/start'):
        if (not BotDB.user_exists(user, message.from_user.id)):
            BotDB.add_user(user, message.from_user.id)
            bot.send_message(message.chat.id, "Добро пожаловать! Этот бот призван упростить жизнь абитуриента, "
                                              "с его помощью можно легко следить за ходом приемной компании."
                                              "\n\nЧто умеет бот:"
                                              "\n/start - информация о командах бота"
                                              "\n🪪 Добавить СНИЛС - добавить или изменить СНИЛС"
                                              "\n🔗 Добавить ссылку - добавить ссылку на конкурсный список"
                                              "\n💻 Просмотр всех ссылок - просмотр всех добавленных ссылок"
                                              "\n📑 Посмотреть список - просмотр конкурсного списка"
                                              "\n📍 Проверить позицию - проверить свою позицию в списке"
                                              "\n🔎 Поиск по номеру - посмотреть информацию по порядковому номеру",
                                              reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "С возвращением!"
                                              "\n\nСписок команд:"
                                              "\n/start - информация о командах бота"
                                              "\n🪪 Добавить СНИЛС - добавить или изменить СНИЛС"
                                              "\n🔗 Добавить ссылку - добавить ссылку на конкурсный список"
                                              "\n💻 Просмотр всех ссылок - просмотр всех добавленных ссылок"
                                              "\n📑 Посмотреть список - просмотр конкурсного списка"
                                              "\n📍 Проверить позицию - проверить свою позицию в списке"
                                              "\n🔎 Поиск по номеру - посмотреть информацию по порядковому номеру",
                                              reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "/get_snils"):
        bot.send_message(message.chat.id, BotDB.get_snils(user, message.from_user.id))

    if(message.text == "🪪 Добавить СНИЛС"):
        bot.send_message(message.chat.id, "Отправьте свой снился в формате: 200-650-900 42")
        bot.register_next_step_handler(message, add_snils)

bot.polling()