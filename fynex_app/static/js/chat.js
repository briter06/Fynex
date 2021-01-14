const roomName = JSON.parse(document.getElementById('room-name').textContent);
    
if (window.location.protocol == "https:") {
    var ws_scheme = "wss://";
} else {
    var ws_scheme = "ws://"
};

const chatSocket = new WebSocket(
    ws_scheme
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    document.querySelector('#chat-log').value += (data.sender + ' : ' + data.message + '\n');
    var textarea = document.getElementById('chat-log');
    textarea.scrollTop = textarea.scrollHeight;
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value.trim();
    if (message.length!=0){
        chatSocket.send(JSON.stringify({
            'message': message,
            'sender' : $('#chat_script').attr('sender_name')
        }));
        messageInputDom.value = '';
    }
};

            