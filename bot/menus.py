from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def menu_principal():
    keyboard = [
        [InlineKeyboardButton("➕ Registrar Gasto", callback_data='menu_gasto')],
        [InlineKeyboardButton("📊 Ver Resumo", callback_data='menu_escolha_de_resumo')],
        [InlineKeyboardButton("⚙️ Configurações", callback_data='menu_config')],
    ]
    return InlineKeyboardMarkup(keyboard)


def menu_configuracoes():
    keyboard = [
        [InlineKeyboardButton("Deletar Gastos", callback_data='confirmacao_delet')],
        [InlineKeyboardButton("⬅️ Voltar", callback_data='voltar_pag')],
    ]
    return InlineKeyboardMarkup(keyboard)


def menu_confirmar_delete():
    keyboard = [
        [InlineKeyboardButton("Sim, tenho certeza", callback_data='delet_gastos')],
        [InlineKeyboardButton("Não", callback_data='voltar_pag')],
    ]
    return InlineKeyboardMarkup(keyboard)


def menu_resumo():
    keyboard = [
        [InlineKeyboardButton("Resumo por Categoria", callback_data='resumo_categoria')],
        [InlineKeyboardButton("Resumo Geral", callback_data='menu_resumo')],
        [InlineKeyboardButton("⬅️ Voltar", callback_data='voltar_pag')],
    ]
    return InlineKeyboardMarkup(keyboard)