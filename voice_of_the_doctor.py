import os
from gtts import gTTS

import os

# Audio directories configuration
AUDIO_DIR = os.getenv('AUDIO_OUTPUT_DIR', '/app/audio_output')
os.makedirs(AUDIO_DIR, exist_ok=True)
TEMP_DIR = os.getenv('TEMP_AUDIO_DIR', '/tmp/audio_cache')
os.makedirs(TEMP_DIR, exist_ok=True)

# Then continue with your existing code...

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language="en"
    full_path = os.path.join(AUDIO_DIR, output_filepath)
    
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(full_path)

input_text="Hi this is Ai with Hassan!"
# text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")

#Step1b: Setup Text to Speech–TTS–model with ElevenLabs
import elevenlabs
from elevenlabs.client import ElevenLabs

# Direct API key implementation
ELEVENLABS_API_KEY = "yourapi"

def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    full_path = os.path.join(AUDIO_DIR, output_filepath)
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio=client.generate(
        text= input_text,
        voice= "Aria",
        output_format= "mp3_22050_32",
        model= "eleven_turbo_v2"
    )
    elevenlabs.save(audio, full_path)

#text_to_speech_with_elevenlabs_old(input_text, output_filepath="elevenlabs_testing.mp3") 

#Step2: Use Model for Text output to Voice
import subprocess
import platform

def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"
    full_path = os.path.join(AUDIO_DIR, output_filepath)

    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(full_path)
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', full_path])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{full_path}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', full_path])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    full_path = os.path.join(AUDIO_DIR, output_filepath)
    try:
        client = ElevenLabs(api_key="yorapi")
        audio = client.generate(
            text=input_text,
            voice="Aria",
            output_format="mp3_22050_32",
            model="eleven_turbo_v2"
        )
        elevenlabs.save(audio, full_path)
        return full_path
    except Exception as e:
        print(f"ElevenLabs Error: {str(e)} - Falling back to gTTS")
        return text_to_speech_with_gtts(input_text, output_filepath)
