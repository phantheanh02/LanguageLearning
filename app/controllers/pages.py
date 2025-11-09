from flask import render_template, jsonify, request

from .chat import ChatController
from .image import ImageController

def home():
    """Render the home page."""
    return render_template('home.html')

def chat():
    """Render the chat page."""
    return render_template('chat.html')

def speech():
    """Render the speech recognition page."""
    current_image = ImageController.get_current_image()
    return render_template('speech.html', image=current_image)

def next_image():
    """Get the next image in sequence."""
    next_img = ImageController.get_next_image()
    return jsonify({'image': next_img})

def chat_send():
    """Handle chat message sending (stub function)."""
    data = request.get_json()
    message = data.get('message', '')
    response = ChatController.get_response(message)
    return jsonify({'response': response})