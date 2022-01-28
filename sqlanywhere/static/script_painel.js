/*jshint esversion: 6 */
/*globals $:false */
$(document).ready(function(){
  "use strict";
  $('#modal').modal();
  $('#modal1').modal();
  $('#modal_enviando').modal({dismissible: false, startingTop: '30%', endingTop: '30%'});
  $('.collapsible').collapsible();
  $('.representante').mask('00000');
  $('.cliente').mask('00000');
  $('.valor').mask('###.##',{reverse: true});
  $('.qtd').mask('000000');
  $('.materialboxed').materialbox();
  M.Datepicker.init($('.datepicker'), {format: 'dd/mm/yyyy',    disableWeekends: true, minDate: new Date(Date.now()),
    i18n:({
      months: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
      monthsShort: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
      weekdays: ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sabádo'],
      weekdaysShort: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab'],
      weekdaysAbbrev: ['D','S','T','Q','Q','S','S'],
      today: 'Hoje',
      done: 'Ok',
      clear: 'Limpar',
      previousMonth:'<',
      nextMonth:'>',
      selectMonths: true,
      selectYears: 15
    })});
  $("#cliente_nome").autocomplete({
    data: {},
    onAutocomplete: (function (selecionado) {
      $("#cliente").val(parseInt(lista_auto[selecionado])).change();
      $("#cliente_label").addClass("active");
    })
  });
});
let items;
let total_ped;
let desconto_ped;
let desconto_max;
let lista_auto;
let stopper_clientes = 0;
let stopper_historico = 0;
let ultimo_cliete = '';
function onload_tabela(produtos){
  "use strict";
  items = produtos;
}

 function handler(componente,id){
  "use strict";
  let quantidade = $("#quantidade-"+id);
  let unidade = $("#unidade-"+id);
  let qtd = parseFloat(quantidade.val());
  let un = parseFloat(unidade.val()).toFixed(2);
  items[id - 1].quantidade = qtd;
  items[id - 1].pedido = un;
  total_pedido();
  if (parseFloat(desconto_ped) < desconto_max){
    //unidade.val(items[id-1].valor);
    qtd = parseFloat(quantidade.val());
    un = parseFloat(unidade.val()).toFixed(2);
    items[id - 1].quantidade = qtd;
    items[id - 1].pedido = un;
    total_pedido();
    M.toast({html:"Desconto máximo excedido"});
    $('#modal').addClass("disabled");
  }
  $("#total-"+id).text((qtd*un).toFixed(2));
  const desc_calc = (1-((qtd*un)/(qtd*items[id-1].valor)))*100;
  let desc = isNaN( desc_calc) ? 0 : desc_calc;
  $("#desconto-"+id).text("%"+(desc).toFixed(2));
 }

function descontoCaixas (caixas) {
  "use strict";
  if (caixas <= 40){
    return 1.0;
  } else if (caixas <= 60){
    return 0.95;
  } else if (caixas <= 80){
    return 0.935;
  } else if (caixas <= 100){
    return 0.92;
  } else if (caixas <= 200){
    return 0.9;
  } else if (caixas <= 400){
    return 0.88;
  } else if (caixas > 400){
    return 0.85;
  } else {
    return 1;
  }
}

 function total_pedido() {
  "use strict";
  let x=0.0;
   let tot_qtd = 0;
   let tot_tabela = 0.0;
   let tot_tabela_cli = 0.0;
   for (let i = 0; i< items.length;i++){
     let qtd = items[i].quantidade !== undefined ? parseInt(items[i].quantidade) : 0;
     let vl_pedido = items[i].pedido !== undefined ? parseFloat(items[i].pedido) : 0;
     tot_qtd += qtd;
     tot_tabela_cli += qtd*items[i].tabela;
     tot_tabela += qtd*items[i].valor;
     x += qtd * vl_pedido;
   }
   desconto_ped = parseFloat(x/tot_tabela_cli);
   let desconto_ped_real = parseFloat(x/tot_tabela);
   total_ped = x.toFixed(2);
   desconto_max = parseFloat(descontoCaixas(tot_qtd));
   let desconto_final = isNaN((1-desconto_ped_real)*100) ? 0 : (1-desconto_ped_real)*100;
   if (descontoCaixas(tot_qtd) <= desconto_ped){
     $("#total_final").text(total_ped);
     $("#desconto_final").text("% "+ desconto_final.toFixed(2));
     habilita_resumo();
   } else {
     $('#modal').addClass("disabled");
     $("#total_final").text("Desconto Maximo excedido");
     $("#desconto_final").text("% "+ desconto_final.toFixed(2));
   }
 }

 function habilita_resumo(){
  "use strict";
  let repre = $("#representante");
  let cli = $("#cliente");
  let cli_nome = $("#cliente_nome");
  if (repre.val() !== ''){
    cli.prop("disabled",false);
    cli_nome.prop("disabled",false);
  } else {
    cli.prop("disabled",true);
    cli_nome.prop("disabled",true);
  }
  if (repre.val() !== '' && cli.val() !== '') {
    $('#modal').removeClass("disabled");
  }
 }

 function limpa_cliente(){
  "use strict";
  let cli = $("#cliente");
  let cli_nome = $("#cliente_nome");
  cli.val('');
  cli_nome.val('');
 }

