import os 
import re
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler, CallbackQueryHandler
import database

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
USER_ID = int(os.getenv("MY_TELEGRAM_ID"))

def menu_principal(): # Menu Principal, para seleção de próximo processo. (Para melhor controle de Usuário.)
    keyboard = [
        [
            InlineKeyboardButton("➕ Registrar Gasto", callback_data='menu_gasto'),
            InlineKeyboardButton("📊 Ver Resumo", callback_data='menu_escolha_de_resumo'),
        ],
        [InlineKeyboardButton("⚙️ Configurações", callback_data='menu_config')]
    ]
    return InlineKeyboardMarkup(keyboard) # Criando o objeto de teclado

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá, Carlos! Como podemos prosseguir?",
        reply_markup=menu_principal()
    )

def menu_configuracoes():
    keyboard = [
        [
            InlineKeyboardButton("Deletar Gastos", callback_data='delet_gastos'),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def resumo_por_categoria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lógica para capturar o ID independente de como o comando veio
    if update.message:
        # Se veio por mensagem (/categoria)
        user_data = update.message.from_user
        responder = update.message.reply_text
    else: 
        # Se veio pelo clique do botão
        user_data = update.callback_query.from_user
        responder = update.callback_query.edit_message_text
    
    uid = user_data.id # Pega o ID do usuário que mandou a mensagem

    if uid != USER_ID: # SEGURANÇA: Só responde se for o ID
        await update.message.reply_text("⚠️ *SECURITY ALERT* ⚠️\n\n"
        "Tentativa de acesso não autorizada detectada.\n"
        "Este bot é de uso privado. 🔒", parse_mode='Markdown'
        )
        return
    total = database.db_resumo_por_categoria(uid)
    mensagem = "📊 *Resumo por Categoria:*\n"
    for linha in total:
        categoria = linha[0]
        valor = linha[1]
        mensagem += f"🔹 {categoria}: R$ {valor:.2f}\n"
    await responder(mensagem, parse_mode='Markdown')
    

async def resumo_geral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lógica para capturar o ID independente de como o comando veio
    if update.message:
        # Se veio por mensagem (/resumo)
        user_data = update.message.from_user
        responder = update.message.reply_text
    else:
        # Se veio pelo clique do botão 
        user_data = update.callback_query.from_user
        responder = update.callback_query.edit_message_text

    uid = user_data.id # Pega o ID de quem mandou a mensagem

    if uid != USER_ID: # SEGURANÇA: Só responde se for o ID
        await update.message.reply_text("⚠️ **SECURITY ALERT** ⚠️\n\n"
        "Tentativa de acesso não autorizada detectada.\n"
        "Este bot é de uso privado. 🔒", parse_mode='Markdown'
        )
        return
    total = database.db_obter_resumo_total(uid)
    mensagem = f"📊 *Seu Resumo Geral*\n\nTotal gasto: *R$ {total:.2f}*"
    await responder(mensagem, parse_mode='Markdown')

def parser_financeiro(texto):
    """Extrai valor, descrição e categoria de uma frase."""
    valor_match = re.search(r'(\d+[.,]\d+|\d+)', texto) # Procura o valor (ex: 50.00 ou 50,00)
    if not valor_match: 
        return None
    
    valor = float(valor_match.group(1).replace(',', '.'))
    categoria_match = re.search(r'#(\w+)', texto) # Procura a categoria (ex: #carro)
    categoria = categoria_match.group(1) if categoria_match else "Geral"
    descricao = texto.replace(valor_match.group(0), "").replace(f"#{categoria}", "").strip() # Remove o valor e a categoria para sobrar a descrição 
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
        try:
            database.salvar_gasto(
                usuario_id=update.message.from_user.id,
                valor=dados['valor'],
                descricao=dados['descricao'],
                categoria=dados['categoria']
            )
            resposta = (
                f"✅ *Gasto Salvo!*\n"
                f"---"
                f"💰 *Valor:* R$ {dados['valor']:.2f}\n"
                f"📝 *Descrição:* {dados['descricao']}\n"
                f"🏷️ *Categoria:* #{dados['categoria']}"
            )
        except Exception as e: 
            resposta = f"❌ Erro ao salvar no banco: {e}"
        await update.message.reply_text(resposta, parse_mode='Markdown')
    else:
        await update.message.reply_text("❓ Não entendi o formato.\n Use: `Valor Descrição #categoria`")

def menu_escolha_de_resumo(): 
    keyboard_resumo = [
        [InlineKeyboardButton("Resumo por Categoria", callback_data='resumo_categoria')], # Use listas dentro de listas
        [InlineKeyboardButton("Resumo Geral", callback_data='menu_resumo')]
    ]
    return InlineKeyboardMarkup(keyboard_resumo) # Criando o Objeto de teclado

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id 

    # SEGURANÇA: IF para verificação externa de segurança de ID, responde apenas ao ID cadastrado
    if uid != USER_ID:
        await update.message.reply_text(
            "⚠️ **SECURITY ALERT** ⚠️\n\nEste bot é de uso privado. 🔒", 
            parse_mode='Markdown'
        )
        return

    await query.answer() 

    # Aqui entra o match/case para tratar os botões
    match query.data:
        case 'menu_gasto':
            await query.edit_message_text(text="Digite o valor:")
        
        case 'menu_escolha_de_resumo':
            await query.edit_message_text(
                text="Selecione o tipo de resumo", 
                reply_markup=menu_escolha_de_resumo()
            )

        case 'menu_resumo': 
            await query.edit_message_text(text="Calculando seus gastos *Gerais*", parse_mode='Markdown')
            return await resumo_geral(update, context)
            
        case 'resumo_categoria':
            await query.edit_message_text(text="Separando e calculando seus gastos por *Categorias*", parse_mode='Markdown')
            return await resumo_por_categoria(update, context)
        
        case 'menu_config':
            await query.edit_message_text(text="Como deseja prosseguir?", reply_markup=menu_configuracoes())
        
        case 'delet_gastos':
            await query.edit_message_text(text="*Gastos* deletado com sucesso!", parse_mode='Markdown')
            return database.deletar_gastos(usuario_id=uid)
        
        case _: # Opcional: equivalente ao "else", captura qualquer comando não mapeado
            await query.edit_message_text(text="Opção inválida.")

if __name__ == '__main__':
    database.criar_tabela() # Cria a tabela no banco de dados assim que o bot liga (se não existir)    
    try:
        print("--- Iniciando o Processo de Boot do Bot ---")
        
        if not TOKEN:
            print("ERRO: TOKEN não encontrado. Verifique seu arquivo .env!")
        else:
            application = ApplicationBuilder().token(TOKEN).build()
            
            # Handler para mensagens de texto
            start_handler = CommandHandler("start", start)
            msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), processar_mensagem)
            resumo_handler = CommandHandler("resumo", resumo_geral)
            categoria_handler = CommandHandler("categoria", resumo_por_categoria)
            
            # Sensores do BOT
            application.add_handler(start_handler)
            application.add_handler(CallbackQueryHandler(button_handler))
            application.add_handler(msg_handler)
            application.add_handler(resumo_handler)
            application.add_handler(categoria_handler)

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