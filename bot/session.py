from dataclasses import dataclass, field
from openai.types.chat import ChatCompletionMessageParam

HISTORY_LIMIT = 20


@dataclass
class Session:
    user_id: int
    messages: list[ChatCompletionMessageParam] = field(default_factory=list)

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > HISTORY_LIMIT:
            self.messages = self.messages[-HISTORY_LIMIT:]


_sessions: dict[int, Session] = {}


def get_session(user_id: int) -> Session:
    if user_id not in _sessions:
        _sessions[user_id] = Session(user_id=user_id)
    return _sessions[user_id]
