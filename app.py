from flask import Flask, render_template
from routes.api.chatbot import chatbot_bp
from routes.api.chat import chat_bp
from utils.chatbot_type_factory import chatbot_type_factory
from chatbot_types.text_chatbot import TextChatbotType
from storage.in_memory_storage import InMemoryStorage
from storage.json_file_storage import JSONFileStorage
import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    # Register blueprints
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    
    # Initialize storage
    app.storage = JSONFileStorage()
    
    # Register chatbot types
    chatbot_type_factory.register(TextChatbotType())
    
    @app.route('/')
    def dashboard():
        chatbots = app.storage.get_chatbots()
        return render_template('dashboard.html', chatbots=chatbots)

    @app.route('/chatbot/<id>/settings')
    def chatbot_settings(id):
        chatbot = app.storage.get_chatbot(id)
        if not chatbot:
            return render_template('error.html', message="Chatbot not found"), 404
        
        chatbot_type = chatbot_type_factory.get(chatbot.chatbot_type_id)
        if not chatbot_type:
            return render_template('error.html', message="Invalid chatbot type"), 400
        
        return render_template('settings.html', chatbot=chatbot, chatbot_type=chatbot_type)
    
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