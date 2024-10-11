import telebot
from secret import API_KEY  # Make sure your API_KEY is set correctly in secret.py
from context import *


bot = telebot.TeleBot(API_KEY)



score = 0
current_question_id = 0

@bot.message_handler(commands=['start'])
def start_quiz(message):
    global score, current_question_id
    score = 0
    current_question_id = 0
    bot.send_message(message.chat.id, "Salom ba shumo muvafaqiyat!")
    ask_question(message.chat.id)

def ask_question(chat_id):
    global current_question_id
    if current_question_id < len(questions):
        question = questions[current_question_id]["qn"]
        bot.send_message(chat_id, question)
        bot.register_next_step_handler_by_chat_id(chat_id, check_answer)
    else:
        global score
        bot.send_message(chat_id, f"Quiz finished! Your score is: {score}")
        current_question_id = 0
        score = 0

def check_answer(message):
    global current_question_id, score
    correct_answer = questions[current_question_id]["ans"]
    if message.text.strip().lower() == correct_answer.lower():
        score += 1
        bot.send_message(message.chat.id, "Correct!")
    else:
        bot.send_message(message.chat.id, f"Wrong! The correct answer was: {correct_answer}")
    
    current_question_id += 1
    ask_question(message.chat.id)

bot.polling()
