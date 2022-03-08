import ujson, ure, time, gc, urequests, _thread
from machine import Timer


class Bot():
    '''
    Base class for interacting with telegram api
    '''

    def __init__(self, token):
        self.url = 'https://api.telegram.org/bot' + token
        self.last_update = 0
        self.command_handlers = {}
        self.callback_handlers = {}
        self.message_handlers = {}
        self.conversation_handlers = []

        self._get_updates()

    def _get_updates(self):
        '''
        Gets all the updates from the telegram api and stores
        latest id for next iteration
        '''
        parameters = {
            'offset': self.last_update + 1,
            'timeout': 2,
            'allowed_updates': ['messages']
            }

        try:
            response = urequests.post(self.url + '/getUpdates', json=parameters)
            data = response.json()
            response.close()
            
            if data['result']:
                self.last_update = data['result'][-1]['update_id'] #storing last update id
                return [Update(self, update) for update in data['result']]

            return None

        except Exception as e:
            print('_get_updates: ',e)
            return  None

    def _handle_update(self, update):
        '''
        Function that chooses the right function to handle the update, 
        based on the previously defined handlers
        '''
        text = update.message['text']

        if update.is_callback:
            self.callback_handlers[update.callback_data](update)



        if text.startswith('/'): #is a command
            #get first word (useful for future implementation of commands with arguments)
            command = text.split(' ')[0].replace('/','')
            
            for c in self.conversation_handlers:
            	if command in c.steps[c.active][0].keys():
            		next_step = c.steps[c.active][0][command](update)
            		c.go_to_step(next_step)
            		return

            if command in set(self.command_handlers.keys()):
                self.command_handlers[command](update)
                return
        else:
                
            for c in self.conversation_handlers:
                    for expression in c.steps[c.active][1].keys():
                        if ure.match(expression, text):
                            next_step = c.steps[c.active][1][expression](update)
                            c.go_to_step(next_step)
                            return
                            
            for expression in set(self.message_handlers.keys()):
                #handling messagges
                if ure.match(expression, text):
                    self.message_handlers[expression](update)
                    return

    def _read(self):
        '''
        main bot read function
        '''
        updates = self._get_updates()
        
        if updates:
            for update in updates:
                self._handle_update(update)
                
        gc.collect() #in case automatic gc is disabled
        return
        
    def _loop(self, period=100):
        while True:
    	    self._read()
        
    def start_loop(self, main_function=None, args=(), period=100):
    	"""
    	main function used to start the bot in a different thread.
    	"""
    	if main_function:
    		_thread.start_new_thread(main_function, args)
    		
    	_thread.start_new_thread(self._loop(), (period,))
    	

    def add_message_handler(self, regular_expression):
        '''
        Decorator to add a message handler with regex validation
        '''

        def decorator(function):
            self.message_handlers[regular_expression] = function

        return decorator

    def add_callback_handler(self, callback_data):
        '''
        Decorator to add a callback handler 
        '''

        def decorator(function):
            self.callback_handlers[callback_data] = function

        return decorator

    def add_command_handler(self, command):
        '''
        Decorator to add a command handler, (write command without '/' as argument)
        '''

        def decorator(function):
            self.command_handlers[command] = function

        return decorator
        
    def add_conversation_handler(self, conversation):
        '''
        Decorator to add a conversation handler
        '''
        
        self.conversation_handlers.append(conversation)


    def send_message(self, chat_id, text, parse_mode='MarkdownV2', reply_markup=None):

        parameters = {
            'chat_id': chat_id,
            'text': text.replace('.', '\.'),
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


    def update_message(self, chat_id, message_id, text, parse_mode='MarkdownV2', reply_markup=None):

        parameters = {
            'chat_id': chat_id,
            'message_id' : message_id,
            'text': text,
            'parse_mode': parse_mode,
            
        }

        if reply_markup:
            parameters['reply_markup'] = reply_markup.data

        try:
            message = urequests.post(self.url + '/editMessageText', json=parameters)
            print(message.text)
            assert message
            message.close()

        except Exception:
            print('update not sent')
            
            
class Conversation():
	"""
	Conversation class used for conversations with multiple steps
	
	STEPS MUST BE DEFINED AT INITIALIZATION, EACH STEP CAN HAVE MULTIPLE HANDLERS
	
	ENTRY STEP IS ADDED BY DEFAULT AND IS USED TO START THE CONVERSATION
	
	every function used as a handler should return the next conversation step
	"""
	
	def __init__(self, steps: list = []):
		self.END = 0
		self.steps = {
			'ENTRY': [{},{}]
		}
		self.active = 'ENTRY'
		
		for step in steps:
			self.steps[step] = [{},{}]
			
	def add_command_handler(self, step, command):
		'''
		Decorator to add a command handler to a specific step,
		(write command without '/' as argument)
		'''

		def decorator(function):
		    self.steps[step][0][command] = function

        	return decorator
        	
        def add_message_handler(self, step, regular_expression):
		'''
		Decorator to add a message handler to a specific step,
		with regex validation
		'''

		def decorator(function):
		    self.steps[step][1][regular_expression] = function

		return decorator
		
	def go_to_step(self, step):
		if step == 0:
			self.active = 'ENTRY'
		elif step in self.steps.keys():
			self.active = step
		else:
			print('[ERROR] No step named {s} defined, staying at current step'.format(step))
			
	def end(self):
		self.active = 'ENTRY'


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

class InlineKeyboardMarkup():
    '''
    class used to as custom reply_markup to send custom keyboards
    '''

    def __init__(self, keyboard):
        self.data = {
            'inline_keyboard': [[k.data for k in row] for row in keyboard]
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

class InlineKeyboardButton():
    '''
    class used to create button objects used with ReplyKeyboardMarkup
    '''

    def __init__(self, text,url="",callback_data = ""):
        self.data = {
            'text': text,
            'url': url,
            'callback_data' : callback_data
            }


class Update():
    '''
    class with basic methods for updates
    '''

    def __init__(self, b, update):
        self.update_id = update['update_id']
        self.bot = b
        self.is_callback = False
        self.callback_data = ""
        try:
            if update['callback_query']:
                    print("IS A CALLBACK")
                    self.is_callback = True
                    self.message = update['callback_query']['message']
                    self.callback_data = update['callback_query']['data']


        except KeyError as e:
            print("Not a Callback")
            self.message = update['message']
            
            

    def reply(self, text, parse_mode='MarkdownV2', reply_markup=None):
        self.bot.send_message(self.message['chat']['id'], text, parse_mode=parse_mode, reply_markup=reply_markup)

    def edit(self,text, parse_mode='MarkdownV2', reply_markup=None):
        self.bot.update_message(self.message['chat']['id'] , self.message['message_id'], text, parse_mode= parse_mode , reply_markup= reply_markup)
