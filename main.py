import os
from flask import Flask
from app.controllers import pages, speech

def create_app():
    """Create and configure the Flask application."""
    
    # Initialize Flask app with correct template and static folders
    app = Flask(__name__,
                template_folder='app/templates',
                static_folder='app/static')

    # Set a secret key for session management
    app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_123')  # In production, use a proper secret key

    # Configure ffmpeg path
    os.environ["PATH"] = (
        os.path.abspath("libs/ffmpeg/bin") + ";" +
        os.environ["PATH"]
    )

    # Register routes
    app.add_url_rule('/', 'home', pages.home)
    app.add_url_rule('/chat', 'chat', pages.chat)
    app.add_url_rule('/chat/send', 'chat_send', pages.chat_send, methods=['POST'])
    app.add_url_rule('/speech', 'speech', pages.speech)
    app.add_url_rule('/recognize', 'recognize', speech.handle_recognition, methods=['POST'])
    app.add_url_rule('/next-image', 'next_image', pages.next_image, methods=['GET'])

    return app

def configure_ngrok(port):
    """Configure and start ngrok tunnel if requested."""
    use_ngrok = os.environ.get('USE_NGROK', '0').lower() in ('1', 'true', 'yes')
    if not use_ngrok:
        return None
        
    try:
        from pyngrok import ngrok
        
        # Set auth token if provided
        auth_token = os.environ.get('NGROK_AUTH_TOKEN')
        if auth_token:
            ngrok.set_auth_token(auth_token)
            
        # Start tunnel
        tunnel = ngrok.connect(port, bind_tls=True)
        print(f'Ngrok tunnel established: {tunnel.public_url}')
        return tunnel
    except Exception as e:
        print('Failed to start ngrok tunnel:', e)
        print('Install pyngrok with: pip install pyngrok')
        return None

if __name__ == '__main__':
    # Create Flask app
    app = create_app()
    
    # Configure server
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', '5000'))
    debug = os.environ.get('FLASK_DEBUG', '1') in ('1', 'true', 'True')
    
    # Optional ngrok tunnel
    # tunnel = configure_ngrok(port)
    
    try:
        # Start server
        print(f'Starting server on {host}:{port} (debug={debug})')
        app.run(host=host, port=port, debug=debug)
    finally:
        pass
        # Cleanup ngrok if used
        # if tunnel:
        #     try:
        #         from pyngrok import ngrok
        #         ngrok.disconnect(tunnel.public_url)
        #         ngrok.kill()
        #     except Exception:
        #         pass
