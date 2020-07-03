import requests
from requests.exceptions import Timeout
import pyodbc
import queriesSQL as Query
import redis

"""Retorna email"""


def getEmails(codigo, tipo):
    conn = pyodbc.connect(Dsn="PW32", uid="BYTEC", pwd="BYTEC")
    emails = conn.cursor().execute(Query.emailporcodigo(codigo, tipo))
    lista_emails = []
    for enderecos in emails:
        endr = {"descricao": enderecos.descr.strip(), "endereco": enderecos.email_site.strip()}
        lista_emails.append(endr)
    conn.close()
    return lista_emails


'''Colecao de Clientes'''


def extratorcliente(listaclientes):
    tempcliente = {}
    lista_cliente = []
    for cliente in listaclientes:
        try:
            tempcliente = {"representante": cliente.REPRE, "zona": cliente.ZONA, "mercado": cliente.MERCADO.strip(),
                           "rota": cliente.ROTA.strip(), "status": cliente.ST.strip(),
                           "codigo": cliente.CODIGO,
                           "fantasia": cliente.FANTASIA.strip(), "razao_social": cliente.AEMPR_RAZAO_SOCIAL.strip(),
                           "endereco": {"rua": cliente.RUA.strip(), "numero": int(cliente.NUMERO),
                                        "complemento": cliente.COMPLEMENTO.strip(),
                                        "bairro": cliente.BAIRRO.strip(),
                                        "cidade": cliente.CIDADE.strip(), "cep": int(cliente.CEP),
                                        "uf": cliente.UF},
                           "telefones": {"fixo": cliente.TELEFONE.strip(), "celular_0": cliente.CELULAR_1.strip(),
                                         "celular_1": cliente.CELULAR_2.strip(),
                                         "celular_2": cliente.CELULAR_3.strip()},
                           "emails": getEmails(codigo=cliente.CODIGO, tipo="C"),
                           "credito": {"pedido": float(cliente.PEDIDO), "aberto": float(cliente.ABERTO),
                                       "vencido": float(cliente.VENCIDO),
                                       "limite": float(cliente.Credito)},
                           "ultimo_pedido": {"quantidade_caixas": int(cliente.NR_CX), "total": float(cliente.TOT_NOTA),
                                             "emissao":
                                                 (cliente.DT_EMISSAO[6:8] + "/" + cliente.DT_EMISSAO[
                                                                                  4:6] + "/" + cliente.DT_EMISSAO[0:4])},
                           "tabela_de_preco": {"prowater": cliente.TAB_PW, "proclean": cliente.TAB_PC,
                                               "prolimp": cliente.TAB_PL},
                           "condicao_de_pagamento": {"prowater": cliente.PGTOPW, "proclean": cliente.PGTOPC,
                                                     "prolimp": cliente.PGTOPL}}
        except:
            print('erro')
        lista_cliente.append(tempcliente)
    return lista_cliente


def clientes(**kwargs):
    clientes = kwargs.get("clientes")
    lista_clientes = None
    if clientes is None:
        conn = pyodbc.connect(
            Dsn="PW32", uid="BYTEC", pwd="BYTEC")
        for query in Query.clientes():
            lista_clientes = conn.cursor().execute(query)
        resultado = extratorcliente(lista_clientes)
        conn.close()
        return resultado
    elif isinstance(clientes, str):
        conn = pyodbc.connect(
            Dsn="PW32", uid="BYTEC", pwd="BYTEC")
        for query in Query.clienteporcodigo(clientes):
            lista_clientes = conn.cursor().execute(query)
        resultado = extratorcliente(lista_clientes)
        conn.close()
        return resultado
    elif isinstance(clientes, list):
        conn = pyodbc.connect(
            Dsn="PW32", uid="BYTEC", pwd="BYTEC")
        lista_clientes = []
        for query in Query.clienteporcodigo(0)[0:18]:
            conn.cursor().execute(query)
        for cliente in clientes:
            clientetemp = conn.cursor().execute(Query.clienteporcodigo(cliente)[-1])
            lista_clientes.append(extratorcliente(clientetemp))
        resultado = lista_clientes
        conn.close()
        return resultado
    else:
        raise ValueError


