def clientes():
    return (
        [
            "SELECT REPRE as repre, ZONA as zona, MERCADO as mercado, ROTA as rota, ST as st, CODIGO as cod, FANTASIA as fant into #cliente FROM BYTEC2.VIEWROTAREPRESENTANTE;",
            "SELECT CodigoEmpresa as emp, LimiteCred as cred into #credito FROM InfoCredCFT WHERE TipoEmpresa = \'C\';",
            "SELECT APEPC_EMPRESA as emp, APEPC_PEDIDO as ped, sum(APEPC_QTD_PEDIDA*APEPC_VALOR_ENC) as tot into #liberado FROM VNDAPEPC where APEPC_STATUS = \'L\' GROUP BY ped,emp;",
            "SELECT APECD_EMPREsA as emp, APECD_PEDIDO as ped, APECD_CLIENTE as cod into #clientepedido FROM VNDAPECD where APECD_TIPO_CLI = \'C\';",
            "SELECT ANFLN_EMPRESA as emp, ANFLN_PEDIDO as ped, ANFLN_NUM_NOTA as nota into #notapedido FROM VNDANFLN;",
            "SELECT codigoemp as emp, numero as nota, sum(valor+valorjuros) as tot into #pendente FROM ParcelaR where isnull(datediff(day,recebimento,getdate()),-1) = -1 GROUP BY emp, nota;",
            "SELECT ido.cod as cod, sum(ado.tot) as tot into #pedidosabertos FROM #clientepedido ido,#liberado ado WHERE ado.ped = ido.ped and ado.emp = ido.emp GROUP BY ido.cod;",
            "SELECT mpr.AEMPR_STATUS as ST,fcd.ANFCD_CLIENTE AS CLI, mpr.AEMPR_NOME_ABREV AS FANTASIA,fcd.ANFCD_EMPRESA AS EMP,fcd.ANFCD_NUM_NOTA AS NOTA, lar.VALOR as valor, lar.valorjuros as juros, lar.PARCELA as PARC, datediff(day,lar.Vencimento,now()) as vencido into #devendo FROM SUPAEMPR mpr, VNDANFCD fcd,VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND datediff(day,lar.Vencimento,now()) <= 0;",
            "select cli as cod,sum(valor) as tot into #dividacliente from #devendo GROUP BY cli;",
            "SELECT fcd.ANFCD_CLIENTE AS cod, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, datediff(day,lar.Vencimento,now()) as vencido, lar.PARCELA as PARC, lar.VALOR as valor into #atrasado FROM     SUPAEMPR mpr,VNDANFCD fcd,VNDAEMDF mdf,PARCELAR lar,BYTEC2.VIEWROTAREPRESENTANTE nte where  fcd.ANFCD_TIPO_EMPR = 'C' AND  fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND    fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND    fcd.ANFCD_CLIENTE = nte.CODIGO AND    fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND    fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND    fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND    fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND    SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND    lar.RECEBIMENTO IS NULL AND     lar.VENCIMENTO+1 <= now() EXCEPT (SELECT fcd.ANFCD_CLIENTE AS CLI, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, datediff(day,lar.Vencimento,now()) as \"D VNC\", lar.PARCELA as PARC, lar.VALOR FROM SUPAEMPR mpr, VNDANFCD fcd, VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = 'C' AND fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND fcd.ANFCD_TIPO_EMPR = 'C' AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND lar.VENCIMENTO+1 <= now() AND lar.Vencimento = fcd.ANFCD_DATA_EMISSAO AND datediff(day,lar.Vencimento,now()) <= 2);",
            "select cod as cod,sum(valor+valor*0.004*vencido) as tot into #atrasocliente from #Atrasado where vencido > 0 GROUP BY cod;",
            "select ecd.APECD_CLIENTE, fcd.ANFCD_TOT_NOTA, sum(fln.ANFLN_QTD_IMP), (fcd.ANFCD_DATA_EMISSAO) INTO #r from VNDAPECD ecd, VNDANFCD fcd, VNDANFLN fln where ecd.APECD_CLIENTE = fcd.ANFCD_CLIENTE AND fln.ANFLN_NUM_NOTA = fcd.ANFCD_NUM_NOTA AND fln.ANFLN_PEDIDO = ecd.APECD_PEDIDO AND fcd.ANFCD_TIPO_OPER = 'NF1' AND datediff(day,ecd.APECD_DATA_CADAST,getdate()) <= 365 GROUP BY fcd.ANFCD_DATA_EMISSAO, ecd.APECD_CLIENTE, fcd.ANFCD_TOT_NOTA order by fcd.ANFCD_DATA_EMISSAO DESC;",
            "select secd.APECD_CLIENTE, sfcd.ANFCD_TOT_NOTA, sum(sfln.ANFLN_QTD_IMP), (sfcd.ANFCD_DATA_EMISSAO) INTO #t from VNDAPECD secd, VNDANFCD sfcd, VNDANFLN sfln, VNDANFCA sfca where secd.APECD_CLIENTE = sfcd.ANFCD_CLIENTE AND sfln.ANFLN_NUM_NOTA = sfcd.ANFCD_NUM_NOTA AND sfcd.ANFCD_NUM_NOTA = sfca.NUMERO_NFF AND sfln.ANFLN_PEDIDO = secd.APECD_PEDIDO AND sfcd.ANFCD_TIPO_OPER = 'NF1' AND datediff(day,secd.APECD_DATA_CADAST,getdate()) <= 365 GROUP BY sfcd.ANFCD_DATA_EMISSAO, secd.APECD_CLIENTE, sfcd.ANFCD_TOT_NOTA order by sfcd.ANFCD_DATA_EMISSAO DESC;",
            "select * INTO #ultimoPedido from #r EXCEPT select * from #t;",
            "select AEMFD_CODIGO as cod, AEMFD_COND_PGTO as PGTOPW into #condicaoPW from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 1",
            "select AEMFD_CODIGO as cod, AEMFD_COND_PGTO as PGTOPC into #condicaoPC from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 2",
            "select AEMFD_CODIGO as cod, AEMFD_COND_PGTO as PGTOPL into #condicaoPL from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 3",
            "select AEMFD_CODIGO as cod, AEMFD_COND_PGTO as PGTOPN into #condicaoPN from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 4",
            "SELECT b.REPRE, b.ZONA, b.MERCADO, b.ROTA, b.ST, b.CODIGO, b.FANTASIA, s.AEMPR_RAZAO_SOCIAL, s.AEMPR_RUA_AV as RUA, s.AEMPR_NRO as NUMERO, s.AEMPR_COMPL as COMPLEMENTO, b.BAIRRO, b.CIDADE, b.CEP, b.UF, b.CONTATO, b.TELEFONE, s.AEMPR_TELEX_CONT1 as CELULAR_1 , s.AEMPR_TELEX_CONT2 as CELULAR_2, s.AEMPR_TELEX_CONT3 as CELULAR_3,isnull((select tot from #pedidosabertos where cod = b.CODIGO),0) as PEDIDO,isnull((select tot from #atrasocliente where cod = b.CODIGO),0) as VENCIDO,isnull((select tot from #dividacliente where cod = b.CODIGO),0) as ABERTO,(select cred from #credito where emp = b.CODIGO) as Credito,isnull((select first ANFCD_TOT_NOTA from #ultimoPedido where APECD_CLIENTE = b.CODIGO),0) as TOT_NOTA,isnull((select first expression from #ultimoPedido where APECD_CLIENTE = b.CODIGO),0) as NR_CX,isnull((select first ANFCD_DATA_EMISSAO from #ultimoPedido where APECD_CLIENTE = b.CODIGO),\'00000000\') as DT_EMISSAO, isnull((select AEMFD_TABELA_PRECO from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 1 AND AEMFD_CODIGO = b.CODIGO),\'00001\') as TAB_PW,isnull((select AEMFD_TABELA_PRECO from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 2 AND AEMFD_CODIGO = b.CODIGO),\'00001\') as TAB_PC,isnull((select AEMFD_TABELA_PRECO from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 3 AND AEMFD_CODIGO = b.CODIGO),\'00001\') as TAB_PL, ( select PGTOPW from #condicaoPW where cod = b.CODIGO ), ( select PGTOPC from #condicaoPC where cod = b.CODIGO ), ( select PGTOPL from #condicaoPL where cod = b.CODIGO ), ( select PGTOPN from #condicaoPN where cod = b.CODIGO ) FROM BYTEC2.VIEWROTAREPRESENTANTE b, SUPAEMPR s WHERE b.CODIGO = s.AEMPR_CODIGO AND s.AEMPR_TIPO = 'C'"]
    )


def tabela4():
    return ("select ATITM_EMPRESA as EMP, ATITM_COD_ITEM as ITEM, ATITM_TABELA_PRECO as TABELA, cast(ATITM_DATA_INICIAL as DATETIME) as DT_INI, cast(ATITM_DATA_FIN as DATETIME) as DT_FIN, ATITM_VALOR as VALOR from  VNDATITM  where  TABELA = '00001' AND  DT_FIN = (select max(cast(ATITM_DATA_FIN as DATETIME)) as DT from VNDATITM WHERE ATITM_EMPRESA = 4) AND  EMP = 4 ORDER BY  EMP, DT_FIN DESC")


def emailporcodigo(codigo, tipo):
    return (
        f"select AMAIL_IDENTIFICA as descr, AMAIL_E_MAIL_WWW as email_site from SUPAMAIL where AMAIL_TIPO = '{tipo}' and AMAIL_CODIGO = {codigo};")


def clienteporcodigo(codigo):
    return (
        [
            f"SELECT REPRE as repre, ZONA as zona, MERCADO as mercado, ROTA as rota, ST as st, CODIGO as cod, FANTASIA as fant into #cliente FROM BYTEC2.VIEWROTAREPRESENTANTE WHERE CODIGO = {codigo};",
            "SELECT CodigoEmpresa as emp, LimiteCred as cred into #credito FROM InfoCredCFT WHERE TipoEmpresa = \'C\';",
            "SELECT APEPC_EMPRESA as emp, APEPC_PEDIDO as ped, sum(APEPC_QTD_PEDIDA*APEPC_VALOR_ENC) as tot into #liberado FROM VNDAPEPC where APEPC_STATUS = \'L\' GROUP BY ped,emp;",
            f"SELECT APECD_EMPREsA as emp, APECD_PEDIDO as ped, APECD_CLIENTE as cod into #clientepedido FROM VNDAPECD where APECD_TIPO_CLI = \'C\' AND APECD_CLIENTE = {codigo};",
            "SELECT ANFLN_EMPRESA as emp, ANFLN_PEDIDO as ped, ANFLN_NUM_NOTA as nota into #notapedido FROM VNDANFLN;",
            "SELECT codigoemp as emp, numero as nota, sum(valor+valorjuros) as tot into #pendente FROM ParcelaR where isnull(datediff(day,recebimento,getdate()),-1) = -1 GROUP BY emp, nota;",
            "SELECT ido.cod as cod, sum(ado.tot) as tot into #pedidosabertos FROM #clientepedido ido,#liberado ado WHERE ado.ped = ido.ped and ado.emp = ido.emp GROUP BY ido.cod;",
            f"SELECT mpr.AEMPR_STATUS as ST,fcd.ANFCD_CLIENTE AS CLI, mpr.AEMPR_NOME_ABREV AS FANTASIA,fcd.ANFCD_EMPRESA AS EMP,fcd.ANFCD_NUM_NOTA AS NOTA, lar.VALOR as valor, lar.valorjuros as juros, lar.PARCELA as PARC, datediff(day,lar.Vencimento,now()) as vencido into #devendo FROM SUPAEMPR mpr, VNDANFCD fcd,VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = {codigo} AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND datediff(day,lar.Vencimento,now()) <= 0;",
            "select cli as cod,sum(valor) as tot into #dividacliente from #devendo GROUP BY cli;",
            f"SELECT fcd.ANFCD_CLIENTE AS cod, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, datediff(day,lar.Vencimento,now()) as vencido, lar.PARCELA as PARC, lar.VALOR as valor into #atrasado FROM     SUPAEMPR mpr,VNDANFCD fcd,VNDAEMDF mdf,PARCELAR lar,BYTEC2.VIEWROTAREPRESENTANTE nte where  fcd.ANFCD_TIPO_EMPR = 'C' AND  fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND    fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = {codigo} AND fcd.ANFCD_CLIENTE = nte.CODIGO AND    fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND    fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND    fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND    fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND    SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND    lar.RECEBIMENTO IS NULL AND     lar.VENCIMENTO+1 <= now() EXCEPT (SELECT fcd.ANFCD_CLIENTE AS CLI, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, datediff(day,lar.Vencimento,now()) as \"D VNC\", lar.PARCELA as PARC, lar.VALOR FROM SUPAEMPR mpr, VNDANFCD fcd, VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = 'C' AND fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = {codigo} AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND fcd.ANFCD_TIPO_EMPR = 'C' AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND lar.VENCIMENTO+1 <= now() AND lar.Vencimento = fcd.ANFCD_DATA_EMISSAO AND datediff(day,lar.Vencimento,now()) <= 2);",
            f"select cod as cod,sum(valor+valor*0.004*vencido) as tot into #atrasocliente from #Atrasado where vencido > 0 AND cod = {codigo} GROUP BY cod;",
            f"select ecd.APECD_CLIENTE, fcd.ANFCD_TOT_NOTA, sum(fln.ANFLN_QTD_IMP), (fcd.ANFCD_DATA_EMISSAO) INTO #r from VNDAPECD ecd, VNDANFCD fcd, VNDANFLN fln where ecd.APECD_CLIENTE = {codigo} AND ecd.APECD_CLIENTE = fcd.ANFCD_CLIENTE AND fln.ANFLN_NUM_NOTA = fcd.ANFCD_NUM_NOTA AND fln.ANFLN_PEDIDO = ecd.APECD_PEDIDO AND fcd.ANFCD_TIPO_OPER = 'NF1' AND datediff(day,ecd.APECD_DATA_CADAST,getdate()) <= 365 GROUP BY fcd.ANFCD_DATA_EMISSAO, ecd.APECD_CLIENTE, fcd.ANFCD_TOT_NOTA order by fcd.ANFCD_DATA_EMISSAO DESC;",
            f"select secd.APECD_CLIENTE, sfcd.ANFCD_TOT_NOTA, sum(sfln.ANFLN_QTD_IMP), (sfcd.ANFCD_DATA_EMISSAO) INTO #t from VNDAPECD secd, VNDANFCD sfcd, VNDANFLN sfln, VNDANFCA sfca where secd.APECD_CLIENTE = {codigo} AND secd.APECD_CLIENTE = sfcd.ANFCD_CLIENTE AND sfln.ANFLN_NUM_NOTA = sfcd.ANFCD_NUM_NOTA AND sfcd.ANFCD_NUM_NOTA = sfca.NUMERO_NFF AND sfln.ANFLN_PEDIDO = secd.APECD_PEDIDO AND sfcd.ANFCD_TIPO_OPER = 'NF1' AND datediff(day,secd.APECD_DATA_CADAST,getdate()) <= 365 GROUP BY sfcd.ANFCD_DATA_EMISSAO, secd.APECD_CLIENTE, sfcd.ANFCD_TOT_NOTA order by sfcd.ANFCD_DATA_EMISSAO DESC;",
            "select * INTO #ultimoPedido from #r EXCEPT select * from #t;",
            "select AEMFD_CODIGO as cod, AEMFD_COND_PGTO as PGTOPW into #condicaoPW from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 1",
            "select AEMFD_CODIGO as cod, AEMFD_COND_PGTO as PGTOPC into #condicaoPC from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 2",
            "select AEMFD_CODIGO as cod, AEMFD_COND_PGTO as PGTOPL into #condicaoPL from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 3",
            "select AEMFD_CODIGO as cod, AEMFD_COND_PGTO as PGTOPN into #condicaoPN from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 4",
            f"SELECT b.REPRE, b.ZONA, b.MERCADO, b.ROTA, b.ST, b.CODIGO, b.FANTASIA, s.AEMPR_RAZAO_SOCIAL, s.AEMPR_RUA_AV as RUA, s.AEMPR_NRO as NUMERO, s.AEMPR_COMPL as COMPLEMENTO, b.BAIRRO, b.CIDADE, b.CEP, b.UF, b.CONTATO, b.TELEFONE, s.AEMPR_TELEX_CONT1 as CELULAR_1 , s.AEMPR_TELEX_CONT2 as CELULAR_2, s.AEMPR_TELEX_CONT3 as CELULAR_3,isnull((select tot from #pedidosabertos where cod = b.CODIGO),0) as PEDIDO,isnull((select tot from #atrasocliente where cod = b.CODIGO),0) as VENCIDO,isnull((select tot from #dividacliente where cod = b.CODIGO),0) as ABERTO,(select cred from #credito where emp = b.CODIGO) as Credito,isnull((select first ANFCD_TOT_NOTA from #ultimoPedido where APECD_CLIENTE = b.CODIGO),0) as TOT_NOTA,isnull((select first expression from #ultimoPedido where APECD_CLIENTE = b.CODIGO),0) as NR_CX,isnull((select first ANFCD_DATA_EMISSAO from #ultimoPedido where APECD_CLIENTE = b.CODIGO),\'00000000\') as DT_EMISSAO, isnull((select AEMFD_TABELA_PRECO from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 1 AND AEMFD_CODIGO = b.CODIGO),\'00001\') as TAB_PW,isnull((select AEMFD_TABELA_PRECO from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 2 AND AEMFD_CODIGO = b.CODIGO),\'00001\') as TAB_PC,isnull((select AEMFD_TABELA_PRECO from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 3 AND AEMFD_CODIGO = b.CODIGO),\'00001\') as TAB_PL, ( select PGTOPW from #condicaoPW where cod = b.CODIGO ), ( select PGTOPC from #condicaoPC where cod = b.CODIGO ), ( select PGTOPL from #condicaoPL where cod = b.CODIGO ), ( select PGTOPN from #condicaoPN where cod = b.CODIGO ) FROM BYTEC2.VIEWROTAREPRESENTANTE b, SUPAEMPR s WHERE b.CODIGO = s.AEMPR_CODIGO AND s.AEMPR_TIPO = 'C' AND b.CODIGO = {codigo}"]
    )


