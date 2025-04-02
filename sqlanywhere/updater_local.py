import datetime
from time import sleep

import pyodbc
import requests
from cryptography.fernet import Fernet
from multiprocessing import Pool

import sqlanywhere as sql

url_servidor = 'http://appprowater.ddns.net:5000'
#url_servidor = 'http://127.0.0.1:5000'
conn = pyodbc.connect(Dsn="PW_CLOUD", uid="BYTEC", pwd="BYTEC")
key = open("key.key", "rb").read()
fk = Fernet(key)


def f(cliente):
    data = sql.relatorio_de_compras_local(repre=cliente.REPRE, cli=cliente.COD, cnpj_cpf=cliente.CNPJ_CPF, top=6)
    res = requests.post(f"{url_servidor}/update",
                        data=fk.encrypt({'data': data, 'collection': 'relatorio_de_compras'}.__str__().encode()))
    print(f"{res.status_code} - {cliente.COD}")


def main():
    clientes = conn.cursor().execute(
        ("select AEMPR_CODIGO as COD,"
         "AEMPR_REPR as REPRE, if(AEMPR_CGC_CPF = 'F') then AEMPR_CPF ELSE AEMPR_CGC ENDIF as CNPJ_CPF "
         "from SUPAEMPR where AEMPR_TIPO = 'C' AND AEMPR_STATUS = 'A' ORDER BY AEMPR_DT_ULT_ATUAL DESC "))
    lista_cli = [r for r in clientes]
    p = Pool()
    p.map(f, lista_cli)
    p.close()


if __name__ == '__main__':
    file = open("updater.log", "a")
    file.write(f"Abrindo: {datetime.datetime.now().ctime()}\n")

    catalogo = sql.atualiza_tabela4_local()
    for item in catalogo:
        res = requests.post(f"{url_servidor}/update",
                            data=fk.encrypt({'data': item, 'collection': 'tabela_precos'}.__str__().encode()))
        print(res.content)
    repres = sql.representante_info()
    res = requests.post(f"{url_servidor}/update",
                        data=fk.encrypt({'data': repres, 'collection': 'representantes'}.__str__().encode()))
    print(res.content)
    print(res.status_code)

    main()

    conn.close()
    file.write(f"Fechando: {datetime.datetime.now().ctime()}\n")
    file.close()
