# main.py (or your app entrypoint)
import sys, asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# 1️⃣ Add this CORS middleware block right after creating `app`:
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # your Vite dev server
        "http://localhost:8080",  # if you use a different port
        "http://localhost:8000",  # if you use a different port
        "https://api.s1mpleai.org",
        "https://s1mpleai.org",
        "https://s1mple-ai-2025.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],        # GET, POST, OPTIONS, etc.
    allow_headers=["*"],        # Content-Type, X-*, etc.
)

class TextRequest(BaseModel):
    text: str

@app.get("/")
async def health_check():
    return {"status": "Langchain Multiagent API is running"}

@app.post("/refresh_token")
async def refresh_token():
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "refresh_token.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, err = await proc.communicate()
    if proc.returncode != 0:
        raise HTTPException(status_code=500, detail=err.decode().strip())
    return {"output": out.decode().strip()}

@app.post("/run")
async def run_agent(req: TextRequest):
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "main_assistant.py", req.text,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, err = await proc.communicate()
    if proc.returncode != 0:
        raise HTTPException(status_code=500, detail=err.decode().strip())
    return {"result": out.decode().strip()}