'''def clienteporcodigo(codigo):
    return (
        [
            f"SELECT b.REPRE as repre, b.ZONA as zona, b.MERCADO as mercado, b.ROTA as rota, b.ST as st, b.CODIGO as cod, b.FANTASIA as fant into #cliente FROM BYTEC2.VIEWROTAREPRESENTANTE b WHERE b.CODIGO = {codigo};",
            f"SELECT CodigoEmpresa as emp, LimiteCred as cred into #credito FROM InfoCredCFT WHERE TipoEmpresa = \'C\' AND CodigoEmpresa = {codigo};",
            f"SELECT APEPC_EMPRESA as emp, APEPC_PEDIDO as ped, sum(APEPC_QTD_PEDIDA*APEPC_VALOR_ENC) as tot into #liberado FROM VNDAPEPC where APEPC_STATUS = \'L\' GROUP BY ped,emp;",
            f"SELECT APECD_EMPREsA as emp, APECD_PEDIDO as ped, APECD_CLIENTE as cod into #clientepedido FROM VNDAPECD where APECD_TIPO_CLI = \'C\' AND APECD_CLIENTE = {codigo};",
            f"SELECT ANFLN_EMPRESA as emp, ANFLN_PEDIDO as ped, ANFLN_NUM_NOTA as nota into #notapedido FROM VNDANFLN;",
            f"SELECT codigoemp as emp, numero as nota, sum(valor+valorjuros) as tot into #pendente FROM ParcelaR where isnull(datediff(day,recebimento,getdate()),-1) = -1 GROUP BY emp, nota;",
            f"SELECT ido.cod as cod, sum(ado.tot) as tot into #pedidosabertos FROM #clientepedido ido,#liberado ado WHERE ado.ped = ido.ped and ado.emp = ido.emp and ido.cod = {codigo} GROUP BY ido.cod;",
            f"SELECT mpr.AEMPR_STATUS as ST,fcd.ANFCD_CLIENTE AS CLI, mpr.AEMPR_NOME_ABREV AS FANTASIA,fcd.ANFCD_EMPRESA AS EMP,fcd.ANFCD_NUM_NOTA AS NOTA, lar.VALOR as valor, lar.valorjuros as juros, lar.PARCELA as PARC, datediff(day,lar.Vencimento,now()) as vencido into #devendo FROM SUPAEMPR mpr, VNDANFCD fcd,VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND RIGHT(fcd.ANFCD_NUM_NOTA,8) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND datediff(day,lar.Vencimento,now()) <= 0 AND CLI = {codigo} ;",
            f"select cli as cod,sum(valor) as tot into #dividacliente from #devendo GROUP BY cli;",
            f"SELECT fcd.ANFCD_CLIENTE AS cod, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, datediff(day,lar.Vencimento,now()) as vencido, lar.PARCELA as PARC, lar.VALOR as valor into #atrasado FROM     SUPAEMPR mpr,VNDANFCD fcd,VNDAEMDF mdf,PARCELAR lar,BYTEC2.VIEWROTAREPRESENTANTE nte where    fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND    fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND    fcd.ANFCD_CLIENTE = nte.CODIGO AND    fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND    fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND    fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND    fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND    SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND    lar.RECEBIMENTO IS NULL AND     lar.VENCIMENTO+1 <= now() EXCEPT (SELECT fcd.ANFCD_CLIENTE AS CLI, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, datediff(day,lar.Vencimento,now()) as \"D VNC\", lar.PARCELA as PARC, lar.VALOR FROM SUPAEMPR mpr, VNDANFCD fcd, VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND lar.VENCIMENTO+1 <= now() AND fcd.ANFCD_DATA_EMISSAO != '00000000' AND lar.Vencimento = fcd.ANFCD_DATA_EMISSAO AND datediff(day,lar.Vencimento,now()) <= 2);",
            f"select cod as cod,sum(valor+valor*0.004*vencido) as tot into #atrasocliente from #Atrasado where vencido > 0 GROUP BY cod;",
            f"select ecd.APECD_CLIENTE, fcd.ANFCD_TOT_NOTA, sum(fln.ANFLN_QTD_IMP), (fcd.ANFCD_DATA_EMISSAO) INTO #r from VNDAPECD ecd, VNDANFCD fcd, VNDANFLN fln where ecd.APECD_CLIENTE = fcd.ANFCD_CLIENTE AND fln.ANFLN_NUM_NOTA = fcd.ANFCD_NUM_NOTA AND fln.ANFLN_PEDIDO = ecd.APECD_PEDIDO AND fcd.ANFCD_TIPO_OPER = 'NF1' AND datediff(day,ecd.APECD_DATA_CADAST,getdate()) <= 365 AND ecd.APECD_CLIENTE = {codigo} GROUP BY fcd.ANFCD_DATA_EMISSAO, ecd.APECD_CLIENTE, fcd.ANFCD_TOT_NOTA order by fcd.ANFCD_DATA_EMISSAO DESC;",
            f"select secd.APECD_CLIENTE, sfcd.ANFCD_TOT_NOTA, sum(sfln.ANFLN_QTD_IMP), (sfcd.ANFCD_DATA_EMISSAO) INTO #t from VNDAPECD secd, VNDANFCD sfcd, VNDANFLN sfln, VNDANFCA sfca where secd.APECD_CLIENTE = sfcd.ANFCD_CLIENTE AND sfln.ANFLN_NUM_NOTA = sfcd.ANFCD_NUM_NOTA AND sfcd.ANFCD_NUM_NOTA = sfca.NUMERO_NFF AND sfln.ANFLN_PEDIDO = secd.APECD_PEDIDO AND sfcd.ANFCD_TIPO_OPER = 'NF1' AND datediff(day,secd.APECD_DATA_CADAST,getdate()) <= 365 AND secd.APECD_CLIENTE = {codigo} GROUP BY sfcd.ANFCD_DATA_EMISSAO, secd.APECD_CLIENTE, sfcd.ANFCD_TOT_NOTA order by sfcd.ANFCD_DATA_EMISSAO DESC;",
            f"select * INTO #ultimoPedido from #r EXCEPT select * from #t;",
            f"select AEMFD_CODIGO as cod, AEMFD_COND_PGTO as PGTOPW into #condicaoPW from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 1 AND AEMFD_CODIGO = {codigo}",
            f"select AEMFD_CODIGO as cod, AEMFD_COND_PGTO as PGTOPC into #condicaoPC from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 2 AND AEMFD_CODIGO = {codigo}",
            f"select AEMFD_CODIGO as cod, AEMFD_COND_PGTO as PGTOPL into #condicaoPL from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 3 AND AEMFD_CODIGO = {codigo}",
            f"SELECT b.REPRE, b.ZONA, b.MERCADO, b.ROTA, b.ST, b.CODIGO, b.FANTASIA, s.AEMPR_RAZAO_SOCIAL, s.AEMPR_RUA_AV as RUA, s.AEMPR_NRO as NUMERO, s.AEMPR_COMPL as COMPLEMENTO, b.BAIRRO, b.CIDADE, b.CEP, b.UF, b.CONTATO, b.TELEFONE, s.AEMPR_TELEX_CONT1 as CELULAR_1 , s.AEMPR_TELEX_CONT2 as CELULAR_2, s.AEMPR_TELEX_CONT3 as CELULAR_3,isnull((select tot from #pedidosabertos where cod = b.CODIGO),0) as PEDIDO,isnull((select tot from #atrasocliente where cod = b.CODIGO),0) as VENCIDO,isnull((select tot from #dividacliente where cod = b.CODIGO),0) as ABERTO,(select cred from #credito where emp = b.CODIGO) as Credito,isnull((select first ANFCD_TOT_NOTA from #ultimoPedido where APECD_CLIENTE = b.CODIGO),0) as TOT_NOTA,isnull((select first expression from #ultimoPedido where APECD_CLIENTE = b.CODIGO),0) as NR_CX,isnull((select first ANFCD_DATA_EMISSAO from #ultimoPedido where APECD_CLIENTE = b.CODIGO),\'00000000\') as DT_EMISSAO, isnull((select AEMFD_TABELA_PRECO from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 1 AND AEMFD_CODIGO = b.CODIGO),\'00001\') as TAB_PW,isnull((select AEMFD_TABELA_PRECO from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 2 AND AEMFD_CODIGO = b.CODIGO),\'00001\') as TAB_PC,isnull((select AEMFD_TABELA_PRECO from VNDAEMFD where AEMFD_TIPO = \'C\' AND AEMFD_EMPRESA = 3 AND AEMFD_CODIGO = b.CODIGO),\'00001\') as TAB_PL, ( select PGTOPW from #condicaoPW where cod = b.CODIGO ), ( select PGTOPC from #condicaoPC where cod = b.CODIGO ), ( select PGTOPL from #condicaoPL where cod = b.CODIGO ) FROM BYTEC2.VIEWROTAREPRESENTANTE b, SUPAEMPR s WHERE b.CODIGO = s.AEMPR_CODIGO AND s.AEMPR_TIPO = 'C' AND b.CODIGO = {codigo}"]
    )'''


