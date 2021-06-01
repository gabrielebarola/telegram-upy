# Telegram-uPy
Telegram API wrapper for micropython, built for ESP32, cannot verify support for other MCUs

---
# INSTALLING
Clone the repository:

```
git clone https://github.com/gabrielebarola/telegram-upy.git
```

upload the **utelegram.py** file to your board using your favourite software (i use ampy):

```
ampy -b 115200 -p /dev/ttyUSB0 put path/to/utelegram.py
```

If you don't have it install urequests via upip using repl:

```
import upip 
upip.install('urequests')
```

---
# USAGE
## Creating the bot
```
from utelegram import Bot

TOKEN = 'your-bot-token-12345'

bot = Bot(TOKEN)
```

Bot token is provided by **BotFather** when creating a new bot on the telegram client

## Adding command handlers
You can create functions that are triggered when a **command** (message starting with '/') is sent to the bot.


For example let's write a function that replies "hello" when **/start** is sent to the bot

```
@bot.add_command_handler('start')
def start(update):
    update.reply('hello')
```

**Every function used as a handler should take the update as an argument**

## Adding message handlers
You can also create functions triggered when a message that matches a **regular expression** is sent to the bot.

If you need a regex cheat sheet you can find it here https://www.w3schools.com/python/python_regex.asp

For example let's write a function that replies "hello" when a message starting with **"Hi"** is sent is sent to the bot

```
@bot.add_message_handler('^Hi')
def start(update):
    update.reply('hello')
```

**The regular expression must be given to the decorator as argument**