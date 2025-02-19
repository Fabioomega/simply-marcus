from ollama import AsyncClient
from typing import TypedDict, Optional, List
from history import ChatHistory, Chat
from environment_loader import Environment


class ChatBotOutput(TypedDict):
    content: str
    think: str


class ChatBot:

    def __init__(
        self,
        host: str = "http://localhost:11434",
        system_prompt: str = "",
        use_system_prompt: bool = False,
        model: str = "qwen2.5:7b",
        max_conversation_size: int = 40,
        introduction: Optional[str] = None,
        environment_path: Optional[str] = None,
    ):
        if not environment_path is None:
            env = Environment(environment_path)
            host = str(env.get("host", host))
            system_prompt = str(env.get("system_prompt", system_prompt))
            use_system_prompt = bool(env.get("use_system_prompt", use_system_prompt))
            model = str(env.get("model", model))
            introduction = str(env.get("introduction", introduction))
            max_conversation_size = str(
                env.get("max_conversation_size", max_conversation_size)
            )

        self.async_client = AsyncClient(host=host)
        self.history = ChatHistory(
            system_prompt,
            use_system_prompt=use_system_prompt,
            introduction=introduction,
        )
        self.model = model

    async def async_chat(self, chat_history: List[Chat]):
        async for part in await self.async_client.chat(
            self.model, messages=self.history.create_history(chat_history), stream=True
        ):
            yield part["message"]["content"]

    def reset_chat(self): ...

    def get_history(self):
        return self.history.empty_history()
