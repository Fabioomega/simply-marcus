from typing import TypedDict, List, Optional


class Chat(TypedDict):
    role: str
    content: str


def create_assistant(message: str):
    return {"role": "assistant", "content": message}


def create_user(message: str):
    return {"role": "user", "content": message}


def create_system(message: str):
    return {"role": "system", "content": message}


def get_first_user(conversations: List[Chat]) -> int:
    for i, c in enumerate(conversations):
        if c["role"] == "user":
            return i

    return -1


class ChatHistory:

    def __init__(
        self,
        prompt: str = "",
        use_system_prompt: bool = False,
        introduction: Optional[str] = None,
        max_conversation_size: int = 40,
    ):
        self.use_system_prompt = use_system_prompt
        self.max_conversation_size = max_conversation_size

        self.system_prompt: Chat | str
        self.set_system_prompt(prompt)
        self.introduction = create_assistant(introduction)

    def set_system_prompt(self, system_prompt: str):
        if self.use_system_prompt:
            self.system_prompt = create_system(system_prompt)
        else:
            self.system_prompt = system_prompt

    def create_history(self, conversation: List[Chat]) -> List[Chat]:
        if len(conversation) > self.max_conversation_size:
            conversation = conversation[
                len(conversation) - self.max_conversation_size :
            ]

        if self.use_system_prompt:
            if self.introduction is None:
                return [self.system_prompt] + conversation
            else:
                return [self.system_prompt, self.introduction] + conversation
        else:
            first_user_idx = get_first_user(conversation)
            if first_user_idx == -1:
                if self.introduction is None:
                    return [create_user(self.system_prompt)]
                else:
                    return [self.introduction, create_user(self.system_prompt)]

            if self.introduction is None:
                conversation[first_user_idx]["content"] = (
                    self.system_prompt + conversation[first_user_idx]["content"]
                )

                return conversation
            else:
                conversation[first_user_idx]["content"] = (
                    self.system_prompt + conversation[first_user_idx]["content"]
                )

                return [self.introduction] + conversation

    def empty_history(self) -> List[Chat]:
        if self.introduction is None:
            return []
        return [self.introduction]
