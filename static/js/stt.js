window.onload = function () {
  init_transcripts();
};

const transcribeBtn = document.querySelector(".transcribe"),
  result = document.querySelector(".result"),
  // downloadBtn = document.querySelector(".download"),
  inputLanguage = document.querySelector("#language"),
  clearBtn = document.querySelector(".clear");

let SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition,
  recognition,
  transcribing = false;

function populateLanguages() {
  languages.forEach((lang) => {
    const option = document.createElement("option");
    option.value = lang.code;
    option.innerHTML = lang.name;
    inputLanguage.appendChild(option);
  });
}

populateLanguages();

function speechToText() {
  try {
    recognition = new SpeechRecognition();
    recognition.lang = inputLanguage.value;
    recognition.interimResults = true;
    transcribeBtn.classList.add("transcribing");
    transcribeBtn.querySelector("p").innerHTML = "Listening...";
    recognition.start();
    recognition.onresult = (event) => {
      const speechResult = event.results[0][0].transcript;
      //detect when intrim results
      if (event.results[0].isFinal) {
        // result.innerHTML += " " + speechResult;
        transciption_real_time(speechResult);
        // result.querySelector("p").remove();
      } else {
        //creative p with class interim if not already there
        if (!document.querySelector(".interim")) {
          const interim = document.createElement("p");
          interim.classList.add("interim");
          result.appendChild(interim);
        }
        //update the interim p with the speech result
        
        document.querySelector(".interim").innerHTML = " " + speechResult;
      }
      // downloadBtn.disabled = false;
    };
    recognition.onspeechend = () => {
      download();
      result.innerHTML = ''
      speechToText();
    };
    recognition.onerror = (event) => {
      stoptranscribing();
      if (event.error === "no-speech") {
        // alert("No speech was detected. Stopping..."+event.error);
        apiObj.executeCommand('showNotification', {
          title: 'No speech was detected. Stopping captions.', // Title of the notification.
          description: "Transcription", // Content of the notification.
          // uid: String, // Optional. Unique identifier for the notification.
          // type: 'info', // Optional. Can be 'info', 'normal', 'success', 'warning' or 'error'. Defaults to 'normal'.
          timeout: 'short' // optional. Can be 'short', 'medium', 'long', or 'sticky'. Defaults to 'short'.
        });
      } else if (event.error === "audio-capture") {
        apiObj.executeCommand('showNotification', {
          title: "Transcription", // Title of the notification.
          description: 'No microphone was found. Ensure that a microphone is installed.', // Content of the notification.
          // uid: String, // Optional. Unique identifier for the notification.
          // type: 'info', // Optional. Can be 'info', 'normal', 'success', 'warning' or 'error'. Defaults to 'normal'.
          timeout: 'short' // optional. Can be 'short', 'medium', 'long', or 'sticky'. Defaults to 'short'.
        });
        // alert(
        //   "No microphone was found. Ensure that a microphone is installed."
        // );
      } else if (event.error === "not-allowed") {
        // alert("Permission to use microphone is blocked.");
        apiObj.executeCommand('showNotification', {
          title: "Transcription", // Title of the notification.
          description: 'Permission to use microphone is blocked.', // Content of the notification.
          // uid: String, // Optional. Unique identifier for the notification.
          // type: 'info', // Optional. Can be 'info', 'normal', 'success', 'warning' or 'error'. Defaults to 'normal'.
          timeout: 'short' // optional. Can be 'short', 'medium', 'long', or 'sticky'. Defaults to 'short'.
        });
      } else if (event.error === "aborted") {
        // alert("Listening Stopped.");
        stoptranscribing();
        apiObj.executeCommand('showNotification', {
          title: "Transcription", // Title of the notification.
          description: 'Listening Stopped.', // Content of the notification.
          // uid: String, // Optional. Unique identifier for the notification.
          // type: 'info', // Optional. Can be 'info', 'normal', 'success', 'warning' or 'error'. Defaults to 'normal'.
          timeout: 'short' // optional. Can be 'short', 'medium', 'long', or 'sticky'. Defaults to 'short'.
        });
      } else {
        apiObj.executeCommand('showNotification', {
          title: "Transcription", // Title of the notification.
          description: 'Speech Recognition Error.', // Content of the notification.
          // uid: String, // Optional. Unique identifier for the notification.
          // type: 'info', // Optional. Can be 'info', 'normal', 'success', 'warning' or 'error'. Defaults to 'normal'.
          timeout: 'short' // optional. Can be 'short', 'medium', 'long', or 'sticky'. Defaults to 'short'.
          // speechToText();
        });
      }
    };
  } catch (error) {
    stoptranscribing();

    console.log(error);
  }
}





