const dyn = require('./src/dynamodb')
const express = require('express');
const axios = require('axios')
const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');
const schedule = require('node-schedule');
const firebaseadmin = require('firebase-admin')


let serviceAccount = require("C:\\Users\\jl_so\\PycharmProjects\\prowater_painel\\sqlanywhere\\prowater-177d3-firebase-adminsdk-o3503-f5bfd1b53c.json");
firebaseadmin.initializeApp({
  credential: firebaseadmin.credential.cert(serviceAccount),
  databaseURL: "https://prowater-177d3.firebaseio.com"
});

const firestoredb = firebaseadmin.firestore();

//Configurações de conexão do MongoDB
const urlmongo = 'mongodb://localhost:27017';
const dbname = 'prowater';
const client = new MongoClient(urlmongo);

const app = express();

//Configurações do nodejs
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  next();
});
const port = process.env.PORT || 5001;

const minuto = 1000*60;

let resumo_cobrancas = {
  atualizados:0, inseridos:0, apagados:0,
  erros_atualizados:0, erros_inseridos:0, erros_apagados:0
};
let resumo_representantes = {
  atualizados:0, inseridos:0, apagados:0,
  erros_atualizados:0, erros_inseridos:0, erros_apagados:0
};
let resumo_cliente = {
  atualizados:0, inseridos:0, apagados:0,
  erros_atualizados:0, erros_inseridos:0, erros_apagados:0
};
let resumo_tabela_de_preco = {
  atualizados:0, inseridos:0, apagados:0,
  erros_atualizados:0, erros_inseridos:0, erros_apagados:0
};
let resumo_notas_canceladas = {
  atualizados:0, inseridos:0, apagados:0,
  erros_atualizados:0, erros_inseridos:0, erros_apagados:0
};
let resumo_pedidos_em_aberto = {
  atualizados:0, inseridos:0, apagados:0,
  erros_atualizados:0, erros_inseridos:0, erros_apagados:0
};
let resumo_historico_de_pedidos = {
  atualizados:0, inseridos:0, apagados:0,
  erros_atualizados:0, erros_inseridos:0, erros_apagados:0
};
let resumo_notas_faturadas = {
  atualizados:0, inseridos:0, apagados:0,
  erros_atualizados:0, erros_inseridos:0, erros_apagados:0
};

function insereAtualizaDynamoDB(tabela, item, resumo) {
  let value = item.value;
  let id = item.value._id.toString();
  delete value._id;
  //value.id =  id;
  if(dyn.pegaItemDynamoDBbyId(tabela,id)){
    dyn.modificaCobrancaDynamoDBbyId(tabela,id,value).then( value2 => {
      resumo.atualizados+=1;
    }).catch( reason => {
      console.error(tabela + ": " + reason);
      resumo.erros_atualizados+=1;
    });
  } else {
    dyn.insereItemDynamoDB(tabela,item.value).then(value2 => {
      resumo.inseridos+=1;
    }).catch(reason => {
      console.error(tabela + reason);
      resumo.erros_inseridos+=1;
    });
  }
}

//Requisição feita para a API do SQLAnywhere
//Usa a conexão do MongoDB como parametro
//Recebe no post do Axios uma lista de Representantes e depois atualiza o registro dele no MongoDB
function getApiRepresentantes(db) {
  axios.post(' http://127.0.0.1:5000/representantes',
  )
  .then((res) => {
    for (const value of res.data){
      db.collection("representantes")
          .findOneAndUpdate(
              {codigo: value.codigo},
              {$set: value},
              {upsert: true, returnOriginal: false})
        .then( value1 => {
          insereAtualizaDynamoDB("Representantes", value1, resumo_representantes);
          console.log("Representante atualizado" + value1)
      })
        .catch(reason => {
        console.error("Error REP",reason)
      })
    }
  })
  .catch((error) => {
    console.error(error)
  })
}

