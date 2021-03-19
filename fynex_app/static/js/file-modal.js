var file_modal =
  file_modal ||
  (function ($) {
    'use strict';

    // Creating modal dialog's DOM
    
    var $dialog = $(
      '<div class="modal fade" data-backdrop="static" data-keyboard="false" tabindex="-1" role="dialog" aria-hidden="true" style="padding-top:1%; overflow-y:visible;">' +
      '<div class="modal-dialog modal-m">' +
      '<div class="modal-content">' +
      '<div class="modal-header"><h3 style="margin:0;"></h3><button style="background-color: Transparent;border: none;" onclick="file_modal.hide();">X</button></div>' +
      '<div class="modal-body" align="center">' +
      '<form method="POST" enctype="multipart/form-data">' +
      $('#file_script').attr('token') +
      '<input type="hidden" name="file" value="file"/>' +
      '<input type="file" class="filestyle" name="myfile" id="myfile" accept="application/pdf, image/png, image/jpeg, image/jpg"/>' +
      '<div id="content_edit">'+
      '</div>'+
      '<div class="row">' +
      '</div><div class="row"><div class="column-md-12 mx-auto">' +
      '<input style="margin-top:20px" type="submit" value="Subir"></input>' +
      '</div></div>' +
      '</form>' +
      '</div>' +
      '</div></div></div>'
    );;

    return {
      /**
       * Opens our dialog
       * @param message Custom message
       * @param options Custom options:
       * 				  options.dialogSize - bootstrap postfix for dialog size, e.g. "sm", "m";
       * 				  options.progressType - bootstrap postfix for progress bar type, e.g. "success", "warning".
       */
      show: function (message,result) {
        // Assigning defaults
        
        var options = {};
        if (typeof message === 'undefined') {
          message = '';
        }
        var settings = $.extend(
          {
            dialogSize: 'm',
            progressType: '',
            onHide: null, // This callback runs after the dialog was hidden
          },
          options
        );

        $dialog.find('h3').text(message);
        var content = '<input type="hidden" name="id" value="'+result+'"/>\n';
        $dialog.find('#content_edit').html(content);
        
        
        // Adding callbacks
        if (typeof settings.onHide === 'function') {
          $dialog.off('hidden.bs.modal').on('hidden.bs.modal', function (e) {
            settings.onHide.call($dialog);
          });
        }
        $dialog.find(":file").filestyle({
          'text' :'Seleccionar archivo',
          'size' :'nr',
          'placeholder':'Sin selección',
          'btnClass' :'btn-secondary left-margin'
        });
        // Opening dialog
        $dialog.modal();
      },
      /**
       * Closes dialog
       */
      hide: function () {
        $dialog.modal('hide');
      },
    };
  })(jQuery);