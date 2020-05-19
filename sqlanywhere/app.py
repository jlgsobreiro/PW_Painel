import flask.json as json
from flask import Flask, request
from flask_cors import CORS
import sqlanywhere as Prowater

app = Flask(__name__)
CORS(app)


@app.route('/', methods=["GET", "POST"])
def home():
    return "Olá"


@app.route('/cliente', methods=["GET", "POST"])
def cliente():
    clientepost = request.form.get("cliente")
    return json.jsonify(Prowater.clientes(clientes=clientepost))


@app.route('/tabela_preco', methods=["GET", "POST"])
def tabela_preco():
    return json.jsonify(Prowater.tabelaprecos())


@app.route('/cobrancas', methods=["GET", "POST"])
def cobrancas():
    return json.jsonify(Prowater.cobrancas())


@app.route('/cobrancaporargumento', methods=["GET", "POST"])
def cobrancaporargumento():
    cliente = request.get_data("cliente")
    empresa = request.args.get("empresa")
    pedido = request.args.get("pedido")
    nota_fiscal = request.args.get("nota_fiscal")
    return json.jsonify(Prowater.selecionaCobranca(
        cliente=cliente, empresa=empresa, pedido=pedido, nota_fiscal=nota_fiscal))


@app.route('/producao', methods=["GET", "POST"])
def producao():
    return json.jsonify(Prowater.producao())


@app.route('/notascanceladas', methods=["GET", "POST"])
def notascanceladas():
    return json.jsonify(Prowater.notascanceladasemotivo())


@app.route('/entregadivida', methods=["GET", "POST"])
def entregadivida():
    return json.jsonify(Prowater.entregadivida())


@app.route('/representantes', methods=["GET", "POST"])
def representantes():
    return json.jsonify(Prowater.representantes())


@app.route('/emissaonotas', methods=["GET", "POST"])
def emissaonotas():
    return json.jsonify(Prowater.emissaodenotasfiscais())


@app.route('/relatoriodecompras', methods=["GET", "POST"])
def relatoriodecompras():
    return json.jsonify(Prowater.relatoriodecompras())


if __name__ == '__main__':
    app.run()
