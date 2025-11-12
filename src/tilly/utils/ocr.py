import os
import logging

logging.basicConfig(level=logging.INFO)

# Optional dependencies for OCR functionality
try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    logging.warning("OCR dependencies not available (PIL, pytesseract). OCR features will be disabled.")

try:
    from chromadb import Client
    from chromadb.utils import embedding_functions
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    logging.warning("ChromaDB not available. Vector memory features will be disabled.")

# --- Vector memory setup ---
if CHROMADB_AVAILABLE:
    chroma_client = Client()
    embedding = embedding_functions.DefaultEmbeddingFunction()
    memory = chroma_client.create_collection("tilly_memory", embedding_function=embedding)
else:
    memory = None

def process_image(file_path: str):
    """Extract text from an image file, store in memory, and return (text, summary)."""
    if not OCR_AVAILABLE:
        return "", "OCR not available"
    
    if not os.path.exists(file_path):
        logging.warning(f"File not found: {file_path}")
        return "", ""
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    logging.info(f"OCR processed: {file_path}")
    # Store and summarize
    try:
        if CHROMADB_AVAILABLE:
            remember_text(text)
        summary = text[:100] + "..." if len(text) > 100 else text
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        summary = ""
    return text, summary

def remember_text(text: str):
    """Store extracted text in vector memory."""
    if not CHROMADB_AVAILABLE or memory is None:
        logging.warning("Vector memory not available")
        return
    
    if text.strip():
        memory.add(documents=[text], ids=[str(hash(text))])
        logging.info("Text stored in Tilly memory.")

def batch_process_folder(folder_path: str):
    """Process all images in a folder; store in memory and print summaries."""
    if not OCR_AVAILABLE:
        logging.warning("OCR not available, cannot process folder")
        return
    
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
            full_path = os.path.join(folder_path, file_name)
            text, summary = process_image(full_path)
            try:
                print(f"Processed {file_name}: {summary}")
            except Exception:
                pass

def process_and_remember_image(file_path: str):
    """Process an image, store its text in vector memory (handled in process_image)."""
    text, summary = process_image(file_path)
    return text, summary

