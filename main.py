import os 
import re
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
USER_ID = int(os.getenv("TELEGRAM_USER_ID"))

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


