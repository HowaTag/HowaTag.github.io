import telebot
from telebot import types

alphabet = {
    'А': 'Пан', 'Б': 'пан', 'В': 'ПаН', 'Г': 'ПАн', 'Д': 'пАн',
    'Е': 'Пан Пан', 'Ж': 'Пан пан', 'З': 'пан Пан', 'И': 'пан пан',
    'Й': 'ПаН Пан', 'К': 'ПаН пан', 'Л': 'ПАн Пан', 'М': 'ПАн пан',
    'Н': 'пАн Пан', 'О': 'пАн пан', 'П': 'Пан Пан Пан', 'Р': 'Пан Пан пан',
    'С': 'Пан пан Пан', 'Т': 'Пан пан пан', 'У': 'пан Пан Пан',
    'Ф': 'пан Пан пан', 'Х': 'пан пан Пан', 'Ц': 'пан пан пан',
    'Ч': 'ПаН Пан Пан', 'Ш': 'ПаН Пан пан', 'Щ': 'ПаН пан Пан',
    'Ъ': 'ПаН пан пан', 'Ы': 'ПАн Пан Пан', 'Ь': 'ПАн Пан пан',
    'Э': 'ПАн пан Пан', 'Ю': 'ПАн пан пан', 'Я': 'пАн Пан Пан'
}

reverse_alphabet = {v: k for k, v in alphabet.items()}

def encode(text):
    encoded_text = ""
    for char in text.upper():
        if char in alphabet:
            encoded_text += alphabet[char] + "|"
        elif char == ',':
            encoded_text += "|||"
        elif char == '.':
            encoded_text += "||||"
        elif char == ' ':
            encoded_text += "||"
        elif char == '?':
            encoded_text += "|||||" # Добавлено для обработки знака вопроса
        elif char == '!':
            encoded_text += "||||||" # Добавлено для обработки знака восклицания

    return encoded_text[:-1] if encoded_text else "" # Удаляем последний "|"


def decode(text):
    decoded_text = ""
    words = text.split('|')
    for word in words:
        if word in reverse_alphabet:
            decoded_text += reverse_alphabet[word]
        elif word == "":
            continue
        elif word == "|||":
            decoded_text += ","
        elif word == "||||":
            decoded_text += "."
        elif word == "||":
            decoded_text += " "
        elif word == "|||||":
            decoded_text += "?"
        elif word == "||||||":
            decoded_text += "!"
        else:
            decoded_text += word
    return decoded_text


bot = telebot.TeleBot("8023929064:AAHhOy6mWerP27wejCJsKWCLIbeq_RIDcGo") # Замените на свой токен

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я могу переводить между вашим Пан-алфавитом и русским языком.\nИспользуйте команды /PanToRus и /RusToPan.")

@bot.message_handler(commands=['PanToRus'])
def handle_pan_to_rus(message):
    bot.reply_to(message, "Введите текст на Пан-языке:")
    bot.register_next_step_handler(message, process_pan_to_rus)

def process_pan_to_rus(message):
    try:
        decoded_text = decode(message.text)
        bot.reply_to(message, f"Перевод на русский: {decoded_text}")
    except Exception as e:
        bot.reply_to(message, f"Ошибка перевода: {e}")


@bot.message_handler(commands=['RusToPan'])
def handle_rus_to_pan(message):
    bot.reply_to(message, "Введите текст на русском языке:")
    bot.register_next_step_handler(message, process_rus_to_pan)

def process_rus_to_pan(message):
    try:
        encoded_text = encode(message.text)
        bot.reply_to(message, f"Перевод на Пан-язык: {encoded_text}")
    except Exception as e:
        bot.reply_to(message, f"Ошибка перевода: {e}")


bot.polling()
