import requests
from bs4 import BeautifulSoup
import time
import pika
import json
from datetime import datetime

# Configurações RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost", 5672))
channel = connection.channel()

# Declara as duas filas (caso não existam ainda)
channel.queue_declare(queue="produtos_populares")
channel.queue_declare(queue="produtos_premium")

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0 Safari/537.36"
}

categoria = "Tecnologia"
# categoria = "Academia"

produto = "creatina"
produto = produto.replace(" ", "-")

url = f"https://lista.mercadolivre.com.br/{produto}"

start = 1

while True:
    url_final = url + str(start) + "_noindex_True"

    r = requests.get(url_final, headers=header)
    print(r)

    site = BeautifulSoup(r.text, "html.parser")

    titulos = site.find_all("a", class_="poly-component__title")
    precos = site.find_all("span", class_="andes-money-amount andes-money-amount--cents-superscript")

    if not titulos or not precos:
        print("Nenhum resultado encontrado.")
        break

    for titulo, preco in zip(titulos, precos):
        nome = titulo.text.strip()
        link = titulo.get("href")
        preco_valor = preco.text.strip().replace("R$", "").replace(".", "").replace(",", ".").strip()

        try:
            preco_float = float(preco_valor)
        except:
            preco_float = 0.0

        # Monta JSON do produto
        produto_json = {
            "nome": nome,
            "link": link,
            "preco": preco_float,
            "categoria": categoria,
            "fonte": "mercadolivre",
            "data_coleta": datetime.utcnow().isoformat() + "Z"
        }

        # Regras de classificação
        if preco_float >= 200:  # Exemplo: produtos acima de 200 vão para "premium"
            queue = "produtos_premium"
            produto_json["tipo"] = "premium"
        else:
            queue = "produtos_populares"
            produto_json["tipo"] = "popular"

        # Envia para fila correta
        channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(produto_json, ensure_ascii=False)
        )

        print(f"[x] Produto enviado para a fila {queue} -> {produto_json}")

    time.sleep(2)
    break

# Fecha conexão
connection.close()
