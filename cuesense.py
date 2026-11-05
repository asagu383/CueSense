# CueSense - Audio Transcription and Cue Detection

from faster_whisper import WhisperModel
import string
import csv
import time

from rapidfuzz import fuzz

# import string used to normalize text by converting to lowercase and removing punctuation
# import csv to record audio file, transcription, and cue detected

# 3 cue lines and corresponding actions
cues = {
    "wait i think i heard something just now": "FOOTSTEPS",
    "theres no turning back now": "CURTAIN CLOSE",
    "something strange is going on up there": "LIGHTS PURPLE"
}

# Map cue actions to cue IDs for evaluation
cue_ids = {
    "FOOTSTEPS": "C01",
    "CURTAIN CLOSE": "C02",
    "LIGHTS PURPLE": "C03",
    "NONE": "NONE"
}

# Load expected labels for the recordings
clip_labels = {}

with open("clip_labels.csv", "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        clip_labels[row["clip_id"]] = row


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

# Ask the user which dataset to process
dataset = input("Choose dataset (development/test): ").strip().lower()

# Development recordings
development_files = [
    "cue01.wav",
    "cue02.wav",
    "cue03.wav",
    "nocue01.wav",
    "nocue02.wav",
    "nocue03.wav"
]

# Held-out test recordings
test_files = [
    "test_cue01a.wav",
    "test_cue01b.wav",
    "test_cue02a.wav",
    "test_cue02b.wav",
    "test_cue03a.wav",
    "test_cue03b.wav",
    "test_nocue01.wav",
    "test_nocue02.wav",
    "test_nocue03.wav",
    "test_nocue04.wav",
    "test_nocue05.wav",
    "test_nocue06.wav"
]

# Prompt to select the appropriate recordings
if dataset == "development":
    audio_files = development_files
    output_file = "development_log.csv"
elif dataset == "test":
    audio_files = test_files
    output_file = "test_log.csv"
else:
    raise ValueError("Please enter 'development' or 'test'.")

# Process each recording and save the results
with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    writer.writerow([
    "clip_id",
    "split",
    "condition",
    "intended_text",
    "expected_cue",
    "asr_text",
    "method",
    "threshold",
    "score",
    "predicted_cue",
    "processing_seconds"
    ])

    for audio_file in audio_files:
        # Start timing this recording
        start_time = time.perf_counter()

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

        # Fuzzy matching using the selected threshold of 90
        fuzzy_cue, fuzzy_score = fuzzy_match(normalized_transcript)

        # Convert detected actions to cue IDs
        exact_cue_id = cue_ids[exact_cue]
        fuzzy_cue_id = cue_ids[fuzzy_cue]

        # Calculate processing time in seconds
        processing_time = time.perf_counter() - start_time

        # Display the results
        print("Exact matching:", exact_cue)
        print("Exact cue ID:", exact_cue_id)
        print("Fuzzy matching (90):", fuzzy_cue)
        print("Fuzzy cue ID:", fuzzy_cue_id)
        print("Best similarity score:", round(fuzzy_score, 2))
        print("Processing time:", round(processing_time, 3), "seconds")

        # Save results to event log
        clip_id = audio_file.replace(".wav", "")
        label = clip_labels[clip_id]

        # Exact matching result
        writer.writerow([
            clip_id,
            label["split"],
            "clean",
            label["intended_text"],
            label["expected_cue"],
            transcript,
            "exact",
            "N/A",
            "N/A",
            exact_cue_id,
            round(processing_time, 3)
        ])

        # Fuzzy matching result
        writer.writerow([
            clip_id,
            label["split"],
            "clean",
            label["intended_text"],
            label["expected_cue"],
            transcript,
            "fuzzy",
            90,
            round(fuzzy_score, 2),
            fuzzy_cue_id,
            round(processing_time, 3)
        ])

        print("Audio file:", audio_file)
        print("Transcription:", transcript)
        print("------------------------------")

print("All results saved to", output_file)