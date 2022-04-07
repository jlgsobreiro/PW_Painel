import datetime
import pyodbc
import requests
from cryptography.fernet import Fernet

import sqlanywhere as sql

file = open("updater.log", "a")
file.write(f"Abrindo: {datetime.datetime.now().ctime()}\n")
conn = pyodbc.connect(Dsn="PW64", uid="BYTEC", pwd="BYTEC")
key = open("key.key", "rb").read()
fk = Fernet(key)
#url_servidor = 'http://appprowater.ddns.net:5000'
url_servidor = 'http://127.0.0.1:5000'
catalogo = sql.atualiza_tabela4_local()
for item in catalogo:
    res = requests.post(f"{url_servidor}/update",
                        data=fk.encrypt({'data': item, 'collection': 'tabela_precos'}.__str__().encode()))
    print(res.content)
clientes = conn.cursor().execute(
    "select AEMPR_CODIGO as COD,AEMPR_REPR as REPRE, if(AEMPR_CGC_CPF = 'F') then AEMPR_CPF ELSE AEMPR_CGC ENDIF as CNPJ_CPF from SUPAEMPR where AEMPR_TIPO = 'C' AND AEMPR_STATUS = 'A' ORDER BY AEMPR_DT_CADASTRO DESC ")
repres = sql.representante_info()
res = requests.post(f"{url_servidor}/update",
              data=fk.encrypt({'data': repres, 'collection': 'representantes'}.__str__().encode()))
print(res.content)
for cliente in clientes:
    data = sql.relatorio_de_compras_local(repre=cliente.REPRE, cli=cliente.COD, cnpj_cpf=cliente.CNPJ_CPF, top=6)
    res = requests.post(f"{url_servidor}/update",
                        data=fk.encrypt({'data': data, 'collection': 'relatorio_de_compras'}.__str__().encode()))
    print(res.content)

conn.close()
file.write(f"Fechando: {datetime.datetime.now().ctime()}\n")
file.close()