//Requisição feita para a API do SQLAnywhere
//Usa a conexão do MongoDB como parametro
//Recebe no post do Axios uma lista de Clientes e
// depois atualiza o registro dele no MongoDB
/**@param {MongoClient} db Cliente MongoDB*/
function getApiclientes(db) {
  //let batchWrites = {batch:[firestoredb.batch()], page:0 , limit: 0};
  axios.post(' http://127.0.0.1:5000/cliente',
  )
  .then(async (res) => {
    console.log("getApiClientes");
    for (const value of res.data) {
      let response = await db.collection("clientes")
        .findOne({codigo: value.codigo}, {projection: {_id: 0, uptodate: 0}})
      if (JSON.stringify(value) === JSON.stringify(response)){
        console.log("%s: %s Uptodate",new Date(),value.codigo);
        db.collection("clientes")
        .findOneAndUpdate(
          {codigo: value.codigo},
          [{$set: {uptodate: true}}]
        )
        .then(value1 => {
          //insereAtualizaDynamoDB("Cliente", value1, resumo_cliente);
        })
        .catch(reason => {console.error("Error CLI",reason)})
      } else {
        value['uptodate'] = false;
        db.collection("clientes")
        .findOneAndUpdate(
          {codigo: value.codigo},
          [{$set: value}],
          {upsert: true}
        )
        .then( value1 => {
          delete value1.uptodate;
          insereAtualizaDynamoDB("Cliente", value1, resumo_cliente);
          //console.log("Cliente atualizado" + value1.value.codigo);
        })
        .catch(reason => {
          console.error("Error CLI",reason);
        })
      }
    }
  })
  .catch((error) => {
    console.error(error)
  })
}

//Requisição feita para a API do SQLAnywhere
//Usa a conexão do MongoDB como parametro
//Recebe no post do Axios uma lista de Produtos e
// seus valores de acordo com a tabela de preços
// e depois atualiza os registros deles no MongoDB
/**@param {MongoClient} db Cliente MongoDB*/
function getApiTabelaPreco(db) {
  axios.post('http://127.0.0.1:5000/tabela_preco',
  )
  .then( async (res) => {
    for (const value of res.data) {
      let id = value.empresa+value.tabela+value.codigo.trim()
      let response = await db.collection("tabela_preco")
        .findOne({codigo: value.codigo, empresa: value.empresa, tabela: value.tabela},
          {projection: {_id: 0, uptodate: 0}});
      if (JSON.stringify(value) === JSON.stringify(response)) {
        db.collection("tabela_preco")
          .findOneAndUpdate(
            {codigo: value.codigo,
              empresa: value.empresa,
              tabela: value.tabela},
            {$set: {uptodate: true}}
            )
          .then(value1 => {
            insereAtualizaDynamoDB("Tabela_de_preco", value1, resumo_tabela_de_preco);
            //console.log("%s: %s Uptodate",new Date(),id)
          })
          .catch(reason => {
            console.error("Error TAB MongoDB", reason)
          });
      } else {
        value["uptodate"] = false;
        db.collection("tabela_preco")
          .findOneAndUpdate(
            {codigo: value.codigo,
              empresa: value.empresa,
              tabela: value.tabela},
            {$set: value},
            {upsert: true})
          .then( async value1 => {
            //console.log("%s: %s Outdated",new Date(),id);
            delete value1.uptodate;
            insereAtualizaDynamoDB("Tabela_de_preco", value1, resumo_tabela_de_preco);
          })
          .catch(reason => {
            console.error("Error TAB MongoDB->Firebase", reason)
          });
      }
    }
  })
  .catch((error) => {
    console.error(error)
  })
}


//Requisição feita para a API do SQLAnywhere
//Usa a conexão do MongoDB como parametro
//Recebe no post do Axios uma lista de Produtos e
// seus valores de acordo com a tabela de preços
// e depois atualiza os registros deles no MongoDB
/**@param {MongoClient} db Cliente MongoDB*/
function getApiTabelaPrecoFinal(db) {
  axios.post('http://127.0.0.1:5000/tabela_preco_final',
  )
  .then( (res) => {
    for (const value of res.data){
      db.collection("tabela_preco_final")
          .findOneAndUpdate(
              {codigo: value.codigo,empresa: value.empresa},
              {$set: value},
              {upsert: true})
          .then(val =>{
            const item = val;
            const id = item._id.toString();
            delete item._id;
            item.id = id;
            if (dyn.pegaItemDynamoDBbyId("Tabela_preco_final",item.id)){
              dyn.modificaCobrancaDynamoDBbyId("Tabela_preco_final",item.id,item)
            } else {
              dyn.insereItemDynamoDB("Tabela_preco_final", item);
            }
          })
          .catch( error => {
            console.log("Tabela_de_preco_final: "+error)
          })
    }
  })
  .catch((error) => {
    console.error(error)
  })
}

