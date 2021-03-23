$(document).ready(function() {
    var table = $('#example').DataTable( {
        responsive: true,
        dom: '<"#toolbar_container.row dom_wrapper fh-fixedHeader"Blf>tip',
        "order": [] ,
        buttons: [
            {
                extend:'print',
                title : $('#datatable_script').attr('title'),
                className: 'data_button',
                text:'<img class="img_data_buttons" src="https://iconarchive.com/download/i47276/avosoft/warm-toolbar/print.ico"/>',
                titleAttr: 'IMPRIMIR',
                exportOptions: {
                    columns: ':not(:last-child)',
                }
            },
            {
                extend:'excelHtml5',
                title : $('#datatable_script').attr('title'),
                className: 'data_button',
                text:'<img class="img_data_buttons" src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Microsoft_Excel_2013_logo.svg/1043px-Microsoft_Excel_2013_logo.svg.png"/>',
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