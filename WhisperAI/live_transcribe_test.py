import pyaudio
import whisper
import numpy as np
import torch
import time

# Constants
CHUNK = 1024  # Chunk size
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono
RATE = 16000  # Sampling rate (Whisper expects 16000 Hz)
CHUNK_DURATION = 3  # Duration of each chunk (seconds)

# Initialize Whisper model
model = whisper.load_model("small")

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open the audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Starting live transcription... (Press Ctrl+C to stop)\n")

try:
    frames_per_window = int(RATE / CHUNK * CHUNK_DURATION)

    while True:
        frames = []
        for _ in range(frames_per_window):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

        # Convert frames to numpy array
        audio_bytes = b''.join(frames)
        audio_np = np.frombuffer(audio_bytes, dtype=np.int16)
        audio_float = audio_np.astype(np.float32) / 32768.0  # Normalize

        # Convert numpy array to torch tensor
        audio_tensor = torch.from_numpy(audio_float)

        # Pad or trim the audio for Whisper model
        audio_tensor = whisper.pad_or_trim(audio_tensor)

        # Transcribe the audio
        result = model.transcribe(audio_tensor)

        # Print the transcription
        print(f"→ {result['text']}")

except KeyboardInterrupt:
    print("\nStopping live transcription.")

finally:
    # Clean up PyAudio stream
    stream.stop_stream()
    stream.close()
    p.terminate()
