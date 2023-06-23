import telebot
import pandas as pd
import requests
import pandas as pd
from langdetect import detect
from transformers import T5ForConditionalGeneration, T5Tokenizer


# Создание экземпляра бота
bot = telebot.TeleBot('6219046220:AAGXfz7CMkGmRSUdVddMbUY9R8T68jOrd2U')

# Счетчик правильных переводов
score = 0

# Словарь с английскими словами и их русскими переводами
dictionary = {
    'cat': 'кот',
    'dog': 'собака',
    'house': 'дом',
    # Добавьте здесь больше слов и переводов
}


# Загрузка модели машинного перевода T5
model = T5ForConditionalGeneration.from_pretrained('t5-base')
tokenizer = T5Tokenizer.from_pretrained('t5-base')


# Choosing the commands
@bot.message_handler(commands=['start'])

def start(message):
    bot.send_message(message.chat.id, "Привет! Это бот для обучения английскому языку, пиши '/translate', если нужно что-то перевести. "
                                      "Для запуска игры-тренировки, пиши /train. Для остановки и вывода счета, пиши '/stop'.")
# Команда /train начинает обучение
@bot.message_handler(commands=['train'])
def train(message):
    global score
    score = 0
    bot.send_message(message.chat.id, "Давайте начнем обучение! Я буду говорить английские слова, а вы должны будете перевести их на русский. Если вы хотите остановить обучение, введите /stop.")
    bot.send_message(message.chat.id," Выберите тему для обучения:\n\
    1. Еда\n \
    2. Части тела\n \
    3. Описание внешности\n \
    4. Хобби\n \
    5. Профессии\n \
    6. Чувства и эмоции\n \
    7. Семья\n \
    8. Путешествия\n \
    9. Погода\n \
    10. Неделя\n \
    11. Рабочее пространство\n \
    12. Деньги\n \
Для выбора введите цифру")

    # Вызываем первое слово
    part = -10
    bot.register_next_step_handler(message, ChooseWord, part)
    

# Функция для получения случайного английского слова и его русского перевода

def ChooseWord(message,part):
    if part!=-10:
        part = part
    else:
        part = int(message.text)-1
    df1 = pd.read_excel('EnglishWords.xlsx', sheet_name=part)
    randomrow = df1.sample(n=1)
    ask_word(message, randomrow, part)




# Функция для задания нового слова
def ask_word(message, randomrow, part):
    # Получение случайного английского слова и его русского перевода
    english_word = randomrow.iloc[0,0].lower()
    russian_translation = randomrow.iloc[0,1].lower()

    # Отправка английского слова пользователю
    bot.send_message(message.chat.id, f"Переведите слово {english_word.upper()} на русский:")

    # Ожидание ответа от пользователя
    bot.register_next_step_handler(message, check_translation, english_word, russian_translation, randomrow, part)

# Функция для проверки перевода
def check_translation(message, english_word, russian_translation, randomrow, part):
    global score

    # Получение ответа пользователя
    user_translation = message.text.lower()

    # Проверка правильности перевода
    if user_translation == russian_translation.lower():
        score += 1
        bot.send_message(message.chat.id, "Правильно!")
         # Задаем новое слово
        ChooseWord(message, part)
    elif user_translation == "/stop":
        stop_training(message)

    else:
        bot.send_message(message.chat.id, f"Неправильно! Правильный перевод слова '{english_word}' - '{russian_translation}'.")
         # Задаем новое слово
        ChooseWord(message, part)

   

# Команда /stop останавливает обучение
@bot.message_handler(commands=['stop'])
def stop_training(message):
    global score
    bot.send_message(message.chat.id, f"Вы завершили обучение. Ваш счет: {score}")
    score = 0
    start(message)

# Команда /translate для перевода сообщений с помощью модели машинного перевода
@bot.message_handler(commands=['translate'])
def translate_message(message):
    input_text = message.text.replace('/translate', '').strip()

    if input_text:
        # Подготовка входных данных для модели
        input_ids = tokenizer.encode(input_text, return_tensors='pt')

        # Генерация перевода с помощью модели
        translated_ids = model.generate(input_ids)

        # Декодирование и отправка перевода пользователю
        translated_text = tokenizer.decode(translated_ids[0], skip_special_tokens=True)
        bot.send_message(message.chat.id, translated_text)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, укажите текст для перевода.")

# Обработка сообщений пользователя
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Определение языка текста
    text_language = detect(message.text)

    # Если язык текста не является русским, пытаемся перевести
    if text_language != 'ru':
        translation = translate_english_to_russian(message.text)
        if translation is not None:
            bot.send_message(message.chat.id, translation)
            return

    # Если язык текста русский или перевод не удался, продолжаем другую обработку
    bot.send_message(message.chat.id, "Я не понимаю вас.")

# Функция для перевода с английского на русский
def translate_english_to_russian(text):
    response = requests.get(f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=ru&dt=t&q={text}")
    if response.status_code == 200:
        translation = response.json()[0][0][0]
        return translation
    return None

# Запуск бота
bot.polling()
