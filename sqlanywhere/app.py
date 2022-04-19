import ast
from datetime import datetime

import flask.json as json
import pymongo
from flask import Flask, request, session, render_template, url_for, redirect

from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

import queriesSQL
import sqlanywhere
from flask_session import Session

import gspread
from google.oauth2 import service_account
import sqlanywhere as Prowater
import pyodbc
from cryptography.fernet import Fernet
from user import Usuario

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
# spreadsheet_id = "1l7KkeMx7rOLYqU1TnXZikuzbQHvN4SJSKiJH3BMQx2c"
spreadsheet_id = "1ITKWGDsDiqNl7NrRzYRqYlZHu6LzGYJJNmANyQgrZrw"
sheet_id = "0"
json_file = "prowater-177d3-e29737f9229f.json"


def login_sheets():
    credentials = service_account.Credentials.from_service_account_file(json_file)
    scoped_credentials = credentials.with_scopes(scopes)
    gc = gspread.authorize(scoped_credentials)
    return gc


def escritor(lista):
    representante = lista[0]
    cliente = lista[1]
    data_entrega = lista[2]
    forma_pagamento = ''
    for pagamento in lista[3]:
        if pagamento is not None:
            forma_pagamento += pagamento + '/'
    forma_pagamento = forma_pagamento[:-1]
    total_caixas = total = sd1k_valor = sd1k = sd40_valor = sd40 = lamo_valor = lamo = affe_valor = affe = 0
    sens_valor = sens = esp4_valor = esp4 = esp3_valor = esp3 = esp_valor = esp1 = cb2_valor = cb2 = cb1_valor = cb1 = 0
    ab2_valor = ab2 = ab1_valor = ab1 = at5_valor = at5 = at2_valor = at2 = at1_valor = at1 = ct5_valor = ct5 = 0
    ct2_valor = ct2 = cti_valor = ct1 = 0
    for produto in lista[4]:
        ct1 += produto['quantidade'] if produto['codigo'] == '011009' else 0
        cti_valor += produto['pedido'] if produto['codigo'] == '011009' else 0
        ct2 += produto['quantidade'] if produto['codigo'] == '011001' else 0
        ct2_valor += produto['pedido'] if produto['codigo'] == '011001' else 0
        ct5 += produto['quantidade'] if produto['codigo'] == '011005' else 0
        ct5_valor += produto['pedido'] if produto['codigo'] == '011005' else 0
        at1 += produto['quantidade'] if produto['codigo'] == '021002' else 0
        at1_valor += produto['pedido'] if produto['codigo'] == '021002' else 0
        at2 += produto['quantidade'] if produto['codigo'] == '021006' else 0
        at2_valor += produto['pedido'] if produto['codigo'] == '021006' else 0
        at5 += produto['quantidade'] if produto['codigo'] == '021007' else 0
        at5_valor += produto['pedido'] if produto['codigo'] == '021007' else 0
        ab1 += produto['quantidade'] if produto['codigo'] == '022004' else 0
        ab1_valor += produto['pedido'] if produto['codigo'] == '022004' else 0
        ab2 += produto['quantidade'] if produto['codigo'] == '022008' else 0
        ab2_valor += produto['pedido'] if produto['codigo'] == '022008' else 0
        cb1 += produto['quantidade'] if produto['codigo'] == '012010' else 0
        cb1_valor += produto['pedido'] if produto['codigo'] == '012010' else 0
        cb2 += produto['quantidade'] if produto['codigo'] == '012003' else 0
        cb2_valor += produto['pedido'] if produto['codigo'] == '012003' else 0
        esp1 += produto['quantidade'] if produto['codigo'] == '031011' else 0
        esp_valor += produto['pedido'] if produto['codigo'] == '031011' else 0
        esp3 += produto['quantidade'] if produto['codigo'] == '031014' else 0
        esp3_valor += produto['pedido'] if produto['codigo'] == '031014' else 0
        esp4 += produto['quantidade'] if produto['codigo'] == '031013' else 0
        esp4_valor += produto['pedido'] if produto['codigo'] == '031013' else 0
        sens += produto['quantidade'] if produto['codigo'] == '041017' else 0
        sens_valor += produto['pedido'] if produto['codigo'] == '041017' else 0
        affe += produto['quantidade'] if produto['codigo'] == '042020' else 0
        affe_valor += produto['pedido'] if produto['codigo'] == '042020' else 0
        lamo += produto['quantidade'] if produto['codigo'] == '043018' else 0
        lamo_valor += produto['pedido'] if produto['codigo'] == '043018' else 0
        sd40 += produto['quantidade'] if produto['codigo'] == '051021' else 0
        sd40_valor += produto['pedido'] if produto['codigo'] == '051021' else 0
        sd1k += produto['quantidade'] if produto['codigo'] == '051022' else 0
        sd1k_valor += produto['pedido'] if produto['codigo'] == '051022' else 0
        total += produto['pedido'] * produto['quantidade']
        total_caixas += produto['quantidade']
    agora = f"{datetime.now().day}/{datetime.now().month}/{datetime.now().year} " \
            f"{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}"
    observacoes = lista[5]
    conn = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
    mongo_client = pymongo.MongoClient(conn)
    rep_cod = '0' * (5 - len(representante)) + representante
    cliente_cod = '0' * (5 - len(cliente)) + cliente
    representante_nome = mongo_client.get_database("prowater").get_collection("relatorio_de_compras").find_one(
        {"representante": rep_cod})['representante_nome']
    fantasia_cliente = mongo_client.get_database("prowater").get_collection("relatorio_de_compras").find_one(
        {"cliente": cliente_cod})['fantasia']
    # print(f"{rep_cod} : {cliente_cod} : {representante_nome} : {fantasia_cliente}")
    linha = [agora, f"({representante})" + representante_nome, cliente, data_entrega,
             forma_pagamento, '', '', '', ct1, cti_valor, ct2, ct2_valor, ct5, ct5_valor, at1, at1_valor,
             at2, at2_valor, at5, at5_valor, '', ab1, ab1_valor, ab2, ab2_valor, cb1, cb1_valor, cb2, cb2_valor, '',
             esp1, esp_valor, esp3, esp3_valor, esp4, esp4_valor, '', sens, sens_valor, affe, affe_valor,
             lamo, lamo_valor, '', sd40, sd40_valor, sd1k, sd1k_valor, '', fantasia_cliente,
             '', '', '', total, '', '', '', observacoes, '', '']
    gc = login_sheets()

    planilha = gc.open_by_key(spreadsheet_id)
    planilha = planilha.get_worksheet_by_id(865878295)
    planilha.insert_row(linha, len(planilha.get_values()) + 1, value_input_option='USER_ENTERED')


