let awayTimes = 0;
let startTimeForAway = null;
let totalAwayTime = 0;

let inactivityTimes = 0;
let startTimeForInactivity = null;
let totalInactivityTime = 0;

let focusLossTimes = 0;
let startTimeForFocusLoss = null;
let totalFocusLossTime = 0;
// Draggable functionality
const floatingBox = document.querySelector('.floating-box');
// let isDragging = false;
// let dragStartX, dragStartY;
let inactivityTimer;
let mouseInWindow = true;
let startTimeForMouseOut = null;
let totalMouseOutTime = 0;

document.addEventListener('DOMContentLoaded', function () {
    // Access the data attribute
    var userInfoElement = document.getElementById('user-info');
    var moderatorInfoElement = document.getElementById('moderator-info');
    var my_username = userInfoElement.getAttribute('data-username');
    var moderator_username = moderatorInfoElement.getAttribute('data-username');
    // console.log('USERNAMES:', my_username, moderator_username);
            
        if (my_username === moderator_username ) {
            const headers = new Headers();
            headers.append('Content-Type', 'application/json; charset=utf-8');
            headers.append('X-Content-Type-Options', 'nosniff');
            headers.append('Cache-Control', 'no-cache');
                
            var allUserData;
            var activeTracking = '';

            function getUsersInfoFromDatabase() {
                // To the moderator
                fetch('api/get_otherusersystem_data/', {
                    method: 'GET',
                    headers: headers
                })
                .then(response => response.json())
                .then(data => {
                    // console.log("DATA from get api",data);
                    allUserData = data.usersData;
                    console.log("ALLUSERDATA:", allUserData);
                    populateParticipantsDropdown();
                    // Iterate over the properties of the object
                    // for (const key in allUserData) {
                    //     if (allUserData.hasOwnProperty(key)) {
                    //     const value = allUserData[key];
                    //     // Do something with the key-value pair
                    //     console.log(`${key}: ${value}`);
                    //     }
                    // }
                    // if (data.status === 'success') {
                    //     console.log('User data updated successfully.');
                    // } else {
                    //     console.error('Failed to update user data:', data.message);
                    // }
                })
                .catch(error => {
                    console.error('Error updating user data:', error);
                });
            }





            // Function to populate the participants dropdown
            function populateParticipantsDropdown() {
                const participantsDropdown = document.getElementById('participantsDropdown');
                for (let username in allUserData) {
                    if (allUserData.hasOwnProperty(username)) {
                        let userData = allUserData[username];
                
                        // Now you can access properties of the userData object
                        const participantItem = document.createElement('a');
                        participantItem.textContent = username;
                        participantItem.addEventListener('click', function() {
                            activeTracking = username;
                            displayUserInfo(allUserData[activeTracking]);
                        });
                        participantsDropdown.appendChild(participantItem);
                        // console.log(`Username: ${username}`);
                        // console.log(`User ID: ${userData.user_id}`);
                        // console.log(`Devices: ${userData.devices.audio}, ${userData.devices.video}, ${userData.devices.display}`);
                        // console.log(`Tracker: ${userData.tracker.awayTimes}, ${userData.tracker.awayMinutes}, ${userData.tracker.awaySeconds}`);
                        // console.log(`Updated On: ${userData.updated_on}`);
                    }
                }
                // allUserData.forEach(user => {
                //   const participantItem = document.createElement('a');
                //   participantItem.textContent = user.name;
                //   participantItem.addEventListener('click', () => displayUserInfo(user));
                //   participantsDropdown.appendChild(participantItem);
                // });
            }

            // Function to display user information sections
            function displayUserInfo(user) {
                // activeTracking  = user; 
                const videoInfoSection = document.getElementById('userInfo');
                const audioInfoSection = document.getElementById('audioInfo');
                const displayInfoSection = document.getElementById('displayInfo');
                const trackerInfoSection = document.getElementById('trackerInfo');
                // Clear existing content
                // console.log("YEAH",user.devices.audio);
                // videoInfoSection.innerHTML = `<li>Camera Info: ${user.devices.video}</li>`;
                // audioInfoSection.innerHTML = `<li>Audio Info: ${user.devices.audio}</li>`;
                // displayInfoSection.innerHTML = `<li>Display Info: ${user.devices.display}</li>`;
                // trackerInfoSection.innerHTML = `<li>Tracking Info:<br>` +
                //                                 `Times away from tab: ${user.tracker.awayTimes}<br>` +
                //                                 `Total away time: ${user.tracker.awayMinutes} minutes and ${user.tracker.awaySeconds} seconds<br><br>` +
                //                                 `Inactivity events (mouse left window): ${user.tracker.inactivityTimes}<br>`+
                //                                 `Total mouse out time: ${user.tracker.mouseOutMinutes} minutes and ${user.tracker.mouseOutSeconds} seconds<br><br></li>` ;

                // Clear existing content
                videoInfoSection.innerHTML = '';
                audioInfoSection.innerHTML = '';
                displayInfoSection.innerHTML = '';
                trackerInfoSection.innerHTML = '';
                // console.log("DATA of",activeTracking,`Total mouse out time: ${user.tracker.mouseOutMinutes} minutes and ${user.tracker.mouseOutSeconds} seconds<br><br>`);
                // Create new elements and append them to the sections
                const videoInfoItem = document.createElement('li');
                videoInfoItem.textContent = `Camera Info: ${user.devices.video}`;
                videoInfoSection.appendChild(videoInfoItem);

                const audioInfoItem = document.createElement('li');
                audioInfoItem.textContent = `Audio Info: ${user.devices.audio}`;
                audioInfoSection.appendChild(audioInfoItem);

                const displayInfoItem = document.createElement('li');
                displayInfoItem.textContent = `Display Info: ${user.devices.display}`;
                displayInfoSection.appendChild(displayInfoItem);

                const trackerInfoItem = document.createElement('li');
                trackerInfoItem.innerHTML = `Tracking Info:<br>` +
                    `Times away from tab: ${user.tracker.awayTimes}<br>` +
                    `Total away time: ${user.tracker.awayMinutes} minutes and ${user.tracker.awaySeconds} seconds<br><br>` +
                    `Inactivity events (mouse left window): ${user.tracker.inactivityTimes}<br>` +
                    `Total mouse out time: ${user.tracker.mouseOutMinutes} minutes and ${user.tracker.mouseOutSeconds} seconds<br><br>`;
                trackerInfoSection.appendChild(trackerInfoItem);
            }


            function getUsersUpdatedInfoFromDatabase(activeUser){
                // To the moderator
                
                fetch('api/get_otherusersystem_data/', {
                    method: 'GET',
                    headers: headers
                })
                .then(response => response.json())
                .then(data => {
                    // console.log("DATA from get api",data);
                    allUserData = data.usersData;
                    // console.log(allUserData[activeUser]);
                    displayUserInfo(allUserData[activeUser]);
                })
                .catch(error => {
                    console.error('Error updating user data:', error);
                });
            };
            
            // Populate the participants dropdown when the page loads
            var getDetailsAnchor = document.getElementById('participants'); 
            getDetailsAnchor.addEventListener('mouseover', getUsersInfoFromDatabase());
            // var trackinguser = document.getElementById('participantsDropdown'); 
            // trackinguser.addEventListener('click', function() {
            //     activeTracking = trackinguser.textContent;
            // });
  

            function freq(){
                // console.log(activeTracking);
                if (!activeTracking==''){
                    // console.log('JOJO');
                    getUsersUpdatedInfoFromDatabase(activeTracking);
                };
                /// When activeTracking is finished stop interval
            }
            // getDetailsAnchor.addEventListener('click', getUsersInfoFromDatabase());
            // Call myFunction every second (1000 milliseconds)
            var intervalId = setInterval(freq, 1000);


        }
        else{

        // function resetInactivityTimer() {
            //     clearTimeout(inactivityTimer);
            //     if (startTimeForInactivity !== null) {
            //         totalInactivityTime += Date.now() - startTimeForInactivity;
            //         updateTrackingInfo();
            //     }
            //     startTimeForInactivity = Date.now();
            //     inactivityTimer = setTimeout(() => {
            //         inactivityTimes++;
            //         updateStatus('User is inactive for past 5 minutes', 'alert-danger');
            //         updateTrackingInfo();
            //     }, 300000); // 5 minutes of inactivity
            // }


            window.addEventListener('blur', () => {
                if (!mouseInWindow) {
                    focusLossTimes++;
                    startTimeForFocusLoss = Date.now();
                    updateStatus('Browser window lost focus', 'alert-danger');
                }
            });

            window.addEventListener('focus', () => {
                if (startTimeForFocusLoss !== null) {
                    totalFocusLossTime += Date.now() - startTimeForFocusLoss;
                    startTimeForFocusLoss = null;
                    updateStatus('Please focus on the test.', 'alert-info'); //If moderator show participant is focusing on the test
                    updateTrackingInfo();
                }
            });



            var awayMinutes = 0;
            var awaySeconds = 0;
            var mouseOutMinutes = 0;
            var mouseOutSeconds = 0;

            function updateTrackingInfo() {
                awayMinutes = Math.floor(totalAwayTime / 60000);
                awaySeconds = ((totalAwayTime % 60000) / 1000).toFixed(0);

                mouseOutMinutes = Math.floor(totalMouseOutTime / 60000);
                mouseOutSeconds = ((totalMouseOutTime % 60000) / 1000).toFixed(0);

                // const focusLossMinutes = Math.floor(totalFocusLossTime / 60000);
                // const focusLossSeconds = ((totalFocusLossTime % 60000) / 1000).toFixed(0);

                document.getElementById('trackingInfo').innerHTML = 
                    `Times away from tab: ${awayTimes}<br>` +
                    `Total away time: ${awayMinutes} minutes and ${awaySeconds} seconds<br><br>` +
                    `Inactivity events (mouse left window): ${inactivityTimes}<br>`+
                    `Total mouse out time: ${mouseOutMinutes} minutes and ${mouseOutSeconds} seconds<br><br>` ;
                    // `Focus loss times: ${focusLossTimes}<br>` +
                    // `Total focus loss time: ${focusLossMinutes} minutes and ${focusLossSeconds} seconds`;
                    updateUserInDatabase();
                    // getUsersInfoFromDatabase();

            }



            var videoDevices;
            function getVideoDevices(){
                videoDevices = [];
                document.getElementById('videoInfo').innerHTML = ``;
                if (!navigator.mediaDevices?.enumerateDevices) {
                    console.log("enumerateDevices() not supported.");
                    } else {
                    // List cameras and microphones.
                    navigator.mediaDevices
                        .enumerateDevices()
                        .then((devices) => {
                        devices.forEach((device) => {
                            // console.log(`${device.kind}: ${device.label} id = ${device.deviceId}`);
                            if(device.kind==='videoinput'){
                                if (!audioDevices.includes(device.label)){
                                    if (device.label===''){
                                        document.getElementById('videoInfo').innerHTML += `Default Video Source</br>`;
    
                                    }
                                    else{
                                    document.getElementById('videoInfo').innerHTML += `${device.label}</br>`;
                                        
                                    }
                                    videoDevices.push(device.label);
                                    updateUserInDatabase();
                                    // getUsersInfoFromDatabase();
                                }
                                
                            }
                            
                        });
                        })
                        .catch((err) => {
                        console.error(`${err.name}: ${err.message}`);
                        });
                    }
                }

            var audioDevices;
            function getAudioDevices(){
                audioDevices = [];
                document.getElementById('audioInfo').innerHTML = ``;
                if (!navigator.mediaDevices?.enumerateDevices) {
                    console.log("enumerateDevices() not supported.");
                    } else {
                    // List cameras and microphones.
                    navigator.mediaDevices
                        .enumerateDevices()
                        .then((devices) => {
                        devices.forEach((device) => {
                            // console.log(`${device.kind}: ${device.label} id = ${device.deviceId}`);
                            
                            if(device.kind==='audioinput'){
                                if (!audioDevices.includes(device.label)) {
                                    document.getElementById('audioInfo').innerHTML += `<li>${device.label}</li></br>`;
                                    audioDevices.push(device.label);
                                    updateUserInDatabase();
                                    // getUsersInfoFromDatabase();
                                } 
                                
                            }
                            
                        });
                        })
                        .catch((err) => {
                        console.error(`${err.name}: ${err.message}`);
                        });
                    }
            }


            function clearVideoDetails(){
                document.getElementById('videoInfo').innerHTML = ``;
            };
            function clearAudioDetails(){
                document.getElementById('audioInfo').innerHTML = ``;
            };
            function clearDisplayDetails(){
                document.getElementById('displayInfo').innerHTML = ``;
            };
            // floatingBox.addEventListener('mousedown', function(e) {
            //     isDragging = true;
            //     dragStartX = e.clientX - floatingBox.getBoundingClientRect().left;
            //     dragStartY = e.clientY - floatingBox.getBoundingClientRect().top;
            //     floatingBox.style.cursor = 'grabbing';
            // });

            // document.addEventListener('mousemove', function(e) {
            //     if (isDragging) {
            //         floatingBox.style.left = (e.clientX - dragStartX) + 'px';
            //         floatingBox.style.top = (e.clientY - dragStartY) + 'px';
            //     }
            // });

            // document.addEventListener('mouseup', function() {
            //     isDragging = false;
            //     floatingBox.style.cursor = 'grab';
            // });



            function updateStatus(message, alertClass) {
                const statusDiv = document.getElementById('status');
                statusDiv.textContent = message;
                statusDiv.className = `alert ${alertClass}`;
            }



            // Mouse Event Listeners
            window.addEventListener('mouseover', () => {
                mouseInWindow = true;
                updateStatus('Please focus on the test.', 'alert-info');
                if (startTimeForMouseOut) {
                    
                    // console.log(Date.now() - startTimeForMouseOut);
                    if((Date.now() - startTimeForMouseOut) > 1000 ){
                        inactivityTimes++;
                        totalMouseOutTime += Date.now() - startTimeForMouseOut;
                    };
                    startTimeForMouseOut = null;
                    updateTrackingInfo();
                }
                // console.log("MouseOver");
            });

            // Mouse Event Listeners for Inactivity Tracking
            window.addEventListener('mouseout', () => {
                // clearTimeout(inactivityTimer);
                if (!startTimeForMouseOut) {
                    startTimeForMouseOut = Date.now();
                }
                updateStatus('Mouse left the window - potential inactivity', 'alert-warning');
                updateTrackingInfo();
            });



            window.addEventListener('focus', () => {
                console.log("Focusing");
                updateStatus('Please focus on the test.', 'alert-info');
            });


            // window.onload = resetInactivityTimer;
            // window.onmousemove = resetInactivityTimer;
            // window.onmousedown = resetInactivityTimer;
            // window.onclick = resetInactivityTimer;
            // window.onscroll = resetInactivityTimer;
            // window.onkeypress = resetInactivityTimer;



            // Keydown Event for Detecting Specific Key Combinations
            window.addEventListener('keydown', (event) => {
                if ((event.key === 'Tab' && event.altKey) || (event.key === 'Tab' && event.metaKey)) {
                    updateStatus('User might be attempting to switch windows', 'alert-warning');
                    awayTimes++;
                    updateTrackingInfo();
                    
                }
                // Add more key detection if necessary
            });





            // const used_devices = mediastream.getTracks()
            //   .map( (track) => track.getSettings().deviceId );
            //   console.log(`List of Media Devices: ${awayTimes}<br>`);
            //   document.getElementById('devicesInfo').innerHTML =  `List of Media Devices: ${awayTimes}<br>` ;


            // If you run this on your left screen (0),
            // the window will open on your right screen

            // JavaScript


            // // Rest of the code remains the same
            // window.onload = function() {
            //     // Show the modal when the window loads
            //     document.getElementById('myModal').style.display = 'block';

            //     // Add an event listener to the button for permission request
            //     document.getElementById('requestPermissionButton').addEventListener('click', () => {
            //         // Request permission here
            //         Notification.requestPermission()
            //             .then(async (permission) => {
            //                 console.log('Permission status:', permission);
            //                 // Call openWindow function
            //                 getDisplayDevices()
            //                 .then((details) => {
            //                     // Handle the result when the promise is resolved
            //                     console.log("Promise resolved:", details);
            //                     // Perform actions with the details
            //                 })
            //                 .catch((error) => {
            //                     // Handle the error when the promise is rejected
            //                     console.error("Promise rejected:", error);
            //                     // Perform actions for error handling
            //                 });
            //             })
            //             .catch((error) => {
            //                 console.error('Permission request error:', error);
            //             });

            //         // Hide the modal after permission is requested
            //         document.getElementById('myModal').style.display = 'none';
            //     });
            // };

            // async function getDisplayDevices() {
            //     return new Promise((resolve, reject) => {
            //         if (window.screen.isExtended) {
            //             // Get screen info
            //             const details = getScreenDetails();
            //             console.log("Display Screens", details);
            //             document.getElementById('displayInfo').innerHTML += `<li>Current Screen: ${details.PromiseResult.currentScreen}</li></br>`;
            //             details.PromiseResult.screens.forEach((display) => {
                            
            //                 if(display.kind==='audioinput'){
            //                     document.getElementById('displayInfo').innerHTML += `<li>${display}</li></br>`;
            //                 }
                            
            //             });
                        
            //             // Simulating an asynchronous operation (e.g., fetching data)
            //             setTimeout(() => {
            //                 resolve(details);
            //             }, 1000);
            //         } else {
            //             // If the screen is not extended, reject the promise
            //             reject("Screen is not extended");
            //             document.getElementById('displayInfo').innerHTML += `<li>${details}</li></br>`;
            //         }
            //     });
            // }
            var displayDevices;
            window.onload = function () {

                // Show the modal when the window loads
                document.getElementById('permissionModal').style.display = 'flex';

                // Add an event listener to the button for permission request
                document.getElementById('requestPermissionButton').addEventListener('click', async () => {
                    try {
                        // Request permission here
                        const permission = await Notification.requestPermission();
                        console.log('Permission status:', permission);

                        // Call openWindow function
                        const details = await getDisplayDevices();
                        // Handle the result when the promise is resolved
                        console.log("Promise resolved:", details);
                        screens(details);
                        updateTrackingInfo();
                        
                        // Perform actions with the details
                    } catch (error) {
                        // Handle the error when the promise is rejected
                        console.error("Promise rejected:", error);
                        // Perform actions for error handling
                    } finally {
                        // Hide the modal after permission is requested
                        document.getElementById('permissionModal').style.display = 'none';
                    }
                });

                // Add event listener for hover on the "projects" anchor tag
                document.getElementById('projects').addEventListener('mouseenter', async () => {
                    try {
                        const details = await getDisplayDevices();
                        // Handle the result when the promise is resolved
                        console.log("Promise resolved on hover:", details);
                        screens(details);

                        // Perform actions with the details
                    } catch (error) {
                        // Handle the error when the promise is rejected
                        console.error("Promise rejected on hover:", error);
                        // Perform actions for error handling
                    }
                });
                
            };

            async function getDisplayDevices() {
                return new Promise((resolve, reject) => {
                    const details = getScreenDetails();
                    console.log("Promised Screens", details);
                    resolve(details);
                });
            }

            function screens(details){
                displayDevices = [];
                document.getElementById('displayInfo').innerHTML = ``;
                if (window.screen.isExtended) {
                    // Get screen info
                    document.getElementById('displayInfo').innerHTML += `<h6>This Screen is EXTENDED!</h6></br>`;
                    // console.log("Display Screens", details.screens);

                    // Simulating an asynchronous operation (e.g., fetching data)
                    // setTimeout(() => {
                    //     resolve(details);
                    // }, 1000);
                } else {
                    // If the screen is not extended, reject the promise
                    console.log("Screen is not extended", details);
    
                   
                }
                details.screens.forEach((display) => {
                    var displayLabel = display.label;
                    if (displayLabel===''){
                        displayLabel = 'Default';
                    }
                    document.getElementById('displayInfo').innerHTML += `<li>${displayLabel}`;
                    if(display.label===details.currentScreen['label']){
                        document.getElementById('displayInfo').innerHTML += `<span>Current Screen: ${details.currentScreen['label']} -> Is Extended : ${details.currentScreen['isExtended']} -> Is Internal : ${details.currentScreen['isInternal']} -> Is Primary : ${details.currentScreen['isPrimary']}</span>`;
                    }
                    document.getElementById('displayInfo').innerHTML += `</li></br>`;
                    displayDevices.push(displayLabel);
                    displayDevices.push([`Current Screen: ${details.currentScreen['label']} -> Is Extended : ${details.currentScreen['isExtended']} -> Is Internal : ${details.currentScreen['isInternal']} -> Is Primary : ${details.currentScreen['isPrimary']}`]);
                    updateUserInDatabase();
                    // getUsersInfoFromDatabase();
                
            });

            }


            // API FOR SENDING DATA

            // JavaScript code
            function updateUserInDatabase() {
                const meetID = '{{ room_code }}';
                var devices = {
                    "audio": audioDevices,
                    "video": videoDevices,
                    "display": displayDevices
                };
                var tracker = {
                    "awayTimes": awayTimes,
                    "awayMinutes": awayMinutes,
                    "awaySeconds": awaySeconds,
                    "inactivityTimes": inactivityTimes,
                    "mouseOutMinutes": mouseOutMinutes,
                    "mouseOutSeconds": mouseOutSeconds
                };
                var userdata = {
                    "devices": devices,
                    "trackingInfo": tracker,
                    "roomId": meetID,
                };

                var jsonData = JSON.stringify(userdata);
                // Make a POST request to the Django view

                fetch('api/update_usersystem_data/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: jsonData,  // Adjust the data you want to send
                })
                .then(response => response.json())
                // .then(data => {
                //     if (data.status === 'success') {
                //         console.log('User data updated successfully.');
                //     } else {
                //         console.error('Failed to update user data:', data.message);
                //     }
                // })
                .catch(error => {
                    console.error('Error updating user data:', error);
                });




            
            };
            var videoAnchor = document.getElementById('about'); // Replace with your actual video element ID
            videoAnchor.addEventListener('mouseover', getVideoDevices());
            getVideoDevices();
            // videoAnchor.addEventListener('mouseout', clearVideoDetails());
            var audioAnchor = document.getElementById('blog'); // Replace with your actual video element ID
            audioAnchor.addEventListener('mouseover', getAudioDevices());
            getAudioDevices();
            // audioAnchor.addEventListener('mouseout', clearAudioDetails());
            var displayAnchor = document.getElementById('projects'); // Replace with your actual video element ID
            // displayAnchor.addEventListener('mouseleave', clearDisplayDetails());
            

        }
        
            
});

