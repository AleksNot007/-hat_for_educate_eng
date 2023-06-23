"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import random
import logging
from telebot import types
import time

import telebot;
bot = telebot.TeleBot('6210749859:AAGd86YJVON5QVXO_lh-8DfgN7Q4iHv4MKs')



@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/show_record":
        bot.send_message(message.from_user.id, "Введи имя пользователя")
        bot.register_next_step_handler(message, check_record)
    elif message.text == "/new_user":
        bot.send_message(message.from_user.id, "Введи имя нового пользователя")
        bot.register_next_step_handler(message, new_user)

    elif message.text == "/train":
        handle = message
        bot.send_message(message.from_user.id, "Ты готов?")
        message = handle
        bot.register_next_step_handler(handle, train)
    
    elif message.text == "/help":
        bot.send_message(message.from_user.id, ("Бот, который тренирует ваши навыки английского языка.\
                                     Есть несколько функций: переводчик (/translate), \
                                    тренер (/train) и писатель (/writer). Выбери команду,\
                                     и узнай, что она делает. Но для начала нужно зарегистрировать пользователя: /new_user"))
    else:
        bot.send_message(message.from_user.id, "Если тебе требуется помощь, напиши /help")

def new_user(message):
    global new_name
    new_name = message.text
    f = open(new_name+".txt", "w+")
    f_rec = open(new_name+"_record"+".txt", "w+")
    f.writelines("0")
    f_rec.writelines("0")
    
def check_record(message):
    current_r = message.text
    with open(current_r+".txt", "r") as f:
            content = f.read()
    bot.send_message(message.from_user.id, "Твой рекорд: "+content+" слов")

def train(message):
    global quiz
    global userword
    quiz = random.choice(list(open('en_dict.txt'))).split()
    translate = quiz[0]
    word = quiz[1]
    k=0
   
    bot.send_message(message.from_user.id, "Как будет на английском "+"'"+word+"'")
    userword = message.text
    if message.text=="/end":
        bot_sen
        bot.register_next_step_handler(message, cheking)
    else:
        bot.register_next_step_handler(message, cheking)
    
        bot.register_next_step_handler(message, train)
    
   


def cheking(message):
    
    if message.text.lower() == quiz[0]:
        bot.send_message(message.from_user.id, "Да! Ты молодец.")
        with open(new_name+".txt", "r") as f:
            content = f.read()
        number = int(content)
        number += 1
        with open(new_name+".txt", 'w') as file:
            file.write(str(number))
        with open(new_name+"_record"+".txt", "r") as file_rec:
            content_rec = file_rec.read()
        number_rec = int(content_rec)
        if number_rec<number:
            with open(new_name+"_record"+".txt", "w") as file_rec_w:
                file_rec_w.write(str(number))
        #bot.send_message(message.from_user.id, "Для продолжения нажми /ok")
        
        return True

    else:
        bot.send_message(message.from_user.id, "Правильно будет "+ quiz[0] )
        #bot.send_message(message.from_user.id, "Для продолжения нажми /ok")
        
        return False

        
   




bot.polling(none_stop=True, interval=0)
   