#!/usr/bin/python3

import csv
import json
import os
import requests
import sys
import time
import utils

__dir__ = os.path.abspath(os.path.dirname(__file__))
MEDIA_DIR = os.path.join(__dir__, "media")
INPUT_FILE = os.path.join(__dir__, "input.csv")
OUTPUT_FILE = os.path.join(__dir__, "output.csv")

def main():
    driver = utils.get_driver()
    os.makedirs(MEDIA_DIR, exists_ok=True)
    config_sv = {
                "lang": "sv-SE",
                "voice": "Astrid"
            }
    try:
        export_words = []
        cookies = utils.generate_cookie(driver, "https://www.gosubtitle.com/tts")
        with open(INPUT_FILE) as csvfile:
            content = csv.reader(csvfile)
            for line in content:
                svenska = line[0]
                name = svenska.replace(' ', '-').replace('/', '-').lower()
                mp3_file = os.path.join(MEDIA_DIR, "{}.mp3".format(name))
                if not os.path.exists(mp3_file):
                    request_sentence(svenska, mp3_file, cookies, config_sv)
                export_words.append(line + ["[sound:{}.mp3]".format(name)])
        with open(OUTPUT_FILE, "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            for line in export_words:
                writer.writerow(line)
    finally:
        driver.close()

def request_sentence(sentence, output_file, cookies, config):
    url = "https://www.gosubtitle.com/generate-tts-voice"
    cookie = "_ga={}; laravel_session={}".format(cookies["_ga"], cookies["laravel_session"])
    headers = {
            "authority": "www.gosubtitle.com",
            "path": "/generate-tts-voice",
            "cookie": cookie,
            "origin": "https://www.gosubtitle.com",
            "referer": "https://www.gosubtitle.com/tts"
            }
    body = {
            "token_validation": "86bd7e39f0192d03792036389e30af51",
            "tts_text": sentence,
            "tts_lang": config["lang"],
            "tts_voice": config["voice"],
            "agreement": "1",
            }
    r = requests.post(url, headers = headers, data=body)
    if r.ok:
        r_content = json.loads(r.content.decode('utf-8', 'ignore'))
        slug = r_content['slug']
        media = requests.get("https://www.gosubtitle.com/temp-download-media/" + slug)
        with open(output_file, 'wb') as f:
            f.write(media.content)
    else:
        print(r.content)
        raise Exception("Requests fails with status code {}".format(r.status_code))

if __name__ == '__main__':
    main()
