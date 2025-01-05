import hashlib
import rsa

def compute_hash(filepath):
    """Computes the SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def rsa_encrypt(data, public_key):
    """Encrypts data using an RSA public key."""
    return rsa.encrypt(data, public_key)

def rsa_decrypt(data, private_key):
    """Decrypts data using an RSA private key."""
    return rsa.decrypt(data, private_key)

def display_progress(sent, total):
    """Displays the progress of data transfer."""
    progress = (sent / total) * 100
    print(f"Progress: {progress:.2f}% ({sent}/{total} bytes)", end='\r')
