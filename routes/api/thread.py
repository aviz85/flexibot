
from flask import Blueprint, jsonify, request
from models.thread import Thread
from storage.in_memory_storage import InMemoryStorage

thread_bp = Blueprint('thread', __name__)
storage = InMemoryStorage()

@thread_bp.route('/', methods=['GET'])
def get_threads():
    threads = storage.get_threads()
    return jsonify([thread.to_dict() for thread in threads])

@thread_bp.route('/<id>', methods=['GET'])
def get_thread(id):
    thread = storage.get_thread(id)
    if thread:
        return jsonify(thread.to_dict())
    return jsonify({"error": "Thread not found"}), 404

@thread_bp.route('/', methods=['POST'])
def create_thread():
    data = request.json
    chatbot_id = data.get('chatbot_id')
    if not chatbot_id:
        return jsonify({"error": "chatbot_id is required"}), 400
    
    thread = Thread(chatbot_id=chatbot_id)
    storage.save_thread(thread)
    return jsonify({"message": "Thread created successfully", "thread_id": thread.id}), 201

@thread_bp.route('/<id>', methods=['DELETE'])
def hide_thread(id):
    thread = storage.get_thread(id)
    if thread:
        thread.visible = False
        storage.save_thread(thread)
        return jsonify({"message": "Thread hidden successfully"})
    return jsonify({"error": "Thread not found"}), 404
