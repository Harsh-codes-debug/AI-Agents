"""
Voice Command Handler Module for DataSage AI

This module provides voice interaction capabilities:
- Speech recognition for voice commands
- Text-to-speech for AI responses
- Voice command processing and routing
- Fallback text-based interface for cloud deployments
"""

import streamlit as st
import os
from typing import Optional, Dict, Any

# Try to import voice libraries with graceful fallbacks
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    st.warning("Speech recognition not available. Using text-based interface.")

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

class VoiceCommandProcessor:
    """Handles voice commands and text-to-speech functionality"""
    
    def __init__(self, ai_assistant=None):
        """
        Initialize voice command processor
        
        Args:
            ai_assistant: AI assistant instance for processing commands
        """
        self.ai_assistant = ai_assistant
        self.recognizer = None
        self.tts_engine = None
        
        # Initialize speech recognition
        if SPEECH_RECOGNITION_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.recognizer.energy_threshold = 300
                self.recognizer.dynamic_energy_threshold = True
            except Exception as e:
                st.warning(f"Speech recognition initialization failed: {str(e)}")
                self.recognizer = None
        
        # Initialize text-to-speech
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                # Configure TTS settings
                self.tts_engine.setProperty('rate', 150)  # Speaking rate
                self.tts_engine.setProperty('volume', 0.8)  # Volume level
            except Exception as e:
                st.warning(f"Text-to-speech initialization failed: {str(e)}")
                self.tts_engine = None
    
    def is_voice_available(self) -> bool:
        """Check if voice features are available"""
        return self.recognizer is not None
    
    def is_tts_available(self) -> bool:
        """Check if text-to-speech is available"""
        return self.tts_engine is not None
    
    def listen_for_command(self, timeout: int = 5) -> Optional[str]:
        """
        Listen for voice command using microphone
        
        Args:
            timeout (int): Timeout in seconds for listening
            
        Returns:
            str: Recognized text or None if failed
        """
        if not self.is_voice_available():
            return None
        
        try:
            with sr.Microphone() as source:
                st.info("🎤 Listening... Speak your command!")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
                st.info("🔄 Processing voice command...")
                
                # Recognize speech using Google Web Speech API
                try:
                    text = self.recognizer.recognize_google(audio)
                    st.success(f"✅ Recognized: '{text}'")
                    return text.lower()
                
                except sr.UnknownValueError:
                    st.error("❌ Could not understand the audio. Please try again.")
                    return None
                
                except sr.RequestError as e:
                    st.error(f"❌ Speech recognition service error: {str(e)}")
                    return None
        
        except Exception as e:
            st.error(f"❌ Voice input error: {str(e)}")
            return None
    
    def speak_response(self, text: str) -> bool:
        """
        Convert text to speech
        
        Args:
            text (str): Text to speak
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_tts_available():
            st.info("🔊 Text-to-speech not available. Response displayed as text.")
            return False
        
        try:
            # Clean text for better speech
            clean_text = self._clean_text_for_speech(text)
            
            # Speak the text
            self.tts_engine.say(clean_text)
            self.tts_engine.runAndWait()
            
            return True
            
        except Exception as e:
            st.error(f"Text-to-speech error: {str(e)}")
            return False
    
    def process_voice_command(self, command_text: str) -> Dict[str, Any]:
        """
        Process voice command and return appropriate response
        
        Args:
            command_text (str): Voice command text
            
        Returns:
            Dict[str, Any]: Response from AI or command processing
        """
        if not command_text:
            return {"error": "No command provided"}
        
        try:
            # Normalize command
            command = command_text.lower().strip()
            
            # Route voice commands to appropriate handlers
            if any(phrase in command for phrase in ['analyze', 'analysis', 'examine']):
                return self._handle_analysis_command(command)
            
            elif any(phrase in command for phrase in ['show', 'display', 'tell me']):
                return self._handle_show_command(command)
            
            elif any(phrase in command for phrase in ['find', 'search', 'look for']):
                return self._handle_search_command(command)
            
            elif any(phrase in command for phrase in ['clean', 'fix', 'improve']):
                return self._handle_cleaning_command(command)
            
            elif any(phrase in command for phrase in ['predict', 'forecast', 'trend']):
                return self._handle_prediction_command(command)
            
            elif any(phrase in command for phrase in ['summary', 'summarize', 'overview']):
                return self._handle_summary_command(command)
            
            else:
                # Use AI assistant for general queries
                if self.ai_assistant and self.ai_assistant.is_available():
                    return self.ai_assistant.process_natural_language_query(command_text)
                else:
                    return {
                        "message": f"Voice command received: '{command_text}'",
                        "suggestions": [
                            "Try: 'analyze my data'",
                            "Try: 'show me insights'", 
                            "Try: 'find outliers'",
                            "Try: 'summarize the data'"
                        ]
                    }
        
        except Exception as e:
            return {"error": f"Error processing voice command: {str(e)}"}
    
    def _handle_analysis_command(self, command: str) -> Dict[str, Any]:
        """Handle analysis-related voice commands"""
        if self.ai_assistant and self.ai_assistant.is_available():
            return self.ai_assistant.generate_automated_insights()
        else:
            return {
                "message": "Analysis command received. Please use the EDA tab for comprehensive analysis.",
                "action": "Navigate to the EDA Report tab and click 'Generate EDA Report'"
            }
    
    def _handle_show_command(self, command: str) -> Dict[str, Any]:
        """Handle show/display commands"""
        if 'null' in command or 'missing' in command:
            return {
                "message": "To see missing values, go to the Query Data tab and ask 'show null values'",
                "action": "Use Query Data tab"
            }
        elif 'type' in command:
            return {
                "message": "To see data types, go to the Query Data tab and ask 'what are the data types?'",
                "action": "Use Query Data tab"
            }
        else:
            return {
                "message": "Show command received. Use the Query Data tab for specific data queries.",
                "suggestions": ["Show null values", "Show data types", "Show basic statistics"]
            }
    
    def _handle_search_command(self, command: str) -> Dict[str, Any]:
        """Handle search/find commands"""
        if 'outlier' in command:
            return {
                "message": "To find outliers, go to the Query Data tab and ask 'find outliers'",
                "action": "Use Query Data tab or EDA Report"
            }
        elif 'correlation' in command:
            return {
                "message": "To find correlations, use the Visualizations tab to generate a correlation heatmap",
                "action": "Use Visualizations tab"
            }
        else:
            return {
                "message": "Search command received. Use the Query Data tab for specific searches.",
                "suggestions": ["Find outliers", "Find correlations", "Find duplicates"]
            }
    
    def _handle_cleaning_command(self, command: str) -> Dict[str, Any]:
        """Handle data cleaning commands"""
        if self.ai_assistant and self.ai_assistant.is_available():
            return self.ai_assistant.suggest_data_cleaning()
        else:
            return {
                "message": "Data cleaning suggestions require AI assistant. Please check your Gemini API key.",
                "action": "Set up Gemini API key for AI-powered cleaning suggestions"
            }
    
    def _handle_prediction_command(self, command: str) -> Dict[str, Any]:
        """Handle prediction/trend commands"""
        if self.ai_assistant and self.ai_assistant.is_available():
            return self.ai_assistant.predict_trends()
        else:
            return {
                "message": "Prediction analysis requires AI assistant. Please check your Gemini API key.",
                "action": "Set up Gemini API key for AI-powered predictions"
            }
    
    def _handle_summary_command(self, command: str) -> Dict[str, Any]:
        """Handle summary commands"""
        if self.ai_assistant and self.ai_assistant.is_available():
            return self.ai_assistant.generate_ai_summary_report()
        else:
            return {
                "message": "AI summary requires Gemini API key. Use the EDA tab for basic summary.",
                "action": "Use EDA Report tab for statistical summary"
            }
    
    def _clean_text_for_speech(self, text: str) -> str:
        """
        Clean text for better text-to-speech output
        
        Args:
            text (str): Original text
            
        Returns:
            str: Cleaned text suitable for speech
        """
        # Remove markdown formatting
        import re
        
        # Remove markdown headers
        text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
        
        # Remove markdown bold/italic
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        
        # Remove bullet points
        text = re.sub(r'^[•\-\*]\s*', '', text, flags=re.MULTILINE)
        
        # Replace technical symbols
        text = text.replace('≥', 'greater than or equal to')
        text = text.replace('≤', 'less than or equal to')
        text = text.replace('%', ' percent')
        
        # Limit length for speech (TTS works better with shorter text)
        if len(text) > 500:
            text = text[:500] + "... and more details are available in the interface."
        
        return text

def create_voice_handler(ai_assistant=None) -> VoiceCommandProcessor:
    """
    Factory function to create voice command processor
    
    Args:
        ai_assistant: AI assistant instance
        
    Returns:
        VoiceCommandProcessor: Initialized voice handler
    """
    return VoiceCommandProcessor(ai_assistant)

def get_voice_command_examples() -> list:
    """Get example voice commands"""
    return [
        "analyze my data",
        "show me insights", 
        "find outliers",
        "tell me about missing values",
        "summarize the data",
        "suggest data cleaning",
        "predict trends",
        "show correlations",
        "give me an overview",
        "find patterns"
    ]

def display_voice_setup_instructions() -> None:
    """Display voice setup instructions for users"""
    st.markdown("""
    ### 🎙️ Voice Feature Setup
    
    **For Local Development:**
    1. Install required packages: `pip install speechrecognition pyttsx3 pyaudio`
    2. Ensure microphone permissions are granted
    3. Use a quiet environment for best results
    
    **For Cloud Deployments (Replit/Streamlit Cloud):**
    - Voice input may not work due to browser/security restrictions
    - Use the text-based voice command interface instead
    - All AI functionality is available through text input
    
    **Supported Voice Commands:**
    - "Analyze my data" - Generate comprehensive insights
    - "Show me patterns" - Find data patterns
    - "Find outliers" - Detect anomalies
    - "Suggest cleaning" - Get data cleaning recommendations
    - "Predict trends" - Explore predictive opportunities
    """)
