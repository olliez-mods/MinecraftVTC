#========================
# Voice model was provided for free by alphacephei
# https://alphacephei.com/vosk/models
#========================

# IMPORTANT:
# RUN AS ADMIN TO ALLOW BLOCKING THE KEYBOARD

from vosk import Model, KaldiRecognizer
import pyaudio
import time
from pynput.keyboard import Key, Controller
from ctypes import windll

# if you want to add more commands, add them first here (or remove them if you don't like them)
commands = ["say", "shout", "party", "chat"]

keyboardController = Controller()


print(" -> Loading Model <-")
model = Model("vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15")
print(" -> Model Loaded <-")

def block_keys():
    windll.user32.BlockInput(True)
    # make sure these keys arnt pressed
    keyboardController.release(Key.ctrl_l)
    keyboardController.release(Key.ctrl_r)
    keyboardController.release(Key.shift_l)
    keyboardController.release(Key.shift_r)


def unblock_keys():
    windll.user32.BlockInput(False)

def sendcommand(command, text):
    block_keys() # blocka arows keys and control key
    keyboardController.tap("t")
    time.sleep(0.25)
    keyboardController.type(command + text_to_type)
    time.sleep(0.1)
    keyboardController.tap(Key.enter)
    unblock_keys()

recognizer = KaldiRecognizer(model, 16000)

frames_per_buff = 8192

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1 ,rate=16000, input=True, frames_per_buffer=frames_per_buff)
stream.start_stream()

print(" -> Start Loop <-")
while(True):
    data = stream.read(int(frames_per_buff/2))
    if (recognizer.AcceptWaveform(data)):
        raw_text = recognizer.Result()
        text = raw_text[14:-3]
        text = text.replace("ink", "inc")
        text = text.replace("smiley face", ":D")
        text = text.replace("frowny face", ":(")
        text = text.replace("angry face", ">:(")
        text = text.replace("got them", "gotem")
        text = text.replace("easy easy", "ez")
        text = text.replace("read", "red")
        text = text.replace(" xd", " XD ")
        text_by_word = text.split(" ")

        try:
            is_commnd = False
            command = ""

            # check if the first or second work is a command
            if(text_by_word[0] in commands):
                is_commnd = True
                command = text_by_word[0]
                del text_by_word[0]
            
            # if the sentence includes cancel we wont send anything
            if(is_commnd):
                text_to_type = " ".join(text_by_word)
                if command == "say":
                    print("Saying:", text_to_type)
                    sendcommand("", text_to_type)
                elif command == "shout":
                    print("Shouting:", text_to_type)
                    sendcommand("/shout", text_to_type)
                elif command == "party":
                    print("Party Chat:", text_to_type)
                    sendcommand("/pc", text_to_type)
                elif command == "chat":
                    print("All Chat:", text_to_type)
                    sendcommand("/ac", text_to_type)
                    

        # we expect index errors it's ok
        except IndexError as e:
            pass
        except Exception as e:
            print(e)

