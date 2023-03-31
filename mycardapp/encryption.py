
import base64
from Crypto.Cipher import AES

# Define the key and initialization vector (IV)
key = b'secretkey1234567'
iv = b'iv12345678901234'

# Define a function to encrypt data using AES
def encrypt(data):
    # Create a new AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Pad the data to a multiple of 16 bytes
    data = data + b"\0" * (AES.block_size - len(data) % AES.block_size)
    
    # Encrypt the data using AES CBC mode
    ciphertext = cipher.encrypt(data)
    
    # Encode the ciphertext using base64 for transport
    return base64.b64encode(ciphertext)

# Define a function to decrypt data using AES
def decrypt(ciphertext):
    # Create a new AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Decode the ciphertext from base64
    ciphertext = base64.b64decode(ciphertext)
    
    # Decrypt the ciphertext using AES CBC mode
    data = cipher.decrypt(ciphertext)
    
    # Remove the padding from the data
    return data.rstrip(b"\0")
