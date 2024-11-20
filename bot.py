import logging
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
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

# Initialize bot
try:
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    logging.info(f"Bot successfully initialized - {formatted_time}\n")
except Exception as e:
    logging.error(f"Bot could not be initialized: {str(e)} - {formatted_time}\n")
    exit()

# Define texts and steps
texts = {
    "en": {
        "steps": [
            ["Hi! I’m your personal assistant during the whole registration process. Complete a few simple steps and get up to 15 USDT reward in 24 hours on your telegram wallet!", None],
            ["I suggest you to make some preps and install Outlook and Alipay apps on your phone before starting to follow the steps that will bring you closer to the reward:\n- Make two emails (Outlook)\n- Register on the platform\n- Complete verification\n- Send screenshots to the bot to confirm your registration.", None],
            ["Step 1: Go to the Outlook application and create 2 emails. Ensure the password has at least one digit, and the region matches your region!", None],
            ["Step 2: Download and log into the Alipay app.", None],
            ["It's time to sign up for an account. Ensure your email password matches your Alipay account password!", {"media": "./media/example_image.jpg"}],
            ["Step 4: Take good-quality passport photos and ensure proper lighting for facial verification!", {"media": "./media/example_image.jpg"}],
            ["Did you encounter any problems during the registration process?", {"media": "./media/example_image.jpg"}],
            ["Step 5: Take 3 screenshots as instructed and upload them.", None],
            ["What problem have you faced?", None],
            ["Solution regarding 'restrictions' field.", {"media": "./media/example_image.jpg"}],
            ["Good. Do you wish to create more accounts or proceed with existing ones?", None],
            ["Accounts will get verified. Payment will be done via Cryptobot receipt within 24 hours.", None],
            ["Congratulations.", None],
            ["Contact support!", None],
        ]
    },
    "ru": {
        "steps": [
            ["Привет! Я ваш личный помощник в процессе регистрации. Пройдите несколько простых шагов и получите до 15 USDT на свой кошелек Telegram в течение 24 часов!", None],
            ["Рекомендую заранее установить приложения Outlook и Alipay на телефон перед выполнением шагов, которые приблизят вас к вознаграждению:\n- Создайте два email-адреса (Outlook)\n- Зарегистрируйтесь на платформе\n- Пройдите верификацию\n- Отправьте скриншоты боту для подтверждения регистрации.", None],
            ["Шаг 1: Откройте приложение Outlook и создайте 2 email-адреса. Убедитесь, что пароль содержит хотя бы одну цифру, и выберите ваш регион!", None],
            ["Шаг 2: Скачайте и войдите в приложение Alipay.", None],
            ["Время зарегистрировать аккаунт. Убедитесь, что пароль от электронной почты совпадает с паролем Alipay!", {"media": "./media/example_image.jpg"}],
            ["Шаг 4: Сделайте качественные фото паспорта с хорошим освещением для прохождения верификации!", {"media": "./media/example_image.jpg"}],
            ["Возникли ли у вас проблемы с процессом регистрации?", {"media": "./media/example_image.jpg"}],
            ["Шаг 5: Сделайте 3 скриншота по инструкции и загрузите их.", None],
            ["С какой проблемой вы столкнулись?", None],
            ["Решение по полю 'ограничения'.", {"media": "./media/example_image.jpg"}],
            ["Все хорошо. Хотите создать больше аккаунтов или продолжить с существующими?", None],
            ["Аккаунты будут проверены. Оплата будет произведена через Cryptobot в течение 24 часов.", None],
            ["Поздравляем.", None],
            ["Связаться с поддержкой!", None],
        ]
    },
    "pt": {
        "steps": [
            ["Oi! Sou seu assistente pessoal durante todo o processo de registro. Conclua alguns passos simples e receba até 15 USDT na sua carteira Telegram em 24 horas!", None],
            ["Sugiro que você prepare e instale os aplicativos Outlook e Alipay no seu telefone antes de começar a seguir os passos para se aproximar da recompensa:\n- Crie dois e-mails (Outlook)\n- Cadastre-se na plataforma\n- Complete a verificação\n- Envie capturas de tela para o bot para confirmar seu registro.", None],
            ["Passo 1: Acesse o aplicativo Outlook e crie 2 e-mails. Certifique-se de que a senha tenha pelo menos um número e que a região corresponda à sua região!", None],
            ["Passo 2: Baixe e faça login no aplicativo Alipay.", None],
            ["É hora de criar uma conta. Certifique-se de que a senha do seu e-mail corresponda à senha da conta do Alipay!", {"media": "./media/example_image.jpg"}],
            ["Passo 4: Tire fotos do passaporte com boa qualidade e boa iluminação para a verificação facial!", {"media": "./media/example_image.jpg"}],
            ["Você encontrou algum problema durante o processo de registro?", {"media": "./media/example_image.jpg"}],
            ["Passo 5: Tire 3 capturas de tela conforme as instruções e envie-as.", None],
            ["Qual problema você enfrentou?", None],
            ["Solução para o campo 'restrições'.", {"media": "./media/example_image.jpg"}],
            ["Tudo bem. Deseja criar mais contas ou prosseguir com as existentes?", None],
            ["As contas serão verificadas. O pagamento será feito por recibo do Cryptobot em 24 horas.", None],
            ["Parabéns.", None],
            ["Entre em contato com o suporte!", None],
        ]
    },
    "pl": {
        "steps": [
            ["Cześć! Jestem twoim osobistym asystentem podczas całego procesu rejestracji. Wykonaj kilka prostych kroków i odbierz do 15 USDT w ciągu 24 godzin na swój portfel Telegram!", None],
            ["Sugeruję przygotowanie się i zainstalowanie aplikacji Outlook oraz Alipay na telefonie przed rozpoczęciem kroków, które przybliżą cię do nagrody:\n- Załóż dwa e-maile (Outlook)\n- Zarejestruj się na platformie\n- Ukończ weryfikację\n- Wyślij zrzuty ekranu do bota, aby potwierdzić rejestrację.", None],
            ["Krok 1: Otwórz aplikację Outlook i utwórz 2 e-maile. Upewnij się, że hasło zawiera co najmniej jedną cyfrę, a region odpowiada twojemu regionowi!", None],
            ["Krok 2: Pobierz i zaloguj się do aplikacji Alipay.", None],
            ["Czas na założenie konta. Upewnij się, że hasło e-mail pasuje do hasła konta Alipay!", {"media": "./media/example_image.jpg"}],
            ["Krok 4: Zrób wysokiej jakości zdjęcia paszportowe i zadbaj o dobre oświetlenie do weryfikacji twarzy!", {"media": "./media/example_image.jpg"}],
            ["Czy napotkałeś jakieś problemy podczas procesu rejestracji?", {"media": "./media/example_image.jpg"}],
            ["Krok 5: Wykonaj 3 zrzuty ekranu zgodnie z instrukcją i prześlij je.", None],
            ["Jaki problem napotkałeś?", None],
            ["Rozwiązanie problemu z polem 'ograniczenia'.", {"media": "./media/example_image.jpg"}],
            ["Dobrze. Czy chcesz założyć więcej kont, czy kontynuować z istniejącymi?", None],
            ["Konta zostaną zweryfikowane. Płatność zostanie dokonana przez Cryptobot w ciągu 24 godzin.", None],
            ["Gratulacje.", None],
            ["Skontaktuj się z pomocą techniczną!", None],
        ]
    }
}

