
# CueSense - Basic Text-Only Cue Matcher

# 3 predefined cues
cues = {
    "wait i think i heard something just now": "FOOTSTEPS",
    "theres no turning back now": "CURTAIN CLOSE",
    "something strange is going on up there": "LIGHTS PURPLE"
}

# Ask user to enter a line of dialogue
dialogue = input("Enter a line of dialogue: ")

# Normalize the text by converting to lowercase and removing punctuation
import string

normalized_dialogue = dialogue.lower().translate(
    str.maketrans("", "", string.punctuation)
).strip()

# Check if dialogue matches a cue
if normalized_dialogue in cues:
    print("Cue detected:", cues[normalized_dialogue])
else:
    print("NO CUE")
