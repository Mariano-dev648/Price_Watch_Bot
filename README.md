# Price Watch Bot

Bot em Python que monitora preços de produtos automaticamente, envia alertas por e-mail e gera relatórios visuais em HTML.

<img width="1894" height="944" alt="image" src="https://github.com/user-attachments/assets/4052c2db-ccd4-4ec6-b9d6-195d4e0a98a1" />


## Funcionalidades

-  Monitora preços de múltiplos produtos simultaneamente
-  Gera relatório visual em HTML com gráfico de histórico
-  Envia alerta por e-mail quando o preço atinge o valor desejado
-  Salva histórico completo de preços em JSON
-  Interface no terminal com tabelas coloridas

## Tecnologias utilizadas

- Python 3
- Requests & BeautifulSoup4 — web scraping
- Rich — interface no terminal
- Chart.js — gráficos no relatório HTML
- SMTP — envio de e-mail
- python-dotenv — variáveis de ambiente

##  Estrutura do projeto
```
price-watch-bot/
├── main.py          # Arquivo principal
├── scraper.py       # Coleta preços da web
├── reporter.py      # Gera relatório HTML
├── notificador.py   # Envia alertas por e-mail
├── config.json      # Produtos monitorados
├── .env             # Credenciais (não sobe pro GitHub)
└── relatorio.html   # Relatório gerado automaticamente
```

## ▶️ Como usar

**1. Clone o repositório**
```
git clone [[https://github.com/Mariano-dev648/Price_Watch_Bot]
cd price_watch_bot
```

**2. Instale as dependências**
```
pip install requests beautifulsoup4 rich python-dotenv
```

**3. Configure o arquivo `.env`**
```
EMAIL_REMETENTE=seugmail@gmail.com
EMAIL_SENHA=sua_senha_de_app
EMAIL_DESTINATARIO=seugmail@gmail.com
```

> Para gerar a senha de app do Gmail acesse: https://myaccount.google.com/apppasswords

**4. Configure os produtos em `config.json`**
```json
{
  "produtos": [
    {
      "nome": "Nome do produto",
      "url": "URL do produto",
      "preco_alvo": 50.00
    }
  ]
}
```

**5. Execute o bot**
```
python main.py
```

**6. Abra o relatório gerado**
```
start relatorio.html
```

## Autor

Feito por [Mariano Lemos]([https://github.com/SEU_USUARIO](https://github.com/Mariano-dev648))
