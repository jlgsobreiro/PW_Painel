from time import strptime

import pyodbc


class Cliente:
    '''Retorna email do cliente'''

    def getEmails(self, codigo):
        conn = pyodbc.connect(Dsn="PW32", uid="BYTEC", pwd="BYTEC")
        emails = conn.cursor().execute(
            "select AMAIL_IDENTIFICA as descr, AMAIL_E_MAIL_WWW as email_site from SUPAMAIL where AMAIL_TIPO = 'C' and AMAIL_CODIGO = " + str(
                codigo) + ";")
        lista_emails = []
        for enderecos in emails:
            endr = {"descricao": enderecos.descr, "endereco": enderecos.email_site}
            lista_emails.append(endr)
        conn.close()
        return lista_emails

    '''Colecao de Clientes'''

    def info(self):
        conn = pyodbc.connect(
            Dsn="PW32", uid="BYTEC", pwd="BYTEC")
        conn.cursor().execute(
            "SELECT b.REPRE as repre, b.ZONA as zona, b.MERCADO as mercado, b.ROTA as rota, b.ST as st, b.CODIGO as cod, b.FANTASIA as fant into #cliente FROM BYTEC2.VIEWROTAREPRESENTANTE b;")
        conn.cursor().execute(
            "SELECT CodigoEmpresa as emp, LimiteCred as cred into #credito FROM InfoCredCFT WHERE TipoEmpresa = \'C\';")
        conn.cursor().execute(
            "SELECT APEPC_EMPRESA as emp, APEPC_PEDIDO as ped, sum(APEPC_QTD_PEDIDA*APEPC_VALOR_ENC) as tot into #liberado FROM VNDAPEPC where APEPC_STATUS = \'L\' GROUP BY ped,emp;")
        conn.cursor().execute(
            "SELECT APECD_EMPREsA as emp, APECD_PEDIDO as ped, APECD_CLIENTE as cod into #clientepedido FROM VNDAPECD where APECD_TIPO_CLI = \'C\';")
        conn.cursor().execute(
            "SELECT ANFLN_EMPRESA as emp, ANFLN_PEDIDO as ped, ANFLN_NUM_NOTA as nota into #notapedido FROM VNDANFLN;")
        conn.cursor().execute(
            "SELECT codigoemp as emp, numero as nota, sum(valor+valorjuros) as tot into #pendente FROM ParcelaR where isnull(datediff(day,recebimento,getdate()),-1) = -1 GROUP BY emp, nota;")
        conn.cursor().execute(
            "SELECT ido.cod as cod, sum(ado.tot) as tot into #pedidosabertos FROM #clientepedido ido,#liberado ado WHERE ado.ped = ido.ped and ado.emp = ido.emp GROUP BY ido.cod;")
        conn.cursor().execute(
            "SELECT mpr.AEMPR_STATUS as ST,fcd.ANFCD_CLIENTE AS CLI, mpr.AEMPR_NOME_ABREV AS FANTASIA,fcd.ANFCD_EMPRESA AS EMP,fcd.ANFCD_NUM_NOTA AS NOTA, lar.VALOR as valor, lar.valorjuros as juros, lar.PARCELA as PARC, datediff(day,lar.Vencimento,now()) as vencido into #devendo FROM SUPAEMPR mpr, VNDANFCD fcd,VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND datediff(day,lar.Vencimento,now()) <= 0;")
        conn.cursor().execute(
            "select cli as cod,sum(valor) as tot into #dividacliente from #devendo GROUP BY cli;")
        conn.cursor().execute(
            "SELECT fcd.ANFCD_CLIENTE AS cod, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, datediff(day,lar.Vencimento,now()) as vencido, lar.PARCELA as PARC, lar.VALOR as valor into #atrasado FROM     SUPAEMPR mpr,    VNDANFCD fcd,    VNDAEMDF mdf,    PARCELAR lar,    BYTEC2.VIEWROTAREPRESENTANTE nte where    fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND    fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND    fcd.ANFCD_CLIENTE = nte.CODIGO AND    fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND    fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND    fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND    fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND    SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND    lar.RECEBIMENTO IS NULL AND     lar.VENCIMENTO+1 <= now() EXCEPT (SELECT fcd.ANFCD_CLIENTE AS CLI, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, datediff(day,lar.Vencimento,now()) as \"D VNC\", lar.PARCELA as PARC, lar.VALOR FROM SUPAEMPR mpr, VNDANFCD fcd, VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND lar.VENCIMENTO+1 <= now() AND lar.Vencimento = fcd.ANFCD_DATA_EMISSAO AND datediff(day,lar.Vencimento,now()) <= 2);")
        conn.cursor().execute(
            "select cod as cod,sum(valor+valor*0.004*vencido) as tot into #atrasocliente from #Atrasado where vencido > 0 GROUP BY cod;")
        conn.cursor().execute(
            "select ecd.APECD_CLIENTE, fcd.ANFCD_TOT_NOTA, sum(fln.ANFLN_QTD_IMP), DATAED(fcd.ANFCD_DATA_EMISSAO) INTO #r from VNDAPECD ecd, VNDANFCD fcd, VNDANFLN fln where ecd.APECD_CLIENTE = fcd.ANFCD_CLIENTE AND fln.ANFLN_NUM_NOTA = fcd.ANFCD_NUM_NOTA AND fln.ANFLN_PEDIDO = ecd.APECD_PEDIDO AND fcd.ANFCD_TIPO_OPER = 'NF1' AND datediff(day,ecd.APECD_DATA_CADAST,getdate()) <= 365 GROUP BY fcd.ANFCD_DATA_EMISSAO, ecd.APECD_CLIENTE, fcd.ANFCD_TOT_NOTA order by fcd.ANFCD_DATA_EMISSAO DESC;")
        conn.cursor().execute(
            "select secd.APECD_CLIENTE, sfcd.ANFCD_TOT_NOTA, sum(sfln.ANFLN_QTD_IMP), DATAED(sfcd.ANFCD_DATA_EMISSAO) INTO #t from VNDAPECD secd, VNDANFCD sfcd, VNDANFLN sfln, VNDANFCA sfca where secd.APECD_CLIENTE = sfcd.ANFCD_CLIENTE AND sfln.ANFLN_NUM_NOTA = sfcd.ANFCD_NUM_NOTA AND sfcd.ANFCD_NUM_NOTA = sfca.NUMERO_NFF AND sfln.ANFLN_PEDIDO = secd.APECD_PEDIDO AND sfcd.ANFCD_TIPO_OPER = 'NF1' AND datediff(day,secd.APECD_DATA_CADAST,getdate()) <= 365 GROUP BY sfcd.ANFCD_DATA_EMISSAO, secd.APECD_CLIENTE, sfcd.ANFCD_TOT_NOTA order by sfcd.ANFCD_DATA_EMISSAO DESC;")
        conn.cursor().execute(
            "select * INTO #ultimoPedido from #r EXCEPT select * from #t;")
        conn.cursor().execute(
            "select AEMFD_CODIGO as cod, AEMFD_COND_PGTO as PGTOPW into #condicaoPW from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 1")
        conn.cursor().execute(
            "select AEMFD_CODIGO as cod, AEMFD_COND_PGTO as PGTOPC into #condicaoPC from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 2")
        conn.cursor().execute(
            "select AEMFD_CODIGO as cod, AEMFD_COND_PGTO as PGTOPL into #condicaoPL from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 3")
        clientes = conn.cursor().execute(
            "SELECT b.REPRE, b.ZONA, b.MERCADO, b.ROTA, b.ST, b.CODIGO, b.FANTASIA, s.AEMPR_RAZAO_SOCIAL, s.AEMPR_RUA_AV as RUA, s.AEMPR_NRO as NUMERO, s.AEMPR_COMPL as COMPLEMENTO, b.BAIRRO, b.CIDADE, b.CEP, b.UF, b.CONTATO, b.TELEFONE, s.AEMPR_TELEX_CONT1 as CELULAR_1 , s.AEMPR_TELEX_CONT2 as CELULAR_2, s.AEMPR_TELEX_CONT3 as CELULAR_3,isnull((select tot from #pedidosabertos where cod = b.CODIGO),0) as PEDIDO,isnull((select tot from #atrasocliente where cod = b.CODIGO),0) as VENCIDO,isnull((select tot from #dividacliente where cod = b.CODIGO),0) as ABERTO,(select cred from #credito where emp = b.CODIGO) as Credito,isnull((select first ANFCD_TOT_NOTA from #ultimoPedido where APECD_CLIENTE = b.CODIGO),0) as TOT_NOTA,isnull((select first expression from #ultimoPedido where APECD_CLIENTE = b.CODIGO),0) as NR_CX,isnull((select first expression1 from #ultimoPedido where APECD_CLIENTE = b.CODIGO),\'00000000\') as DT_EMISSAO, isnull((select AEMFD_TABELA_PRECO from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 1 AND AEMFD_CODIGO = b.CODIGO),\'00001\') as TAB_PW,isnull((select AEMFD_TABELA_PRECO from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 2 AND AEMFD_CODIGO = b.CODIGO),\'00001\') as TAB_PC,isnull((select AEMFD_TABELA_PRECO from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 3 AND AEMFD_CODIGO = b.CODIGO),\'00001\') as TAB_PL, ( select PGTOPW from #condicaoPW where cod = b.CODIGO ), ( select PGTOPC from #condicaoPC where cod = b.CODIGO ), ( select PGTOPL from #condicaoPL where cod = b.CODIGO ) FROM BYTEC2.VIEWROTAREPRESENTANTE b, SUPAEMPR s WHERE b.CODIGO = s.AEMPR_CODIGO AND s.AEMPR_TIPO = 'C'")
        lista_cliente = []
        for x in clientes:
            cliente = {"representante": x.REPRE, "zona": x.ZONA, "mercado": x.MERCADO, "rota": x.ROTA, "status": x.ST,
                       "codigo": x.CODIGO,
                       "fantasia": x.FANTASIA, "razao_social": x.AEMPR_RAZAO_SOCIAL,
                       "endereco": {"rua": x.RUA, "numero": int(x.NUMERO),
                                    "complemento": x.COMPLEMENTO,
                                    "bairro": x.BAIRRO,
                                    "cidade": x.CIDADE, "cep": int(x.CEP),
                                    "uf": x.UF},
                       "telefones": {"fixo": x.TELEFONE, "celular_0": x.CELULAR_1, "celular_1": x.CELULAR_2,
                                     "celular_2": x.CELULAR_3},
                       "emails": self.getEmails(codigo=x.CODIGO),
                       "credito": {"pedido": float(x.PEDIDO), "aberto": float(x.ABERTO), "vencido": float(x.VENCIDO),
                                   "limite": float(x.Credito)},
                       "ultimo_pedido": {"quantidade_caixas": int(x.NR_CX), "total": float(x.TOT_NOTA),
                                         "emissao": (x.DT_EMISSAO[0:3] + "/" + x.DT_EMISSAO[4:5] + "/" + x.DT_EMISSAO[
                                                                                                         6:7])},
                       "tabela_de_preco": {"prowater": x.TAB_PW, "proclean": x.TAB_PC, "prolimp": x.TAB_PL},
                       "condicao_de_pagamento": {"prowater": x.PGTOPW, "proclean": x.PGTOPC, "prolimp": x.PGTOPL}}
            lista_cliente.append(cliente)
        conn.close()
        return lista_cliente

    def infoFirst(self):
        conn = pyodbc.connect(
            Dsn="PW32", uid="BYTEC", pwd="BYTEC")
        conn.cursor().execute(
            "SELECT b.REPRE as repre, b.ZONA as zona, b.MERCADO as mercado, b.ROTA as rota, b.ST as st, b.CODIGO as cod, b.FANTASIA as fant into #cliente FROM BYTEC2.VIEWROTAREPRESENTANTE b;")
        conn.cursor().execute(
            "SELECT CodigoEmpresa as emp, LimiteCred as cred into #credito FROM InfoCredCFT WHERE TipoEmpresa = \'C\';")
        conn.cursor().execute(
            "SELECT APEPC_EMPRESA as emp, APEPC_PEDIDO as ped, sum(APEPC_QTD_PEDIDA*APEPC_VALOR_ENC) as tot into #liberado FROM VNDAPEPC where APEPC_STATUS = \'L\' GROUP BY ped,emp;")
        conn.cursor().execute(
            "SELECT APECD_EMPREsA as emp, APECD_PEDIDO as ped, APECD_CLIENTE as cod into #clientepedido FROM VNDAPECD where APECD_TIPO_CLI = \'C\';")
        conn.cursor().execute(
            "SELECT ANFLN_EMPRESA as emp, ANFLN_PEDIDO as ped, ANFLN_NUM_NOTA as nota into #notapedido FROM VNDANFLN;")
        conn.cursor().execute(
            "SELECT codigoemp as emp, numero as nota, sum(valor+valorjuros) as tot into #pendente FROM ParcelaR where isnull(datediff(day,recebimento,getdate()),-1) = -1 GROUP BY emp, nota;")
        conn.cursor().execute(
            "SELECT ido.cod as cod, sum(ado.tot) as tot into #pedidosabertos FROM #clientepedido ido,#liberado ado WHERE ado.ped = ido.ped and ado.emp = ido.emp GROUP BY ido.cod;")
        conn.cursor().execute(
            "SELECT mpr.AEMPR_STATUS as ST,fcd.ANFCD_CLIENTE AS CLI, mpr.AEMPR_NOME_ABREV AS FANTASIA,fcd.ANFCD_EMPRESA AS EMP,fcd.ANFCD_NUM_NOTA AS NOTA, lar.VALOR as valor, lar.valorjuros as juros, lar.PARCELA as PARC, datediff(day,lar.Vencimento,now()) as vencido into #devendo FROM SUPAEMPR mpr, VNDANFCD fcd,VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND datediff(day,lar.Vencimento,now()) <= 0;")
        conn.cursor().execute("select cli as cod,sum(valor) as tot into #dividacliente from #devendo GROUP BY cli;")
        conn.cursor().execute(
            "SELECT fcd.ANFCD_CLIENTE AS cod, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, datediff(day,lar.Vencimento,now()) as vencido, lar.PARCELA as PARC, lar.VALOR as valor into #atrasado FROM     SUPAEMPR mpr,    VNDANFCD fcd,    VNDAEMDF mdf,    PARCELAR lar,    BYTEC2.VIEWROTAREPRESENTANTE nte where    fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND    fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND    fcd.ANFCD_CLIENTE = nte.CODIGO AND    fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND    fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND    fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND    fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND    SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND    lar.RECEBIMENTO IS NULL AND     lar.VENCIMENTO+1 <= now() EXCEPT (SELECT fcd.ANFCD_CLIENTE AS CLI, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, datediff(day,lar.Vencimento,now()) as \"D VNC\", lar.PARCELA as PARC, lar.VALOR FROM SUPAEMPR mpr, VNDANFCD fcd, VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND lar.VENCIMENTO+1 <= now() AND lar.Vencimento = fcd.ANFCD_DATA_EMISSAO AND datediff(day,lar.Vencimento,now()) <= 2);")
        conn.cursor().execute(
            "select cod as cod,sum(valor+valor*0.004*vencido) as tot into #atrasocliente from #Atrasado where vencido > 0 GROUP BY cod;")
        conn.cursor().execute(
            "select ecd.APECD_CLIENTE, fcd.ANFCD_TOT_NOTA, sum(fln.ANFLN_QTD_IMP), DATAED(fcd.ANFCD_DATA_EMISSAO) INTO #r from VNDAPECD ecd, VNDANFCD fcd, VNDANFLN fln where ecd.APECD_CLIENTE = fcd.ANFCD_CLIENTE AND fln.ANFLN_NUM_NOTA = fcd.ANFCD_NUM_NOTA AND fln.ANFLN_PEDIDO = ecd.APECD_PEDIDO AND fcd.ANFCD_TIPO_OPER = 'NF1' AND datediff(day,ecd.APECD_DATA_CADAST,getdate()) <= 365 GROUP BY fcd.ANFCD_DATA_EMISSAO, ecd.APECD_CLIENTE, fcd.ANFCD_TOT_NOTA order by fcd.ANFCD_DATA_EMISSAO DESC;")
        conn.cursor().execute(
            "select secd.APECD_CLIENTE, sfcd.ANFCD_TOT_NOTA, sum(sfln.ANFLN_QTD_IMP), DATAED(sfcd.ANFCD_DATA_EMISSAO) INTO #t from VNDAPECD secd, VNDANFCD sfcd, VNDANFLN sfln, VNDANFCA sfca where secd.APECD_CLIENTE = sfcd.ANFCD_CLIENTE AND sfln.ANFLN_NUM_NOTA = sfcd.ANFCD_NUM_NOTA AND sfcd.ANFCD_NUM_NOTA = sfca.NUMERO_NFF AND sfln.ANFLN_PEDIDO = secd.APECD_PEDIDO AND sfcd.ANFCD_TIPO_OPER = 'NF1' AND datediff(day,secd.APECD_DATA_CADAST,getdate()) <= 365 GROUP BY sfcd.ANFCD_DATA_EMISSAO, secd.APECD_CLIENTE, sfcd.ANFCD_TOT_NOTA order by sfcd.ANFCD_DATA_EMISSAO DESC;")
        conn.cursor().execute("select * INTO #ultimoPedido from #r EXCEPT select * from #t;")
        clientes = conn.cursor().execute(
            "SELECT b.REPRE, b.ZONA, b.MERCADO, b.ROTA, b.ST, b.CODIGO, b.FANTASIA, s.AEMPR_RAZAO_SOCIAL, s.AEMPR_RUA_AV as RUA, s.AEMPR_NRO as NUMERO, s.AEMPR_COMPL as COMPLEMENTO, b.BAIRRO, b.CIDADE, b.CEP, b.UF, b.CONTATO, b.TELEFONE, s.AEMPR_TELEX_CONT1 as CELULAR_1 , s.AEMPR_TELEX_CONT2 as CELULAR_2, s.AEMPR_TELEX_CONT3 as CELULAR_3,isnull((select tot from #pedidosabertos where cod = b.CODIGO),0) as PEDIDO,isnull((select tot from #atrasocliente where cod = b.CODIGO),0) as VENCIDO,isnull((select tot from #dividacliente where cod = b.CODIGO),0) as ABERTO,(select cred from #credito where emp = b.CODIGO) as Credito,isnull((select first ANFCD_TOT_NOTA from #ultimoPedido where APECD_CLIENTE = b.CODIGO),0) as TOT_NOTA,isnull((select first expression from #ultimoPedido where APECD_CLIENTE = b.CODIGO),0) as NR_CX,isnull((select first expression1 from #ultimoPedido where APECD_CLIENTE = b.CODIGO),'00000000') as DT_EMISSAO, isnull((select AEMFD_TABELA_PRECO from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 1 AND AEMFD_CODIGO = b.CODIGO),\'00001\') as TAB_PW,isnull((select AEMFD_TABELA_PRECO from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 2 AND AEMFD_CODIGO = b.CODIGO),\'00001\') as TAB_PC,isnull((select AEMFD_TABELA_PRECO from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 3 AND AEMFD_CODIGO = b.CODIGO),\'00001\') as TAB_PL FROM BYTEC2.VIEWROTAREPRESENTANTE b, SUPAEMPR s WHERE b.CODIGO = s.AEMPR_CODIGO AND s.AEMPR_TIPO = 'C'")
        lista_cliente = []
        print(clientes.description)
        for x in clientes:
            cliente = {"representante": x.REPRE, "zona": x.ZONA, "mercado": x.MERCADO, "rota": x.ROTA, "status": x.ST,
                       "codigo": x.CODIGO,
                       "fantasia": x.FANTASIA, "razao_social": x.AEMPR_RAZAO_SOCIAL,
                       "endereco": {"rua": x.RUA, "numero": int(x.NUMERO),
                                    "complemento": x.COMPLEMENTO,
                                    "bairro": x.BAIRRO,
                                    "cidade": x.CIDADE, "cep": int(x.CEP),
                                    "uf": x.UF},
                       "telefones": {"fixo": x.TELEFONE, "celular_0": x.CELULAR_1, "celular_1": x.CELULAR_2,
                                     "celular_2": x.CELULAR_3},
                       "emails": self.getEmails(codigo=x.CODIGO),
                       "credito": {"pedido": float(x.PEDIDO), "aberto": float(x.ABERTO), "vencido": float(x.VENCIDO),
                                   "limite": float(x.Credito)},
                       "ultimo_pedido": {"quantidade_caixas": int(x.NR_CX), "total": float(x.TOT_NOTA),
                                         "emissao": (x.DT_EMISSAO[0:3] + "/" + x.DT_EMISSAO[4:5] + "/" + x.DT_EMISSAO[
                                                                                                         6:7])},
                       "tabela_de_preco": {"prowater": x.TAB_PW, "proclean": x.TAB_PC, "prolimp": x.TAB_PL}}
            lista_cliente.append(cliente)
        conn.close()
        return lista_cliente


