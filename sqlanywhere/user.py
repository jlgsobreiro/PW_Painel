import pyodbc

import sqlanywhere as SQL


class Usuario:
    def __init__(self, cnpj_cpf, codigo):
        self.qtd_clientes = None
        self.vlr_pedidos = None
        self.qtd_pedidos = None
        self.info = SQL.representante_info(cnpj_cpf=cnpj_cpf, codigo=codigo)
        if self.info:
            self.qtdclientes()
            self.vlrpedidos()
            self.qtdpedidos()

    def qtdpedidos(self):
        conn = pyodbc.connect(Dsn="PW64", uid="BYTEC", pwd="BYTEC")
        qtd_pedidos = conn.execute(
            f"select count(*) as res from VNDANFCD where ANFCD_REPRE = {self.info.get('AEMPR_CODIGO')}")
        res = SQL.cursor_para_lista_dict(qtd_pedidos)
        self.qtd_pedidos = res[0].get('res')
        conn.close()

    def vlrpedidos(self):
        conn = pyodbc.connect(Dsn="PW64", uid="BYTEC", pwd="BYTEC")
        vlr_pedidos = conn.execute(
            f"select sum(ANFCD_TOT_NOTA) as res from VNDANFCD where ANFCD_REPRE = {self.info.get('AEMPR_CODIGO')}")
        res = SQL.cursor_para_lista_dict(vlr_pedidos)
        self.vlr_pedidos = res[0].get('res')
        conn.close()

    def qtdclientes(self):
        conn = pyodbc.connect(Dsn="PW64", uid="BYTEC", pwd="BYTEC")
        query = f"select count(*) as res from SUPAEMPR where AEMPR_REPR = '{self.info.get('AEMPR_CODIGO')}' AND AEMPR_TIPO = 'C' AND AEMPR_STATUS = 'A'"
        qtd_clientes = conn.execute(query)
        res = SQL.cursor_para_lista_dict(qtd_clientes)
        self.qtd_clientes = res[0].get('res')
        conn.close()

    def is_authenticated(self):
        if self.is_active() and self.is_active():
            return True
        else:
            return False

    def is_active(self):
        if self.info.get("AEMPR_STATUS") == 'A':
            return True
        else:
            return False

    def is_anonymous(self):
        return False

    def get_id(self):
        if self.info:
            if self.info.get('AEMPR_CGC_CPF') == 'F':
                cpf_cnpj = self.info.get('AEMPR_CPF')
                return cpf_cnpj
            else:
                cpf_cnpj = self.info.get('AEMPR_CGC')
                return cpf_cnpj
        return None
