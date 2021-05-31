import ujson, urequests, ure, time
from config import TOKEN

class Bot():
    '''
    Base class for interacting with telegram api
    '''

    def __init__(self, token):
        self.url = 'https://api.telegram.org/bot' + token
        self.last_update = 0
        self.message_handlers = {}

        self._get_updates()

    def _get_updates(self):
        '''
        Gets all the updates from the telegram api and stores
        lates id for next iteration
        '''
        parameters = {
            'offset': self.last_update + 1,
            'timeout': 10,
            'allowed_updates': ['messages']
            }

        try:
            response = urequests.post(self.url + '/getUpdates', json=parameters).json()

            if 'result' in response:
                self.last_update = response['result'][-1]['update_id']
                return [update for update in response['result']]

            return None

        except:
            return  None

    def _handle_update(self, update):
        for key in list(self.message_handlers.keys()):
            if ure.match(key, update['message']['text']):
                self.message_handlers[key](update)
                return


    def loop(self):
        '''
        main bot loop function
        '''
        time.sleep(0.5)
        while True:
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

if __name__ == '__main__':
    b = Bot(TOKEN)

    @b.add_message_handler('^ciao$')
    def ciao(update):
        print(update)

    b.loop()
