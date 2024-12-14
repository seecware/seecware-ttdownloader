# # The purpose of this code is to automate the use of an API
# # which downloads all video posts from a given user, so
# # the main achievement is to reduce API calls.

# # This code uses MySQL to preserve logs about downloaded
# # data, so when called over a previously downloaded user
# # it avoids using all calls again, based on the first call
# # which match any aweme_id primary key from a user's video.

# # IMPORTING DEPENDENCIES

from db_downloader_middleware import create_new_user, insert_video

import http.client
import json
import os

UNIQUE_ID = "aweme_id"
videos = []
images = []

def execute_logic(user, selected_key):
    HEADERS = {
        'X-RapidAPI-Key': selected_key,
        'X-RapidAPI-Host': "tiktok-video-no-watermark2.p.rapidapi.com"
    }

    cursor = "0"
    hasMore = True
    videos_acc = []
    images_acc = []

    conn = http.client.HTTPSConnection(HEADERS["X-RapidAPI-Host"])

    # Getting user_id from given user string.
    conn.request("GET", "/user/info?unique_id=" + user, headers=HEADERS)
    res = conn.getresponse()
    data = res.read()
    jsonized_data = json.loads(data)
    user_id = jsonized_data['data']['user']['id']
    create_new_user(user_id, user)
    os.mkdir(user)
    
    # Getting video data.
    while hasMore:
        hasMore, cursor, video_fragment, image_fragment = video_fetcher(user_id, cursor, HEADERS, conn)
        videos_acc.extend(video_fragment)
        print(f"Found videos: {len(videos_acc)}")
        images_acc.extend(image_fragment)
        print(f"Found images: {len(images_acc)}")
    
    download_videos(videos_acc, user)
    download_images(images_acc, user)
    


# # video_fetcher takes username, cursor and HEADERS as params
# # in order to fetch data from API, so we can actively use it
# # in a loop so we return cursor, hasMore and video_buffer da-
# # ta in order to refactor all in another function.

def video_fetcher(user_id, cursor, headers, conn):
    conn.request("GET", "/user/posts?user_id=" + user_id +"&count=35&cursor=" + str(cursor), headers=headers)
    res = conn.getresponse()
    data = res.read()
    jsonized_data = json.loads(data)
    video_fragment = [(video['aweme_id'], video['play'], video['video_id'], video['title']) for video in jsonized_data['data']['videos'] if video['aweme_id'] != ""]
    image_fragment = []
    for item in jsonized_data['data']['videos']:
        if (item['aweme_id'] == ""):
            print("aux")
            image_fragment.extend([image for image in item['images']])

    new_cursor = jsonized_data['data']['cursor']
    hasMore = jsonized_data['data']['hasMore']
    return (hasMore, new_cursor, video_fragment, image_fragment)


# # download_videos fnc workaround the process of taking the
# # complete video list, so it can use wget from system to do-
# # load videos to disk.

def download_videos(video_list, user):
    count = 0
    for item in video_list:
        video_url = item[1]
        insert_video(item[0], item[2], item[1], item[3], user)
        cmd = "wget -O " + "./" + user + "/" + user + str(count) + ".mp4 " + "'" + video_url + "'"
        os.system(cmd)
        count += 1


def download_images(image_list, user):
    count = 0
    os.mkdir("./" + user + "/img")
    for item in image_list:
        image_url = item
        cmd = "wget -O " + "./" + user + "/img/" + user + str(count) + ".jpeg " + "'" + image_url + "'"
        os.system(cmd)
        count += 1

# # further objective is to save all data in MySQL so we can
# # download only newer videos, reducing the API calls so we
# # avoid reaching montly quota limit that quickly.


# # Function to save later users, storing in database to start
# # downloaded when needed.
