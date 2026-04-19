import uuid
from datetime import datetime


class Message:
    def __init__(
        self,
        sender,
        receiver,
        content,
        msg_type="TASK",
        status="REQUEST",
        metadata=None,
        parent_id=None,
    ):
        self.id = str(uuid.uuid4())
        self.sender = sender
        self.receiver = receiver
        self.type = msg_type  # TASK / RESPONSE / ERROR
        self.status = status  # REQUEST / SUCCESS / FAILED
        self.content = content
        self.metadata = metadata or {}
        self.parent_id = parent_id
        self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self):
        return self.__dict__
