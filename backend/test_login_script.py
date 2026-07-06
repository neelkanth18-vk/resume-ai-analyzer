import sys
import os
sys.path.insert(0, r"C:\Users\Neel\.gemini\antigravity\scratch\resume-ai-app\backend")

from core.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta

print("Hashing password...")
h = get_password_hash("password123")
print("Hash:", h)
print("Verifying password...")
print("Valid:", verify_password("password123", h))
print("Creating token...")
try:
    token = create_access_token({"sub": "1"}, timedelta(minutes=60))
    print("Token:", token)
except Exception as e:
    print(f"Error: {e}")
