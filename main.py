import json
import os
from datetime import datetime
from scraper import buscar_preco

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

    for produto in config["produtos"]:
        nome = produto["nome"]
        url = produto["url"]
        preco_alvo = produto["preco_alvo"]

        print(f"\n🔍 Buscando: {nome}")
        preco_atual = buscar_preco(url)

        if preco_atual is None:
            print("  ❌ Não foi possível obter o preço.")
            continue

        print(f"  💰 Preço atual: £{preco_atual}")
        print(f"  🎯 Preço alvo:  £{preco_alvo}")

        if preco_atual <= preco_alvo:
            print("  ✅ ALERTA: Preço abaixo do alvo!")
        else:
            print("  📈 Preço ainda acima do alvo.")

        # Salva no histórico
        if nome not in historico:
            historico[nome] = []

        historico[nome].append({
            "data": agora,
            "preco": preco_atual,
            "alvo": preco_alvo,
            "alerta": preco_atual <= preco_alvo
        })
    salvar_historico(historico)
    print("\n✅ Histórico salvo!")

    from reporter import gerar_relatorio
    gerar_relatorio(historico, config)

if __name__ == "__main__":
    monitorar()
