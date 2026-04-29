from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from repositories.database import criar_tabela
from config.settings import TOKEN
from bot.handlers import start, processar_mensagem, button_handler

def main():
    criar_tabela()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), processar_mensagem))
    

    app.run_polling()

if __name__ == "__main__":
    main()