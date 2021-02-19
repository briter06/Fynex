chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data.is_paciente);
    console.log(data.paciente_sender);
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

            