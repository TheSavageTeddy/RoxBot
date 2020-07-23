import os
import sys
import json

import urllib3
import requests
import praw
import random

from dotenv import load_dotenv
from utils.cli_logging import *

class ImageAPI:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("client_id")
        self.client_secret = os.getenv("client_secret")
        self.user_agent = "RoxBot PRAW API"

    def getImgflip(self, memeCode, textInput):
        params={
            "username":"roxiun",
            "password":"supergoodpassword",
            "template_id":memeCode
        }
        for i in range(len(textInput)):
            params[f'boxes[{i}][text]'] = textInput[i]
        resp = requests.get(url="https://api.imgflip.com/caption_image", params=params)
        dictResp = resp.json()
        return dictResp["data"]["url"]
    
    def getMeme(self, subreddit, amount: int = None, time: str = None):
        r = praw.Reddit(client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent)

        subreddit = subreddit.replace("r/", "")

        all_submissions = r.subreddit(subreddit)
        posts = []
 

        if not amount:
            amount=50
        if not time:
            time = 'month'
        
        info(f"Searching {subreddit} (Amount:{str(amount)})")
        
        for submission in r.subreddit(subreddit).top(time, limit=amount):
            if submission and not submission.stickied:
                posts.append(submission)

        
        post = posts[random.randint(1, amount)-1]
        while post.over_18:
            warning("Post rated nsfw")
            post = posts[random.randint(1, amount)-1]
        return {"title":post.title, "url":post.url, "upvotes":post.score}
        

if __name__ == "__main__":
    a=ImageAPI()
    print(a.getPrequelMeme())