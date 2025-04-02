import boto3

dynamodb = boto3.resource("dynamodb")


def verifica_tabela(nome_tabela):
    try:
        tabela = dynamodb.Table(nome_tabela)
        print(f"{nome_tabela} carregado")
        return tabela
    except:
        tabela = dynamodb.create_table(
            TableName=nome_tabela,
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        print(f"Tabela {nome_tabela} criada")
        return tabela
