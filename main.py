# The purpose of this code is to automate the use of an API
# which downloads all video posts from a given user, so
# the main achievement is to reduce API calls.

# This code uses MySQL to preserve logs about downloaded
# data, so when called over a previously downloaded user
# it avoids using all calls again, based on the first call
# which match any aweme_id primary key from a user's video.

# IMPORTING DEPENDENCIES

import http.client
import json
import os
import sys
import sqlite3

# DECLARING CONSTANTS

UNIQUE_ID = "aweme_id"
API_KEYS = [
    "3c2fc2209dmshc3bce8ff31f324dp198189jsnce2b27876d7c",
    "a0fb98bf70msh43f594ae0b631f7p1b1362jsnfd0f6b5f5946",
    "832a4ba4e8msha46c32bfcd098c8p175dfdjsnd639890d4569",
    "3518e3c984msheac5f647506d910p13f8dcjsnb58faa53c8ff",
    "fdce325e93msha59ea42f8f99503p172ff1jsn02fdf56fe0fe",  # ABARROTESDONRAFA@GMAIL.COM
    ]

HEADERS = {
    'X-RapidAPI-Key': API_KEYS[4],
    'X-RapidAPI-Host': "tiktok-video-no-watermark2.p.rapidapi.com"
}


# DECLARING GLOBAL VARIABLES

user = sys.argv[1]
cursor = "0"
hasMore = True
videos = {}
flag = True

# DATABASE PARAMS
#---------------------------------------------------

# $video VARIABLE STRUCTURE IS GIVEN AS FOLLOWS:
#videos = {
#  user_id: { 
#    username: [(aweme_id_1, conut_name_1),
#               (aweme_id_2, count_name_2),
#               .
#               .
#               . 
#               (aweme_id_n, conut_name_n)]
#  }
# }

# CREATING HTTP CLIENT OBJECT: 

conn = http.client.HTTPSConnection(HEADERS["X-RapidAPI-Host"])

# CREAING USER FOLDER CONTAINER

os.system('mkdir ' + user)

# Defining the variable allocator function to design variable structure:

def variable_alocator(user, HEADERS):
    global videos
    conn.request("GET", "/user/info?unique_id=%40" + user, headers=HEADERS)
    res = conn.getresponse()
    data = res.read()
    jsonized_data = json.loads(data)
    # CREATING DATA SCTRUCTURE
    videos[jsonized_data["data"]["user"]["uniqueId"]] = {
        jsonized_data["data"]["user"]["id"]: []
    }
    return jsonized_data["data"]["user"]["id"]

user_id = variable_alocator(user, HEADERS)

# video_fetcher takes username, cursor and HEADERS as params
# in order to fetch data from API, so we can actively use it
# in a loop so we return cursor, hasMore and video_buffer da-
# ta in order to refactor all in another function.

def video_fetcher(user, cursor, HEADERS):
    global videos
    conn.request("GET", "/user/posts?unique_id=%40" + user + "&count=35&cursor=" + cursor , headers=HEADERS)
    res = conn.getresponse()
    data = res.read()
    jsonized_data = json.loads(data)
    video_buffer = [(video["aweme_id"], video["play"]) for video in jsonized_data["data"]["videos"]]
    return (jsonized_data["data"]["cursor"], jsonized_data["data"]["hasMore"], video_buffer)

# download_videos fnc worksaround the process of taking the
# complete video list, so it can use wget from system to do-
# load videos to disk.

def download_videos(video_list):
    count = 0
    for item in video_list:
        video_url = item[1]
        cmd = "wget -O " + "./" + user + "/" + user + str(count) + ".mp4 " + "'" + video_url + "'"
        os.system(cmd)
        count += 1

# Here we use a While loop in order to iterate over our data.

while hasMore:
    cursor, hasMore, video_buffer = video_fetcher(user, cursor, HEADERS)
    videos[user][user_id].extend(video_buffer)
    print("Videos found: " + str(len(videos[user][user_id])))
    if not hasMore:
        print("Downloading a Video! You got Lucky!")
        download_videos(videos[user][user_id])

# further objective is to save all data in MySQL so we can
# download only newer videos, reducing the API calls so we
# avoid reaching montly quota limit that quickly.


# Function to save later users, storing in database to start
# downloaded when needed.