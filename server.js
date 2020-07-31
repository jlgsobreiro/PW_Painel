const express = require('express');
const axios = require('axios')
const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');
const schedule = require('node-schedule');
const firebaseadmin = require('firebase-admin')

let serviceAccount = require("C:\\Users\\JLGS\\PycharmProjects\\prowater_painel\\sqlanywhere\\prowater-177d3-firebase-adminsdk-o3503-f5bfd1b53c.json");
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

//Requisição feita para a API do SQLAnywhere
//Usa a conexão do MongoDB como parametro
//Recebe no post do Axios uma lista de Representantes e depois atualiza o registro dele no MongoDB
function getApiRepresentantes(db) {
  axios.post(' http://127.0.0.1:5000/representantes',
  )
  .then((res) => {
    for (const value of res.data){
      db.collection("representantes").update({codigo: value.codigo}, {$set: value},{upsert: true})
        .then(value => {
        //console.log("OK",value)
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
  let batchWrites = {batch:[firestoredb.batch()], page:0 , limit: 0};

  axios.post(' http://127.0.0.1:5000/cliente',
  )
  .then(async (res) => {
    console.log("getApiClientes");
    for (const value of res.data) {
      let response = await db.collection("clientes")
        .findOne({codigo: value.codigo}, {projection: {_id: 0, uptodate: 0}})
      if (JSON.stringify(value) === JSON.stringify(response)){
        db.collection("clientes")
        .findOneAndUpdate(
          {codigo: value.codigo},
          [{$set: {uptodate: true}}]
        )
        .then(value => {})
        .catch(reason => {console.error("Error CLI",reason)})
      } else {
        value['uptodate'] = false;
        db.collection("clientes")
        .findOneAndUpdate(
          {codigo: value.codigo},
          [{$set: value}],
          {upsert: true}
        )
        .then( async v => {
          console.log("atualizando");
          let cliente = await firestoredb.collection("clientes").doc(value.codigo).set(value);
          let tries = 0;
          while (!cliente && tries < 3){
            try {
              let cliente = await firestoredb.collection("clientes").doc(value.codigo).set(value);
              console.log("Cliente: ",cliente);
            } catch (e) {
              tries++;
              console.log("Erro ao ao enviar documento. Tentativa ",tries,"/3")
            }
          }


          /*batchWrites.limit+=1;
          updateClienteFirestore(value, batchWrites).then(async value1 => {
            if (batchWrites.limit === 0) {
              await batchWrites.batch[batchWrites.page-1].commit()
                .then(value => {
                  console.log("Commited Batch Documentes");
                })
                .catch(reason => {
                  console.error("Error Batch Commit: ",reason);
                });
              }
          }).catch(reason => {
            console.error("Error Update Cliente Firestore: ",reason)
          });*/
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
  axios.post(' http://127.0.0.1:5000/tabela_preco',
  )
  .then((res) => {
    res.data.forEach(value => {
      db.collection("tabela_preco")
        .update({codigo: value.codigo, empresa: value.empresa, tabela: value.tabela}, {$set: value},{upsert: true})
        .then(value => {
        //console.log("OK",value)
      })
        .catch(reason => {
        console.error("Error TAB",reason)
      })
    })
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
function getApicobrancas(db) {
  axios.post(' http://127.0.0.1:5000/cobrancas',
  )
  .then((res) => {
    let tempo_recebido = Date.now()
    res.data.forEach(value => {
      value["valido"] = tempo_recebido;
      db.collection("cobrancas")
        .update({cliente: value.cliente, empresa: value.empresa, nota_fiscal: value.nota_fiscal},{$set: value},{upsert: true})
        .then(value => {
        //console.log("OK",value)
      })
        .catch(reason => {
        console.error("Error COB",reason)
      })
    })
    db.collection("cobrancas")
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
//Recebe no post do Axios uma lista de Produtos
// produzidos e depois atualiza o registro deles no
// MongoDB
/**@param {MongoClient} db Cliente MongoDB*/
function getApiProducao(db) {
  axios.post(' http://127.0.0.1:5000/producao',
  )
  .then((res) => {
    res.data.forEach(value => {
      db.collection("producao").update({numero_op: value.numero_op},{$set: value},{upsert: true}).then(value => {
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
        .update({cliente: value.cliente, empresa: value.empresa, nff: value.nff},{$set: value},{upsert: true})
        .then(value => {
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
      db.collection("emissao_notas").update({data: value.data},{$set: value},{upsert: true}).then(value => {
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

//Requisição feita para a API do SQLAnywhere
//Usa a conexão do MongoDB como parametro
//Recebe no post do Axios uma lista de Clientes e a ultima
//compra feita por ele e outras informações e atualiza ou
//insere no MongoDB
/**@param {MongoClient} db Cliente MongoDB*/
function getApiRelatoriodecompras(db) {
  axios.post(' http://127.0.0.1:5000/relatoriodecompras',
  )
  .then((res) => {
    res.data.forEach(value => {
      db.collection("relatorio_de_compras").update({codigo: value.codigo},{$set: value},{upsert: true}).then(value => {
    //console.log("OK",value)
  }).catch(reason => {
    console.error("Error REL",reason)
  })
    })
  })
  .catch((error) => {
    console.error(error)
  })
}


/**@param {MongoClient} mongoClient Cliente MongoDB
 * @param {firestoredb} firestoreDatabase Cliente Firestore
 * @this getFirestoreClientes
 * Sincroniza dados de Clientes do Firebase com a coleção "relatorio_de_compras_firestore"
 * @deprecated Não é mais necessario */
function getFirestoreClientes(mongoClient, firestoreDatabase){
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
}
/** @deprecated Não é mais necessario */
function getFirestoreCobrancas(db){
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
}
/** @deprecated Não é mais necessario */
function getFirestoreRepresentantes(db){
  firestoredb.collection("representantes_firestore")
    .get()
    .then(value => {})
    .catch(reason => {})
}
/** @deprecated Não é mais necessario */
function getFirestoreTabeladePreco(db){
  firestoredb.collection("tabela_de_preco_firestore")
    .get()
    .then(value => {})
    .catch(reason => {})
}
/** @deprecated Não é mais necessario */
function getFirestorePedidos(db){
  firestoredb.collection("teste_firestore")
    .get()
    .then(value => {})
    .catch(reason => {})
}

//Conexão com MongoDb
//Sincroniza com banco de dados SQLAnywhere
client.connect(async (mongoError) =>{
  assert.strictEqual(null,mongoError);
  console.log("Connected to mongodb server");
  const db = client.db(dbname);
  //setTimeout(() => {getApiProducao(db)}, 5000);
  //setTimeout(() => {getApiTabelaPreco(db)},5000);
  //setTimeout(() => {getApiRepresentantes(db);},5000);
  //setTimeout(() => {getApicobrancas(db)},5000);
  //setTimeout(() => {getApiNotasCanceladas(db)},5000);
  //setTimeout(() => {getApiEmissaoNotas(db)},5000);
  //setTimeout(() => {getApiEntregaDivida(db)},5000);
  //setTimeout(() => {getApiRelatoriodecompras(db)},5000);
  //setTimeout(() => {getFirestoreClientes(db)},5000);
  setTimeout(() => {getApiclientes(db)},5000);
  //await client.close();
});

/** @param batchWrites {{batch:Object},{page:number},{limit:number}} Batch de documentos e quantidade,
 * @param documento {Object} Documento do cliente */
async function updateClienteFirestore( documento, batchWrites) {
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
}

//setInterval(() => {getApiProducao(client.db(dbname))}, 3*minuto);
//setInterval(() => {getApiTabelaPreco(client.db(dbname))},3*minuto);
//setInterval(() => {getApiRepresentantes(client.db(dbname));},3*minuto);
//setInterval(() => {getApicobrancas(client.db(dbname))},3*minuto);
//setInterval(() => {getApiNotasCanceladas(client.db(dbname))},3*minuto);
//setInterval(() => {getApiEmissaoNotas(client.db(dbname))},3*minuto);
//setInterval(() => {getApiEntregaDivida(client.db(dbname))},3*minuto);
//setInterval(() => {getApiRelatoriodecompras(client.db(dbname))},3*minuto);
//setInterval(() => {getApiclientes(client.db(dbname))},3*minuto);

app.get('/api/producao', (req, res) => {
  client.db(dbname).collection("producao").find({}).sort({numero_op: -1}).toArray( (err, result) => {
    if (err) throw err;
    res.send(result);
  })
});
app.get('/api/tabelapreco', (req, res) => {
  res.send({ express: 'Hello From Express' });
});
app.get('/api/representantes', (req, res) => {
  res.send({ express: 'Hello From Express' });
});
app.get('/api/cobrancas', (req, res) => {
  res.send({ express: 'Hello From Express' });
});
app.get('/api/notascanceladas', (req, res) => {
  res.send({ express: 'Hello From Express' });
});
app.get('/api/emissaonotas', (req, res) => {
  res.send({ express: 'Hello From Express' });
});
app.get('/api/entregadivida', (req, res) => {
  res.send({ express: 'Hello From Express' });
});
app.get('/api/relatoriodecompras', (req, res) => {
  res.send({ express: 'Hello From Express' });
});
app.get('/api/clientes', (req, res) => {
  res.send({ express: 'Hello From Express' });
});
app.get('/api/mensagem', (req, res) => {
  res.send({ express: 'Hello From Express' });
});

app.listen(port, () => console.log(`Listening on port ${port}`));
