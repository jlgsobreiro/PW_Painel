import pymongo

import sqlanywhere as SQL


class Usuario:
    conn = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

    def __init__(self, cnpj_cpf, codigo):
        self.qtd_clientes = None
        self.vlr_pedidos = None
        self.qtd_pedidos = None
        self.info = self.get_info(cnpj_cpf=cnpj_cpf, codigo=codigo)

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

    @staticmethod
    def is_anonymous():
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

    def get_info(self, cnpj_cpf, codigo):
        mongo_client = pymongo.MongoClient(self.conn)
        if codigo is None:
            if len(cnpj_cpf) == 11:
                repre = mongo_client.get_database('prowater').get_collection('representantes').find_one(
                    {'AEMPR_CPF': cnpj_cpf})
            else:
                repre = mongo_client.get_database('prowater').get_collection('representantes').find_one(
                    {'AEMPR_CGC': cnpj_cpf})
            return repre
        repre = mongo_client.get_database('prowater').get_collection('representantes').find_one(
            {'AEMPR_CODIGO': codigo})
        if repre.get('AEMPR_CGC_CPF') == 'F':
            if repre.get('AEMPR_CPF') == cnpj_cpf:
                return repre
        else:
            if repre.get('AEMPR_CGC') == cnpj_cpf:
                return repre
        return None

    def get_clientes(self):
        mongo_client = pymongo.MongoClient(self.conn)
        res = mongo_client.get_database('prowater').get_collection('relatorio_de_compras').find(
            {'supervisores': self.info.get('AEMPR_CODIGO')})
        return res.__dict__()
