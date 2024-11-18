import logging
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Configure logging
current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
logging.basicConfig(level=logging.INFO)
logging.info(f'Starting Bot {formatted_time}')

try:
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    logging.info(f"Bot successfully initialized - {formatted_time}\n")
except Exception as e:
    logging.error(f"Bot could not be initialized: {str(e)} - {formatted_time}\n")

# Define texts for English and Russian
texts = {
    "en": {
        "welcome": "Hello! I will guide you through the verification process in the AliPay app...",
        "overview": "The process consists of 4 steps:\n1. Create an email.\n2. Register in the app.\n3. Pass verification.\n4. Send the photo to the bot.",
        "steps": [
            "Step 1: Create an email in the Outlook.com app. The email region must match your country of residence. Save the account details (login and password).",
            "Step 2: Download and log in to the AliPay app.",
            "Step 3: Register an account (video on how to do this will follow). The password for the email and the AliPay account must match!",
            "Step 4: Complete the verification process (video will follow)."
        ],
        "completion": "Send the photo to the bot, and we’ll verify your account.",
        "back_to_language": "Back to language selection"
    },
    "ru": {
        "welcome": "Привет! Я помогу тебе пройти процесс верификации в приложении AliPay...",
        "overview": "Процесс состоит из 4 шагов:\n1. Создание почты.\n2. Регистрация в приложении.\n3. Прохождение верификации.\n4. Отправить фото боту.",
        "steps": [
            "1 шаг: Создать почту в приложении Outlook.com. Регион почты должен совпадать с вашей страной проживания. Данные от аккаунта сохранить (логин и пароль).",
            "2 шаг: Скачиваем и заходим в приложение AliPay.",
            "3 шаг: Регистрируем аккаунт (видео как именно потом). Пароль от почты и от аккаунта AliPay обязательно должен совпадать!",
            "4 шаг: Прохождение верификации (тоже видео потом)."
        ],
        "completion": "Отправьте фото боту, и мы проверим ваш аккаунт.",
        "back_to_language": "Вернуться к выбору языка"
    }
}

# Track user data
user_data = {}

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    logging.info(f"User - {user_id} started the conversation\n")
    
    # Language selection keyboard
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        KeyboardButton("English"),
        KeyboardButton("Русский")
    )
    
    bot.send_message(
        message.chat.id,
        "Choose your language / Выберите язык:",
        reply_markup=keyboard
    )

# Handle language selection
@bot.message_handler(func=lambda message: message.text in ["English", "Русский"])
def set_language(message):
    lang = "en" if message.text == "English" else "ru"
    user_data[message.from_user.id] = {"lang": lang, "step": -1}  # Step -1 for overview

    keyboard = overview_buttons(lang)
    bot.send_message(
        message.chat.id,
        texts[lang]["welcome"],
        reply_markup=keyboard
    )

# Generate overview buttons
def overview_buttons(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(
        KeyboardButton("Start Process"),
        KeyboardButton(texts[lang]["back_to_language"])
    )
    return keyboard

# Generate step buttons
def step_buttons(lang, step):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        KeyboardButton("Back")
    )
    if step < len(texts[lang]["steps"]) - 1:  # Add "Next" button if not on the last step
        keyboard.add(KeyboardButton("Next"))
    return keyboard

# Handle navigation
@bot.message_handler(func=lambda message: message.text in ["Start Process", "Back", "Next", "Back to language selection", "Вернуться к выбору языка"])
def navigate_steps(message):
    user_id = message.from_user.id

    # Ensure user exists in user_data
    if user_id not in user_data:
        bot.send_message(message.chat.id, "Please restart the process using /start.")
        return
    
    lang = user_data[user_id]["lang"]
    step = user_data[user_id]["step"]

    # Navigation logic
    if message.text == "Start Process":
        step = 0
    elif message.text == "Next":
        step += 1
    elif message.text == "Back":
        if step > 0:
            step -= 1
        else:  # If at step 0, go back to the overview step
            step = -1
    elif message.text in ["Back to language selection", "Вернуться к выбору языка"]:
        # Restart the language selection
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(
            KeyboardButton("English"),
            KeyboardButton("Русский")
        )
        bot.send_message(
            message.chat.id,
            "Choose your language / Выберите язык:",
            reply_markup=keyboard
        )
        return

    # Validate step range
    if step < -1:  # Prevent invalid steps
        step = -1
    elif step >= len(texts[lang]["steps"]):  # Prevent going beyond last step
        step = len(texts[lang]["steps"]) - 1

    # Update user step
    user_data[user_id]["step"] = step

    # Display appropriate message based on step
    if step == -1:  # Overview step
        bot.send_message(
            message.chat.id,
            texts[lang]["overview"],
            reply_markup=overview_buttons(lang)
        )
    else:  # Regular steps
        bot.send_message(
            message.chat.id,
            texts[lang]["steps"][step],
            reply_markup=step_buttons(lang, step)
        )

# Run the bot
if __name__ == "__main__":
    bot.infinity_polling()
