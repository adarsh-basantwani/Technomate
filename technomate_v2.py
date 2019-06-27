import ctypes
import os
import random
import webbrowser
import pyautogui
import wolframalpha
import subprocess

import boto3
import speech_recognition as sr
from google import google
from playsound import playsound


import lookup_drive_change
import image
from run_lookup import RunLookup
import chatbot_train
from pygame import mixer

client = wolframalpha.Client('WTU5K4-TA8UV22E35')

speech = sr.Recognizer()

greeting_dict = {'hello':'hello','hi':'hi'}
open_launch_dict = {'open':'open','launch':'launch'}
social_media_dict = {'facebook':'https://www.facebook.com','twitter':'https://www.twitter.com','instagram':'https://www.instagram.com','google':'https://www.google.com','gmail':'https://www.gmail.com'}
google_searches_dict = {'what':'what','why':'why','who':'who','which':'which','how':'how','where':'where','when':'when'}


mp3_greeting_list = ['mp3/greeting.mp3']
open_launch_list = ['mp3/open_1.mp3']
listening_problem_list = ['mp3/listning_problem.mp3']
struggling_list = ['mp3/struggling.mp3']

error_occurence = 0
counter = 0

polly = boto3.client('polly')

def mouse():
    x_change = 0
    y_change = 0

    while True:
        d = pyautogui.position()
        i = list(d)
        print(i)
        k = read_voice_cmd()
        print(k)

        if k == 'down':
            y_change = 30
            x_change = 0
        elif k == 'up':
            y_change = -30
            x_change = 0
        elif k == 'right':
            x_change = 30
            y_change = 0
        else:
            x_change = -30
            y_change = 0

        i[0] += x_change
        i[1] += y_change

        pyautogui.moveTo(i[0], i[1], duration = 1)
        if 'click' or 'press' in k:
            pyautogui.click()
        elif 'deactivate' in k:
            break

def get_index(text):
    if 'first' in text:
        return 0
    elif 'second' in text:
        return 1
    elif 'third' in text:
        return 2
    elif 'fourth' in text:
        return 3
    elif 'fifth' in text:
        return 4
    elif 'sixth' in text:
        return 5
    else:
        return None

def play_sound_from_polly(result, is_google=False):
    global counter
    mp3_name = 'output{}.mp3'.format(counter)
    obj = polly.synthesize_speech(Text = result, OutputFormat = 'mp3', VoiceId = 'Joanna')
    if is_google:
        playsound('mp3/google_search.mp3')
    with open(mp3_name,'wb') as file:
        file.write(obj['AudioStream'].read())
        file.close()
    playsound(mp3_name)
    os.remove(mp3_name)
    counter += 1
    
def google_search_result(query):
    
    search_result = google.search(query)
    
    for result in search_result:
        print(result.description.replace('...','').rsplit('.',3)[0])
        if result.description!='':
            play_sound_from_polly(result.description.replace('...','').rsplit('.',3)[0], is_google=True)
            break
        
def is_valid_google_search(phrase):
    if (google_searches_dict.get(phrase.split(' ')[0]) == phrase.split(' ')[0]):
        return True

def play_sound(mp3_list):
    mp3 = random.choice(mp3_list)
    playsound(mp3)

def read_voice_cmd():
    voice_text = ''
    play_sound_from_polly('How do you want to give input. Press 1 for command or press 2 for voice')
    t = int(input('How do you want to give input \n 1. Command \n 2. Voice \n'))
    if t == 1:
        voice_text = str(input('cmd : '))
    else:
        print('Listening...')
        global error_occurence
    
        try:
            with sr.Microphone() as source:
                audio = speech.listen(source=source,timeout=10,phrase_time_limit=5)
            voice_text = speech.recognize_google(audio)
        except sr.UnknownValueError:
            if error_occurence == 0:
                play_sound(listening_problem_list)
                error_occurence += 1
            elif error_occurence == 1:
                play_sound(struggling_list)
                voice_text = str(input('cmd : '))
                error_occurence = 0
        except sr.RequestError as e:
            playsound('mp3/network_error.mp3')
        except sr.WaitTimeoutError:
            if error_occurence == 0:
                play_sound(listening_problem_list)
                error_occurence += 1
            elif error_occurence == 1:
                play_sound(struggling_list)
                error_occurence +=1
    return voice_text

def is_valid_note(greeting_dict,voice_note):
    for key, value in greeting_dict.items():
        #hello buddy
        try:
            if value == voice_note.split(' ')[0]:
                return True
                break
            elif key == voice_note.split(' ')[1]:
                return True
                break
        except:
            pass
    return False
def control_system(cmd):
    play_sound_from_polly('wait a moment sir')
    os.system(cmd)

def music(count):
    music_folder = 'songs/'
    music = []
    for file in os.listdir(music_folder):
        music.append(file)
    random_music = music_folder + random.choice(music)
    mixer.init()
    mixer.music.load(random_music)
    if count == 0:
        play_sound_from_polly('Okay, here is your music! Enjoy!')
        mixer.music.play()
    else:
        mixer.music.stop()
    
