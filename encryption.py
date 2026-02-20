"""Encryption utilities: Caesar and Fernet-like (fallback) implementations."""
import base64
import os
import time
from typing import Optional

try:
    from cryptography.fernet import Fernet
    _HAS_CRYPTO = True
except Exception:
    Fernet = None
    _HAS_CRYPTO = False


class EncryptionManager:
    def __init__(self):
        self.current_key: Optional[bytes] = None

    def generate_key(self) -> bytes:
        """Generate a key. Uses real Fernet if available, otherwise a base64 key."""
        if _HAS_CRYPTO:
            key = Fernet.generate_key()
            self.current_key = key
            return key
        else:
            raw = os.urandom(32)
            key = base64.urlsafe_b64encode(raw)
            self.current_key = key
            return key

    def get_key_string(self) -> Optional[str]:
        if not self.current_key:
            return None
        return self.current_key.decode('utf-8')

    def save_key_to_file(self, filename: str) -> None:
        with open(filename, 'wb') as f:
            f.write(self.current_key or b"")

    def load_key_from_file(self, filename: str) -> bool:
        try:
            with open(filename, 'rb') as f:
                data = f.read()
            self.current_key = data
            return True
        except FileNotFoundError:
            return False

    def load_key(self, key_str: str) -> None:
        if isinstance(key_str, str):
            self.current_key = key_str.encode('utf-8')
        elif isinstance(key_str, bytes):
            self.current_key = key_str
        else:
            raise TypeError('Key must be str or bytes')

    # Fernet-like methods (use real Fernet when available)
    def fernet_encrypt(self, plaintext: str) -> str:
        if not self.current_key:
            raise ValueError('No key loaded')
        if _HAS_CRYPTO:
            f = Fernet(self.current_key)
            token = f.encrypt(plaintext.encode('utf-8'))
            return token.decode('utf-8')
        else:
            key = base64.urlsafe_b64decode(self.current_key)
            data = plaintext.encode('utf-8')
            cipher = bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
            return base64.urlsafe_b64encode(cipher).decode('utf-8')

    def fernet_decrypt(self, token: str) -> str:
        if not self.current_key:
            raise ValueError('No key loaded')
        if _HAS_CRYPTO:
            f = Fernet(self.current_key)
            data = f.decrypt(token.encode('utf-8'))
            return data.decode('utf-8')
        else:
            cipher = base64.urlsafe_b64decode(token)
            key = base64.urlsafe_b64decode(self.current_key)
            data = bytes([cipher[i] ^ key[i % len(key)] for i in range(len(cipher))])
            return data.decode('utf-8')

    # Simple Caesar cipher for demonstration
    def caesar_encrypt(self, plaintext: str, shift: int = 3) -> str:
        result_chars = []
        for ch in plaintext:
            if 'a' <= ch <= 'z':
                result_chars.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
            elif 'A' <= ch <= 'Z':
                result_chars.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
            else:
                result_chars.append(ch)
        return ''.join(result_chars)

    def caesar_decrypt(self, ciphertext: str, shift: int = 3) -> str:
        return self.caesar_encrypt(ciphertext, -shift)
