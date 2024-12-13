from database import add_key_to_db, fetch_keys

def add_api_key(api_key, email):
    print(f"Adding API key: {api_key} with email: {email}")
    add_key_to_db(api_key, email)

def get_api_keys():
    return fetch_keys()