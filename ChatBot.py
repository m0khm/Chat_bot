from telebot import *
import webbrowser
import random
from collections import deque

token = '6859364358:AAHHTy-kixk-ab3CkghS5KKsCqaNQqvF_G0'
bot = telebot.TeleBot(token)
answers = ['Я не понял, что ты хочешь сказать.', 'Извини, я тебя не понимаю.', 'Я не знаю такой команды.']
users = []
chats = {} # Словарь для хранения информации о чате между пользователями

@bot.message_handler(commands=['start'])
def welcome(message):
    # Добавляем кнопки, которые будут появляться после ввода команды /start
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🧿 Узнать мой айди')
    button2 = types.KeyboardButton('💬 Начать чат')
    button3 = types.KeyboardButton('📄 Данные о разработчике')
    # Разделяю кнопки по строкам так, чтобы товары были отдельно от остальных кнопок
    markup.row(button1)
    markup.row(button2, button3)
    if message.chat.id in chats:
        del chats[message.chat.id]
    if message.text == '/start':
        # Отправляю приветственный текст
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\nУ меня ты сможешь пообщаться с разными людьми или же узнать свой id\nКонтакт моего разработчика: https://t.me/nookiqq', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Перекинул тебя в главном меню! Выбирай!', reply_markup=markup)

@bot.message_handler()
def info(message):
    if message.text == '🧿 Узнать мой айди':
        aidi(message)
    elif message.text == '💬 Начать чат':
        chat(message)
    elif message.text == '📄 Данные о разработчике':
        infos(message)
    elif message.text == '✏️ Написать разработчику':
        bot.send_message(message.chat.id, 'Успешно!')
    elif message.text == '↩️ Назад в меню':
        welcome(message)
    elif message.text == '❌ Закончить чат':
        # Удаляем пользователя из словаря chats
        
        # Отправляем сообщение о завершении чата второму пользователю
        bot.send_message(chats[message.chat.id], 'Чат завершен!', reply_markup=types.ReplyKeyboardRemove())
        # Удаляем второго пользователя из словаря chats
        del chats[chats[message.chat.id]]
        welcome(message)
    else:
        # Если сообщение не является командой, пересылаем его второму пользователю, если он есть в словаре chats
        if message.chat.id in chats:
            bot.forward_message(chats[message.chat.id], message.chat.id, message.message_id)
        else:
            bot.send_message(message.chat.id, answers[random.randint(0, 2)])

def infos(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('✏️ Написать разработчику')
    button2 = types.KeyboardButton('↩️ Назад в меню')
    markup.row(button1, button2)
    bot.send_message(message.chat.id, 'Раздел справки.\nЗдесь ты можешь написать моему разработчику.', reply_markup=markup)

def chat(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('❌ Закончить чат')
    friend_id = message.from_user.id
    users.append(friend_id)
    if len(users) > 1:
        markup.row(button1)
        # Добавляем пользователей в словарь
        chats[users[0]] = users[1]
        chats[users[1]] = users[0]
        bot.send_message(users[1], 'Начался чат!', reply_markup=markup)
        # Отправляем сообщение о начале чата второму пользователю
        bot.send_message(users[0], 'Начался чат!', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Найдите другого пользователя, который также нажал на кнопку "Начать чат"')

def aidi(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('↩️ Назад в меню')
    markup.row(button1)
    bot.send_message(message.chat.id, f'Твой айди:{message.chat.id}', reply_markup=markup)


# Обработчик сообщений, который будет пересылать сообщения между пользователями, если они находятся в чате
@bot.message_handler(func=lambda message: message.chat.id in chats)
def forward_message(message):
    if message.text == '❌ Закончить чат':
        # Удаляем пользователя из словаря chats
        del chats[message.chat.id]
        # Отправляем сообщение о завершении чата второму пользователю
        bot.send_message(chats[message.chat.id], 'Чат завершен!', reply_markup=types.ReplyKeyboardRemove())
        # Удаляем второго пользователя из словаря chats
        del chats[chats[message.chat.id]]
    else:
        # Пересылаем сообщение второму пользователю
        bot.forward_message(chats[message.chat.id], message.chat.id, message.message_id)

bot.polling()


