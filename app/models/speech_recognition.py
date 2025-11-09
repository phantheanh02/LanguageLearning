import whisper
import os
import csv

from app.controllers.image import ImageController

class SpeechRecognizer:
    _instance = None
    _model = None
    
    
    @classmethod
    def get_instance(self):
        if self._instance is None:
            self._instance = SpeechRecognizer()
        return self._instance
    
    def __init__(self):
        """Initialize the speech recognizer with Whisper model."""
        if SpeechRecognizer._model is None:
            SpeechRecognizer._model = whisper.load_model("base")
        
    
    def transcribe(self, audio_path, language="ja"):
        """
        Transcribe audio file using Whisper model.
        
        Args:
            audio_path (str): Path to the audio file
            language (str): Target language code (default: "ja" for Japanese)
            
        Returns:
            dict: Contains transcription text, detected language, and other metadata
        """
        try:
            result = self._model.transcribe(audio_path, language=language)
            return result
        except Exception as e:
            raise TranscriptionError(f"Failed to transcribe audio: {str(e)}")
    
    def format_response(self, transcription, current_image):
        """
        Format the transcription result for response.
        
        Args:
            transcription (dict): Raw transcription result from Whisper
            
        Returns:
            tuple: (text, language_name, result_message)
        """
        if not isinstance(transcription, dict):
            return '', '', 'Sai rồi bạn ơi'
            
        text = transcription.get('text', '')
        lang_code = transcription.get('language') or transcription.get('language_code') or ''
        
        # Map language codes to readable names
        lang_map = {'ja': 'Japanese', 'en': 'English'}
        lang_name = lang_map.get(lang_code, lang_code)

        # Custom validation logic
        result_message = "Sai rồi bạn ơi"
        text_original = ImageController.get_current_text()
        if text == text_original:
            result_message = "Đúng rồi bạn ơi"

        return text, lang_name, result_message

class TranscriptionError(Exception):
    """Custom exception for transcription errors."""
    pass