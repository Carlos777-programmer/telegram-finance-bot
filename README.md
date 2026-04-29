# 💰 Telegram Financial Bot

Um bot de gestão financeira pessoal que permite registrar gastos de forma rápida e prática diretamente pelo Telegram, utilizando linguagem natural.

---

## 💡 Problema

Controlar gastos no dia a dia costuma ser algo demorado e pouco prático. Muitas pessoas deixam de registrar despesas por falta de agilidade.

---

## ✅ Solução

Este bot permite registrar despesas em segundos, usando mensagens simples como: 50 gasolina #carro


Os dados são processados automaticamente e armazenados em banco de dados, permitindo consultas rápidas diretamente no chat.

---

## 🚀 Funcionalidades

- ✔️ Registro rápido de gastos via texto  
- ✔️ Categorização automática com hashtags  
- ✔️ Resumo geral de gastos  
- ✔️ Resumo por categoria  
- ✔️ Sistema de segurança (uso privado por ID)  
- 🔜 Resumo mensal  
- 🔜 Exportação para CSV/Excel  

---

## 💬 Exemplos de uso

### Entrada: 
50 gasolina #carro

### Saída:
✅ Gasto Salvo!
💰 R$ 50.00
📝 gasolina
🏷️ #carro

---

## 🧠 Arquitetura

O projeto foi estruturado com separação de responsabilidades:

- `bot/` → Interface com o Telegram (handlers e menus)  
- `services/` → Regras de negócio  
- `repositories/` → Acesso ao banco de dados  
- `utils/` → Funções auxiliares (parser, autenticação)  
- `config/` → Configurações e variáveis de ambiente  

---

## ⚙️ Tecnologias

- Python 3.x  
- Telegram Bot API  
- SQLite  
- python-telegram-bot  
- python-dotenv  

---

## ▶️ Como rodar o projeto

```bash
git clone https://github.com/Carlos777-programmer/telegram-finance-bot.git
cd telegram-finance-bot
pip install -r requirements.txt

# Crie um arquivo .env na raiz do projeto:

TELEGRAM_TOKEN=seu_token 
MY_TELEGRAM_ID=seu_id

# Execute o projeto:

python main.py
```
---

## 📌 Melhorias futuras

- Filtro por período (mensal/semanal)  
- Exportação de dados  
- Suporte a múltiplos usuários  
- Dashboard web  

---

## 👤 Autor

Carlos Marques  
Estudante de Engenharia da Computação (UNIVESP)

[LinkedIn](https://www.linkedin.com/in/carlos-marques-0b9346267/) | [GitHub](https://github.com/Carlos777-programmer)