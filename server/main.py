from fastapi import FastAPI, Body
from fastapi.responses import PlainTextResponse


app = FastAPI()
messages: dict[str, str] = {}


@app.get("/message/{key}", response_class=PlainTextResponse)
async def get_message(key: str):
    return messages.get(key, "")


@app.post("/message/{key}", response_class=PlainTextResponse)
async def post_message(key: str, message: str = Body()):
    messages[key] = message

    return ""
