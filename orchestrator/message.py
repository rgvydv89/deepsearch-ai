class Message:
    def __init__(self, sender, receiver, content, metadata=None):
        self.sender = sender          # who sent
        self.receiver = receiver      # who should handle
        self.content = content        # main data
        self.metadata = metadata or {}  # extra info

    def __repr__(self):
        return f"""
        Message(
            from={self.sender},
            to={self.receiver},
            content={self.content},
            metadata={self.metadata}
        )
        """