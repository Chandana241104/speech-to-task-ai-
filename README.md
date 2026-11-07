# Speech-to-Task AI

A lightweight Python project that converts spoken audio into structured task data. The workflow is:

1. Transcribe speech from an audio file
2. Extract tasks from the transcript using a local LLM
3. Save the results as JSON

This project is designed for local execution and uses open-source components, including `faster-whisper` for transcription and `Ollama` with `tinyllama` for task extraction.

## Project purpose

The script listens for spoken instructions or notes and turns them into a machine-readable list of tasks, each with:

- task description
- category
- frequency
- start time
- end time

This makes it useful for turning meeting notes, voice reminders, or spoken planning input into structured task records.

## File overview

- `speech_task_agent.py` — main application logic
- `requirements.txt` — required Python dependencies
- `sample.wav` — example audio input file
- `output.json` — generated result after running the script
- `.gitignore` — project ignore rules

## How it works

### 1. Audio preprocessing
The script reads an audio file using `pydub`, converts it to mono audio at 16kHz, and saves a temporary WAV file.

### 2. Speech transcription
It uses `faster_whisper.WhisperModel("base", compute_type="int8")` to transcribe the WAV audio into text.

### 3. Task extraction
The transcript is sent to a LangChain prompt that instructs the LLM to output valid JSON in a specific schema. The script uses Ollama with the `tinyllama` model.

### 4. Output generation
The extracted tasks are written to `output.json` as a JSON array.

## Example output

The script expects the model to return data like this:

```json
[
  {
    "task": "Schedule a meeting with the team",
    "category": "planning",
    "frequency": null,
    "start_time": null,
    "end_time": null
  }
]
```

## Requirements

Python 3.9+ is recommended.

Install dependencies:

```bash
pip install -r requirements.txt
```

Dependencies include:

- `faster-whisper`
- `langchain`
- `pydub`
- `python-dotenv`

## Local LLM setup

This project uses Ollama locally. Before running the script, make sure Ollama is installed and the `tinyllama` model is available.

Example:

```bash
ollama pull tinyllama
```

Then ensure the Ollama service is running locally so the script can connect to it.

## Usage

Run the script from the project root:

```bash
python speech_task_agent.py
```

By default, it looks for:

```bash
sample.wav
```

If the file exists, it processes it and saves the JSON result to:

```bash
output.json
```

## Notes

- The script currently expects a file named `sample.wav` in the project directory.
- It writes a temporary file named `temp.wav` during processing.
- The generated JSON depends on the quality of the speech transcription and the local language model output.

## License

This project does not currently include a license file. Add one if you plan to distribute or publish the repository publicly.

## Future improvements

Potential enhancements include:

- support for multiple audio files or directories
- better parsing of times and frequencies
- command-line arguments for input/output paths
- improved fallback handling when the LLM returns invalid JSON
- packaging as a CLI tool or API service

## Summary

Speech-to-Task AI is a simple local pipeline for turning voice recordings into structured tasks. It combines speech recognition and generative AI to transform human speech into task data suitable for automation and productivity workflows.
