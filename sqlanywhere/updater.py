import pyodbc
import sqlanywhere as sql

conn = pyodbc.connect(Dsn="PW64", uid="BYTEC", pwd="BYTEC")
clientes = conn.cursor().execute(
    "select AEMPR_CODIGO as COD,AEMPR_REPR as REPRE from SUPAEMPR where AEMPR_TIPO = 'C' AND AEMPR_STATUS = 'A'")
for cliente in clientes:
    sql.relatorio_de_compras(repre=cliente.REPRE, cli=cliente.COD, top=6)
conn.close()