def tabelaprecos():
    conn = pyodbc.connect(
        Dsn="PW32", uid="BYTEC", pwd="BYTEC")
    tabela_preco = conn.cursor().execute(Query.tabelaprecos())
    lista_tabela_preco = []
    for item in tabela_preco:
        temp = {"empresa": item.emp, "codigo": item.cod, "valor": float(item.valor), "tabela": item.tabela}
        lista_tabela_preco.append(temp)
    conn.close()
    return lista_tabela_preco


def extratorcobranca(tabelacobrancas):
    lista_de_cobrancas = []
    for linha in tabelacobrancas:
        temp = {"representante": linha.REPR, "cliente": linha.CLI, "empresa": linha.EMP, "nota_fiscal": linha.NOTA,
                "pedido": linha.PED, "vencimento": linha.VCTO, "emissao": linha.EMISSAO, "parcela": linha.PARC,
                "valor": float(linha.VALOR)}
        lista_de_cobrancas.append(temp)
    return lista_de_cobrancas


def cobrancas():
    conn = pyodbc.connect(
        Dsn="PW32", uid="BYTEC", pwd="BYTEC")
    tabelacobrancas = conn.cursor().execute(Query.cobrancas())
    resultado = extratorcobranca(tabelacobrancas)
    conn.close()
    return resultado


def selecionaCobranca(**kwargs):
    cliente = kwargs.get("cliente")
    empresa = kwargs.get("empresa")
    pedido = kwargs.get("pedido")
    nota_fiscal = kwargs.get("nota_fiscal")
    conn = pyodbc.connect(
        Dsn="PW32", uid="BYTEC", pwd="BYTEC")
    tabelacobrancas = conn.cursor().execute(
        Query.cobrancasporargumentos(cliente=cliente, empresa=empresa, pedido=pedido, nota_fiscal=nota_fiscal))
    resultado = extratorcobranca(tabelacobrancas)
    conn.close()
    return resultado


def representantes():
    conn = pyodbc.connect(
        Dsn="PW32", uid="BYTEC", pwd="BYTEC")
    representantes = conn.cursor().execute(Query.representantes())
    lista_de_representantes = []
    for item in representantes:
        temp = {"codigo": item.COD, "razao_social": item.RAZAO, "fantasia": item.FANT,
                "email": getEmails(item.COD, tipo="R")}
        lista_de_representantes.append(temp)
    conn.close()
    return lista_de_representantes


def entregadivida():
    conn = pyodbc.connect(
        Dsn="PW32", uid="BYTEC", pwd="BYTEC")
    consultas = None
    for query in Query.entregadivida():
        consultas = conn.cursor().execute(query)
    lista_entrega = []
    for item in consultas:
        temp = {"representante": item.REPRE, "mercado": item.MERCADO.strip(), "rota": item.ROTA.strip(),
                "cliente": item.CLIENTE,
                "fantasia": item.FANTASIA.strip(), "data_cadastro": item.CADAST, "previsao": item.PREV,
                "empresa": item.EMPRESA,
                "pedido": item.PEDIDO, "caixas": int(item.CX), "peso": float(item.PESO), "vencimento": item.VENCIMENTO}
        lista_entrega.append(temp)
    conn.close()
    return lista_entrega


def notascanceladasemotivo():
    conn = pyodbc.connect(
        Dsn="PW32", uid="BYTEC", pwd="BYTEC")
    consultas = None
    for query in Query.notascanceladasemotivo():
        consultas = conn.cursor().execute(query)
    lista_notas_canceladas_e_motivo = []
    for item in consultas:
        temp = {"empresa": item.EMPRESA, "representante": item.REPRE, "rota": item.ROTA, "cliente": item.CLIENTE,
                "fantasia": item.FANTASIA, "nff": item.NFF, "data_emissao": item.DATA_EMISSAO, "total": float(item.TOT),
                "caixas": int(item.CX), "transporte": item.TRANSP, "nome_transporte": item.TRANSP_NOME,
                "motivo": item.MOTIVO}
        lista_notas_canceladas_e_motivo.append(temp)
    conn.close()
    return lista_notas_canceladas_e_motivo


