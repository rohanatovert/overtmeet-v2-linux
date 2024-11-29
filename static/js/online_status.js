var loc = window.location;
var wsStart = 'ws://';
if (loc.protocol == 'https:') {
    wsStart = 'wss://'
}
var endpoint = wsStart + '20.207.207.133:8001' + '/ws/online/';

const loggedin_user = document.getElementById('userName').textContent;

const online_status = new WebSocket(endpoint);

online_status.onopen = function(e){
    console.log("CONNECTED TO ONLINE CONSUMER");
    online_status.send(JSON.stringify({
        'username': loggedin_user,
        'type': 'open'
    }))
};

online_status.onclose = function(e){
    console.log("DISCONNECTED FROM ONLINE CONSUMER")
};

window.addEventListener('beforeunload', ev => {
    online_status.send(JSON.stringify(
        {
            'username':loggedin_user,
            'type':'offline'
        }
    ));
    

});

// window.addEventListener("beforeunload", function(e){
//     console.log("sending request");
//     online_status.send(JSON.stringify(
//         {
//             'username':loggedin_user,
//             'type':'offline'
//         }
//     ))
// });

online_status.onmessage = function(e){
    var data = JSON.parse(e.data);
    if (data.username != loggedin_user){
        var user_to_change = document.getElementById(`${data.username}_status`)
        if (data.online_status==true){
            user_to_change.style.color = 'green'
        }
        else{
            user_to_change.style.color = 'grey'
        }
    }
};