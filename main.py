from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from chat import ChatBot


class ChatBotInput(BaseModel):
    text: str


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
chatbot = ChatBot(environment_path="env.json")


@app.post("/chat")
async def chat(inp: ChatBotInput):
    return StreamingResponse(chatbot.async_chat(inp.text))


@app.delete("/history")
def reset_chat():
    chatbot.reset_chat()
    return {"status": 200, "response": "No history here but removed anyway!"}


@app.get("/history")
def get_history():
    return chatbot.get_history()


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
