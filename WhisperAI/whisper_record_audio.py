import pyaudio
import wave
import whisper
import time

# Constants
CHUNK_SIZE = 1024  # Smaller chunks to reduce overflow risk
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Whisper expects 16000 Hz
RECORD_SECONDS = 5  # Recording duration in seconds
OUTPUT_FILENAME = "output.wav"  # Output file name

# Initialize Whisper model
model = whisper.load_model("small")

# Initialize pyaudio
audio_interface = pyaudio.PyAudio()

# Function to record audio
def record_audio(seconds):
    print(f"Recording for {seconds} seconds...")
    
    # Set up the stream for recording
    stream = audio_interface.open(format=FORMAT,
                                  channels=1,
                                  rate=RATE,
                                  input=True,
                                  input_device_index=0, # built-in mic
                                  frames_per_buffer=CHUNK_SIZE)
    
    frames = []
    
    # Record audio for the specified duration
    for _ in range(0, int(RATE / CHUNK_SIZE * seconds)):
        data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
        frames.append(data)
        
    print("First frame sample (hex):", frames[0][:10].hex())

    
    # Stop the recording stream
    print("Recording complete.")
    stream.stop_stream()
    stream.close()
    
    # Save the audio to a .wav file
    with wave.open(OUTPUT_FILENAME, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio_interface.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))

    audio_interface.terminate()

    print(f"Audio saved as {OUTPUT_FILENAME}")

# Function to transcribe audio using Whisper
def transcribe_audio(filename):
    print("Transcribing...")
    
    # Make prediction
    result = model.transcribe(filename)
    
    print("--- Transcription ---")
    print(result["text"])

# Main function to manage the recording and transcription
def main():
    record_audio(RECORD_SECONDS)  # Record for the specified number of seconds
    transcribe_audio(OUTPUT_FILENAME)  # Transcribe the recorded audio

if __name__ == "__main__":
    main()