//Requisição feita para a API do SQLAnywhere
//Usa a conexão do MongoDB como parametro
//Recebe no post do Axios uma lista de Empresas
// devedoras e depois atualiza ou apaga o registro
// dela no MongoDB casa já não exista no SQLAnywhere
/**@param {MongoClient} db Cliente MongoDB*/
async function getApicobrancas(db) {
  let tempo_recebido = Date.now()
  //let cobs = await dyn.listaItemsTabela("Cobrancas");
  //console.log(cobs)
  await axios.post(' http://127.0.0.1:5000/cobrancas')
      .then((res) => {
        while (res.data) {
          let value = res.data.pop();
          value["valido"] = tempo_recebido;
          db.collection("cobrancas")
              .findOneAndUpdate(
                  {cliente: value.cliente, empresa: value.empresa, nota_fiscal: value.nota_fiscal},
                  {$set: value},
                  {upsert: true, returnOriginal: false})
              .then( value1 => {
                insereAtualizaDynamoDB("Cobrancas", value1, resumo_cobrancas)
                //console.log("OK",value)
              })
              .catch(reason => {
                console.error("Error COB", reason)
              })
        }
      }).catch(e => {
      console.log("Erro,",e);
    })
  console.log("Apagando?");
  db.collection("cobrancas")
    .find({valido : {$ne: tempo_recebido}})
      .toArray( function (err, result) {
        if (err) throw err
        else {
          for (const val in result) {
            //console.log(result[val]._id + ' Apagando');
            dyn.apagaItemDynamoDBbyId('Cobrancas', result[val]._id).then(value => {
              resumo_cobrancas.apagados += 1;
            }).catch(reason => {
              console.log('Não foi possivel apagar item: ' + reason);
              resumo_cobrancas.erros_apagados += 1;
            });

            db.collection('cobrancas').deleteOne({_id: result[val]._id}, function (err, res) {
              if (err) {
                throw err;
              } else {
                console.log(' Documento de id %s apagado', result[val]._id)
              }
            })
          }
        }
      })
}

//Requisição feita para a API do SQLAnywhere
//Usa a conexão do MongoDB como parametro
//Recebe no post do Axios uma lista de Produtos
// produzidos e depois atualiza o registro deles no
// MongoDB
/**@param {MongoClient} db Cliente MongoDB*/
function getApiProducao(db) {
  axios.post(' http://127.0.0.1:5000/producao',
  )
  .then((res) => {
    res.data.forEach(value => {
      db.collection("producao").findOneAndUpdate({numero_op: value.numero_op},{$set: value},{upsert: true}).then(value => {
        //console.log("OK",value)
      }).catch(reason => {
        console.error("Error PROD",reason)
      })
    })
  })
  .catch((error) => {
    console.error(error)
  })
}

//Requisição feita para a API do SQLAnywhere
//Usa a conexão do MongoDB como parametro
//Recebe no post do Axios uma lista de Notas que foram
// canceladas e o motivo e depois atualiza o registro
// dele no MongoDB
/**@param {MongoClient} db Cliente MongoDB*/
function getApiNotasCanceladas(db) {
  axios.post(' http://127.0.0.1:5000/notascanceladas',
  )
  .then((res) => {
    res.data.forEach(value => {
      db.collection("notas_canceladas")
        .findOneAndUpdate(
            {cliente: value.cliente, empresa: value.empresa, nff: value.nff},
            {$set: value},
            {upsert: true})
        .then(value1 => {
          insereAtualizaDynamoDB("Notas_canceladas", value1, resumo_notas_canceladas);
        //console.log("OK",value)
      }).catch(reason => {
        console.error("Error NC",reason)
      })
    })
  })
  .catch((error) => {
    console.error(error)
  })
}

