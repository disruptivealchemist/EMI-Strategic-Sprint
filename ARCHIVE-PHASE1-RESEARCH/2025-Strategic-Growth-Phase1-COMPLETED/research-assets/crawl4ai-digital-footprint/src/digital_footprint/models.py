class Footprint:
    def __init__(self, url, timestamp, data):
        self.url = url
        self.timestamp = timestamp
        self.data = data

class UserProfile:
    def __init__(self, username, email, preferences):
        self.username = username
        self.email = email
        self.preferences = preferences

    def update_preferences(self, new_preferences):
        self.preferences = new_preferences

    def __repr__(self):
        return f"UserProfile(username={self.username}, email={self.email}, preferences={self.preferences})"