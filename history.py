from typing import TypedDict, List, Optional
from collections import deque
import json


class Chat(TypedDict):
    role: str
    content: str


def create_assistant(message: str):
    return {"role": "assistant", "content": message}


def create_user(message: str):
    return {"role": "user", "content": message}


def create_system(message: str):
    return {"role": "system", "content": message}


class NoChatHistory:

    def __init__(
        self,
        prompt: str = "",
        use_system_prompt: bool = False,
        introduction: Optional[str] = None,
    ):
        self.use_system_prompt = use_system_prompt

        self.system_prompt: Chat | str
        self.set_system_prompt(prompt)
        self.introduction = create_assistant(introduction)

    def set_system_prompt(self, system_prompt: str):
        if self.use_system_prompt:
            self.system_prompt = create_system(system_prompt)
        else:
            self.system_prompt = system_prompt

    def get_history(self, user_text: str) -> List[Chat]:
        if self.use_system_prompt:
            return [self.system_prompt, create_user(user_text)]
        else:
            return [create_user(self.system_prompt + user_text)]

    def empty_history(self) -> List[Chat]:
        if self.introduction is None:
            return []
        return [self.introduction]
