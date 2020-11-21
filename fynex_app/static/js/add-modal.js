var add_modal =
  add_modal ||
  (function ($) {
    'use strict';

    // Creating modal dialog's DOM
    
    var $dialog = $(
      '<div class="modal fade" data-backdrop="static" data-keyboard="false" tabindex="-1" role="dialog" aria-hidden="true" style="padding-top:1%; overflow-y:visible;">' +
      '<div class="modal-dialog modal-m">' +
      '<div class="modal-content">' +
      '<div class="modal-header"><h3 style="margin:0;"></h3><button style="background-color: Transparent;border: none;" onclick="add_modal.hide();">X</button></div>' +
      '<div class="modal-body" align="center">' +
      '<form method="POST">' +
      $('#add_script').attr('token') +
      '<input type="hidden" name="add" value="add"/>' +
      '<div id="content_edit">'+
      '</div>'+
      '<div class="row">' +
      '</div><div class="row"><div class="column-md-12 mx-auto">' +
      '<input style="margin-top:20px" type="submit" value="Agregar"></input>' +
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
      show: function (message) {
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
        var titulos = $('#titulos').children();
        var content = '';
        for (var i = 0; i < titulos.length-1; i++) {
          var elem = titulos[i];
          content = content + '<label for="'+elem.getAttribute('field')+'">'+elem.innerHTML+'</label>' + "\n";
          var step = 'maxlength';
          if (elem.getAttribute('type')=='number'){
            step = 'step';
          }
          content = content + '<input required type="'+elem.getAttribute('type')+'" name="'+elem.getAttribute('field')+'" '+step+'="'+elem.getAttribute('max')+'"/>' + "\n";

        }
        $dialog.find('#content_edit').html(content);
        
        
        // Adding callbacks
        if (typeof settings.onHide === 'function') {
          $dialog.off('hidden.bs.modal').on('hidden.bs.modal', function (e) {
            settings.onHide.call($dialog);
          });
        }
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