from elevenlabs import generate
import os
import requests
import json

def generate_audio(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/h4tndIlIAkgh2fsjWL6Z"
    headers = {
        "accept": "audio/mpeg",
        "xi-api-key": os.environ["eleven_api_key"],
        "Content-Type": "application/json"
    }
    params = {"optimize_streaming_latency": 0}

    data = {
        "text": text,
        "model_id": "eleven_turbo_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.2,
            "use_speaker_boost": True
        }
    }

    response = requests.post(url, headers=headers, params=params, data=json.dumps(data))

    if response.status_code == 200:
        return response.content
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

starting_lines = [
    "Wake up buddy!",
    "Com'on motherfucker!",
    "You're so weak!"
]

ending_lines = [
    "Who's gonna carry the boat!",
    "They don't know you son!",
    "Stay hard!"
]

for i, line in enumerate(starting_lines):
    audio = generate_audio(line)

    with open(f'audio/start/{i}.mp3', 'wb') as file:
        file.write(audio)

for i, line in enumerate(ending_lines):
    audio = generate_audio(line)

    with open(f'audio/end/{i}.mp3', 'wb') as file:
        file.write(audio)