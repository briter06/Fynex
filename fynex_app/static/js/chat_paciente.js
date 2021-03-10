chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if(data.paciente_sender){
        $('#chat-log').prepend(`
        
        <div class="message_container_right" >
            <div class="arrow">
            <div class="outer"></div>
            <div class="inner"></div>
            </div>
            <div class="message-body">
                <strong>`+data.sender+`</strong>
                <p>`+data.message+`</p>
                <p style="font-size: small;">`+getDate()+`</p>
            </div>
        </div>

        `);
    }else{
        $('#chat-log').prepend(`
        
        <div class="message_container_left" >
            <div class="arrow">
            <div class="outer"></div>
            <div class="inner"></div>
            </div>
            <div class="message-body">
                <strong>`+data.sender+`</strong>
                <p>`+data.message+`</p>
                <p style="font-size: small;">`+getDate()+`</p>
            </div>
        </div>

        `);
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value.trim();
    if (message.length!=0){
        chatSocket.send(JSON.stringify({
            'message': message,
            'sender' : $('#chat_script').attr('sender_name'),
            'paciente_sender' : true
        }));
        messageInputDom.value = '';
    }
};

function getDate(){
    var event = new Date();
    mes = event.getMonth()+1;
    if(mes<10){
    mes_s = "0"+mes;
    }else{
    mes_s = mes;
    }
    dia = event.getDate();
    if(dia<10){
    dia_s = "0"+dia;
    }else{
    dia_s = dia;
    }

    fecha = (event.getYear()+1900)+"-"+mes_s+"-"+dia_s;
    return fecha;
}

            