#REMEMBER TO RENAME FILE TO main.py BEFORE UPLOAING TO THE BOARD

#THIS SIMPLE EXAMPLE IS USED TO TURN AN LED CONNECTED TO PIN 2 ON AND OFF USING A CUSTOM KEYBOARDAD,
#IT IS ALSO POSSIBLE TO KNOW THE CURRENT STATE OF THE PIN
from utelegram import Bot, ReplyKeyboardMarkup, KeyboardButton
from machine import Pin

TOKEN = 'YourTokenGoesHere'

bot = Bot(TOKEN)
led = Pin(2, Pin.OUT)

#KEYBOARD DEFINED AS ARRAY OF ARRAYS OF KEYBOARDBUTTONS
keyboard = [
        [KeyboardButton('ON'), KeyboardButton('OFF')],
        [KeyboardButton('Toggle')]
        ]
replyKeyboard = ReplyKeyboardMarkup(keyboard)

@bot.add_command_handler('help')
def help(update):
    print('entered')
    update.reply('Write /start to get a custom keyboard or /value to get the current led status')

@bot.add_command_handler('start')
def start(update):
    update.reply('Led control keyboard enabled', reply_markup=replyKeyboard)

@bot.add_command_handler('value')
def value(update):
    if led.value():
        update.reply('LED is on')
    else:
        update.reply('LED is off')

@bot.add_message_handler('^on|On|ON$')
def on(update):
    led.on()

@bot.add_message_handler('^off|Off|OFF$')
def off(update):
    led.off()

@bot.add_message_handler('^Toggle|TOGGLE|toggle$')
def toggle(update):
    old_status = bool(led.value())
    led.value(not old_status)

bot.loop()
