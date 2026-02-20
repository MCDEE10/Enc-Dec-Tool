from encryption import EncryptionManager
from file_handler import FileHandler


def smoke_test():
    mgr = EncryptionManager()
    fh = FileHandler()

    # Test Fernet-like flow
    plain = "The quick brown fox jumps over 13 lazy dogs."
    key = mgr.generate_key()
    token = mgr.fernet_encrypt(plain)

    path = fh.save_encrypted_text(token, method='fernet')
    loaded = fh.load_encrypted_text(path)

    # Decrypt using same manager (key is loaded)
    out = mgr.fernet_decrypt(loaded)
    assert out == plain, f"Fernet flow failed: {out!r} != {plain!r}"

    # Test Caesar
    c = mgr.caesar_encrypt("abc XYZ", 4)
    d = mgr.caesar_decrypt(c, 4)
    assert d == "abc XYZ", "Caesar cipher failed"

    print("SMOKE TEST PASSED")


if __name__ == '__main__':
    smoke_test()