def entregadivida():
    return (
        [
            "SELECT * into #nfcan FROM VNDANFCD where (ANFCD_STS_NFE = 'C' or ANFCD_STS_NFE = 'D') AND ANFCD_TIPO_EMPR = 'C';",
            "SELECT ANFLN_EMPRESA as EMP, ANFLN_NUM_NOTA as NOTA, sum(ANFLN_QTD_IMP) as CX into #r FROM VNDANFLN GROUP BY ANFLN_NUM_NOTA, ANFLN_EMPRESA;",
            "select AEMPR_CODIGO AS COD, AEMPR_NOME_ABREV AS FANT into #t from supaempr where AEMPR_TIPO = 'T';",
            "SELECT fcd.ANFCD_EMPRESA AS EMPRESA, fcd.ANFCD_REPRE as REPRE, ROTA AS ROTA, fcd.ANFCD_CLIENTE AS CLIENTE, FANTASIA, fcd.ANFCD_NUM_NOTA as NFF, DATAED(fcd.ANFCD_DATA_EMISSAO) as DATA_EMISSAO, fcd.ANFCD_TOT_NOTA AS TOT, #r.CX, fcd.ANFCD_TRANSP as TRANSP, FANT as TRANSP_NOME, isnull((select OBS_CANC_NFE from VNDANFCA where  fcd.ANFCD_NUM_NOTA = NUMERO_NFF AND fcd.ANFCD_EMPRESA = Empresa),'DENEGADA') AS MOTIVO into #canceladas FROM #nfcan fcd, #r, #t, BYTEC.VIEWROTAREPRESENTANTE where NOTA = fcd.ANFCD_NUM_NOTA AND fcd.ANFCD_CLIENTE = CODIGO AND  fcd.ANFCD_EMPRESA = EMP AND  COD = fcd.ANFCD_TRANSP ORDER BY  fcd.ANFCD_DATA_EMISSAO DESC;",
            "SELECT fcd.ANFCD_CLIENTE AS CLI, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, DATAEF(lar.VENCIMENTO) AS VCTO,  datediff(day,lar.Vencimento,now()) as D_VNC, lar.PARCELA as PARC, lar.VALOR into #dividas FROM SUPAEMPR mpr, VNDANFCD fcd, VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND fcd.ANFCD_TIPO_EMPR = 'C' AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND  lar.VENCIMENTO+1 <= now() EXCEPT ( SELECT  fcd.ANFCD_CLIENTE AS CLI, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, DATAEF(lar.VENCIMENTO) AS VCTO,  datediff(day,lar.Vencimento,now()) as D_VNC, lar.PARCELA as PARC, lar.VALOR FROM  SUPAEMPR mpr, VNDANFCD fcd, VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND fcd.ANFCD_TIPO_EMPR = 'C' AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND  lar.VENCIMENTO+1 <= now() AND  lar.Vencimento = fcd.ANFCD_DATA_EMISSAO AND  datediff(day,lar.Vencimento,now()) <= 2);",
            "SELECT ANFLN_EMPRESA as EMP,  ANFLN_PEDIDO as PED,  ANFLN_NUM_NOTA as NOTA  into #faturados  FROM VNDANFLN  EXCEPT (  select  EMPRESA,  ANFLN_PEDIDO as PED,  NFF  FROM  #canceladas,  VNDANFLN  where  EMPRESA = ANFLN_EMPRESA AND  ANFLN_NUM_NOTA = NFF GROUP BY  EMPRESA,  PED,  NFF );",
            "select APEPC_EMPRESA as EMP, APEPC_PEDIDO as PED, SUM(APEPC_QTD_PEDIDA) as CX, SUM((select APEPC_QTD_PEDIDA * ADFIT_PESO_LIQUIDO from VNDADFIT where APEIT_COD_ITEM = ADFIT_COD_ITEM)) AS PESO into #cxpeso from VNDAPEPC, VNDAPEIT WHERE APEIT_PEDIDO = APEPC_PEDIDO AND APEIT_LINHA = APEPC_LINHA AND APEIT_EMPRESA = APEPC_EMPRESA GROUP BY PED, EMP;",
            "SELECT REPRE,  MERCADO, ROTA,  APECD_CLIENTE as CLIENTE,  FANTASIA,  DATAED(APECD_DATA_CADAST) as CADAST,  DATAED(APEPC_DATA_PREV) as PREV, APECD_EMPRESA as EMPRESA, APECD_PEDIDO AS PEDIDO, CX, PESO, (select FIRST VCTO from #dividas where CLI = APECD_CLIENTE) AS VENCIMENTO FROM  VNDAPECD,  VNDAPEPC,  BYTEC.VIEWROTAREPRESENTANTE , #cxpeso cp where  APECD_CLIENTE = CODIGO AND  APEPC_DATA_CANCEL = '00000000' AND  APEPC_EMPRESA = EMPRESA AND  APEPC_PEDIDO = PEDIDO AND  APEPC_STATUS = 'L' AND cp.EMP = EMPRESA AND  cp.PED = PEDIDO GROUP BY  REPRE,  MERCADO, ROTA,  CLIENTE,  FANTASIA,  APECD_DATA_CADAST,  EMPRESA, PEDIDO, CX, PESO, PREV EXCEPT ( SELECT  REPRE,  MERCADO, ROTA,  APECD_CLIENTE as CLIENTE,  FANTASIA,  DATAED(APECD_DATA_CADAST) as CADAST,  DATAED(APEPC_DATA_PREV) as PREV, APECD_EMPRESA as EMPRESA, APECD_PEDIDO AS PEDIDO, CX, PESO, (select FIRST VCTO from #dividas where CLI = APECD_CLIENTE) AS VENCIMENTO FROM  VNDAPECD,  VNDAPEPC,  BYTEC.VIEWROTAREPRESENTANTE , #faturados fat, #cxpeso cp where  APECD_CLIENTE = CODIGO AND  APEPC_EMPRESA = EMPRESA AND  APEPC_PEDIDO = PEDIDO AND  fat.EMP = EMPRESA AND fat.PED = PEDIDO AND  cp.EMP = EMPRESA AND  cp.PED = PEDIDO GROUP BY  REPRE,  MERCADO, ROTA,  CLIENTE,  FANTASIA,  APECD_DATA_CADAST, EMPRESA, PEDIDO, CX, PESO, PREV ORDER by  APECD_DATA_CADAST DESC )"
        ])


def tabelaprecos():
    return (
        "select ( case ATITM_EMPRESA when 1 then 'prowater' when 2 then 'proclean' when 3 then 'prolimp' when 4 then 'pronew' "
        "end CASE ) as emp, ATITM_COD_ITEM as ITEM,ATITM_TABELA_PRECO as TABELA,cast(ATITM_DATA_INICIAL as DATETIME) as DT_INI,"
        "cast(ATITM_DATA_FIN as DATETIME) as DT_FIN, ATITM_VALOR as VALOR from VNDATITM ORDER BY EMP,DT_FIN DESC; "
    )


def tabelaprecosfinal():
    return (
        "select  ATITM_EMPRESA as EMPRESA, ATITM_COD_ITEM as ITEM, (select ADFIT_DESCRICAO from VNDADFIT where "
        "ADFIT_COD_ITEM = ITEM) as \"DESC\", cast(ATITM_DATA_INICIAL as DATETIME) as DATA_I, cast(ATITM_DATA_FIN as "
        "DATETIME) as DATA_F, ATITM_VALOR as VALOR from VNDATITM where  ATITM_TABELA_PRECO = '00001' AND  DATA_I = ("
        "select FIRST cast(ATITM_DATA_INICIAL as DATETIME) from VNDATITM order by ATITM_DATA_INICIAL DESC) AND  "
        "EMPRESA = 1 order BY  EMPRESA, DATA_I DESC, ITEM;")


def cobrancas():
    return (
        "SELECT mpr.AEMPR_REPR AS REPR,fcd.ANFCD_CLIENTE AS CLI,( case fcd.ANFCD_EMPRESA when 1 then 'prowater' when "
        "2 then 'proclean' when 3 then 'prolimp' end when 4 then 'pronew' end CASE ) AS EMP,fcd.ANFCD_NUM_NOTA AS "
        "NOTA,(select ANFLN_PEDIDO as PED from VNDANFLN WHERE ANFLN_EMPRESA = fcd.ANFCD_EMPRESA AND ANFLN_NUM_NOTA = "
        "NOTA GROUP BY PED),DATAED(fcd.ANFCD_DATA_EMISSAO) AS EMISSAO, DATAEF(lar.VENCIMENTO) AS VCTO, lar.PARCELA as "
        "PARC, lar.VALOR FROM SUPAEMPR mpr, VNDANFCD fcd, VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE "
        "nte where fcd.ANFCD_TIPO_EMPR = 'C' AND fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = "
        "mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND "
        "fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = "
        "LAR.CODIGOUNIDADE AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND  "
        "lar.VENCIMENTO+1 <= now() EXCEPT ( SELECT mpr.AEMPR_REPR AS REPR, fcd.ANFCD_CLIENTE AS CLI, "
        "fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, (select ANFLN_PEDIDO as pedido from VNDANFLN WHERE "
        "ANFLN_EMPRESA = fcd.ANFCD_EMPRESA AND ANFLN_NUM_NOTA = NOTA GROUP BY pedido), DATAED(fcd.ANFCD_DATA_EMISSAO) "
        "AS EMISSAO,  DATAEF(lar.VENCIMENTO) AS VCTO, lar.PARCELA as PARC, lar.VALOR FROM SUPAEMPR mpr, VNDANFCD fcd, "
        "VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = 'C' AND "
        "fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = "
        "nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND "
        "fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,"
        "10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND  lar.VENCIMENTO+1 <= now() AND  lar.Vencimento = "
        "fcd.ANFCD_DATA_EMISSAO AND  datediff(day,lar.Vencimento,now()) <= 2)")


def cobrancasporargumentos(**kwargs):
    cliente = "" if kwargs.get('cliente') is None else f"AND CLI = {kwargs.get('cliente')}"
    empresa = "" if kwargs.get('empresa') is None else f"AND EMP = {kwargs.get('empresa')}"
    pedido = "" if kwargs.get('pedido') is None else f"AND PED = {kwargs.get('pedido')}"
    nota_fiscal = "" if kwargs.get('nota_fiscal') is None else f"AND NOTA = {kwargs.get('nota_fiscal')}"
    return (
        f"SELECT mpr.AEMPR_REPR AS REPR,fcd.ANFCD_CLIENTE AS CLI,( case fcd.ANFCD_EMPRESA when 1 then 'prowater' when 2 then 'proclean' when 3 then 'prolimp' when 4 then 'pronew'end CASE ) AS EMP,fcd.ANFCD_NUM_NOTA AS NOTA,(select ANFLN_PEDIDO as PED from VNDANFLN WHERE ANFLN_EMPRESA = fcd.ANFCD_EMPRESA AND ANFLN_NUM_NOTA = NOTA GROUP BY PED) as PED,cast(fcd.ANFCD_DATA_EMISSAO as DATETIME) AS EMISSAO, cast(lar.VENCIMENTO as DATETIME) AS VCTO, lar.PARCELA as PARC, lar.VALOR FROM SUPAEMPR mpr, VNDANFCD fcd, VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = 'C' AND fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO {empresa} {pedido} {nota_fiscal} {cliente} AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND  lar.VENCIMENTO+1 <= now() EXCEPT ( SELECT mpr.AEMPR_REPR AS REPR, fcd.ANFCD_CLIENTE AS CLI, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, (select ANFLN_PEDIDO as pedido from VNDANFLN WHERE ANFLN_EMPRESA = fcd.ANFCD_EMPRESA AND ANFLN_NUM_NOTA = NOTA GROUP BY pedido) as PED, cast(fcd.ANFCD_DATA_EMISSAO as DATETIME) AS EMISSAO,  cast(lar.VENCIMENTO as DATETIME) AS VCTO, lar.PARCELA as PARC, lar.VALOR FROM SUPAEMPR mpr, VNDANFCD fcd, VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = 'C' AND fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO {empresa} {pedido} {nota_fiscal} {cliente} AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND  lar.VENCIMENTO+1 <= now() AND  lar.Vencimento = fcd.ANFCD_DATA_EMISSAO AND  datediff(day,lar.Vencimento,now()) <= 2)")


def representantes(repre):
    repre = f" AND AEMPR_CODIGO = {repre}" if repre != "" else ""
    return (
        "SELECT AEMPR_CODIGO as COD, AEMPR_RAZAO_SOCIAL as RAZAO, AEMPR_NOME_ABREV AS FANT FROM SUPAEMPR where "
        f"AEMPR_TIPO = 'R' {repre}")


def representante(codigo):
    return (
        "SELECT AEMPR_CODIGO as COD, AEMPR_RAZAO_SOCIAL as RAZAO, AEMPR_NOME_ABREV AS FANT FROM SUPAEMPR where "
        f"AEMPR_TIPO = 'R' AND COD = {codigo}")


def notascanceladasemotivo():
    return ([
        "SELECT * into #nfcan FROM VNDANFCD where ANFCD_STS_NFE = 'C' or ANFCD_STS_NFE = 'D';",
        "SELECT ANFLN_EMPRESA as EMP, ANFLN_NUM_NOTA as NOTA, sum(ANFLN_QTD_IMP) as CX into #r FROM VNDANFLN GROUP BY "
        "ANFLN_NUM_NOTA, ANFLN_EMPRESA;",
        "select AEMPR_CODIGO AS COD, AEMPR_NOME_ABREV AS FANT into #t from supaempr where AEMPR_TIPO = 'T';",
        "SELECT fcd.ANFCD_EMPRESA AS EMPRESA, fcd.ANFCD_REPRE as REPRE, ROTA AS ROTA,fcd.ANFCD_CLIENTE AS CLIENTE, "
        "FANTASIA, fcd.ANFCD_NUM_NOTA as NFF, DATAED(fcd.ANFCD_DATA_EMISSAO) as DATA_EMISSAO, fcd.ANFCD_TOT_NOTA AS "
        "TOT, #r.CX, fcd.ANFCD_TRANSP as TRANSP, FANT as TRANSP_NOME, isnull((select OBS_CANC_NFE from VNDANFCA where "
        "fcd.ANFCD_NUM_NOTA = NUMERO_NFF AND fcd.ANFCD_EMPRESA = Empresa),'DENEGADA') AS MOTIVO FROM #nfcan fcd, #r, "
        "#t, BYTEC.VIEWROTAREPRESENTANTE where NOTA = fcd.ANFCD_NUM_NOTA AND fcd.ANFCD_CLIENTE = CODIGO AND "
        "fcd.ANFCD_EMPRESA = EMP AND COD = fcd.ANFCD_TRANSP ORDER BY fcd.ANFCD_DATA_EMISSAO DESC"])


