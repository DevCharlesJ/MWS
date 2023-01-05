from datetime import datetime

class Message():
    def __init__(self, author, text, target=None):
        self.author = author
        self.text = text
        self.target = target

        dt = datetime.now()
        meridiem = "PM" if dt.hour >= 12 and dt.hour < 24 else "AM"
        self.created = f"{dt.month:02}/{dt.day:02}/{dt.year} at {dt.hour:02}:{dt.minute:02} {meridiem}"


class User():
    def __init__(self, username=None):
        self.username = username or "UNKNOWN"