from cryptography.fernet import Fernet
import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_key():
    return Fernet.generate_key()

def get_encryption_key(password: str, salt: bytes = None):
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def encrypt_file(file_path: str, key: bytes):
    f = Fernet(key)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    encrypted_path = file_path + '.encrypted'
    with open(encrypted_path, 'wb') as file:
        file.write(encrypted_data)
    return encrypted_path

def decrypt_file(encrypted_file_path: str, key: bytes, output_path: str = None):
    f = Fernet(key)
    with open(encrypted_file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    
    if output_path is None:
        output_path = encrypted_file_path.replace('.encrypted', '.decrypted')
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'wb') as file:
        file.write(decrypted_data)
    return output_path 