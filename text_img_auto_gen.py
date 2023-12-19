from openai import OpenAI
import re
import json
from tweet_it import tweet_it
import requests
from datetime import datetime
from dotenv import load_dotenv
import os 
load_dotenv()

OAI_api_key = os.getenv('OAI_api_key')

base_path = './imgs/dalle_generation'
extension = 'jpeg'
# start client
client = OpenAI(api_key=OAI_api_key)


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

def chat_with_openai(messages, output_file, history_file, option=None):

    with open(output_file, "a", encoding='utf-8') as file:

        # get one generation and jolt down the outputs
        response = client.chat.completions.create(model="gpt-3.5-turbo", 
                                                  messages=messages)
        model_response = response.choices[0].message.content
        messages.append({"role": "system", "content": model_response})
        file.write("AI: " + model_response + "\n")
        print("AI:", model_response)

        # either tweet text only or with img
        if option == "tweet_w_img":
            # Image generation trigger
            if messages and messages[-1]["role"] == "system":
                text = messages[-1]["content"]
                img_url = generate_image(text)
                local_img_path = download_image(img_url)
                tweet_it(text, local_img_path)
            else:
                print("No recent AI message to use for image generation.")
        
        elif option == "tweet":
            # If the last message was from the AI, tweet it
            if messages and messages[-1]["role"] == "system":
                tweet_it(messages[-1]["content"])
            else:
                print("No recent AI message to tweet.")
        
        # save the chat history
        save_messages(messages, history_file)

if __name__ == "__main__":
  history_file = './files/art.json'
  output_file = './files/output.txt'

  messages = load_messages(history_file)
  messages.append({"role": "user", "content": "Write a different painting that  in different reimagined style. "})
  
  chat_with_openai(messages, output_file, history_file, "tweet_w_img")
