import telebot
from config import keys, TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для начала работы введите команду боту в следующем виде: \n<имя валюты> \ <имя валюты, в которой надо узнать цену первой валюты> \ <количество первой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)
api = '56e225afe1ea84310b5a9d635192f23b'
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text,key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types= ['text', ])
def convert(message:telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Лишние параметры или не хватет определённых параметров')

        quote, base, amount = values
        total_base = Converter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} на данный момент равна: {total_base}'
        bot.send_message(message.chat.id, text)
bot.polling()