var app = angular.module("app", []);
  app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
  });
  app.controller("controlador_nutricion", function($scope,$timeout){
    $scope.desayuno_img = Math.round(Math.random());
    $scope.almuerzo_img = Math.round(Math.random());
    $scope.comida_img = Math.round(Math.random());
  });
  app.directive("detalleNutricion", function(){
    return { 
      scope: {
        id:'@',
        alimento:'@',
        tipoAlimento:'@',
        calorias:'@',
        proteinas:'@',
        carbohidratos:'@',
        grasas:'@'
      },
      template: `<div class="modal fade mensaje"  data-backdrop="static" data-keyboard="false" tabindex="-1" role="dialog" aria-hidden="true" style="padding-top:10%; overflow-y:visible;">
      <div class="modal-dialog modal-m">
      <div class="modal-content">
      <div class="modal-header"><h3 style="margin:0;"> <strong>Detalle nutricional</strong> </h3><button style="background-color: Transparent;border: none;" ng-click="esconder()">X</button></div>
      <div class="modal-body" align="left">
        <h4> <strong>ALIMENTO:</strong> {[{alimento}]}</h4>
        <h4> <strong>GRAMOS TOTALES:</strong> 100 gramos </h4><br>
        <h4> <strong>TIPO ALIMENTO:</strong> {[{tipoAlimento}]}</h4>
        <h4> <strong>CALORIAS TOTALES:</strong> {[{calorias}]} calorias</h4>
        <h4> <strong>PROTEINAS TOTALES:</strong> {[{proteinas}]} gramos</h4>
        <h4> <strong>CARBOHIDRATOS TOTALES:</strong> {[{carbohidratos}]} gramos</h4>
        <h4> <strong>GRASAS TOTALES:</strong> {[{grasas}]} gramos</h4>
      </div>
      </div></div></div>`,
    link: function(scope, element, attrs) {
      scope.esconder=function(){
        $('#'+scope.id+' .mensaje').modal('hide')
      }
    }
    }
  });

  app.directive("detalleParte", function(){
    return { 
      scope: {
        id:'@',
        parte:'@',
        proteinas:'@',
        carbohidratos:'@',
        grasas:'@'
      },
      template: `<div class="modal fade mensaje"  data-backdrop="static" data-keyboard="false" tabindex="-1" role="dialog" aria-hidden="true" style="padding-top:10%; overflow-y:visible;">
      <div class="modal-dialog modal-m">
      <div class="modal-content">
      <div class="modal-header"><h3 style="margin:0;"> <strong>Detalle nutricional</strong> </h3><button style="background-color: Transparent;border: none;" ng-click="esconder()">X</button></div>
      <div class="modal-body" align="left">
        <h4> <strong>PARTE:</strong> {[{parte.toUpperCase()}]}</h4><br>
        <h4> Comparación con el consumo ideal:</h4>
        <h4> <strong>CAMBIO EN PROTEINAS:</strong> {[{round(proteinas)}]} gramos</h4>
        <h4> <strong>CAMBIO EN CARBOHIDRATOS:</strong> {[{round(carbohidratos)}]} gramos</h4>
        <h4> <strong>CAMBIO EN GRASAS:</strong> {[{round(grasas)}]} gramos</h4>
      </div>
      </div></div></div>`,
      link: function(scope, element, attrs) {
        scope.esconder=function(){
          $('#'+scope.id+' .mensaje').modal('hide')
        }
        scope.round = function(num_t){
          try{
            var num = parseFloat(num_t);
            num = num.toFixed(2);
            var res = ""+num;
            if (num>0){
              res = "+"+res;
            }
            return res;
          }catch(err){
            return 0;
          }
        }
      }
    }
  });