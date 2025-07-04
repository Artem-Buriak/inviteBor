import logging
import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Load environment variables from .env file
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get the bot token from the environment variable
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# --- Texts ---
WELCOME_TEXT = """
Привіт❤️
Ви чекали? 
Ми дуууже) 

Це особливий момент нашого життя, і ми мріємо розділити його з тобою — з тими, кого любимо, цінуємо і хочемо бачити поруч.

Тож чекаємо вас 1 серпня у комплексі Relax Resort
Початок церемонії о 13:30 

❤️дізнавайтесь деталі святкування
❤️спілкуйтесь в чаті
❤️задавайте свої питання
❤️відправляйте фото з весілля в груповий чат з гостями 

А тепер — найважливіше:
👉 Чи зможеш бути з нами в цей особливий день?
"""

REGRET_TEXT = """
Шкода, що не вийде побачитись у цей день 😔
Але ми все одно дуууже раді, що ви є в нашому житті і ми обов'язково побачимось пізніше, щоб відсвяткувати наше весілля 💛
"""


LOCATION_TEXT = """
📍 *Локація*
– *Назва:* Relax Resort
– *Адреса:* м. Самар, вул. Гідності, 2А
[Посилання на Google Maps](https://maps.app.goo.gl/z4oGZf5d5aJ6fHcPA)
"""

TIMING_TEXT = """
🕓 *Таймінг*
– *Збір гостей:* 13:30
– *Початок весільної церемонії:* 14:00
– *Конкурси, пісні, танці:* 15:30
– *Завершення святкування:* 22:00 
"""

TRANSPORT_TEXT = """
🚖 *Транспорт*
Ми дуже хочемо, щоб вам було комфортно дістатись до місця святкування — тому попіклувалися про транспорт для всіх гостей 💛
🕐 *Виїзд:* о 12:50 від ТЦ «Мост Сіті»
Просимо бути трохи завчасно, щоб усе пройшло спокійно і вчасно :)

А якщо ви плануєте їхати на власному авто і маєте вільні місця — буде чудово, якщо зможете прихопити когось за компанію 🚗

Усі деталі, побажання і координацію можна зручно обговорити у спільному чатику гостей — посилання знайдеш у меню 💬

Після завершення вечора транспорт також поверне гостей назад до міста.
"""

DRESS_CODE_TEXT = """
💃🏼 *Дрес-код*
Ми вирішили не встановлювати суворих правил у стилі "бузкова сорочка й сукня кольору марсала" 🙃

Ніякого офіційного дрес-коду немає.
Просто оберіть образ, у якому вам буде комфортно, красиво й святково.
Головне - щоби ви почувалися собою, і щоб ваш настрій пасував до нашого дня 💛

А ще — буде багато фото, тож якщо раптом давно хотіли вигуляти щось особливе — саме час 😉
"""

GIFTS_TEXT = """
💸 *Подарунки*
Найбільший подарунок для нас — це ваша присутність у цей день 🤍
Але якщо захочеться потішити нас ще й матеріально — ми будемо щиро раді грошовому подарунку 💌

Ми вже потроху збираємо на спільні мрії — тому готівка, банківські перекази, акції чи навіть криптовалюта — все підійде 😄

🌸 А замість живих квітів нам буде дуже приємно отримати щось невеличке й пам’ятне - те, що залишиться на згадку.

Обіймаємо і дякуємо, що ви з нами 💛
"""

GUEST_CHAT_TEXT = """
💌 *Чат з гостями*
Ми створили спільний чат для гостей — там можна ставити питання, дізнаватись актуальні новини стосовно святкування, знайомитись а також надсилати спільні фото і відео з весілля📸
Приєднуйся 💬
"""

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message with invitation buttons."""
    keyboard = [
        [InlineKeyboardButton("✅ Так, буду з вами", callback_data="attend_yes")],
        [InlineKeyboardButton("❌ На жаль, не зможу", callback_data="attend_no")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(WELCOME_TEXT, reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    user = query.from_user
    await query.answer()

    # Store the main menu message id if it's not already stored
    if 'main_menu_message_id' not in context.user_data:
        if query.message:
            context.user_data['main_menu_message_id'] = query.message.message_id

    if query.data == "attend_yes":
        # Notify the admin
        admin_chat_id = os.getenv("ADMIN_CHAT_ID")
        if admin_chat_id:
            user_info = f"""✅ Новий гість!

