chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const date = new Date(data.date);
    var anio = date.getYear() + 1900;
    var mes = date.getMonth()+1;
    var dia = date.getDate();
    var h = date.getHours();
    var m = date.getMinutes();
    var fecha = dia+' de '+meses[mes]+' de '+anio+' a las '+h+":"+m
    if(!data.paciente_sender){
        $('#chat-log').prepend(`
        
        <div class="message_container_right" >
            <div class="arrow">
            <div class="outer"></div>
            <div class="inner"></div>
            </div>
            <div class="message-body">
                <strong>`+data.sender+`</strong>
                <p>`+data.message+`</p>
                <p class="fecha_chat">`+fecha+`</p>
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
                <p class="fecha_chat">`+fecha+`</p>
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
            'paciente_sender' : false,
            'date':getDate()
        }));
        messageInputDom.value = '';
    }
};

function getDate(){
    var event = new Date();
    return event;
}
            