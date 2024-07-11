
from flask import Blueprint, jsonify, request
from models.message import Message, Content
from models.thread import Thread
from storage.in_memory_storage import InMemoryStorage
from uuid import uuid4

message_bp = Blueprint('message', __name__)
storage = InMemoryStorage()

@message_bp.route('/', methods=['POST'])
def create_message():
    data = request.json
    thread_id = data.get('thread_id')
    if not thread_id:
        return jsonify({"error": "thread_id is required"}), 400
    
    thread = storage.get_thread(thread_id)
    if not thread:
        return jsonify({"error": "Thread not found"}), 404
    
    chatbot = storage.get_chatbot(thread.chatbot_id)
    if not chatbot:
        return jsonify({"error": "Chatbot not found"}), 404
    
    contents = [Content(type=c['type'], content=c['content']) for c in data.get('contents', [])]
    user_message = Message(
        thread_id=thread_id,
        role="user",
        contents=contents
    )
    storage.save_message(user_message)
    
    # Process the message using the appropriate chatbot
    chatbot_response = chatbot.get_chat_response(user_message, thread)
    storage.save_message(chatbot_response)
    
    return jsonify({
        "message": "Messages processed successfully",
        "user_message_id": user_message.id,
        "chatbot_response_id": chatbot_response.id
    }), 201

@message_bp.route('/<id>', methods=['DELETE'])
def hide_message(id):
    message = storage.get_message(id)
    if message:
        message.visible = False
        storage.save_message(message)
        return jsonify({"message": "Message hidden successfully"})
    return jsonify({"error": "Message not found"}), 404