transcribeBtn.addEventListener("click", () => {
    console.log("Listening..");
  if (!transcribing) {
    // speechToText();  //should be optional; start only when mic is on.
    transcribing = true;
  } else {
    stoptranscribing();
  }
});

function stoptranscribing() {
  recognition.stop();
  transcribeBtn.querySelector("p").innerHTML = "Start Listening";
  transcribeBtn.classList.remove("transcribing");
  transcribing = false;
}


function download() {
  const text = result.innerText; // Assuming result is the element containing the transcription text
  console.log("TEXT:",text);
  // Convert the text to a JSON object
  // var username = '{{request.user.username}}';
  const jsonData = {
    username: username,
    transcription: text,
    timestamp: new Date().toISOString()
  };
  // URL of the API endpoint
const apiUrl = 'https://20.207.207.133:8000/api/transcripts/';

// Perform the POST request
fetch(apiUrl, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(jsonData),
})
  .then(response => response.json())
  .then(data => {
    console.log('Success:', data);
  })
  .catch(error => {
    console.error('Error:', error);
  });
  
  // const filename = "transcription.json";

  // // Create a Blob containing the JSON data
  // const blob = new Blob([JSON.stringify(jsonData, null, 2)], { type: "application/json" });

  // // Create a download link
  // const element = document.createElement("a");
  // element.href = window.URL.createObjectURL(blob);
  // element.download = filename;

  // // Hide the link
  // element.style.display = "none";

  // // Append the link to the document and trigger the click event
  // document.body.appendChild(element);
  // element.click();

  // // Clean up
  // document.body.removeChild(element);
}


function transciption_real_time(speechResult) {
  // Convert the text to a JSON object
  // var username = '{{request.user.username}}';
  // console.log("SPEECH RESULT:",speechResult);
  const thisUserData = {
    username: username,
    transcription: speechResult,
    timestamp: new Date().toISOString()
  };
  // URL of the API endpoint
  const apiUrl = 'https://20.207.207.133:8000/api/realtime/';

  // Perform the POST request
  fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(thisUserData),
  })
    .then(response => response.json())
    .then(data => {
      const combinedData = data['text'];
      result.innerHTML =  combinedData;
      console.log('Success:', data);
    })
    .catch(error => {
      console.error('Error:', error);
    });

    
  }

  


// function download() {
//   const text = result.innerText;
//   const filename = "speech.txt";

//   const element = document.createElement("a");
//   element.setAttribute(
//     "href",
//     "data:text/plain;charset=utf-8," + encodeURIComponent(text)
//   );
//   element.setAttribute("download", filename);
//   element.style.display = "none";
//   document.body.appendChild(element);
//   element.click();
//   document.body.removeChild(element);
// }

// downloadBtn.addEventListener("click", download);

// clearBtn.addEventListener("click", () => {
//   result.innerHTML = "";
//   // downloadBtn.disabled = true;
// });


function init_transcripts(){
    // URL of the API endpoint
    const url = 'https://20.207.207.133:8000/api/clear/';

    fetch(url, {
      method: 'POST', // Use the appropriate HTTP method (POST in this case)
      headers: {
        'Content-Type': 'application/json', // Set the content type if needed
      },
      body: JSON.stringify({}), // An empty object as the body
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
  
}