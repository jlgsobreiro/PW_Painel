import React from "react";
import {DataGrid} from '@material-ui/data-grid'
import {CircularProgress} from '@material-ui/core';

class TelaCobrancas extends React.Component {
  constructor(props) {
    super(props);
        this.state = {
      dataCobranca: [],
      tabelaCobrancas: {},
          currentWindow: props.currentWindow,
    };
  }

  componentDidMount() {
    this.consultaListaDeCobranca();
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
      return (<div style={{
        display: 'flex',
        height: '100%',
        alignItems: 'center',
        justifyContent: 'center'
      }}><CircularProgress/></div>)
    }
  }

  consultaListaDeCobranca = () => {
    let formatter = new Intl.NumberFormat('pt-BR',{
      style: 'currency',
      currency: 'BRL'
    })
    const colunas = [
      {field:'id',headerName:'id', width: 50, hide: true, type: "number"},
      {field:'Representante',headerName:'Representante', width: 80, hide: false, type: "number"},
      {field:'Empresa',headerName:'Empresa', width: 90, hide: false, type: "string"},
      {field:'Cliente',headerName:'Cliente', width: 80, hide: false, type: "number"},
      {field:'Pedido',headerName:'Pedido', width: 110, hide: false, type: "number"},
      {field:'Nota',headerName:'Nota', width: 110, hide: false, type: "number"},
      {field:'Parcela',headerName:'Parcela', width: 90, hide: false, type: "number"},
      {field:'Emissao',headerName:'Emissao', width: 120, hide: false, type: "dateTime"},
      {field:'Vencimento',headerName:'Vencimento', width: 120, hide: false, type: "dateTime"},
      {field:'Valor',headerName:'Valor', width: 110, hide: false, type: "number"},
      {field:'Juros',headerName:'Juros', width: 110, hide: false, type: "number"},
      {field:'Dias',headerName:'Dias', width: 70, hide: false, type: "number"},
      {field:'Total',headerName:'Total', width: 120, hide: false, type: "number"},
    ];
    let body = [];
    fetch("http://localhost:5001/api/cobrancas")
        .then(res => res.json())
        .then( value => {
          const tempo_ms = 1000 * 60 * 60 * 24;
          let hoje = new Date();
          if (value){
            for(let cob in value) {
              let doc = value[cob] ;
              if (doc !== undefined){
                let data_vencimento,data_emissao;
                try {
                  data_vencimento = new Date(doc.vencimento.replace( /(\d{2})\/(\d{2})\/(\d{4})/, "$2/$1/$3"))
                  data_emissao = new Date(doc.emissao.replace( /(\d{2})\/(\d{2})\/(\d{4})/, "$2/$1/$3"))
                } catch (e) {
                  console.log("erro",e);
                }
                let dias_vencidos = Math.floor((hoje - data_vencimento) / tempo_ms);
                let item = {
                  id: cob,
                  Representante:doc.representante,
                  Empresa: doc.empresa,
                  Cliente: doc.cliente,
                  Pedido: doc.pedido,
                  Nota: doc.nota_fiscal,
                  Parcela: doc.parcela,
                  Emissao: data_emissao.toISOString()
                      .replace( /(\d{4})-(\d{2})-(\d{2})/, "$1/$2/$3")
                      .substring(0,10),
                  Vencimento: data_vencimento.toISOString()
                      .replace( /(\d{4})-(\d{2})-(\d{2})/, "$1/$2/$3")
                      .substring(0,10),
                  Valor: formatter.format(doc.valor),
                  Juros: formatter.format(doc.valor*0.004*dias_vencidos),
                  Dias: dias_vencidos,
                  Total: formatter.format(doc.valor+doc.valor*0.004*dias_vencidos)
                }
                body.push(item);
              }
            }
          }
          this.setState({dataCobranca: {rows:body, col: colunas}});
        }).catch(reason => {
          console.log(reason);
    })
  };

  render() {
    return (
        <>{this.MakeDataGrid(this.state.dataCobranca)}</>
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

export default TelaCobrancas;
