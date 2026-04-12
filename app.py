import gradio as gr
from dotenv import load_dotenv
from agent import run, get_history

load_dotenv()

def process_audio(audio_path):
    if audio_path is None:
        return "no audio provided.", "—", "—", "please record or upload audio.", []
    r = run(audio_path)
    history = [[h["user"][:60], h["intent"]] for h in get_history()]
    return (
        r.get("transcription") or "—",
        f"{r.get('intent') or '—'} [{r.get('confidence', '')}]",
        r.get("action") or "—",
        r.get("output") or "—",
        history,
    )

with gr.Blocks(title="Voice Agent") as demo:
    gr.Markdown("# Voice AI Agent")
    gr.Markdown("Speak or upload audio. The agent transcribes, classifies intent, and acts.")

    with gr.Row():
        audio_input = gr.Audio(sources=["microphone", "upload"], type="filepath", label="Audio Input")
        run_btn = gr.Button("Run Agent", variant="primary", size="lg")

    with gr.Row():
        transcription_box = gr.Textbox(label="Transcribed Text", interactive=False)
        intent_box = gr.Textbox(label="Detected Intent", interactive=False)

    with gr.Row():
        action_box = gr.Textbox(label="Action Taken", interactive=False)
        output_box = gr.Textbox(label="Final Output", interactive=False, lines=10)

    with gr.Accordion("Session History", open=False):
        history_table = gr.Dataframe(headers=["Input", "Intent"], interactive=False)

    run_btn.click(
        fn=process_audio,
        inputs=[audio_input],
        outputs=[transcription_box, intent_box, action_box, output_box, history_table],
    )

if __name__ == "__main__":
    demo.launch()