"""Test basic MongoDB connection."""
from mongodb_controller.mongodb_connector import test_connection

def main():
    try:
        client = test_connection()
        client.close()
        print("Connection closed")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
