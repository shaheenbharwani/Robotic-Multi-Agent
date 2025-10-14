"""
Message Bus for Agent Communication
Enables asynchronous message passing between agents
"""
from collections import deque
from datetime import datetime

class Message:
    def __init__(self, sender, recipient, msg_type, content):
        self.sender = sender
        self.recipient = recipient
        self.msg_type = msg_type
        self.content = content
        self.timestamp = datetime.now()
    
    def __repr__(self):
        return f"[{self.sender} → {self.recipient}] {self.msg_type}: {self.content}"

class MessageBus:
    def __init__(self):
        self.messages = deque()
        self.message_history = []
        
    def send_message(self, sender, recipient, msg_type, content):
        """Send a message from one agent to another"""
        msg = Message(sender, recipient, msg_type, content)
        self.messages.append(msg)
        self.message_history.append(msg)
        return msg
    
    def get_messages(self, recipient):
        """Get all messages for a specific recipient"""
        recipient_msgs = [msg for msg in self.messages if msg.recipient == recipient or msg.recipient == "ALL"]
        # Remove retrieved messages
        self.messages = deque([msg for msg in self.messages if msg.recipient != recipient and msg.recipient != "ALL"])
        return recipient_msgs
    
    def broadcast(self, sender, msg_type, content):
        """Broadcast a message to all agents"""
        return self.send_message(sender, "ALL", msg_type, content)
    
    def get_history(self, limit=None):
        """Get message history"""
        if limit:
            return self.message_history[-limit:]
        return self.message_history
