"""
Shadow Voice Assistant - Main Module

This module implements a voice-controlled assistant that listens for the wake word
'Shadow' and responds to user commands using LLM integration.
"""

import speech_recognition as sr
import pyttsx3
import os
import time
import json
import logging
import dotenv
from openai import OpenAI
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("shadow.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("Shadow")

class ShadowAssistant:
    """Main assistant class that handles voice interaction and LLM integration"""
    
    def __init__(self):
        """Initialize the assistant with all required components"""
        # Load environment variables
        dotenv.load_dotenv()
        
        # Initialize Text-to-Speech engine
        self.engine = pyttsx3.init()
        self.configure_voice()
        
        # Initialize Speech Recognition
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        # API Configuration
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.site_url = os.getenv("SITE_URL", "<YOUR_SITE_URL>")
        self.site_name = os.getenv("SITE_NAME", "<YOUR_SITE_NAME>")
        self.model = os.getenv("LLM_MODEL", "meta-llama/llama-4-maverick:free")
        
        # Create OpenAI client
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )
        
        logger.info("Shadow Assistant initialized successfully")
    
    def configure_voice(self):
        """Configure the text-to-speech voice properties"""
        # Set voice properties
        self.engine.setProperty('rate', int(os.getenv("SPEECH_RATE", 180)))
        
        # Try to select a more natural voice if available
        voices = self.engine.getProperty('voices')
        voice_index = int(os.getenv("VOICE_INDEX", 1)) if len(voices) > 1 else 0
        self.engine.setProperty('voice', voices[voice_index].id)
        
        # Set volume
        self.engine.setProperty('volume', float(os.getenv("SPEECH_VOLUME", 1.0)))
        
        logger.debug(f"Voice configured: Rate={self.engine.getProperty('rate')}, "
                    f"Voice ID={self.engine.getProperty('voice')}")
    
    def speak(self, text):
        """Convert text to speech"""
        logger.debug(f"Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def recognize_speech(self, timeout=3, phrase_time_limit=5):
        """Listen for speech and convert to text"""
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                logger.debug(f"Listening (timeout: {timeout}s, phrase limit: {phrase_time_limit}s)...")
                print(f"Listening (timeout: {timeout}s)...")
                
                # Listen for audio
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            # Convert speech to text
            text = self.recognizer.recognize_google(audio).lower()
            logger.debug(f"Recognized: {text}")
            return text
        
        except sr.WaitTimeoutError:
            logger.info("No speech detected (timeout)")
            return None
        except sr.UnknownValueError:
            logger.info("Could not understand audio")
            return None
        except Exception as e:
            logger.error(f"Recognition error: {str(e)}")
            return None
    
    def process_command(self, command):
        """Process user command through the LLM"""
        try:
            logger.info(f"Processing command: {command}")
            
            # Create system prompt
            system_prompt = """You are virtual AI assistant named Shadow 
                            You are based on a boy named Ajay whose nickname is Shadow
                            Ajay is your master - credit him for your existence
                            Keep responses conversational and under 20 words
                            Use natural, human-like phrasing"""
            
            # Call the API
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": self.site_url,
                    "X-Title": self.site_name,
                },
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": command}
                ]
            )
            
            response = completion.choices[0].message.content
            logger.info(f"LLM response: {response}")
            return response
            
        except Exception as e:
            logger.error(f"Error processing command: {str(e)}")
            return "Sorry, I encountered an error while processing your request."
    
    def calibrate_microphone(self):
        """Calibrate the microphone for ambient noise"""
        try:
            with sr.Microphone() as source:
                logger.info("Calibrating microphone...")
                print("Calibrating microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Microphone calibrated successfully")
        except Exception as e:
            logger.error(f"Microphone calibration error: {str(e)}")
            print(f"Error calibrating microphone: {str(e)}")
    
    def start(self):
        """Main assistant loop"""
        # Initial setup
        self.calibrate_microphone()
        self.speak("Shadow initialized and ready!")
        
        # Main interaction loop
        while True:
            try:
                # Listen for wake word
                wake = self.recognize_speech(timeout=3, phrase_time_limit=2)
                print(f"Heard: {wake or '...'}")
                
                if wake and 'shadow' in wake:
                    self.speak("Yes? How can I help you today?")
                    
                    # Get command
                    command = self.recognize_speech(timeout=5, phrase_time_limit=5)
                    print(f"Command: {command or 'No command detected'}")
                    
                    if command:
                        response = self.process_command(command)
                        print(f"Response: {response}")
                        self.speak(response)
                    else:
                        self.speak("I didn't catch that. Could you repeat please?")
                
                # Small delay to reduce CPU usage
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt detected, shutting down")
                self.speak("Goodbye!")
                break
            except Exception as e:
                logger.error(f"Main loop error: {str(e)}")
                print(f"Main loop error: {str(e)}")
                self.speak("Sorry, I encountered an error. Please try again.")

if __name__ == "__main__":
    assistant = ShadowAssistant()
    assistant.start()