import json
import os
from datetime import datetime
from scraper import buscar_preco
from rich.console import Console
from rich.table import Table
from rich import print as rprint

console = Console()

ARQUIVO_HISTORICO = "historico.json"
ARQUIVO_CONFIG = "config.json"

def carregar_config():
    with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)

def carregar_historico():
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_historico(historico):
    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

def monitorar():
    config = carregar_config()
    historico = carregar_historico()
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")

    console.rule("[bold cyan]🤖 Price Watch Bot[/bold cyan]")
    console.print(f"\n[dim]Monitoramento iniciado em {agora}[/dim]\n")

    tabela = Table(show_header=True, header_style="bold cyan")
    tabela.add_column("Produto", style="white", width=30)
    tabela.add_column("Preço Atual", justify="right")
    tabela.add_column("Preço Alvo", justify="right")
    tabela.add_column("Status", justify="center")

    for produto in config["produtos"]:
        nome = produto["nome"]
        url = produto["url"]
        preco_alvo = produto["preco_alvo"]

        console.print(f"[dim]🔍 Buscando {nome}...[/dim]")
        preco_atual = buscar_preco(url)

        if preco_atual is None:
            tabela.add_row(nome, "[red]Erro[/red]", f"£{preco_alvo}", "[red]❌ Falha[/red]")
            continue

        alerta = preco_atual <= preco_alvo
        if alerta:
            status = "[bold green]✅ Abaixo do alvo![/bold green]"
            preco_str = f"[bold green]£{preco_atual}[/bold green]"
            from notificador import enviar_alerta
            enviar_alerta(nome, preco_atual, preco_alvo, url)
        else:
            status = "[red]📈 Acima do alvo[/red]"
            preco_str = f"[red]£{preco_atual}[/red]"

        tabela.add_row(nome, preco_str, f"£{preco_alvo}", status)

        if nome not in historico:
            historico[nome] = []

        historico[nome].append({
            "data": agora,
            "preco": preco_atual,
            "alvo": preco_alvo,
            "alerta": alerta
        })

    console.print(tabela)

    salvar_historico(historico)
    console.print("\n[bold green]✅ Histórico salvo![/bold green]")

    from reporter import gerar_relatorio
    gerar_relatorio(historico, config)

if __name__ == "__main__":
    monitorar()
