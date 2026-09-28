"""
JARVIS Wake Word Detection Module
Runs locally in a lightweight background thread.
Listens for "Jarvis", "Hey Jarvis", "Wake up Jarvis", etc. to awaken JARVIS from standby.
"""

import time
import threading
import traceback
import speech_recognition as sr

class WakeWordDetector:
    def __init__(self, on_wake_callback=None, keywords=None):
        self.on_wake_callback = on_wake_callback
        self.keywords = [k.lower() for k in (keywords or [
            "jarvis", "hey jarvis", "hi jarvis", "ok jarvis", 
            "wake up jarvis", "wake up", "hello jarvis",
            "travis", "javis", "jarves", "charvis", "service"
        ])]
        self._running = False
        self._listening = False
        self._thread = None
        self.recognizer = sr.Recognizer()
        # Tune recognizer for fast, sensitive keyword detection
        self.recognizer.energy_threshold = 200
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.dynamic_energy_adjustment_damping = 0.15
        self.recognizer.dynamic_energy_ratio = 1.5
        self.recognizer.pause_threshold = 0.4
        self.recognizer.phrase_threshold = 0.15
        self.recognizer.non_speaking_duration = 0.2

    def start(self):
        """Starts the wake word background monitor thread."""
        if self._running:
            return
        self._running = True
        self._listening = True
        self._thread = threading.Thread(target=self._run_loop, name="WakeWordDetectorThread", daemon=True)
        self._thread.start()
        print("[WakeWord] 🟢 Wake word engine started. Listening for:", self.keywords)

    def stop(self):
        """Stops the wake word engine completely."""
        self._running = False
        self._listening = False

    def pause(self):
        """Temporarily pauses wake word listening (e.g. while JARVIS is actively chatting)."""
        self._listening = False

    def resume(self):
        """Resumes wake word listening (e.g. when entering standby/sleep)."""
        self._listening = True
        print("[WakeWord] 👂 Standby mode active: Listening for 'Jarvis'...")

    def _run_loop(self):
        while self._running:
            if not self._listening:
                time.sleep(0.3)
                continue

            try:
                with sr.Microphone() as source:
                    # Quick ambient adjustment if needed
                    try:
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.4)
                    except Exception:
                        pass

                    while self._running and self._listening:
                        try:
                            # Listen for short phrase with timeout
                            audio = self.recognizer.listen(source, timeout=1.5, phrase_time_limit=3.0)
                            if not self._listening or not self._running:
                                break

                            # Recognize speech using Google's free endpoint or local recognition
                            text = ""
                            try:
                                text = self.recognizer.recognize_google(audio).lower().strip()
                            except sr.UnknownValueError:
                                pass
                            except sr.RequestError:
                                # Network glitch, sleep briefly and retry
                                time.sleep(0.5)
                            except Exception:
                                pass

                            if text:
                                print(f"[WakeWord] 🎙 Heard: '{text}'")
                                if any(kw in text for kw in self.keywords):
                                    print(f"[WakeWord] ⚡ WAKE WORD TRIGGERED: '{text}'")
                                    self._listening = False  # Pause while waking up
                                    if self.on_wake_callback:
                                        try:
                                            self.on_wake_callback(text)
                                        except Exception as cb_err:
                                            print(f"[WakeWord] Callback error: {cb_err}")
                                    break

                        except sr.WaitTimeoutError:
                            # Normal timeout when silence, keep listening
                            continue
                        except Exception as e:
                            # Ignore intermittent audio stream interruptions
                            time.sleep(0.2)

            except Exception as mic_err:
                print(f"[WakeWord] Mic error: {mic_err}. Retrying in 2s...")
                time.sleep(2)
