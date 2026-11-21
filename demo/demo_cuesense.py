# CueSense - Prerecorded Audio Demo
# Separate from the frozen evaluation

from pathlib import Path
import string
import sys

from faster_whisper import WhisperModel
from rapidfuzz import fuzz
from demo_helpers import play_cue

# Same cue lines and actions as the original CueSense script
cues = {
    "wait i think i heard something just now": "FOOTSTEPS",
    "theres no turning back now": "CURTAIN CLOSE",
    "something strange is going on up there": "LIGHTS PURPLE"
}

# Map cue actions to cue IDs
cue_ids = {
    "FOOTSTEPS": "C01",
    "CURTAIN CLOSE": "C02",
    "LIGHTS PURPLE": "C03",
    "NONE": "NONE"
}


# Same fuzzy matching logic as the original script
def fuzzy_match(transcript, threshold=90):
    if not transcript:
        return "NONE", 0

    best_score = 0
    best_cue = "NONE"
    tie = False

    for cue_line, cue_action in cues.items():
        score = fuzz.ratio(transcript, cue_line)

        if score > best_score:
            best_score = score
            best_cue = cue_action
            tie = False
        elif score == best_score:
            tie = True

    if best_score < threshold or tie:
        return "NONE", best_score

    return best_cue, best_score


# Choose one prerecorded WAV file
if len(sys.argv) != 2:
    raise SystemExit("Usage: python demo_cuesense.py path_to_audio.wav")

audio_file = Path(sys.argv[1])

if not audio_file.is_file():
    raise SystemExit(f"Audio file not found: {audio_file}")

# Load the same ASR model and settings
model = WhisperModel("tiny.en", device="cpu", compute_type="int8")

# Transcribe and combine all speech segments
segments, info = model.transcribe(str(audio_file), language="en")
transcript = " ".join(segment.text.strip() for segment in segments)

# Normalize the transcript exactly as in the original script
normalized_transcript = transcript.lower().translate(
    str.maketrans("", "", string.punctuation)
)
normalized_transcript = " ".join(normalized_transcript.split())

# Make one final fuzzy-matching decision
fuzzy_cue, fuzzy_score = fuzzy_match(normalized_transcript)
accepted_cue_id = cue_ids[fuzzy_cue]

print("Audio file:", audio_file.name)
print("Transcription:", transcript)
print("Fuzzy matching (90):", fuzzy_cue)
print("Fuzzy cue ID:", accepted_cue_id)
print("Best similarity score:", round(fuzzy_score, 2))

# Call the playback helper once, after the final decision
play_cue(accepted_cue_id)
