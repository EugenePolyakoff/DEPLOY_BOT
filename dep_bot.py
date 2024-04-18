import csv
import logging
import os
import re
import telebot
from time import sleep
from test_json import json_parser


BOT_TOKEN = "6707281922:AAEsdZWnILxsOl3qx9a0JOR7nrK3C_0qjf8"
bot = telebot.TeleBot(BOT_TOKEN)


def start_deploy():
    os.system("/Users/e.polyakov/Downloads/DEPLOY_BOT/qradare_remote_deploy.sh")


# Обработчик команды /start
@bot.message_handler(commands=['deploy_siem'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = telebot.types.KeyboardButton('Проверка наличия сёрча')
    markup.add(itembtn1)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):

    search_exists = False  # Логика проверки наличия серча

    try:
        os.system("/Users/e.polyakov/Downloads/DEPLOY_BOT/get_json_to_bot.sh")
    except Exception as e:
        logging.error(f"ERROR: {e}")
    while os.stat('/Users/e.polyakov/Downloads/DEPLOY_BOT/stdout.json').st_size == 0:
        continue
    users = json_parser()
    if users:
        search_exists = True

    if message.text == 'Проверка наличия сёрча':
        # Проверка наличия серча
        if search_exists:
            searchers = take_peoples_from_bd(users)
            if not searchers or searchers == None:
                bot.send_message(message.chat.id, f"You don't have permission to DB or DB is empty.")
                logging.error(f"ERROR: You don't have permission to DB or DB is empty.")
                return
            bot.send_message(message.chat.id, f"Всем привет! Планируем сейчас запустить деплой!\n"
                                              f"{get_tg_tags(searchers)}"
                                              f"Подтвердите запуск сёрча!\n"
                                              f"С момента появления этого сообщения, не стройте сёрчи.")

            # Если серч есть, отправляем сообщение и прячем кнопки
            bot.send_message(message.chat.id, "Сёрч строится: руки убрать от кнопки деплоя.", reply_markup=telebot.types.ReplyKeyboardRemove())
        else:
            # Если серча нет, создаем кнопку с одной кнопкой
            markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
            itembtn2 = telebot.types.KeyboardButton('Планируем сейчас запустить деплой!')
            markup.add(itembtn2)

            # Отправляем сообщение с кнопкой
            bot.send_message(message.chat.id, "Сёрча нет. Планируем сейчас запустить деплой!", reply_markup=markup)
    elif message.text == 'Планируем сейчас запустить деплой!':
        # Создаем две кнопки
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = telebot.types.KeyboardButton('Можно')
        itembtn2 = telebot.types.KeyboardButton('Нельзя')
        markup.add(itembtn1, itembtn2)

        # Отправляем сообщение с кнопкой
        bot.send_message(message.chat.id, "Планируется запуск. Можно или нельзя?", reply_markup=markup)
    elif message.text == 'Можно':
        # Отправляем сообщение о начале деплоя через 5 минут
        bot.send_message(message.chat.id, "Деплой начнется через 5 минут.", reply_markup=telebot.types.ReplyKeyboardRemove())
        # Ждем 5 минут (300 секунд)
        sleep(3)
        # После 5 минут отправляем сообщение о завершении деплоя
        bot.send_message(message.chat.id, "Деплой начат.")
        start_deploy()
        sleep(3)
        bot.send_message(message.chat.id, "Деплой окончен.")
    elif message.text == 'Нельзя':
        # Создаем клавиатуру с кнопками для выбора времени
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = telebot.types.KeyboardButton('30 мин')
        itembtn2 = telebot.types.KeyboardButton('1 час')
        itembtn3 = telebot.types.KeyboardButton('1,5 часа')
        itembtn4 = telebot.types.KeyboardButton('2 часа')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

        # Отправляем сообщение с кнопкой
        bot.send_message(message.chat.id, "Выберите время через сколько можно прожать деплой:", reply_markup=markup)
    elif message.text in ['30 мин', '1 час', '1,5 часа', '2 часа']:
        # Получаем выбранное время
        chosen_time = message.text
        # Преобразуем в секунды
        if chosen_time == '30 мин':
            wait_time = 1  # 30 минут в секундах
        elif chosen_time == '1 час':
            wait_time = 2  # 1 час в секундах
        elif chosen_time == '1,5 часа':
            wait_time = 3  # 1,5 часа в секундах
        elif chosen_time == '2 часа':
            wait_time = 4  # 2 часа в секундах

        # Уведомляем пользователя о выбранном времени и предлагаем подождать
        bot.send_message(message.chat.id, f"Деплой можно будет запустить через {chosen_time}. Пожалуйста, подождите.")
        # Ждем указанное время и отправляем уведомление о повторной проверке
        sleep(wait_time)
        bot.send_message(message.chat.id, "Проверьте наличие сёрча еще раз.")
        # Возвращаемся к начальным кнопкам проверки серча
        send_welcome(message)



def take_peoples_from_bd(users) -> list:
    searchers_ids = []
    with open('employees_bd.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        if not reader:
            return None
        for user in users:
            for i_people in reader:
                if str(user) in str(i_people):
                    searchers_ids.append(re.search(r'(\w+) - (\S+)', i_people[0]).group(2))
    return searchers_ids


def get_tg_tags(searchers_tags) -> str:
    text_with_tags = ''
    for i_emp in searchers_tags:
        text_with_tags += f'{str(i_emp)}' + '\n'
    print(text_with_tags)
    return text_with_tags


def main():
    bot.polling()


if __name__ == '__main__':
    logging.basicConfig(filename='log.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

    while True:
        main()


