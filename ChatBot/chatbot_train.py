from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

def chat():
    bot=ChatBot('Bot')
    #bot.set_trainer(ListTrainer)
    trainer = ListTrainer(bot)
    print('Wait..I am in training mode')
    for files in os.listdir('C:/Users/Adarsh Basantwani\Downloads/chatterbot-corpus-master/chatterbot_corpus/data/english/'):
                            data = open('C:/Users/Adarsh Basantwani\Downloads/chatterbot-corpus-master/chatterbot_corpus/data/english/' + files ,'r').readlines()
                            trainer.train(data)
    print('Training Completed..Now we can chat.')
    while True:
                message = input('You :')
                if message.strip() != 'Bye':         
                     reply = bot.get_response(message)
                     print('Technomate :',reply)
                if message.strip() == 'Bye':
                     print('Technomate : Bye. Have a great day.')
                     break