function handler_cliente() {
  "use strict";
  let repre = $("#representante").val();
  let cnpj_cpf = $("#cnpj_cpf");
  let cli = $("#cliente");
  let cli_nome = $("#cliente_nome");
  let repre_nome = $("#representante_nome");
  var instance = M.Autocomplete.getInstance(cli_nome);
  if (ultimo_cliete === cli.val()){
    stopper_clientes += 1;
    stopper_historico += 1;
  } else {
    stopper_clientes = 0;
    stopper_historico = 0;
  }
  if (repre !== '' && stopper_clientes<2){
    $.post("/clientes",{representante:repre},function (data) {
      let lista = {};
      lista_auto = {};
      for (let i = 0; i < data.length; i++){
        let chave = "" + data[i].fantasia;
        lista[chave] = null;
        lista_auto[chave] = data[i].cliente;
      }
      instance.updateData(lista);
    });
    cli.prop("disabled",false);
    cli_nome.prop("disabled",false);
    cnpj_cpf.prop("disabled",false);
  }
  if (repre !== '' && (cli.val() !== '' || cnpj_cpf.val() !== '') && stopper_clientes < 2) {
    $("#texto_enviando").text("Carregando Informações do cliente");
    M.Modal.getInstance($("#modal_enviando")).open();
    $.post("/historico_cliente", {cliente: cli.val(), representante: repre, cnpj_cpf: cnpj_cpf.val()}, function (data) {
      repre_nome.html(data.representante_nome);
      cli_nome.val(data.fantasia);
      $('#cliente_nome_label').addClass('active');
      if (cli.val() === ''){
        cli.val(data.cliente);
        $('#cliente_label').addClass('active');
      }
      if (cnpj_cpf.val() === ''){
        cnpj_cpf.val(data.cnpj_cpf);
        $('#cnpj_cpf_label').addClass('active');
      }
      repre_nome.removeClass("hide");
      $("#cliente_nome_label").addClass("active");
      handle_cobrancas(data.cobrancas);
      handle_historico(data.historico);
      handle_tabela(data.tabela);
      habilita_resumo();
    }).done(function () {
      M.Modal.getInstance($("#modal_enviando")).close();
    }).fail(function () {
      M.Modal.getInstance($("#modal_enviando")).close();
      M.toast({html: "Erro ao consultar cliente"});
    });
  }
 }

 function handle_tabela(tabela) {
  "use strict";
  for (let i = 0; i < items.length; i++) {
    let achado;
    if (tabela){
     let achado = tabela.find(elem => elem.ITEM === items[i].codigo);
    }
    if (achado !== undefined){
      items[i].tabela = achado.VALOR;
    } else {
      items[i].tabela = items[i].valor;
    }
  }
 }

 function handle_historico(historico) {
  "use strict";
  var comprados = [];
  var historico_tam = historico.length;
  for (let nota = 0; nota< historico.length; nota++){
    var notas = historico[nota];
    if (notas.bonificacao === true){
      historico_tam--;
      continue;
    }
    for (let prod = 0; prod< notas.produtos.length; prod++) {
      var produto = notas.produtos[prod];
      var x = comprados.find((item) => {
        if (item.codigo === produto.produto) {
          return item;
        }
      });
      if (x === undefined){
        comprados.push({codigo:produto.produto, quantidade: produto.quantidade});
      } else {
        x.quantidade += produto.quantidade;
      }
    }
  }
  comprados.sort((a,b) => {
    if (a.codigo>b.codigo) {
      return 1;
    } else {
      return -1;
    }
  });
  for(let i = 0; i<items.length; i++){
    let l = 0;
    var span = $("#"+items[i].codigo);
    var comprado = comprados.find((compra) =>{
      if (compra.codigo === items[i].codigo){
        return compra;
      }
      l++;
    });
    if (comprado !== undefined){
      var ult_qtd = historico[0].produtos.find((hist) => {
          if (hist.produto === items[i].codigo){
            return hist;
          }
        });
      ult_qtd = ult_qtd === undefined ? {quantidade:0} : ult_qtd;
      span.removeClass("hide");
      span.text("Média: "+(comprado.quantidade/historico_tam).toFixed(2)+
        " Ultima: "+ ult_qtd.quantidade);
    } else {
      span.addClass("hide");
    }
  }
}


