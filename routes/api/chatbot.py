# File: routes/api/chatbot.py

from flask import Blueprint, jsonify, request, current_app
from chatbot_types.base import BaseChatbot
from models.thread import Thread
from models.message import Message, Content
from models.settings import Settings
from utils.chatbot_type_factory import chatbot_factory
from datetime import datetime

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/', methods=['GET'])
def get_chatbots():
    chatbots = current_app.storage.get_chatbots()
    return jsonify([chatbot.to_dict() for chatbot in chatbots])

@chatbot_bp.route('/<id>', methods=['GET'])
def get_chatbot(id):
    chatbot = current_app.storage.get_chatbot(id)
    if not chatbot:
        return jsonify({'error': 'Chatbot not found'}), 404
    return jsonify(chatbot.to_dict())

@chatbot_bp.route('/', methods=['POST'])
def create_chatbot():
    data = request.json
    if not data or 'name' not in data or 'type' not in data:
        return jsonify({'error': 'Name and type are required'}), 400

    chatbot_class = chatbot_factory.get(data['type'])
    if not chatbot_class:
        return jsonify({'error': 'Invalid chatbot type'}), 400

    settings = Settings(
        general=data.get('general_settings', {}),
        type_specific=data.get('type_specific_settings', {})
    )

    chatbot = chatbot_class(
        name=data['name'],
        settings=settings,
        created_at=datetime.fromisoformat(data['created_at']) if 'created_at' in data else None
    )

    try:
        chatbot.apply_settings()
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    current_app.storage.save_chatbot(chatbot)
    return jsonify(chatbot.to_dict()), 201

@chatbot_bp.route('/<id>', methods=['PUT'])
def update_chatbot(id):
    chatbot = current_app.storage.get_chatbot(id)
    if not chatbot:
        return jsonify({'error': 'Chatbot not found'}), 404

    data = request.json
    if 'name' in data:
        chatbot.name = data['name']
    if 'type' in data and data['type'] != chatbot.__class__.__name__.lower():
        return jsonify({'error': 'Changing chatbot type is not supported'}), 400

    if 'general_settings' in data:
        chatbot.settings.update(general=data['general_settings'])
    if 'type_specific_settings' in data:
        chatbot.settings.update(type_specific=data['type_specific_settings'])

    try:
        chatbot.apply_settings()
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    current_app.storage.save_chatbot(chatbot)
    return jsonify(chatbot.to_dict())

@chatbot_bp.route('/<id>', methods=['DELETE'])
def delete_chatbot(id):
    chatbot = current_app.storage.get_chatbot(id)
    if not chatbot:
        return jsonify({'error': 'Chatbot not found'}), 404
    
    current_app.storage.delete_chatbot(id)
    return '', 204

@chatbot_bp.route('/<id>/settings', methods=['GET'])
def get_settings(id):
    chatbot = current_app.storage.get_chatbot(id)
    if not chatbot:
        return jsonify({'error': 'Chatbot not found'}), 404
    
    return jsonify(chatbot.settings.to_dict())

@chatbot_bp.route('/<id>/settings', methods=['PUT'])
def update_settings(id):
    chatbot = current_app.storage.get_chatbot(id)
    if not chatbot:
        return jsonify({'error': 'Chatbot not found'}), 404
    
    data = request.json
    general_settings = data.get('general')
    type_specific_settings = data.get('type_specific')
    
    if general_settings:
        chatbot.settings.update(general=general_settings)
    
    if type_specific_settings:
        try:
            if chatbot.validate_settings(type_specific_settings):
                chatbot.settings.update(type_specific=type_specific_settings)
            else:
                return jsonify({'error': 'Invalid type-specific settings'}), 400
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    
    try:
        chatbot.apply_settings()
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    current_app.storage.save_chatbot(chatbot)
    return jsonify(chatbot.settings.to_dict())

@chatbot_bp.route('/<id>/settings/<setting_key>', methods=['GET'])
def get_setting(id, setting_key):
    chatbot = current_app.storage.get_chatbot(id)
    if not chatbot:
        return jsonify({'error': 'Chatbot not found'}), 404
    
    value = chatbot.settings.get(setting_key)
    if value is None:
        return jsonify({'error': 'Setting not found'}), 404
    
    return jsonify({setting_key: value})

@chatbot_bp.route('/<id>/settings/<setting_key>', methods=['PUT'])
def update_setting(id, setting_key):
    chatbot = current_app.storage.get_chatbot(id)
    if not chatbot:
        return jsonify({'error': 'Chatbot not found'}), 404
    
    value = request.json.get('value')
    if value is None:
        return jsonify({'error': 'Value is required'}), 400
    
    if setting_key in chatbot.get_default_settings():
        try:
            if chatbot.validate_settings({setting_key: value}):
                chatbot.settings.set_type_specific(setting_key, value)
            else:
                return jsonify({'error': 'Invalid setting value'}), 400
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    else:
        chatbot.settings.set_general(setting_key, value)
    
    try:
        chatbot.apply_settings()
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    current_app.storage.save_chatbot(chatbot)
    return jsonify({setting_key: value})

@chatbot_bp.route('/<id>/thread', methods=['POST'])
def create_thread(id):
    chatbot = current_app.storage.get_chatbot(id)
    if not chatbot:
        return jsonify({'error': 'Chatbot not found'}), 404

    thread = Thread(chatbot_id=id)
    current_app.storage.save_thread(thread)

    return jsonify(thread.to_dict()), 201

@chatbot_bp.route('/<id>/thread/<thread_id>/messages', methods=['GET'])
def get_thread_messages(id, thread_id):
    chatbot = current_app.storage.get_chatbot(id)
    if not chatbot:
        return jsonify({'error': 'Chatbot not found'}), 404

    thread = current_app.storage.get_thread(thread_id)
    if not thread or thread.chatbot_id != id:
        return jsonify({'error': 'Thread not found'}), 404

    messages = current_app.storage.get_messages(query={"thread_id": thread_id})
    return jsonify([message.to_dict() for message in messages])

@chatbot_bp.route('/<id>/chat', methods=['POST'])
def chat(id):
    chatbot = current_app.storage.get_chatbot(id)
    if not chatbot:
        return jsonify({'error': 'Chatbot not found'}), 404

    data = request.json
    thread_id = data.get('thread_id')
    content = data.get('content')

    if not thread_id or not content:
        return jsonify({"error": "thread_id and content are required"}), 400

    thread = current_app.storage.get_thread(thread_id)
    if not thread or thread.chatbot_id != id:
        return jsonify({'error': 'Thread not found'}), 404

    user_message = Message(
        thread_id=thread_id,
        role="user",
        contents=[Content(type="text", content=content)]
    )
    current_app.storage.save_message(user_message)

    response_message = chatbot.chat(user_message, thread)
    current_app.storage.save_message(response_message)

    return jsonify(response_message.to_dict())

@chatbot_bp.route('/<id>/logs', methods=['GET'])
def get_chat_logs(id):
    chatbot = current_app.storage.get_chatbot(id)
    if not chatbot:
        return jsonify({'error': 'Chatbot not found'}), 404

    threads = current_app.storage.get_threads(query={"chatbot_id": id})
    logs = []
    for thread in threads:
        messages = current_app.storage.get_messages(query={"thread_id": thread.id})
        messages.sort(key=lambda message: message.created_at)
        logs.append({
            'thread_id': thread.id,
            'created_at': thread.created_at.isoformat(),
            'messages': [message.to_dict() for message in messages]
        })

    logs.sort(key=lambda log: log['created_at'], reverse=True)
    return jsonify(logs)