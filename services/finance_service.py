from utils.parser import parser_financeiro
from repositories import database


def registrar_gasto(user_id: int, texto: str):
    dados = parser_financeiro(texto)

    if not dados:
        return {"❓ Formato inválido.": "Use o padrão:/n `50 gasolina #carro"}

    database.salvar_gasto(
        usuario_id=user_id,
        valor=dados["valor"],
        descricao=dados["descricao"],
        categoria=dados["categoria"]
    )

    return dados


def obter_resumo_geral(user_id: int):
    return database.obter_resumo_total(user_id)


def obter_resumo_categoria(user_id: int):
    return database.obter_resumo_por_categoria(user_id)


def deletar_tudo(user_id: int):
    database.deletar_gastos(user_id)