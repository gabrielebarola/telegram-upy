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

## Starting the bot loop

```python
bot.loop()
```

Default delay between executions is 200mS, you can change it with:

```python
bot.change_loop_sleep(time_in_ms)
```
