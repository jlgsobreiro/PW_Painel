import datetime
import pyodbc
import requests

import sqlanywhere as sql

file = open("updater.log", "a")
file.write(f"Abrindo: {datetime.datetime.now().ctime()}\n")
conn = pyodbc.connect(Dsn="PW64", uid="BYTEC", pwd="BYTEC")
clientes = conn.cursor().execute(
    "select AEMPR_CODIGO as COD,AEMPR_REPR as REPRE, if(AEMPR_CGC_CPF = 'F') then AEMPR_CPF ELSE AEMPR_CGC ENDIF as CNPJ_CPF from SUPAEMPR where AEMPR_TIPO = 'C' AND AEMPR_STATUS = 'A' ORDER BY AEMPR_DT_CADASTRO DESC ")
for cliente in clientes:
    data = sql.relatorio_de_compras_local(repre=cliente.REPRE, cli=cliente.COD, cnpj_cpf=cliente.CNPJ_CPF, top=6)
    requests.post("http://appprowater.ddns.net:5000//update", data=data)
conn.close()
file.write(f"Fechando: {datetime.datetime.now().ctime()}\n")
file.close()
