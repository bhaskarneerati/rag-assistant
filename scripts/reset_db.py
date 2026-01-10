"""
CLI script to reset the vector database.

This script deletes the persistence directory used by ChromaDB. This is useful
when you want to wipe all indexed documents and start from scratch.

Usage:
    python scripts/reset_db.py
"""
import shutil
import os

CHROMA_PATH = "./backend/chroma_db"

def main():
    """
    Checks if the database directory exists and deletes it if it does.
    """
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print("Chroma DB reset successfully.")
    else:
        print("Chroma DB does not exist.")

if __name__ == "__main__":
    main()