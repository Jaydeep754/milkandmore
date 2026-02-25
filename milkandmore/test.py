# test_paths.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

print(f"BASE_DIR: {BASE_DIR}")
print(f"MEDIA_ROOT: {MEDIA_ROOT}")
print(f"MEDIA_ROOT exists: {os.path.exists(MEDIA_ROOT)}")
print(f"media/products exists: {os.path.exists(os.path.join(MEDIA_ROOT, 'products'))}")

if not os.path.exists(MEDIA_ROOT):
    print("❌ Media folder doesn't exist!")
else:
    print("✅ Media folder exists!")