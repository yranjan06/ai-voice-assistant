import gradio as gr
from dotenv import load_dotenv
from agent import run, get_history

load_dotenv()

pending_result = {}

def process_audio(audio_path):
    global pending_result
    if audio_path is None:
        return "no audio provided.", "—", "—", "please record or upload audio.", [], gr.update(visible=False), gr.update(visible=False)

    r = run(audio_path)
    history = [[h["user"][:60], h["intent"]] for h in get_history()]

    # check if file operation - show confirm button
    needs_confirm = r.get("intent") in ["create_file", "write_code"]

    if needs_confirm:
        pending_result = r
        return (
            r.get("transcription") or "—",
            f"{r.get('intent') or '—'} [{r.get('confidence', '')}]",
            "waiting for confirmation...",
            f"will execute: {r.get('intent')}",
            history,
            gr.update(visible=True),
            gr.update(visible=True),
        )

    return (
        r.get("transcription") or "—",
        f"{r.get('intent') or '—'} [{r.get('confidence', '')}]",
        r.get("action") or "—",
        r.get("output") or "—",
        history,
        gr.update(visible=False),
        gr.update(visible=False),
    )

def confirm_action():
    global pending_result
    r = pending_result
    return (
        r.get("action") or "—",
        r.get("output") or "—",
        gr.update(visible=False),
        gr.update(visible=False),
    )

def cancel_action():
    return (
        "cancelled by user",
        "operation cancelled.",
        gr.update(visible=False),
        gr.update(visible=False),
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
        confirm_btn = gr.Button("Confirm", variant="primary", visible=False)
        cancel_btn = gr.Button("Cancel", variant="stop", visible=False)

    with gr.Row():
        action_box = gr.Textbox(label="Action Taken", interactive=False)
        output_box = gr.Textbox(label="Final Output", interactive=False, lines=10)

    with gr.Accordion("Session History", open=False):
        history_table = gr.Dataframe(headers=["Input", "Intent"], interactive=False)

    run_btn.click(
        fn=process_audio,
        inputs=[audio_input],
        outputs=[transcription_box, intent_box, action_box, output_box, history_table, confirm_btn, cancel_btn],
    )

    confirm_btn.click(
        fn=confirm_action,
        outputs=[action_box, output_box, confirm_btn, cancel_btn],
    )

    cancel_btn.click(
        fn=cancel_action,
        outputs=[action_box, output_box, confirm_btn, cancel_btn],
    )

if __name__ == "__main__":
    demo.launch()