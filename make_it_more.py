from openai import OpenAI
import re
import json

import requests
from datetime import datetime
from dotenv import load_dotenv
import os 

from tweet_it import tweet_it
from text_img_auto_gen import save_messages, load_messages, download_image, generate_image 

load_dotenv()
OAI_api_key = os.getenv('OAI_api_key')
base_path = './imgs/make_it_more'
extension = 'jpeg'

def save_messages(messages, file_path):
    """Save messages to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(messages, file)

def load_messages(file_path):
    """Load messages from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist

def download_image(image_url):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    response = requests.get(image_url)
    
    if response.status_code == 200:
        local_img_path = f"{base_path}_{timestamp}.{extension}"
        with open(local_img_path, 'wb') as file:
            file.write(response.content)
        return local_img_path
    else:
        print(f"Failed to download the image. Status code: {response.status_code}")

def generate_image(prompt):
    try:
        print(f"Generating an image for: {prompt}")
        response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
        )
        return response.data[0].url
    except Exception as e:
        print(f"An error occurred while generating the image: {e}")


def make_it_more(orig_prompt, make_more, max_iter=5):
        # reply_id = None
        reply_to_id = None
        iter = 1
        prompt = orig_prompt
        # while within iterations
        while iter <= max_iter:
            prompt = f"{orig_prompt} {iter}"
            img_url = generate_image(prompt)
            local_img_path = download_image(img_url)

            # tweet it
            text = f"{orig_prompt} {iter}" if iter == 1 else f"{make_more} {iter}" 
            response = tweet_it(prompt, local_img_path, reply_to_id)
            reply_to_id = response["data"]["id"]  

            iter += 1

if __name__ == "__main__":
#   history_file = './files/make_it_more.json'
#   output_file = './files/make_it_more_output.txt'
    client = OpenAI(api_key=OAI_api_key)
    orig_prompt = "No text anywhere. Generate a photo-realistic portrait of a human from a society. If being in stone age is 1 and being the most advanced and futuristic society is 5. This society is the at "
    make_more = "make it more advanced"
    make_it_more(orig_prompt, make_more, 5)