"""
            user_info += f"""Ім'я: {user.first_name}
"""
            if user.last_name:
                user_info += f"""Прізвище: {user.last_name}
"""
            if user.username:
                user_info += f"""Username: @{user.username}
"""
            user_info += f"ID: {user.id}"
            
            try:
                await context.bot.send_message(chat_id=admin_chat_id, text=user_info)
            except Exception as e:
                logger.error(f"Failed to send notification to admin: {e}")

        # Remove buttons from the original message
        if query.message:
            await query.edit_message_reply_markup(reply_markup=None)
        
        # Send a new confirmation message and the main menu
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Дякуємо за відповідь! ❤️")
        await main_menu(update, context)

    elif query.data == "attend_no":
        # Notify the admin
        admin_chat_id = os.getenv("ADMIN_CHAT_ID")
        if admin_chat_id:
            user_info = f"""❌ На жаль, гість не зможе бути присутнім

"""
            user_info += f"""Ім'я: {user.first_name}
"""
            if user.last_name:
                user_info += f"""Прізвище: {user.last_name}
"""
            if user.username:
                user_info += f"""Username: @{user.username}
"""
            user_info += f"ID: {user.id}"

            try:
                await context.bot.send_message(chat_id=admin_chat_id, text=user_info)
            except Exception as e:
                logger.error(f"Failed to send notification to admin: {e}")
        
        # Remove buttons from the original message and send a new one
        if query.message:
            await query.edit_message_reply_markup(reply_markup=None)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=REGRET_TEXT)

    elif query.data == "main_menu":
        # Edit the message to show the main menu
        await main_menu(update, context, edit_message=True)

    else:
        # For other buttons, edit the message to show details
        text, reply_markup = get_details(query.data)
        if text and query.message:
            try:
                await query.edit_message_text(
                    text=text,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Failed to edit message to show details: {e}")


def get_details(data):
    """Returns the text and keyboard for a given detail."""
    text = ""
    reply_markup = back_to_menu_keyboard()

    if data == "location":
        text = LOCATION_TEXT
    elif data == "timing":
        text = TIMING_TEXT
    elif data == "transport":
        text = TRANSPORT_TEXT
    elif data == "dress_code":
        text = DRESS_CODE_TEXT
    elif data == "gifts":
        text = GIFTS_TEXT
    elif data == "guest_chat":
        text = GUEST_CHAT_TEXT
        keyboard = [
            [InlineKeyboardButton("Приєднатись до чату", url="https://t.me/+HAdohx3VjvRmZjQy")],
            [InlineKeyboardButton("⬅️ Повернутись у головне меню", callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
    
    return text, reply_markup


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, edit_message: bool = False) -> None:
    """Displays the main menu."""
    keyboard = [
        [InlineKeyboardButton("📍 Локація", callback_data="location"), InlineKeyboardButton("🕓 Таймінг", callback_data="timing")],
        [InlineKeyboardButton("🚖 Транспорт", callback_data="transport"), InlineKeyboardButton("💃🏼 Дрес-код", callback_data="dress_code")],
        [InlineKeyboardButton("💸 Подарунки", callback_data="gifts"), InlineKeyboardButton("💌 Чат з гостями", callback_data="guest_chat")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    menu_text = "Оберіть, що вас цікавить:"

    if edit_message and update.callback_query:
        try:
            await update.callback_query.edit_message_text(menu_text, reply_markup=reply_markup)
            context.user_data['main_menu_message_id'] = update.callback_query.message.message_id
        except Exception as e:
            logger.error(f"Failed to edit main menu message: {e}")
    else:
        menu_message = await context.bot.send_message(chat_id=update.effective_chat.id, text=menu_text, reply_markup=reply_markup)
        context.user_data['main_menu_message_id'] = menu_message.message_id



def back_to_menu_keyboard():
    """Returns a keyboard with a back to main menu button."""
    keyboard = [
        [InlineKeyboardButton("⬅️ Повернутись у головне меню", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("menu", main_menu))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
