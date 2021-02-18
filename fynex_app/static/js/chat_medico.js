document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value.trim();
    if (message.length!=0){
        chatSocket.send(JSON.stringify({
            'message': message,
            'sender' : $('#chat_script').attr('sender_name'),
            'paciente_sender' : false
        }));
        messageInputDom.value = '';
    }
};

            