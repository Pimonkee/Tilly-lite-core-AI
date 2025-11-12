#!/usr/bin/env python3
"""
Tilly AI - Main Entry Point
An empathetic AI companion focused on mental wellness
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    import argparse
    import uvicorn
    
    parser = argparse.ArgumentParser(description="Tilly AI - Your Empathetic AI Companion")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    args = parser.parse_args()
    
    print("""
    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║         🤖 Tilly AI Companion v1.0            ║
    ║    An Empathetic AI for Mental Wellness       ║
    ║                                               ║
    ╚═══════════════════════════════════════════════╝
    """)
    
    print(f"🚀 Starting Tilly on http://{args.host}:{args.port}")
    print(f"📚 API Documentation: http://{args.host}:{args.port}/docs")
    print(f"💬 Chat Interface: http://{args.host}:{args.port}/\n")
    
    # Run the FastAPI application
    uvicorn.run(
        "tilly.api.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )
