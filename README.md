# RabbitDeals Scraper Python

> **Este script foi autorizado pelo professor para ser em Python**. Ele atua como o produtor de mensagens, enviando produtos para o RabbitMQ, que são consumidos pelo Spring Boot (Consumidor 1) e outro consumidor Python (Consumidor 2 - Telegram).

## Integrantes

| Nome Completo                        | RA        |
|-------------------------------------|-----------|
| Alejandro Castor da Costa Fadim     | 01241115  |
| Felipe Ferreira Albertim           | 01241160  |

---

## Descrição do Projeto

Este script é o **Produtor Python** do RabbitDeals:

- **Função:** Busca produtos no Mercado Livre por categoria e palavra-chave, formata os dados e envia para a fila RabbitMQ.
- **Categorias:** Definidas em `categorias.py`.
- **Fila RabbitMQ:** Cada categoria possui sua própria fila, vinculada à exchange `categoria_exchange`.

---

## Configuração do RabbitMQ

O script envia mensagens para o RabbitMQ, que deve estar rodando localmente ou em outro host configurado.

- **Host:** localhost  
- **Exchange:** `categoria_exchange` (tipo `direct`)  
- **Credenciais:** admin / admin  
- **Filas:** Definidas no script, como `tecnologia_queue` e `academia_queue`.

> Certifique-se de que o RabbitMQ está ativo antes de rodar o script.

---

## Como Rodar o Script

1. **Instale as dependências**
```sh
pip install requests beautifulsoup4 pika
```

2. **Certifique-se de ter o RabbitMQ rodando** (local ou remoto).

3. **Execute o script**
```sh
python script-integrado.py
```

> O script executa em loop infinito, buscando produtos aleatórios por categoria e enviando para o RabbitMQ a cada 30 segundos.

---

## Estrutura das Mensagens Enviadas

Cada produto enviado para a exchange possui o seguinte JSON:

```json
{
    "titulo": "Halter Ajustável 20kg",
    "vendedorNome": "Loja Fitness Pro",
    "linkProduto": "https://www.exemplo.com.br/halter-ajustavel-20kg",
    "preco": 299.90,
    "avaliacao": 4.8,
    "imagens": "https://www.exemplo.com.br/images/halter1.jpg",
    "categoria": "Academia"
}
```

- **Routing Key:** corresponde à categoria do produto.

---

## Observações

- O script inclui delays de 10 segundos entre produtos e 30 segundos entre buscas de palavras-chave para evitar sobrecarga.
- As categorias e palavras-chave são definidas no arquivo `categorias.py`.
- Recomendado rodar em ambiente Python 3.10 ou superior.

