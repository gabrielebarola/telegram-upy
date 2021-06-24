#REMEMBER TO RENAME FILE TO main.py BEFORE UPLOAING TO THE BOARD

#THIS SIMPLE EXAMPLE IS USED TO TURN AN LED CONNECTED TO PIN 2 ON AND OFF BY SENDING MESSAGGES TO THE BOT,
#IT IS ALSO POSSIBLE TO KNOW THE CURRENT STATE OF THE PIN
from utelegram import Bot
from machine import Pin

TOKEN = 'YourTokenGoesHere'

bot = Bot(TOKEN)
led = Pin(2, Pin.OUT)

@bot.add_command_handler('help')
def help(update):
    update.reply('Write on to power the led on \nWrite off to power the led off \nWrite /value to retrieve the current status of the led')

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

bot.start_loop()
