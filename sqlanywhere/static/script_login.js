/*jshint esversion: 6 */
/*globals $:false */
$(document).ready(function(){
  "use strict";
  $('#modal_login').modal({dismissible: false});
  M.Modal.getInstance($("#modal_login")).open();
});

function onload_tabela() {}

function login() {
  "use strict";
  let cnpj_cpf = $("#cnpj_cpf").val();
  let codigo = $("#codigo").val();
  $.post("/login",{cnpj_cpf: cnpj_cpf, codigo: codigo}, function (data){
    console.log(data)
  });
}
