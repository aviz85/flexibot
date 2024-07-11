
from abc import ABC, abstractmethod

class BaseStorage(ABC):
    @abstractmethod
    def save_chatbot(self, chatbot):
        pass

    @abstractmethod
    def get_chatbot(self, chatbot_id):
        pass

    @abstractmethod
    def get_chatbots(self):
        pass

    @abstractmethod
    def save_thread(self, thread):
        pass

    @abstractmethod
    def get_thread(self, thread_id):
        pass

    @abstractmethod
    def get_threads(self):
        pass

    @abstractmethod
    def save_message(self, message):
        pass

    @abstractmethod
    def get_message(self, message_id):
        pass

    @abstractmethod
    def get_messages(self):
        pass

    @abstractmethod
    def get_messages_for_thread(self, thread_id):
        pass
