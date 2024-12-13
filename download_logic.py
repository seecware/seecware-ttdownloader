# # The purpose of this code is to automate the use of an API
# # which downloads all video posts from a given user, so
# # the main achievement is to reduce API calls.

# # This code uses MySQL to preserve logs about downloaded
# # data, so when called over a previously downloaded user
# # it avoids using all calls again, based on the first call
# # which match any aweme_id primary key from a user's video.

# # IMPORTING DEPENDENCIES

import http.client
import json
import os
import sys
import database

# DECLARING CONSTANTS

# DATABASE PARAMS
#---------------------------------------------------
UNIQUE_ID = "aweme_id"
HEADERS = {
    'X-RapidAPI-Key': NULL,
    'X-RapidAPI-Host': "tiktok-video-no-watermark2.p.rapidapi.com"
}

cursor = "0"
hasMore = True
videos = {}
flag = True
    
conn = http.client.HTTPSConnection(HEADERS["X-RapidAPI-Host"])

# # $video VARIABLE STRUCTURE IS GIVEN AS FOLLOWS:
# #videos = {
# #  user_id: { 
# #    username: [(aweme_id_1, conut_name_1),
# #               (aweme_id_2, count_name_2),
# #               .
# #               .
# #               . 
# #               (aweme_id_n, conut_name_n)]
# #  }
# # }

# CREAING USER FOLDER CONTAINER

# Defining the variable allocator function to design variable structure:

def variable_alocator(user, HEADERS):
    global videos
    conn.request("GET", "/user/info?unique_id=%40" + user, headers=HEADERS)
    res = conn.getresponse()
    data = res.read()
    jsonized_data = json.loads(data)
    add_user(jsonized_data["data"]["user"]["uniqueId"], jsonized_data["data"]["user"]["id"])        # Lacks of cheking if user_id already exists! Add later.
    # CREATING DATA SCTRUCTURE
    videos[jsonized_data["data"]["user"]["uniqueId"]] = {
        jsonized_data["data"]["user"]["id"]: []
    }
    return (jsonized_data["data"]["user"]["id"], jsonized_data["data"]["user"]["uniqueId"])

# # video_fetcher takes username, cursor and HEADERS as params
# # in order to fetch data from API, so we can actively use it
# # in a loop so we return cursor, hasMore and video_buffer da-
# # ta in order to refactor all in another function.

def video_fetcher(user, cursor, HEADERS):
    global videos
    conn.request("GET", "/user/posts?unique_id=%40" + user + "&count=35&cursor=" + cursor , headers=HEADERS)
    res = conn.getresponse()
    data = res.read()
    jsonized_data = json.loads(data)
    video_buffer = [(video["aweme_id"], video["play"]) for video in jsonized_data["data"]["videos"]]
    return (jsonized_data["data"]["cursor"], jsonized_data["data"]["hasMore"], video_buffer)

# # download_videos fnc worksaround the process of taking the
# # complete video list, so it can use wget from system to do-
# # load videos to disk.

def download_videos(video_list):
    count = 0
    for item in video_list:
        add_video(aweme_id, video_id, video_url, tittle, user_id)
        video_url = item[1]
        cmd = "wget -O " + "./" + user + "/" + user + str(count) + ".mp4 " + "'" + video_url + "'"
        os.system(cmd)
        count += 1


# # further objective is to save all data in MySQL so we can
# # download only newer videos, reducing the API calls so we
# # avoid reaching montly quota limit that quickly.


# # Function to save later users, storing in database to start
# # downloaded when needed.

def execute_logic(user, selected_key):
    os.system('mkdir ' + user)
    [user_id, user_id_unique] = variable_alocator(user, HEADERS)

    while hasMore:
        cursor, hasMore, video_buffer = video_fetcher(user, cursor, HEADERS)
        videos[user][user_id].extend(video_buffer)
        print(videos)
        print("Videos found: " + str(len(videos[user][user_id])))
        if not hasMore:
            print("Downloading a Video! You got Lucky!")
            download_videos(videos[user][user_id])