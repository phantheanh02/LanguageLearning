import os
from flask import request, jsonify, render_template
from ..models.speech_recognition import SpeechRecognizer, TranscriptionError

def handle_recognition():
    """Handle speech recognition requests."""
    
    # Check if audio file was uploaded
    if 'file' not in request.files:
        error_msg = 'No audio file uploaded'
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': error_msg}), 400
        return render_template('speech.html', error=error_msg)

    # Get the current image being shown
    current_image = request.form.get('image', '')

    file = request.files['file']
    if file.filename == '':
        error_msg = 'No audio file selected'
        return render_template('speech.html', error=error_msg)

    # Save the uploaded audio file to a temporary path
    suffix = os.path.splitext(file.filename)[1] or '.wav'
    tmp_path = os.path.join('.', 'tmp_upload' + suffix)
    file.save(tmp_path)

    try:
        # Get singleton instance of speech recognizer
        recognizer = SpeechRecognizer.get_instance()
        
        # Perform transcription
        transcription = recognizer.transcribe(tmp_path)
        
        # Format the response
        text, lang_name, result = recognizer.format_response(transcription, current_image)
        
        # Return response based on request type
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'transcription': text,
                'language': result,  # Using result message as language feedback
                'image': current_image  # Return current image for context
            })
        
        return render_template('speech.html',
                             transcription=text,
                             language=lang_name,
                             image=current_image)
                             
    except TranscriptionError as e:
        error_msg = str(e)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': error_msg}), 500
        return render_template('speech.html', error=error_msg)
        
    finally:
        # Clean up temporary file
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except OSError:
            pass  # Ignore cleanup errors
