import argparse
from api_key import add_api_key, get_api_keys
from download_logic import execute_logic

def main():
    parser = argparse.ArgumentParser(description="Data scraping tool with API key management (RapidApi).")
    parser.add_argument("-a", "--add", nargs=2, metavar=("API_KEY", "EMAIL"), help="Add a new Api Key to the database.")
    parser.add_argument("user", nargs="?", help="Scrap and download user data into disk.")

    args = parser.parse_args()

    if args.add:
        print(f"Received arguments for add: {args.add}")
        api_key, email = args.add
        add_api_key(api_key, email)
        print(f"API key related with email < {email} > added successfully!")
    elif args.user:
        api_keys = get_api_keys()
        if not api_keys:
            print("No API keys available. Please add one first.")
            return
        print("Available API keys: ")
        for idx, (key, email) in enumerate(api_keys):
            print(f"{idx+1}. {key} (Email: {email})")
        selected = int(input("Select an API key by number: "))-1

        if len(api_keys) > selected >= 0:
            selected_key, selected_email = api_keys[selected]
            print(f"Using API key for email: {selected_email}")
            execute_logic(args.user, selected_key)
        else:
            print("Invalid selection.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()