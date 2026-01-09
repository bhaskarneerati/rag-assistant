"""
Reset the local Chroma vector database.

Usage:
python scripts/reset_db.py
"""

import shutil
import os

CHROMA_PATH = "./backend/chroma_db"

def main():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print("Chroma DB reset successfully.")
    else:
        print("Chroma DB does not exist.")

if __name__ == "__main__":
    main()