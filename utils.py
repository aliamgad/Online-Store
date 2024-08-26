import re
import hashlib
import hmac
import bcrypt


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password.decode()


def is_password_match(entered_password, stored_hash):
    stored_hash_bytes = stored_hash.encode()

    return bcrypt.checkpw(entered_password.encode(), stored_hash_bytes)

def create_mac(price):
    secret_password = b"v9bX@34l!zM5Pq8tqwokdop1ie9021212"
    # Ensure the price is in string format and then encode it to bytes
    price = str(price).encode('utf-8')
    
    # Create an HMAC object using SHA-256
    mac = hmac.new(secret_password, price, hashlib.sha256).hexdigest()

    return mac


def is_strong_password(password):
    min_length = 8
    require_uppercase = True
    require_lowercase = True
    require_digit = True
    require_special_char = True

    if len(password) < min_length:
        return False

    if require_uppercase and not any(char.isupper() for char in password):
        return False

    if require_lowercase and not any(char.islower() for char in password):
        return False

    if require_digit and not any(char.isdigit() for char in password):
        return False

    if require_special_char and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False

    return True
