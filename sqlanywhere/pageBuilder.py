import datetime


def collapsible(header, body):
    return f"<div class =\"collapsible-header\">{header}</div> <div class =\"collapsible-body\">{body}</div>"


def tabela(dados):
    linhas = ''
    historico = ''
    for nota in dados["historico"]:
        produtos = ''
        for produto in nota["produtos"]:
            if produto['tabela'] != 0:
                desconto = round(1 - (produto['total_linha'] / produto['tabela']), 2)
            else:
                desconto = 0
            produtos += f"<li><span> Produto: {produto['produto']} Quantidade: {produto['quantidade']} Total produto: {produto['total_linha']} Desconto: {desconto}</span> </li>"
        if nota['bonificacao']:
            bonifica = 'Sim'
        else:
            bonifica = 'Não'

        header = f"Nota: {nota['nota']} Data:{nota['data']} Total: {nota['total_nota']} Bonificação: {bonifica}"
        body = f"<ul>{produtos}</ul>"
        historico += f"<li> {collapsible(header, body)} </li>"
    media_tempo = 'Sem dados'
    if len(dados['historico']) > 1:
        total_entre_compras = dados['historico'][0]['data'] - dados['historico'][-1]['data']
        media_tempo = total_entre_compras.days()/len(dados['historico'])
    header = (f"Codigo: {dados['cliente']} Status: {dados['estado']}<br> "
              f"Nome fantasia: {dados['fantasia']}<br> Endereço: {dados['endereco']}<br>  Ultimo faturamento: "
              f"{dados['tmp_fat']} - Ultimo pedido: {dados['tmp_ped']} - Tempo entre compras: {media_tempo}")
    body = f"<ul class =\"collapsible\">{historico}</ul>"
    linhas += f"<li>{collapsible(header, body)}</li>"
    coluna = f"<ul class =\"collapsible\">{linhas}</ul>"
    return coluna


def body(conteudo):
    script = "<script>$(document).ready(function(){$('.collapsible').collapsible();});</script>"
    res = f"<body>{conteudo}{script}</body>"
    return res


def head(title):
    res = (
        "<head>"
        "<link href=\"https://fonts.googleapis.com/icon?family=Material+Icons\" rel=\"stylesheet\">"
        "<link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize"
        ".min.css\"> "
        "<script src=\"https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js\"></script>"
        f"<title>{title}</title>"
        "</head>"
    )
    return res


def build(dados):
    lista = ''
    if type(dados) is list:
        for item in dados:
            if item is None:
                continue
            lista += tabela(item)
        return f"<html>{head('teste')}{body(lista)}</html>"
    else:
        return f"<html>{head('teste')}{body(dados)}</html>"


class Site:
    pass
