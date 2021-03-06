# Telegram-uPy
Telegram API wrapper for micropython, built for ESP32, cannot verify support for other MCUs

---
# INSTALLING
Clone the repository:

```bash
git clone https://github.com/gabrielebarola/telegram-upy.git
```

upload the **utelegram.py** file to your board using your favourite software (i use ampy):

```bash
ampy -b 115200 -p /dev/ttyUSB0 put path/to/utelegram.py
```

Install urequests library using upip in repl

```python
import upip

upip.install('urequests')
```

---
# USAGE
You can find simple examples in the **examples** folder.
## Creating the bot
```python
from utelegram import Bot

TOKEN = 'your-bot-token-12345'

bot = Bot(TOKEN)
```

Bot token is provided by **BotFather** when creating a new bot on the telegram client

## Adding command handlers
You can create functions that are triggered when a **command** (message starting with '/') is sent to the bot.


For example let's write a function that replies "hello" when **/start** is sent to the bot

```python
@bot.add_command_handler('start')
def start(update):
    update.reply('hello')
```

**Every function used as a handler should take the update as an argument**

## Adding message handlers
You can also create functions triggered when a message that matches a **regular expression** is sent to the bot.

If you need a regex cheat sheet you can find it here https://www.w3schools.com/python/python_regex.asp

For example let's write a function that replies "hello" when a message starting with **"Hi"** is sent is sent to the bot

```python
@bot.add_message_handler('^Hi')
def hello(update):
    update.reply('hello')
```

**The regular expression must be given to the decorator as argument**

## Using custom keyboards
You can define custom keyboards to send with a reply
```python
from utelegram import ReplyKeyboardMarkup, KeyboardButton

keyboard = [
    [KeyboardButton('Btn1')], #each list is a row, each element is a column
    [KeyboardButton('Btn2'), KeyboardButton('Btn3')],
]

reply_keyboard = ReplyMarkupKeyboard(keyboard) #pass your array as the keyboard

@bot.add_message_handler('^Show keyboard')
def show(update):
    update.reply('here it is!', reply_markup=reply_keyboard)
```

## Using conversations
A conversation is a multi-step handler with subhandlers.
To create a conversation:

```python
from utelegram import Conversation

c = Conversation(['STEP1','STEP2']) #ENTRY STEP IS DEFAULT
```

Handlers can be added similarly to the bot ones:
```python
@c.add_command_handler('ENTRY', '/started')
def do(update):
    update.reply('moving to step 1')
    return 'STEP1'

@c.add_command_handler('STEP1', '/dosomething')
def do(update):
    update.reply('did it!')
    return 'STEP2'

@c.add_message_handler('STEP2', '^end$')
def end(update):
    update.reply('ending')
    return c.END
```

**An handler must always return the next step you want to take in the conversation, use c.END to end the conversation**

Add the conversation to the bot:

```python
bot.add_conversation_handler(c)
```

## Starting the bot loop

```python
bot.start_loop()
```

if you want to use another function in parallel with the bot do it this way:

```python
def main(text):
    while True:
        print(text)
	
bot.start_loop(main, (text,))
```

if your function has arguments pass them as a touple


# Donating
If you appreciate my work and want to donate, you can do it with PayPal at https://www.paypal.me/gabrielebarola
