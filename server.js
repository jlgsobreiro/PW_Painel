const express = require('express');
const axios = require('axios')
const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');
var schedule = require('node-schedule');

const urlmongo = 'mongodb://localhost:27017';
const dbname = 'prowater';
const client = new MongoClient(urlmongo);
const app = express();

app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  next();
});
const port = process.env.PORT || 5001;
const minuto = 1000*60;

function getApiRepresentantes(db) {
  axios.post(' http://127.0.0.1:5000/representantes',
  )
  .then((res) => {
    res.data.forEach(value => {
      db.collection("representantes").update({codigo: value.codigo}, {$set: value}).then(value => {
        //console.log("OK",value)
      }).catch(reason => {
        console.error("Error REP",reason)
      })
    })
  })
  .catch((error) => {
    console.error(error)
  })
}

function getApiclientes(db) {
  axios.post(' http://127.0.0.1:5000/cliente',
  )
  .then((res) => {
    res.data.forEach(value => {
      db.collection("clientes").update({codigo: value.codigo}, {$set: value}).then(value => {
        //console.log("OK",value)
      }).catch(reason => {
        console.error("Error CLI",reason)
      })
    })

  })
  .catch((error) => {
    console.error(error)
  })
}

function getApiTabelaPreco(db) {
  axios.post(' http://127.0.0.1:5000/tabela_preco',
  )
  .then((res) => {
    res.data.forEach(value => {
      db.collection("tabela_preco")
        .update({codigo: value.codigo, empresa: value.empresa, tabela: value.tabela}, {$set: value})
        .then(value => {
        //console.log("OK",value)
      }).catch(reason => {
        console.error("Error TAB",reason)
      })
    })
  })
  .catch((error) => {
    console.error(error)
  })
}

function getApicobrancas(db) {
  axios.post(' http://127.0.0.1:5000/cobrancas',
  )
  .then((res) => {
    res.data.forEach(value => {
      db.collection("cobrancas")
        .update({cliente: value.cliente, empresa: value.empresa, nota_fiscal: value.nota_fiscal},{$set: value},{upsert: true})
        .then(value => {
        //console.log("OK",value)
      }).catch(reason => {
        console.error("Error COB",reason)
      })
    })
  })
  .catch((error) => {
    console.error(error)
  })
}

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

function getApiEntregaDivida(db) {
  axios.post(' http://127.0.0.1:5000/entregadivida',
  )
  .then((res) => {
    res.data.forEach(value => {
      db.collection("entrega_divida")
        .update({cliente: value.cliente,empresa: value.empresa, pedido: value.pedido},{$set: value},{upsert: true})
        .then(value => {
        //console.log("OK",value)
      }).catch(reason => {
        console.error("Error ENTD",reason)
      })
    })
  })
  .catch((error) => {
    console.error(error)
  })
}

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

client.connect(async (mongoError) =>{
  assert.equal(null,mongoError);
  console.log("Connected to mongodb server");
  const db = client.db(dbname);
  setTimeout(() => {getApiProducao(db)}, 5000);
  setTimeout(() => {getApiTabelaPreco(db)},5000);
  setTimeout(() => {getApiRepresentantes(db);},5000);
  setTimeout(() => {getApicobrancas(db)},5000);
  setTimeout(() => {getApiNotasCanceladas(db)},5000);
  setTimeout(() => {getApiEmissaoNotas(db)},5000);
  setTimeout(() => {getApiEntregaDivida(db)},5000);
  setTimeout(() => {getApiRelatoriodecompras(db)},5000);
  setTimeout(() => {getApiclientes(db)},5000);
  //await client.close();
});

setInterval(() => {getApiProducao(client.db(dbname))}, 10*minuto);
setInterval(() => {getApiTabelaPreco(client.db(dbname))},10*minuto);
setInterval(() => {getApiRepresentantes(client.db(dbname));},10*minuto);
setInterval(() => {getApicobrancas(client.db(dbname))},10*minuto);
setInterval(() => {getApiNotasCanceladas(client.db(dbname))},10*minuto);
setInterval(() => {getApiEmissaoNotas(client.db(dbname))},10*minuto);
setInterval(() => {getApiEntregaDivida(client.db(dbname))},10*minuto);
setInterval(() => {getApiRelatoriodecompras(client.db(dbname))},10*minuto);
setInterval(() => {getApiclientes(client.db(dbname))},10*minuto);

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
