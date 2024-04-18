# alert.py
from datetime import datetime

class Alert:
    def __init__(self, id, subscription_id, message, sent_at=None):
        self.id = id
        self.subscription_id = subscription_id
        self.message = message
        self.sent_at = sent_at if sent_at else datetime.now()

    def __str__(self):
        return f"Alert(id={self.id}, subscription_id={self.subscription_id}, message={self.message}, sent_at={self.sent_at})"

    def to_dict(self):
        return {
            "id": self.id,
            "subscription_id": self.subscription_id,
            "message": self.message,
            "sent_at": self.sent_at.isoformat() if isinstance(self.sent_at, datetime) else None,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            subscription_id=data.get("subscription_id"),
            message=data.get("message"),
            sent_at=datetime.fromisoformat(data.get("sent_at")) if data.get("sent_at") else None,
        )