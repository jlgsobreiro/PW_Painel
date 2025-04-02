import * as dyn from '../dynamodb';
import React, {useState} from "react";
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
import {DataGrid} from '@material-ui/data-grid'
import * as firebase from 'firebase';
import Chart from "react-google-charts";
import Amplify, { Auth } from 'aws-amplify';
import awsconfig from '../aws-exports';
import {CircularProgress} from '@material-ui/core';
import TabelaCobrancas from '../components/TabelaCobrancas';
import TelaMediaDeCompras from '../components/TabelaMediaDeCompras';
import TabelaMediaDeCompras from '../components/TabelaMediaDeCompras';

Amplify.configure(awsconfig);

class TelaLogin extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      usuario: "",
      senha: "",
      response: "",
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
      nomesTabelasDynamo: [],
      tabelaCobrancas: {},
    };
    this.handleChangeUser = this.handleChangeUser.bind(this);
    this.handleChangePassword = this.handleChangePassword.bind(this);
  }

  componentDidMount() {
    this.consultaTabelasDynamoDB();
  }

  handleChangeUser (event) {
    this.setState({usuario: event.target.value});
  }

  handleChangePassword (event) {
    this.setState({senha: event.target.value});
  }

  autenticaUsuario = (usuario, senha) => {
    Auth.signIn({username: usuario, password: senha})
        .then(value => {
          window.M.toast({html:"Sucesso", inDuration:600, outDuration: 600, displayLength: 1600});
          this.setState({logged: true});
        })
        .catch(reason => {
          //console.error(reason);
          window.M.toast({html:"Email ou senha incorretos", inDuration:600, outDuration: 600, displayLength: 1600});
          this.setState({logged: false});
          return false;
        })
  }

  logOut = () => {
    Auth.signOut()
        .then(value => {
          this.setState({logged:false})
          window.M.toast({html:"Até breve", inDuration:600, outDuration: 600, displayLength: 1600});
        })
        .catch(reason => {
          window.M.toast({html:"Erro ao sair", inDuration:600, outDuration: 600, displayLength: 1600});
        })
  }

  consultaTabelasDynamoDB = () => {
      dyn.listaTabelas2().then(value => {
          console.log(value);
          console.log(value.TableNames);
          this.setState({nomesTabelasDynamo: value.TableNames});
      }).catch(reason => {
          console.error(reason);
      })

  }

  consultaListaDeProducao = () => {
    let formatter = new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    })
    const titles = [
      {cabecalho: 'id', tamanho: 50, hide: true, tipo: "number"},
      {cabecalho: 'Numero_OP', tamanho: 150, hide: false, tipo: "number"},
      {cabecalho: 'Item', tamanho: 400, hide: false, tipo: "string"},
      {cabecalho: 'Estimado', tamanho: 120, hide: false, tipo: "number"},
      {cabecalho: 'Emissao', tamanho: 120, hide: false, tipo: "datetime"},
      {cabecalho: 'Estado', tamanho: 120, hide: false, tipo: "string"},
      {cabecalho: 'Diferenca', tamanho: 120, hide: false, tipo: "number"},
      {cabecalho: 'Efetuado', tamanho: 120, hide: false, tipo: "number"},
      {cabecalho: 'Input', tamanho: 120, hide: false, tipo: "number"},
    ];
    let colunas = [];
    let body = [];
    for (let titulo in titles) {
      colunas.push({
        field: titles[titulo].cabecalho,
        headerName: titles[titulo].cabecalho,
        width: titles[titulo].tamanho,
        hide: titles[titulo].hide
      });
      fetch('http://127.0.0.1:5001/api/producao')
          .then(res => res.json())
          .then(value => {
            if (value) {
              for (let cob in value) {
                let doc = value[cob];
                if (doc !== undefined) {
                  let data_emissao = new Date(doc.data_emissao.replace(/(\d{2})\/(\d{2})\/(\d{4})/, "$2/$1/$3"))
                  let item = {
                    id: cob,
                    Numero_OP: doc.numero_op,
                    Estimado: doc.a_fabricar,
                    Emissao: data_emissao.toISOString()
                        .replace(/(\d{4})-(\d{2})-(\d{2})/, "$1/$2/$3")
                        .substring(0, 10),
                    Diferenca: doc.diferenca,
                    Efetuado: doc.efetuado,
                    Fabricado: doc.fabricado,
                    Item: doc.item,
                    Estado: doc.status
                  }
                  body.push(item);
                  //console.log(item);
                }
              }
            }
            this.setState({dataProducao: {rows: body, col: colunas}})
            this.setState({currentWindow: "Producao"});
          })
          .catch(reason => {
            console.error(reason)
          })
    }
  }

  consultaTabelaDeProdutos = () => {
    let formatter = new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    })
    const titles = [
      {cabecalho: 'id', tamanho: 50, hide: true, tipo: "number"},
      {cabecalho: 'Empresa', tamanho: 150, hide: false, tipo: "number"},
      {cabecalho: 'Codigo', tamanho: 400, hide: false, tipo: "string"},
      {cabecalho: 'Descricao', tamanho: 120, hide: false, tipo: "number"},
      {cabecalho: 'Data_Inicial', tamanho: 120, hide: false, tipo: "datetime"},
      {cabecalho: 'Data_Final', tamanho: 120, hide: false, tipo: "string"},
      {cabecalho: 'Valor', tamanho: 120, hide: false, tipo: "number"},
    ];
    let colunas = [];
    let body = [];
    for (let titulo in titles) {
      colunas.push({
        field: titles[titulo].cabecalho,
        headerName: titles[titulo].cabecalho,
        width: titles[titulo].tamanho,
        hide: titles[titulo].hide
      });
      fetch('http://127.0.0.1:5001/api/producao')
          .then(res => res.json())
          .then(value => {
            if (value) {
              for (let cob in value) {
                let doc = value[cob];
                if (doc !== undefined) {
                  let data_inicial = new Date(doc.data_inicial.replace(/(\d{2})\/(\d{2})\/(\d{4})/, "$2/$1/$3"))
                  let data_final = new Date(doc.data_inicial.replace(/(\d{2})\/(\d{2})\/(\d{4})/, "$2/$1/$3"))
                  let item = {
                    id: cob,
                    Empresa: doc.empresa,
                    Codigo: doc.codigo,
                    Descricao: doc.descricao,
                    Data_inicial: doc.data_inicial.toISOString()
                        .replace(/(\d{4})-(\d{2})-(\d{2})/, "$1/$2/$3")
                        .substring(0, 10),
                    Data_final: doc.data_final,
                    Valor: doc.efetuado,
                    Fabricado: doc.fabricado,
                    Item: doc.item,
                    Estado: doc.status
                  }
                  body.push(item);
                  //console.log(item);
                }
              }
            }
            this.setState({dataProducao: {rows: body, col: colunas}})
            this.setState({currentWindow: "Producao"});
          })
          .catch(reason => {
            console.error(reason)
          })
    }
  }

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

  mostraTabelaPedido = () => {
    this.setState({currentWindow: "Pedidos"})
  };

  mostraTabelaCobranca = () => {
    //this.setState({currentWindow: "Loading"});
    this.setState({currentWindow: "Cobrancas"});
    //this.consultaListaDeCobranca();
    //console.log(this.state.dataCobranca);
  };

  mostraTabelaProducao = () => {
    this.setState({currentWindow: "Loading"});
    this.consultaListaDeProducao();
  };

  mostraTabelaMediaDeCompras = () => {
    this.setState({currentWindow: "MediaDeCompras"});
  };

  mostraDynamoDB = () => {
      this.setState({currentWindow: "DynamoDB"});
  }

  insereCodigoPedido = async (id, codigo) => {
    const db = await this.state.firebaseapp.firestore();
    db.collection("teste")
      .doc(id)
      .update({codigoPedido: codigo})
      .then(() => {
        window.M.toast({html:"Sucesso", inDuration:600, outDuration: 600, displayLength: 1600});
       //this.consulta();
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
                  this.autenticaUsuario(this.state.usuario, this.state.senha);
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

  BotaoLateralv2 (props) {
     return (
      <Button
        style={styles.botaoLateral}
        className="waves-effect waves-light btn blue"
        onClick={() => {
          this.setState({currentWindow: props.tela})
        }}
      >
        {props.label}
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
  MakeDataGrid = (dataPlanilha) => {
    console.log(dataPlanilha);
    try {
     return (
         <DataGrid
             columns={dataPlanilha.col}
             rows={dataPlanilha.rows}
             pageSize={10}
             rowsPerPageOptions={[10, 25, 50,dataPlanilha.rows.length]}
         />)
    } catch (e) {
      console.log("Erro"+e);
      return (<DataGrid columns={["Carregando"]} rows={["Carregando"]} pageSize={25}  />)
    }
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

  DynamoDBPainel() {
      return (
          <h1>{this.state.nomesTabelasDynamo}</h1>
      );
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
          {/*this.BotaoLateralv2({tela:"Pedidos",label:"Pedidos"})*/}
          {this.BotaoLateral("Pedidos",this.mostraTabelaPedido)}
          {this.BotaoLateral("Cobrancas", this.mostraTabelaCobranca)}
          {/*this.BotaoLateral("Clientes", this.callApiClientes)*/}
          {this.BotaoLateral("Produção", this.mostraTabelaProducao)}
          {this.BotaoLateral("Média Compras", this.mostraTabelaMediaDeCompras)}
          {this.BotaoLateral("Sair",this.logOut)}
          </div>
          <div style={{flex:1}}>
          {this.state.currentWindow === "Loading" && (<CircularProgress/>)}
          {this.state.currentWindow === "Painel" && this.Painel()}
          {this.state.currentWindow === "Pedidos" && this.TabelaPedidos(0, 8).tabela}
          {this.state.currentWindow === "Cobrancas" && (<TabelaCobrancas/>)}
          {this.state.currentWindow === "Producao" && this.MakeDataGrid(this.state.dataProducao)}
          {this.state.currentWindow === "DynamoDB" && this.DynamoDBPainel()}
          {this.state.currentWindow === "MediaDeCompras" && <TabelaMediaDeCompras/>}
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

