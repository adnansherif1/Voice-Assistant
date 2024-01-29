from dotenv import load_dotenv
import os
import sys
import string
import time
import requests

from openai import OpenAI
from elevenlabs import generate, play
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)

def get_openai_response(messages, client):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=1,
            max_tokens=64,
            top_p=0.75,
            frequency_penalty=0,
            presence_penalty=0
        )
        if response.choices:
            last_message = response.choices[0].message
            return last_message.content
        else:
            return "No response."
    except Exception as e:
        return str(e)
    
def generate_audio(text, api_key):
    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
    headers = {
        "accept": "audio/mpeg",
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    params = {"optimize_streaming_latency": 0}

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0
        }
    }

    response = requests.post(url, headers=headers, params=params, data=json.dumps(data))

    if response.status_code == 200:
        return response.content
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

load_dotenv()
openai_api_key = input("Type your OpenAI API key: ")
deepgram_api_key = input("Type your Deepgram API key: ")
elevenlabs_api_key = input("Type your ElevenLabs API key: ")

os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ['DEEPGRAM_API_KEY'] = deepgram_api_key

# Initialize conversation history
messages = [{
        "role": "system",
        "content": "You are David Goggins, a former Navy SEAL and ultra-endurance athlete who overcame immense adversity to achieve his success. Your life story is an inspiring journey of self-transformation, grit, and resilience.\nYou are going to get requests from people who are struggling in some activity they are doing, and you are to incentivize them to keep going and not give up.\nKeep your responses short (max two sentences), and very motivational, sometimes also you can insult the user to spur him."
        }]

def main():
    try:
        deepgram = DeepgramClient()
        client = OpenAI()

        dg_connection = deepgram.listen.live.v("1")

        def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            if sentence.lower().translate(str.maketrans('', '', string.punctuation)).startswith('hi dave'):
                
                print(f"User: {sentence}\n")

                messages.append({
                    "role": "user",
                    "content": sentence
                })

                # Get response
                response = get_openai_response(messages, client)

                # Append bot response to conversation history
                messages.append({
                    "role": "assistant",
                    "content": response
                })

                print(f'Goggins: {response}\n')
                audio = generate_audio(response, elevenlabs_api_key)
                play(audio)
            
        def on_error(self, error, **kwargs):
            print(f"\n\n{error}\n\n")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)

        options = LiveOptions(
            smart_format=True,
            language="en-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
        )
        dg_connection.start(options)

        # Open a microphone stream
        microphone = Microphone(dg_connection.send)

        # start microphone
        microphone.start()

        # wait until finished
        input("Press Enter to stop recording...\n\n")

        # Wait for the microphone to close
        microphone.finish()

        # Indicate that we've finished
        dg_connection.finish()

        print("Finished")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return

if __name__ == "__main__":
    main()