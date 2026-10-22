# CueSense

CueSense is a senior project prototype that uses speech recognition to identify specific lines of dialogue and trigger simulated theatrical cues (e.g., sound, lighting, or curtain actions).

**Note:** The project currently uses prerecorded audio files, not live microphone input.

## How It Works Currently

1. The program loads prerecorded audio files (WAV files for this project)
2. Faster-whisper transcribes the speech into text
3. The transcription is normalized by removing punctuation and converting text to lowercase
4. The normalized transcription is then compared against 3 predefined cue lines using exact matching
5. The program prints the detected cue or `NO CUE` and saves the results to a CSV event log

## Requirements

- Python 3.12
- faster-whisper
- WAV audio recordings

## To Run

1. Download/clone the repository
2. Open Command Prompt and navigate to the CueSense project folder
3. Create and activate a virtual environment:

   ```bat
   python -m venv .venv
   .venv\Scripts\activate.bat
   ```

4. Install faster-whisper:

   ```bat
   python -m pip install faster-whisper
   ```

5. Make sure the following audio files are in the project folder:

   - `cue01.wav`
   - `cue02.wav`
   - `cue03.wav`
   - `nocue01.wav`
   - `nocue02.wav`
   - `nocue03.wav`

6. Run the program:

   ```bat
   python cuesense.py
   ```

The program displays the transcription and cue decision for each recording. It also creates `event_log.csv`, which contains the clip ID, transcript, and detected cue.

**Note:** As of the moment, running the program again overwrites the previous CSV log.

## Files

- `cue_matcher.py` - Initial text-only cue matcher
- `transcribe_audio.py` - Initial speech recognition test
- `cuesense.py` - Current main program