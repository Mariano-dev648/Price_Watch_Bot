from datetime import datetime

def gerar_relatorio(historico, config):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    produtos = config["produtos"]

    cards = ""
    graficos_js = ""

    for i, produto in enumerate(produtos):
        nome = produto["nome"]
        alvo = produto["preco_alvo"]
        registros = historico.get(nome, [])

        if not registros:
            continue

        ultimo = registros[-1]
        preco_atual = ultimo["preco"]
        alerta = ultimo["alerta"]

        cor = "#2ecc71" if alerta else "#e74c3c"
        status = "✅ Abaixo do alvo!" if alerta else "📈 Acima do alvo"

        historico_linhas = ""
        for r in registros[-5:]:
            historico_linhas += f"""
            <tr>
                <td>{r['data']}</td>
                <td>£{r['preco']}</td>
                <td>£{r['alvo']}</td>
                <td style="color: {'green' if r['alerta'] else 'red'}">
                    {'✅ Alerta' if r['alerta'] else '📈 Normal'}
                </td>
            </tr>"""

        # Dados para o gráfico
        labels = [r['data'] for r in registros]
        precos = [r['preco'] for r in registros]
        alvos = [r['alvo'] for r in registros]
        chart_id = f"chart_{i}"

        graficos_js += f"""
        new Chart(document.getElementById('{chart_id}'), {{
            type: 'line',
            data: {{
                labels: {labels},
                datasets: [
                    {{
                        label: 'Preço',
                        data: {precos},
                        borderColor: '#00d4ff',
                        backgroundColor: 'rgba(0,212,255,0.1)',
                        tension: 0.4,
                        fill: true,
                        pointRadius: 5,
                        pointBackgroundColor: '#00d4ff'
                    }},
                    {{
                        label: 'Alvo',
                        data: {alvos},
                        borderColor: '#2ecc71',
                        borderDash: [6, 3],
                        pointRadius: 0,
                        tension: 0
                    }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        labels: {{ color: '#ccc' }}
                    }}
                }},
                scales: {{
                    x: {{
                        ticks: {{ color: '#888', maxRotation: 45 }},
                        grid: {{ color: '#2a2a4a' }}
                    }},
                    y: {{
                        ticks: {{ color: '#888' }},
                        grid: {{ color: '#2a2a4a' }}
                    }}
                }}
            }}
        }});
        """

        cards += f"""
        <div class="card">
            <h2>{nome}</h2>
            <div class="preco" style="color: {cor}">£{preco_atual}</div>
            <div class="alvo">Preço alvo: £{alvo}</div>
            <div class="status" style="background: {cor}">{status}</div>
            <canvas id="{chart_id}" style="margin: 20px 0;"></canvas>
            <table>
                <thead>
                    <tr>
                        <th>Data</th>
                        <th>Preço</th>
                        <th>Alvo</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>{historico_linhas}</tbody>
            </table>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Price Watch Bot</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: #0f0f1a;
            color: #eee;
            padding: 30px;
        }}
        header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        header h1 {{
            font-size: 2.5rem;
            color: #00d4ff;
            letter-spacing: 2px;
        }}
        header p {{
            color: #888;
            margin-top: 8px;
        }}
        .container {{
            display: flex;
            flex-wrap: wrap;
            gap: 24px;
            justify-content: center;
        }}
        .card {{
            background: #1a1a2e;
            border-radius: 16px;
            padding: 28px;
            width: 520px;
            border: 1px solid #2a2a4a;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        }}
        .card h2 {{
            font-size: 1.2rem;
            margin-bottom: 16px;
            color: #ccc;
        }}
        .preco {{
            font-size: 2.8rem;
            font-weight: bold;
            margin-bottom: 6px;
        }}
        .alvo {{
            color: #888;
            margin-bottom: 14px;
            font-size: 0.95rem;
        }}
        .status {{
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: bold;
            color: white;
            margin-bottom: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
        }}
        th {{
            background: #0f0f1a;
            padding: 8px;
            text-align: left;
            color: #00d4ff;
            border-bottom: 1px solid #2a2a4a;
        }}
        td {{
            padding: 8px;
            border-bottom: 1px solid #1e1e3a;
            color: #ccc;
        }}
        footer {{
            text-align: center;
            margin-top: 50px;
            color: #444;
            font-size: 0.85rem;
        }}
    </style>
</head>
<body>
    <header>
        <h1> Price Watch Bot</h1>
        <p>Última atualização: {agora}</p>
    </header>
    <div class="container">
        {cards}
    </div>
    <footer>
        <p>Gerado automaticamente por Price Watch Bot • Python + BeautifulSoup</p>
    </footer>
    <script>
        {graficos_js}
    </script>
</body>
</html>"""

    with open("relatorio.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Relatório HTML gerado: relatorio.html")