def emissaodenotasfiscais():
    conn = pyodbc.connect(
        Dsn="PW32", uid="BYTEC", pwd="BYTEC")
    consultas = None
    for query in Query.emissaonotasfiscais():
        consultas = conn.cursor().execute(query)
    lista_notas_emitidas = []
    for item in consultas:
        temp = {"data": item.DATA, "trasnportes": item.TRANSP, "notas_fiscais": item.NR_NF,
                "notas_bonificadas": item.NR_NB, "notas_fiscais_caixas": int(item.CX_NF),
                "notas_bonificadas_caixas": int(item.CX_NB), "notas_fiscais_canceladas": (item.NR_NF_CAN),
                "notas_bonificadas_canceladas": (item.NR_NB_CAN),
                "notas_fiscais_canceladas_caixas": int(item.CX_NF_CAN),
                "notas_bonificadas_canceladas_caixas": int(item.CX_NB_CAN),
                "notas_fiscais_realizado": (item.NR_NF_REAL),
                "notas_bonificadas_realizado": (item.NR_NB_REAL),
                "notas_fiscais_caixas_realizado": int(item.REALIZADO_NF),
                "notas_bonificadas_caixas_realizado": int(item.REALIZADO_NB), "taxa_bonificacao": float(item.BNF)}
        lista_notas_emitidas.append(temp)
    conn.close()
    return lista_notas_emitidas


def producao():
    conn = pyodbc.connect(
        Dsn="PW32", uid="BYTEC", pwd="BYTEC")
    consultas = conn.cursor().execute(Query.producao())
    lista_producao = []
    for item in consultas:
        temp = {"numero_op": item.NUM_OP, "item": item.ITEM, "data_emissao": item.DT_EMISSAO, "status": item.ST,
                "a_fabricar": int(item.A_FABRICAR), "fabricado": int(item.FABRICADO), "diferenca": int(item.DIFERENCA),
                "efetuado": float(item.EFETUADO)}
        lista_producao.append(temp)
    conn.close()
    return lista_producao


def relatoriodecompras():
    conn = pyodbc.connect(
        Dsn="PW32", uid="BYTEC", pwd="BYTEC")
    consultas = None
    for query in Query.relatoriodecompas():
        consultas = conn.cursor().execute(query)
    lista_clientes = []
    for item in consultas:
        temp = {"representante": item.REPRE, "zona": item.ZONA.strip(), "rota": item.ROTA.strip(),
                "tempo_pedido": int(item.PED),
                "tempo_faturado": int(item.FAT), "data_faturamento": item.DT_FAT, "total_valor": float(item.VLR_NF),
                "total_caixas": int(item.NR_CX), "cobrancas": int(item.COB), "status": item.ST, "codigo": item.CODIGO,
                "fantasia": item.FANTASIA.strip(), "razao_social": item.RAZAO_SOCIAL.strip(), "cnpj_cpf": item.CNPJ_CPF,
                "email": item.EMAIL,
                "contato": item.CONTATO.strip(), "celular": item.CELULAR.strip(), "telefone": item.TELEFONE.strip(),
                "endereco": item.ENDERECO.strip(),
                "bairro": item.BAIRRO.strip(), "cidade": item.CIDADE.strip(), "cep": int(item.CEP), "uf": item.UF}
        lista_clientes.append(temp)
    conn.close()
    return lista_clientes


