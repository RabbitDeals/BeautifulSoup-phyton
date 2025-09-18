import requests
from bs4 import BeautifulSoup
import time

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
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
        preco_valor = preco.text.strip()
        print("nome:", nome)
        print("url-anuncio:", link)
        print("preco:", preco_valor)
        print("-" * 40)

    time.sleep(2)
    break  