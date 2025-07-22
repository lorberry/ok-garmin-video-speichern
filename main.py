import sounddevice as sd
import queue
import json
import os
from vosk import Model, KaldiRecognizer
from pynput.keyboard import Controller, Key

MODEL_DIR = "vosk-model-de-0.21"
SAMPLE_RATE = 16000

def init_speech_recognition():
    if not os.path.exists(MODEL_DIR):
        print(f"model '{MODEL_DIR}' not found")
        exit(1)
    
    model = Model(MODEL_DIR)
    return KaldiRecognizer(model, SAMPLE_RATE)

def audio_callback(indata, frames, time, status):
    if status:
        print(f"Audio Status: {status}")
    q.put(bytes(indata))

def process_command(text):
    text = text.lower().strip()
    if not text:
        return False
    
    print(f"u said: {text}")
    
    trigger_phrases = [
        "okay garmin video speichern",
        "ok garmin video speichern", 
        "okay garmin videospeichern",
        "ok garmin videospeichern"
    ]
    
    for phrase in trigger_phrases:
        if phrase in text:
            kbd.press(Key.f10)
            kbd.release(Key.f10)
            print("triggered f10")
            return True
    
    return False

if __name__ == "__main__":
    rec = init_speech_recognition()
    kbd = Controller()
    q = queue.Queue()
    
    print("running")
    
    try:
        with sd.RawInputStream(
            samplerate=SAMPLE_RATE, 
            blocksize=8000, 
            dtype='int16', 
            channels=1, 
            callback=audio_callback
        ):
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    if result.get("text"):
                        process_command(result["text"])
                        
    except KeyboardInterrupt:
        print("\e")
    except Exception as e:
        print(f"error: {e}")
