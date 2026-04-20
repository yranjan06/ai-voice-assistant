# Voice AI Agent

A voice controlled local AI agent that accepts audio input, classifies user intent, executes tools, and displays results in a clean UI.

## Architecture

    Audio Input (mic / upload)
           |
       STT - Groq Whisper API
           |
    3-Tier Intent Classifier
      Tier 1: Regex  - instant, 0 API cost
      Tier 2: Keywords - fast scoring
      Tier 3: LLM fallback - Groq Llama 3.3
           |
    Tool Executor
      file_ops.py   - create file/folder in output/
      code_gen.py   - generate + save code
      summarizer.py - summarize text
      chat.py       - general conversation
      web_search.py - search web using DuckDuckGo
           |
    Session Memory - injects last 3 turns into LLM context
           |
    Gradio UI (4 panels + session history)

## Why Groq API instead of local models

Running whisper-large-v3 locally requires 8GB+ VRAM. My machine (MacBook Air 2017) cannot run it at acceptable latency. Groq provides the same Whisper model via API with sub-2s response time. Similarly, running Llama 3.3 70B locally is not feasible on this hardware.

Switching to local models would require changing only `stt.py` and `llm.py` - the rest of the pipeline stays the same.

## Setup

1. Clone the repo

        git clone https://github.com/yranjan06/ai-voice-assistant.git
        cd ai-voice-assistant

2. Create and activate virtual environment

        python -m venv venv
        source venv/bin/activate

3. Install dependencies

        pip install -r requirements.txt

4. Configure environment

        cp .env.example .env
        # add your GROQ_API_KEY in .env

5. Run the app

        python app.py
        # open http://localhost:7860

## Running Tests

    python tests/test_intent.py

## Supported Intents

| Intent       | Example                                 | Classifier Tier |
|--------------|-----------------------------------------|-----------------|
| create_file  | "create a file called notes.txt"        | Regex           |
| write_code   | "write a python function for fibonacci" | Keyword         |
| summarize    | "summarize this paragraph"              | Regex           |
| web_search   | "search for machine learning trends"    | Regex           |
| general_chat | "what is machine learning"              | LLM fallback    |

## Safety

All file operations are restricted to the `output/` directory. Path traversal attempts like `../../etc/passwd` are blocked using `os.path.basename`.

## Challenges Faced

- **Groq model deprecation**: llama3-70b-8192 was decommissioned mid-development, switched to llama-3.3-70b-versatile
- **Intent classifier false positives**: overlapping keywords (csv matched both create_file and write_code), fixed by refining keyword lists
- **STT accuracy with accents**: Whisper occasionally misinterprets words, e.g. "machine" transcribed as "muscle"
- **ffmpeg build time on older macOS**: no pre-built bottles available for macOS 12, had to compile from source


## Bonus Features

- **Compound Commands**: supports multiple intents in one command, e.g. "create a file and write a python function for hello world" detects both create_file + write_code and executes sequentially
- **Human-in-the-Loop**: file operations (create_file, write_code) show Confirm/Cancel buttons before execution
- **Session Memory**: maintains last 10 turns of conversation history, injects context into LLM for better responses
- **Graceful Degradation**: errors at any stage (audio, STT, intent, tools) are caught and shown in UI without crashing

## Project Structure

    app.py              - gradio ui entry point
    agent.py            - pipeline orchestrator
    stt.py              - groq whisper stt
    intent.py           - 3-tier intent classifier
    llm.py              - groq llama wrapper
    memory.py           - session history
    tools/file_ops.py   - file creation
    tools/code_gen.py   - code generation
    tools/summarizer.py - text summarization
    tools/chat.py       - general chat
    tools/web_search.py - web search
    utils/audio.py      - audio format conversion
    output/             - sandboxed output folder
    tests/test_intent.py - intent tests