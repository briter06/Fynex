var login_modal =
  login_modal ||
  (function ($) {
    'use strict';

    // Creating modal dialog's DOM
    var $dialog = $(
      '<div class="modal fade" data-backdrop="static" data-keyboard="false" tabindex="-1" role="dialog" aria-hidden="true" style="padding-top:1%; overflow-y:visible;">' +
      '<div class="modal-dialog modal-m">' +
      '<div class="modal-content">' +
      '<div class="modal-header"><h3 style="margin:0;"></h3><button style="background-color: Transparent;border: none;" onclick="login_modal.hide();">X</button></div>' +
      '<div class="modal-body" align="center">' +
      '<form method="POST">' +
      $('#login_script').attr('token') +
      '<input type="hidden" name="login" value="login"/>' +
      '<label for="user_name">Correo Electrónico</label>' +
      '<input required type="email" id="user_name" name="user_name" maxlength = "150">' +
      '<label for="password">Contraseña</label>' +
      '<input required type="password" id="password" name="password" maxlength = "128">' +
      '<div class="row">' +
      '<a href="' + $('#login_script').attr('forgot_url') + '">¿Olvidó su contraseña?</a>' +
      '</div><div class="row"><div class="col-md-12 mx-auto">' +
      '<div id="captcha_div">'+
      $('#login_script').attr('captcha') +
      '</div>'+
      '<input style="margin-top:20px" type="submit" value="Entrar"></input>' +
      '</div></div>' +
      '</form>' +
      '</div>' +
      '</div></div></div>'
      
    );

    return {
      /**
       * Opens our dialog
       * @param message Custom message
       * @param options Custom options:
       * 				  options.dialogSize - bootstrap postfix for dialog size, e.g. "sm", "m";
       * 				  options.progressType - bootstrap postfix for progress bar type, e.g. "success", "warning".
       */
      show: function (message, options) {
        // Assigning defaults
        if (typeof options === 'undefined') {
          options = {};
        }
        if (typeof message === 'undefined') {
          message = 'Iniciar sesión';
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
        // Adding callbacks
        if (typeof settings.onHide === 'function') {
          $dialog.off('hidden.bs.modal').on('hidden.bs.modal', function (e) {
            settings.onHide.call($dialog);
          });
        }

        var cap_div = $dialog.find('#captcha_div');
        var captcha_img = $(`<div class="col-md-4" id="captcha_img_custom">
        </div>`);
        var captcha_input = $(`<div class="col-md-8" id="captcha_input_custom">
        </div>
        `)
        var captcha_row = $(`<div class="row">
        </div>`)
        captcha_row.append(captcha_img);
        captcha_row.append(captcha_input);
        cap_div.find('img[class="captcha"]').appendTo(captcha_img); 
        cap_div.find('input[type="text"]').appendTo(captcha_input); 
        cap_div.append(captcha_row)

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