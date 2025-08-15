#!/usr/bin/env python3
"""
Password Encoder for Email Server
This script helps encode your Gmail App Password to base64 for secure configuration.
"""

import base64
import getpass

def encode_password():
    """Encode password to base64"""
    print("🔐 Password Encoder for Email Server")
    print("=" * 40)
    print()
    print("This script will encode your Gmail App Password to base64.")
    print("The encoded password will be safe to use in your .env file.")
    print()
    
    # Get password securely (hidden input)
    password = getpass.getpass("Enter your Gmail App Password: ")
    
    if not password:
        print("❌ No password entered. Exiting.")
        return
    
    try:
        # Encode to base64
        encoded = base64.b64encode(password.encode('utf-8')).decode('utf-8')
        
        print()
        print("✅ Password encoded successfully!")
        print("=" * 40)
        print()
        print("📝 Add this to your .env file:")
        print(f"MAIL_PASSWORD={encoded}")
        print()
        print("🔒 Your original password is NOT stored anywhere.")
        print("💡 You can now safely use this encoded value in your configuration.")
        
    except Exception as e:
        print(f"❌ Error encoding password: {e}")

def decode_password():
    """Decode base64 password (for testing)"""
    print("🔓 Password Decoder (for testing)")
    print("=" * 40)
    print()
    
    encoded = input("Enter your base64 encoded password: ")
    
    if not encoded:
        print("❌ No encoded password entered. Exiting.")
        return
    
    try:
        # Decode from base64
        decoded = base64.b64decode(encoded).decode('utf-8')
        
        print()
        print("✅ Password decoded successfully!")
        print("=" * 40)
        print()
        print("🔓 Decoded password (first 4 chars):", decoded[:4] + "*" * (len(decoded) - 4))
        print("📏 Password length:", len(decoded))
        
    except Exception as e:
        print(f"❌ Error decoding password: {e}")

def main():
    """Main function"""
    print("🚀 Email Server Password Encoder")
    print("=" * 40)
    print()
    print("Choose an option:")
    print("1. Encode password (recommended)")
    print("2. Decode password (for testing)")
    print("3. Exit")
    print()
    
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            encode_password()
            break
        elif choice == "2":
            decode_password()
            break
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
