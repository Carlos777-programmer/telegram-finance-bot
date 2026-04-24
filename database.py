import sqlite3
from datetime import datetime

def conectar():
    """Conecta ao arquivo de banco de dados. Se não existir, o SQLite cria na hora."""
    return sqlite3.connect('financeiro.db')

def criar_tabela():
    """Define a estrutura (colunas) da nossa tabela de gastos."""
    conn = conectar()
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
    conn.commit()
    conn.close()
    print("🗄️ Tabela verificada/criada com sucesso!")

def salvar_gasto(usuario_id, valor, descricao, categoria):
    """Mapeia os dados do Python para as colunas do SQL."""
    conn = conectar()
    cursor = conn.cursor()
    data_hoje = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    cursor.execute('''
        INSERT INTO gastos (usuario_id, valor, descricao, categoria, data)
        VALUES (?, ?, ?, ?, ?)
    ''', (usuario_id, valor, descricao, categoria, data_hoje))

    conn.commit()
    conn.close()

def db_obter_resumo_total(usuario_id):
    """Faz um resumo geral de cada coluna."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(valor) FROM gastos WHERE usuario_id = ?", (usuario_id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado[0] is not None else 0

def db_resumo_por_categoria(usuario_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT categoria, SUM(valor) FROM gastos WHERE usuario_id = ? GROUP BY categoria", (usuario_id,))
    resultado = cursor.fetchall()
    print(f"O que o banco devolveu: {resultado}") # Para listar no terminal os dados
    conn.close()
    return resultado

def deletar_gastos(usuario_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM gastos WHERE usuario_id = ?", (usuario_id,))
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='gastos'")
    conn.commit()
    conn.close()
    return True

