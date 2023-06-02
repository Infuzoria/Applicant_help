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

# Добавить ссылку
def add_url(message):
    find_record = re.findall(r"(https?://[\S]+)", message.text)
    if len(find_record) != 0:
        result = BotDB.get_records(user, message.from_user.id)
        for i in result:
            if i == find_record[0]:
                bot.send_message(message.chat.id, "Такая ссылка уже есть")
                return True
        BotDB.add_record(user, message.from_user.id, find_record[0])
        bot.send_message(message.chat.id, "Ссылка успешно добавлена")
    else:
        bot.send_message(message.chat.id, "Ссылка введена некорректно, попробуйте ещё раз")

def check_list(message):
    if all([x.isdigit() for x in message.text]):
        number = int(message.text)
        count = BotDB.count_of_records(user, message.from_user.id)
        if 1 <= number <= count:
            result = BotDB.get_records(user, message.from_user.id)
            url = result[number - 1]

            # Разбиваем на части и выводим список по 10 позиций
            table = parser(str(url))
            for i in range(len(table) // 10):
                if i == 0:
                    text = "Конкурсный список:"
                else:
                    text = ""
                for row in range(i * 10, i * 10 + 10):
                    for key, val in table[row].items():
                        text += f'\n{key}: {val}'
                    text += '\n---------------------------'
                bot.send_message(message.chat.id, text)

            # Выводим оставшиеся записи
            text = ""
            for i in range((len(table) // 10) * 10, len(table)):
                for key, val in table[i].items():
                    text += f'\n{key}: {val}'
                text += '\n---------------------------'
            if text != "":
                bot.send_message(message.chat.id, text)
        else:
            bot.send_message(message.chat.id, "Такого номера нет в списке, попробуйте ввести значение ещё раз")
    else:
        bot.send_message(message.chat.id, "Номер введен некорректно, попробуйте ещё раз")

def check_position(message):
    if all([x.isdigit() for x in message.text]):
        number = int(message.text)
        count = BotDB.count_of_records(user, message.from_user.id)

        if 1 <= number <= count:
            snils = BotDB.get_snils(user, message.from_user.id)
            result = BotDB.get_records(user, message.from_user.id)
            url = result[number - 1]
            table = parser(str(url))

            for row in table:
                if row['ID'] == snils:
                    text = f"Ваш порядковый номер: {row['№']}"
                    text += '\n---------------------------'
                    text += f"\nID: {row['ID']}"
                    text += f"\nРус. язык: {row['Рус. язык']}"
                    text += f"\nМатематика(профиль): {row['Математика(профиль)']}"
                    text += f"\nИнформатика и ИКТ: {row['Информатика и ИКТ']}"
                    text += f"\nДоп. баллы: {row['Доп. баллы']}"
                    text += f"\nСумма баллов: {row['Сумма баллов']}"
                    text += f"\nСогласие на зачисление: {row['Согласие на зачисление']}"
                    bot.send_message(message.chat.id, text)
                    return True
            bot.send_message(message.chat.id, "Кажется, вас нет в этом списке. Проверьте введенный номер СНИЛС и номер выбранного списка")

        else:
            bot.send_message(message.chat.id, "Такого номера нет в списке, попробуйте ввести значение ещё раз")
    else:
        bot.send_message(message.chat.id, "Номер введен некорректно, попробуйте ещё раз")

def check_by_number(message):
    request = message.text.split()

    if all([x.isdigit() for x in request[0]]):
        number = int(request[0])
        count = BotDB.count_of_records(user, message.from_user.id)

        if 1 <= number <= count:
            if all([x.isdigit() for x in request[1]]):
                result = BotDB.get_records(user, message.from_user.id)
                url = result[number - 1]
                table = parser(str(url))
                text = ""

                if 1 <= int(request[1]) <= len(table):
                    for row in table:
                        if row['№'] == request[1]:
                            text += '\n---------------------------'
                            text += f"\n№: {row['№']}"
                            text += f"\nID: {row['ID']}"
                            text += f"\nРус. язык: {row['Рус. язык']}"
                            text += f"\nМатематика(профиль): {row['Математика(профиль)']}"
                            text += f"\nИнформатика и ИКТ: {row['Информатика и ИКТ']}"
                            text += f"\nДоп. баллы: {row['Доп. баллы']}"
                            text += f"\nСумма баллов: {row['Сумма баллов']}"
                            text += f"\nСогласие на зачисление: {row['Согласие на зачисление']}"
                            text += '\n---------------------------'
                            bot.send_message(message.chat.id, text)
                else:
                    bot.send_message(message.chat.id, "Такого номера нет в списке, проверьте введенные данные")
            else:
                bot.send_message(message.chat.id, "Номер строки введен некорректно, попробуйте ещё раз")
        else:
            bot.send_message(message.chat.id, "Такого номера нет в списке, попробуйте ввести значение ещё раз")
    else:
        bot.send_message(message.chat.id, "Номер списка введен некорректно, попробуйте ещё раз")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Добавление клавиатуры с кнопками
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🪪 Добавить СНИЛС")
    btn2 = types.KeyboardButton("🔗 Добавить ссылку")
    btn3 = types.KeyboardButton("💻 Просмотр всех ссылок")
    btn4 = types.KeyboardButton("📑 Посмотреть список")
    btn5 = types.KeyboardButton("📍 Проверить позицию")
    btn6 = types.KeyboardButton("🔎 Поиск по номеру")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)

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

    if(message.text == "🔗 Добавить ссылку"):
        bot.send_message(message.chat.id, "Введите ссылку на страницу с конкурсным списком")
        bot.register_next_step_handler(message, add_url)

    if(message.text == "💻 Просмотр всех ссылок"):
        result = BotDB.get_records(user, message.from_user.id)
        if len(result) != 0:
            text = "Список введенных ссылок:"
            for index, url in enumerate(result):
                text += f'\n{index+1}. {url}'
            bot.send_message(message.chat.id, text)
        else:
            bot.send_message(message.chat.id, "Вы не добавили ни одной ссылки")

    if(message.text == "📍 Проверить позицию"):
        bot.send_message(message.chat.id, "Введите порядковый номер конкурсного списка, в котором желаете проверить свою позицию."
                                          "Для того, чтобы посмотреть список ссылок, используйте команду: 💻 Просмотр всех ссылок")
        bot.register_next_step_handler(message, check_position)

    if(message.text == "📑 Посмотреть список"):
        bot.send_message(message.chat.id, "Введите порядковый номер url из списка ваших добавленных ссылок. "
                                          "Для того, чтобы посмотреть список ссылок, используйте команду: 💻 Просмотр всех ссылок")
        bot.register_next_step_handler(message, check_list)

    if(message.text == "🔎 Поиск по номеру"):
        bot.send_message(message.chat.id, "Введите порядковый номер списка, в котором желаете посмотреть информацию. "
                                          "Через пробел укажите порядковый номер записи в списке. "
                                          "Для того, чтобы посмотреть список ссылок, используйте команду: 💻 Просмотр всех ссылок")
        bot.register_next_step_handler(message, check_by_number)

bot.polling()