def emissaonotasfiscais():
    return ([
        "select ANFLN_EMPRESA as EMP, ANFLN_NUM_NOTA as NOTA, sum(ANFLN_QTD_ENTR) as QTD into #notacaixa from VNDANFLN GROUP BY ANFLN_NUM_NOTA,ANFLN_EMPRESA;",
        "select ANFCD_DATA_EMISSAO as EMI, isnull(count(*),0) as NR into #nrnf1 from VNDANFCD where ANFCD_TIPO_OPER = 'NF1' GROUP BY ANFCD_DATA_EMISSAO;",
        "select ANFCD_DATA_EMISSAO as EMI, isnull(count(*),0) as NR into #nrnb1 from VNDANFCD where ANFCD_TIPO_OPER = 'NB1' GROUP BY ANFCD_DATA_EMISSAO;",
        "select ANFCD_DATA_EMISSAO as EMI, sum(QTD) as QTD into #caixasnf1 from VNDANFCD, #notacaixa where ANFCD_EMPRESA = EMP AND ANFCD_NUM_NOTA = NOTA AND ANFCD_TIPO_OPER = 'NF1' AND ANFCD_CLIENTE != 1 AND ANFCD_CLIENTE != 2 AND ANFCD_CLIENTE != 2048 GROUP BY ANFCD_DATA_EMISSAO,ANFCD_EMPRESA, ANFCD_NUM_NOTA, EMP, NOTA;",
        "select ANFCD_DATA_EMISSAO as EMI, sum(QTD) as QTD into #caixasnb1 from VNDANFCD, #notacaixa where ANFCD_EMPRESA = EMP AND ANFCD_NUM_NOTA = NOTA AND ANFCD_TIPO_OPER = 'NB1' AND ANFCD_CLIENTE != 1 AND ANFCD_CLIENTE != 2 AND ANFCD_CLIENTE != 2048 GROUP BY ANFCD_DATA_EMISSAO,ANFCD_EMPRESA, ANFCD_NUM_NOTA, EMP, NOTA;",
        "select ANFCD_DATA_EMISSAO as EMI, sum(QTD) as QTD into #caixascannf1 from VNDANFCD, #notacaixa, VNDANFCA where EMPRESA = EMP AND NUMERO_NFF = NOTA AND ANFCD_EMPRESA = EMP AND ANFCD_NUM_NOTA = NOTA AND ANFCD_TIPO_OPER = 'NF1' GROUP BY ANFCD_DATA_EMISSAO,ANFCD_EMPRESA, ANFCD_NUM_NOTA, EMP, NOTA;",
        "select ANFCD_DATA_EMISSAO as EMI, sum(QTD) as QTD into #caixascannb1 from VNDANFCD, #notacaixa, VNDANFCA where EMPRESA = EMP AND NUMERO_NFF = NOTA AND ANFCD_EMPRESA = EMP AND ANFCD_NUM_NOTA = NOTA AND ANFCD_TIPO_OPER = 'NB1' GROUP BY ANFCD_DATA_EMISSAO,ANFCD_EMPRESA, ANFCD_NUM_NOTA, EMP, NOTA;",
        "select ANFCD_DATA_EMISSAO as EMI, sum(QTD) as QTD into #caixasnf1dene from VNDANFCD, #notacaixa where ANFCD_EMPRESA = EMP AND ANFCD_NUM_NOTA = NOTA AND ANFCD_TIPO_OPER = 'NF1' AND ANFCD_STS_NFE = 'D' GROUP BY ANFCD_DATA_EMISSAO,ANFCD_EMPRESA, ANFCD_NUM_NOTA, EMP, NOTA;",
        "select ANFCD_DATA_EMISSAO as EMI, sum(QTD) as QTD into #caixasnb1dene from VNDANFCD, #notacaixa where ANFCD_EMPRESA = EMP AND ANFCD_NUM_NOTA = NOTA AND ANFCD_TIPO_OPER = 'NB1' AND ANFCD_STS_NFE = 'D' GROUP BY ANFCD_DATA_EMISSAO,ANFCD_EMPRESA, ANFCD_NUM_NOTA, EMP, NOTA;",
        "select DATAED(ANFCD_DATA_EMISSAO) AS \"DATA\", count(DISTINCT ANFCD_TRANSP) as TRANSP, (select isnull(NR,0) from #nrnf1 where EMI = ANFCD_DATA_EMISSAO) as NR_NF, (select isnull(NR,0) from #nrnb1 where EMI = ANFCD_DATA_EMISSAO) as NR_NB, (select isnull(sum(QTD),0) from #caixasnf1 where EMI = ANFCD_DATA_EMISSAO) as CX_NF, (select isnull(sum(QTD),0) from #caixasnb1 where EMI = ANFCD_DATA_EMISSAO) as CX_NB, ((select count(QTD) from #caixascannf1 where EMI = ANFCD_DATA_EMISSAO)+(select count(QTD) from #caixasnf1dene where EMI = ANFCD_DATA_EMISSAO)) as NR_NF_CAN, ((select count(QTD) from #caixascannb1 where EMI = ANFCD_DATA_EMISSAO)+(select count(QTD) from #caixasnb1dene where EMI = ANFCD_DATA_EMISSAO)) as NR_NB_CAN, ((select isnull(sum(QTD),0) from #caixascannf1 where EMI = ANFCD_DATA_EMISSAO)+(select isnull(sum(QTD),0) from #caixasnf1dene where EMI = ANFCD_DATA_EMISSAO)) as CX_NF_CAN, ((select isnull(sum(QTD),0) from #caixascannb1 where EMI = ANFCD_DATA_EMISSAO)+(select isnull(sum(QTD),0) from #caixasnb1dene where EMI = ANFCD_DATA_EMISSAO)) as CX_NB_CAN, (NR_NF - NR_NF_CAN) as NR_NF_REAL, (NR_NB - NR_NB_CAN) as NR_NB_REAL, (CX_NF - CX_NF_CAN) as REALIZADO_NF, (CX_NB - CX_NB_CAN) as REALIZADO_NB, (if REALIZADO_NF > 0 then (((REALIZADO_NB+REALIZADO_NF)/REALIZADO_NF)-1) ELSE 0 endif) as \"BNF\" from VNDANFCD where ANFCD_DATA_EMISSAO > 20190000 GROUP BY ANFCD_DATA_EMISSAO order by ANFCD_DATA_EMISSAO DESC"
    ])


def producao():
    return (
        "select AOPSF_NUM_OP as NUM_OP, (SELECT ADFIT_DESCRICAO FROM VNDADFIT where ADFIT_COD_ITEM = AOPSF_COD_ITEM) "
        "as ITEM, DATABD(AOPSF_DATA_EMISSAO) as DT_EMISSAO,if(AOPSF_DATA_TER = '00000000') then 'AB' else 'EN' endif "
        "as ST, AOPSF_QTD_FABRICAR as A_FABRICAR, AOPSF_QTD_FABRICAD as FABRICADO,"
        "(AOPSF_QTD_FABRICAR-AOPSF_QTD_FABRICAD) as DIFERENCA, FABRICADO/A_FABRICAR AS EFETUADO from BYTEC.CPRAOPSF "
        "order by AOPSF_DATA_EMISSAO DESC")


def historiconotas(**kwargs):
    cliente = f" AND ANFCD_CLIENTE = {kwargs.get('cliente')}" if kwargs.get('cliente') is not None else ''
    top = f'TOP {kwargs.get("top")}' if kwargs.get('top') else ''
    return ([
        "select ADREP_CODIGO, ADREP_ZONA_ATUA into #zonarep from SUPADREP where ADREP_TIPO = 'R';",
        "select ATITM_EMPRESA as EMP, ATITM_COD_ITEM as ITEM, ATITM_TABELA_PRECO as TABELA, cast(ATITM_DATA_INICIAL as DATETIME) as DT_INI, cast(ATITM_DATA_FIN as DATETIME) as DT_FIN, ATITM_VALOR as VALOR into #tabelas from VNDATITM where TABELA = '00001' ORDER BY EMP, DT_FIN DESC;",
        f"select {top} ANFCD_EMPRESA as EMPRESA, ANFCD_CLIENTE as CLIENTE,  ANFCD_NUM_NOTA as NOTA, cast(ANFCD_DATA_CAD as DATETIME) as PERIODO, ANFCD_REPRE AS REPRESENTANTE,  ANFCD_TOT_DUPL as TOT_NOTA,  ANFLN_PRODUTO as PRODUTO,  ANFLN_QTD_ENTR as QTD, ANFLN_VALOR_LINHA as TOT_PRODUTO, ANFCD_TIPO_OPER as NF_NB, isnull((select FIRST VALOR from #tabelas where ITEM = PRODUTO AND EMP = EMPRESA AND DT_INI <= PERIODO AND DT_FIN > PERIODO ORDER BY DT_INI DESC),(select FIRST VALOR from #tabelas where ITEM = PRODUTO AND EMP = 4 AND DT_INI <= PERIODO AND DT_FIN > PERIODO ORDER BY DT_INI DESC),(select FIRST VALOR from #tabelas where ITEM = PRODUTO AND EMP = 3 AND DT_INI <= PERIODO AND DT_FIN > PERIODO ORDER BY DT_INI DESC),(select FIRST VALOR from #tabelas where ITEM = PRODUTO AND EMP = 2 AND DT_INI <= PERIODO AND DT_FIN > PERIODO ORDER BY DT_INI DESC),(select FIRST VALOR from #tabelas where ITEM = PRODUTO AND EMP = 1 AND DT_INI <= PERIODO AND DT_FIN > PERIODO ORDER BY DT_INI DESC),(select FIRST VALOR from #tabelas where ITEM = PRODUTO AND DT_INI <= PERIODO AND DT_FIN > PERIODO ORDER BY DT_INI DESC))*QTD as TABELA into #res from VNDANFLN, VNDANFCD, VIEWROTAREPRESENTANTE nte WHERE ANFCD_EMPRESA = ANFLN_EMPRESA AND ANFCD_NUM_NOTA = ANFLN_NUM_NOTA AND nte.Codigo = ANFCD_CLIENTE {cliente} AND ANFCD_TIPO_OPER != 'NF1' AND  ANFCD_STS_NFE = 'P' AND  ANFCD_CLIENTE != 1 AND  ANFCD_CLIENTE != 2 AND  ANFCD_CLIENTE != 2058 ORDER BY PERIODO DESC"
    ])


'''["select ATITM_EMPRESA as EMP,ATITM_COD_ITEM as ITEM,ATITM_TABELA_PRECO as TABELA,cast(ATITM_DATA_INICIAL as DATETIME) as DT_INI,cast(ATITM_DATA_FIN as DATETIME) as DT_FIN,ATITM_VALOR as VALOR into #tabelas from  VNDATITM  ORDER BY  EMP, DT_FIN DESC;",
"select ANFCD_EMPRESA as EMP, ANFCD_REPRE as REPRE, ANFCD_TIPO_OPER as TIPO, ANFCD_NUM_NOTA as NOTA,ANFLN_PEDIDO as PED, cast(ANFCD_DATA_EMISSAO as DATETIME) as DT_EMI, ANFCD_TOT_NOTA as TOT,sum(ANFLN_QTD_ENTR) as qtd,    TOT/qtd as VL_UN into #faturados from    VNDANFCD,    VNDANFLN  where     ANFCD_EMPRESA = ANFLN_EMPRESA AND     ANFCD_NUM_NOTA = ANFLN_NUM_NOTA AND    ANFCD_TIPO_OPER != 'NVI' AND     ANFCD_STS_NFE = 'P' AND     ANFCD_CLIENTE != 1 AND     ANFCD_CLIENTE != 2 AND     ANFCD_CLIENTE != 2058 AND     ANFCD_DATA_EMISSAO > 20190000 GROUP BY     ANFCD_EMPRESA,     ANFCD_NUM_NOTA,     ANFCD_DATA_EMISSAO,     ANFCD_TOT_NOTA,    ANFLN_PEDIDO,    REPRE,    TIPO ORDER BY    DT_EMI DESC;",
"select     APECD_EMPRESA as EMP,APECD_REPRE as REPRE,    APECD_PEDIDO as PED,     APECD_CLIENTE as CLI,     APECD_DESTINO as TIPO,     cast(APECD_DATA_CADAST as DATETIME) as DT_CAD,    cast(APEPC_DATA_PREV as DATETIME) as DT_PREV,    sum(APEPC_QTD_PEDIDA) as QTD,    (APEPC_VALOR_ENC*QTD) as TOT,    (isnull((SELECT FIRST VALOR from #tabelas WHERE ITEM = APEIT_COD_ITEM AND EMP = EMP AND TABELA = '00001' AND DT_INI <= DT_CAD AND DT_FIN >= DT_CAD ORDER BY DT_INI DESC)*QTD,        (SELECT FIRST VALOR from #tabelas WHERE ITEM = APEIT_COD_ITEM AND EMP = 4 AND TABELA = '00001' AND DT_INI >= DT_CAD AND DT_FIN >= DT_CAD ORDER BY DT_INI DESC)*QTD,        (SELECT FIRST VALOR from #tabelas WHERE ITEM = APEIT_COD_ITEM AND EMP = 3 AND TABELA = '00001' AND DT_INI <= DT_CAD AND DT_FIN >= DT_CAD ORDER BY DT_INI DESC)*QTD,        (SELECT FIRST VALOR from #tabelas WHERE ITEM = APEIT_COD_ITEM AND EMP = 1 AND TABELA = '00001' AND DT_INI <= DT_CAD AND DT_FIN >= DT_CAD ORDER BY DT_INI DESC)*QTD,        (SELECT FIRST VALOR from #tabelas WHERE ITEM = APEIT_COD_ITEM AND TABELA = '00001' AND DT_INI <= DT_CAD AND DT_FIN >= DT_CAD ORDER BY DT_INI DESC)*QTD,0)) as TABELA into #pedidos from     VNDAPECD,     VNDAPEPC,    VNDAPEIT  where     APECD_EMPRESA = APEPC_EMPRESA AND     APEPC_PEDIDO = APECD_PEDIDO AND     APEPC_STATUS != 'C' AND    APECD_DESTINO != 'VI' AND    APECD_CLIENTE != 1 AND     APECD_CLIENTE != 2 AND     APECD_CLIENTE != 2058 AND    APECD_DATA_CADAST > 20190000 AND    APEIT_EMPRESA = APECD_EMPRESA AND     APEIT_PEDIDO = APECD_PEDIDO AND     APEIT_LINHA = APEPC_LINHA GROUP BY     EMP,    PED,     CLI,     TIPO,     DT_CAD,    DT_PREV,    APEIT_COD_ITEM,    APEPC_VALOR_ENC, REPRE;",
"select     EMP,    PED, REPRE,     CLI,     TIPO,     DT_CAD,    DT_PREV,    QTD,    sum(TOT) as TOT,    sum(TABELA) as TABELA into #ped  from #pedidos GROUP BY     EMP,    PED,     CLI,     TIPO,     DT_CAD,    DT_PREV,    QTD, REPRE;",
"select p.EMP as EMPRESA,    P.REPRE as REPRESENTANTE,    p.CLI as CLIENTE,    P.PED AS PEDIDO,    f.NOTA,    p.TIPO as NF_NB,    p.DT_CAD as DATA_CADASTRO,    p.DT_PREV as DATA_PREVISAO,    f.DT_EMI as DATA_EMISSAO,    f.TOT as TOT_NOTA,    SUM(p.TOT) as TOT_PED,    SUM(p.QTD) as QTD,    SUM(p.tabela) as TABELA from     #ped p left join     #faturados f on        p.EMP = f.EMP AND        p.PED = f.PED GROUP BY     p.EMP,    REPRE,    p.CLI,    P.PED,    f.NOTA,    p.TIPO,    p.DT_CAD,    p.DT_PREV,    f.DT_EMI,    f.TOT ORDER BY DT_CAD DESC;"
]'''


