
import os
import importlib

def load_chatbot_types():
    chatbot_types = {}
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    for item in os.listdir(current_dir):
        if os.path.isdir(os.path.join(current_dir, item)) and not item.startswith('__'):
            try:
                # Import the module
                module = importlib.import_module(f'chatbot_types.{item}.{item}_chatbot')

                # Convert item to PascalCase for class name
                chatbot_class = f'{item.capitalize()}Chatbot'
                chatbot_types[item] = chatbot_class
            except (ImportError, AttributeError) as e:
                print(f"Error loading chatbot type {item}: {str(e)}")
    
    return chatbot_types

CHATBOT_TYPES = load_chatbot_types()
