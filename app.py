import telebot
from extensions import ConvertionException, ConvertValues
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_message(message: telebot.types.Message):
    text = 'Чтобы начать работу с ботом, введите команду боту в следующем формате:\n<Валюта, которую надо перевести> <В какую валюту перевести> <Количество>\n \
Посмотреть доступные валюты: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def available_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Неверно заполнена форма')
        quote, base, amount = values
        total_base = ConvertValues.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка с серверной части\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {float(total_base) * int(amount)}'
        bot.send_message(message.chat.id, text)

bot.polling()
