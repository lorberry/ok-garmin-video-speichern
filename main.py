import sounddevice as sd
import queue
import json
import os
import time
import simpleaudio as sa
from vosk import Model, KaldiRecognizer
from pynput.keyboard import Controller, Key

MODEL_DIR = "vosk-model-de-0.21"
SAMPLE_RATE = 16000

last_okay_garmin_time = None

def init_speech_recognition():
    print("checking model directory")
    if not os.path.exists(MODEL_DIR):
        print(f"model {MODEL_DIR} not found")
        exit(1)
    
    print("loading vosk model")
    model = Model(MODEL_DIR)
    print("model loaded")
    
    print("creating recognizer")
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)
    print("recognizer created")
    return recognizer

def audio_callback(indata, frames, time, status):
    if status:
        print(f"audio status {status}")
    q.put(bytes(indata))

def process_command(text):
    global last_okay_garmin_time
    text = text.lower().strip()
    if not text:
        return False
    
    print(f"processing {text}")
    
    if "okay garmin" in text or "ok garmin" in text:
        print("playing biep wav")
        try:
            wave_obj = sa.WaveObject.from_wave_file("biep.wav")
            play_obj = wave_obj.play()
        except Exception as e:
            print(f"error playing biep wav {e}")
        
        last_okay_garmin_time = time.time()
        print("waiting for video speichern command")
        return True

    video_save_variants = [
        "video speichern",
        "videospeichern", 
        "video spychern",
        "video spaichern",
        "video spei chern",
        "wideo speichern",
        "video speiern",
        "video speichern"
    ]
    
    video_command_found = any(variant in text for variant in video_save_variants)
    
    if video_command_found:
        print(f"video save command detected {text}")
        
        if last_okay_garmin_time:
            time_diff = time.time() - last_okay_garmin_time
            print(f"time since okay garmin {time_diff:.1f}s")
            
            if time_diff <= 8:
                kbd.press(Key.f10)
                kbd.release(Key.f10)
                print("f10 triggered")
                
                print("playing dideldip wav")
                try:
                    wave_obj = sa.WaveObject.from_wave_file("dideldip.wav")
                    play_obj = wave_obj.play()
                except Exception as e:
                    print(f"error playing dideldip wav {e}")
                
                last_okay_garmin_time = None
                return True
            else:
                print(f"timeout exceeded {time_diff:.1f}s")
        else:
            print("no recent okay garmin command")
    
    return False

if __name__ == "__main__":
    print("starting program")
    
    print("checking audio devices")
    print("available audio devices")
    print(sd.query_devices())
    
    print("initializing speech recognition")
    rec = init_speech_recognition()
    
    print("creating keyboard controller")
    kbd = Controller()
    
    print("creating audio queue")
    q = queue.Queue()
    
    print("starting audio stream")
    print("running say okay garmin followed by video speichern within 8 seconds")
    
    try:
        with sd.RawInputStream(
            samplerate=SAMPLE_RATE, 
            blocksize=8000, 
            dtype='int16', 
            channels=1, 
            callback=audio_callback
        ):
            print("audio stream started")
            print("listening for speech")
            
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    if result.get("text"):
                        print(f"final {result['text']}")
                        process_command(result["text"])
                else:
                    partial = json.loads(rec.PartialResult())
                    if partial.get("partial"):
                        partial_text = partial["partial"]  
                        print(f"partial {partial_text}", end='\r')
                        
                        if "video" in partial_text.lower() and ("speich" in partial_text.lower() or "spych" in partial_text.lower()):
                            process_command(partial_text)
                        
    except KeyboardInterrupt:
        print("stopped")
    except Exception as e:
        print(f"error {e}")
        import traceback
        traceback.print_exc()
