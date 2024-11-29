from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pyautogui
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# Replace 'path_to_web_driver' with the actual path to your web driver executable.
from django.conf import settings
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
import subprocess


script = '''
var runtimePort = chrome.runtime.connect({
    name: location.href.replace(/\/|:|#|\?|\$|\^|%|\.|`|~|!|\+|@|\[|\||]|\|*. /g, '').split('\n').join('').split('\r').join('')
});

runtimePort.onMessage.addListener(function(message) {
    if (!message || !message.messageFromContentScript1234) {
        return;
    }
});

var isRecording = false;
chrome.storage.sync.get('isRecording', function(obj) {
    document.getElementById('default-section').style.display = obj.isRecording === 'true' ? 'none' : 'block';
    document.getElementById('stop-section').style.display = obj.isRecording === 'true' ? 'block' : 'none';

    isRecording = obj.isRecording === 'true';

    // auto-stop-recording
    if (isRecording === true) {
        document.getElementById('stop-recording').click();

        chrome.tabs.query({}, function(tabs) {
        var tabIds = [];
        var url = 'chrome-extension://' + chrome.runtime.id + '/video.html';
        for (var i = tabs.length - 1; i >= 0; i--) {
            if (tabs[i].url === url) {
                tabIds.push(tabs[i].id);
                chrome.tabs.update(tabs[i].id, {
                    active: true,
                    url: url
                });
                break;
            }
        }
        if (tabIds.length) {
            chrome.tabs.remove(tabIds);
        }
    });
    }
});

function(stop-recording) {
    chrome.storage.sync.set({
        isRecording: 'false'
    }, function() {
        runtimePort.postMessage({
            messageFromContentScript1234: true,
            stopRecording: true,
            dropdown: true
        });
        window.close();
    });
};


chrome.storage.sync.set({
        enableTabCaptureAPI: 'true',
        enableTabCaptureAPIAudioOnly: 'false',
        enableMicrophone: 'false',
        enableCamera: 'false',
        enableScreen: 'false',
        isRecording: 'true',
        enableSpeakers: 'false'
    }, function() {
        runtimePort.postMessage({
            messageFromContentScript1234: true,
            startRecording: true,
            dropdown: true
        });
        window.close();
    });

'''

def open_extension(driver):
    # driver.get('extension://ndcljioonkecdnaaihodjgiliohngojp/options.html')
    driver.get('chrome-extension://ndcljioonkecdnaaihodjgiliohngojp/options.html')
    # window_before = driver.window_handles[0]
    # print(window_before)
    time.sleep(200)
    # window_before = driver.window_handles[0]
    # print(window_before)
    # EXTENSION_ID = "ndcljioonkecdnaaihodjgiliohngojp"
    driver.switch_to.window("extension://ndcljioonkecdnaaihodjgiliohngojp/dropdown.html")
    # driver.execute_script("var runtimePort = chrome.runtime.connect({name: location.href .replace(/\/|:|#|\?|\$|\^|%|\.|`|~|!|\+|@|\[|\||]|\|*. /g, '').split('\n').join('').split('\r').join('')});")
    time.sleep(10)
    