//Requisição feita para a API do SQLAnywhere
//Usa a conexão do MongoDB como parametro
//Recebe no post do Axios uma lista de Pedidos em aberto
// e depois atualiza ou apaga o registro dele no MongoDB
// caso já tenha sido entregue
/** @deprecated  Precisa se Atualizada para ser equivalente
 * a tabela de pedidos em aberto
*@param {MongoClient} db Cliente MongoDB*/
function getApiEntregaDivida(db) {
  axios.post(' http://127.0.0.1:5000/entregadivida',
  )
  .then((res) => {
    let tempo_recebido = Date.now()
    res.data.forEach(value => {
      value["valido"] = tempo_recebido;
      db.collection("entrega_divida")
        .update({cliente: value.cliente,empresa: value.empresa, pedido: value.pedido},{$set: value},{upsert: true})
        .then(value => {
        //console.log("OK",value)
      }).catch(reason => {
        console.error("Error ENTD",reason)
      })
    })
      db.collection("entrega_divida")
        .removeMany({valido : {$ne: tempo_recebido}})
        .then(value => {})
        .catch( reason => {})
  })
  .catch((error) => {
    console.error(error)
  })
}

//Requisição feita para a API do SQLAnywhere
//Usa a conexão do MongoDB como parametro
//Recebe no post do Axios uma lista de Notas fiscais emitidas
// e depois atualiza ou insere o registro delas no MongoDB
// caso não existam
/**@param {MongoClient} db Cliente MongoDB*/
function getApiEmissaoNotas(db) {
  axios.post(' http://127.0.0.1:5000/emissaonotas',
  )
  .then((res) => {
    res.data.forEach(value => {
      db.collection("emissao_notas")
          .findOneAndUpdate({data: value.data},{$set: value},{upsert: true})
          .then(value => {
        //insereAtualizaDynamoDB("")
        //console.log("OK",value)
      }).catch(reason => {
        console.error("Error EMN",reason)
      })
    })
  })
  .catch((error) => {
    console.error(error)
  })
}

function getApiNotasFaturadas(db) {
  let tempo_recebido = Date.now()
  axios.post(' http://127.0.0.1:5000/notasfaturadas',
  )
  .then((res) => {
    console.log("notas faturadas: ",res.data.length);
    while (res.data) {
      let value = res.data.pop();
      value.atualizado = tempo_recebido;
      db.collection("notas_faturadas")
          .findOneAndUpdate(
              {produto: value.produto, nota: value.nota, cliente: value.cliente, empresa: value.empresa},
              {$set: value},
              {upsert: true})
          .then(value1 => {
            //console.log(value1)
            if (value1.lastErrorObject.updatedExisting === true){
              insereAtualizaDynamoDB("Notas_faturadas",value1, resumo_notas_faturadas);
            }
      }).catch(reason => {
        console.error("Error NOTA_FAT",reason)
      })
    }
  })
  .catch((error) => {
    console.error(error)
  })
}

function getApiPedidosEmAberto(db) {
  //console.log("Pedidos_em_aberto");
  axios.post('http://127.0.0.1:5000/pedidosabertos',
  )
  .then((res) => {
    while (res.data){
      let value = res.data.pop();
      db.collection("pedidos_abertos")
          .findOneAndUpdate(
              {pedido: value.pedido, cliente: value.cliente, empresa: value.empresa},
              {$set: value},
              {upsert: true})
          .then(value1 => {
            if (value1.lastErrorObject.updatedExisting === true){
              //console.log(value1);
              insereAtualizaDynamoDB("Pedidos_em_aberto",value1,resumo_pedidos_em_aberto);
            }
            //console.log("OK",value)
          }).catch(reason => {
            console.error("Error PED_AB",reason);
          })
    }
  })
  .catch((error) => {
    console.error(error)
  })
}

