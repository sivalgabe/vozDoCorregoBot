from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

import os
import logging
import answers
import mainMenu
import secondaryMenu
import whereMenu

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    print("ERRO: TOKEN não foi carregado")
    exit()

print(f"TOKEN carregado: {TOKEN}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Recebi um /start de {update.effective_user.first_name}")

    keyboard = [
        [mainMenu.menuWhat, mainMenu.menuHow],
        [mainMenu.menuWhere, mainMenu.menuContact]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(answers.greetings,
        reply_markup=reply_markup
    )

async def send_main_menu(update: Update):
    keyboard = [
        [mainMenu.menuWhat, mainMenu.menuHow],
        [mainMenu.menuWhere, mainMenu.menuContact]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(answers.greetings,
        reply_markup=reply_markup
    )

async def send_secondary_menu(update: Update):
    keyboard = [
        [secondaryMenu.menuCommon, secondaryMenu.menuRecyclable]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(answers.whatAnswer,
        reply_markup=reply_markup
    )

async def send_where_menu(update: Update):
    keyboard = [
        [whereMenu.menuReject, whereMenu.menuPaper],
        [whereMenu.menuWood, whereMenu.menuEletronics],
        [whereMenu.menuOil, whereMenu.menuMedicine],
        [whereMenu.menuNonRecyclable]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(answers.whereAnswer,
        reply_markup=reply_markup
    )

async def debug_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    text = update.message.text

    print(f"[DEBUG] Mensagem de {user}: {text}")
    
    if text == mainMenu.menuWhat:
        await send_secondary_menu(update)
    elif text == mainMenu.menuHow:
        await update.message.reply_text(answers.howAnswer)
    elif text == mainMenu.menuContact:
        await update.message.reply_text(answers.contactAnswer)
    elif text == mainMenu.menuWhere:
        await send_where_menu(update)
    elif text == whereMenu.menuReject:
        await update.message.reply_text(answers.rejectAnswer)
        await send_main_menu(update)
    elif text == whereMenu.menuPaper:
        await update.message.reply_text(answers.paperAnswer)
        await send_main_menu(update)
    elif text == whereMenu.menuWood:
        await update.message.reply_text(answers.woodAnswer)
        await send_main_menu(update)
    elif text == whereMenu.menuEletronics:
        await update.message.reply_text(answers.eletronicsAnswer)
        await send_main_menu(update)
    elif text == whereMenu.menuOil:
        await update.message.reply_text(answers.oilAnswer)
        await send_main_menu(update)
    elif text == whereMenu.menuMedicine:
        await update.message.reply_text(answers.medicineAnswer)
        await send_main_menu(update)
    elif text == whereMenu.menuNonRecyclable:
        await update.message.reply_text(answers.nonRecyclableAnswer)
        await send_main_menu(update)
    elif text == secondaryMenu.menuCommon:
        await update.message.reply_text(answers.commonAnswer)
        await send_main_menu(update)
    elif text == secondaryMenu.menuRecyclable:
        await update.message.reply_text(answers.recyclableMetalAnswer)
        await update.message.reply_text(answers.recyclablePaperAnswer)
        await update.message.reply_text(answers.recyclableGlassAnswer)
        await update.message.reply_text(answers.recyclablePlasticAnswer)
        await send_main_menu(update)
    else:
        await update.message.reply_text(answers.tryagain)
        await send_main_menu(update)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, debug_message))

print("Voz online")

app.run_polling()