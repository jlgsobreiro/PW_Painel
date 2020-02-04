import flask.json as json
from flask import Flask
from flask_cors import CORS
from sqlanywhere import Cliente, TabelaPreco, Cobrancas

app = Flask(__name__)
CORS(app)


@app.route('/cliente', methods=["GET", "POST"])
def cliente():
    return json.jsonify(Cliente().info())


@app.route('/tabela_preco', methods=["GET", "POST"])
def tabela_preco():
    return json.jsonify(TabelaPreco().tabela())


@app.route('/cobrancas', methods=["GET", "POST"])
def cobrancas():
    return json.jsonify(Cobrancas().cobrancas())


if __name__ == '__main__':
    app.run()
