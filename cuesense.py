# CueSense - Audio Transcription and Cue Detection

from faster_whisper import WhisperModel
import string
import csv

# import string used to normalize text by converting to lowercase and removing punctuation
# import csv to record audio file, transcription, and cue detected

# 3 cue lines and corresponding actions
cues = {
    "wait i think i heard something just now": "FOOTSTEPS",
    "theres no turning back now": "CURTAIN CLOSE",
    "something strange is going on up there": "LIGHTS PURPLE"
}

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
    writer.writerow(["clip_id", "transcript", "detected_cue"])

    for audio_file in audio_files:
        # Transcribe recording
        segments, info = model.transcribe(audio_file, language="en")

        # Combine recognized speech into 1 string
        transcript = " ".join(segment.text.strip() for segment in segments)

        # Normalize transcript
        normalized_transcript = transcript.lower().translate(str.maketrans("", "", string.punctuation)).strip()

        # Check if transcript matches a cue line
        if normalized_transcript in cues:
            detected_cue = cues[normalized_transcript]
            print("Cue detected:", detected_cue)
        else:
            detected_cue = "NONE"
            print("NO CUE")

        # Save to event log (separate rows)
        clip_id = audio_file.replace(".wav", "")
        writer.writerow([clip_id, transcript, detected_cue])

        print("Audio file:", audio_file)
        print("Transcription:", transcript)
        print("------------------------------")

print("All results saved to event_log.csv")