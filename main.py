from openai import OpenAI
import sqlite3

class StatelessDetector:
    def __init__(self, history_storage):
        self.client = OpenAI(api_key='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')
        self.history_storage = history_storage
    def evaluate_message(self, user, message):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user",
                       "content": f'Message: [{message}] condition under which a response is required: '
                                  f'[the message must be related to the AigentX project or the AIX cryptocurrency] '
                                  f'conditions under which the response must be "False": [any message unrelated to '
                                  f'the AigentX project or the AIX cryptocurrency]'
                                 f'Strictly adhere to these conditions. For the first condition, respond clearly to'
                                  f' the message and offer assistance with other questions. For the second condition'
                                  f' simply respond "False"'
                                  f'The next data object [{self.history_storage.get_all_info()}] is the '
                                  f'latest messages; just analyze them for a deeper understanding of the context, do not return them'}],
            max_tokens=50)
        self.history_storage.add_message(user, message)
        return response.choices[0].message.content


class ConversationHistoryStorage:
    def __init__(self, db_path='chat_history.db'):
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            message TEXT
            )''')

    def add_message(self, user, message):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO chat_history (user, message) VALUES (?, ?)''', (user, message))

    def get_all_info(self):
        with sqlite3.connect('chat_history.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT user, message FROM chat_history ORDER BY id DESC LIMIT 3')
            data = ''
            info = cursor.fetchall()
            for el in info:
                data += f'User: "{el[0]}" Message: "{el[1]}" \n'
            return data
