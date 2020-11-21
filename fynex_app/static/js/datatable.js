$(document).ready(function() {
    var table = $('#example').DataTable( {
        responsive: true,
        "order": [] 
    } );
 
    new $.fn.dataTable.FixedHeader( table );
} );