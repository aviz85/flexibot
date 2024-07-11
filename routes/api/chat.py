# File: routes/api/chat.py

from flask import Blueprint, jsonify, request, current_app
from models.message import Message, Content
from models.thread import Thread

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/<chatbot_id>', methods=['POST'])
def chat(chatbot_id):
    data = request.json
    thread_id = data.get('thread_id')
    content = data.get('content')
    
    if not thread_id or not content:
        return jsonify({"error": "thread_id and content are required"}), 400
    
    try:
        chatbot = current_app.storage.get_chatbot(chatbot_id)
        if not chatbot:
            return jsonify({'error': 'Invalid chatbot ID'}), 404
        
        thread = current_app.storage.get_thread(thread_id)
        if not thread:
            # Create a new thread if it doesn't exist
            thread = Thread(chatbot_id=chatbot_id)
            current_app.storage.save_thread(thread)
        
        user_message = Message(
            thread_id=thread.id,
            role="user",
            contents=[Content(type="text", content=content)]
        )
        current_app.storage.save_message(user_message)
        
        response_message = chatbot.chat(user_message, thread)
        current_app.storage.save_message(response_message)
        
        return jsonify(response_message.to_dict())
    except Exception as e:
        current_app.logger.error(f"Error in chat processing: {str(e)}")
        return jsonify({'error': 'An error occurred while processing the chat'}), 500

@chat_bp.route('/thread/<thread_id>', methods=['GET'])
def get_thread_messages(thread_id):
    try:
        thread = current_app.storage.get_thread(thread_id)
        if not thread:
            return jsonify({'error': 'Invalid thread ID'}), 404
        
        messages = current_app.storage.get_messages(query={"thread_id": thread_id})
        return jsonify([message.to_dict() for message in messages])
    except Exception as e:
        current_app.logger.error(f"Error retrieving thread messages: {str(e)}")
        return jsonify({'error': 'An error occurred while retrieving messages'}), 500