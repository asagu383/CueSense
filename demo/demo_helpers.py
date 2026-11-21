"""CueSense demonstration helpers, prepared 10 November 2026.

These helpers add input/output only. They do not implement speech recognition,
matching, threshold selection or evaluation. Keep them out of the frozen study.
Windows playback is intentionally synchronous: record, stop, process, play.
"""
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Mapping

BASE_DIR = Path(__file__).resolve().parent
# Example only: replace C01 with the exact ID returned by your accepted matcher.
SOUND_FILES = {"C01": BASE_DIR / "sounds" / "footsteps.wav"}


def play_cue(
    cue_id: str | None,
    sound_files: Mapping[str, Path] | None = None,
) -> bool:
    """Play one mapped cue. Rejected/unmapped decisions remain silent.

    Call this ONCE after the selected demo matcher has returned its final
    accepted ID. Do not call once for exact and again for fuzzy matching.
    False means no playback succeeded, not that matching was incorrect.
    """
    mapping = SOUND_FILES if sound_files is None else sound_files
    path = mapping.get(cue_id) if cue_id is not None else None
    if path is None:
        print(f"No sound mapped for decision {cue_id!r}; remaining silent.")
        return False
    path = Path(path)
    if not path.is_file():
        print(f"Sound file missing: {path}")
        return False
    if path.suffix.lower() != ".wav":
        print("Use a genuine WAV file, not an MP3 renamed to .wav.")
        return False
    try:
        import winsound  # Built into Windows Python; no pip install needed.
    except ImportError:
        print("This playback helper requires Windows Python.")
        return False
    try:
        # No SND_ASYNC: wait until playback finishes before the next recording.
        winsound.PlaySound(
            str(path), winsound.SND_FILENAME | winsound.SND_NODEFAULT
        )
    except (RuntimeError, OSError) as error:
        print(f"Playback failed for {cue_id}: {error}")
        return False
    print(f"Played once: {cue_id} -> {path.name}")
    return True


def record_demo_clip(
    seconds: float = 6.0,
    output_dir: Path | None = None,
    device: int | str | None = None,
) -> Path:
    """Manually start one bounded microphone recording; save a unique mono WAV.

    The returned path is an INPUT to the student's existing processing routine.
    Only record your own voice. Do not include these files in the held-out set.
    """
    if not 0 < seconds <= 30:
        raise ValueError("Choose a recording duration greater than 0 and at most 30 seconds.")
    try:
        import sounddevice as sd
        import soundfile as sf
    except ImportError as error:
        raise RuntimeError(
            "Install sounddevice and soundfile in the separate demo environment."
        ) from error

    folder = BASE_DIR / "demo_recordings" if output_dir is None else Path(output_dir)
    try:
        folder.mkdir(parents=True, exist_ok=True)
        info = sd.query_devices(device, kind="input")
        sample_rate = int(info["default_samplerate"])
        sd.check_input_settings(
            device=device, channels=1, dtype="float32", samplerate=sample_rate
        )
        input("Press Enter when ready. Recording starts immediately after Enter: ")
        print(f"Speak now. Recording for {seconds:g} seconds...")
        audio = sd.rec(
            frames=round(seconds * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="float32",
            device=device,
            blocking=True,
        )
        path = folder / f"demo_{datetime.now():%Y%m%d_%H%M%S_%f}.wav"
        sf.write(str(path), audio, sample_rate, subtype="PCM_16")
    except (sd.PortAudioError, OSError, RuntimeError, ValueError) as error:
        raise RuntimeError(
            "Recording or saving failed. Check microphone selection/access, "
            f"mono support and the output folder. Details: {error}"
        ) from error
    except KeyboardInterrupt:
        sd.stop()
        raise
    print(f"Microphone capture finished. Saved: {path}")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Test CueSense demo I/O helpers only.")
    sub = parser.add_subparsers(dest="command", required=True)
    play = sub.add_parser("play", help="Test a sound without running the recognizer.")
    play.add_argument("cue_id", help="Example: C01; adapt SOUND_FILES first.")
    record = sub.add_parser("record", help="Record one microphone clip; no matching yet.")
    record.add_argument("--seconds", type=float, default=6.0)
    record.add_argument("--device", type=int, default=None, help="Optional input-device ID.")
    sub.add_parser("devices", help="List the available audio devices.")
    args = parser.parse_args()
    try:
        if args.command == "play":
            return 0 if play_cue(args.cue_id) else 1
        if args.command == "record":
            record_demo_clip(args.seconds, device=args.device)
        else:
            import sounddevice as sd
            print(sd.query_devices())
    except (ImportError, RuntimeError, ValueError) as error:
        print(f"Cannot complete helper test: {error}")
        return 1
    except (KeyboardInterrupt, EOFError):
        print("Cancelled; no further cue processing requested.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
