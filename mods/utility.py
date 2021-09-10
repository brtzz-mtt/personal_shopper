import hashlib
import time

def generate_md5_hash():
    return hashlib.md5(str(time.time()).encode()).hexdigest()