def contaconotas(**kwargs):
    cliente = kwargs.get('cliente')
    return f"select count(ANFCD_NUM_NOTA) as NOTA from VNDANFCD WHERE ANFCD_CLIENTE = {cliente} AND ANFCD_TIPO_OPER != 'NVI' AND  ANFCD_STS_NFE = 'P' AND  ANFCD_CLIENTE != 1 AND  ANFCD_CLIENTE != 2 AND  ANFCD_CLIENTE != 2058;"


def relatoriodecompas():
    return ([
        "select ecd.APECD_CLIENTE as CODIGO, fcd.ANFCD_TOT_NOTA as TOTAL, sum(fln.ANFLN_QTD_IMP) as CX, (fcd.ANFCD_DATA_EMISSAO) as DATA_EMS INTO #r from VNDAPECD ecd, VNDANFCD fcd, VNDANFLN fln where ecd.APECD_CLIENTE = fcd.ANFCD_CLIENTE AND fln.ANFLN_NUM_NOTA = fcd.ANFCD_NUM_NOTA AND fln.ANFLN_PEDIDO = ecd.APECD_PEDIDO AND fcd.ANFCD_TIPO_OPER = 'NF1' AND datediff(day,ecd.APECD_DATA_CADAST,getdate()) <= 365 GROUP BY fcd.ANFCD_DATA_EMISSAO, ecd.APECD_CLIENTE, fcd.ANFCD_TOT_NOTA order by fcd.ANFCD_DATA_EMISSAO DESC;",
        "select secd.APECD_CLIENTE as CODIGO, sfcd.ANFCD_TOT_NOTA as TOTAL, sum(sfln.ANFLN_QTD_IMP) as CX, (sfcd.ANFCD_DATA_EMISSAO) as DATA_EMS INTO #t from VNDAPECD secd, VNDANFCD sfcd, VNDANFLN sfln, VNDANFCA sfca where secd.APECD_CLIENTE = sfcd.ANFCD_CLIENTE AND sfln.ANFLN_NUM_NOTA = sfcd.ANFCD_NUM_NOTA AND sfcd.ANFCD_NUM_NOTA = sfca.NUMERO_NFF AND sfln.ANFLN_PEDIDO = secd.APECD_PEDIDO AND sfcd.ANFCD_TIPO_OPER = 'NF1' AND datediff(day,secd.APECD_DATA_CADAST,getdate()) <= 365 GROUP BY sfcd.ANFCD_DATA_EMISSAO,secd.APECD_CLIENTE, sfcd.ANFCD_TOT_NOTA order by sfcd.ANFCD_DATA_EMISSAO DESC ;",
        "select * into #ultimofaturado from #r EXCEPT select * from #t;",
        "SELECT DATAED(max(fcd.ANFCD_DATA_EMISSAO)) as DATA_EMS,   MPR.AEMPR_CODIGO as CODIGO into #datafaturamento from  VNDAPECD ecd, SUPAEMPR mpr, VNDANFCD fcd, VNDANFLN fln WHERE  ecd.APECD_CLIENTE = mpr.AEMPR_CODIGO AND mpr.AEMPR_CODIGO = fcd.ANFCD_CLIENTE AND fln.ANFLN_NUM_NOTA = fcd.ANFCD_NUM_NOTA AND fln.ANFLN_PEDIDO = ecd.APECD_PEDIDO AND ecd.APECD_EMPRESA = fcd.ANFCD_EMPRESA AND ecd.APECD_TIPO_CLI = fcd.ANFCD_TIPO_EMPR AND ecd.APECD_TIPO_CLI = mpr.AEMPR_TIPO AND fcd.ANFCD_TIPO_OPER = 'NF1' AND datediff(day,ecd.APECD_DATA_CADAST,getdate()) <= 365 GROUP BY MPR.AEMPR_CODIGO;",
        "SELECT mpr.AEMPR_CODIGO as CODIGO, (datediff(day,max(ANFCD_DATA_EMISSAO),getdate())) as ULTIMO_FATURAMENTO into #tempofaturamento from VNDAPECD ecd, SUPAEMPR mpr, VNDANFCD fcd, VNDANFLN fln WHERE ecd.APECD_CLIENTE = mpr.AEMPR_CODIGO AND mpr.AEMPR_CODIGO = fcd.ANFCD_CLIENTE AND mpr.AEMPR_TIPO = 'C' AND fln.ANFLN_NUM_NOTA = fcd.ANFCD_NUM_NOTA AND fln.ANFLN_PEDIDO = ecd.APECD_PEDIDO AND ecd.APECD_EMPRESA = fcd.ANFCD_EMPRESA AND ecd.APECD_TIPO_CLI = fcd.ANFCD_TIPO_EMPR AND ecd.APECD_TIPO_CLI = mpr.AEMPR_TIPO GROUP BY MPR.AEMPR_CODIGO;",
        "SELECT mpr.AEMPR_CODIGO as CODIGO, min(datediff(day,ecd.APECD_DATA_CADAST,getdate())) as ULTIMO_PEDIDO into #tempopedido from VNDAPECD ecd,  SUPAEMPR mpr, WHERE  ecd.APECD_CLIENTE = mpr.AEMPR_CODIGO AND  ecd.APECD_TIPO_CLI = mpr.AEMPR_TIPO AND mpr.AEMPR_TIPO = 'C' GROUP BY CODIGO;",
        "select BYTEC.SUPAEMPR.AEMPR_CODIGO as COD into #emails from SUPAEMPR where AEMPR_TIPO = 'C' EXCEPT ( select AMAIL_CODIGO FROM SUPAMAIL WHERE AMAIL_TIPO = 'C' AND locate(AMAIL_E_MAIL_WWW,'@',-1)>0 GROUP BY AMAIL_CODIGO);",
        "SELECT mpr.AEMPR_REPR as REPR, nte.ROTA, mpr.AEMPR_STATUS as ST, fcd.ANFCD_CLIENTE AS CLI, mpr.AEMPR_NOME_ABREV AS FANTASIA, mpr.AEMPR_CEP AS CEP, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, DATAED(fcd.ANFCD_DATA_EMISSAO) AS EMISSAO,  DATAEF(lar.VENCIMENTO) AS VCTO,  datediff(day,lar.Vencimento,now()) as DIAS_VNC, lar.PARCELA, lar.VALOR into #cobrancas FROM  SUPAEMPR mpr, VNDANFCD fcd, VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND  lar.VENCIMENTO+1 <= now() ORDER BY  mpr.AEMPR_CEP, lar.Vencimento desc;",
        "SELECT b.REPRE, b.ZONA, b.MERCADO, b.ROTA, isnull((select ULTIMO_PEDIDO from #tempopedido where b.CODIGO = CODIGO),0) as PED, isnull((select ULTIMO_FATURAMENTO from #tempofaturamento where b.CODIGO = CODIGO),0) as FAT, isnull((select DATA_EMS from #datafaturamento where b.CODIGO = CODIGO),'**/**/***') as DT_FAT, isnull((select FIRST TOTAL from #ultimofaturado where b.CODIGO = CODIGO),0) as VLR_NF, isnull((select FIRST CX from #ultimofaturado where b.CODIGO = CODIGO),0) as NR_CX, (select count(*) from #cobrancas where CLI = b.CODIGO )AS COB, b.ST, b.CODIGO,b.FANTASIA, s.AEMPR_RAZAO_SOCIAL as RAZAO_SOCIAL, if(s.AEMPR_CGC = '000000000000000') then AEMPR_CPF else AEMPR_CGC ENDIF as CNPJ_CPF, ifnull((select COD from #emails where b.CODIGO = COD),'','N' ) as EMAIL, b.CONTATO, s.AEMPR_TELEX_CONT1 as CELULAR, b.TELEFONE, b.ENDERECO, b.BAIRRO, b.CIDADE, b.CEP, b.UF FROM BYTEC2.VIEWROTAREPRESENTANTE b, SUPAEMPR s WHERE b.CODIGO = s.AEMPR_CODIGO AND s.AEMPR_TIPO = 'C'"
    ])


def supervisores(repre):
    return (f"select AEMPR_REPR as SUPERVISOR from SUPAEMPR where AEMPR_CODIGO = {repre} AND AEMPR_TIPO = 'R'")


def relatoriodecomprasleve(**kwargs):
    cli = f" AND b.CODIGO = {kwargs.get('cliente')}" if kwargs.get('cliente') is not None else ''
    repre = f" AND b.REPRE = {kwargs.get('repre')}" if kwargs.get("repre") is not None else ""
    return ([
        f"SELECT cast(max(ANFCD_DATA_CAD) as DATETIME) as DT INTO #ultimo_pedido FROM VNDANFCD,VNDANFLN where ANFCD_NUM_NOTA = ANFLN_NUM_NOTA AND ANFCD_EMPRESA = ANFLN_EMPRESA AND (ANFCD_STS_NFE != 'C' OR ANFCD_STS_NFE != 'D') AND ANFCD_TIPO_OPER = 'NF1' AND ANFCD_CLIENTE = {kwargs.get('cliente')}",
        f"SELECT cast(max(APECD_DATA_EMISSAO) as DATETIME) as DT INTO #ultimo_faturado FROM VNDAPECD WHERE APECD_DESTINO = '01' AND APECD_CLIENTE = {kwargs.get('cliente')}",
        f"SELECT b.REPRE, b.ST, (select DT from  #ultimo_pedido where b.CODIGO = CODIGO) as PED, (select DT from #ultimo_faturado where b.CODIGO = CODIGO) as FAT, b.CODIGO + ' - ' + b.FANTASIA + ' - ' + trim(s.AEMPR_RUA_AV) + ', ' + trim(s.AEMPR_NRO)+ ', ' + trim(s.AEMPR_COMPL) as ENDERECO FROM BYTEC2.VIEWROTAREPRESENTANTE b, SUPAEMPR s WHERE b.CODIGO = s.AEMPR_CODIGO AND s.AEMPR_TIPO = 'C' {cli} {repre} "
     ])


