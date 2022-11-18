import telebot
import requests
import os, os.path
import random
from telebot import types
from tockenbot import tocken
import time



sticker1 = open("/script/sticker.webp", "rb")
bot = telebot.TeleBot(tocken)
photo = []
stick = 0


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🥰🥰Сонечка🥰🥰")
    btn2 = types.KeyboardButton("Егорик👻")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Ты -", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text(message):
    global stick
    vibor = ""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Фоточка")
    markup.add(btn1)
    if (message.text == "🥰🥰Сонечка🥰🥰"):
        bot.send_message(message.chat.id, "Привет солнце😘")

        if (os.path.isfile("/script/id/" + str(message.chat.id) + ".txt") == True):
            with open("/script/id/" + str(message.chat.id) + ".txt", "r") as f:
                f.seek(0)
                vibor = f.readline()
        else:
            with open("/script/id/" + str(message.chat.id) + ".txt", "w+") as f:
                f.write("Sonya")
                f.seek(0)
                vibor = f.readline()
        if (stick == 0):
            bot.send_sticker(message.chat.id, sticker1)
            stick = stick + 1
        bot.send_message(
            message.chat.id, "Отправь фотку, чтобы я её сохранил<3", reply_markup=markup)
    elif (message.text == "Егорик👻"):
        if (os.path.isfile("/script/id/" + str(message.chat.id) + ".txt") == True):
            with open("/script/id/" + str(message.chat.id) + ".txt", "r") as f:
                f.seek(0)
                vibor = f.readline()
        else:
            with open("/script/id/" + str(message.chat.id) + ".txt", "w+") as f:
                f.write("Egor")
                f.seek(0)
                vibor = f.readline()
        bot.send_message(
            message.chat.id, "Отправь фотку своей женщине бездарь", reply_markup=markup)

    if (message.text == "Фоточка"):
        with open("/script/id/" + str(message.chat.id) + ".txt", "r") as f:
            f.seek(0)
            vibor = f.readline()
        if (vibor == "Sonya"):
            answer = random.choice(os.listdir("/script/Egor/"))
            try:
                bot.send_photo(message.chat.id, open(
                    "/script/Egor/" + answer, "rb"), reply_markup=markup)
            except:
                time.sleep(1)
        elif (vibor == "Egor"):
            if (len(os.listdir("/script/Sonya/")) == 0):
                bot.send_message(message.chat.id, "Ещё пока пусто")
            else:
                answer = random.choice(os.listdir("/script/Sonya/"))
                try:
                    bot.send_photo(message.chat.id, open(
                        "/script/Sonya/" + answer, "rb"), reply_markup=markup)
                except:
                    time.sleep(1)

@bot.message_handler(content_types=['photo'])
def save_photo(message):
    fileid = message.photo[-1].file_id
    file_info = bot.get_file(fileid)
    photo.clear()
    with open("/script/id/" + str(message.chat.id) + ".txt", "r") as f:
        f.seek(0)
        vibor = f.readline()
    if (vibor == "Sonya"):
        photo.append(fileid)
        if (len(photo) == 1):
            bot.send_message(message.chat.id, "Фоточка пришла зайчик❤️")
            photo.clear()
            respone = requests.get(
                "https://api.telegram.org/file/bot" + tocken + "/" + file_info.file_path)
            if (respone.status_code == 200):
                with open("/script/Sonya/" + "Photo_" + str(len(os.listdir(vibor))) + ".jpg", "wb") as f:
                    f.write(respone.content)
            else:
                bot.send_message(message.chat_id, "Ещё раз")
        else:
            try:
                bot.send_message(message.chat.id, "Фоточка не пришла :( Попробуй ещё раз")
            except:
                time.sleep(1)
    elif (vibor == "Egor"):
        photo.append(fileid)
        if (len(photo) == 1):
            bot.send_message(message.chat.id, "Фоточка пришла")
            photo.clear()
            respone = requests.get(
                'https://api.telegram.org/file/bot' + tocken + "/" + file_info.file_path)
            if (respone.status_code == 200):
                with open("/script/Egor/" + "Photo_" + str(len(os.listdir(vibor))) + ".jpg", "wb") as f:
                    f.write(respone.content)
            else:
                bot.send_message(message.chat_id, "Ещё раз")
        else:
            try:
                bot.send_message(message.chat.id, "Фоточка не пришла :( Попробуй ещё раз")
            except:
                time.sleep(1)

 
bot.infinity_polling()
