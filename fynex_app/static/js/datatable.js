$(document).ready(function() {
    var table = $('#example').DataTable( {
        responsive: true,
        "order": [] ,
        oLanguage:{"sSearch": "<strong style='font-weight:normal;font-size:20px'>Buscar:</strong>"},
        language:{"lengthMenu": "Mostrar _MENU_ registros","info": "Mostrando del registro _START_ al _END_. Total registros: _MAX_","paginate": {"previous": "Anterior","next":"Siguiente"}}
    } );
} );