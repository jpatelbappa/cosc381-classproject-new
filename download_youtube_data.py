import json
import sys
import os
import shutil
from googleapiclient.discovery import build
import config
from tqdm import tqdm

data_dir = 'youtube_data'

def youtube_data(api_key, video_id):
    service = build("youtube", "v3", developerKey=api_key)
    result = service.videos().list(part='snippet', id=video_id).execute()
    return result

if __name__ == '__main__':
    video_ids_file = sys.argv[1]
    my_api_key = config.api_key

    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)

    os.makedirs(data_dir)

    with open(video_ids_file) as f:
        video_ids = f.readlines()
        for video_id in tqdm(video_ids):
            video_id = video_id.strip()
            result = youtube_data(my_api_key, video_id)
            with open(data_dir+ '/' + video_id + '.json', 'w') as f:
                json.dump(result, f)
        