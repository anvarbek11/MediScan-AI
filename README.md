# 🩺 MediScan AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

AI-powered medical consultation system that analyzes symptoms through voice and image inputs, providing doctor-like responses.

![finalllm1](https://github.com/user-attachments/assets/d7756356-5960-4df8-bbec-cd2d1a1152a7)
![finalllm2](https://github.com/user-attachments/assets/99f7d31a-4cd4-4215-8688-cd6ea4007e00)
## DEMO LINK 
https://huggingface.co/spaces/Anvarbekk/mybot

## Features ✨

- **Voice Symptom Analysis** 🎤
  - Real-time audio recording/upload
  - Whisper-large-v3 transcription via Groq
- **Medical Image Analysis** 🖼️
  - Multimodal diagnosis with Llama-4-scout
  - Base64 image processing
- **Doctor Voice Response** 🗣️
  - ElevenLabs AI voice (Aria)
  - gTTS fallback option
- **Professional UI** 💻
  - Gradio web interface
  - Medical-themed design

## Installation ⚙️

```bash
# Clone repository
git clone https://github.com/anvarbek11/MediScan-AI.git
cd MediScan-AI

# Install dependencies
pip install -r requirements.txt
```

## Configuration 🔧

1. Get API keys:
   - [Groq Cloud](https://console.groq.com/)
   - [ElevenLabs](https://elevenlabs.io/)

2. Create `.env` file:
```ini
GROQ_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
AUDIO_OUTPUT_DIR=./audio_output
```

## Usage 🚀

```bash
python app.py
```
Access the web interface at `http://localhost:7860`

## Project Structure 📂

```
MediScan-AI/
├── app.py               # Main Gradio application
├── brain_of_the_doctor.py # Image analysis module
├── voice_of_the_doctor.py # TTS response system
├── voice_of_the_patient.py # STT processing
├── requirements.txt     # Dependencies
├── .gitignore
└── README.md
```

## License 📜

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
---
📌 **Author**: Anvarbek Kuziboev  
📄 **Note**: This project is part of my personal portfolio.  
🚫 Unauthorized copying or use without attribution is not permitted.