if __name__ == '__main__':

    playsound('mp3/hello.mp3')
    play_sound_from_polly('starting all system applications')
    play_sound_from_polly('installing all drivers')
    play_sound_from_polly('connecting to local servers')
    cmd = "C:\\Program Files\\Rainmeter\\Rainmeter.exe"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
    play_sound_from_polly('every driver is installed')
    play_sound_from_polly('all systems have been started')
    play_sound_from_polly('now i am online sir')
    while True:
        voice_note = read_voice_cmd().lower()
        print('cmd : {}'.format(voice_note))
    
        if is_valid_note(greeting_dict,voice_note):
            print('In greeting...')
            play_sound(mp3_greeting_list)
            continue
        elif is_valid_note(open_launch_dict,voice_note):
            print('In open...')
            play_sound(open_launch_list)
            if (is_valid_note(social_media_dict,voice_note)):
                key = voice_note.split(' ')[1]
                webbrowser.open(social_media_dict.get(key))
            else:
                key = voice_note.replace('open ', '').replace('launch ', '')
                print('Key is : ' + key)
                # print(list(lookup_drive_change.lookup_dict.keys()))

                opt_dict = {}
                for k in list(lookup_drive_change.lookup_dict.keys()):
                    if key in k.lower():
                        opt_dict.update({k: lookup_drive_change.lookup_dict.get(k)})

                print(opt_dict)
                if len(opt_dict) == 1:
                    for key in opt_dict.keys():
                        print('explorer {}'.format(opt_dict.get(key)))
                        os.system('explorer {}'.format(opt_dict.get(key)))
                elif len(opt_dict) > 1:
                    play_sound_from_polly('I have found multiple instances. Which one you want?',is_google=False)
                    default = 0
                    index = None
                    for i, k in enumerate(opt_dict.keys()):
                        print(k.split('.')[0].split('_')[0] + ' from {} folder'.format(opt_dict.get(k).split('\\')[-2]))
                        play_sound_from_polly(
                            k.split('.')[0].split('_')[0] + ' from {} folder '.format(opt_dict.get(k).split('\\')[-2]),is_google=False)

                        default = i

                    text = read_voice_cmd().lower()
                    print(text)
                    index = get_index(text)

                    if index != None:
                        print('explorer {}"'.format(
                            lookup_drive_change.lookup_dict.get(list(opt_dict.keys())[index])) + ' ' + str(index))
                        play_sound_from_polly('Ok Sir', False)
                        os.system(
                            'explorer {}"'.format(lookup_drive_change.lookup_dict.get(list(opt_dict.keys())[index])))

            continue
        elif is_valid_google_search(voice_note):
            print("In google search...")
            playsound('mp3/search.mp3')
            #webbrowser.open("https://www.google.com/search?q={}".format(voice_note))
            google_search_result(voice_note)
            continue
        elif 'lock' in voice_note:
            for value in ['pc','system','windows']:
                ctypes.windll.user32.LockWorkStation()
            play_sound_from_polly('Your system is locked.')   
        elif 'thank you' in voice_note:
            playsound('mp3/thank_you.mp3')
            continue
        elif 'activate' in voice_note:
            play_sound_from_polly('Sure sir.')
            mouse()
        elif 'chat' in voice_note:
            play_sound_from_polly('Sure sir.')
            chatbot_train.chat()
        elif 'search' in voice_note:
            query = voice_note.split(' ',1)[1]
            play_sound_from_polly('Wait a moment sir. I am searching.')
            res = client.query(query)
            play_sound_from_polly('Result Found Sir.')
            answer = next(res.results).text
            print(answer)
            play_sound_from_polly(answer)
            continue
        elif 'login to facebook' in voice_note:
            play_sound_from_polly('Logging you to facebook sir by userid and password you had given')
            cmd = "scripts/facebook_login.exe"
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
            process.wait()
            continue
        elif 'logout from facebook' in voice_note:
            play_sound_from_polly('Log out from facebook sir.')
            cmd = "scripts/facebook_logout.exe"
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
            process.wait()
            continue
        elif 'close window' in voice_note:
            play_sound_from_polly('Closing Window')
            cmd = "scripts/close_window.exe"
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
            process.wait()
            continue
        elif 'minimize window' in voice_note:
            play_sound_from_polly('Minimizing window')
            cmd = "scripts/minimize_window.exe"
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
            process.wait()
            continue
        elif 'convert image to text' == voice_note:
            play_sound_from_polly('Enter image path sir')
            print(image.img())
            continue
        elif 'accessibility options' in voice_note:
            control_system('control access.cpl')
            continue
        elif 'add new hardware' in voice_note:
            control_system('control sysdm.cpl add new hardware')
            continue
        elif 'add or remove programs' in voice_note:
            control_system('control appwiz.cpl')
            continue
        elif 'time or date settings' in voice_note:
            control_system('control timedate.cpl')
            continue
        elif 'display settings' in voice_note:
            control_system('control desk.cpl')
            continue
        elif 'check fonts' in voice_note:
            control_system('control fonts')
            continue
        elif 'internet properties' in voice_note:
            control_system('control inetcpl.cpl')
            continue
        elif 'keyboard properties' in voice_note:
            control_system('control main.cpl keyboard')
            continue
        elif 'modem properties' in voice_note:
            control_system('control modem.cpl')
            continue
        elif 'mouse properties' in voice_note:
            control_system('control main.cpl')
            continue
        elif 'multimedia properties' in voice_note:
            control_system('control mmsys.cpl')
            continue
        elif 'power management' in voice_note:
            control_system('control powercfg.cpl')
            continue
        elif 'printers properties' in voice_note:
            control_system('control printers')
            continue
        elif 'regional settings' in voice_note:
            control_system('control intl.cpl')
            continue
        elif 'scanners and cammeras' in voice_note:
            control_system('control sticpl.cpl')
            continue
        elif 'sound properties' in voice_note:
            control_system('control mmsys.cpl sounds')
            continue
        elif 'system properties' in voice_note:
            control_system('control sysdm.cpl')
            continue
        elif 'goodbye' in voice_note:
            playsound('mp3/bye.mp3')
            quit()
        elif 'stop song' == voice_note:
            music(1)
            continue
        elif 'play music' == voice_note or 'next music' == voice_note:
            music(0)
            continue
        else:
            if voice_note != '':
                play_sound_from_polly('command not found.')
