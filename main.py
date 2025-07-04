import sys
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.get("/")
async def health_check():
    """
    Health check endpoint to verify the API is up.
    """
    return {"status": "Langchain Multiagent API is running"}

@app.post("/refresh_token")
async def refresh_token():
    """
    Launches your refresh_token.py as a subprocess.
    Returns stdout on success or raises 500 with stderr.
    """
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
    """
    Launches your main_assistant.py, passing the user’s text.
    Expects that main_assistant.py consumes a single CLI arg (the prompt)
    and prints its result to stdout.
    """
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "main_assistant.py", req.text,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, err = await proc.communicate()
    if proc.returncode != 0:
        raise HTTPException(status_code=500, detail=err.decode().strip())
    return {"result": out.decode().strip()}

# If you prefer to pass a flag, e.g. `--text`, just change the args list above to:
# [sys.executable, "main_assistant.py", "--text", req.text, ...]
