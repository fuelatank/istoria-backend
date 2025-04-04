from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from Chat_AI import generate_chat_response
from Summary_AI import summarize_conversation
from file_service import download_audio, upload_audio

app = FastAPI()


class ChatRequest(BaseModel):
    content: str


class SummaryRequest(BaseModel):
    conversation: str


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = generate_chat_response(request.content)
        summary = summarize_conversation(request.content)
        if response is None:
            raise HTTPException(status_code=500, detail="No response generated.")
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/summary")
async def summarize(request: SummaryRequest):
    try:
        summary = summarize_conversation(request.conversation)
        if not summary:
            raise HTTPException(status_code=500, detail="No summary generated.")
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return upload_audio(file)

@app.get("/download/{filename}")
async def download(filename: str):
    return download_audio(filename)

@app.get("/")
async def root():
    return {"message": "Moonshot48 Backend is running!"}
