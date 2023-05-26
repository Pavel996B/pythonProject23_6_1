import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    text = 'Для начала работы через пробел введите: \n <имя валюты, цену которой хотите узнать> ' \
           '\n <имя валюты, в которой надо узнать цену первой валюты>' \
           '\n <количество первой валюты> ' \
           '\n \n Чтобы вызвать список доступных валют, воспользуйтесь командой /values.'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values_list(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Параметров больше или меньше, чем нужно. Используйте формат:\n<название валюты> \
    <название валюты, в которую нужно перевести> \
    <количество переводимой валюты>')

        base, quote, amount = values
        total_base = CurrencyConverter.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'{amount} {base} = {total_base} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling()