import os

def find_all_matches(text, match):
    hasMore = text.find(match)
    indexes = []
    while hasMore != -1:
        indexes.append(hasMore)
        slice_start = indexes[-1] + len(match)
        hasMore = text[slice_start:].find(match)
        if hasMore != -1:
            hasMore += slice_start
    return indexes



def safe_mkdir(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)