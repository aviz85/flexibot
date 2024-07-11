# FlexiBot

FlexiBot is a flexible chatbot framework that allows you to create and manage multiple types of chatbots through a unified interface.

## Features

- Create and manage multiple chatbots
- Supports different types of chatbots (Text, Claude, etc.)
- RESTful API for chatbot operations
- Web interface for chatbot management and interaction

## Getting Started

### Prerequisites

- Python 3.8+
- Flask
- (List other dependencies)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/flexibot.git
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory and add the following:
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   ANTHROPIC_API_KEY=your_anthropic_api_key (if using Claude)
   ```

4. Run the application:
   ```
   python app.py
   ```

## Chatbot Types

### BaseChatbot

The `BaseChatbot` class is the foundation for all chatbot types in FlexiBot. It provides the basic structure and functionality that all chatbots share.

### TextChatbot

A simple chatbot that echoes user messages.

### ClaudeChatbot

A more advanced chatbot that uses the Anthropic Claude API for generating responses.

## Creating a New Chatbot Type

To create a new chatbot type:

1. Create a new class that inherits from `BaseChatbot` or `ConversationalChatbot`.
2. Implement the required methods: `chat`, `get_default_settings`, and `validate_settings`.
3. Register your new chatbot type in the `ChatbotFactory`.

Example:

```python
from chatbot_types.base import BaseChatbot

class MyNewChatbot(BaseChatbot):
    def chat(self, message, thread):
        # Implement chat logic
        pass

    @staticmethod
    def get_default_settings():
        return {
            "my_setting": "default_value"
        }

    @staticmethod
    def validate_settings(settings):
        return "my_setting" in settings and isinstance(settings["my_setting"], str)

# In chatbot_type_factory.py
chatbot_factory.register(MyNewChatbot)
```

## API Documentation

(Provide details about your API endpoints here)

## Contributing

(Provide guidelines for contributing to the project)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.