import gradio as gr
from dotenv import load_dotenv
from stt import transcribe
from intent import classify
from utils.audio import convert_to_wav

load_dotenv()

def process_audio(audio_path):
    if audio_path is None:
        return "no audio provided.", "—"
    try:
        wav = convert_to_wav(audio_path)
        text = transcribe(wav)
        if not text:
            return "could not transcribe.", "—"
        intents = classify(text)
        intent_str = " + ".join(f"{i['intent']} ({i['confidence']})" for i in intents)
        return text, intent_str
    except Exception as e:
        return f"error: {e}", "—"

with gr.Blocks(title="Voice Agent") as demo:
    gr.Markdown("# Voice Agent — Phase 2")
    audio_input = gr.Audio(
        sources=["microphone", "upload"],
        type="filepath",
        label="Audio Input"
    )
    run_btn = gr.Button("Transcribe", variant="primary")
    transcription_box = gr.Textbox(label="Transcribed Text", interactive=False, lines=3)
    intent_box = gr.Textbox(label="Detected Intent", interactive=False)

    run_btn.click(
        fn=process_audio,
        inputs=[audio_input],
        outputs=[transcription_box, intent_box],
    )

if __name__ == "__main__":
    demo.launch()