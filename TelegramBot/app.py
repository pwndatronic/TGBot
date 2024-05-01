import telebot
from extensions import ConvertionException, CurrencyConverter
from config import TOKEN, keys


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = ('Для начала работы введите боту команду в следующем формате: \n<Имя валюты>\
<В какую валюту перевести><Количество переводимой валюты>\n\nДля просмотра всех \
доступных валют введите команду: /values.')
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key.capitalize()))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        vals = message.text.split(' ')
        if len(vals) != 3:
            raise ConvertionException('Неверное количество параметров.')

        quote, base, amount = vals
        quote = quote.lower()
        base = base.lower()
        total_base = CurrencyConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользовательского ввода.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        # text = f'{amount} {keys[quote]} = {round(total_base, 2)} {keys[base]}'
        text = f'{amount} {quote} = {round(total_base, 2)} {base}.'
        bot.reply_to(message, text)


bot.polling(none_stop=True)
