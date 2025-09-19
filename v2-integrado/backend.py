from flask import Flask, jsonify
from flask_cors import CORS
import pika
import json

# Inicializa o app Flask e habilita CORS
app = Flask(__name__)
CORS(app, resources={r"/produto": {"origins": "*"}})

# Configuração da conexão com RabbitMQ
RABBITMQ_USER = 'admin'
RABBITMQ_PASS = 'admin'
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'academia_queue'

credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Função para consumir uma única mensagem da fila
def consumir_uma_mensagem():
    method_frame, header_frame, body = channel.basic_get(queue=QUEUE_NAME, auto_ack=True)
    if method_frame and body:
        try:
            return json.loads(body)
        except Exception as e:
            print(f"Erro ao decodificar JSON: {e}")
    return None

# Rota para retornar uma única mensagem
@app.route("/produto")
def listar_um_produto():
    produto = consumir_uma_mensagem()
    return jsonify(produto if produto else {})

# Executa o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
