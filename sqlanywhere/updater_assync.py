import datetime
import asyncio
import aiohttp
import aiofiles
import aioodbc
import pyodbc  # Se possível, use aiomssql para um acesso assíncrono ao SQL Server
from cryptography.fernet import Fernet
import sqlanywhere as sql
import time

MAX_RETRIES = 5
RETRY_DELAY = 5  # segundos

async def log_message(message):
    async with aiofiles.open("updater.log", "a") as file:
        await file.write(f"{message}\n")

async def retry_connection(coro, *args, retries=MAX_RETRIES):
    """Função para retentar uma operação assíncrona com um limite de tentativas."""
    for attempt in range(retries):
        try:
            return await coro(*args)
        except Exception as e:
            if attempt < retries - 1:
                print(f"Erro: {e}. Retentativa {attempt + 1} de {retries} em {RETRY_DELAY} segundos.")
                await log_message(f"Erro: {e}. Retentativa {attempt + 1} de {retries}.")
                await asyncio.sleep(RETRY_DELAY)
            else:
                await log_message(f"Falha após {retries} tentativas: {e}")
                raise

async def post_data(session, url, data):
    for attempt in range(MAX_RETRIES):
        try:
            async with session.post(url, data=data) as response:
                content = await response.content.read()
                print(content)
                return
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                print(f"Falha ao enviar dados: {e}. Tentativa {attempt + 1} de {MAX_RETRIES}.")
                await log_message(f"Falha ao enviar dados: {e}. Tentativa {attempt + 1} de {MAX_RETRIES}.")
                await asyncio.sleep(RETRY_DELAY)
            else:
                await log_message(f"Falha ao enviar dados após {MAX_RETRIES} tentativas: {e}")
                raise

async def connect_to_db():
    """Tenta conectar ao banco de dados com retentativas."""
    for attempt in range(MAX_RETRIES):
        try:
            dsn = "Driver=SQL Anywhere 12;ENG=PW_CLOUD;UID=BYTEC;PWD=BYTEC"
            conn = await aioodbc.connect(dsn=dsn)
            return conn
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                print(f"Erro ao conectar ao banco de dados: {e}. Tentativa {attempt + 1} de {MAX_RETRIES}.")
                await log_message(f"Erro ao conectar ao banco de dados: {e}. Tentativa {attempt + 1} de {MAX_RETRIES}.")
                await asyncio.sleep(RETRY_DELAY)
            else:
                await log_message(f"Falha ao conectar ao banco de dados após {MAX_RETRIES} tentativas: {e}")
                raise

async def main():
    await log_message(f"Abrindo: {datetime.datetime.now().ctime()}")
    
    # Conectando ao banco de dados com retentativas
    conn = await retry_connection(connect_to_db)

    key = open("key.key", "rb").read()
    fk = Fernet(key)
    url_servidor = 'http://prowaterapp.ddns.net:5000'

    # Atualização de tabela local
    catalogo = sql.atualiza_tabela4_local()

    async with aiohttp.ClientSession() as session:
        tasks = []
        # Envia dados da tabela de preços
        for item in catalogo:
            encrypted_data = fk.encrypt(str({'data': item, 'collection': 'tabela_precos'}).encode())
            tasks.append(retry_connection(post_data, session, f"{url_servidor}/update", encrypted_data))
        
        # Busca informações de clientes
        clientes = conn.cursor().execute(
            "SELECT AEMPR_CODIGO AS COD, AEMPR_REPR AS REPRE, "
            "IF(AEMPR_CGC_CPF = 'F') THEN AEMPR_CPF ELSE AEMPR_CGC ENDIF AS CNPJ_CPF "
            "FROM SUPAEMPR WHERE AEMPR_TIPO = 'C' AND AEMPR_STATUS = 'A' "
            "ORDER BY AEMPR_DT_CADASTRO DESC"
        )
        
        # Envia dados dos representantes
        repres = sql.representante_info()
        encrypted_repres = fk.encrypt(str({'data': repres, 'collection': 'representantes'}).encode())
        tasks.append(retry_connection(post_data, session, f"{url_servidor}/update", encrypted_repres))

        # Envia relatório de compras para cada cliente
        async for cliente in clientes:
            data = await sql.async_relatorio_de_compras_local(repre=cliente.REPRE, cli=cliente.COD, cnpj_cpf=cliente.CNPJ_CPF, top=6)

            encrypted_data = fk.encrypt(str({'data': data, 'collection': 'relatorio_de_compras'}).encode())
            coro = await retry_connection(post_data, session, f"{url_servidor}/update", encrypted_data)
            tasks.append(coro)
        
        # Aguarda todas as requisições serem concluídas
        await asyncio.gather(*tasks)

    conn.close()
    await log_message(f"Fechando: {datetime.datetime.now().ctime()}")

# Executa a função principal assíncrona
asyncio.run(main())
