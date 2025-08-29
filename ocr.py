import os
from PIL import Image
import pytesseract
from chromadb import Client
from chromadb.utils import embedding_functions
import logging

logging.basicConfig(level=logging.INFO)

# --- Vector memory setup ---
chroma_client = Client()
embedding = embedding_functions.DefaultEmbeddingFunction()
memory = chroma_client.create_collection("tilly_memory", embedding_function=embedding)

def process_image(file_path: str):
    """Extract text from an image file, store in memory, and return (text, summary)."""
    if not os.path.exists(file_path):
        logging.warning(f"File not found: {file_path}")
        return "", ""
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    logging.info(f"OCR processed: {file_path}")
    # Store and summarize
    try:
        from memory import remember_text as mem_remember_text, summarize_text
        mem_remember_text(text)
        summary = summarize_text(text)
    except Exception:
        summary = ""
    return text, summary

def remember_text(text: str):
    """Store extracted text in vector memory."""
    if text.strip():
        memory.add(documents=[text], ids=[str(hash(text))])
        logging.info("Text stored in Tilly memory.")

def batch_process_folder(folder_path: str):
    """Process all images in a folder; store in memory and print summaries."""
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

