import re
import random

def validate_username(username):
    if not re.match(r'^[A-Za-z0-9]+$', username):
        return "Username must contain only letters and numbers"
    return None

def validate_password(password, username):
    if len(password) < 8 or len(password) > 20:
        return "Password must be 8 to 20 characters long"

    if password.lower() == username.lower():
        return "Password cannot be same as username"

    if not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter"

    if not re.search(r'[a-z]', password):
        return "Password must contain at least one lowercase letter"

    if not re.search(r'[0-9]', password):
        return "Password must contain at least one number"

    if not re.search(r'[!@#$%^&*()]', password):
        return "Password must contain at least one special character"

    return None

def generate_otp():
    return f"{random.randint(0, 999999):06d}"