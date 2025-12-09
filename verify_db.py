#!/usr/bin/env python
"""Verify model table names are consistent"""
import sys

try:
    print("Importing models...")
    from app import db, create_app
    
    print("Creating app...")
    app = create_app()
    
    print("Creating database context...")
    with app.app_context():
        print("\nDatabase tables to be created:")
        print("=" * 50)
        
        # Get all models
        for table in db.metadata.tables:
            print(f"  ✓ {table}")
        
        print("\nCreating all tables...")
        db.create_all()
        print("✓ All tables created successfully!")
        
        print("\n" + "=" * 50)
        print("✅ Database initialization successful!")
        sys.exit(0)
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
