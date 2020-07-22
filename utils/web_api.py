import os
import sys
import json

import urllib3
import requests

class ImageAPI:
    def __init__(self):
        pass

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
    
    def getPrequelMeme(self):
        params={
            "sort":"top",
            "t":"week"
        }

        resp = requests.get(url="https://www.reddit.com/r/PrequelMemes.json", params=params)
        dictResp = resp.json()
        return dictResp["data"]["children"][random.randint(1, 100)]["data"]["preview"]["images"][0]["source"]["url"]