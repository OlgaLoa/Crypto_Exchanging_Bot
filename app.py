import telebot  # Импортируем библиотеку telebot, которая позволяет взаимодействовать с Telegram API.
from config import keys, TOKEN  # Импортируем словарь ключей и токен бота из файла config.py.
from extensions import APIException, CryptoConverter  # Импортируем классы APIException и CryptoConverter из файла extensions.py.

bot = telebot.TeleBot(TOKEN)

# обработчик help и start
@bot.message_handler(commands = ["start", "help"])
def help (message:telebot.types.Message):
    text = "Чтобы начать работу введите команду боту в следующем формате:\n <имя валюты>\
<в какую валюту нужно перевести> <количество переводимой валюты>\
\n Увидеть список всех доступных валют: /values"
    bot.reply_to(message, text)


# обработчик values
@bot.message_handler(commands = ["values"])
def values (message:telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key, ))#каждая нов. валюта б переноситься на строчку вниз
    bot.reply_to(message, text)

@bot.message_handler(content_types = ["text", ])#по типу обращения
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise APIException("введено неправильное количество параметров")

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя: \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду {e}')
    else:
        bot.send_message(message.chat.id, total_base)  # возвращает ТОЛЬКО СУММУ в валюте(как написано в задании)

bot.polling()
