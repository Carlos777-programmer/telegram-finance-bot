import sqlite3
from datetime import datetime

DB_NAME = "financeiro.db"


def conectar():
    return sqlite3.connect(DB_NAME)


def criar_tabela():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gastos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                valor REAL NOT NULL,
                descricao TEXT,
                categoria TEXT,
                data TEXT NOT NULL
            )
        ''')
    print("🗄️ Tabela verificada/criada com sucesso!")


def salvar_gasto(usuario_id, valor, descricao, categoria):
    data_hoje = datetime.now().isoformat()  

    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO gastos (usuario_id, valor, descricao, categoria, data)
            VALUES (?, ?, ?, ?, ?)
        ''', (usuario_id, valor, descricao, categoria, data_hoje))


def obter_resumo_total(usuario_id):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT SUM(valor) FROM gastos WHERE usuario_id = ?",
            (usuario_id,)
        )
        resultado = cursor.fetchone()

    return resultado[0] if resultado[0] else 0


def obter_resumo_por_categoria(usuario_id):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT categoria, SUM(valor) FROM gastos WHERE usuario_id = ? GROUP BY categoria",
            (usuario_id,)
        )
        resultado = cursor.fetchall()

    return resultado


def deletar_gastos(usuario_id):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM gastos WHERE usuario_id = ?", (usuario_id,))
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='gastos'")