# Track user data
user_data = {}

# Generate buttons dynamically
def step_buttons(lang, step):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = {
        0: [("Show the steps", "step_1"), ("Back to language selection", "language_selection")],
        1: [("Let's go", "step_2"), ("Back", "step_0")],
        2: [("Next step", "step_3"), ("Back", "step_1")],
        3: [("Let's go to the 3rd step", "step_4"), ("Back", "step_2")],
        4: [("To the final step", "step_5"), ("Back", "step_3")],
        5: [("Approve account", "step_6"), ("Back", "step_4")],
        6: [("No", "step_7"), ("Screenshot doesn't look alike", "step_8"), ("Back", "step_5")],
        7: [("Submit Screenshots", "submit_screenshots"), ("Back", "step_6")],
        8: [("Support", "redirect to support"), ("Restriction problem", "step_9"), ("Back", "step_6")],
        9: [("All good", "step_7"), ("Back", "step_8"), ("Support", "redirect to support")],
        10: [("Proceed", "step_11"), ("Create", "step_7")],
        11: [("Received Payment", "step_12"), ("Not received Payment", "step_13")],
        13: [("Support", "redirect to support")],
    }
    for text, callback in buttons.get(step, []):
        keyboard.add(KeyboardButton(text))
    return keyboard

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_data[user_id] = {"lang": "en", "step": 0, "screenshots": []}
    logging.info(f"User - {user_id} started the conversation\n")

    # Language selection keyboard
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        KeyboardButton("English"),
        KeyboardButton("Русский"),
        KeyboardButton("Polski"),
        KeyboardButton("Português")
    )
    bot.send_message(
        message.chat.id,
        "Please, choose your language: ",
        reply_markup=keyboard
    )

