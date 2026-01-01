from fastapi import FastAPI, Body

app = FastAPI()
messages: dict[str, str] = {}


@app.get("/message/{key}")
async def get_message(key: str):
    return messages.get(key, "")


@app.post("/message/{key}")
async def post_message(key: str, message: str = Body()):
    messages[key] = message

    return ""