@app.route('/', methods=["GET", "POST"])
def home():
    erro = False
    if request.method == 'POST':
        codigo = request.form.get("codigo")
        codigo = '0' * (5 - len(codigo)) + codigo
        cnpj_cpf = request.form.get("cnpj_cpf")
        lembrar = request.form.get("lembrar")
        usuario = Usuario(codigo=codigo, cnpj_cpf=cnpj_cpf)
        if usuario.info:
            login_user(usuario, lembrar)
            return redirect(url_for("perfil"))
        else:
            erro = True
    return render_template("login.html", title="Home", erro=erro)


@login_manager.user_loader
def load_user(user_id):
    return Usuario(codigo=None, cnpj_cpf=user_id)


@app.route('/perfil', methods=["GET", "POST"])
@login_required
def perfil():
    if request.method == "POST":
        if request.form.get('sair'):
            logout_user()
            return redirect('/')
        elif request.form.get('pedido'):
            cli = (request.form.get('pedido'))
            repre = (current_user.info.get("AEMPR_CODIGO"))
            return redirect(url_for('painel', cli=cli, repre=repre))
    nome = current_user.info.get("AEMPR_NOME_ABREV")
    qtd_pedidos = current_user.qtd_pedidos
    vlr_pedidos = current_user.vlr_pedidos
    qtd_clientes = current_user.qtd_clientes
    conn = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
    mongo_client = pymongo.MongoClient(conn)
    clientes = mongo_client.get_database("prowater").get_collection("relatorio_de_compras").find(
        {"supervisores": current_user.info.get('AEMPR_CODIGO')})
    # print(clientes.count())
    lista_clientes = list(clientes)
    lista_clientes_sem_ataque = [r for r in lista_clientes if r.get('ataque') is None]
    lista_clientes = [r for r in lista_clientes if r.get('ataque') is not None]
    lista_clientes = [r for r in lista_clientes if datetime.strptime(r.get('ataque'), '%Y/%m/%d') <= datetime.now()]
    lista_clientes = sorted(lista_clientes, key=lambda k: k['ataque'], reverse=True)
    lista_clientes += lista_clientes_sem_ataque
    return render_template("perfil.html", nome=nome, qtd_pedidos=qtd_pedidos, vlr_pedidos=vlr_pedidos,
                           qtd_clientes=qtd_clientes, clientes=lista_clientes)


@app.route('/cliente', methods=["GET", "POST"])
def cliente():
    clientepost = request.form.get("cliente")
    return json.jsonify(Prowater.clientes(clientes=clientepost))