# Handle language selection
@bot.message_handler(func=lambda message: message.text in ["English", "Русский"])
def set_language(message):
    lang = "en" if message.text == "English" else "ru"
    user_data[message.from_user.id] = {"lang": lang, "step": 0, "screenshots": []}
    bot.send_message(
        message.chat.id,
        texts[lang]["steps"][0][0],
        reply_markup=step_buttons(lang, 0)
    )
# Handle navigation and media display
# Handle navigation and media display
# Navigation logic
@bot.message_handler(func=lambda message: True)
def navigate_steps(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        bot.send_message(message.chat.id, "Please use /start to begin.")
        return

    lang = user_data[user_id]["lang"]
    step = user_data[user_id]["step"]

    # Handle special cases
    if message.text == "Back to language selection":
        start(message)
        return
    if message.text == "Submit Screenshots":
        if len(user_data[user_id]["screenshots"]) < 3:
            bot.send_message(message.chat.id, "Please upload 3 screenshots before proceeding.")
            return
        # Transition to step 10
        user_data[user_id]["step"] = 10
        step = 10
    if message.text == "Create":
        # Reset screenshots for a new account
        user_data[user_id]["screenshots"] = []
        bot.send_message(message.chat.id, "You chose to create a new account. Please upload 3 new screenshots.")
        step = 7
    if message.text == "Support":
        # Inline button for support
        markup = InlineKeyboardMarkup()
        support_button = InlineKeyboardButton(
            text="Contact Support",
            url="https://t.me/Losand"  # Replace with your desired Telegram support link
        )
        markup.add(support_button)

        bot.send_message(
            message.chat.id,
            "Define your problem below or click the button to contact support:",
            reply_markup=markup
        )
        return

    # Navigation mapping
    next_steps = {
        "Show the steps": 1,
        "Let's go": 2,
        "Next step": 3,
        "Let's go to the 3rd step": 4,
        "To the final step": 5,
        "Approve account": 6,
        "No": 7,
        "Screenshot doesn't look alike": 8,
        "Restriction problem": 9,
        "All good": 7,
        "Proceed": step + 1,
        "Create": 7,
        "Received Payment": 12,
        "Not received Payment": 13,
        "Restart": 0,
        "Back": step - 1,
    }

    # Determine the next step
    new_step = next_steps.get(message.text, step)
    user_data[user_id]["step"] = new_step

    # Get text and media for the current step
    text, media = texts[lang]["steps"][new_step]
    keyboard = step_buttons(lang, new_step)

    # Send the appropriate response
    if media and "media" in media:
        with open(media["media"], "rb") as img:
            bot.send_photo(message.chat.id, img, caption=text, reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        bot.send_message(message.chat.id, "Please use /start to begin.")
        return
    step = user_data[user_id]["step"]
    if step == 7:  # Screenshot step
        user_data[user_id]["screenshots"].append(message.photo[-1].file_id)
        uploaded_count = len(user_data[user_id]["screenshots"])
        bot.send_message(message.chat.id, f"Screenshot {uploaded_count}/3 uploaded.")
        if uploaded_count == 3:
            bot.send_message(message.chat.id, "All screenshots uploaded! Click 'Submit Screenshots' to proceed.")
# Run the bot
if __name__ == "__main__":
    bot.infinity_polling()


  #here you need to implement navigation like this:
    # text[steps[0]] goes to step[1] if button "Show the steps" pressed if button "Back to language selection goes to language selection"]
    # text[steps[1] goes to step[2] if button "Let's go" pressed if button "Back" goes to step[1]
    # text[steps[2] goes to step[3] if button "Next step" pressed if button "Back" goes to step[2]
    # text[steps[3] goes to step[4] if button "Let's go to the 3rd step" pressed if button "Back" goes to step[2]
    # text[steps[4] goes to step[5] if button "To the final step " pressed if button "Back" goes to step[3]
    # text[steps[5] goes to step[6] if button "Approve account " pressed if button "Back" goes to step[4]
    # text[steps[6] goes to step[7] if button "No " pressed if button "Screenshot don't look alike" goes to step[8] if button "back" goes to step[5]
    # text[steps[7] goes to step[10] if button "next" pressed and screenshots 3 uploded if button "back" goes to step[6]
    # text[steps[10] goes to step[11] if button "Proceed" pressed if button "create" goes to step[7]
    # text[steps[11] goes to step[12] if button "Proceed" pressed 
    # text[steps[12] goes to step[13] if button "Proceed" pressed
    # text[steps[13] goes to step[14] if button "Payment received" pressed button "Payment not received" goes to step[15]