#!/usr/bin/env python
"""Simple test to verify app imports correctly"""
import sys

try:
    print("Importing Flask...")
    from flask import Flask
    print("✓ Flask imported")
    
    print("Importing app factory...")
    from app import create_app, db
    print("✓ App factory imported")
    
    print("Creating app...")
    app = create_app()
    print("✓ App created successfully")
    
    print("Creating app context...")
    with app.app_context():
        print("✓ App context created")
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created")
    
    print("\n✅ All imports successful! App is ready to run.")
    sys.exit(0)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
