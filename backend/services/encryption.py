import bcrypt
import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# A fixed secret key for demonstration. In a real-world scenario, this should be an environment variable.
AES_SECRET_KEY = b'16BytesSecretKey1234567890123456' # 32 bytes for AES-256

def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt for user credentials.
    Bcrypt is industry-standard as it includes salting and is computationally intensive.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    """Verifies a password against a bcrypt hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def encrypt_vault_data(plain_text: str) -> tuple[str, str]:
    """
    Encrypts vault passwords using AES-256.
    AES (Advanced Encryption Standard) is a symmetric encryption algorithm.
    We use CBC mode which requires an Initialization Vector (IV).
    Returns (encrypted_data_base64, iv_base64).
    """
    iv = os.urandom(AES.block_size)
    cipher = AES.new(AES_SECRET_KEY, AES.MODE_CBC, iv)
    encrypted_bytes = cipher.encrypt(pad(plain_text.encode('utf-8'), AES.block_size))
    
    return base64.b64encode(encrypted_bytes).decode('utf-8'), base64.b64encode(iv).decode('utf-8')

def decrypt_vault_data(encrypted_text: str, iv: str) -> str:
    """
    Decrypts vault passwords using AES-256.
    """
    encrypted_bytes = base64.b64decode(encrypted_text)
    iv_bytes = base64.b64decode(iv)
    cipher = AES.new(AES_SECRET_KEY, AES.MODE_CBC, iv_bytes)
    decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
    
    return decrypted_bytes.decode('utf-8')
