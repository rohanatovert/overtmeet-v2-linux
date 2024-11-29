var loc = window.location;
var wsStart = 'ws://';
if (loc.protocol == 'https:') {
    wsStart = 'wss://'
}
var endpoint = wsStart + '20.207.207.133:8001' + '/ws/notify/';


const notify_socket = new WebSocket(
    endpoint
)

notify_socket.onopen = function(e){
    console.log("CONNECTED TO NOTIFICATION");
}

var count_badge = document.getElementById('count_badge');

notify_socket.onmessage = function(e){
    console.log(e);
    const data = JSON.parse(e.data);
    count_badge.innerHTML = data.count;
}

notify_socket.onclose = function(e){
    console.log("DISCONNECTED FROM NOTIFICATION");
}