class TabelaPreco:
    def tabela(self):
        conn = pyodbc.connect(
            Dsn="PW32", uid="BYTEC", pwd="BYTEC")
        tabela_preco = conn.cursor().execute(
            "select ( case ATITM_EMPRESA when 1 then 'prowater' when 2 then 'proclean' when 3 then 'prolimp'end CASE ) as emp, ATITM_TABELA_PRECO as tabela, ATITM_COD_ITEM as cod, ATITM_VALOR as valor from VNDATITM  where datediff(year,ATITM_DATA_FIN,getdate()) = 0 order by ATITM_DATA_FIN desc")
        lista_tabela_preco = []
        for item in tabela_preco:
            temp = {"empresa": item.emp, "codigo": item.cod, "valor": float(item.valor), "tabela": item.tabela}
            lista_tabela_preco.append(temp)
        conn.close()
        print(lista_tabela_preco)
        return lista_tabela_preco


class Cobrancas:
    def cobrancas(self):
        conn = pyodbc.connect(
            Dsn="PW32", uid="BYTEC", pwd="BYTEC")
        cobrancas = conn.cursor().execute(
            "SELECT mpr.AEMPR_REPR AS REPR,fcd.ANFCD_CLIENTE AS CLI,( case fcd.ANFCD_EMPRESA when 1 then 'prowater' when 2 then 'proclean' when 3 then 'prolimp'end CASE ) AS EMP,fcd.ANFCD_NUM_NOTA AS NOTA,(select ANFLN_PEDIDO as PED from VNDANFLN WHERE ANFLN_EMPRESA = fcd.ANFCD_EMPRESA AND ANFLN_NUM_NOTA = NOTA GROUP BY PED),    DATAED(fcd.ANFCD_DATA_EMISSAO) AS EMISSAO, DATAEF(lar.VENCIMENTO) AS VCTO, lar.PARCELA as PARC, lar.VALOR FROM SUPAEMPR mpr, VNDANFCD fcd, VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND  lar.VENCIMENTO+1 <= now() EXCEPT ( SELECT mpr.AEMPR_REPR AS REPR, fcd.ANFCD_CLIENTE AS CLI, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, (select ANFLN_PEDIDO as pedido from VNDANFLN WHERE ANFLN_EMPRESA = fcd.ANFCD_EMPRESA AND ANFLN_NUM_NOTA = NOTA GROUP BY pedido), DATAED(fcd.ANFCD_DATA_EMISSAO) AS EMISSAO,  DATAEF(lar.VENCIMENTO) AS VCTO, lar.PARCELA as PARC, lar.VALOR FROM SUPAEMPR mpr, VNDANFCD fcd, VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND  lar.VENCIMENTO+1 <= now() AND  lar.Vencimento = fcd.ANFCD_DATA_EMISSAO AND  datediff(day,lar.Vencimento,now()) <= 2)")
        lista_de_cobrancas = []
        for item in cobrancas:
            temp = {"representante": item.REPR, "cliente": item.CLI, "empresa": item.EMP, "nota_fiscal": item.NOTA,
                    "pedido": item.PED, "vencimento": item.VCTO, "emissao": item.EMISSAO, "parcela": item.PARC, "valor": float(item.VALOR)}
            lista_de_cobrancas.append(temp)
        conn.close()
        return lista_de_cobrancas