function getApiPedidosCadastrados(db) {
  axios.post('http://127.0.0.1:5000/pedidoscadastrados',
  )
  .then((res) => {
    while (res.data) {
      let value = res.data.pop();
      db.collection("pedidos_cadastrados")
          .findOneAndUpdate(
              {produto: value.produto, pedido: value.pedido, cliente: value.cliente, empresa: value.empresa},
              {$set: value},
              {upsert: true})
          .then(value1 => {
            if (value1.lastErrorObject.updatedExisting === true) {
              //console.log(value1);
              insereAtualizaDynamoDB("Historico_de_pedidos", value1, resumo_historico_de_pedidos);
            }
            //console.log("OK",value)
          }).catch(reason => {
        console.error("Error PED_CAD", reason)
      })
    }
  }).catch((error) => {
    console.error(error)
  })
}

//Requisição feita para a API do SQLAnywhere
//Usa a conexão do MongoDB como parametro
//Recebe no post do Axios uma lista de Clientes e a ultima
//compra feita por ele e outras informações e atualiza ou
//insere no MongoDB
/**@param {MongoClient} db Cliente MongoDB*/
/*function getApiRelatoriodecompras(db) {
  axios.post(' http://127.0.0.1:5000/relatoriodecompras',
  )
  .then((res) => {
    res.data.forEach(value => {
      db.collection("relatorio_de_compras").findOneAndUpdate({codigo: value.codigo},{$set: value},{upsert: true}).then(value => {
    //console.log("OK",value)
  }).catch(reason => {
    console.error("Error REL",reason)
  })
    })
  })
  .catch((error) => {
    console.error(error)
  })
}*/


/**@param {MongoClient} mongoClient Cliente MongoDB
 * @param {firestoredb} firestoreDatabase Cliente Firestore
 * @this getFirestoreClientes
 * Sincroniza dados de Clientes do Firebase com a coleção "relatorio_de_compras_firestore"
 * @deprecated Não é mais necessario */
/*function getFirestoreClientes(mongoClient, firestoreDatabase){
  firestoredb.collection("clientes")
    .get()
    .then(value => {
      mongoClient
        .collection("relatorio_de_compras_firestore")
        .updateMany(
          {codigo: value.codigo},
          {$set: value},
          {upsert: true})
        .then(value => {
          console.log("??",value.toString().hashCode())
        })
        .catch(reason => {
          console.error("Error REL",reason)
        })
    })
    .catch(reason => {})
}*/
/** @deprecated Não é mais necessario */
/*function getFirestoreCobrancas(db){
  firestoredb.collection("cobrancas_firestore")
    .get()
    .then(value => {
      db.collection("cobrancas")
        .update(
          {cliente: value.cliente, empresa: value.empresa, nota_fiscal: value.nota_fiscal},
          {$set: value},
          {upsert: true})
        .then(value => {
        //console.log("OK",value)
      }).catch(reason => {
        console.error("Error COB",reason)
      })
    })
    .catch(reason => {})
}*/
/** @deprecated Não é mais necessario */
/*function getFirestoreRepresentantes(db){
  firestoredb.collection("representantes_firestore")
    .get()
    .then(value => {})
    .catch(reason => {})
}*/
/** @deprecated Não é mais necessario */
/*function getFirestoreTabeladePreco(db){
  firestoredb.collection("tabela_de_preco_firestore")
    .get()
    .then(value => {})
    .catch(reason => {})
}*/
/** @deprecated Não é mais necessario */
/*function getFirestorePedidos(db){
  firestoredb.collection("teste_firestore")
    .get()
    .then(value => {})
    .catch(reason => {})
}*/

