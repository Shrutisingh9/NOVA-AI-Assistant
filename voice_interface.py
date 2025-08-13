"""
Voice Interface Module for Nova AI Assistant
Handles Speech-to-Text (STT) and Text-to-Speech (TTS) operations
"""

import speech_recognition as sr
import pyttsx3
import time
import threading
from typing import Optional, Callable


class VoiceInterface:
    """Handles voice input/output for Nova AI Assistant"""
    
    def __init__(self):
        """Initialize voice interface components"""
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.is_listening = False
        self.callback = None
        
        # Configure TTS engine
        self._setup_tts()
        
        # Configure STT
        self._setup_stt()
    
    def _setup_tts(self):
        """Configure text-to-speech engine"""
        try:
            # Get available voices and set a good one
            voices = self.engine.getProperty('voices')
            if voices:
                # Prefer a female voice if available, otherwise use first available
                for voice in voices:
                    if "female" in voice.name.lower() or "zira" in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
                else:
                    self.engine.setProperty('voice', voices[0].id)
            
            # Set speech rate and volume
            self.engine.setProperty('rate', 180)  # Words per minute
            self.engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
            
        except Exception as e:
            print(f"Warning: Could not configure TTS engine: {e}")
    
    def _setup_stt(self):
        """Configure speech recognition"""
        try:
            # Adjust recognition parameters
            self.recognizer.energy_threshold = 4000  # Minimum audio energy
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8  # Seconds of silence to mark end
            self.recognizer.phrase_threshold = 0.3  # Minimum seconds of speaking
            self.recognizer.non_speaking_duration = 0.5  # Seconds of non-speaking before stopping
            
        except Exception as e:
            print(f"Warning: Could not configure STT: {e}")
    
    def speak(self, text: str, wait: bool = True) -> None:
        """
        Convert text to speech
        
        Args:
            text: Text to speak
            wait: Whether to wait for speech to complete
        """
        try:
            if wait:
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                # Run in separate thread to avoid blocking
                threading.Thread(target=self._speak_thread, args=(text,), daemon=True).start()
        except Exception as e:
            print(f"Error in speech synthesis: {e}")
    
    def _speak_thread(self, text: str):
        """Internal method for non-blocking speech"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in speech thread: {e}")
    
    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen for voice input and convert to text
        
        Args:
            timeout: Seconds to wait for speech to start
            phrase_time_limit: Maximum seconds for a single phrase
            
        Returns:
            Recognized text or None if failed
        """
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio input
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
                
                print("🔍 Processing speech...")
                
                # Use Google's speech recognition
                text = self.recognizer.recognize_google(audio)
                print(f"✅ Recognized: {text}")
                return text.lower()
                
        except sr.WaitTimeoutError:
            print("⏰ No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            print("❓ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"🌐 Speech recognition service error: {e}")
            return None
        except Exception as e:
            print(f"❌ Error in speech recognition: {e}")
            return None
    
    def start_listening_loop(self, callback: Callable[[str], None], 
                           wake_word: str = "nova") -> None:
        """
        Start continuous listening for wake word and commands
        
        Args:
            callback: Function to call when command is detected
            wake_word: Word to listen for to activate Nova
        """
        self.is_listening = True
        self.callback = callback
        
        print(f"🎧 Nova is listening for '{wake_word}'...")
        
        while self.is_listening:
            try:
                # Listen for wake word
                text = self.listen(timeout=3, phrase_time_limit=5)
                
                if text and wake_word in text.lower():
                    # Wake word detected, listen for command
                    self.speak("Yes, sir? I'm listening.", wait=False)
                    
                    # Listen for actual command
                    command = self.listen(timeout=5, phrase_time_limit=15)
                    
                    if command:
                        # Remove wake word from command
                        command = command.replace(wake_word, "").strip()
                        if command:
                            callback(command)
                    else:
                        self.speak("I didn't catch that. Could you repeat your command?")
                        
            except KeyboardInterrupt:
                print("\n🛑 Listening stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in listening loop: {e}")
                time.sleep(1)
    
    def stop_listening(self) -> None:
        """Stop the listening loop"""
        self.is_listening = False
        print("🔇 Nova stopped listening")
    
    def test_microphone(self) -> bool:
        """Test if microphone is working properly"""
        try:
            with sr.Microphone() as source:
                print("🎤 Testing microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("✅ Microphone test successful")
                return True
        except Exception as e:
            print(f"❌ Microphone test failed: {e}")
            return False
    
    def test_speakers(self) -> bool:
        """Test if speakers are working properly"""
        try:
            test_text = "Testing Nova's voice interface. If you can hear this, everything is working perfectly."
            print("🔊 Testing speakers...")
            self.speak(test_text)
            print("✅ Speaker test successful")
            return True
        except Exception as e:
            print(f"❌ Speaker test failed: {e}")
            return False


if __name__ == "__main__":
    # Test the voice interface
    voice = VoiceInterface()
    
    print("🎯 Testing Nova's Voice Interface")
    print("=" * 40)
    
    # Test speakers
    voice.test_speakers()
    
    # Test microphone
    if voice.test_microphone():
        print("\n🎤 Microphone test passed! You can now test voice commands.")
        print("Say something like 'Hello Nova' to test speech recognition...")
        
        # Test speech recognition
        result = voice.listen(timeout=10)
        if result:
            print(f"🎉 Speech recognition successful: '{result}'")
            voice.speak(f"I heard you say: {result}")
        else:
            print("❌ Speech recognition test failed")
    else:
        print("❌ Microphone test failed. Please check your microphone settings.")
