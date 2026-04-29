import re

def parser_financeiro(texto):
    """Extrai valor, descrição e categoria de uma frase."""
    valor_match = re.search(r'(\d+[.,]\d+|\d+)', texto) # Procura o valor (ex: 50.00 ou 50,00)
    if not valor_match: 
        return None
    
    valor = float(valor_match.group(1).replace(',', '.'))

    categoria_match = re.search(r'#(\w+)', texto) # Procura a categoria (ex: #carro)
    categoria = categoria_match.group(1) if categoria_match else "Geral"

    descricao = texto.replace(valor_match.group(0), "").replace(f"#{categoria}", "").strip() # Remove o valor e a categoria para sobrar a descrição 
    
    return {
        "valor": valor,
        "descricao": descricao or "Sem Descrição",
        "categoria": categoria
    }