def relatoriodecompras(**kwargs):
    cli = f" AND b.CODIGO = {kwargs.get('cliente')}" if kwargs.get('cliente') is not None else ''
    repre = f" AND b.REPRE = {kwargs.get('repre')}" if kwargs.get("repre") is not None else ""
    return ([
        "select AEMFD_CODIGO as CLI, max(AEMFD_COND_PGTO) as COND into  #condcliente from VNDAEMFD where AEMFD_TIPO "
        "= 'C' AND AEMFD_EMPRESA = 1 GROUP BY AEMFD_CODIGO;",
        "select ecd.APECD_CLIENTE as CODIGO, fcd.ANFCD_TOT_NOTA as TOTAL, sum(fln.ANFLN_QTD_IMP) as CX, "
        "( fcd.ANFCD_DATA_EMISSAO) as DATA_EMS INTO  #r from VNDAPECD ecd, VNDANFCD fcd, VNDANFLN fln where "
        "ecd.APECD_CLIENTE = fcd.ANFCD_CLIENTE AND fln.ANFLN_NUM_NOTA = fcd.ANFCD_NUM_NOTA AND fln.ANFLN_PEDIDO = "
        "ecd.APECD_PEDIDO AND fcd.ANFCD_TIPO_OPER = 'NF1' AND datediff(day,ecd.APECD_DATA_CADAST,getdate()) <= 365 "
        "GROUP BY fcd.ANFCD_DATA_EMISSAO, ecd.APECD_CLIENTE, fcd.ANFCD_TOT_NOTA order by fcd.ANFCD_DATA_EMISSAO DESC;",
        "select    secd.APECD_CLIENTE as CODIGO, sfcd.ANFCD_TOT_NOTA as TOTAL, sum(sfln.ANFLN_QTD_IMP) as CX, "
        "( sfcd.ANFCD_DATA_EMISSAO) as DATA_EMS INTO  #t from VNDAPECD secd, VNDANFCD sfcd, VNDANFLN sfln, "
        "VNDANFCA sfca where secd.APECD_CLIENTE = sfcd.ANFCD_CLIENTE AND sfln.ANFLN_NUM_NOTA = sfcd.ANFCD_NUM_NOTA "
        "AND sfcd.ANFCD_NUM_NOTA = sfca.NUMERO_NFF AND sfln.ANFLN_PEDIDO = secd.APECD_PEDIDO AND sfcd.ANFCD_TIPO_OPER "
        "= 'NF1' AND datediff(day,secd.APECD_DATA_CADAST,getdate()) <= 365 GROUP BY sfcd.ANFCD_DATA_EMISSAO, "
        "secd.APECD_CLIENTE, sfcd.ANFCD_TOT_NOTA order by sfcd.ANFCD_DATA_EMISSAO DESC;",
        "select * into  #ultimofaturado from #r EXCEPT select * from #t;",
        "SELECT DATAED(max(fcd.ANFCD_DATA_EMISSAO)) as DATA_EMS, MPR.AEMPR_CODIGO as CODIGO into  #datafaturamento "
        "from VNDAPECD ecd, SUPAEMPR mpr, VNDANFCD fcd, VNDANFLN fln WHERE ecd.APECD_CLIENTE = mpr.AEMPR_CODIGO AND "
        "mpr.AEMPR_CODIGO = fcd.ANFCD_CLIENTE AND fln.ANFLN_NUM_NOTA = fcd.ANFCD_NUM_NOTA AND fln.ANFLN_PEDIDO = "
        "ecd.APECD_PEDIDO AND ecd.APECD_EMPRESA = fcd.ANFCD_EMPRESA AND ecd.APECD_TIPO_CLI = fcd.ANFCD_TIPO_EMPR AND "
        "ecd.APECD_TIPO_CLI = mpr.AEMPR_TIPO AND fcd.ANFCD_TIPO_OPER = 'NF1' AND datediff(day,ecd.APECD_DATA_CADAST,"
        "getdate()) <= 365 GROUP BY MPR.AEMPR_CODIGO;",
        "SELECT mpr.AEMPR_CODIGO as CODIGO, (datediff(day, max(ANFCD_DATA_EMISSAO), getdate())) as ULTIMO_FATURAMENTO "
        "into  #tempofaturamento from VNDAPECD ecd, SUPAEMPR mpr, VNDANFCD fcd, VNDANFLN fln WHERE ecd.APECD_CLIENTE "
        "= mpr.AEMPR_CODIGO AND mpr.AEMPR_CODIGO = fcd.ANFCD_CLIENTE AND mpr.AEMPR_TIPO = 'C' AND fln.ANFLN_NUM_NOTA "
        "= fcd.ANFCD_NUM_NOTA AND fln.ANFLN_PEDIDO = ecd.APECD_PEDIDO AND ecd.APECD_EMPRESA = fcd.ANFCD_EMPRESA AND "
        "ecd.APECD_TIPO_CLI = fcd.ANFCD_TIPO_EMPR AND ecd.APECD_TIPO_CLI = mpr.AEMPR_TIPO GROUP BY MPR.AEMPR_CODIGO;",
        "SELECT mpr.AEMPR_CODIGO as CODIGO, min(datediff(day, ecd.APECD_DATA_CADAST, getdate())) as ULTIMO_PEDIDO "
        "into  #tempopedido from VNDAPECD ecd, SUPAEMPR mpr, WHERE ecd.APECD_CLIENTE = mpr.AEMPR_CODIGO AND "
        "ecd.APECD_TIPO_CLI = mpr.AEMPR_TIPO AND mpr.AEMPR_TIPO = 'C' GROUP BY CODIGO;",
        "select BYTEC.SUPAEMPR.AEMPR_CODIGO as COD into  #emails from SUPAEMPR where AEMPR_TIPO = 'C' EXCEPT ( "
        "select AMAIL_CODIGO FROM SUPAMAIL WHERE AMAIL_TIPO = 'C' AND locate(AMAIL_E_MAIL_WWW,'@',-1)>0 GROUP BY "
        "AMAIL_CODIGO);",
        "select AMAIL_CODIGO as CODIGO, AMAIL_IDENTIFICA as TIPO, AMAIL_E_MAIL_WWW as ENDERECO into  #emailwww FROM "
        "SUPAMAIL where AMAIL_TIPO = 'C' ORDER BY TIPO;",
        "SELECT mpr.AEMPR_REPR as REPR, nte.ROTA, mpr.AEMPR_STATUS as ST, fcd.ANFCD_CLIENTE AS CLI, "
        "mpr.AEMPR_NOME_ABREV AS FANTASIA, mpr.AEMPR_CEP AS CEP, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS "
        "NOTA, DATAED(fcd.ANFCD_DATA_EMISSAO) AS EMISSAO, DATAEF(lar.VENCIMENTO) AS VCTO, datediff(day, "
        "lar.Vencimento, now()) as \"DIAS VNC\", lar.PARCELA, lar.VALOR into  #cobrancas FROM SUPAEMPR mpr, "
        "VNDANFCD fcd, VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = "
        "mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND "
        "fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = "
        "LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND "
        "lar.RECEBIMENTO IS NULL AND lar.VENCIMENTO+1 <= now() ORDER BY mpr.AEMPR_CEP, lar.Vencimento desc;",
        "SELECT b.REPRE, (select ULTIMO_PEDIDO from  #tempopedido where b.CODIGO = CODIGO) as PED, "
        "(select ULTIMO_FATURAMENTO from #tempofaturamento where b.CODIGO = CODIGO) as FAT, (select count(*) from "
        "#cobrancas where CLI = b.CODIGO )AS COB, b.ST, b.CODIGO + ' - ' + b.FANTASIA + ' - ' + trim(s.AEMPR_RUA_AV) "
        "+ ', ' + trim(s.AEMPR_NRO)+ ', ' + trim(s.AEMPR_COMPL) as ENDERECO FROM BYTEC2.VIEWROTAREPRESENTANTE b, "
        f"SUPAEMPR s WHERE b.CODIGO = s.AEMPR_CODIGO AND s.AEMPR_TIPO = 'C' {repre} {cli}"
    ])


def tabelacliente(cli):
    return f"select AEMFD_CODIGO as CLI,AEMFD_COND_PGTO as COND_PAG, AEMFD_TABELA_PRECO as TABELA from VNDAEMFD WHERE TABELA != '00001' AND AEMFD_TIPO = 'C' AND AEMFD_EMPRESA != 2 AND CLI = {cli} GROUP BY CLI,COND_PAG, TABELA "


def produtostabela(tabela):
    return f"select ATITM_COD_ITEM as ITEM, ATITM_TABELA_PRECO as TABELA, cast(ATITM_DATA_INICIAL as DATETIME) as DT_INI,cast(ATITM_DATA_FIN as DATETIME) as DT_FIN , ATITM_VALOR as VALOR from VNDATITM WHERE ATITM_TABELA_PRECO = '{tabela}' AND DT_INI = (select max(cast(ATITM_DATA_INICIAL as DATETIME)) from VNDATITM where TABELA = ATITM_TABELA_PRECO) GROUP BY ITEM, TABELA, DT_INI, DT_FIN, VALOR"


def notasepedidos(**kwargs):
    cliente = ""
    nota = ""
    on = ""
    e = " AND "
    if kwargs.get("cliente") is not None:
        cliente = f"CODIGO = {kwargs.get('cliente')}"
        on = "ON"
        if kwargs.get("nota") is not None:
            nota = f"{e} NOTA = {kwargs.get('nota')}"
    return ([
        "select ANFCD_EMPRESA as EMP, ANFCD_REPRE as REPRE, ANFCD_TIPO_OPER as TIPO, ANFCD_NUM_NOTA as NOTA, ANFLN_PEDIDO as PED,  cast(ANFCD_DATA_EMISSAO as DATETIME) as DT_EMI, ANFCD_TOT_NOTA as TOT, sum(ANFLN_QTD_ENTR) as qtd, TOT/qtd as VL_UN into #faturados from VNDANFCD, VNDANFLN  where  ANFCD_EMPRESA = ANFLN_EMPRESA AND ANFCD_NUM_NOTA = ANFLN_NUM_NOTA AND ANFCD_TIPO_OPER != 'NVI' AND  ANFCD_STS_NFE = 'P' AND  ANFCD_CLIENTE != 1 AND  ANFCD_CLIENTE != 2 AND  ANFCD_CLIENTE != 2058 GROUP BY  ANFCD_EMPRESA,  ANFCD_NUM_NOTA,  ANFCD_DATA_EMISSAO,  ANFCD_TOT_NOTA, ANFLN_PEDIDO, REPRE, TIPO ORDER BY  DT_EMI DESC;",
        "select  APECD_EMPRESA as EMP, APECD_PEDIDO as PED,  APECD_CLIENTE as CLI,  APECD_DESTINO as TIPO,  cast(APECD_DATA_CADAST as DATETIME) as DT_CAD, cast(APEPC_DATA_PREV as DATETIME) as DT_PREV, sum(APEPC_QTD_PEDIDA) as QTD into #pedidos from  VNDAPECD,  VNDAPEPC  where  APECD_EMPRESA = APEPC_EMPRESA AND  APEPC_PEDIDO = APECD_PEDIDO AND  APEPC_STATUS != 'C' AND APECD_DESTINO != 'VI' AND APECD_CLIENTE != 1 AND  APECD_CLIENTE != 2 AND  APECD_CLIENTE != 2058 GROUP BY  EMP, PED,  CLI,  TIPO,  DT_CAD, DT_PREV;",
        "select  p.EMP, f.REPRE as REPRE_F, p.CLI, P.PED, f.NOTA, p.TIPO, p.DT_CAD, p.DT_PREV, f.DT_EMI, f.TOT, p.QTD into #ped_fat from  #pedidos p left join  #faturados f on p.EMP = f.EMP AND p.PED = f.PED ORDER BY DT_CAD DESC;",
        f"select  CODIGO, pf.EMP, pf.REPRE_F, pf.PED, pf.NOTA, if (left(pf.TIPO,1) = 'B') then 'BNF' else 'NF' ENDIF as TIPO, pf.DT_CAD, pf.DT_PREV, pf.DT_EMI, pf.TOT, pf.QTD  from  BYTEC.VIEWROTAREPRESENTANTE LEFT JOIN #ped_fat pf {on} {cliente} {nota}"
    ])


def relatoriopedidosrepresentantes():
    return (
        "select     APECD_EMPRESA as EMPRESA, APECD_REPRE as REPRE, APECD_CLIENTE as CLI, APECD_PEDIDO as PEDIDO, "
        "DATAED(APECD_DATA_CADAST) as CADAST, if (LEFT(APECD_DESTINO, 1) = 'B') then 'BNF' ELSE IF (LEFT("
        "APECD_DESTINO, 1)) = '0' THEN 'NF' endif endif as TIPO, (CL_TRAD_1 * V_CL_TRAD_1 + CL_TRAD_2 * V_CL_TRAD_2 + "
        "CL_TRAD_5 * V_CL_TRAD_5 + CL_BRAN_1 * V_CL_BRAN_1 + CL_BRAN_2 * V_CL_BRAN_2 + AG_TRAD_1 * V_AG_TRAD_1 + "
        "AG_TRAD_2 * V_AG_TRAD_2 + AG_TRAD_5 * V_AG_TRAD_5 + AG_BRAN_1 * V_AG_BRAN_1 + AG_BRAN_2 * V_AG_BRAN_2 + "
        "ES_TRAD_1 * V_ES_TRAD_1 + ES_TRAD_3 * V_ES_TRAD_3 + ES_PROM_4 * V_ES_PROM_4 + LP_SENS * V_LP_SENS + LP_AFFE "
        "* V_LP_AFFE + LP_LAMO * V_LP_LAMO) as TOTALRS, (CL_TRAD_1 + CL_TRAD_2 + CL_TRAD_5 + CL_BRAN_1 + CL_BRAN_2 + "
        "AG_TRAD_1 + AG_TRAD_2 + AG_TRAD_5 + AG_BRAN_1 + AG_BRAN_2 + ES_TRAD_1 + ES_TRAD_3 + ES_PROM_4 + LP_SENS + "
        "LP_AFFE + LP_LAMO) as TOTALCX, (if APEIT_COD_ITEM = '011009' THEN APEPC_QTD_PEDIDA ENDIF ) as CL_TRAD_1, "
        "(if APEIT_COD_ITEM = '011009' THEN APEPC_VALOR_ENC ENDIF ) as V_CL_TRAD_1, (if APEIT_COD_ITEM = '011001' "
        "THEN APEPC_QTD_PEDIDA ENDIF ) as CL_TRAD_2, (if APEIT_COD_ITEM = '011001' THEN APEPC_VALOR_ENC ENDIF ) as "
        "V_CL_TRAD_2, (if APEIT_COD_ITEM = '011005' THEN APEPC_QTD_PEDIDA ENDIF ) as CL_TRAD_5, (if APEIT_COD_ITEM = "
        "'011005' THEN APEPC_VALOR_ENC ENDIF ) as V_CL_TRAD_5, (if APEIT_COD_ITEM = '012010' THEN APEPC_QTD_PEDIDA "
        "ENDIF ) as CL_BRAN_1, (if APEIT_COD_ITEM = '012010' THEN APEPC_VALOR_ENC ENDIF ) as V_CL_BRAN_1, "
        "(if APEIT_COD_ITEM = '012003' THEN APEPC_QTD_PEDIDA ENDIF ) as CL_BRAN_2, (if APEIT_COD_ITEM = '012003' THEN "
        "APEPC_VALOR_ENC ENDIF ) as V_CL_BRAN_2, (if APEIT_COD_ITEM = '021002' THEN APEPC_QTD_PEDIDA ENDIF ) as "
        "AG_TRAD_1, (if APEIT_COD_ITEM = '021002' THEN APEPC_VALOR_ENC ENDIF ) as V_AG_TRAD_1, (if APEIT_COD_ITEM = "
        "'021006' THEN APEPC_QTD_PEDIDA ENDIF ) as AG_TRAD_2, (if APEIT_COD_ITEM = '021006' THEN APEPC_VALOR_ENC "
        "ENDIF ) as V_AG_TRAD_2, (if APEIT_COD_ITEM = '021007' THEN APEPC_QTD_PEDIDA ENDIF ) as AG_TRAD_5, "
        "(if APEIT_COD_ITEM = '021007' THEN APEPC_VALOR_ENC ENDIF ) as V_AG_TRAD_5, (if APEIT_COD_ITEM = '022004' "
        "THEN APEPC_QTD_PEDIDA ENDIF ) as AG_BRAN_1, (if APEIT_COD_ITEM = '022004' THEN APEPC_VALOR_ENC ENDIF ) as "
        "V_AG_BRAN_1, (if APEIT_COD_ITEM = '022008' THEN APEPC_QTD_PEDIDA ENDIF ) as AG_BRAN_2, (if APEIT_COD_ITEM = "
        "'022008' THEN APEPC_VALOR_ENC ENDIF ) as V_AG_BRAN_2, (if APEIT_COD_ITEM = '031011' THEN APEPC_QTD_PEDIDA "
        "ENDIF ) as ES_TRAD_1, (if APEIT_COD_ITEM = '031011' THEN APEPC_VALOR_ENC ENDIF ) as V_ES_TRAD_1, "
        "(if APEIT_COD_ITEM = '031014' THEN APEPC_QTD_PEDIDA ENDIF ) as ES_TRAD_3, (if APEIT_COD_ITEM = '031014' THEN "
        "APEPC_VALOR_ENC ENDIF ) as V_ES_TRAD_3, (if APEIT_COD_ITEM = '031013' THEN APEPC_QTD_PEDIDA ENDIF ) as "
        "ES_PROM_4, (if APEIT_COD_ITEM = '031013' THEN APEPC_VALOR_ENC ENDIF ) as V_ES_PROM_4, (if APEIT_COD_ITEM = "
        "'041017' THEN APEPC_QTD_PEDIDA ENDIF ) as LP_SENS,  (if APEIT_COD_ITEM = '041017' THEN APEPC_VALOR_ENC ENDIF "
        ") as V_LP_SENS, (if APEIT_COD_ITEM = '042020' THEN APEPC_QTD_PEDIDA ENDIF ) as LP_AFFE,  (if APEIT_COD_ITEM "
        "= '042020' THEN APEPC_VALOR_ENC ENDIF ) as V_LP_AFFE, (if APEIT_COD_ITEM = '043018' THEN APEPC_QTD_PEDIDA "
        "ENDIF ) as LP_LAMO, (if APEIT_COD_ITEM = '043018' THEN APEPC_VALOR_ENC ENDIF ) as V_LP_LAMO from     "
        "VNDAPECD, VNDAPEPC, VNDAPEIT WHERE     APECD_DATA_CADAST >= 20190000 AND     LEFT(APECD_DESTINO, "
        "1) != 'V' AND     APEPC_EMPRESA = EMPRESA AND     APEPC_PEDIDO = PEDIDO AND     APEIT_EMPRESA = "
        "APEPC_EMPRESA AND     APEIT_PEDIDO = APEPC_PEDIDO AND     APEIT_LINHA = APEPC_LINHA AND     APEPC_STATUS != "
        "'C' AND     APEPC_DATA_LIBE >= 20181200 GROUP BY     PEDIDO, EMPRESA, REPRE, APECD_DATA_CADAST, CLI, "
        "APECD_DESTINO, APEPC_QTD_PEDIDA, APEIT_COD_ITEM, APEPC_VALOR_ENC ORDER BY     APECD_DATA_CADAST DESC ")


