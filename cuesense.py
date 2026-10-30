# CueSense - Audio Transcription and Cue Detection

from faster_whisper import WhisperModel
import string
import csv

from rapidfuzz import fuzz

# import string used to normalize text by converting to lowercase and removing punctuation
# import csv to record audio file, transcription, and cue detected

# 3 cue lines and corresponding actions
cues = {
    "wait i think i heard something just now": "FOOTSTEPS",
    "theres no turning back now": "CURTAIN CLOSE",
    "something strange is going on up there": "LIGHTS PURPLE"
}

# Compare a transcript against the cue lines using fuzzy matching
def fuzzy_match(transcript, threshold=90):
    # Return no cue if the transcript is empty
    if not transcript:
        return "NONE", 0

    best_score = 0
    best_cue = "NONE"
    tie = False

    # Compare the transcript against each cue line
    for cue_line, cue_action in cues.items():
        score = fuzz.ratio(transcript, cue_line)

        if score > best_score:
            best_score = score
            best_cue = cue_action
            tie = False
        elif score == best_score:
            tie = True

    # Only accept a cue if its score meets the threshold
    if best_score < threshold or tie:
        return "NONE", best_score

    return best_cue, best_score

# Load the speech recognition model
# tiny.en small model designed for English speech
model = WhisperModel("tiny.en", device="cpu", compute_type="int8")

# List of audio recordings to process
audio_files = [
    "cue01.wav",
    "cue02.wav",
    "cue03.wav",
    "nocue01.wav",
    "nocue02.wav",
    "nocue03.wav"
]

# Process each recording and save the results
with open("event_log.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["clip_id", "transcript", "exact_cue", "fuzzy_80", "fuzzy_90", "fuzzy_95", "fuzzy_score"])

    for audio_file in audio_files:
        # Transcribe recording
        segments, info = model.transcribe(audio_file, language="en")

        # Combine recognized speech into 1 string
        transcript = " ".join(segment.text.strip() for segment in segments)

        # Normalize transcript
        normalized_transcript = transcript.lower().translate(str.maketrans("", "", string.punctuation))
        normalized_transcript = " ".join(normalized_transcript.split())

        # Exact matching - check if transcript matches a cue line
        if normalized_transcript in cues:
            exact_cue = cues[normalized_transcript]
        else:
            exact_cue = "NONE"

        # Fuzzy matching with 3 diff. thresholds
        fuzzy_cue_80, fuzzy_score = fuzzy_match(normalized_transcript, 80)
        fuzzy_cue_90, _ = fuzzy_match(normalized_transcript, 90)
        fuzzy_cue_95, _ = fuzzy_match(normalized_transcript, 95)

        # Display the results
        # Note similarity score will be the same regardless of threshold
        print("Exact matching:", exact_cue)
        print("Fuzzy matching (80):", fuzzy_cue_80)
        print("Fuzzy matching (90):", fuzzy_cue_90)
        print("Fuzzy matching (95):", fuzzy_cue_95)
        print("Best similarity score:", round(fuzzy_score, 2))

        # Save to event log (separate rows)
        clip_id = audio_file.replace(".wav", "")
        writer.writerow([clip_id, transcript, exact_cue, fuzzy_cue_80, fuzzy_cue_90, fuzzy_cue_95, round(fuzzy_score, 2)])

        print("Audio file:", audio_file)
        print("Transcription:", transcript)
        print("------------------------------")

print("All results saved to event_log.csv")