function handle_cobrancas(cobs){
  "use strict";
  if (cobs.length === 0){
    $('#atrasado_header').addClass("hide");
  } else {
    cobs.sort((a,b) => {
      if (a.vencimento.$date > b.vencimento.$date){
        return 1;
      }
      else {
        return -1;
      }
    });
    var cobrancas = "";
    if (cobs.length >0){
      $('#atrasado_header').removeClass("hide");
    }
    for (let i = 0; i < cobs.length; i++){
      var cob = cobs[i];
      cobrancas += (
        "<tr>"+
        "<td>"+cob.nota_fiscal+"</td>"+
        "<td>"+ new Date(cob.vencimento.$date).toISOString().slice(0,10)+"</td>"+
        "<td>R$"+cob.valor+"</td>"+
        "<td>R$"+(parseFloat(cob.valor) + parseFloat(cob.valor)*0.004*((Date.now()-cob.vencimento.$date)/(1000*3600*24))).toFixed(2) +"</td>"+
        "</tr>"
      );
    }
    $('#linha_atrasado').html(cobrancas);
  }
}

function zerar(id){
  "use strict";
  let input_qtd = $("#quantidade-"+id);
  let input_un = $("#unidade-"+id);
  let desconto = $("#desconto-"+id);
  desconto.val(0);
  input_qtd.val('0');
  input_un.val(items[id-1].valor);
  handler("quantidade",id);
}


function resumo_pedido(){
  "use strict";
  let comprados = [];
  for (let i = 0; i< items.length;i++){
    if (items[i].quantidade !== undefined){
      if (items[i].quantidade !== 0){
        comprados.push(items[i]);
      }
    }
  }
  return comprados;
}


function resumo(){
  "use strict";
  let repre = $("#representante").val();
  let cli = $("#cliente").val();
  if (repre === '' || cli === ''){
    M.toast({html:"Representante ou cliente não inseridos"});
  } else {
    let ped = resumo_pedido();
    let peds = '';
    for (let i = 0; i < ped.length; i++){
      peds += (
        "<tr>"+
          "<td>"+ped[i].codigo+"</td>"+
          "<td>"+ped[i].descricao+"</td>"+
          "<td>"+ped[i].quantidade+"</td>"+
          "<td>"+ped[i].pedido+"</td>"+
          "<td><b>R$ "+(ped[i].pedido * ped[i].quantidade).toFixed(2)+"</b></td>"+
        "</tr>"
      );
    }
    $('#linha_resumo').html(peds);
    $('#final_resumo').html(
      "<tr>" +
      "<td><span>Total</span></td>" +
      "<td><span><b>R$ "+ total_ped +"</b></span></td>" +
      "</tr>"
    );
    $('#representante_resumo').html("Representante: <b>"+repre+"</b>");
    $('#cliente_resumo').html("Cliente: <b>"+cli+"</b>");
  }
}

function enviar() {

}


function formas_de_pagamento() {
  "use strict";
  return {pag0: $("#pag0:checked").val() !== undefined,pag7: $("#pag7:checked").val() !== undefined,
    pag14: $("#pag14:checked").val() !== undefined, pag21: $("#pag21:checked").val() !== undefined,
    pag28: $("#pag28:checked").val() !== undefined,pag35: $("#pag35:checked").val() !== undefined};
}


function cria_pdf(){
  "use strict";
  let repre = $("#representante").val();
  let cli = $("#cliente").val();
  let items = resumo_pedido();
  let data_entrega = $("#entrega").val();
  let observacoes = $("#observacoes").val();
  let forma_de_pagamento = formas_de_pagamento();
  M.Modal.getInstance($("#modal1")).close();
  $("#texto_enviando").text("Por favor aguarde, seu pedido está sendo enviado.");
  M.Modal.getInstance($("#modal_enviando")).open();
  $.post("/resumo", {cliente: cli, representante: repre, items: items, numero: items.length,
      pagamento: forma_de_pagamento, data_entrega: data_entrega, observacoes: observacoes},
    function (data) {
    if (data.res === 200){
      M.toast({html:"Enviado com Sucesso"});
      for (let i =0; i<items.length; i++){
        zerar(items[i].id);
      }
    } else {
      M.toast({html:"Houve algum erro"});
    }
    M.Modal.getInstance($("#modal_enviando")).close();
  });
}

function forma_de_pagamento(){
  "use strict";
  let pagamento = formas_de_pagamento();
  if (pagamento.pag0 && (pagamento.pag7 || pagamento.pag14 || pagamento.pag21 || pagamento.pag28 || pagamento.pag35)){
    $("#pag0").prop( "checked", false );
  } else if (!(pagamento.pag7 || pagamento.pag14 || pagamento.pag21 || pagamento.pag28 || pagamento.pag35)) {
    $("#pag0").prop( "checked", true );
  }
}