dyn.verificaTabelaDynamoDb("Cliente");
console.log("Verifica CLiente")
dyn.verificaTabelaDynamoDb("Cobrancas");
console.log("Verifica Cobrancas")
dyn.verificaTabelaDynamoDb("Tabela_de_preco");
console.log("Verifica Tabela de Preco")
dyn.verificaTabelaDynamoDb("Tabela_de_preco_final");
console.log("Verifica Tabela de preco final")
dyn.verificaTabelaDynamoDb("Emails");
console.log("Verifica Emails")
dyn.verificaTabelaDynamoDb("Endereco");
console.log("Verifica endereco")
dyn.verificaTabelaDynamoDb("Linha_pedidos");
console.log("Verifica Linha pedidos")
dyn.verificaTabelaDynamoDb("Notas_canceladas");
console.log("Verifica Notas Canceladas")
dyn.verificaTabelaDynamoDb("Pedidos");
console.log("Verifica Pedidos")
dyn.verificaTabelaDynamoDb("Telefones");
console.log("Verifica Telefones")
dyn.verificaTabelaDynamoDb("Representantes");
console.log("Verifica Representantes")
dyn.verificaTabelaDynamoDb("Notas_faturadas");
console.log("Verifica Notas Faturadas")
//dyn.verificaTabelaDynamoDb("Pedidos_em_aberto");
console.log("Verifica Pedidos em aberto")
//dyn.verificaTabelaDynamoDb("Historico_de_pedidos");
console.log("Verifica historico de pedidos")
dyn.listaTabelas();
//dyn.apagaItemDynamoDBbyId("Cobrancas", "MdfMPsEgf24J4VuGVqHK");

//Conexão com MongoDb
//Sincroniza com banco de dados SQLAnywhere
client.connect(async (mongoError) =>{
  assert.strictEqual(null,mongoError);
  console.log("Connected to mongodb server");
  const db = client.db(dbname);

  //setTimeout(() => {getApiclientes(db)},5000);
  //setTimeout(() => {getApiTabelaPreco(db)},5000);
  //setTimeout(() => {getApiTabelaPrecoFinal(db)},5000);
  //setTimeout(() => {getApiRepresentantes(db);},5000);
  //setTimeout(() => {getApiNotasCanceladas(db)},5000);
  //setTimeout(() => {getApiEmissaoNotas(db)},5000);
  //setTimeout(() => {getApiPedidosEmAberto(db)},5000);
  //setTimeout(() => {getApiPedidosCadastrados(db)},5000);
  //setTimeout(() => {getApiNotasFaturadas(db)},5000);
  //setTimeout(() => {getApicobrancas(db)},5000);
  //setTimeout(() => {getApiEntregaDivida(db)},5000);
  //setTimeout(() => {getApiRelatoriodecompras(db)},5000);
  //setTimeout(() => {getFirestoreClientes(db)},5000);
  //setTimeout(() => {getApiProducao(db)}, 5000);
  //await client.close();
});

/** @param batchWrites {{batch:Object},{page:number},{limit:number}} Batch de documentos e quantidade,
 * @param documento {Object} Documento do cliente */
/*async function updateClienteFirestore( documento, batchWrites) {
  let clienteRef = await firestoredb.collection("clientes").doc(documento.codigo);
  if (batchWrites.limit <= 2) {
    try {
      batchWrites.batch[batchWrites.page] = firestoredb.batch().set(clienteRef,documento)
      console.log("UpdateClienteFirestore: ", batchWrites.limit);
    }catch (e) {
      console.log("UpdateClienteFirestore catch:",e);
    }
  } else {
    batchWrites.page+=1
    batchWrites.limit = 0;
    console.log("Batch Page Created:", batchWrites.page);
  }
}*/

//setInterval(() => {getApiProducao(client.db(dbname))}, 3*minuto);
//setInterval(() => {getApiTabelaPreco(client.db(dbname))},3*minuto);
//setInterval(() => {getApiRepresentantes(client.db(dbname));},3*minuto);
//setInterval(() => {getApicobrancas(client.db(dbname))},3*minuto);
//setInterval(() => {getApiNotasCanceladas(client.db(dbname))},3*minuto);
//setInterval(() => {getApiEmissaoNotas(client.db(dbname))},3*minuto);
//setInterval(() => {getApiEntregaDivida(client.db(dbname))},3*minuto);
//setInterval(() => {getApiRelatoriodecompras(client.db(dbname))},3*minuto);
//setInterval(() => {getApiclientes(client.db(dbname))},3*minuto);
//setInterval(() => {console.log("RES_cob: "+resumo_cobrancas.erros_atualizados)},minuto/10);
//setInterval(() => {console.log("RES_cli: "+resumo_cliente.erros_atualizados)},minuto/10);
//setInterval(() => {console.log("RES_rep: "+resumo_representantes.erros_atualizados)},minuto/10);
//setInterval(() => {console.log("RES_not: "+resumo_notas_canceladas.erros_atualizados)},minuto/10);
//setInterval(() => {console.log("RES_tab: "+resumo_tabela_de_preco.erros_atualizados)},minuto/10);
//setInterval(() => {console.log("RES_HIST_PED: "+resumo_historico_de_pedidos.erros_atualizados)},minuto/10);
//setInterval(() => {console.log("RES_NOTA_FAT: "+resumo_notas_faturadas.erros_atualizados)},minuto/10);
//setInterval(() => {console.log("RES_PED_ABR: "+resumo_pedidos_em_aberto.erros_atualizados)},minuto/10);

