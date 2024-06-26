import sys

def main():
    # Check if a text argument is provided
    if len(sys.argv) != 2:
        print("Usage: python cats.py <your_text>")
        sys.exit(1)
    
    # Get the input text from the command line argument
    user_input = sys.argv[1]

    # Print the input text
    print(f"Contexts: {user_input}")




if __name__ == "__main__":
    main()