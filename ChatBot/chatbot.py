from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

def chat():
    bot = ChatBot('Bot')
    #bot.set_trainer(ListTrainer)
    trainer = ListTrainer(bot)
    while True:
        message = input('You :')
        if message.strip() != 'Bye':
            reply = bot.get_response(message)
            print('Technomate :',reply)
        if message.strip() == 'Bye':
            print('Technomate : Bye. Have a great day.')
            break
chat()
