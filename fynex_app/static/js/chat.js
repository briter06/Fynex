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



chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};   