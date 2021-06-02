import ujson, ure, time, gc, urequests

class Bot():
    '''
    Base class for interacting with telegram api
    '''

    def __init__(self, token):
        self.url = 'https://api.telegram.org/bot' + token
        self.last_update = 0
        self.loop_sleep = 200
        self.message_handlers = {}
        self.command_handlers = {}

        self._get_updates()

    def change_loop_sleep(self, time_in_ms: int):
        self.loop_sleep = time_in_ms

    def _get_updates(self):
        '''
        Gets all the updates from the telegram api and stores
        latest id for next iteration
        '''
        parameters = {
            'offset': self.last_update + 1,
            'timeout': 10,
            'allowed_updates': ['messages']
            }

        try:
            response = urequests.post(self.url + '/getUpdates', json=parameters)
            data = response.json()
            response.close()

            if 'result' in data:
                self.last_update = data['result'][-1]['update_id'] #storing last update id
                return [Update(self, update) for update in data['result']]

            return None

        except:
            return  None

    def _handle_update(self, update):
        '''
        Function that chooses the right function to handle the update, 
        based on the previously defined handlers
        '''
        text = update.message['text']

        if text.startswith('/'): #is a command
            #get first word (useful for future implementation of commands with arguments)
            command = text.split(' ')[0].replace('/','')

            if command in set(self.command_handlers.keys()):
                self.command_handlers[command](update)
                return

        for expression in set(self.message_handlers.keys()):
            #handling messagges
            if ure.match(expression, text):
                self.message_handlers[expression](update)
                return

    def loop(self):
        '''
        main bot loop function
        '''

        while True:
            gc.collect() #in case automatic gc is disabled
            time.sleep_ms(self.loop_sleep)

            updates = self._get_updates()

            if updates:
                for update in updates:
                    self._handle_update(update)

    def add_message_handler(self, regular_expression):
        '''
        Decorator to add a message handler with regex validation
        '''

        def decorator(function):
            self.message_handlers[regular_expression] = function

        return decorator

    def add_command_handler(self, command):
        '''
        Decorator to add a command handler, (write command without '/' as argument)
        '''

        def decorator(function):
            self.command_handlers[command] = function

        return decorator

    def send_message(self, chat_id, text, parse_mode='MarkdownV2', reply_markup=None):

        parameters = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode
        }

        if reply_markup:
            parameters['reply_markup'] = reply_markup.data

        try:
            message = urequests.post(self.url + '/sendMessage', json=parameters)
            assert message
            message.close()

        except Exception:
            print('message not sent')

class ReplyKeyboardMarkup():
    '''
    class used to as custom reply_markup to send custom keyboards
    '''

    def __init__(self, keyboard, resize_keyboard=False, one_time_keyboard=False, selective=False):
        self.data = {
            'keyboard': [[k.data for k in row] for row in keyboard],
            'resize_keyboard': resize_keyboard,
            'one_time_keyboard': one_time_keyboard,
            'selective': selective
            }

class KeyboardButton():
    '''
    class used to create button objects used with ReplyKeyboardMarkup
    '''

    def __init__(self, text, request_contact=False, request_location=False):
        self.data = {
            'text': text,
            'request_contact': request_contact,
            'request_location': request_location
            }

class Update():
    '''
    class with basic methods for updates
    '''

    def __init__(self, b, update):
        self.update_id = update['update_id']
        self.message = update['message']
        self.bot = b

    def reply(self, text, parse_mode='MarkdownV2', reply_markup=None):
        self.bot.send_message(self.message['chat']['id'], text, parse_mode=parse_mode, reply_markup=reply_markup)
