import requests
from bs4 import BeautifulSoup
import time
import pika
import json
from datetime import datetime
from categorias import CATEGORIAS
import random

# ----------------------------
# Configurações RabbitMQ
# ----------------------------
RABBIT_HOST = "localhost"
EXCHANGE = "categoria_exchange"

credentials = pika.PlainCredentials('admin', 'admin')
parameters = pika.ConnectionParameters(host=RABBIT_HOST, credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

# Declara exchange tipo direct
channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct', durable=True)

# Declara filas e bindings (se ainda não existirem)
filas = {
    "Tecnologia": "tecnologia_queue",
    "Academia": "academia_queue"
}

for routing_key, queue_name in filas.items():
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=routing_key)

# ----------------------------
# Configurações Scraper
# ----------------------------
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}

def buscar_produtos(produto, categoria="Tecnologia", max_paginas=1):
    produto_formatado = produto.replace(" ", "-")
    url_base = f"https://lista.mercadolivre.com.br/{produto_formatado}"

    for pagina in range(1, max_paginas + 1):
        url_final = f"{url_base}{pagina}_noindex_True"
        response = requests.get(url_final, headers=HEADERS)
        print(f"Buscando {url_final} → Status: {response.status_code}")

        if response.status_code != 200:
            print("Erro ao acessar a página.")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        titulos = soup.find_all("a", class_="poly-component__title")
        precos = soup.find_all("span", class_="andes-money-amount andes-money-amount--cents-superscript")
        imagens = soup.find_all("img", class_="poly-component__picture")
        estrelas = soup.find_all("span", class_="andes-visually-hidden")
        frete = soup.find_all("div", class_="poly-component__shipping")
        nomeVendedor = soup.find_all("span", class_="poly-component__seller")

        if not titulos or not precos or not imagens:
            print("Nenhum resultado encontrado.")
            break

        titulo = titulos[0]
        preco = precos[0]
        imagem = imagens[0]
        nome = titulo.text.strip()
        link = titulo.get("href")
        preco_valor = preco.text.strip().replace("R$", "").replace(".", "").replace(",", ".").strip()
        img_url = imagem.get("data-src") or imagem.get("src") or ""
        vendedor = nomeVendedor[0].text.strip() if nomeVendedor else "Vendedor não informado"
        estrela = estrelas[0].text.strip() if estrelas else "Sem avaliação"
        fretes = frete[0].text.strip() if frete else "Frete não informado"

        try:
            preco_float = float(preco_valor)
        except:
            preco_float = 0.0

        produto_json = {
            "titulo": nome,
            "vendedorNome": vendedor,
            "linkProduto": link,
            "preco": preco_float,
            "avaliacao": estrela,
            "imagens": img_url,
            "categoria": categoria
        }

        routing_key = categoria

        # Envia para exchange
        channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=routing_key,
            body=json.dumps(produto_json, ensure_ascii=False)
        )

        print(f"[x] Produto enviado -> {produto_json}")

        time.sleep(10)

# ----------------------------
# Execução
# ----------------------------
if __name__ == "__main__":
    while True:
        categoria_escolhida = random.choice(list(CATEGORIAS.keys()))

        produto_escolhido = random.choice(CATEGORIAS[categoria_escolhida])

        print(f"\n🔎 Categoria sorteada: {categoria_escolhida}")
        print(f"🔑 Palavra-chave sorteada: {produto_escolhido}\n")

        buscar_produtos(produto_escolhido, categoria=categoria_escolhida, max_paginas=1)

        print("Aguardando 30 segundos para buscar novo produto...")
        time.sleep(30)








