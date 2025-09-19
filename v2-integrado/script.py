import requests
from bs4 import BeautifulSoup
import time

HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}

def buscar_produtos(produto, categoria="Tecnologia", max_paginas=1):
    produto_formatado = produto.replace(" ", "-")
    url_base = f"https://lista.mercadolivre.com.br/{produto_formatado}"

    for pagina in range(1, max_paginas + 1):
        url_final = f"{url_base}{pagina}_noindex_True"
        response = requests.get(url_final, headers=HEADER)
        print(f"Buscando {url_final} → Status: {response.status_code}")

        if response.status_code != 200:
            print("Erro ao acessar a página.")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        titulos = soup.find_all("a", class_="poly-component__title")
        precos = soup.find_all("span", class_="andes-money-amount andes-money-amount--cents-superscript")

        if not titulos or not precos:
            print("Nenhum resultado encontrado.")
            break

        for titulo, preco in zip(titulos, precos):
            nome = titulo.text.strip()
            link = titulo.get("href")
            preco_valor = preco.text.strip()
            print(f"Nome: {nome}")
            print(f"URL: {link}")
            print(f"Preço: {preco_valor}")
            print("-" * 40)

        time.sleep(2)  # espera 2 segundos entre páginas


# Exemplo de uso
buscar_produtos("creatina", categoria="Academia")