app.get('/api/producao', (req, res) => {
  client.db(dbname).collection("producao")
      .find({})
      .sort({numero_op: -1})
      .limit(200)
      .toArray( (err, result) => {
    if (err) throw err;
    res.send(result);
  })
});
app.get('/api/tabelapreco', (req, res) => {
  client.db(dbname).collection("tabela_preco")
      .find({})
      .sort({})
      .toArray( (err, result) => {
    if (err) throw err;
    res.send(result);
  })
});
app.get('/api/tabelaprecofinal', (req, res) => {
  client.db(dbname).collection("tabela_preco_final")
      .find({})
      .sort({})
      .toArray( (err, result) => {
    if (err) throw err;
    res.send(result);
  })
});
app.get('/api/representantes', (req, res) => {
  client.db(dbname).collection("representantes")
      .find({})
      .sort({})
      .toArray( (err, result) => {
    if (err) throw err;
    res.send(result);
  })
});
app.get('/api/cobrancas', (req, res) => {
  client.db(dbname).collection("cobrancas")
      .find({})
      .toArray( (err, result) => {
    if (err) throw err;
    res.send(result);
  })
});
app.get('/api/notascanceladas', (req, res) => {
  client.db(dbname).collection("notas_canceladas")
      .find({})
      .sort({})
      .toArray( (err, result) => {
    if (err) throw err;
    res.send(result);
  })
});
app.get('/api/emissaonotas', (req, res) => {
  client.db(dbname).collection("emissao_notas")
      .find({})
      .sort({})
      .toArray( (err, result) => {
    if (err) throw err;
    res.send(result);
  })
});
app.get('/api/entregadivida', (req, res) => {
  res.send({ express: 'Hello From Express' });
});
app.get('/api/relatoriodecompras', (req, res) => {
  res.send({ express: 'Hello From Express' });
});
app.get('/api/clientes', (req, res) => {
  client.db(dbname).collection("Clientes")
      .find({})
      .sort({})
      .toArray( (err, result) => {
    if (err) throw err;
    res.send(result);
  })
});
app.get('/api/notasfaturadas', (req, res) => {
  client.db(dbname).collection("notas_faturadas")
      .find({})
      .sort({})
      .toArray( (err, result) => {
    if (err) throw err;
    res.send(result);
  })
});
app.get('/api/pedidosabertos', (req, res) => {
  client.db(dbname).collection("pedidos_abertos")
      .find({})
      .sort({})
      .toArray( (err, result) => {
    if (err) throw err;
    res.send(result);
  })
});
app.route('/api/pedidoscadastrados').post((req, res) => {
  client.db(dbname).collection("pedidos_cadastrados")
      .find({cliente:req.cliente.codigo})
      .sort({})
      .toArray( (err, result) => {
    if (err) throw err;
    res.send(result);
  })
}).get((req, res) => {
  client.db(dbname).collection("pedidos_cadastrados")
      .find({})
      .sort({})
      .toArray( (err, result) => {
    if (err) throw err;
    res.send(result);
  })
});
app.get('/api/mensagem', (req, res) => {
  res.send({ express: 'Hello From Express' });
});

app.listen(port, () => console.log(`Listening on port ${port}`));