def divisaodefaturamento():
    return ([
        "select     nte.REPRE as REPRE,     ANFCD_EMPRESA as EMP,     sum(valor) as TOT,     left(right(ANFCD_DATA_CAD,4),2) as MES,     left(right(ANFCD_DATA_CAD,8),4) as ANO into #total from     parcelar,     VNDANFCD,     BYTEC.VIEWROTAREPRESENTANTE nte where     nte.CODIGO = ANFCD_CLIENTE AND     numero = RIGHT(ANFCD_NUM_NOTA,8) AND     datediff(month,emissao,getdate()) <= 11 AND     datediff(month,ANFCD_DATA_CAD,getdate()) <= 11 AND     DoctoRecebimento != 'RECCAN' AND     CodigoEmp = EMP GROUP BY     EMP,    nte.REPRE,     MES,     ANO;",
        "select     nte.REPRE as REPRE,    EMP,    count(numero) as NR_BLT,     sum(valor) as TOT,     (sum(valor)/#total.TOT) AS PARTE,     avg(valor) as MED,     datediff(day,Emissao,Vencimento) as PRAZO,     left(right(ANFCD_DATA_CAD,4),2) as MES,     left(right(ANFCD_DATA_CAD,8),4) as ANO from     parcelar,     VNDANFCD,     BYTEC.VIEWROTAREPRESENTANTE nte,     #total where     #total.REPRE = nte.REPRE AND     #total.MES = MES AND     #total.ANO = ANO AND     nte.CODIGO = ANFCD_CLIENTE AND     numero = RIGHT(ANFCD_NUM_NOTA,8) AND     datediff(month,emissao,getdate()) <= 11 AND     datediff(month,ANFCD_DATA_CAD,getdate()) <= 11 AND     DoctoRecebimento != 'RECCAN' AND     CodigoEmp = EMP GROUP BY     nte.REPRE,     datediff(day,Emissao,Vencimento),     MES,     ANO,     #total.TOT,    EMP"
    ])


def transportes():
    return ([
        "select ANFLN_EMPRESA as EMP, ANFLN_NUM_NOTA as NOTA, sum(ANFLN_QTD_ENTR) as QTD, SUM((select ANFLN_QTD_ENTR * ADFIT_PESO_LIQUIDO from VNDADFIT where ANFLN_PRODUTO = ADFIT_COD_ITEM)) as PESO into #notacaixa from VNDANFLN GROUP BY  ANFLN_NUM_NOTA, ANFLN_EMPRESA;",
        "select  ANFCD_DATA_EMISSAO as EMI,  isnull(count(*),0) as nr,  ANFCD_TRANSP AS TR into #nrnf1 from VNDANFCD where  ANFCD_TIPO_OPER = 'NF1' AND  ANFCD_CLIENTE != 1 AND ANFCD_CLIENTE != 2 AND ANFCD_CLIENTE != 2048 GROUP BY  ANFCD_DATA_EMISSAO, TR;",
        "select  ANFCD_DATA_EMISSAO as EMI,  isnull(count(*),0) as nr,  ANFCD_TRANSP AS TR into #nrnb1 from VNDANFCD where  ANFCD_TIPO_OPER = 'NB1' AND  ANFCD_CLIENTE != 1 AND ANFCD_CLIENTE != 2 AND ANFCD_CLIENTE != 2048 GROUP BY ANFCD_DATA_EMISSAO, TR;",
        "select  ANFCD_DATA_EMISSAO as EMI,  ANFCD_TRANSP as TR,  sum(QTD) as QTD,  sum(PESO) as PESO into #caixasnf1 from  VNDANFCD,  #notacaixa where  ANFCD_EMPRESA = EMP AND  ANFCD_NUM_NOTA = NOTA AND  ANFCD_TIPO_OPER = 'NF1' GROUP BY  ANFCD_DATA_EMISSAO, ANFCD_EMPRESA,  ANFCD_NUM_NOTA,  EMP,  NOTA,  TR;",
        "select  ANFCD_DATA_EMISSAO as EMI,  ANFCD_TRANSP as TR,  sum(QTD) as QTD,  sum(PESO) as PESO into #caixasnb1 from  VNDANFCD,  #notacaixa where  ANFCD_EMPRESA = EMP AND  ANFCD_NUM_NOTA = NOTA AND  ANFCD_TIPO_OPER = 'NB1' GROUP BY  ANFCD_DATA_EMISSAO, ANFCD_EMPRESA,  ANFCD_NUM_NOTA,  EMP,  NOTA,  TR;",
        "select  ANFCD_DATA_EMISSAO as EMI,  ANFCD_TRANSP as TR,  sum(QTD) as QTD,  sum(PESO) as PESO into #caixascannf1 from  VNDANFCD,  #notacaixa,  VNDANFCA where  EMPRESA = EMP AND  NUMERO_NFF = NOTA AND  ANFCD_EMPRESA = EMP AND  ANFCD_NUM_NOTA = NOTA AND  ANFCD_TIPO_OPER = 'NF1' GROUP BY  ANFCD_DATA_EMISSAO, ANFCD_EMPRESA,  ANFCD_NUM_NOTA,  EMP,  NOTA,  TR;",
        "select  ANFCD_DATA_EMISSAO as EMI,  ANFCD_TRANSP as TR,  sum(QTD) as QTD,  sum(PESO) as PESO into #caixascannb1 from  VNDANFCD,  #notacaixa,  VNDANFCA where  EMPRESA = EMP AND  NUMERO_NFF = NOTA AND  ANFCD_EMPRESA = EMP AND  ANFCD_NUM_NOTA = NOTA AND  ANFCD_TIPO_OPER = 'NB1' GROUP BY  ANFCD_DATA_EMISSAO, ANFCD_EMPRESA,  ANFCD_NUM_NOTA,  EMP,  NOTA,  TR;",
        "select  ANFCD_DATA_EMISSAO as EMI,  isnull(count(*),0) as nr,  ANFCD_TRANSP AS TR into #nrnf1dene from VNDANFCD where  ANFCD_TIPO_OPER = 'NF1' AND  ANFCD_CLIENTE != 1 AND ANFCD_CLIENTE != 2 AND ANFCD_CLIENTE != 2048 AND  ANFCD_STS_NFE = 'D'GROUP BY  ANFCD_DATA_EMISSAO, TR;",
        "select  ANFCD_DATA_EMISSAO as EMI,  isnull(count(*),0) as nr,  ANFCD_TRANSP AS TR into #nrnb1dene from VNDANFCD where  ANFCD_TIPO_OPER = 'NB1' AND  ANFCD_CLIENTE != 1 AND ANFCD_CLIENTE != 2 AND ANFCD_CLIENTE != 2048 AND  ANFCD_STS_NFE = 'D'GROUP BY ANFCD_DATA_EMISSAO, TR;",
        "select  ANFCD_DATA_EMISSAO as EMI,  ANFCD_TRANSP as TR,  sum(QTD) as QTD,  sum(PESO) as PESO into #caixasnf1dene from  VNDANFCD,  #notacaixa where  ANFCD_EMPRESA = EMP AND  ANFCD_NUM_NOTA = NOTA AND  ANFCD_TIPO_OPER = 'NF1' AND  ANFCD_STS_NFE = 'D' GROUP BY  ANFCD_DATA_EMISSAO, ANFCD_EMPRESA,  ANFCD_NUM_NOTA,  EMP,  NOTA,  TR;",
        "select  ANFCD_DATA_EMISSAO as EMI,  ANFCD_TRANSP as TR,  sum(QTD) as QTD,  sum(PESO) as PESO into #caixasnb1dene from  VNDANFCD,  #notacaixa where  ANFCD_EMPRESA = EMP AND  ANFCD_NUM_NOTA = NOTA AND  ANFCD_TIPO_OPER = 'NB1' AND  ANFCD_STS_NFE = 'D' GROUP BY  ANFCD_DATA_EMISSAO, ANFCD_EMPRESA,  ANFCD_NUM_NOTA,  EMP,  NOTA,  TR;",
        "select  DATAED(ANFCD_DATA_EMISSAO) AS DATA_EM,  ANFCD_TRANSP AS TRANSP,  (select isnull(sum(nr),0) from #nrnf1 where EMI = ANFCD_DATA_EMISSAO AND TR = TRANSP) AS NR_NF, (select isnull(sum(nr),0) from #nrnb1 where EMI = ANFCD_DATA_EMISSAO AND TR = TRANSP) AS NR_BN, (select isnull(sum(QTD),0) from #caixasnf1 where EMI = ANFCD_DATA_EMISSAO AND TR = TRANSP) AS CX_NF, (select isnull(sum(QTD),0) from #caixasnb1 where EMI = ANFCD_DATA_EMISSAO AND TR = TRANSP) as CX_BN, (select isnull(sum(PESO),0) from #caixasnf1 where EMI = ANFCD_DATA_EMISSAO AND TR = TRANSP) AS KG_NF, (select isnull(sum(PESO),0) from #caixasnb1 where EMI = ANFCD_DATA_EMISSAO AND TR = TRANSP) as KG_BN, (select isnull(count(QTD),0) from #caixascannf1 where EMI = ANFCD_DATA_EMISSAO AND TR = TRANSP) + (select isnull(sum(nr),0) from #nrnf1dene where EMI = ANFCD_DATA_EMISSAO AND TR = TRANSP) AS CAN_NF, (select isnull(count(QTD),0) from #caixascannb1 where EMI = ANFCD_DATA_EMISSAO AND TR = TRANSP) + (select isnull(sum(nr),0) from #nrnb1dene where EMI = ANFCD_DATA_EMISSAO AND TR = TRANSP) AS CAN_BN, (select isnull(sum(QTD),0) from #caixascannf1 where EMI = ANFCD_DATA_EMISSAO AND TR = TRANSP)  + (select isnull(sum(QTD),0) from #caixasnf1dene where EMI = ANFCD_DATA_EMISSAO AND TR = TRANSP) AS CAN_CX_NF, (select isnull(sum(QTD),0) from #caixascannb1 where EMI = ANFCD_DATA_EMISSAO AND TR = TRANSP)  + (select isnull(sum(QTD),0) from #caixasnb1dene where EMI = ANFCD_DATA_EMISSAO AND TR = TRANSP) AS CAN_CX_BN, (select isnull(sum(PESO),0) from #caixascannf1 where EMI = ANFCD_DATA_EMISSAO AND TR = TRANSP)  + (select isnull(sum(PESO),0) from #caixasnf1dene where EMI = ANFCD_DATA_EMISSAO AND TR = TRANSP) AS CAN_KG_NF, (select isnull(sum(PESO),0) from #caixascannb1 where EMI = ANFCD_DATA_EMISSAO AND TR = TRANSP)  + (select isnull(sum(PESO),0) from #caixasnb1dene where EMI = ANFCD_DATA_EMISSAO AND TR = TRANSP) AS CAN_KG_BN, (NR_NF - CAN_NF) as REAL_NF, (NR_BN - CAN_BN) as REAL_BN, (CX_NF - CAN_CX_NF) as REAL_CX_NF, (CX_BN - CAN_CX_BN) as REAL_CX_BN, (KG_NF + KG_BN) AS CAP, (CAP - (CAN_KG_NF+ CAN_KG_BN)) AS CAP_EFET from  VNDANFCD WHERE  ANFCD_TIPO_OPER = 'NF1' OR ANFCD_TIPO_OPER = 'NB1' GROUP BY  TRANSP,  ANFCD_DATA_EMISSAO order BY  ANFCD_DATA_EMISSAO DESC;"
    ])


def itenspedidos():
    return ([
        "select APECD_EMPRESA as EMPRESA, APECD_REPRE as REPRE, vr.ROTA as ROTA, vr.ZONA as ZONA, vr.MERCADO as MERCADO, APECD_CLIENTE as CLI, APECD_PEDIDO as PEDIDO, cast(APECD_DATA_CADAST as DATETIME) as CADAST, if (LEFT(APECD_DESTINO,1) = 'B') then 'BNF' ELSE IF (LEFT(APECD_DESTINO,1)) = '0' THEN 'NF' endif endif as TIPO, APEIT_COD_ITEM as COD_ITEM, APEPC_QTD_PEDIDA as QTD, APEPC_VALOR_ENC as VALOR_UN, APEPC_VALOR_ENC*APEPC_QTD_PEDIDA as TOTAL from VNDAPECD, VNDAPEPC, VNDAPEIT, BYTEC.VIEWROTAREPRESENTANTE vr, WHERE APECD_CLIENTE = vr.CODIGO AND APECD_REPRE = vr.REPRE AND APECD_DATA_CADAST >= 20190000 AND LEFT(APECD_DESTINO,1) != 'V' AND APEPC_EMPRESA = EMPRESA AND APEPC_PEDIDO = PEDIDO AND APEIT_EMPRESA = APEPC_EMPRESA AND APEIT_PEDIDO = APEPC_PEDIDO AND APEIT_LINHA = APEPC_LINHA AND APEPC_STATUS != 'C' AND APEPC_DATA_LIBE >= 20181200 GROUP BY PEDIDO, EMPRESA, REPRE, APECD_DATA_CADAST, CLI, APECD_DESTINO, APEPC_QTD_PEDIDA, APEIT_COD_ITEM, APEPC_VALOR_ENC, ROTA, ZONA, MERCADO ORDER BY APECD_DATA_CADAST DESC"
    ])


