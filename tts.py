import time
from xml.etree import ElementTree

import requests

try:
    input = raw_input
except NameError:
    pass


class TextToSpeech(object):
    def __init__(self, subscription_key):
        self.subscription_key = subscription_key
        self.access_token = None
        self.start = None
        self.end = None
        self.list = None

    def create_array(self):
        self.list = list(range(self.start, (self.end+1)))

    def get_token(self):
        fetch_token_url = "https://australiaeast.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def save_audio(self):
        base_url = 'https://australiaeast.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'audio-24khz-96kbitrate-mono-mp3',
            'User-Agent': 'ZFRCognitiveServicesResource'
        }
        for num in self.list:
            tts = str(num).zfill(3)
            xml_body = ElementTree.Element('speak', version='1.0')
            xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
            voice = ElementTree.SubElement(xml_body, 'voice')
            voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
            voice.set(
                'name', 'Microsoft Server Speech Text to Speech Voice (en-US, JessaNeural)'
            )
            prosody = ElementTree.SubElement(voice, 'prosody')
            prosody.set('rate', 'slow')
            say_as = ElementTree.SubElement(prosody, 'say-as')
            say_as.set('interpret-as', 'number_digit')
            say_as.text = tts
            # voice.text = self.tts
            body = ElementTree.tostring(xml_body)

            response = requests.post(constructed_url, headers=headers, data=body)
            if response.status_code == 200:
                with open(tts + '.mp3', 'wb') as audio:
                    audio.write(response.content)
                    print("\nStatus code: " + str(response.status_code) +
                    "\nYour TTS is ready for playback. \n")
            else:
                print("\nStatus code: " + str(response.status_code) +
                      "\nSomething went wrong. Check your subscription key and headers. \n")
            time.sleep(1)


if __name__ == '__main__':
    subscription_key = "b4ac853966194099b8fe88c449eb34f2"
    app = TextToSpeech(subscription_key)
    app.get_token()
    app.start = int(input("Start number? "))
    app.end = int(input("End number? "))
    app.create_array()
    app.save_audio()

