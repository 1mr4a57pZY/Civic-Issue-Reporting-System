#!/usr/bin/env python3
"""
Test script to verify the problematic query works correctly.
This tests: User.query.filter((User.mobile == mobile) | (User.email == email)).first()
"""

import os
import sys
from datetime import datetime
import pytz

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User

def test_problematic_query():
    """Test the specific query that was failing"""

    print("🧪 Testing the problematic query...")
    print("Query: User.query.filter((User.mobile == mobile) | (User.email == email)).first()")

    with app.app_context():
        try:
            # Test Case 1: Search by mobile only
            print("\n📱 Test Case 1: Search by mobile only")
            mobile = "9876543210"
            result = User.query.filter((User.mobile == mobile) | (User.email == "nonexistent@example.com")).first()
            print(f"   Mobile: {mobile}")
            print(f"   Result: {result}")
            print("   ✅ Mobile search works!")

            # Test Case 2: Search by email only
            print("\n📧 Test Case 2: Search by email only")
            email = "test@example.com"
            result = User.query.filter((User.mobile == "9999999999") | (User.email == email)).first()
            print(f"   Email: {email}")
            print(f"   Result: {result}")
            print("   ✅ Email search works!")

            # Test Case 3: Search with both (OR condition)
            print("\n🔍 Test Case 3: Search with both mobile and email (OR condition)")
            result = User.query.filter((User.mobile == mobile) | (User.email == email)).first()
            print(f"   Mobile: {mobile}, Email: {email}")
            print(f"   Result: {result}")
            print("   ✅ Combined OR query works!")

            # Test Case 4: No matches found
            print("\n❓ Test Case 4: No matches found")
            result = User.query.filter((User.mobile == "0000000000") | (User.email == "nonexistent@example.com")).first()
            print(f"   Mobile: 0000000000, Email: nonexistent@example.com")
            print(f"   Result: {result}")
            print("   ✅ No matches query works!")

            # Test Case 5: Create a test user and search for it
            print("\n👤 Test Case 5: Create test user and search")
            test_user = User(
                name="Test User",
                email="testuser@example.com",
                mobile="1234567890",
                is_verified=True
            )
            db.session.add(test_user)
            db.session.commit()

            # Now search for this user
            result = User.query.filter((User.mobile == "1234567890") | (User.email == "testuser@example.com")).first()
            print(f"   Created user: {test_user.name}")
            print(f"   Search result: {result}")
            if result and result.id == test_user.id:
                print("   ✅ User creation and search works!")
            else:
                print("   ❌ User search failed!")
                return False

            # Clean up test user
            db.session.delete(test_user)
            db.session.commit()

            print("\n🎉 All query tests passed successfully!")
            print("✅ The problematic query should now work in your application!")
            return True

        except Exception as e:
            print(f"❌ Query test failed: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    test_problematic_query()
