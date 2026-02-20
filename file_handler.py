"""Simple file handler for encrypted files."""
import os
import time
from typing import List


class FileHandler:
    def __init__(self, default_dir: str = 'encrypted_files'):
        self.default_dir = default_dir
        os.makedirs(self.default_dir, exist_ok=True)

    def save_encrypted_text(self, text: str, method: str = 'fernet') -> str:
        ts = int(time.time())
        filename = f"{method}_{ts}.enc"
        path = os.path.join(self.default_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        return path

    def list_encrypted_files(self) -> List[str]:
        try:
            items = [f for f in os.listdir(self.default_dir) if os.path.isfile(os.path.join(self.default_dir, f))]
            items.sort()
            return items
        except FileNotFoundError:
            return []

    def load_encrypted_text(self, filename: str) -> str:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
