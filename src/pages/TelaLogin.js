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
  state = {
    usuario: "jlgsobreiro@gmail.com",
    senha: "zaion6491",
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
    text:""
  };

  componentDidMount() {
    this.state.firebaseapp.auth().onAuthStateChanged( user => {
      if (user){
        this.setState({logged: true});
        this.consulta();
      }
    })
  }

  autenticaUsuario = async () => {
    this.state.firebaseapp
      .auth()
      .signInWithEmailAndPassword(this.state.usuario,this.state.senha)
      .then(
        r => {
          window.M.toast({html:"Sucesso", inDuration:600, outDuration: 600, displayLength: 1600});
          return true;
        },
        r => {
          window.M.toast({html:"Email ou senha incorretos", inDuration:600, outDuration: 600, displayLength: 1600});
          return false;
        }
      )
      .catch(function(error) {
        window.M.toast({html:error, inDuration:600, outDuration: 600, displayLength: 1600});
        return false;
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

  callApiCobrancas = async () => {
    const response = await fetch('http://127.0.0.1:5000/cobrancas');
    const body = await response.json();
    if (response.status !== 200) throw Error(body.message);
    window.M.toast({html:"Cobrancas", inDuration:600, outDuration: 600, displayLength: 1600});
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

  logOut (){
    this.state.firebaseapp.auth().signOut();
    this.setState({logged:false})
  }

  mostraTabelaPedido = () => {
    this.setState({currentWindow: "Pedidos"})
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
    return listaDePedidos;
  };

  insereCodigoPedido = async (id, codigo) => {
    const db = await this.state.firebaseapp.firestore();
    db.collection("teste")
      .doc(id)
      .update({codigoPedido: codigo})
      .then(() => {
        window.M.toast({html:"Sucesso", inDuration:600, outDuration: 600, displayLength: 1600});
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
              <input id="Email" type="email" className="validate"/>
              <label htmlFor="Email">Email</label>
            </div>
            <div className="input-field col s12">
              <input id="Password" type="text" className="validate"/>
              <label htmlFor="Password">Senha</label>
            </div>
            <div className="input-field col s12 m12 l12">
              <Button
                style={{width:"100%"}} type="submit"
                className="waves-effect waves-light btn"
                onClick={() => {this.setState({logged: this.autenticaUsuario()});
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

  TabelaPedidos () {
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
      <Table striped={true} hoverable={true} >
        <thead>
          {head}
        </thead>
        <tbody>
          {body}
        </tbody>
      </Table>
    )
  }

  TabelaPedidosNovo () {
    let titles = ["Representante","Cliente","Prazo","Entrega","Entrada","Obs"];
    let pedidos = this.state.dataTable;

    let body = [];
    let produtos = [];
    let total = 0.0;
    for(let item in pedidos){
      let temp = [];
        for(let produto of pedidos[item].data.produtos){
          temp.push(
            this.make_row([
              this.make_col(produto.codigo),
              this.make_col(produto.quantidade),
              this.make_col((produto.total/produto.quantidade).toFixed(2)),
              this.make_col(produto.total),
              this.make_col(<Checkbox checked={produto.bonificacao} disabled={true} filledIn={true}/>),
            ])
          );
          total += !produto.bonificacao ? produto.total : 0;
        }
        produtos.push(temp);
      body.push(
        this.make_row_collapsible(
          [this.make_col(pedidos[item].data.representante),
          this.make_col(pedidos[item].data.cliente),
          this.make_col(this.checaPrazo(pedidos[item].data.prazo)),
          this.make_col(new Date(pedidos[item].data.dataEntrega).toLocaleDateString("pt-br")),
          this.make_col((pedidos[item].data.data.data+"-"+pedidos[item].data.data.mes+"-"+pedidos[item].data.data.ano)),
          this.make_col(pedidos[item].data.obs),
          ],
          <Table style={{fontsize:6}} striped={true} hoverable={true}>
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
            {this.make_row(this.make_col_title("Total : R$"+total))}
            </tbody>
          </Table>
        )
      );
      total = 0.0;
    }
    let head = [];
    head.push(
      <div style={{width:"100%"}}>
        <div style={{width:"10%"}}>{titles[0]}</div>
        <div style={{width:"10%"}}>{titles[1]}</div>
        <div style={{width:"10%"}}>{titles[2]}</div>
        <div style={{width:"10%"}}>{titles[3]}</div>
        <div style={{width:"10%"}}>{titles[4]}</div>
        <div style={{width:"50%"}}>{titles[5]}</div>
      </div>
    );
    return (
      <div className="row">
        <Collapsible>
          <CollapsibleItem
            header={head}
            node="div"
          >
            {body}
          </CollapsibleItem>
        </Collapsible>
      </div>
    )
  }

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
      <div style={{display:"flex", flexDirection:"row"}}>
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
          {this.BotaoLateral("Sair",this.logOut)}
        </div>
        {this.state.currentWindow === "Painel" && this.Painel()}
        {this.state.currentWindow === "Pedidos" && this.TabelaPedidos(this.state.dataTable)}
      </div>
    );
  }
}
/*<div
  style={this.state.buttonStyle}
  id="teste"
  onMouseOver={() => this.setState({buttonStyle: styles.mouseOverStyle})}
  onMouseOut={() => this.setState({buttonStyle: styles.mouseOutStyle})}
> oin</div>*/
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
