# CueSense: two demonstration additions
Prepared for Aulphrine Cyrille Sagudan with Jordan Kidney, 10 November 2026.

These are instructional helpers, NOT a patch reviewed against your current source.
They provide microphone input and WAV output only. You retain responsibility for
integrating, understanding, testing and explaining your recognizer and matcher.
Acknowledge these supplied helpers and any other assistance in your project.

## Work in this order
1. Finish the frozen evaluation and outstanding reading notes for November 13.
2. For November 20: connect one accepted cue to one sound; retain paper/slide drafts.
3. For November 27: record a short phrase, stop, process it, then play the cue.
4. December 4: rehearsal/final review. December 9: complete supervisor package.
All checkpoints remain 8 p.m. Calgary/MRU time. Report blockers before deadlines.

## Protect the original experiment
Keep the November 6 code/settings, original requirements and evaluation data/logs.
Use a separate demo branch or working copy plus .venv-demo. Do not overwrite the
frozen requirements.txt or tune the threshold on the held-out clips. Keep 90 for
the agreed fuzzy demo method. Noise testing is parked; do not add continuous
listening, live theatre hardware or a new interface. Save microphone trials in
demo_recordings and any demo log in demo_log.csv, not in evaluation results.
The record/stop/process/play demonstration is NOT continuous real-time ASR.

## Files
- demo_helpers.py: reusable play_cue() and record_demo_clip(), plus helper CLI.
- requirements-demo.txt: separate demo environment inputs.
- README_demo_helpers.md: these instructions.
No audio samples or replacement matching code are supplied.

## A. Play one sound (Windows)
Place demo_helpers.py beside your demo script. Create sounds/footsteps.wav using
your own recording or a sound you have permission to redistribute. Start with a
short, genuine PCM WAV at low volume. Edit SOUND_FILES to use your actual cue ID.
The example C01 is a mapping key, not a claim about your current function output.

    python demo_helpers.py play C01

This tests only the speaker/file path. Next call play_cue(accepted_cue_id) ONCE
from your existing demo path AFTER its final accepted fuzzy decision. NONE,
blank input, ties and below-threshold results must NOT fire a sound. Do not
call playback in both exact/fuzzy evaluation rows. Unmapped visual cues may
remain printed labels. Do not replace legitimate no-cue output with a canned cue.

## B. Record a short phrase (Windows Command Prompt)
With your frozen requirements.txt available, create a separate environment:

    python -m venv .venv-demo
    .venv-demo\Scripts\python.exe -m pip install -r requirements-demo.txt
    .venv-demo\Scripts\python.exe demo_helpers.py devices
    .venv-demo\Scripts\python.exe demo_helpers.py record --seconds 6

The two added versions are documented example pins, not a claim they are latest.
If dependency resolution fails, save the error and ask Jordan; do not loosen the
frozen evaluation requirements to make installation succeed.

Use the returned WAV path in the SAME transcription/normalization/matching
routine used in your project. Join/consume all faster-whisper segments before
matching. Load the existing model once before starting a series of demo trials.
Do not alter its existing transcription options. You do not need GPU setup.

Conceptual wiring only (adapt to YOUR function names/return values):

    path = record_demo_clip()
    [existing transcription + normalization + fuzzy decision at 90]
    [display transcript and final accepted cue ID, or NONE]
    play_cue(accepted_cue_id)

The bracketed lines are instructions, not executable Python. Your exact source
has not been inspected, so no assumed recognizer/matcher function is supplied.
Stop recording before sound playback. Wait for playback to end before manually
starting the next recording. Repeating the same cue in a NEW deliberate trial
is allowed; a single trial must not fire twice.

## Evidence to send
Nov 20: one positive prerecorded clip plays once; one unrelated clip stays silent;
include code/diff, sound attribution, screen recording with audible output, paper
and slide drafts, and the short update.
Nov 27: a freshly spoken cue is processed and plays once; an unrelated phrase
stays silent. Include revised paper/slides, demo instructions, demo dependencies,
code/diff, private demonstration recordings and a backup video WITH audible sound.
Show actual recognition errors honestly. Do not claim general reliability from
these demonstrations. Save your demo environment separately:

    .venv-demo\Scripts\python.exe -m pip freeze > demo_environment.txt

## When stuck
No sound: check volume/output device, the real WAV file, path and mapping key;
run the isolated play command before debugging the matcher.
No microphone: run the devices command; select an input with --device ID; check
Windows microphone/desktop-app permission; close another app using the device.
If recording is clipped, choose a slightly longer bounded clip, not streaming.
If ASR drops a word, keep the transcript. Do not manually fix it or tune on tests.
If blocked for around 30 minutes, send the command, full error and what worked.
Continue with writing/results; keep prerecorded-input playback as the fallback.
Any scope/date adjustment requires agreement, not silent delay.

## Research/report separation
Keep the submitted November 6 test-plan PDF as the historical frozen protocol.
Add a dated demonstration subsection to the report/README, rather than rewriting
that protocol to suggest microphone/audio playback were tested in the original
experiment. Record demo code/version, helpers and sound-file attribution.
Exclude recording and sound duration from the original offline processing-time
metric. If you additionally time the demo, label it separately and define start/end.

## Official documentation (checked 10 November 2026)
https://docs.python.org/3.12/library/winsound.html
https://python-sounddevice.readthedocs.io/en/0.5.3/usage.html
https://python-sounddevice.readthedocs.io/en/0.5.3/api/convenience-functions.html
https://python-soundfile.readthedocs.io/en/0.13.1/
https://github.com/SYSTRAN/faster-whisper/tree/v1.2.1

## Validation boundary
The supplied helper syntax and selected control paths were checked with mocked
audio backends. No real microphone, Windows sound output, ASR integration or
student laptop execution was validated here. Run the isolated tests locally.
