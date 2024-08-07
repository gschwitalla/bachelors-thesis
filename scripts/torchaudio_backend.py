import torchaudio
from pathlib import Path
from typing import Union, Optional

# Pfad zur Audiodatei (ersetze durch eine gültige Datei in deinem System)
audio_path = Path("tests/samples/ASR/spk1_snt1.wav")

# Versuche, Informationen zur Datei zu laden und gib sie aus
try:
    info = torchaudio.info(audio_path, backend="ffmpeg")
    print(f"Sample Rate: {info.sample_rate}")
    print(f"Channels: {info.num_channels}")
    print(f"Duration (seconds): {info.num_frames / info.sample_rate}")
except Exception as e:
    print(f"Fehler beim Laden der Datei: {e}")

input("Drücke Enter, um die Konsole zu schließen...")
