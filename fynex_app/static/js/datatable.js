$(document).ready(function() {
    function getToday(){
        var d = new Date();
        var anio = d.getFullYear();
        var mes = ("0"+(d.getMonth()+1)).slice(-2);
        var dia = ("0"+(d.getDate())).slice(-2);
        return anio+'-'+mes+'-'+dia;
    }

    var order = $('#datatable_script').attr('order')||'';
    var order_o = order.split(',');
    var order_o = order_o.length !=2 ? [] : order_o;

    var table = $('#example').DataTable( {
        responsive: true,
        dom: '<"#toolbar_container.row dom_wrapper fh-fixedHeader"Blf>tip',
        "order": order_o ,
        buttons: [
            {
                extend:'print',
                title : function (){return $('#datatable_script').attr('title')+" "+getToday();},
                className: 'data_button',
                text:'<img class="img_data_buttons" src="/static/images/print.png"/>',
                titleAttr: 'IMPRIMIR',
                exportOptions: {
                    columns: ':not(:last-child)',
                }
            },
            {
                extend:'excelHtml5',
                title : function (){return $('#datatable_script').attr('title')+" "+getToday();},
                className: 'data_button',
                text:'<img class="img_data_buttons" src="/static/images/excel.png"/>',
                titleAttr: 'EXCEL',
                exportData: { decodeEntities: true },
                exportOptions: {
                    columns: ':not(:last-child)',
                }
            },
            // {
            //     extend:'pdfHtml5',
            //     title : $('#datatable_script').attr('title'),
            //     className: 'data_button',
            //     text:'<img class="img_data_buttons" src="https://www.biochek.com/wp-content/uploads/2018/07/adobe-pdf-icon-logo-png-transparent.png"/>',
            //     titleAttr: 'PDF',
            //     exportData: { decodeEntities: true },
            //     exportOptions: {
            //         columns: ':not(:last-child)',
            //     }
            // }
        ],
        oLanguage:{"sSearch": "<strong style='font-weight:normal;font-size:20px'>Buscar:</strong>"},
        language:{"lengthMenu": "Mostrar _MENU_ registros","info": "Mostrando del registro _START_ al _END_. Total registros: _MAX_","paginate": {"previous": "Anterior","next":"Siguiente"}}
    } );
} );