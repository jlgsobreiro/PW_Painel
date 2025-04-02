import json
from datetime import datetime, timedelta

from bson import json_util
from bson.json_util import loads, dumps
import requests
from requests.exceptions import Timeout
import pyodbc
import aioodbc
import queriesSQL as Query
import pymongo

"""Retorna email"""


def getEmails(codigo: any, tipo: str):
    conn = pyodbc.connect(Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    emails = conn.cursor().execute(Query.emailporcodigo(codigo, tipo))
    lista_emails = []
    for enderecos in emails:
        endr = {"descricao": enderecos.descr.strip(), "endereco": enderecos.email_site.strip()}
        lista_emails.append(endr)
    conn.close()
    return lista_emails

async def async_getEmails(codigo: any, tipo: str):
    conn = await aioodbc.connect(dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    emails = await conn.cursor().execute(Query.emailporcodigo(codigo, tipo))
    lista_emails = []
    for enderecos in emails:
        endr = {"descricao": enderecos.descr.strip(), "endereco": enderecos.email_site.strip()}
        lista_emails.append(endr)
    await conn.close()
    return lista_emails


'''Colecao de Clientes'''


def clientefantasia(codigo):
    conn = pyodbc.connect(Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    tabela = conn.cursor().execute(
        f"SELECT AEMPR_NOME_ABREV as FANT FROM SUPAEMPR where AEMPR_TIPO = 'C' AND AEMPR_CODIGO = {codigo}")
    fantasia = ''
    for cli in tabela:
        fantasia = cli.FANT.strip()
    conn.close()
    return fantasia


def cursor_para_lista_dict(cursor):
    colunas = [coluna[0] for coluna in cursor.description]
    linhas = []
    x = cursor.fetchall()
    for linha in x:
        linhas.append(dict(zip(colunas, linha)))
    return linhas


def extratorcliente(listaclientes: list):
    tempcliente = {}
    lista_cliente = []
    for cliente in listaclientes:
        try:
            tempcliente = {
                "representante": cliente.REPRE, "zona": cliente.ZONA, "mercado": cliente.MERCADO.strip(),
                "rota": cliente.ROTA.strip(), "estado": cliente.ST.strip(),
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
                "ultimo_pedido": {"quantidade_caixas": int(cliente.NR_CX), "total_nota": float(cliente.TOT_NOTA),
                                  "emissao":
                                      (cliente.DT_EMISSAO[6:8] + "/" + cliente.DT_EMISSAO[
                                                                       4:6] + "/" + cliente.DT_EMISSAO[0:4])},
                "tabela_de_preco": {"prowater": cliente.TAB_PW, "proclean": cliente.TAB_PC,
                                    "prolimp": cliente.TAB_PL, "pronew": cliente.TAB_PN},
                "condicao_de_pagamento": {"prowater": cliente.PGTOPW, "proclean": cliente.PGTOPC,
                                          "prolimp": cliente.PGTOPL, "pronew": cliente.PGTOPN}
            }
        except:
            print('erro')
        lista_cliente.append(tempcliente)
    return lista_cliente


def clientes_repre(**kwargs):
    repre = kwargs.get("repre")
    conn = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
    mongo_client = pymongo.MongoClient(conn)
    item_bd = mongo_client.get_database("prowater") \
        .get_collection("relatorio_de_compras") \
        .find({"supervisores": repre}, {"fantasia": 1, "cliente": 1, "_id": 0})
    return json.loads(dumps(item_bd, default=json_util.default))


def clientes(**kwargs):
    """
    :param kwargs: str or list or none
    :return: list
    """
    clientes = kwargs.get("clientes")
    lista_clientes = None
    if clientes is None:
        conn = pyodbc.connect(
            Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
        for query in Query.clientes():
            lista_clientes = conn.cursor().execute(query)
        resultado = extratorcliente(lista_clientes)
        conn.close()
        return resultado
    elif isinstance(clientes, str):
        conn = pyodbc.connect(
            Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
        for query in Query.clienteporcodigo(clientes):
            lista_clientes = conn.cursor().execute(query)
        resultado = extratorcliente([lista_clientes])
        conn.close()
        return resultado
    elif isinstance(clientes, list):
        conn = pyodbc.connect(
            Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
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
    conn = pyodbc.connect(Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    tabela_preco = conn.cursor().execute(Query.tabela4())
    lista_tabela_preco = []
    for item in tabela_preco:
        temp = {"empresa": item.EMP, "codigo": str(item.ITEM).strip(), "valor": float(item.VALOR),
                "tabela": item.TABELA}
        lista_tabela_preco.append(temp)
    conn.close()
    return lista_tabela_preco


def tabelaprecosfinal():
    conn = pyodbc.connect(
        Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    tabela_preco = conn.cursor().execute(Query.tabelaprecosfinal())
    lista_tabela_preco_final = []
    for item in tabela_preco:
        temp = {
            "empresa": item.EMPRESA,
            "codigo": str(item.ITEM).strip(),
            "descricao": str(item.DESC).strip(),
            "data_inicial": item.DATA_I,
            "data_final": item.DATA_F,
            "valor": float(item.VALOR)
        }
        lista_tabela_preco_final.append(temp)
    conn.close()
    return lista_tabela_preco_final


def extratorcobranca(tabelacobrancas):
    lista_de_cobrancas = []
    for linha in tabelacobrancas:
        temp = {"representante": linha.REPR, "cliente": linha.CLI, "empresa": linha.EMP, "nota_fiscal": linha.NOTA,
                "pedido": linha.PED, "vencimento": linha.VCTO, "emissao": linha.EMISSAO, "parcela": linha.PARC,
                "valor": float(linha.VALOR)}
        lista_de_cobrancas.append(temp)
    return lista_de_cobrancas


def extratorcobranca_local(tabelacobrancas):
    lista_de_cobrancas = []
    for linha in tabelacobrancas:
        temp = {"representante": linha.REPR, "cliente": linha.CLI, "empresa": linha.EMP, "nota_fiscal": linha.NOTA,
                "pedido": linha.PED, "vencimento": linha.VCTO.__str__(), "emissao": linha.EMISSAO.__str__(),
                "parcela": linha.PARC, "valor": float(linha.VALOR)}
        lista_de_cobrancas.append(temp)
    return lista_de_cobrancas


def cobrancas():
    conn = pyodbc.connect(
        Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    tabelacobrancas = conn.cursor().execute(Query.cobrancas())
    resultado = extratorcobranca(tabelacobrancas)
    conn.close()
    return resultado


def selecionaCobranca(tabelacobrancas, **kwargs):
    cliente = kwargs.get("cliente")
    empresa = kwargs.get("empresa")
    pedido = kwargs.get("pedido")
    local = kwargs.get("local")
    nota_fiscal = kwargs.get("nota_fiscal")
    conn = pyodbc.connect(
        Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    if tabelacobrancas is None:
        tabelacobrancas = conn.cursor().execute(
            Query.cobrancasporargumentos(cliente=cliente, empresa=empresa, pedido=pedido, nota_fiscal=nota_fiscal))
    if local:
        resultado = extratorcobranca_local(tabelacobrancas)
    else:
        resultado = extratorcobranca(tabelacobrancas)
    conn.close()
    return resultado


async def async_selecionaCobranca(tabelacobrancas, **kwargs):
    cliente = kwargs.get("cliente")
    empresa = kwargs.get("empresa")
    pedido = kwargs.get("pedido")
    local = kwargs.get("local")
    nota_fiscal = kwargs.get("nota_fiscal")
    conn = await aioodbc.connect(dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    if tabelacobrancas is None:
        tabelacobrancas = await conn.cursor().execute(
            Query.cobrancasporargumentos(cliente=cliente, empresa=empresa, pedido=pedido, nota_fiscal=nota_fiscal))
    if local:
        resultado = extratorcobranca_local(tabelacobrancas)
    else:
        resultado = extratorcobranca(tabelacobrancas)
    await conn.close()
    return resultado


def representantes(**kwargs):
    repre = kwargs.get("repre") if kwargs.get("repre") is None else ""
    conn = pyodbc.connect(
        Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    representantes = conn.cursor().execute(Query.representantes(repre))
    lista_de_representantes = []
    for item in representantes:
        temp = {"codigo": item.COD, "razao_social": item.RAZAO, "fantasia": item.FANT,
                "email": getEmails(item.COD, tipo="R")}
        lista_de_representantes.append(temp)
    conn.close()
    return lista_de_representantes


def representante(codigo):
    conn = pyodbc.connect(Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    repre = conn.cursor().execute(Query.representante(codigo))
    for item in repre:
        temp = {"codigo": item.COD, "razao_social": item.RAZAO, "fantasia": item.FANT,
                "email": getEmails(item.COD, tipo="R")}
    conn.close()
    return temp

async def async_representante(codigo):
    conn = await aioodbc.connect(dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    repre = await conn.cursor().execute(Query.representante(codigo)).fetchone()
    email = await async_getEmails(repre.COD, tipo="R")
    res = {"codigo": repre.COD, "razao_social": repre.RAZAO, "fantasia": repre.FANT,
            "email": email}
    await conn.close()
    return res


def entregadivida():
    conn = pyodbc.connect(
        Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
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
        Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    consultas = None
    for query in Query.notascanceladasemotivo():
        consultas = conn.cursor().execute(query)
    lista_notas_canceladas_e_motivo = []
    for item in consultas:
        temp = {"empresa": item.EMPRESA, "representante": item.REPRE, "rota": item.ROTA, "cliente": item.CLIENTE,
                "fantasia": item.FANTASIA, "nff": item.NFF, "data_emissao": item.DATA_EMISSAO, "valor": float(item.TOT),
                "caixas": int(item.CX), "transporte": item.TRANSP, "nome_transporte": item.TRANSP_NOME,
                "motivo": item.MOTIVO}
        lista_notas_canceladas_e_motivo.append(temp)
    conn.close()
    return lista_notas_canceladas_e_motivo


def emissaodenotasfiscais():
    conn = pyodbc.connect(
        Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
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
        Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    consultas = conn.cursor().execute(Query.producao())
    lista_producao = []
    for item in consultas:
        temp = {"numero_op": item.NUM_OP, "item": item.ITEM, "data_emissao": item.DT_EMISSAO, "estado": item.ST,
                "a_fabricar": int(item.A_FABRICAR), "fabricado": int(item.FABRICADO), "diferenca": int(item.DIFERENCA),
                "efetuado": float(item.EFETUADO)}
        lista_producao.append(temp)
    conn.close()
    return lista_producao


def relatoriodecompras():
    conn = pyodbc.connect(
        Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    consultas = None
    for query in Query.relatoriodecompas():
        consultas = conn.cursor().execute(query)
    lista_clientes = []
    for item in consultas:
        temp = {"representante": item.REPRE, "zona": item.ZONA.strip(), "rota": item.ROTA.strip(),
                "tempo_pedido": int(item.PED),
                "tempo_faturado": int(item.FAT), "data_faturamento": item.DT_FAT, "total_valor": float(item.VLR_NF),
                "total_caixas": int(item.NR_CX), "cobrancas": int(item.COB), "estado": item.ST, "codigo": item.CODIGO,
                "fantasia": item.FANTASIA.strip(), "razao_social": item.RAZAO_SOCIAL.strip(), "cnpj_cpf": item.CNPJ_CPF,
                "email": item.EMAIL,
                "contato": item.CONTATO.strip(), "celular": item.CELULAR.strip(), "telefone": item.TELEFONE.strip(),
                "endereco": item.ENDERECO.strip(),
                "bairro": item.BAIRRO.strip(), "cidade": item.CIDADE.strip(), "cep": int(item.CEP), "uf": item.UF}
        lista_clientes.append(temp)
    conn.close()
    return lista_clientes


def itenspedidos():
    conn = pyodbc.connect(
        Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    consultas = None
    for query in Query.itenspedidos():
        consultas = conn.cursor().execute(query)
    pedidos_faturados = []
    for item in consultas:
        temp = {"empresa": item.EMPRESA, "representante": item.REPRE, "rota": item.ROTA, "zona": item.ZONA,
                "mercado": item.MERCADO, "cliente": item.CLI, "pedido": item.PEDIDO, "data_cadastro": item.CADAST,
                "tipo": item.TIPO, "produto": item.COD_ITEM, "quantidade": int(item.QTD),
                "valor_unitario": float(item.VALOR_UN), "valor_total": float(item.TOTAL)
                }
        pedidos_faturados.append(temp)
    conn.close()
    return pedidos_faturados


def pedidosabertos():
    conn = pyodbc.connect(
        Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    consultas = None
    for query in Query.pedidosabertos():
        consultas = conn.cursor().execute(query)
    pedidos_cadastrados = []
    for item in consultas:
        temp = {"representante": item.REPRE, "zona": item.ZONA, "mercado": item.MERCADO, "rota": item.ROTA,
                "cliente": item.CLIENTE,
                "fantasia": item.FANTASIA, "cadastro": item.CADAST, "previsao": item.PREV, "empresa": item.EMPRESA,
                "reperesentante_pedido": item.REPRE_PED,
                "pedido": item.PEDIDO, "tipo": item.TIPO, "condicao_pagamento": int(item.COND_PGTO),
                "prazo": item.PRAZO,
                "valor": float(item.VALOR),
                "caixas": int(item.CX), "peso": int(item.PESO), "vencimento": item.VENCIMENTO,
                "boletos_a_vencer": float(item.BL_A_Vencer),
                "boletos_atrasado": float(item.BL_Atrasado), "saldo": float(item.Saldo)}
        pedidos_cadastrados.append(temp)
    conn.close()
    return pedidos_cadastrados


def quantidadefathistorico(**kwargs):
    cliente = kwargs.get("cliente")
    conn = pyodbc.connect(Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    consultas = conn.cursor().execute(Query.contaconotas(cliente=cliente))
    res = None
    for item in consultas:
        print(f"{cliente} : {int(item.NOTA)}")
        res = int(item.NOTA)
    return res


async def async_quantidadefathistorico(**kwargs):
    cliente = kwargs.get("cliente")
    conn = await aioodbc.connect(dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    consultas = await conn.cursor().execute(Query.contaconotas(cliente=cliente)).fetchone()
    print(f"{cliente} : {int(consultas.NOTA)}")
    res = int(consultas.NOTA)
    return res


def historicofaturamento(conn: pyodbc.Cursor, **kwargs):
    cliente = kwargs.get("cliente")
    notaf = kwargs.get("nota")
    top = kwargs.get("top")
    consultas = None
    fecha_conn = False
    if conn is None:
        fecha_conn = True
        conn = pyodbc.connect(
            Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
        for query in Query.historiconotas(cliente=cliente, nota=notaf, top=top):
            consultas = conn.cursor().execute(query)
    else:
        consultas = conn.execute(f"select * from #res where CLIENTE = {cliente}")
    notas = []
    nota = {"nota": None, "data": None, "bonificacao": False, "total_nota": 0, "produtos": []}
    if consultas is None:
        return notas
    for item in consultas:
        if item is None:
            return None
        tabela = item.TABELA
        if tabela is None:
            tabela = 0
        temp = {"produto": str(item.PRODUTO).strip(), "quantidade": int(item.QTD),
                "total_linha": float(item.TOT_PRODUTO),
                "tabela": float(tabela)}
        if nota.get("nota") == item.NOTA:
            nota.get("produtos").append(temp)
        else:
            if nota.get("nota") is not None:
                notas.append(nota)
            nota = {"nota": item.NOTA, "data": item.PERIODO.strftime('%Y/%m/%d'), "bonificacao": item.NF_NB[:2],
                    "total_nota": float(item.TOT_NOTA), "produtos": []}
            nota.get("produtos").append(temp)
    notas.append(nota)
    if fecha_conn:
        conn.close()
    return notas


async def async_historicofaturamento(conn: pyodbc.Cursor, **kwargs):
    cliente = kwargs.get("cliente")
    notaf = kwargs.get("nota")
    top = kwargs.get("top")
    consultas = None
    fecha_conn = False
    if conn is None:
        fecha_conn = True
        conn = await aioodbc.connect(dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
        for query in Query.historiconotas(cliente=cliente, nota=notaf, top=top):
            consultas = await conn.cursor().execute(query)
    else:
        consultas = await conn.execute(f"select * from #res where CLIENTE = {cliente}")
    notas = []
    nota = {"nota": None, "data": None, "bonificacao": False, "total_nota": 0, "produtos": []}
    if consultas is None:
        return notas
    for item in consultas:
        if item is None:
            return None
        tabela = item.TABELA
        if tabela is None:
            tabela = 0
        temp = {"produto": str(item.PRODUTO).strip(), "quantidade": int(item.QTD),
                "total_linha": float(item.TOT_PRODUTO),
                "tabela": float(tabela)}
        if nota.get("nota") == item.NOTA:
            nota.get("produtos").append(temp)
        else:
            if nota.get("nota") is not None:
                notas.append(nota)
            nota = {"nota": item.NOTA, "data": item.PERIODO.strftime('%Y/%m/%d'), "bonificacao": item.NF_NB[:2],
                    "total_nota": float(item.TOT_NOTA), "produtos": []}
            nota.get("produtos").append(temp)
    notas.append(nota)
    if fecha_conn:
        await conn.close()
    return notas


def itemsnotasfaturadas():
    conn = pyodbc.connect(
        Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    consultas = None
    for query in Query.itensnotasfaturadas():
        consultas = conn.cursor().execute(query)
    item_nota_faturada = []
    for item in consultas:
        temp = {"representante": item.REPRE, "rota": item.ROTA, "zona": item.ZONA, "mercado": item.MERCADO,
                "cliente": item.CODIGO, "estado": item.ST, "fantasia": item.FANTASIA, "empresa": item.EMP,
                "nota": item.NOTA,
                "pedido": item.PEDIDO, "data_faturamento": item.DT.strftime('%Y/%m/%d'), "produto": item.PRODUTO,
                "quantidade": int(item.QTD),
                "valor_unitario": float(item.UN)}
        item_nota_faturada.append(temp)
    conn.close()
    return item_nota_faturada


def notasepedidos(cliente):
    conn = pyodbc.connect(
        Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    consultas = None
    for query in Query.notasepedidos(cliente=cliente):
        consultas = conn.cursor().execute(query)
    notas_pedidos = []
    for item in consultas:
        temp = f"{item.CODIGO},{item.EMP},{item.REPRE_F},{item.PED},{item.NOTA},{item.TIPO},"


def supervisores(repre):
    conn = pyodbc.connect(Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    superv = [repre]
    consultas = conn.cursor().execute(Query.supervisores(repre=repre))
    for item in consultas:
        if item.SUPERVISOR != repre:
            temp = str(item.SUPERVISOR)
            superv += supervisores(temp)
    conn.close()
    return superv

async def async_supervisores(repre):
    conn = await aioodbc.connect(dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    superv = [repre]
    consultas = await conn.cursor().execute(Query.supervisores(repre=repre))
    for item in consultas:
        if item.SUPERVISOR != repre:
            temp = str(item.SUPERVISOR)
            superv += await async_supervisores(temp)
    await conn.close()
    return superv


def relatorio_de_compras(repre, cli, cnpj_cpf, top, forcar):
    conn = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
    mongo_client = pymongo.MongoClient(conn)
    conn = pyodbc.connect(Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    consultas = None
    historico_mem = None
    for query in Query.relatoriodecomprasleve(repre=repre, cliente=cli, cnpj_cpf=cnpj_cpf):
        consultas = conn.cursor().execute(query)

    repre_dados = representante(repre)
    lista_clientes = []
    for item in consultas:
        clinte = str(item.ENDERECO).split("-")
        # cobrancas_mem = conn.cursor().execute(Query.cobrancasporargumentos())
        item_bd = mongo_client.get_database("prowater") \
            .get_collection("relatorio_de_compras") \
            .find_one({"cliente": clinte[0].strip()})
        historico = []
        cobs = selecionaCobranca(None, cliente=clinte[0].strip())
        quantidade_historico = quantidadefathistorico(cliente=clinte[0].strip())
        if not forcar:
            if item_bd is not None:
                qtd_h = item_bd.get('qtd_historico') if item_bd.get('qtd_historico') is not None else 0
                if qtd_h != quantidade_historico:
                    for query in Query.historiconotas(cliente=cli):
                        historico_mem = conn.cursor().execute(query)
                    historico = historicofaturamento(historico_mem, cliente=clinte[0].strip())
                    historico_mem.close()
            else:
                print(f"Novo cliente: {clinte[0].strip()}")
                for query in Query.historiconotas(cliente=cli):
                    historico_mem = conn.cursor().execute(query)
                historico = historicofaturamento(historico_mem, cliente=clinte[0].strip())
                historico_mem.close()
        else:
            for query in Query.historiconotas(cliente=cli):
                historico_mem = conn.cursor().execute(query)
            historico = historicofaturamento(historico_mem, cliente=clinte[0].strip())
            historico_mem.close()
        temp = {
            "representante": item.REPRE,
            "representante_nome": repre_dados.get("fantasia"),
            "tmp_ped": item.PED,
            "tmp_fat": item.FAT,
            "estado": str(item.ST).strip(),
            "cobrancas": cobs,
            "cliente": clinte[0].strip(),
            "fantasia": clinte[1].strip(),
            "endereco": clinte[2].strip(),
            "supervisores": supervisores(repre=item.REPRE),
            "qtd_historico": quantidade_historico,
            "cnpj_cpf": item.CNPJ_CPF
        }
        temp['media_compras'] = 21
        temp['ataque'] = (datetime.strptime(temp['tmp_fat'], '%Y/%m/%d') + timedelta(days=14)).strptime('%Y/%m/%d')
        if len(historico) > 1:
            historico = sorted(historico, key=lambda k: k['data'], reverse=True)
            filtro = [data for data in historico if data.get('data') >= datetime.now() - timedelta(days=365)]
            temp['historico'] = filtro[:top]
            if len(filtro) > 1:
                entre_compras = []
                for venda in range((len(filtro) - 1)):
                    entre_compras.append(
                        filtro[venda].get('data') - filtro[venda + 1].get('data'))
                media_compra = timedelta(days=0)
                for tempo in entre_compras:
                    media_compra += tempo
                temp['media_compras'] = int(media_compra.days / len(filtro))
                temp['ataque'] = (datetime.strptime(temp['tmp_fat'], '%Y/%m/%d') + (
                        (timedelta(days=int(media_compra.days / (len(filtro))))) - timedelta(days=7))).strftime(
                    '%Y/%m/%d')
        tabela_preco = cursor_para_lista_dict(conn.cursor().execute(Query.tabelacliente(cli=clinte[0].strip())))
        if tabela_preco:
            lista_produtos = cursor_para_lista_dict(
                conn.cursor().execute(Query.produtostabela(tabela=tabela_preco[0].get("TABELA"))))
            for i in range(len(lista_produtos)):
                lista_produtos[i]["VALOR"] = float(lista_produtos[i].get("VALOR"))
                lista_produtos[i]["ITEM"] = lista_produtos[i].get("ITEM").strip()
            temp['tabela'] = lista_produtos
        lista_clientes.append(temp)
        mongo_client.get_database("prowater").get_collection("relatorio_de_compras").update_one(
            {"cliente": clinte[0].strip()},
            {"$set": temp},
            upsert=True
        )
    print(lista_clientes)
    # cobrancas_mem.close()
    conn.close()
    print('Enviando')
    return lista_clientes


def relatorio_de_compras_local(repre, cli, cnpj_cpf, top):
    global temp
    conn = pyodbc.connect(Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    consultas = None
    historico_mem = None
    for query in Query.relatoriodecomprasleve(repre=repre, cliente=cli, cnpj_cpf=cnpj_cpf):
        consultas = conn.cursor().execute(query)
    repre_dados = representante(repre)
    lista_clientes = []
    for item in consultas:
        clinte = str(item.ENDERECO).split("-")
        cobs = selecionaCobranca(None, cliente=clinte[0].strip(), local=True)
        quantidade_historico = quantidadefathistorico(cliente=clinte[0].strip())
        for query in Query.historiconotas(cliente=cli):
            historico_mem = conn.cursor().execute(query)
        historico = historicofaturamento(historico_mem, cliente=clinte[0].strip())
        historico_mem.close()
        temp = {
            "representante": item.REPRE,
            "representante_nome": repre_dados.get("fantasia"),
            "tmp_ped": item.PED.strftime('%Y/%m/%d') if item.PED is not None else '9999/12/31',
            "tmp_fat": item.FAT.strftime('%Y/%m/%d') if item.FAT is not None else '9999/12/31',
            "estado": str(item.ST).strip(),
            "cobrancas": cobs,
            "cliente": clinte[0].strip(),
            "fantasia": clinte[1].strip(),
            "endereco": clinte[2].strip(),
            "supervisores": supervisores(repre=item.REPRE),
            "qtd_historico": quantidade_historico,
            "cnpj_cpf": item.CNPJ_CPF
        }
        temp['media_compras'] = 21
        tmp_fat = temp['tmp_fat'] if temp['tmp_fat'] != '9999/12/31' else (
                    datetime.now() - timedelta(days=14)).strftime('%Y/%m/%d')
        temp['ataque'] = (datetime.strptime(tmp_fat, '%Y/%m/%d') + timedelta(days=14)).strftime('%Y/%m/%d')
        if len(historico) > 1:
            historico = sorted(historico, key=lambda k: k['data'], reverse=True)
            filtro = [data for data in historico if
                      datetime.strptime(data.get('data'), '%Y/%m/%d') >= datetime.now() - timedelta(days=365)]
            temp['historico'] = filtro[:top]
            if len(filtro) > 1:
                entre_compras = []
                for venda in range((len(filtro) - 1)):
                    entre_compras.append(
                        datetime.strptime(filtro[venda].get('data'), '%Y/%m/%d') -
                        datetime.strptime(filtro[venda + 1].get('data'), '%Y/%m/%d'))
                media_compra = timedelta(days=0)
                for tempo in entre_compras:
                    media_compra += tempo
                temp['media_compras'] = int(media_compra.days / len(filtro))
                temp['ataque'] = (datetime.strptime(temp['tmp_fat'], '%Y/%m/%d') + (
                        (timedelta(days=int(media_compra.days / (len(filtro))))) - timedelta(days=7))).strftime(
                    '%Y/%m/%d')
        tabela_preco = cursor_para_lista_dict(conn.cursor().execute(Query.tabelacliente(cli=clinte[0].strip())))
        if tabela_preco:
            lista_produtos = cursor_para_lista_dict(
                conn.cursor().execute(Query.produtostabela(tabela=tabela_preco[0].get("TABELA"))))
            for i in range(len(lista_produtos)):
                lista_produtos[i]["VALOR"] = float(lista_produtos[i].get("VALOR"))
                lista_produtos[i]["ITEM"] = lista_produtos[i].get("ITEM").strip()
                lista_produtos[i]["DT_INI"] = lista_produtos[i]["DT_INI"].strftime('%Y/%m/%d')
                lista_produtos[i]["DT_FIN"] = lista_produtos[i]["DT_FIN"].strftime('%Y/%m/%d')
            temp['tabela'] = lista_produtos
    conn.close()
    return temp


async def async_relatorio_de_compras_local(repre, cli, cnpj_cpf, top):
    global temp
    dsn = "Driver=SQL Anywhere 12;ENG=PW_CLOUD;UID=BYTEC;PWD=BYTEC"
    conn = await aioodbc.connect(dsn=dsn)
    consultas = None
    historico_mem = None
    for query in Query.relatoriodecomprasleve(repre=repre, cliente=cli, cnpj_cpf=cnpj_cpf):
        consultas = await conn.cursor().execute(query)
    repre_dados = await async_representante(repre)
    lista_clientes = []
    for item in consultas:
        clinte = str(item.ENDERECO).split("-")
        cobs = await async_selecionaCobranca(None, cliente=clinte[0].strip(), local=True)
        quantidade_historico = await async_quantidadefathistorico(cliente=clinte[0].strip())
        for query in Query.historiconotas(cliente=cli):
            historico_mem = await conn.cursor().execute(query)
        historico = await async_historicofaturamento(historico_mem, cliente=clinte[0].strip())
        await historico_mem.close()
        temp = {
            "representante": item.REPRE,
            "representante_nome": repre_dados.get("fantasia"),
            "tmp_ped": item.PED.strftime('%Y/%m/%d') if item.PED is not None else '9999/12/31',
            "tmp_fat": item.FAT.strftime('%Y/%m/%d') if item.FAT is not None else '9999/12/31',
            "estado": str(item.ST).strip(),
            "cobrancas": cobs,
            "cliente": clinte[0].strip(),
            "fantasia": clinte[1].strip(),
            "endereco": clinte[2].strip(),
            "supervisores": await async_supervisores(repre=item.REPRE),
            "qtd_historico": quantidade_historico,
            "cnpj_cpf": item.CNPJ_CPF
        }
        temp['media_compras'] = 21
        tmp_fat = temp['tmp_fat'] if temp['tmp_fat'] != '9999/12/31' else (
                    datetime.now() - timedelta(days=14)).strftime('%Y/%m/%d')
        temp['ataque'] = (datetime.strptime(tmp_fat, '%Y/%m/%d') + timedelta(days=14)).strftime('%Y/%m/%d')
        if len(historico) > 1:
            historico = sorted(historico, key=lambda k: k['data'], reverse=True)
            filtro = [data for data in historico if
                      datetime.strptime(data.get('data'), '%Y/%m/%d') >= datetime.now() - timedelta(days=365)]
            temp['historico'] = filtro[:top]
            if len(filtro) > 1:
                entre_compras = []
                for venda in range((len(filtro) - 1)):
                    entre_compras.append(
                        datetime.strptime(filtro[venda].get('data'), '%Y/%m/%d') -
                        datetime.strptime(filtro[venda + 1].get('data'), '%Y/%m/%d'))
                media_compra = timedelta(days=0)
                for tempo in entre_compras:
                    media_compra += tempo
                temp['media_compras'] = int(media_compra.days / len(filtro))
                temp['ataque'] = (datetime.strptime(temp['tmp_fat'], '%Y/%m/%d') + (
                        (timedelta(days=int(media_compra.days / (len(filtro))))) - timedelta(days=7))).strftime(
                    '%Y/%m/%d')
        tabela_preco = cursor_para_lista_dict(await conn.cursor().execute(Query.tabelacliente(cli=clinte[0].strip())))
        if tabela_preco:
            lista_produtos = cursor_para_lista_dict(
                await conn.cursor().execute(Query.produtostabela(tabela=tabela_preco[0].get("TABELA"))))
            for i in range(len(lista_produtos)):
                lista_produtos[i]["VALOR"] = float(lista_produtos[i].get("VALOR"))
                lista_produtos[i]["ITEM"] = lista_produtos[i].get("ITEM").strip()
                lista_produtos[i]["DT_INI"] = lista_produtos[i]["DT_INI"].strftime('%Y/%m/%d')
                lista_produtos[i]["DT_FIN"] = lista_produtos[i]["DT_FIN"].strftime('%Y/%m/%d')
            temp['tabela'] = lista_produtos
    await conn.close()
    return temp



def relatorio_cliente(**kwargs):
    query = {}
    if kwargs.get('repre') != '00000':
        query['supervisores'] = kwargs.get('repre')
    if kwargs.get('cli') != '00000':
        query['cliente'] = kwargs.get('cli')
    if kwargs.get('cnpj_cpf'):
        query['cnpj_cpf'] = kwargs.get('cnpj_cpf')
    top = kwargs.get('top')
    conn = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
    mongo_client = pymongo.MongoClient(conn)
    item_bd = mongo_client.get_database("prowater") \
        .get_collection("relatorio_de_compras") \
        .find_one(query)
    if item_bd is None:
        try:
            item_bd = relatorio_de_compras(query.get('supervisores'), query.get('cliente'), query.get('cnpj_cpf'), top)
            return item_bd
        except:
            return json.loads(dumps(item_bd, default=json_util.default))
    return json.loads(dumps(item_bd, default=json_util.default))


def aplicacaop():
    conn = pyodbc.connect(Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    res = conn.cursor().execute(Query.aplicacaop())
    cursor_res = cursor_para_lista_dict(res)
    conn.close()
    return cursor_res


def aplicacaor():
    conn = pyodbc.connect(Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    res = conn.cursor().execute(Query.aplicacaor())
    cursor_res = cursor_para_lista_dict(res)
    conn.close()
    return cursor_res


def custos():
    conn = pyodbc.connect(Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    res = None
    for linha in Query.custos():
        res = conn.cursor().execute(linha)
    cursor_res = cursor_para_lista_dict(res)
    conn.close()
    return cursor_res


def representante_info(**kwargs):
    codigo = f" AND AEMPR_CODIGO = {kwargs.get('codigo')} " if kwargs.get('codigo') is not None else ''
    cnpj_cpf = f" AND (if AEMPR_CGC_CPF = 'F' then AEMPR_CPF else AEMPR_CGC ENDIF) = {kwargs.get('cnpj_cpf')}" if kwargs.get(
        'cnpj_cpf') else ''
    conn = pyodbc.connect(Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    query = f"SELECT * FROM SUPAEMPR WHERE AEMPR_TIPO = 'R' {codigo} {cnpj_cpf}"
    consulta = conn.cursor().execute(query)
    teste = cursor_para_lista_dict(consulta)
    id_l = 0
    for x in teste:
        teste[id_l] = {k: str(v) for k, v in x.items()}
        id_l += 1
    conn.close()
    if teste:
        return teste
    else:
        return None


def atualiza_tabela4(conn, mongo_client):
    tabela_preco = conn.cursor().execute(Query.tabela4())
    for item in tabela_preco:
        temp = {"empresa": item.EMP, "codigo": str(item.ITEM).strip(), "valor": float(item.VALOR),
                "tabela": item.TABELA}
        mongo_client.get_database("prowater").get_collection("tabela_precos").update_one({"codigo": temp.get('codigo')},
                                                                                         {"$set": temp}, upsert=True)
    conn.close()


def atualiza_tabela4_local():
    conn = pyodbc.connect(Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
    tabela_preco = conn.cursor().execute(Query.tabela4())
    catalogo = [{"empresa": item.EMP, "codigo": str(item.ITEM).strip(), "valor": float(item.VALOR),"tabela": item.TABELA} for item in tabela_preco]
    conn.close()
    return catalogo


class Exportar:
    def relatoriodecompras(self):
        conn = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
        mongo_client = pymongo.MongoClient(conn)
        conn = pyodbc.connect(Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
        consultas = None
        historico_mem = None
        for query in Query.relatoriodecompras():
            consultas = conn.cursor().execute(query)
        for query in Query.historiconotas():
            historico_mem = conn.cursor().execute(query)
        cobrancas_mem = conn.cursor().execute(Query.cobrancasporargumentos())
        lista_clientes = []

        for item in consultas:
            clinte = str(item.ENDERECO).split("-")
            item_bd = mongo_client.get_database("prowater") \
                .get_collection("relatorio_de_compras") \
                .find_one({"cliente": clinte[0].strip()})
            historico = []
            cobs = selecionaCobranca(cobrancas_mem, cliente=clinte[0].strip())
            if item_bd is not None:
                if len(item_bd['historico']) != quantidadefathistorico(cliente=clinte[0].strip()):
                    historico = historicofaturamento(historico_mem, cliente=clinte[0].strip())
            else:
                print(f"Novo cliente: {clinte[0].strip()}")
                historico = historicofaturamento(historico_mem, cliente=clinte[0].strip())
            if len(historico) > 1:
                historico = sorted(historico, key=lambda k: k['data'], reverse=True)
            temp = {
                "representante": item.REPRE,
                "tmp_ped": item.PED,
                "tmp_fat": item.FAT,
                "estado": str(item.ST).strip(),
                "cobrancas": cobs,
                "cliente": clinte[0].strip(),
                "fantasia": clinte[1].strip(),
                "endereco": clinte[2].strip()
            }
            if historico:
                temp['historico'] = historico
            lista_clientes.append(temp)
            mongo_client.get_database("prowater").get_collection("relatorio_de_compras").update_one(
                {"cliente": clinte[0].strip()},
                {"$set": temp},
                upsert=True
            )
        print(lista_clientes)
        historico_mem.close()
        cobrancas_mem.close()
        conn.close()
        return lista_clientes

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
            Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
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
                    f"{x['cliente']['estado']};"
                    f"{x['cliente']['fantasia']};"
                    f"{x['cliente']['codigo']};"
                    f"{x['cliente']['rota']}\n")
            else:
                geolocation = str(0) + ";" + str(0)
                file.write(
                    f"{geolocation};"
                    f"{x['endereco']};"
                    f"{x['cliente']['estado']};"
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
            Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
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
                f"{x['cliente']['estado']};"
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
            Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
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
                    f"{x['cliente']['estado']};"
                    f"{x['cliente']['fantasia']};"
                    f"{x['cliente']['codigo']};"
                    f"{x['cliente']['rota']}\n")
            else:
                geolocation = str(0) + ";" + str(0)
                file.write(
                    f"{geolocation};"
                    f"{x['endereco']};"
                    f"{x['cliente']['estado']};"
                    f"{x['cliente']['fantasia']};"
                    f"{x['cliente']['codigo']};"
                    f"{x['cliente']['rota']}\n")
        file.close()
