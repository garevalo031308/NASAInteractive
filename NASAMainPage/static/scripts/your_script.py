# NASAMainPage/your_script.py
import sys

def main(user_input):
    print(f"Received input: {user_input}")

if __name__ == "__main__":
    user_input = sys.argv[1] if len(sys.argv) > 1 else "No input provided"
    main(user_input)