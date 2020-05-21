import React from "react";
import {
  Toast,
  Button,
  Modal,
  Table,
  Collapsible,
  CollapsibleItem,
  Checkbox,
  TextInput,
  Icon
} from "react-materialize"
import * as firebase from 'firebase';
import Chart from "react-google-charts";

class TelaLogin extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      usuario: "",
      senha: "",
      response: '',
      firebaseapp: firebase.initializeApp({
        apiKey: 'AIzaSyDGcf4b5BG9NNV__GQbzTdZ7QJAcOeMyRA',
        authDomain: 'https://accounts.google.com/o/oauth2/auth',
        projectId: 'prowater-177d3'
      }),
      logged:false,
      mouseOverStyle: {marginLeft:"10%", borderRadius:"21px",width:"80%", height: 42, backgroundColor:"white"},
      mouseOutStyle: {marginLeft:"10%",width:"80%", height: 32},
      buttonStyle: {},
      currentWindow: "Painel",
      dataTable: {},
      text:"",
      dataCobranca: [],
      dataProducao: [],
    };
    this.handleChangeUser = this.handleChangeUser.bind(this);
    this.handleChangePassword = this.handleChangePassword.bind(this);
  }

  componentDidMount() {
    this.state.firebaseapp.auth().onAuthStateChanged( user => {
      console.log(user);
      if (user){
        this.setState({logged: true});
        this.consulta();
      }
    })
  }

  handleChangeUser (event) {
    this.setState({usuario: event.target.value});
  }

  handleChangePassword (event) {
    this.setState({senha: event.target.value});
  }

  autenticaUsuario = async (usuario, senha, status) => {
    this.state.firebaseapp
      .auth()
      .signInWithEmailAndPassword(usuario,senha)
      .then(
        r => {
          window.M.toast({html:"Sucesso", inDuration:600, outDuration: 600, displayLength: 1600});
          status = true;
        },
        r => {
          window.M.toast({html:"Email ou senha incorretos", inDuration:600, outDuration: 600, displayLength: 1600});
          status = false;
        }
      )
      .catch(function(error) {
        window.M.toast({html:error, inDuration:600, outDuration: 600, displayLength: 1600});
        status = false;
      });
  };

  callApiClientes = async () => {
    const response = await fetch('http://127.0.0.1:5000/cliente');
    const body = await response.json();
    if (response.status !== 200) throw Error(body.message);
    window.M.toast({html:"Clientes", inDuration:600, outDuration: 600, displayLength: 1600});
    const db = this.state.firebaseapp.firestore();
    for ( var cliente in body) {
      db.collection("clientes")
        .add(body[cliente])
        .then(function (docRef) {
          console.log("Document written with ID: ", docRef.id);
        })
        .catch(function (error) {
          console.error("Error adding document: ", error);
        });
    }
  };

  callApiTabelaPreco = async () => {
    const response = await fetch('http://127.0.0.1:5000/tabela_preco');
    const body = await response.json();
    if (response.status !== 200) throw Error(body.message);
    window.M.toast({html:"Tabela", inDuration:600, outDuration: 600, displayLength: 1600});
    const db = this.state.firebaseapp.firestore();
    for ( var produtos in body) {
      console.log(produtos)
      db.collection("tabela_de_preco").add(body[produtos])
        .then(function (docRef) {
          console.log("Document written with ID: ", docRef.id);
        })
        .catch(function (error) {
          console.error("Error adding document: ", error);
        });
    }
  };

  callApiTabelaRepresentantes = async () => {
    const response = await fetch('http://127.0.0.1:5000/representantes');
    const body = await response.json();
    if (response.status !== 200) throw Error(body.message);
    window.M.toast({html:"Tabela", inDuration:600, outDuration: 600, displayLength: 1600});
    const db = this.state.firebaseapp.firestore();
    for ( var representante in body) {
      console.log(representante)
      db.collection("representantes").add(body[representante])
        .then(function (docRef) {
          console.log("Document written with ID: ", docRef.id);
        })
        .catch(function (error) {
          console.error("Error adding document: ", error);
        });
    }
  };

  carregaCobrancas = async () => {
    const response = await fetch('http://127.0.0.1:5000/cobrancas');
    const body = await response.json();
    if (response.status !== 200) throw Error(body.message);
    window.M.toast({html:"Cobrancas", inDuration:600, outDuration: 600, displayLength: 1600});
  };

  addCobrancasFirebase = async (body) => {
    const db = this.state.firebaseapp.firestore();
    for ( var cobranca in body) {
      db.collection("cobrancas")
        .add(body[cobranca])
        .then(function (docRef) {
          console.log("Document written with ID: ", docRef.id);
        })
        .catch(function (error) {
          console.error("Error adding document: ", error);
        });
    }
  };

  updateCobrancasFirebase = async (id, body) => {
    const db = this.state.firebaseapp.firestore();
    await db.collection("cobrancas")
      .where("cliente", "==", id.cliente)
      .where("pedido", "==", id.pedido)
      .where( "nota_fiscal", "==", id.nota_fiscal)
      .where( "empresa", "==", id.empresa)
      .where( "parcela", "==", id.parcela)
      .update(body)
      .then(function (docRef) {
        console.log("Document: ", docRef.id, " updated");
      })
      .catch(function (error) {
        console.error("Error updating document: ", error);
      });
  };

  checaPrazo(prazo){
    let sete = (prazo["seteDias"] ? "7/" : "");
    let quatorze =(prazo["quatorzeDias"] ? "14/" : "");
    let vinteUm = (prazo["vinteUmDias"] ? "21/" : "");
    let vinteOito = (prazo["vinteOitoDias"] ? "28" : "");
    if(prazo.constructor === Object){
      return ( sete + quatorze + vinteUm + vinteOito );
    } else {
      return prazo
    }

  }

  logOut = async () => {
    await this.state.firebaseapp.auth().signOut().then(r => {
      this.setState({logged:false})
    });
  }

  mostraTabelaPedido = () => {
    this.setState({currentWindow: "Pedidos"})
  };

  mostraTabelaCobranca = () => {
    this.setState({currentWindow: "Cobrancas"});
    this.consultaListaDeCobranca();
  };

  mostraTabelaProducao = () => {
    this.setState({currentWindow: "Producao"});
    this.consultaListaDeProducao();
  };

  consulta = async () =>{
    let listaDePedidos = [];
    const db = await this.state.firebaseapp.firestore();
    db.collection("teste").orderBy("data", "desc").get().then((querySnapshot) => {
      querySnapshot.forEach((doc) => {
        listaDePedidos.push({id:doc.id,data:doc.data()});
      });
    });
    this.setState({dataTable: listaDePedidos});
  };

  consultaListaDeCobranca = async () => {
    let listaDeClientes = [];
    const db = await this.state.firebaseapp.firestore();
    await db
      .collection("cobrancas")
      .get()
      .then(querySnapShot => {
        querySnapShot.forEach(doc => {
          listaDeClientes.push({ id: doc.id, data: doc.data() });
        });
        //console.log("Lista Cob", listaDeClientes);
      })
      .catch(error => {
        console.log("Deu ruim", error);
      });
    this.setState({dataCobranca: listaDeClientes}) ;
  };

  insereCodigoPedido = async (id, codigo) => {
    const db = await this.state.firebaseapp.firestore();
    db.collection("teste")
      .doc(id)
      .update({codigoPedido: codigo})
      .then(() => {
        window.M.toast({html:"Sucesso", inDuration:600, outDuration: 600, displayLength: 1600});
       this.consulta();
      }).catch((error) => {
        console.error("Erro ao escrever no documento",error);
    });
  };

  LoginModal(){
    return (
      <Modal
        header="Login"
        id="modal-0"
        open={!this.state.logged}
        options={{dismissible: false, preventScrolling: true}}
        style={{overflow:"hidden"}}
        className="s8 m4 l3"
      >
        <div className="col s6">
          <div className="row">
            <div className="input-field col s12">
              <input id="Email" type="email" className="validate" value={this.state.usuario} onChange={this.handleChangeUser}/>
              <label htmlFor="Email">Email</label>
            </div>
            <div className="input-field col s12">
              <input id="Password" type="text" className="validate" value={this.state.senha} onChange={this.handleChangePassword}/>
              <label htmlFor="Password">Senha</label>
            </div>
            <div className="input-field col s12 m12 l12">
              <Button
                style={{width:"100%"}} type="submit"
                className="waves-effect waves-light btn"
                onClick={() => {
                  let logged = false;
                  this.autenticaUsuario(this.state.usuario, this.state.senha,logged);
                  this.setState({logged: logged}
                  );
                }}
              >
                Login
              </Button>
            </div>
            <div className="input-field col s12">
              <a href="#">Esqueceu a senha?</a>
            </div>
          </div>
        </div>
      </Modal>
    )
  }

  BotaoLateral (label, functionCall) {
     return (
      <Button
        style={styles.botaoLateral}
        className="waves-effect waves-light btn blue"
        onClick={() => {
          functionCall();
        }}
      >
        {label}
      </Button>
    )
  }

  make_row (item){
    return (<tr>{item}</tr>)
  }
  make_row_collapsible (item, collapse){
    return (
      <Collapsible>
        <CollapsibleItem
          header={item}
          node="div"
        >
          {collapse}
        </CollapsibleItem>
      </Collapsible>
    )
  }
  make_col (item){
    return (<td >{item}</td>)
  }
  make_col_title (item){
    return (<th>{item}</th>)
  }
  make_table (head,body){
    return (
      <Table striped={true} hoverable={true} >
        <thead>
          {head}
        </thead>
        <tbody>
          {body}
        </tbody>
      </Table>
    );
  }

  TabelaPedidos (indice, quantidade) {
    let titles = ["Representante","Cliente","Prazo","Entrega","Entrada","Obs"];
    let pedidos = this.state.dataTable;
    let body = [];
    let produtos = [];
    let total = 0.0;
    for(let item in pedidos){
      console.log(pedidos[item].data.codigoPedido === undefined);
      if (pedidos[item].data.codigoPedido === undefined) {
        let temp = [];
        for (let produto of pedidos[item].data.produtos) {
          temp.push(
            this.make_row([
              this.make_col(produto.codigo),
              this.make_col(produto.quantidade),
              this.make_col((produto.total / produto.quantidade).toFixed(2)),
              this.make_col(produto.total),
              this.make_col(<Checkbox checked={produto.bonificacao} disabled={true} filledIn={true}/>),
            ])
          );
          total += !produto.bonificacao ? produto.total : 0;
        }
        produtos.push(temp);
        body.push(
          this.make_row(
            [this.make_col(pedidos[item].data.representante),
              this.make_col(pedidos[item].data.cliente),
              this.make_col(this.checaPrazo(pedidos[item].data.prazo)),
              this.make_col(new Date(pedidos[item].data.dataEntrega).toLocaleDateString("pt-br")),
              this.make_col((pedidos[item].data.data.data + "-" + pedidos[item].data.data.mes + "-" + pedidos[item].data.data.ano)),
              this.make_col(pedidos[item].data.obs),
              <Collapsible>
                <CollapsibleItem
                  header="Produtos"
                  node="div"
                >
                  <Table style={{fontsize: 6}} striped={true} hoverable={true}>
                    <thead>
                    {this.make_row([
                      this.make_col_title("Codigo"),
                      this.make_col_title("Quantidade"),
                      this.make_col_title("Unitario"),
                      this.make_col_title("Total"),
                      this.make_col_title("Bonificacao"),
                    ])}
                    </thead>
                    <tbody>
                    {produtos[item]}
                    {this.make_row(this.make_col_title("Total : R$" + total))}
                    </tbody>
                    <div className="row" style={{width: "150%", flexDirection: "row"}}>
                      <TextInput
                        placeHolder="Codigo"
                        style={{width: "100%"}}
                        onChange={(text) => {
                          this.setState({text: text.target.value});
                          console.log(text.target.value)
                        }}/>
                      <Button
                        style={{marginRight: "4%"}}
                        onClick={() => {
                          this.insereCodigoPedido(pedidos[item].id, this.state.text);
                          console.log(pedidos[item].id)
                        }}
                      >
                        <Icon children="done"/>
                      </Button>
                      <Button><Icon children="delete"/></Button>
                    </div>
                  </Table>
                </CollapsibleItem>
              </Collapsible>
            ]
          )
        );
        total = 0.0;
      }
    }
    let head = [];
    head.push(
      this.make_row([
        this.make_col_title(titles[0]),
        this.make_col_title(titles[1]),
        this.make_col_title(titles[2]),
        this.make_col_title(titles[3]),
        this.make_col_title(titles[4]),
        this.make_col_title(titles[5])
      ])
    );
    return (
      {
        tabela:
          this.make_table(head,body.slice(indice, quantidade)),
        itens: body.length}
        )
  }

  TabelaDeCobranca () {
    let titles = ["Representante", "Empresa", "Cliente", "Pedido", "Nota", "Parcela", "Emissao", "Vencimento", "Valor",
      "Juros", "Dias", "Total"];
    let head = [];
    let body = [];
    let cobrancas = this.state.dataCobranca.sort((a, b) => { return a.data.vencimento - b.data.vencimento });
    const tempo_ms = 1000 * 60 * 60 * 24;
    let hoje = new Date();
    head.push(
      this.make_row([
        this.make_col_title(titles[0]),
        this.make_col_title(titles[1]),
        this.make_col_title(titles[2]),
        this.make_col_title(titles[3]),
        this.make_col_title(titles[4]),
        this.make_col_title(titles[5]),
        this.make_col_title(titles[6]),
        this.make_col_title(titles[7]),
        this.make_col_title(titles[8]),
        this.make_col_title(titles[9]),
        this.make_col_title(titles[10]),
        this.make_col_title(titles[11]),
      ])
    );
    console.log(cobrancas);
    cobrancas.forEach(doc => {
      let data_vencimento;
      try {
        data_vencimento = new Date(doc.data.vencimento.substr(6, 4) +
          "-" +
          doc.data.vencimento.substr(3, 2) +
          "-" +
          doc.data.vencimento.substr(0, 2));
          } catch (e) {
          console.log("erro",e);
          }
          let dias_vencidos = Math.floor((hoje - data_vencimento) / tempo_ms);
      body.push(
        this.make_row([
          this.make_col(doc.data.representante),
          this.make_col(doc.data.empresa),
          this.make_col(doc.data.cliente),
          this.make_col(doc.data.pedido),
          this.make_col(doc.data.nota_fiscal),
          this.make_col(doc.data.parcela),
          this.make_col(doc.data.emissao),
          this.make_col(doc.data.vencimento),
          this.make_col("R$ "+doc.data.valor),
          this.make_col("R$ "+(doc.data.valor*0.004*dias_vencidos).toFixed(2)),
          this.make_col(dias_vencidos),
          this.make_col("R$ "+(doc.data.valor+doc.data.valor*0.004*dias_vencidos).toFixed(2)),
        ]))
    });
    return this.make_table(head,body);
  };

  consultaListaDeProducao = async() => {
    try {
      let response = await fetch(
        'http://127.0.0.1:5001/api/producao'
      );
      let json = await response.json()
      this.setState({dataProducao: json})
    } catch (e) {
      console.error(e)
    }

  }

  TabelaDeProducao () {
    let titles = ["numero_op", "item", "data_emissao", "status", "a_fabricar", "fabricado", "diferenca", "efetuado"]
    let head = [];
    let body = [];
    let producao = this.state.dataProducao

     head.push(
      this.make_row([
        this.make_col_title(titles[0]),
        this.make_col_title(titles[1]),
        this.make_col_title(titles[2]),
        this.make_col_title(titles[3]),
        this.make_col_title(titles[4]),
        this.make_col_title(titles[5]),
        this.make_col_title(titles[6]),
        this.make_col_title(titles[7]),
      ])
    );
    producao.forEach(doc => {
      body.push(this.make_row([
       this.make_col(doc.numero_op),
     this.make_col(doc.item),
     this.make_col(doc.data_emissao),
     this.make_col(doc.status),
     this.make_col(doc.a_fabricar),
     this.make_col(doc.fabricado),
     this.make_col(-1*doc.diferenca),
     this.make_col((100*doc.efetuado).toFixed(2)+"%")
     ]))
    });
     return this.make_table(head,body);
  };

  Painel() {
    return (
      <Chart
        width={"100%"}
        height={'100vh'}
        chartType="LineChart"
        loader={<div>Loading Chart</div>}
        data={[
          ['x', 'dogs'],
          [0, 0],
          [1, 10],
          [2, 23],
          [3, 17],
          [4, 18],
          [5, 9],
          [6, 11],
          [7, 27],
          [8, 33],
          [9, 40],
          [10, 32],
          [11, 35],
        ]}
        options={{
          hAxis: {
            title: 'Time',
          },
          vAxis: {
            title: 'Popularity',
          },
          }}
        rootProps={{ 'data-testid': '1' }}
      />
      )
  }

  render() {
    return (
      <div style={{display:"flex", flexDirection:"row", overflow: "hidden"}}>
        {this.LoginModal()}
        <div className="center-align" style={{width: "200px", height: "100vh", backgroundColor:"blue"}}>
          <div style={{height:62,paddingTop:"10%"}}>
          <a className="white-text" style={{
            marginBottom:"20px"
          }}>
            Prowater
          </a>
          </div>
          <div style={{backgroundColor: "white",height: "1px",width: "80%",paddingLeft: "20px",marginLeft: "20px",marginBottom: "5px"}}/>
          {this.BotaoLateral("Pedidos",this.mostraTabelaPedido)}
          {this.BotaoLateral("Cobrancas", this.mostraTabelaCobranca)}
          {/*this.BotaoLateral("Clientes", this.callApiClientes)*/}
          {this.BotaoLateral("Produção", this.mostraTabelaProducao)}
          {this.BotaoLateral("Sair",this.logOut)}
          </div>
          <div style={{flex:1, overflowY: "scroll"}}>
          {this.state.currentWindow === "Painel" && this.Painel()}
          {this.state.currentWindow === "Pedidos" && this.TabelaPedidos(0, 8).tabela}
          {this.state.currentWindow === "Cobrancas" && this.TabelaDeCobranca()}
          {this.state.currentWindow === "Producao" && this.TabelaDeProducao()}
          </div>
          </div>
    );
  }

}
  const styles = {
    mouseOverStyle: {
      alignment:"center",
      marginLeft:"10%",
      borderRadius:"21px",
      width:"80%",
      height: 42,
      backgroundColor:"white"},
    mouseOutStyle: {
      color:"white",
      marginLeft:"10%",
      width:"80%",
      height: 32},
    botaoLateral: {
      width:"80%",
      borderRadius:"5px",
      paddingLeft:"5%",
      marginBottom:"2%"
    },
  };
  export default TelaLogin;
