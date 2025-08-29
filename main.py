"""
Tilly FastAPI Application - The Web Interface
Bringing Tilly to the world through a beautiful API!
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional
import logging
from pathlib import Path
from tilly_intelligence_pipeline import TillyPipeline
from tilly_configuration_manager3 import get_config
from tilly_path_management import DATA_ROOT, get_log_path, ensure_data_dirs
from ocr import process_image, remember_text, memory, batch_process_folder
from ollama_client import generate_with_ollama

# Initialize FastAPI app early so decorators bind to the correct instance
app = FastAPI(
    title="Tilly - AI Companion",
    description="An empathetic AI companion focused on mental wellness and genuine human connection",
    version="1.0.0"
)

@app.get("/ollama/fibonacci")
async def ollama_fib():
    prompt = "Write me a function that outputs the Fibonacci sequence"
    code = generate_with_ollama(prompt)
    return {"fibonacci_code": code}

@app.get("/ollama/prime")
async def ollama_prime():
    prompt = "Write me a function that outputs the prime numbers"
    code = generate_with_ollama(prompt)
    return {"prime_code": code}

# Load .env early for local development
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# File logging to data/logs/tilly.log with rotation
try:
    ensure_data_dirs()
    from logging.handlers import RotatingFileHandler
    log_file = get_log_path("tilly.log")
    fh = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    root_logger = logging.getLogger()
    # Avoid duplicate handlers if running under reload
    if not any(isinstance(h, RotatingFileHandler) for h in root_logger.handlers):
        root_logger.addHandler(fh)
except Exception:
    pass


# Initialize Tilly pipeline
tilly = TillyPipeline()

# OCR paths
SCREENSHOTS_DIR = DATA_ROOT / "screenshots"


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    intent: str
    mood: str
    model_used: str


class HealthResponse(BaseModel):
    status: str
    components: dict


@app.on_event("startup")
async def startup_event():
    """Initialize Tilly on startup"""
    logger.info("🚀 Starting Tilly API server...")
    config = get_config()
    logger.info(f"🔧 Environment: {config.environment}")
    logger.info(f"🧠 Primary Model: {config.primary_model.provider}")
    try:
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        logger.info(f"📸 Screenshots directory: {SCREENSHOTS_DIR}")
    except Exception as e:
        logger.warning(f"Could not create screenshots directory: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    logger.info("🔒 Shutting down Tilly...")
    await tilly.close()


@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "Hello! I'm Tilly, your AI companion. I'm here to listen and support you.",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "health": "/health"
        }
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with Tilly - the main conversation endpoint.
    This is where the magic happens!
    """
    try:
        # Process through Tilly pipeline
        response, context = await tilly.process(request.message, request.session_id)

        # Return actual context details
        return ChatResponse(
            response=response,
            session_id=context.session_id,
            intent=context.intent.value,
            mood=context.mood.value,
            model_used=context.model_used or "unknown"
        )

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check the health of all Tilly components"""
    try:
        health_status = await tilly.health_check()

        return HealthResponse(
            status=health_status.get("pipeline", "unknown"),
            components=health_status
        )

    except Exception as e:
        logger.error(f"Health check error: {e}")
        return HealthResponse(
            status="unhealthy",
            components={"error": str(e)}
        )


@app.get("/hello/{name}")
async def say_hello(name: str):
    """Personalized greeting - keeping the original endpoint"""
    return {"message": f"Hello {name}! I'm Tilly, and I'm delighted to meet you. How are you feeling today?"}


# OCR endpoints
@app.post("/ocr/upload/")
async def ocr_upload(file: UploadFile = File(...)):
    """Upload an image, extract text via OCR, store in memory, and return text + summary."""
    try:
        filename = Path(file.filename).name  # basic sanitization
        file_path = SCREENSHOTS_DIR / filename
        data = await file.read()
        file_path.write_bytes(data)
        # process_image now returns (text, summary) and stores to memory internally
        text, summary = process_image(str(file_path))
        return {"filename": filename, "extracted_text": text, "summary": summary}
    except Exception as e:
        logger.error(f"OCR upload error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process the uploaded file")


@app.get("/ocr/memory/{query}")
def query_memory(query: str):
    """Query the OCR memory for similar stored texts."""
    try:
        results = memory.query(query_texts=[query], n_results=3)
        return {"query": query, "results": results}
    except Exception as e:
        logger.error(f"Memory query error: {e}")
        raise HTTPException(status_code=500, detail="Failed to query memory")


# Additional command endpoints for Tilly desktop assistant
@app.post("/tilly/ocr/")
def tilly_run_ocr():
    """Process any images currently in data/screenshots and store text in memory."""
    try:
        batch_process_folder(str(SCREENSHOTS_DIR))
        return {"status": "OCR complete"}
    except Exception as e:
        logger.error(f"/tilly/ocr error: {e}")
        raise HTTPException(status_code=500, detail="Failed to run OCR")


@app.post("/tilly/action/")
def tilly_perform_action():
    """Read a default screen region and optionally click based on OCR content. Returns screen_text."""
    try:
        # Lazy import to avoid issues in headless environments
        try:
            from desktop_automation import read_screen_and_click  # type: ignore
        except Exception as e:
            logger.error(f"Failed to import desktop_automation: {e}")
            raise HTTPException(status_code=500, detail="Desktop automation unavailable")
        result = read_screen_and_click((100, 100, 500, 300))
        return {"screen_text": result}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"/tilly/action error: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform action")


if __name__ == "__main__":
    import argparse
    import threading
    import uvicorn
    import os

    parser = argparse.ArgumentParser(description="Tilly: API and Desktop modes")
    parser.add_argument("--desktop", action="store_true", help="Launch desktop GUI and watcher instead of API server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if args.desktop:
        logger.info("Starting Tilly Desktop mode (GUI + watcher)...")
        # Lazy imports to avoid GUI libs in API-only environments
        try:
            from gui import start_gui
        except Exception as e:
            logger.error(f"Failed to load GUI: {e}")
            start_gui = None  # type: ignore
        try:
            from watcher import watch
        except Exception as e:
            logger.error(f"Failed to load watcher: {e}")
            watch = None  # type: ignore

        stop_event = threading.Event()

        threads = []
        if watch:
            t_watch = threading.Thread(target=watch, name="TillyWatcher", daemon=True)
            t_watch.start()
            threads.append(t_watch)
        # Autonomous loop
        try:
            from assistant_loop import run_loop  # type: ignore
            t_loop = threading.Thread(target=run_loop, args=(stop_event, 5.0), name="TillyAutoLoop", daemon=True)
            t_loop.start()
            threads.append(t_loop)
        except Exception as e:
            logger.error(f"Failed to start autonomous loop: {e}")
        # Start FastAPI API in background thread (api.py)
        try:
            api_thread = threading.Thread(target=lambda: uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True), daemon=True)
            api_thread.start()
            threads.append(api_thread)
        except Exception as e:
            logger.error(f"Failed to start API thread: {e}")

        # Start secure API in background (token-protected)
        try:
            secure_api_thread = threading.Thread(target=lambda: uvicorn.run("secure_api:app", host="127.0.0.1", port=8001, log_level="info"), daemon=True)
            secure_api_thread.start()
            threads.append(secure_api_thread)
        except Exception as e:
            logger.error(f"Failed to start secure API thread: {e}")

        # Start wake-word listener (Vosk) in background
        try:
            import listener  # type: ignore
            t_listener = threading.Thread(target=lambda: listener.run_listener(listener.on_command), name="TillyListener", daemon=True)
            t_listener.start()
            threads.append(t_listener)
        except Exception as e:
            logger.error(f"Failed to start listener: {e}")

        # Load plugins (best-effort)
        try:
            import plugin_loader  # type: ignore
            _plugins = plugin_loader.load_plugins()
            logger.info(f"Loaded plugins: {list(_plugins.keys())}")
        except Exception as e:
            logger.error(f"Failed to load plugins: {e}")

        # Ensure scheduler is initialized
        try:
            import scheduler  # noqa: F401
        except Exception as e:
            logger.error(f"Scheduler failed to initialize: {e}")

        if start_gui:
            t_gui = threading.Thread(target=start_gui, args=(stop_event,), name="TillyGUI", daemon=False)
            t_gui.start()
            threads.append(t_gui)

        # Wait for GUI thread to finish (user closes window)
        for t in threads:
            if t.name == "TillyGUI":
                t.join()
        # Signal other threads to stop if applicable
        stop_event.set()
        logger.info("Tilly Desktop mode exited.")
    else:
        uvicorn.run(app, host=args.host, port=args.port)
