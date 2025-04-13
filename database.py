import sqlite3

DB_FILE = "app_data.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_key TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS videos (aweme_id text primary key, video_id text unique not null, video_url text, tittle text, user_id text not null, foreign key (user_id) references users(user_id));
    CREATE TABLE users (user_id text primary key, username text unique not null, created timestamp default current_timestamp, updated timestamp default current_timestamp);
    """)
    conn.commit()
    conn.close()

def add_key_to_db(api_key, email):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO api_keys (api_key, email) VALUES (?, ?)", (api_key, email))
    conn.commit()
    conn.close()

def fetch_keys():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT api_key, email FROM api_keys")
    keys = cursor.fetchall()
    conn.close()
    return keys

def add_user(user_id, user_name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, user_name))
    conn.commit()
    conn.close()

def add_video(aweme_id, video_id, video_url, tittle, user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO videos (aweme_id, video_id, video_url, tittle, user_id) VALUES(?, ?, ?, ?, ?)", (aweme_id, video_id, video_url, tittle, user_id))
    conn.commit()
    conn.close()