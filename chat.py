from ollama import AsyncClient
from typing import TypedDict, Optional
from history import NoChatHistory
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

        self.async_client = AsyncClient(host=host)
        self.history = NoChatHistory(
            system_prompt,
            use_system_prompt=use_system_prompt,
            introduction=introduction,
        )
        self.model = model

    async def async_chat(self, text: str):
        async for part in await self.async_client.chat(
            self.model, messages=self.history.get_history(text), stream=True
        ):
            yield part["message"]["content"]

    def reset_chat(self): ...

    def get_history(self):
        return self.history.empty_history()
