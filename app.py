import os
import gradio as gr
from gradio.themes import Soft
import time

# Import your existing functions
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

# Direct API keys implementation
GROQ_API_KEY = "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"
ELEVENLABS_API_KEY = "sk_2a0f49fb03a7ee81c8d28740d2485d5fe21251b739b73550"

# Audio output directory setup
AUDIO_DIR = "/app/audio_output"
os.makedirs(AUDIO_DIR, exist_ok=True)

system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
What's in this image?. Do you find anything wrong with it medically? 
If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
Donot say 'In the image I see' but say 'With what I see, I think you have ....'
Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def process_inputs(audio_filepath, image_filepath):
    # Check if audio was provided
    if audio_filepath is None:
        return "No audio provided", "Please record or upload audio first", None
    
    try:
        # Speech to text
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=GROQ_API_KEY, 
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )

        # Prepare the full query
        full_query = f"{system_prompt}\nPatient says: {speech_to_text_output}"
        
        # Handle the image input
        if image_filepath:
            doctor_response = analyze_image_with_query(
                query=full_query,
                encoded_image=encode_image(image_filepath)
            )
        else:
            doctor_response = "No image provided for me to analyze"

        # Generate audio output
        output_path = os.path.join(AUDIO_DIR, "final.mp3")
        voice_of_doctor = text_to_speech_with_elevenlabs(
            input_text=doctor_response, 
            output_filepath=output_path
        ) 

        return speech_to_text_output, doctor_response, output_path
    
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        return error_msg, error_msg, None

# Custom medical theme
med_theme = Soft(
    primary_hue="teal",
    secondary_hue="blue",
    neutral_hue="stone",
    font=[gr.themes.GoogleFont("Poppins")]
)

# Custom CSS for medical UI
custom_css = """
:root {
    --primary: #0d9488;
    --secondary: #0891b2;
}
.gradio-container {
    background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%) !important;
    font-family: 'Poppins', sans-serif;
}
.header {
    text-align: center;
    padding: 20px;
    background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
    color: white;
    border-radius: 12px;
    margin-bottom: 24px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.diagnosis-box {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    border-left: 4px solid var(--primary);
}
.audio-box {
    background: #f8fafc;
    border-radius: 12px;
    padding: 15px;
    border: 1px solid #e2e8f0;
}
.consult-panel {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}
footer {
    text-align: center;
    margin-top: 20px;
    font-size: 0.9em;
    color: #64748b;
}
button {
    transition: all 0.3s ease !important;
}
button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 12px rgba(0,0,0,0.1) !important;
}
"""

# Create the enhanced interface
with gr.Blocks(theme=med_theme, css=custom_css, title="MediScan AI") as app:
    with gr.Column():
        gr.Markdown("""
        <div class="header">
            <h1 style="margin-bottom: 8px;">🩺 MediScan AI</h1>
            <p style="opacity: 0.9; margin: 0;">AI-powered medical symptom analysis</p>
        </div>
        """)
        
        gr.Markdown("""
        ## User Guide 📖
        
        <div style="background: #f8fafc; padding: 16px; border-radius: 8px; border-left: 4px solid #0d9488; margin-bottom: 24px;">
        <h3 style="margin-top: 0;">How to use MediScan AI:</h3>
        <ol>
            <li><b>Record or upload</b> your symptoms using the microphone or file upload</li>
            <li><b>Image:</b> Upload any medical images (X-rays, skin conditions, etc.)</li>
            <li>Click <b>Analyze Symptoms</b> to get your diagnosis</li>
            <li>View the text analysis and listen to the doctor's voice response</li>
            <li>Use <b>Clear</b> to start a new consultation</li>
        </ol>
        
        <h4>Tips for best results:</h4>
        <ul>
            <li>Speak clearly when describing symptoms</li>
            <li>Use good lighting for medical images</li>
            <li>Keep descriptions concise (30 seconds or less)</li>
        </ul>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1, elem_classes=["consult-panel"]):
                gr.Markdown("### Patient Consultation")
                audio_input = gr.Audio(
                    sources=["microphone", "upload"],
                    type="filepath",
                    label="Record or Upload Symptoms",
                    elem_classes=["audio-box"]
                )
                image_input = gr.Image(
                    type="filepath",
                    label="Upload Medical Image",
                    height=200
                )
                with gr.Row():
                    clear_btn = gr.Button("Clear", variant="secondary")
                    submit_btn = gr.Button(
                        "Analyze Symptoms", 
                        variant="primary",
                        size="lg"
                    )
            
            with gr.Column(scale=1):
                gr.Markdown("### Diagnosis Results")
                with gr.Group():
                    speech_text = gr.Textbox(
                        label="Patient Description",
                        interactive=False,
                        lines=3,
                        placeholder="Your described symptoms will appear here..."
                    )
                with gr.Group():
                    diagnosis = gr.Textbox(
                        label="Doctor's Analysis",
                        interactive=False,
                        elem_classes=["diagnosis-box"],
                        lines=5,
                        placeholder="The AI doctor's analysis will appear here..."
                    )
                audio_output = gr.Audio(
                    label="Doctor's Voice Response",
                    autoplay=True,
                    elem_classes=["audio-box"],
                    visible=True
                )
        
        gr.Markdown("""
        <footer>
            <small>Note: This AI assistant is for educational purposes only. 
            Always consult a qualified healthcare professional for medical advice.</small>
        </footer>
        """)
    
    # Connect the functionality
    submit_btn.click(
        lambda: [gr.Button(interactive=False), gr.Textbox(value="Analyzing...")],
        outputs=[submit_btn, diagnosis]
    ).then(
        fn=process_inputs,
        inputs=[audio_input, image_input],
        outputs=[speech_text, diagnosis, audio_output]
    ).then(
        lambda: gr.Button(interactive=True),
        outputs=[submit_btn]
    )
    
    # Clear button functionality
    clear_btn.click(
        lambda: [None, None, "", "", None],
        outputs=[audio_input, image_input, speech_text, diagnosis, audio_output]
    )

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        favicon_path=None,  
        share=False
    )