def pedidosabertos():
    return ([
        "SELECT b.REPRE as repre, b.ZONA as zona, b.MERCADO as mercado, b.ROTA as rota, b.ST as st, b.CODIGO as cod, b.FANTASIA as fant into #cliente FROM BYTEC2.VIEWROTAREPRESENTANTE b;",
        "SELECT CodigoEmpresa as emp, LimiteCred as cred into #credito FROM InfoCredCFT WHERE TipoEmpresa = 'C';",
        "SELECT APEPC_EMPRESA as emp, APEPC_PEDIDO as ped, sum(APEPC_QTD_PEDIDA*APEPC_VALOR_ENC) as tot into #liberado FROM VNDAPEPC where APEPC_STATUS = 'L' GROUP BY ped,emp;",
        "SELECT APECD_EMPREsA as emp, APECD_PEDIDO as ped, APECD_CLIENTE as cod into #clientepedido FROM VNDAPECD where APECD_TIPO_CLI = 'C';",
        "SELECT ANFLN_EMPRESA as emp, ANFLN_PEDIDO as ped, ANFLN_NUM_NOTA as nota into #notapedido FROM VNDANFLN;",
        "SELECT codigoemp as emp, numero as nota, sum(valor+valorjuros) as tot into #pendente FROM ParcelaR where isnull(datediff(day,recebimento,getdate()),-1) = -1 GROUP BY emp, nota;",
        "SELECT ido.cod as cod, sum(ado.tot) as tot into #pedidosabertos FROM #clientepedido ido,#liberado ado WHERE ado.ped = ido.ped and ado.emp = ido.emp GROUP BY ido.cod;",
        "SELECT mpr.AEMPR_STATUS as ST, fcd.ANFCD_CLIENTE AS CLI, mpr.AEMPR_NOME_ABREV AS FANTASIA, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, lar.VALOR as valor, lar.valorjuros as juros, lar.PARCELA as PARC, datediff(day,lar.Vencimento,now()) as vencido into #devendo FROM SUPAEMPR mpr, VNDANFCD fcd, VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND datediff(day,lar.Vencimento,now()) <= 0;",
        "select cli as cod,sum(valor) as tot into #dividacliente from #devendo GROUP BY cli;",
        "SELECT fcd.ANFCD_CLIENTE AS cod, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, datediff(day,lar.Vencimento,now()) as vencido, lar.PARCELA as PARC, lar.VALOR as valor into #atrasado FROM SUPAEMPR mpr, VNDANFCD fcd, VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND lar.VENCIMENTO+1 <= now() EXCEPT ( SELECT fcd.ANFCD_CLIENTE AS CLI, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, datediff(day,lar.Vencimento,now()) as \"D VNC\", lar.PARCELA as PARC, lar.VALOR FROM SUPAEMPR mpr, VNDANFCD fcd, VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND lar.VENCIMENTO+1 <= now() AND lar.Vencimento = fcd.ANFCD_DATA_EMISSAO AND fcd.ANFCD_DATA_EMISSAO != '00000000' AND datediff(day,lar.Vencimento,now()) <= 2 );",
        "select cod as cod,sum(valor) as tot into #atrasocliente from #Atrasado where vencido > 0 GROUP BY cod;",
        "SELECT nte.repre as Repr, nte.zona as Zona, nte.mercado as Mercad, nte.rota as Rot, nte.cod as Cod, nte.fant as Fantasi, nte.st as ST, isnull((select tot from #pedidosabertos where cod = nte.cod),0) as Pedido, isnull((select tot from #atrasocliente where cod = nte.cod),0) as \"BL Atrasado\", isnull((select tot from #dividacliente where cod = nte.cod),0) as \"BL À Vencer\", Pedido+\"BL À Vencer\"+\"BL Atrasado\" as \"Limite Utilizado\", (select cred from #credito where emp = nte.cod) as \"Total Credito\", \"Total Credito\" - \"Limite Utilizado\" as Saldo into #analisecredito from #cliente nte;",
        "SELECT * into #nfcan FROM VNDANFCD where (ANFCD_STS_NFE = 'C' or ANFCD_STS_NFE = 'D') AND ANFCD_TIPO_EMPR = 'C';",
        "SELECT ANFLN_EMPRESA as EMP, ANFLN_NUM_NOTA as NOTA, sum(ANFLN_QTD_IMP) as CX into #r FROM VNDANFLN GROUP BY ANFLN_NUM_NOTA, ANFLN_EMPRESA;",
        "select AEMPR_CODIGO AS COD, AEMPR_NOME_ABREV AS FANT into #t from supaempr where AEMPR_TIPO = 'T';",
        "SELECT fcd.ANFCD_EMPRESA AS EMPRESA, fcd.ANFCD_REPRE as REPRE, ROTA AS ROTA, fcd.ANFCD_CLIENTE AS CLIENTE, FANTASIA, fcd.ANFCD_NUM_NOTA as NFF, DATAED(fcd.ANFCD_DATA_EMISSAO) as DATA_EMISSAO, fcd.ANFCD_TOT_NOTA AS TOT, #r.CX, fcd.ANFCD_TRANSP as TRANSP, FANT as \"TRANSP NOME\", isnull((select OBS_CANC_NFE from VNDANFCA where fcd.ANFCD_NUM_NOTA = NUMERO_NFF AND fcd.ANFCD_EMPRESA = Empresa),'DENEGADA') AS MOTIVO into #canceladas FROM #nfcan fcd, #r, #t, BYTEC.VIEWROTAREPRESENTANTE, where NOTA = fcd.ANFCD_NUM_NOTA AND fcd.ANFCD_CLIENTE = CODIGO AND fcd.ANFCD_EMPRESA = EMP AND COD = fcd.ANFCD_TRANSP ORDER BY fcd.ANFCD_DATA_EMISSAO DESC;",
        "SELECT fcd.ANFCD_CLIENTE AS CLI, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, DATAEF(lar.VENCIMENTO) AS VCTO, datediff(day,lar.Vencimento,now()) as \"D VNC\", lar.PARCELA as PARC, lar.VALOR into #dividas FROM SUPAEMPR mpr, VNDANFCD fcd, VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND fcd.ANFCD_TIPO_EMPR = 'C' AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND lar.VENCIMENTO+1 <= now() EXCEPT ( SELECT fcd.ANFCD_CLIENTE AS CLI, fcd.ANFCD_EMPRESA AS EMP, fcd.ANFCD_NUM_NOTA AS NOTA, DATAEF(lar.VENCIMENTO) AS VCTO, datediff(day,lar.Vencimento,now()) as \"D VNC\", lar.PARCELA as PARC, lar.VALOR FROM SUPAEMPR mpr, VNDANFCD fcd, VNDAEMDF mdf, PARCELAR lar, BYTEC2.VIEWROTAREPRESENTANTE nte where fcd.ANFCD_TIPO_EMPR = mpr.AEMPR_TIPO AND fcd.ANFCD_CLIENTE = mpr.AEMPR_CODIGO AND fcd.ANFCD_CLIENTE = nte.CODIGO AND fcd.ANFCD_TIPO_EMPR = mdf.AEMDF_TIPO AND fcd.ANFCD_CLIENTE = mdf.AEMDF_CODIGO AND fcd.ANFCD_EMPRESA = LAR.CODIGOEMP AND fcd.ANFCD_UNIDADE = LAR.CODIGOUNIDADE AND fcd.ANFCD_TIPO_EMPR = 'C' AND SUBSTR(fcd.ANFCD_NUM_NOTA,3,10) = LAR.NUMERO AND lar.RECEBIMENTO IS NULL AND lar.VENCIMENTO+1 <= now() AND lar.Vencimento = fcd.ANFCD_DATA_EMISSAO AND datediff(day,lar.Vencimento,now()) <= 2 ); ",
        "SELECT ANFLN_EMPRESA as EMP, ANFLN_PEDIDO as PED, ANFLN_NUM_NOTA as NOTA, sum(ANFLN_VALOR_LINHA) as VALOR into #faturados FROM VNDANFLN GROUP BY EMP, PED, NOTA EXCEPT ( select EMPRESA, ANFLN_PEDIDO as PED, NFF , sum(ANFLN_VALOR_LINHA) as VALOR FROM #canceladas, VNDANFLN where EMPRESA = ANFLN_EMPRESA AND ANFLN_NUM_NOTA = NFF GROUP BY EMPRESA, PED, NFF );",
        "select APEPC_EMPRESA as EMP, APEPC_PEDIDO as PED, SUM(APEPC_QTD_PEDIDA) as CX, SUM((select APEPC_QTD_PEDIDA * ADFIT_PESO_LIQUIDO from VNDADFIT where APEIT_COD_ITEM = ADFIT_COD_ITEM)) AS PESO into #cxpeso from VNDAPEPC, VNDAPEIT WHERE APEIT_PEDIDO = APEPC_PEDIDO AND APEIT_LINHA = APEPC_LINHA AND APEIT_EMPRESA = APEPC_EMPRESA GROUP BY PED, EMP;",
        "SELECT REPRE, vr.ZONA, MERCADO, ROTA, APECD_CLIENTE as CLIENTE, FANTASIA, cast(APECD_DATA_CADAST as datetime) as CADAST, cast(APEPC_DATA_PREV as datetime) as PREV, APECD_EMPRESA as EMPRESA, APECD_REPRE as REPRE_PED, APECD_PEDIDO AS PEDIDO, if (APECD_DESTINO = 'B1') then 'BNF' else 'NF' endif as TIPO, (select isnull(max(AEMFD_COND_PGTO),0) from VNDAEMFD where AEMFD_CODIGO = CLIENTE AND AEMFD_TIPO = 'C') as COND_PGTO, APECD_COND_PGTO as PRAZO, sum(APEPC_QTD_PEDIDA*APEPC_VALOR_ENC) as VALOR, CX, PESO, (select FIRST VCTO from #dividas where CLI = APECD_CLIENTE) AS VENCIMENTO, \"BL À Vencer\" as BL_A_Vencer, \"BL Atrasado\" as BL_Atrasado, \"Saldo\" FROM VNDAPECD, VNDAPEPC, BYTEC.VIEWROTAREPRESENTANTE vr, #cxpeso cp, #analisecredito where Cod = CODIGO AND APECD_CLIENTE = CODIGO AND APEPC_DATA_CANCEL = '00000000' AND APEPC_EMPRESA = EMPRESA AND APEPC_PEDIDO = PEDIDO AND APECD_TRANSP = 99 AND APEPC_STATUS = 'L' AND cp.EMP = EMPRESA AND cp.PED = PEDIDO GROUP BY REPRE, vr.ZONA, MERCADO, ROTA, CLIENTE, FANTASIA, APECD_DATA_CADAST, EMPRESA, PEDIDO, PRAZO, CX, PESO, PREV, REPRE_PED, TIPO, BL_A_Vencer, BL_Atrasado, \"Saldo\" EXCEPT ( SELECT REPRE, vr.ZONA, MERCADO, ROTA, APECD_CLIENTE as CLIENTE, FANTASIA, cast(APECD_DATA_CADAST as datetime) as CADAST, cast(APEPC_DATA_PREV as datetime) as PREV, APECD_EMPRESA as EMPRESA, APECD_REPRE as REPRE_PED, APECD_PEDIDO AS PEDIDO, if (APECD_DESTINO = 'B1') then 'BNF' else 'NF' endif as TIPO, (select isnull(max(AEMFD_COND_PGTO),0) from VNDAEMFD where AEMFD_CODIGO = CLIENTE AND AEMFD_TIPO = 'C') as COND_PGTO, APECD_COND_PGTO as PRAZO, SUM(VALOR), CX, PESO, (select FIRST VCTO from #dividas where CLI = APECD_CLIENTE) AS VENCIMENTO, \"BL À Vencer\" as BL_A_Vencer, \"BL Atrasado\" as BL_Atrasado, \"Saldo\" FROM VNDAPECD, VNDAPEPC, BYTEC.VIEWROTAREPRESENTANTE vr, #faturados fat, #cxpeso cp, #analisecredito where Cod = CODIGO AND APECD_CLIENTE = CODIGO AND APEPC_STATUS != 'L' AND APEPC_EMPRESA = EMPRESA AND APEPC_PEDIDO = PEDIDO AND fat.EMP = EMPRESA AND fat.PED = PEDIDO AND cp.EMP = EMPRESA AND cp.PED = PEDIDO GROUP BY REPRE, vr.ZONA, MERCADO, ROTA, CLIENTE, FANTASIA, APECD_DATA_CADAST, EMPRESA, PEDIDO, PRAZO, CX, PESO, PREV, REPRE_PED, TIPO, BL_A_Vencer, BL_Atrasado, \"Saldo\" ORDER by APECD_DATA_CADAST DESC )"
    ])


def itensnotasfaturadas():
    return ([
        "SELECT ANFCD_EMPRESA as EMP, ANFCD_CLIENTE as CLIENTE, ANFLN_PRODUTO as PRODUTO, ANFLN_NUM_NOTA as NOTA, ANFLN_PEDIDO as PEDIDO, ANFLN_QTD_ENTR as QTD, ANFLN_VALOR_UNIT as UN, ANFCD_REPRE as REPR, cast (ANFCD_DATA_EMISSAO as DATETIME) as DT INTO #faturados FROM VNDANFLN, VNDANFCD where ANFLN_EMPRESA = ANFCD_EMPRESA AND ANFLN_NUM_NOTA = ANFCD_NUM_NOTA AND ANFCD_STS_NFE = 'P' ORDER BY ANFCD_DATA_EMISSAO DESC ;",
        "select TOP 5000 REPRE, ROTA, ZONA, MERCADO, CODIGO, ST, FANTASIA, isnull(EMP,'00') as EMP, isnull(NOTA,'0000000000') as NOTA, isnull(PEDIDO,'0000000000') as PEDIDO, isnull(DT,cast(99991231 as DATETIME)) as DT, isnull(PRODUTO,'000000') as PRODUTO, isnull(QTD,0) as QTD, isnull(UN,0) as UN from BYTEC.VIEWROTAREPRESENTANTE left JOIN #faturados on CLIENTE = CODIGO AND datediff(year,dt,now()) <= 2 ORDER BY DT DESC"]
    )


def pedidosemaberto():
    return ([])
