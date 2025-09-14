#!/usr/bin/env python3
"""
Test script to demonstrate real-time ticket creation.
Run this while the dashboard is open to see tickets appear instantly.
"""

import requests
import json
import time
import random

# Configuration
API_URL = "http://localhost:5000/create_ticket"
SAMPLE_USERS = ["john_doe", "jane_smith", "bob_wilson", "alice_brown", "charlie_davis"]
SAMPLE_PDFS = [
    "https://example.com/product-guide-1.pdf",
    "https://example.com/installation-manual.pdf",
    "https://example.com/troubleshooting-guide.pdf",
    "https://example.com/user-manual.pdf",
    "https://example.com/quick-start-guide.pdf"
]
SAMPLE_PRODUCTS = ["PROD-001", "PROD-002", "PROD-003", "WIDGET-A", "WIDGET-B"]

def create_sample_ticket():
    """Create a sample ticket with random data."""
    data = {
        "user_id": random.choice(SAMPLE_USERS),
        "pdf_link": random.choice(SAMPLE_PDFS),
        "product_id": random.choice(SAMPLE_PRODUCTS),
        "other_ids": f"REF-{random.randint(1000, 9999)}"
    }
    
    try:
        response = requests.post(API_URL, json=data, headers={'Content-Type': 'application/json'})
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Created ticket #{result['ticket_id']} for user {data['user_id']}")
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure the Flask app is running on localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🎫 Ticketing System API Test")
    print("=" * 40)
    print("This script will create sample tickets to demonstrate real-time updates.")
    print("Make sure your Flask app is running and dashboard is open in browser.")
    print()
    
    while True:
        print("\nOptions:")
        print("1. Create single ticket")
        print("2. Create 3 tickets with delay")
        print("3. Create 5 tickets rapidly")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            create_sample_ticket()
            
        elif choice == "2":
            print("Creating 3 tickets with 2-second delays...")
            for i in range(3):
                if create_sample_ticket():
                    if i < 2:  # Don't wait after the last ticket
                        print("Waiting 2 seconds...")
                        time.sleep(2)
                        
        elif choice == "3":
            print("Creating 5 tickets rapidly...")
            for i in range(5):
                create_sample_ticket()
                time.sleep(0.5)  # Small delay to see the effect
                
        elif choice == "4":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()
