#REMEMBER TO RENAME FILE TO main.py BEFORE UPLOAING TO THE BOARD

#THIS SIMPLE EXAMPLE IS USED TO TURN AN LED CONNECTED TO PIN 2 ON AND OFF USING A CUSTOM KEYBOARDAD,
#IT IS ALSO POSSIBLE TO KNOW THE CURRENT STATE OF THE PIN
from utelegram import Bot, Conversation, ReplyKeyboardMarkup, KeyboardButton
from machine import Pin

TOKEN = 'TokenGoesHere'

bot = Bot(TOKEN)
led = Pin(2, Pin.OUT)
c = Conversation(['NAME', 'AGE']) #2-step conversation

@c.add_command_handler('ENTRY', 'start')
def start(update):
	update.reply('What\'s your name?')
	return 'NAME'
	
@c.add_message_handler('NAME', '(.*?)') #every message
def nome(update):
	update.reply('Hi {}, how old are you?'.format(update.message['text']))
	return 'AGE'
	
@c.add_command_handler('AGE', 'value') #used to demonstrate priority of conversation over global handler
def fake_value(update):
	update.reply('you cannot get the value right now, please tell me your age')
	return 'AGE'
	
@c.add_message_handler('AGE', '^[0-9]*$') #only numbers
def eta(update):
	if int(update.message['text']) > 17:
		update.reply('You are verified')
		led.on()
		return c.END
	else: 
		update.reply('access denied, try again...')
		led.off()
		return 'AGE'

@bot.add_command_handler('value')
def value(update):
    if led.value():
        update.reply('LED is on')
    else:
        update.reply('LED is off')
        
bot.add_conversation_handler(c)
bot.start_loop()
