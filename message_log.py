class MessageLog:
    def __init__(self, max_messages=5):
        self.messages = []  # List of {'text': str, 'color': tuple}
        self.max_messages = max_messages

    def add_message(self, message_text, color=(255, 255, 255)):
        """Adds a new message to the log."""
        new_message = {'text': message_text, 'color': color}
        self.messages.append(new_message)
        
        # Ensure the log doesn't exceed max_messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_display_messages(self):
        """Returns the current list of messages to be displayed."""
        return self.messages
