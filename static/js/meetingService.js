var apiObj = null;

var recording = false;

function BindEvent(){
    
    $("#btnHangup").on('click', function () {
        apiObj.executeCommand('hangup');
    });
    $("#btnCustomMic").on('click', function () {
        apiObj.executeCommand('toggleAudio');
    });
    $("#btnCustomCamera").on('click', function () {
        apiObj.executeCommand('toggleVideo');
    });
    $("#btnCustomTileView").on('click', function () {
        apiObj.executeCommand('toggleTileView');
    });
    $("#btnScreenShareCustom").on('click', function () {
        apiObj.executeCommand('toggleShareScreen');
    });
    $("#btn-record-screen").on('click', function () {
        if (!recording){
            apiObj.executeCommand('startRecording' ,{mode: 'local' });
            recording = true;
        }
        else{
            apiObj.executeCommand('stopRecording' ,'local');
            recording = false;
        }
        
    });
}

function StartMeeting(roomId, roomName, dispNme, moderator){
    const domain = 'overtmeet.overtideasandsolutions.in/';

    //var roomName = 'newRoome_' + (new Date()).getTime();
    
    const options = {
        roomName: roomId,
        width: '100%',
        height: '100%',
        parentNode: document.querySelector('#jitsi-meet-conf-container'),
        DEFAULT_REMOTE_DISPLAY_NAME: 'New User',
        userInfo: {
            displayName: dispNme
        },
        jwt:"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiI0QzY5MiIsImlzcyI6IjRDNjkyIiwic3ViIjoib3ZlcnRtZWV0Lm92ZXJ0aWRlYXNhbmRzb2x1dGlvbnMuaW4iLCJyb29tIjoiKiJ9.dewL2mEANrOKOHTavT6aJEYusPMaY-5SkIeEgyL8Zac",
        configOverwrite:{
            doNotStoreRoom: true,
            startVideoMuted: 0,
            startWithVideoMuted: true,
            startWithAudioMuted: true,
            enableWelcomePage: false,
            prejoinPageEnabled: false,
            disableRemoteMute: true,
            remoteVideoMenu: {
                disableKick: false
            },
        },
        interfaceConfigOverwrite: {
            filmStripOnly: false,
            DEFAULT_REMOTE_DISPLAY_NAME: 'New User'
        },
        onload: function () {
            //alert('loaded');
            $('#joinMsg').hide();
            $('#container').show();
            $('#toolbox').show();
            // $('#btnStart').text("Copy Room Code");
            // $('#btnStart').attr("data-clipboard-target","#copyText");
        }
    };
    // console.log("MEETING INFO:",dispNme , moderator);
    if( dispNme != moderator){
        console.log("removing moderator rights");
        delete options['jwt'];
        console.log(options);
    }
    apiObj = new JitsiMeetExternalAPI(domain, options);
    apiObj.executeCommand('subject', roomName);
    
    
    apiObj.executeCommand('avatarUrl', userImageUrl);
    console.log("USER IMAGE:",userImageUrl);
    apiObj.addEventListeners({
        readyToClose: function () {
            //alert('going to close');
            $('#jitsi-meet-conf-container').empty();
            $('#toolbox').hide();
            $('#container').hide();
            $('#joinMsg').show().text('Meeting Ended');
        },
        audioMuteStatusChanged: function (data) {
            if(data.muted)
                $("#btnCustomMic").text('Unmute');
            else
                $("#btnCustomMic").text('Mute');
        },
        videoMuteStatusChanged: function (data) {
            if(data.muted)
                $("#btnCustomCamera").text('Start Cam');
            else
                $("#btnCustomCamera").text('Stop Cam');
        },
        recordingStatusChanged: function (data) {
            if(data.muted)
                $("#btn-record-screen").text('Stop Recording');
            else
                $("#btn-record-screen").text('Start Recording');
        },
        tileViewChanged: function (data) {
            
        },
        screenSharingStatusChanged: function (data) {
            if(data.on)
                $("#btnScreenShareCustom").text('Stop SS');
            else
                $("#btnScreenShareCustom").text('Start SS');
        },
        // participantJoined: function(data){
        //     console.log('participantJoined', data);
        //     console.log("moderator:",moderator);
        //     console.log('myJoinedName', dispNme);
        //     // console.log('participantJoinedId', data.id);
        //     if( dispNme === moderator){
        //         apiObj.executeCommand('grantModerator',
        //         data.id
        //         );
        //         console.log("Moderator Changed")
        //     }

        // },
        participantLeft: function(data){
            console.log('participantLeft', data);
        }

        
    });

    // apiObj.executeCommand('subject', 'New Room 2');
    
    apiObj.addEventListener('audioMuteStatusChanged', obj=>{
        const mutedStatus = obj.muted ? "muted" : "unmuted";
        console.log(`Mute Status$ ${mutedStatus}`);
        
        if (mutedStatus=='unmuted'){
            apiObj.executeCommand('setNoiseSuppressionEnabled', {
                enabled: true // Enable or disable noise suppression.
            });
            speechToText();
        }
        else{
            // transcribing = false;
            stoptranscribing();
        }
        
        // apiObj.executeCommand('sendChatMessage', `I ${mutedStatus}`);
    });
    apiObj.isAudioMuted().then(muted => {
        stoptranscribing();
    });

    
    // Get the local audio tracks
 
    const localAudioTracks = apiObj.getCurrentDevices().audioInput;

        // Check if at least one audio track is unmuted
    const isAnyAudioTrackUnmuted = localAudioTracks.some(track => track && !track.isMuted());

    if (isAnyAudioTrackUnmuted) {
    console.log('At least one audio track is unmuted');
    speechToText();
    } else {
    console.log('All audio tracks are muted');
    stoptranscribing();
    }
    
    apiObj.on('readyToClose', () => {
        // URL of the API endpoint
    if( dispNme != moderator){
        // Data to be sent in the request body
        const data = {
            "roomId": roomId
        };

        const url = 'https://20.207.207.133:8000/api/stop/';

        fetch(url, {
        method: 'POST', // Use the appropriate HTTP method (POST in this case)
        headers: {
            'Content-Type': 'application/json', // Set the content type if needed
        },
        body: JSON.stringify(data), // An empty object as the body
        })
        .then(response => {
            if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json(); // Parse the JSON response if needed
        })
        .then(data => {
            console.log('Success:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });

    };
    
    document.location.href="/login";
        });
    // var recording = false;
    // apiObj.addListener("participantJoined", (data) => {
    //       // get the total number of participants
    //       const numParticipants = apiObj.getNumberOfParticipants();
    //       if (numParticipants >= 2 && !recording && "{{ current_user }}=={{ moderator }}") {
    //         // start recording
    //         apiObj.startRecording({
    //           mode: "file",
    //         });
    //         recording = true;
    //       }
    //     });

    //For start recording
    // api.addEventListener('videoConferenceStart', () => {
    //     api.executeCommand('startRecording', {
    //         mode: 'file',
    //         // dropboxToken: 'MyToken',
    //     });
    // });
}
    // apiObj.executeCommand('startRecording',{mode: 'local' })//recording mode to stop, `local`, `stream` or `file`
    
    

// var session = document.getElementById("session");
// document.getElementById("btn-toggle-remote").addEventListener("click", function() {
//     window.open("http://20.207.207.133:8501/", "_blank");
//     // session.style.display = "block";
//   });

