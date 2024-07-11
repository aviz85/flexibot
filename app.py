# File: app.py

from flask import Flask, render_template
from routes.api.chatbot import chatbot_bp
from routes.api.chat import chat_bp
from utils.chatbot_type_factory import chatbot_factory
from chatbot_types.text_chatbot import TextChatbot
from chatbot_types.claude.claude_chatbot import ClaudeChatbot
from storage.json_file_storage import JSONFileStorage
import config
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    # Register blueprints
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    
    # Initialize storage
    app.storage = JSONFileStorage()
    
    # Register chatbot types
    chatbot_factory.register(TextChatbot)
    chatbot_factory.register(ClaudeChatbot)
    
    @app.route('/')
    def dashboard():
        chatbots = app.storage.get_chatbots()
        return render_template('dashboard.html', chatbots=chatbots)

    @app.route('/chatbot/<id>/settings')
    def chatbot_settings(id):
        chatbot = app.storage.get_chatbot(id)
        if not chatbot:
            return render_template('error.html', message="Chatbot not found"), 404
        
        return render_template('settings.html', chatbot=chatbot)
    
    @app.route('/chatbot/<id>/chat')
    def chatbot_chat(id):
        chatbot = app.storage.get_chatbot(id)
        if not chatbot:
            return render_template('error.html', message="Chatbot not found"), 404
        return render_template('chat.html', chatbot=chatbot)

    @app.route('/chatbot/<id>/logs')
    def chatbot_logs(id):
        chatbot = app.storage.get_chatbot(id)
        if not chatbot:
            return render_template('error.html', message="Chatbot not found"), 404
        
        threads = app.storage.get_threads(query={"chatbot_id": id})
        return render_template('chat_logs.html', chatbot=chatbot, threads=threads)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port="5002")