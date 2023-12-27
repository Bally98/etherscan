import telebot
import psycopg2

TOKEN = '6757466398:AAFoGdqNogxG9nKjG8xivdTgT661Kgc90Wg'
DATABASE_URL = 'postgresql://user:password@localhost:5432/db_name'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, 'Hi')

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text

    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO messages (user_id, chat_id, text) VALUES (%s, %s, %s)",
                       (user_id, chat_id, text))
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    with bot.get_updates():
        pass

    bot.polling()
