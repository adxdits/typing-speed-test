import hashlib
import os

def hash_password(password: str) -> str:
    """Hash a password for storing."""
    salt = os.urandom(16)  # Generate a random salt
    salt_hex = salt.hex()  # Convert the salt to a hex string
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    password_hash_hex = password_hash.hex()
    return f"{salt_hex}${password_hash_hex}"

def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verify a stored password against one provided by user"""
    salt_hex, stored_password_hash_hex = stored_password.split('$')
    salt = bytes.fromhex(salt_hex)
    stored_password_hash = bytes.fromhex(stored_password_hash_hex)

    password_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)

    return password_hash == stored_password_hash
