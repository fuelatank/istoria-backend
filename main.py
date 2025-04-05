from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, File, HTTPException, UploadFile, WebSocket
from pydantic import BaseModel

from core.Chat_AI import generate_chat_response
from Speech_To_Text import speech_to_text
from core.Summary_AI import summarize_conversation
from core.file_service import download_audio, upload_audio
from core.summary_service import record_summary_to_db
from db import SessionDep, init_db


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    init_db()
    yield
    # Shutdown logic (if needed)


app = FastAPI(lifespan=lifespan)


class ChatRequest(BaseModel):
    content: str


class SummaryRequest(BaseModel):
    conversation: str


@app.post("/chat")
async def chat(request: ChatRequest, session: SessionDep):
    try:
        response = generate_chat_response(request.content)
        summary = summarize_conversation(request.content)

        record_summary_to_db(session, summary)

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
async def upload(session: SessionDep, file: UploadFile = File(...)):
    upload_result = await upload_audio(file)
    transcript = await speech_to_text(upload_result["filename"])

    response = generate_chat_response(transcript)
    summary = summarize_conversation(transcript)

    record_summary_to_db(session, summary)

    return {"response": response}


@app.get("/download/{filename}")
async def download(filename: str):
    return await download_audio(filename)


@app.get("/")
async def root():
    return {"message": "Moonshot48 Backend is running!"}
