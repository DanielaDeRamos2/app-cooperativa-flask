#!/usr/bin/env python
"""Comprehensive import verification"""
import sys
import traceback

print("=" * 60)
print("IMPORT VERIFICATION SCRIPT")
print("=" * 60)

errors = []

# Test 1: Flask imports
try:
    print("\n[1/6] Importing Flask dependencies...")
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import LoginManager
    from flask_mail import Mail
    print("✓ Flask dependencies OK")
except Exception as e:
    errors.append(f"Flask imports failed: {e}")
    print(f"✗ Flask imports failed: {e}")

# Test 2: Config
try:
    print("[2/6] Importing Config...")
    from config import Config
    print("✓ Config OK")
except Exception as e:
    errors.append(f"Config import failed: {e}")
    print(f"✗ Config import failed: {e}")

# Test 3: App factory
try:
    print("[3/6] Importing app factory...")
    from app import create_app, db
    print("✓ App factory OK")
except Exception as e:
    errors.append(f"App factory import failed: {e}")
    traceback.print_exc()
    print(f"✗ App factory import failed: {e}")

# Test 4: Create app
try:
    print("[4/6] Creating app instance...")
    app = create_app()
    print("✓ App instance created OK")
except Exception as e:
    errors.append(f"App creation failed: {e}")
    traceback.print_exc()
    print(f"✗ App creation failed: {e}")
    sys.exit(1)

# Test 5: App context
try:
    print("[5/6] Creating app context...")
    with app.app_context():
        print("✓ App context OK")
except Exception as e:
    errors.append(f"App context failed: {e}")
    traceback.print_exc()
    print(f"✗ App context failed: {e}")
    sys.exit(1)

# Test 6: Database tables
try:
    print("[6/6] Creating database tables...")
    with app.app_context():
        db.create_all()
    print("✓ Database tables created OK")
except Exception as e:
    errors.append(f"Database creation failed: {e}")
    traceback.print_exc()
    print(f"✗ Database creation failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
if errors:
    print(f"❌ {len(errors)} ERROR(S) FOUND:")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)
else:
    print("✅ ALL IMPORTS AND INITIALIZATION SUCCESSFUL!")
    print("=" * 60)
    sys.exit(0)