@app.route('/clientes', methods=["GET", "POST"])
def clientes():
    representante = request.form.get("representante")
    representante = '0' * (5 - len(representante)) + representante
    return json.jsonify(Prowater.clientes_repre(repre=representante))


@app.route('/tabela_preco', methods=["GET", "POST"])
def tabela_preco():
    return json.jsonify(Prowater.tabelaprecos())


@app.route('/tabela_preco_final', methods=["GET", "POST"])
def tabela_preco_final():
    return json.jsonify(Prowater.tabelaprecosfinal())


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


@app.route('/pedidosabertos', methods=["GET", "POST"])
def pedidosabertos():
    return json.jsonify(Prowater.pedidosabertos())


@app.route('/pedidoscadastrados', methods=["GET", "POST"])
def pedidosfaturados():
    return json.jsonify(Prowater.itenspedidos())


@app.route('/notasfaturadas', methods=["GET", "POST"])
def notasfaturadas():
    return json.jsonify(Prowater.itemsnotasfaturadas())


@app.route('/vendedores', methods=["GET", "POST"])
def vendedores():
    '''conn = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
    mongo_client = pymongo.MongoClient(conn)
    mongo_client.get_database("prowater").get_collection("relatorio_de_compras").find_one({"cliente": "12430"})'''
    return render_template("login.html", title="boa")


@app.route('/historico_cliente', methods=["GET", "POST"])
def historico_cliente():
    cliente = request.form['cliente']
    representante = request.form['representante']
    cnpj_cpf = request.form['cnpj_cpf']
    cliente = '0' * (5 - len(cliente)) + cliente
    representante = '0' * (5 - len(representante)) + representante
    res = Prowater.relatorio_cliente(cli=cliente, repre=representante, cnpj_cpf=cnpj_cpf, top=6)
    return json.jsonify(res)


@app.route('/painel', methods=["GET", "POST"])
def painel():
    def tabelaprecos():
        conn_mg = ("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&"
                   "directConnection=true&ssl=false")
        mongo_client = pymongo.MongoClient(conn_mg)
        tabela_base = mongo_client.get_database("prowater").get_collection("tabela_precos").find()
        lista_tabela_preco = list(tabela_base)
        if len(lista_tabela_preco) == 0:
            conn = pyodbc.connect(Dsn="PW64", uid="BYTEC", pwd="BYTEC")
            Prowater.atualiza_tabela4(conn=conn, mongo_client=mongo_client)
        return lista_tabela_preco

    tabela = tabelaprecos()
    return render_template("painel.html", title="Painel", cli=request.args.get('cli'), repre=request.args.get('repre'),
                           produtos=[
                               {"id": 1, "descricao": "CT-1",
                                "valor": [item for item in tabela if item['codigo'] == '011009'][0]['valor'],
                                "codigo": '011009'},
                               {"id": 2, "descricao": "CT-2",
                                "valor": [item for item in tabela if item['codigo'] == '011001'][0]['valor'],
                                "codigo": '011001'},
                               {"id": 3, "descricao": "CT-5",
                                "valor": [item for item in tabela if item['codigo'] == '011005'][0]['valor'],
                                "codigo": '011005'},
                               {"id": 4, "descricao": "CB-1",
                                "valor": [item for item in tabela if item['codigo'] == '012010'][0]['valor'],
                                "codigo": '012010'},
                               {"id": 5, "descricao": "CB-2",
                                "valor": [item for item in tabela if item['codigo'] == '012003'][0]['valor'],
                                "codigo": '012003'},
                               {"id": 6, "descricao": "AT-1",
                                "valor": [item for item in tabela if item['codigo'] == '021002'][0]['valor'],
                                "codigo": '021002'},
                               {"id": 7, "descricao": "AT-2",
                                "valor": [item for item in tabela if item['codigo'] == '021006'][0]['valor'],
                                "codigo": '021006'},
                               {"id": 8, "descricao": "AT-5",
                                "valor": [item for item in tabela if item['codigo'] == '021007'][0]['valor'],
                                "codigo": '021007'},
                               {"id": 9, "descricao": "AB-1",
                                "valor": [item for item in tabela if item['codigo'] == '022004'][0]['valor'],
                                "codigo": '022004'},
                               {"id": 10, "descricao": "AB-2",
                                "valor": [item for item in tabela if item['codigo'] == '022008'][0]['valor'],
                                "codigo": '022008'},
                               {"id": 11, "descricao": "ESP-1",
                                "valor": [item for item in tabela if item['codigo'] == '031011'][0]['valor'],
                                "codigo": '031011'},
                               {"id": 12, "descricao": "ESP-3",
                                "valor": [item for item in tabela if item['codigo'] == '031014'][0]['valor'],
                                "codigo": '031014'},
                               {"id": 13, "descricao": "ESP-DISP",
                                "valor": [item for item in tabela if item['codigo'] == '031013'][0]['valor'],
                                "codigo": '031013'},
                               {"id": 14, "descricao": "SENS",
                                "valor": [item for item in tabela if item['codigo'] == '041017'][0]['valor'],
                                "codigo": '041017'},
                               {"id": 15, "descricao": "LAMO",
                                "valor": [item for item in tabela if item['codigo'] == '042020'][0]['valor'],
                                "codigo": '042020'},
                               {"id": 16, "descricao": "AFEC",
                                "valor": [item for item in tabela if item['codigo'] == '043018'][0]['valor'],
                                "codigo": '043018'},
                               {"id": 17, "descricao": "SD-400G",
                                "valor": [item for item in tabela if item['codigo'] == '051021'][0]['valor'],
                                "codigo": '051021'},
                               {"id": 18, "descricao": "SD-1KG",
                                "valor": [item for item in tabela if item['codigo'] == '051022'][0]['valor'],
                                "codigo": '051022'}
                           ])


