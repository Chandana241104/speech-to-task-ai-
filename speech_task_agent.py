import os
import json
from pydub import AudioSegment
from faster_whisper import WhisperModel
from langchain_community.llms import Ollama  # Updated import
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# STEP 1: Transcribe audio using faster-whisper
def transcribe_audio(audio_path: str) -> str:
    print("🔊 Converting audio to WAV format...")
    audio = AudioSegment.from_file(audio_path)
    audio = audio.set_channels(1).set_frame_rate(16000)  # Ensures correct format
    audio.export("temp.wav", format="wav")

    print("📝 Transcribing audio...")
    model = WhisperModel("base", compute_type="int8")
    segments, _ = model.transcribe("temp.wav")
    transcript = " ".join([seg.text.strip() for seg in segments])
    print("📄 Transcript:", transcript)
    return transcript

# STEP 2: Categorize tasks using LangChain + Ollama (tinyllama)
def categorize_tasks(transcript: str) -> list:
    prompt_template = """
You are a helpful AI assistant that extracts structured task information from a natural language sentence.

Input:
"{text}"

Respond only with valid JSON. Do NOT include any explanation, code blocks, or markdown formatting.
Format:
[
  {{
    "task": "<task description>",
    "category": "<category>",
    "frequency": "<frequency or null>",
    "start_time": "<start time or null>",
    "end_time": "<end time or null>"
  }}
]
"""

    print("🧠 Categorizing tasks with LLM...")
    llm = Ollama(model="tinyllama")  # Make sure tinyllama is running
    prompt = PromptTemplate(input_variables=["text"], template=prompt_template)
    chain = LLMChain(llm=llm, prompt=prompt)

    result = chain.invoke({"text": transcript})  # Updated from .run() to .invoke()

    try:
        parsed = result  # Directly use the result as it should be JSON formatted
        print("✅ JSON Output:")
        print(json.dumps(parsed, indent=2))
        return parsed
    except json.JSONDecodeError:
        print("❌ Error: Could not parse model output to JSON.")
        print("Raw output:\n", result)
        return []

# STEP 3: Main flow
if __name__ == "__main__":
    AUDIO_FILE = "sample.wav"

    if not os.path.exists(AUDIO_FILE):
        print(f"⚠️  File '{AUDIO_FILE}' not found. Please place your .wav file in this directory.")
        exit(1)

    transcript = transcribe_audio(AUDIO_FILE)
    categorized_tasks = categorize_tasks(transcript)

    # Save to output.json
    with open("output.json", "w") as f:
        json.dump(categorized_tasks, f, indent=2)

    print("\n🎉 All done! Output saved to output.json")
