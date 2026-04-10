# 💰 Financial Management Bot (Telegram + Python)

Este projeto é um sistema de gestão financeira pessoal que utiliza o Telegram como interface de entrada. O objetivo é permitir o registro rápido de despesas e receitas através de mensagens de texto simples, que são processadas e armazenadas em um banco de dados estruturado.

---

## 🚀 Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Interface:** Telegram Bot API
* **Banco de Dados:** SQLite (Desenvolvimento) / PostgreSQL (Produção)
* **Bibliotecas Principais:** * `python-telegram-bot`: Integração com a API do Telegram.
    * `python-dotenv`: Gerenciamento de variáveis de ambiente (Segurança).
    * `re` (Regex): Processamento de linguagem natural para extração de dados.

---

## 🛠️ Funcionalidades Planejadas

- [ ] Registro de gastos via comandos simples (Ex: `50.00 Gasolina #carro`).
- [ ] Categorização automática utilizando hashtags.
- [ ] Consulta de saldo e resumo mensal diretamente pelo chat.
- [ ] Sistema de segurança que responde apenas ao ID do proprietário.
- [ ] Exportação de dados para CSV/Excel.

---

## 🏗️ Arquitetura do Projeto

O projeto segue princípios de **Clean Code** e separação de responsabilidades:

- `bot/`: Lógica de interface e comandos do Telegram.
- `core/`: Motor de processamento (Parser) que converte texto em objetos JSON.
- `db/`: Camada de persistência e modelos do banco de dados.

---

## 🔧 Como Rodar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/Carlos777-programmer/financeiro-bot-telegram.git](https://github.com/Carlos777-programmer/financeiro-bot-telegram.git)

2. **Instale as dependências**
  - `pip install -r requirements.txt`

3. **Configure as Variáveis de Ambiente**
  - Crie um arquivo `.env` na raiz do seu projeto com as seguintes chaves:
  - `TELEGRAM_TOKEN=seu_token_aqui`, `USER_ID=seu_id_telegram`

4. **Inicie o Bot**
  - `python main.py`

---

👤 Autor
Carlos Marques - Estudante de Engenharia de Computação (UNIVESP) | CNC Programmer



   