@app.route('/resumo', methods=["GET", "POST"])
def resumo():
    x = json.jsonify(request.form)
    produtos = None
    cliente = request.form.getlist('cliente')[0]
    representante = request.form.getlist('representante')[0]
    data_entrega = request.form.getlist('data_entrega')[0]
    observcoes = f"Via web: {request.form.getlist('observacoes')[0]}"
    forma_de_pagamento = None
    try:
        produtos = []
        numero_items = int(request.form.getlist('numero')[0])
        for i in range(numero_items):
            produtos.append({'descricao': request.form.getlist(f'items[{i}][descricao]')[0],
                             'valor': float(request.form.getlist(f'items[{i}][valor]')[0]),
                             'codigo': request.form.getlist(f'items[{i}][codigo]')[0],
                             'quantidade': int(request.form.getlist(f'items[{i}][quantidade]')[0]),
                             'pedido': float(request.form.getlist(f'items[{i}][pedido]')[0]),
                             'id': request.form.getlist(f'items[{i}][id]')[0]})
        pag0 = 'À vista' if request.form.getlist('pagamento[pag0]')[0] != 'false' else None
        pag7 = '7' if request.form.getlist('pagamento[pag7]')[0] != 'false' else None
        pag14 = '14' if request.form.getlist('pagamento[pag14]')[0] != 'false' else None
        pag21 = '21' if request.form.getlist('pagamento[pag21]')[0] != 'false' else None
        pag28 = '28' if request.form.getlist('pagamento[pag28]')[0] != 'false' else None
        pag35 = '35' if request.form.getlist('pagamento[pag35]')[0] != 'false' else None
        forma_de_pagamento = [pag0, pag7, pag14, pag21, pag28, pag35]

        return {"res": 200}
    except:
        return {"res": "Produtos não enviados"}
    finally:
        escritor([representante, cliente, data_entrega, forma_de_pagamento, produtos, observcoes])


@app.route('/update', methods=["GET", "POST"])
def update():
    global res, update_info
    if request.method == "POST":
        key = open("key.key", "rb").read()
        fk = Fernet(key)
        # print(fk.decrypt(request.data).decode('utf-8'))
        res = json.loads(fk.decrypt(request.data).decode('utf-8').replace('\'', '\"'))
        conn_mg = ("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&"
                   "directConnection=true&ssl=false")
        mongo_client = pymongo.MongoClient(conn_mg)
        collection = res.get('collection')
        if collection == 'relatorio_de_compras':
            mongo_client.get_database("prowater").get_collection(collection).update_one(
                {"cliente": res.get('data').get('cliente')}, {"$set": res.get('data')}, upsert=True)
        elif collection == 'representantes':
            for repre in res.get('data'):
                mongo_client.get_database("prowater").get_collection(collection).update_one(
                    {"AEMPR_CODIGO": repre.get('AEMPR_CODIGO')},
                    {"$set": repre},
                    upsert=True)
        elif collection == 'tabela_precos':
            produto = res.get('data')
            mongo_client.get_database("prowater").get_collection(collection).update_one(
                {"codigo": produto.get('codigo')},
                {"$set": produto},
                upsert=True)
    return res


@app.route('/admin', methods=["GET", "POST"])
def admin():
    conn_mg = ("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&"
               "directConnection=true&ssl=false")
    mongo_client = pymongo.MongoClient(conn_mg)
    conn = pyodbc.connect(Dsn="PW64", uid="BYTEC", pwd="BYTEC")
    Prowater.atualiza_tabela4(conn=conn, mongo_client=mongo_client)
    return render_template("admin.html", tittle="Admin")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
