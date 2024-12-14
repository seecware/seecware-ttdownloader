from database import add_user, add_video

def create_new_user(user_id, username):
    print(f"Creating new user into database registers. {username} added.")
    add_user(user_id, username)


def insert_video(aweme_id, video_id, video_url, tittle, user_id):
    add_video(aweme_id, video_id, video_url, tittle, user_id)
    print(f"Inserting video data into database: {video_id} added correctly to db.")

