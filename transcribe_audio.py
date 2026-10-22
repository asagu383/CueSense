
# CueSense - First Audio Transcription

from faster_whisper import WhisperModel

# Load pretrained speech-recognition model
# "tiny.en" - small model designed for English speech
model = WhisperModel("tiny.en", device="cpu", compute_type="int8")

# Transcribe recorded audio file
segments, info = model.transcribe("cue01.wav", language="en")

# Combine recognized speech into 1 string
transcript = " ".join(segment.text.strip() for segment in segments)

# Display transcription
print("Transcription:", transcript)

# Save the actual transcription to a text file
with open("cue01_transcript.txt", "w", encoding="utf-8") as file:
    file.write(transcript)
