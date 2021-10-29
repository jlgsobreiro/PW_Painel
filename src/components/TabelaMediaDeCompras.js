import React from "react";
import {DataGrid} from '@material-ui/data-grid'
import {Button, CircularProgress, Card, CardContent, Typography, CardActions} from '@material-ui/core';

class TelaMediaDeCompras extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      dataPedidosAbertos: [],
      dataPedidosCadastrados: [],
      dataNotasFaturadas: [],
      dataMediaCompras: {},
      clienteSelecionado: "",
      nomeCliente: "",
    };
    this.handleCliente = this.handleCliente.bind(this);
  }

  componentDidMount() {
    this.consultaNotasFaturadas();
    //this.consultaPedidosAbertos();
    this.consultaPedidosCadastrados();
  }

  handleCliente (event) {
    if (this.state.nomeCliente !== ""){
      this.setState({nomeCliente:""});
    }
    this.setState({clienteSelecionado: event.target.value});
  }

  consultaPedidosCadastrados = () =>{
     fetch("http://localhost:5001/api/pedidoscadastrados")
        .then(res => res.json())
        .then( value => {
          this.setState({dataPedidosCadastrados: value})
        } ).catch(reason => {
          console.log(reason);
    })
  }

  consultaPedidosAbertos = () =>{
     fetch("http://localhost:5001/api/pedidosabertos")
        .then(res => res.json())
        .then( value => {
          this.setState({dataPedidosAbertos: value})
        } ).catch(reason => {
          console.log(reason);
    })
  }

  consultaNotasFaturadas = () =>{
     fetch("http://localhost:5001/api/notasfaturadas")
        .then(res => res.json())
        .then( value => {
          this.setState({dataNotasFaturadas: value})
        } ).catch(reason => {
          console.log(reason);
    })
  }

  MakeDataGrid = (dataPlanilha) => {
    console.log(dataPlanilha);
    try {
     return (
         <DataGrid
             columns={dataPlanilha.col}
             rows={dataPlanilha.rows}
             pageSize={18}
             rowHeight={25}
             rowsPerPageOptions={[dataPlanilha.rows.length]}
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

  consultaMediaCompras = () => {
    let formatter = new Intl.NumberFormat('pt-BR',{
      style: 'currency',
      currency: 'BRL'
    })
    const colunas = [
      {field:'id',headerName:'id', width: 50, hide: true, type: "number"},
      {field:'cod',headerName:'Codigo', width: 80, hide: false, type: "string"},
      {field:'descr',headerName:'Descrição', width: 400, hide: false, type: "string"},
      {field:'qtdmed',headerName:'QTD Med', width: 90, hide: false, type: "number"},
      {field:'vlunmed',headerName:'Valor UN', width: 90, hide: false, type: "number"},
      {field:'vltotmed',headerName:'Valor Med Total', width: 100, hide: false, type: "number"},
      {field:'ultqtdfat',headerName:'QTD Ultimo FAT', width: 100, hide: false, type: "number"},
      {field:'ultunfat',headerName:'Valor UN Ultimo FAT', width: 120, hide: false, type: "number"},
      {field:'ultdtfat',headerName:'Data FAT', width: 120, hide: false, type: "dateTime"},
    ];
    let body = [];
    let produtos =[
        {cod:"011001",descr:"CLORO PROWATER TRAD    CX C/ 08 X 02 l"},
        {cod:"011005",descr:"CLORO PROWATER TRAD    CX C/ 04 X 05 l"},
        {cod:"011009",descr:"CLORO PROWATER TRAD    CX C/ 12 X 01 l"},
        {cod:"012003",descr:"CLORO PROWATER BRAN    CX C/ 08 X 02 l"},
        {cod:"012010",descr:"CLORO PROWATER BRAN    CX C/ 12 X 01 l"},
        {cod:"021002",descr:"AG SANIT PROWATER TRAD CX C/ 12 X 01 l"},
        {cod:"021006",descr:"AG SANIT PROWATER TRAD CX C/ 08 X 02 l"},
        {cod:"021007",descr:"AG SANIT PROWATER TRAD CX C/ 04 X 05 l"},
        {cod:"022004",descr:"AG SANIT PROWATER BRAN CX C/ 12 X 01 l"},
        {cod:"022008",descr:"AG SANIT PROWATER BRAN CX C/ 08 X 02 l"},
        {cod:"031011",descr:"ESPONJA PROWATER MULTIUSO un"},
        {cod:"031014",descr:"ESPONJA PROWATER MULTIUSO 03 un"},
        {cod:"031013",descr:"ESPONJA PROWATER MULTIUSO  CX C/ 144X04 un"},
        {cod:"041017",descr:"LIMPADOR PROWATER SENSUALITE CX C/ 12 X 500ML"},
        {cod:"043018",descr:"LIMPADOR PROWATER LAMOUR CX C/ 12 X 500ML"},
        {cod:"042020",descr:"LIMPADOR PROWATER AFECTION CX C/ 12 X 500ML"},
        {cod:"051021",descr:"SODA CAUSTICA EM ESCAMA PROWATER CX C 12 X 400G"},
        {cod:"051022",descr:"SODA CAUSTICA EM ESCAMA PROWATER CX C 06 X 1KG"},
    ]
    for (let produto in produtos){
      let vlr = 0.0;
      let qtd = 0.0;
      let pedidosCadastrados = [];
      let faturados = [];
      //filtro pedidos cadastrados não bonificados
      pedidosCadastrados = this.state.dataPedidosCadastrados.filter((value => {
        return value.tipo === "NF" &&
            value.cliente.trim() === this.state.clienteSelecionado &&
            value.produto.trim() === produtos[produto].cod;
      }))
      //filtro notas faturadas
      faturados = this.state.dataNotasFaturadas.filter((value => {
        return value.cliente.trim() === this.state.clienteSelecionado &&
            value.produto.trim() === produtos[produto].cod;
      })).sort((a,b) => {return b.data_faturamento - a.data_faturamento})
      //Quantidade media de compras do produto
      let qtdmed = 0.0;
      for (let pedidos in pedidosCadastrados){
        qtd += pedidosCadastrados[pedidos].quantidade;
        vlr += pedidosCadastrados[pedidos].valor_total;
      }
      qtdmed = pedidosCadastrados.length>0 ? Math.round(qtd/pedidosCadastrados.length) : 0;
      //Valor medio de compras do produto
      let vlunmed = 0.0
      vlunmed = pedidosCadastrados.length>0 ?  formatter.format(vlr/qtd) : 0;
      //Valor total da media de compras do produto
      let vltotmed = 0.0;
      vltotmed = formatter.format(qtdmed*(vlr/qtd));
      //Ultima quantidade faturada do produto
      let ultqtdfat = 0
      ultqtdfat = faturados.length>0 ? faturados[0].quantidade : 0;
      //Ultimo valor unitario faturado do produto
      let ultunfat = 0
      ultunfat = faturados.length>0 ? formatter.format(faturados[0].valor_unitario) : 0;

      //Ultima data de faturamento do produto
      let ultdtfat = 0
      ultdtfat = faturados.length>0 ? faturados[0].data_faturamento : 0;
      let item = {
      id: produto,
      cod: produtos[produto].cod,
      descr: produtos[produto].descr,
      qtdmed: qtdmed,
      vlunmed: vlunmed,
      vltotmed: vltotmed,
      ultqtdfat: ultqtdfat,
      ultunfat: ultunfat,
      ultdtfat: new Date(ultdtfat).toISOString()
          .replace( /(\d{4})-(\d{2})-(\d{2})/, "$1/$2/$3")
          .substring(0,10)
      }
      body.push(item);
      if (this.state.nomeCliente === "" && faturados.length > 0){
        this.setState({nomeCliente:faturados[0].fantasia});
      }
    }
    this.setState({dataMediaCompras: {rows:body, col: colunas}});
  };

  render() {
    return (
      <>
        <div id={"headerMC"} style={{flex:1, flexDirection: 'row'}}>
          <label style={{width:'150px', paddingRight:'30px', paddingLeft:'30px', fontSize:'large'}}>Cliente:</label>
          <input type={"text"} placeholder={"teste"} style={{width:'100px'}}
                 value={this.state.clienteSelecionado}
                 onChange={this.handleCliente}/>
          <label style={{width:'150px', fontSize:'large'}}>{this.state.nomeCliente}</label>
          <div class="card" style={{alignItems:"center",paddingLeft:"5px", width:"60px", height:"60px", display:'flex', flexDirection:"column"}}>
            <label style={{justifyContent:'center'}}>Tempo</label>
            <div style={{justifyContent:"center"}}>
              <label style={{justifyContent:'center', fontSize: 'large'}}>40</label>
            </div>
          </div>
          <Button variant='contained' color='primary' onClick={()=>{this.consultaMediaCompras();}}>
            pesquisar
          </Button>
        </div>
        <div id={"bodyMC"} style={{height: "100%",flex:1}}>
          <div id={"datagtidMC"} style={{height: "100%"}}>
            {this.MakeDataGrid(this.state.dataMediaCompras)}
          </div>
        </div>
      </>
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

export default TelaMediaDeCompras;
