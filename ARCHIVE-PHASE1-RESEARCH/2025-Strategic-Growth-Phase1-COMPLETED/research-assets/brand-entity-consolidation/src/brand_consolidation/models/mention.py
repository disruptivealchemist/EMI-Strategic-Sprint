class Mention:
    def __init__(self, source, content, timestamp):
        self.source = source
        self.content = content
        self.timestamp = timestamp

    def __repr__(self):
        return f"Mention(source={self.source}, content={self.content}, timestamp={self.timestamp})"

    def to_dict(self):
        return {
            "source": self.source,
            "content": self.content,
            "timestamp": self.timestamp
        }