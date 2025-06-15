from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agents import Runner
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional, List
from agent_modules.agent_systems import triage_agent

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://hackathon-2-flax.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Metadata(BaseModel):
    timestamp: int
    userId: Optional[str] = None

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    metadata: Metadata

@app.post("/chat")
async def chat(query: ChatRequest):
    # Extract latest user message
    latest_user_message = None
    for message in reversed(query.messages):
        if message.role == "user":
            latest_user_message = message.content
            break

    context = Metadata(timestamp=query.metadata.timestamp, userId=query.metadata.userId)

    if not latest_user_message:
        return {"error": "No user message found."}
    
    result = await Runner.run(starting_agent=triage_agent, input=latest_user_message, context=context)
    return {"response": result.final_output}
