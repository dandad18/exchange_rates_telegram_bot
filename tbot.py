import telebot
from telebot import types
from get_currency_info import get_exchange_rates_info, CurrencyInfo
from exceptions import ConnectionErrorException

def telegram_bot(TOKEN: str) -> None:
    # Creating a bot
    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(content_types=['text'])
    def start(message):
        if message.text == '/start':
            bot.send_message(message.chat.id, text="Hello, I'm Exchange rates Bot! Write '/help' to get commands list.")
        elif message.text.lower() == '/get_exchange_rates':
            # KeyBoard
            keyboard = types.InlineKeyboardMarkup()
            key_USD = types.InlineKeyboardButton(text='USD', callback_data='USD')
            keyboard.add(key_USD)
            key_EUR = types.InlineKeyboardButton(text='EUR', callback_data='EUR')
            keyboard.add(key_EUR)
            key_RUB = types.InlineKeyboardButton(text='RUB', callback_data='RUB')
            keyboard.add(key_RUB)

            # Question
            question = "Choose currency and I will give you some information about it. If you need to help, " \
                       "write '/help'."

            # Asking
            bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
        elif message.text.lower() == '/get_best_bank_to_buy_currency':
            bot.send_message(message.chat.id, text='This function is under development :(')
        elif message.text.lower() == '/get_best_bank_to_sell_currency':
            bot.send_message(message.chat.id, text='This function is under development :(')
        elif message.text.lower() == '/help':
            bot.send_message(message.chat.id, text="You can choose several commands:\n"
                                                   "1. /get_exchange_rates\n2. /get_best_bank_to_buy_currency\n"
                                                   "3. /get_best_bank_to_sell_currency")
        else:
            bot.send_message(message.from_user.id, 'Write "/start" to begin :)')

    @bot.callback_query_handler(func=lambda call: True)
    def give_callback(call):
        main_text = 'Information about chosen currency:\n'
        if call.data == 'USD':
            try:
                USD_info = get_exchange_rates_info(currency='USD')
            except ConnectionErrorException as error:
                bot.send_message(call.message.chat.id, text=error.message)
            else:
                info = main_text + f'Name: {USD_info.name}\nSale: {USD_info.sale} BYN\nBuy: {USD_info.buy} BYN\n' \
                                   f'Nat.Bank: {USD_info.national_bank} BYN'
                bot.send_message(call.message.chat.id, text=info)
        elif call.data == 'EUR':
            try:
                EUR_info = get_exchange_rates_info(currency='EUR')
            except ConnectionErrorException as error:
                bot.send_message(call.message.chat.id, text=error.message)
            else:
                info = main_text + f'Name: {EUR_info.name}\nSale: {EUR_info.sale} BYN\nBuy: {EUR_info.buy} BYN\n' \
                                   f'Nat.Bank: {EUR_info.national_bank} BYN'
                bot.send_message(call.message.chat.id, text=info)
        elif call.data == 'RUB':
            try:
                RUB_info = get_exchange_rates_info(currency='RUB')
            except ConnectionErrorException as error:
                bot.send_message(call.message.chat.id, text=error.message)
            else:
                info = main_text + f'Name: {RUB_info.name}\nSale: {RUB_info.sale} BYN\nBuy: {RUB_info.buy} BYN\n' \
                                   f'Nat.Bank: {RUB_info.national_bank} BYN'
                bot.send_message(call.message.chat.id, text=info)

    bot.polling(non_stop=True, interval=0)