class Exportar:
    def geolocationAPI(self, respostas, cliente, session):
        endereco = f"{str(cliente['endereco']['numero'])}+{cliente['endereco']['rua'].strip().replace(' ', '+')},+{cliente['endereco']['cidade'].strip().replace(' ', '+')},+{cliente['endereco']['uf']}"
        endereco_b = f"{cliente['endereco']['numero']} {cliente['endereco']['rua'].strip()}, {cliente['endereco']['cidade'].strip()}, {cliente['endereco']['uf']}"
        key = "AIzaSyDGcf4b5BG9NNV__GQbzTdZ7QJAcOeMyRA"
        try:
            location = session.get(
                url=f"https://maps.googleapis.com/maps/api/geocode/json?address={endereco}&key={key}",
                timeout=(2, 2)).json()
        except Timeout:
            location = {"status": Timeout}

        respostas.append({"location": location,
                          "cliente": cliente, "endereco": endereco_b})

    def NogeolocationAPI(self, respostas, cliente):
        endereco_b = f"{cliente['endereco']['numero']} {cliente['endereco']['rua'].strip()}, {cliente['endereco']['cidade'].strip()}, {cliente['endereco']['uf']}"

        respostas.append({"cliente": cliente, "endereco": endereco_b})

    def clientes(self):
        sessison = requests.Session()
        sessison.auth = ("username", "password")
        file_path = "C:\\Teste\\locais.csv"
        file = open(file_path, "w")
        file.write("Latitude;Longitude;Address;ST;Name;Codigo;Rota\n")
        respostas = []
        conn = pyodbc.connect(
            Dsn="PW32", uid="BYTEC", pwd="BYTEC")
        listaClientes = clientes()
        conn.close()
        numero_de_clientes = len(listaClientes)
        i = 0
        print(f"Consulta resultou em {numero_de_clientes} resultados")
        for cliente in listaClientes:
            self.geolocationAPI(respostas, cliente, sessison)
            i += 1
            print(f'Cliente {i} de {numero_de_clientes}')
        print(f"Consulta de geolocalização terminada\n Iniciando escrita de arquivo em {file_path}")
        for x in respostas:
            if x["location"].get("status") == "OK":
                geolocation = str(
                    x.get("location").get("results")[0].get("geometry").get("location").get("lat")) + ";" + str(
                    x.get("location").get("results")[0].get("geometry").get("location").get("lng"))
                file.write(
                    f"{geolocation};"
                    f"{x['endereco']};"
                    f"{x['cliente']['status']};"
                    f"{x['cliente']['fantasia']};"
                    f"{x['cliente']['codigo']};"
                    f"{x['cliente']['rota']}\n")
            else:
                geolocation = str(0) + ";" + str(0)
                file.write(
                    f"{geolocation};"
                    f"{x['endereco']};"
                    f"{x['cliente']['status']};"
                    f"{x['cliente']['fantasia']};"
                    f"{x['cliente']['codigo']};"
                    f"{x['cliente']['rota']}\n")
        file.close()

    def clientes_nogeo(self):
        file_path = "C:\\Teste\\locais.csv"
        file = open(file_path, "w")
        file.write("Address;ST;Name;Codigo;Rota\n")
        respostas = []
        conn = pyodbc.connect(
            Dsn="PW32", uid="BYTEC", pwd="BYTEC")
        listaClientes = clientes()
        conn.close()
        numero_de_clientes = len(listaClientes)
        i = 0
        print(f"Consulta resultou em {numero_de_clientes} resultados")
        for cliente in listaClientes:
            self.NogeolocationAPI(respostas, cliente)
            i += 1
            print(f'Cliente {i} de {numero_de_clientes}')
        print(f"Iniciando escrita de arquivo em {file_path}")
        for x in respostas:
            file.write(
                f"{x['endereco']};"
                f"{x['cliente']['status']};"
                f"{x['cliente']['fantasia']};"
                f"{x['cliente']['codigo']};"
                f"{x['cliente']['rota']}\n")
        file.close()

    def cliente(self, codigo):
        sessison = requests.Session()
        sessison.auth = ("username", "password")
        file_path = f"C:\\Teste\\local{codigo}.csv"
        file = open(file_path, "w")
        file.write("Latitude;Longitude;Address;ST;Name;Codigo;Rota\n")
        respostas = []
        conn = pyodbc.connect(
            Dsn="PW32", uid="BYTEC", pwd="BYTEC")
        listaClientes = clientes(clientes=codigo)
        conn.close()
        numero_de_clientes = len(listaClientes)
        i = 0
        print(f"Consulta resultou em {numero_de_clientes} resultados")
        for cliente in listaClientes:
            self.geolocationAPI(respostas, cliente[0], sessison)
            i += 1
            print(f'Cliente {i} de {numero_de_clientes}')
        print(f"Consulta de geolocalização terminada\n Iniciando escrita de arquivo em {file_path}")
        for x in respostas:
            if x["location"].get("status") == "OK":
                geolocation = str(
                    x.get("location").get("results")[0].get("geometry").get("location").get("lat")) + ";" + str(
                    x.get("location").get("results")[0].get("geometry").get("location").get("lng"))
                file.write(
                    f"{geolocation};"
                    f"{x['endereco']};"
                    f"{x['cliente']['status']};"
                    f"{x['cliente']['fantasia']};"
                    f"{x['cliente']['codigo']};"
                    f"{x['cliente']['rota']}\n")
            else:
                geolocation = str(0) + ";" + str(0)
                file.write(
                    f"{geolocation};"
                    f"{x['endereco']};"
                    f"{x['cliente']['status']};"
                    f"{x['cliente']['fantasia']};"
                    f"{x['cliente']['codigo']};"
                    f"{x['cliente']['rota']}\n")
        file.close()
