import gradio as gr
from dotenv import load_dotenv
from stt import transcribe
from utils.audio import convert_to_wav

load_dotenv()

def process_audio(audio_path):
    if audio_path is None:
        return "no audio provided. please record or upload."
    try:
        wav = convert_to_wav(audio_path)
        text = transcribe(wav)
        return text if text else "could not transcribe. try speaking clearly."
    except Exception as e:
        return f"error: {e}"

with gr.Blocks(title="Voice Agent") as demo:
    gr.Markdown("# Voice Agent — Phase 1")
    audio_input = gr.Audio(
        sources=["microphone", "upload"],
        type="filepath",
        label="Audio Input"
    )
    run_btn = gr.Button("Transcribe", variant="primary")
    output_box = gr.Textbox(label="Transcribed Text", interactive=False, lines=4)

    run_btn.click(fn=process_audio, inputs=[audio_input], outputs=[output_box])

if __name__ == "__main__":
    demo.launch()