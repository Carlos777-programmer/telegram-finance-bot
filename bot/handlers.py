from telegram import Update
from telegram.ext import ContextTypes
from bot.menus import *
from services.finance_service import *
from utils.auth import autorizado
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, nova_mensagem=False):
    texto = "Olá, Carlos! Como podemos prosseguir?"

    if update.callback_query and not nova_mensagem:
        await update.callback_query.edit_message_text(text=texto, reply_markup=menu_principal())
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=texto,
            reply_markup=menu_principal()
        )


async def processar_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not autorizado(user_id):
        return await update.message.reply_text("⛔ Acesso negado.")

    dados = registrar_gasto(user_id, update.message.text)

    if not dados:
        return await update.message.reply_text("❓ Formato inválido.")

    resposta = (
        f"✅ *Gasto Salvo!*\n"
        f"💰 R$ {dados['valor']:.2f}\n"
        f"📝 {dados['descricao']}\n"
        f"🏷️ #{dados['categoria']}"
    )

    await update.message.reply_text(resposta, parse_mode='Markdown')
    await start(update, context, nova_mensagem=True)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    # Segurança
    if not autorizado(user_id):
        return await query.answer("⛔ Acesso negado.", show_alert=True)

    await query.answer()

    match query.data:

        case 'menu_gasto':
            keyboard = [[InlineKeyboardButton("⬅️ Voltar", callback_data='voltar_pag')]]
            await query.edit_message_text(
                text="💰 *REGISTRAR GASTO*\n\nDigite: `50 gasolina #carro`",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        case 'menu_escolha_de_resumo':
            await query.edit_message_text(
                text="Escolha o tipo de resumo:",
                reply_markup=menu_resumo()
            )

        case 'menu_resumo':
            total = obter_resumo_geral(user_id)
            await query.edit_message_text(
                text=f"📊 Total gasto: R$ {total:.2f}",
                parse_mode='Markdown'
            )
            return await start(update, context, nova_mensagem=True)

        case 'resumo_categoria':
            dados = obter_resumo_categoria(user_id)

            mensagem = "📊 *Resumo por Categoria:*\n"
            for categoria, valor in dados:
                mensagem += f"🔹 {categoria}: R$ {valor:.2f}\n"

            await query.edit_message_text(mensagem, parse_mode='Markdown')
            return await start(update, context, nova_mensagem=True)

        case 'menu_config':
            await query.edit_message_text(
                text="Configurações:",
                reply_markup=menu_configuracoes()
            )

        case 'confirmacao_delet':
            await query.edit_message_text(
                text="⚠️ Tem certeza que deseja deletar tudo?",
                reply_markup=menu_confirmar_delete()
            )

        case 'delet_gastos':
            deletar_tudo(user_id)
            await query.edit_message_text("✅ Dados apagados com sucesso!")
            return await start(update, context, nova_mensagem=True)

        case 'voltar_pag':
            await start(update, context, nova_mensagem=False)

        case _:
            await query.edit_message_text("Opção inválida.")