def joinAsBot(room_code, userid):
 
    room_code = room_code.lower()
    chrome_options = Options()
    chrome_options.add_argument('use-fake-device-for-media-stream')
    chrome_options.add_argument("--disable-user-media-security=true")
    chrome_options.add_argument("ngrok-skip-browser-warning=true")
    chrome_options.add_experimental_option("prefs", { \
        "profile.default_content_setting_values.media_stream_mic": 1, 
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 1, 
        "profile.default_content_setting_values.notifications": 1 ,
        "download.default_directory": fr"C:\inetpub\wwwroot\homiechat\homiechat\homiechat\media\recordings\{userid}_"+  timestr,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        
    })
    chrome_options.add_extension('C:\inetpub\wwwroot\homiechat\homiechat\static\RecordRTC.crx')
    driver = webdriver.Chrome(options=chrome_options)
    is_minimized = driver.execute_script("return document.hidden;")
    print(is_minimized)
    
    driver.execute_script("window.focus();")
    # Replace 'your_jitsi_meet_url' with the URL of your Jitsi meeting.
    driver.get(f'https://overtmeet.overtideasandsolutions.in/{room_code}?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiI0QzY5MiIsImlzcyI6IjRDNjkyIiwic3ViIjoib3ZlcnRtZWV0Lm92ZXJ0aWRlYXNhbmRzb2x1dGlvbnMuaW4iLCJyb29tIjoiKiJ9.dewL2mEANrOKOHTavT6aJEYusPMaY-5SkIeEgyL8Zac#config.startWithVideoMuted=true&config.startWithAudioMuted=true')
    # Locate and enter your name in the input field to join the meeting.
    actions = ActionChains(driver) 
    time.sleep(1)
    open_extension(driver)
    # Join the meeting.
    # join_button = driver.find_element(By.XPATH, '//span[text()="Visit Site"]')
    # join_button.click()
    # time.sleep(1)
    # Start recording using FFmpeg for the specific Chrome window
    # ffmpeg -f gdigrab -framerate 30 -i title=Calculator C:\Users\overtadmin\Downloads\output.mp4
    # ffmpeg_process = subprocess.Popen([
    #     'ffmpeg',
    #     '-f', 'gdigrab',
    #     '-framerate', '30',
    #     '-i', f'title={driver.title} - Google Chrome',  # Replace with actual window title
    #     '-c:v', 'libx264',
    #     'output.mp4'
    # ])

    name_input = driver.find_element(By.XPATH, '//input[@placeholder="Enter your name"]')
    name_input.send_keys(f"{userid}'s Bot")
    time.sleep(1)
    join_button = driver.find_element(By.XPATH, '//div[text()="Join meeting"]')
    join_button.click()
    time.sleep(1)

    toolbox = driver.find_element(By.XPATH, '//div[@id="new-toolbox"]')
    driver.execute_script("arguments[0].setAttribute('class', 'new-toolbox visible')", toolbox)
    record_button = driver.find_element(By.XPATH, '//div[@class="toolbox-button-wth-dialog context-menu"]')
    record_button.click()
    time.sleep(1)
    record_button = driver.find_element(By.XPATH, '//div[contains(@aria-label,"Toggle recording")]')
    record_button.click()
    time.sleep(1)
    # Click Start Recording
    start_button = driver.find_element(By.XPATH, '//span[text()="Start recording"]')
    start_button.click()

    # element = driver.find_element(By.TAG_NAME,'body')
    # ActionChains(driver) \
    # .click(element) \
    #     .key_down(Keys.TAB) \
    #     .key_up(Keys.TAB) \
    #     .key_down(Keys.RETURN) \
    #     .key_up(Keys.RETURN) \
    #     .perform()

    driver.maximize_window()
    # while True:
    #     print(pyautogui.position())
    time.sleep(1)
    for i in range(10):
        pyautogui.click(1420,578)  
    # time.sleep(1)
    # toolbox = driver.find_element(By.XPATH, '//div[@id="new-toolbox"]')
    # driver.execute_script("arguments[0].setAttribute('class', 'new-toolbox visible')", toolbox) 
    badge = driver.find_element(By.XPATH, '//div[contains(@aria-label,"Open participants pane")]')
    badge.click()
    time.sleep(20)
    while True:
        noOfParticipants = driver.find_element(By.XPATH, '//div[@class="css-115vpy6-heading"]').text
        noOfParticipants = noOfParticipants.split()[2].strip("(").strip(")")
        print(noOfParticipants)
        if int(noOfParticipants) == 1:
            break


    toolbox = driver.find_element(By.XPATH, '//div[@id="new-toolbox"]')
    driver.execute_script("arguments[0].setAttribute('class', 'new-toolbox visible')", toolbox)
    time.sleep(1)
    record_button = driver.find_element(By.XPATH, '//div[@class="toolbox-button-wth-dialog context-menu"]')
    record_button.click()
    time.sleep(1)
    record_button = driver.find_element(By.XPATH, '//div[contains(@aria-label,"Toggle recording")]')
    record_button.click()
    time.sleep(1)
    start_button = driver.find_element(By.XPATH, '//button[@id="modal-dialog-ok-button"]')
    start_button.click()
    time.sleep(5)
    # Depending on the network speed and other factors, you may need to adjust the waiting time.
    # driver.quit()
    
    # Close the WebDriver and stop the FFmpeg recording
    ffmpeg_process.terminate()

    driver.quit()
    

from sys import argv
if __name__ ==  '__main__':
    joinAsBot(argv[1], argv[2])



