import os 
import re
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
USER_ID = int(os.getenv("MY_TELEGRAM_ID"))

def parser_financeiro(texto):
    """Extrai valor, descrição e categoria de uma frase."""
    valor_match = re.search(r'(\d+[.,]\d+|\d+)', texto) # Procura o valor (ex: 50.00 ou 50,00)
    if not valor_match: 
        return None
    
    valor = float(valor_match.group(1).replace(',', '.'))

    # Procura a categoria (ex: #carro)
    categoria_match = re.search(r'#(\w+)', texto)
    categoria = categoria_match.group(1) if categoria_match else "Geral"

    # Remove o valor e a categoria para sobrar a descrição 
    descricao = texto.replace(valor_match.group(0), "").replace(f"#{categoria}", "").strip()
    
    return {"valor": valor, "descricao": descricao or "Sem Descrição", "categoria": categoria}

async def processar_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Recebi mensagem de: {update.message.from_user.id}") # DEBUG 1
    # SEGURANÇA: Bloqueia qualquer ID que não seja o do Usuário Cadastrado
    if update.message.from_user.id != USER_ID:
        print("Bloqueado por segurança!") # DEBUG 2
        await update.message.reply_text("⛔ Acesso negado. Bot privado.")
        return
    
    dados = parser_financeiro(update.message.text)

    if dados:
        resposta = (
            f"✅ *Gasto Identificado!*\n"
            f"---"
            f"💰 *Valor:* R$ {dados['valor']:.2f}\n"
            f"📝 *Descrição:* {dados['descricao']}\n"
            f"🏷️ *Categoria:* #{dados['categoria']}"
        )
        await update.message.reply_text(resposta, parse_mode='Markdown')
    else:
        await update.message.reply_text("❓ Não entendi o formato.\n Use: `Valor Descrição #categoria`")
    
if __name__ == '__main__':
        
    try:
        print("--- Iniciando o Processo de Boot do Bot ---")
        
        if not TOKEN:
            print("ERRO: TOKEN não encontrado. Verifique seu arquivo .env!")
        else:
            application = ApplicationBuilder().token(TOKEN).build()
            
            # Handler para mensagens de texto
            msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), processar_mensagem)
            application.add_handler(msg_handler)
            
            print("✅ Bot está online e ouvindo...")
            application.run_polling()
            
    except Exception as e:
        print(f"❌ Ocorreu um erro crítico: {e}")

        # Inicializa o bot
        application = ApplicationBuilder().token(TOKEN).build()
        # Handler: Filtra apenas mensagens de texto que não seja comandos
        msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), processar_mensagem)
        application.add_handler(msg_handler)

        print("Bot rodando... Pressione Ctrl+C para encerrar.")
        application.run_polling()