const express = require('express');
const axios = require('axios')
const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');

const urlmongo = 'mongodb://localhost:27017';
const dbname = 'prowater';
const client = new MongoClient(urlmongo);
const app = express();
const port = process.env.PORT || 5001;

client.connect(async (mongoError) =>{
  assert.equal(null,mongoError);
  console.log("Connected to mongodb server");
  const db = client.db(dbname);
  let resultadoRepresentantes = [];
  let resultadoTabelaPreco = [];
  let resultadoClientes = [];
  let resultadoCobrancas = [];
  let resultadoEmissaoNotas = [];
  let resultadoEntregaDivida = [];
  let resultadoNotasCanceladas = [];
  let resultadoProducao = [];
  let resultadoRelatoriodeCompras = [];
  setTimeout(() => {resultadoProducao = getApiProducao()}, 5000);
  setTimeout(() => {resultadoTabelaPreco = getApiTabelaPreco()},5000);
  setTimeout(() => {resultadoRepresentantes =  getApiRepresentantes();},5000);
  setTimeout(() => {resultadoCobrancas = getApicobrancas()},5000);
  setTimeout(() => {resultadoNotasCanceladas = getApiNotasCanceladas()},5000);
  setTimeout(() => {resultadoEmissaoNotas = getApiEmissaoNotas()},5000);
  setTimeout(() => {resultadoEntregaDivida = getApiEntregaDivida()},5000);
  setTimeout(() => {resultadoRelatoriodeCompras = getApiRelatoriodecompras()},5000);
  setTimeout(() => {resultadoClientes = getApiclientes()},5000);
  await db.collection("representantes").insertMany(resultadoRepresentantes).then(value => {
    console.log("OK",value)
  }).catch(reason => {
    console.error("Error REP",reason)
  })
  await db.collection("tabela_preco").insertMany(resultadoTabelaPreco).then(value => {
    console.log("OK",value)
  }).catch(reason => {
    console.error("Error TAB",reason)
  })
  await db.collection("clientes").insertMany(resultadoClientes).then(value => {
    console.log("OK",value)
  }).catch(reason => {
    console.error("Error CLI",reason)
  })
  await db.collection("cobrancas").insertMany(resultadoCobrancas).then(value => {
    console.log("OK",value)
  }).catch(reason => {
    console.error("Error COB",reason)
  })
  await db.collection("producao").insertMany(resultadoProducao).then(value => {
    console.log("OK",value)
  }).catch(reason => {
    console.error("Error PROD",reason)
  })
  await db.collection("notas_canceladas").insertMany(resultadoNotasCanceladas).then(value => {
    console.log("OK",value)
  }).catch(reason => {
    console.error("Error NC",reason)
  })
  await db.collection("entrega_divida").insertMany(resultadoEntregaDivida).then(value => {
    console.log("OK",value)
  }).catch(reason => {
    console.error("Error ENTD",reason)
  })
  await db.collection("emissao_notas").insertMany(resultadoEmissaoNotas).then(value => {
    console.log("OK",value)
  }).catch(reason => {
    console.error("Error EMN",reason)
  })
  await db.collection("relatorio_de_compras").insertMany(resultadoRelatoriodeCompras).then(value => {
    console.log("OK",value)
  }).catch(reason => {
    console.error("Error REL",reason)
  })
  client.close();
});

function getApiRepresentantes() {
  axios.post(' http://127.0.0.1:5000/representantes',
  )
  .then((res) => {
    return res.data
  })
  .catch((error) => {
    console.error(error)
  })
}

function getApiclientes() {
  axios.post(' http://127.0.0.1:5000/cliente',
  )
  .then((res) => {
    return res.data

  })
  .catch((error) => {
    console.error(error)
  })
}

function getApiTabelaPreco() {
  axios.post(' http://127.0.0.1:5000/tabela_preco',
  )
  .then((res) => {
    return res.data

  })
  .catch((error) => {
    console.error(error)
  })
}

function getApicobrancas() {
  axios.post(' http://127.0.0.1:5000/cobrancas',
  )
  .then((res) => {
    return res.data

  })
  .catch((error) => {
    console.error(error)
  })
}

function getApiProducao() {
  axios.post(' http://127.0.0.1:5000/producao',
  )
  .then((res) => {
    return res.data

  })
  .catch((error) => {
    console.error(error)
  })
}

function getApiNotasCanceladas() {
  axios.post(' http://127.0.0.1:5000/notascanceladas',
  )
  .then((res) => {
    return res.data

  })
  .catch((error) => {
    console.error(error)
  })
}

function getApiEntregaDivida() {
  axios.post(' http://127.0.0.1:5000/entregadivida',
  )
  .then((res) => {
    return res.data

  })
  .catch((error) => {
    console.error(error)
  })
}

function getApiEmissaoNotas() {
  axios.post(' http://127.0.0.1:5000/emissaonotas',
  )
  .then((res) => {
    return res.data

  })
  .catch((error) => {
    console.error(error)
  })
}

function getApiRelatoriodecompras() {
  axios.post(' http://127.0.0.1:5000/relatoriodecompras',
  )
  .then((res) => {
    return res.data

  })
  .catch((error) => {
    console.error(error)
  })
}

app.get('/api/mensagem', (req, res) => {

  res.send({ express: 'Hello From Express' });
});

app.listen(port, () => console.log(`Listening on port ${port}`));
