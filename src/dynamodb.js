const AWS = require("aws-sdk");

AWS.config.update({
  region: "us-east-1",
  endpoint: "http://localhost:8000",
  accessKeyId: "AKIAYTPQYP6WK2RLCWXQ",
  secretAccessKey: "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"
});

var dynamodb = new AWS.DynamoDB();

module.exports = {
  listaItemsTabela: function listaItemsTabela(tabela_nome){
    var params = {
      TableName: tabela_nome
    };
    dynamodb.scan(params, function(err, data) {
      if (err) console.log(err, err.stack); // an error occurred
      else return data; // successful response
    });
  },
  listaTabelas: function listaTabelas(){
    var params = {};
    dynamodb.listTables(params, function(err, data) {
      if (err) {
        console.log(err, err.stack);
      } // an error occurred
      else {
        console.log(data);
        return data;
      } // successful response
    });
  },
   listaTabelas2: function listaTabelas2(){
    return new Promise((resolve, reject) => {
      var params = {};
      dynamodb.listTables(params, function(err, data) {
        if (err) {
          reject(err)
        } // an error occurred
        else {
          resolve(data);
        } // successful response
      });
    })
  },
  verificaTabelaDynamoDb: function verificaTabelaDynamoDb(nome_tabela) {
    let params = {
      TableName : nome_tabela,
      KeySchema : [{AttributeName: 'id', KeyType: 'HASH'}],
      AttributeDefinitions: [
          {AttributeName: 'id', AttributeType: 'S'}
      ],
      ProvisionedThroughput: {
        ReadCapacityUnits: 1,
        WriteCapacityUnits: 1
      },
    }
    dynamodb.createTable(params, function(err, data) {
      if (err) {
        if (err.code === "ResourceInUseException"){
          console.error("Tabela %s já existe",nome_tabela);
        } else {
          console.error("Unable to create table. Error JSON:", JSON.stringify(err, null, 2));
        }
      } else {
          console.log("Created table. Table description JSON:", JSON.stringify(data, null, 2));
      }
    });
  },
  insereItemDynamoDB: function insereItemDynamoDB(tabela, Item){
    let docClient = new AWS.DynamoDB.DocumentClient();
    let dynamoDBParams = {
      TableName: tabela,
      Item: Item
    };
    return new Promise((resolve, reject) => {
      docClient.put(dynamoDBParams, function (err,data) {
      if (err){
        reject(err);
      } else {
        resolve(data);
      }
    })
    })
  },
  pegaItemDynamoDBbyId: function pegaItemDynamoDBbyId(tabela, id){
    let docClient = new AWS.DynamoDB.DocumentClient();
    let dynamoDBParams = {
      TableName: tabela,
      Key: {id: id}
    }
    return new Promise((resolve, reject) => {
      try {
        docClient.get(dynamoDBParams, function (err,data) {
          if (err){
            reject(err);
          } else {
            //console.log("Got item:", JSON.stringify(data, null, 2));
            resolve(data);
          }
        })
      } catch (e) {
        reject(e);
      }
    })
  },
  apagaItemDynamoDBbyId: function apagaItemDynamoDBbyId(tabela, id){
    let docClient = new AWS.DynamoDB.DocumentClient();
    let dynamoDBParams = {
      TableName: tabela,
      Key: {id: id}
    }
    return new Promise((resolve, reject) => {
      docClient.delete(dynamoDBParams, function (err,data) {
        if (err){
          reject(err);
        } else {
          resolve(data);
        }
      })
    })
  },
  modificaCobrancaDynamoDBbyId: function modificaCobrancaDynamoDBbyId(tabela, id, valores){
    let docClient = new AWS.DynamoDB.DocumentClient();
    let updateExpression = "set ";
    let expressionAttributeValues = {};
   for (let item in valores){
     updateExpression += item+' = :'+item+', ';
     expressionAttributeValues[':'+item] = valores[item];
   }
   updateExpression = updateExpression.substring(0,updateExpression.length-2)
    let dynamoDBParams = {
      TableName: tabela,
      Key: {id: id},
      UpdateExpression: updateExpression,
      ExpressionAttributeValues: expressionAttributeValues
    }
   return new Promise((resolve, reject) => {
     docClient.update(dynamoDBParams, function (err,data) {
      if (err){
        reject(err);
      } else {
        resolve(data);
      }
    })
   })
  },
  pegaItemDynamoDBbyKey: function pegaItemDynamoDBbyKey(tabela, key){
    let docClient = new AWS.DynamoDB.DocumentClient();
    let dynamoDBParams = {
      TableName: tabela,
      Key: key
    }
    docClient.get(dynamoDBParams, function (err,data) {
      if (err){
        console.error("Unable to get item. Error JSON:", JSON.stringify(err, null, 2));
      } else {
        //console.log("Got item:", JSON.stringify(data, null, 2));
        return data.Item;
      }
    })
  },
  apagaItemDynamoDBbyKey: function apagaItemDynamoDBbyKey(tabela, key){
    let docClient = new AWS.DynamoDB.DocumentClient();
    let dynamoDBParams = {
      TableName: tabela,
      Key: key
    }
    docClient.delete(dynamoDBParams, function (err,data) {
      if (err){
        console.error("Unable to get item. Error JSON:", JSON.stringify(err, null, 2));
      } else {
        //console.log("Got item:", JSON.stringify(data, null, 2));
        return data.Item;
      }
    })
  }
}
