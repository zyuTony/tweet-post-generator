from openai import OpenAI
import re
import json
from tweet_it import tweet_it
import requests
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

def download_image(image_url, local_img_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(local_img_path, 'wb') as file:
            file.write(response.content)
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

def chat_with_openai(messages, output_file, history_file):
    """
    Function to interact with OpenAI's chat model, save outputs, and identify links.
    
    :param messages: A list of messages in the conversation history.
    :param output_file: File path to save the conversation.
    """
    with open(output_file, "a", encoding='utf-8') as file:
        while True:
            new_user_message = input("You: ")

            if new_user_message.lower() in ["exit", "quit", "stop"]:
                print("Exiting the conversation.")
                save_messages(messages, history_file)
                break
            
            if new_user_message.lower() == "tweet with img":
                # Image generation trigger
                if messages and messages[-1]["role"] == "system":
                    text = messages[-1]["content"]
                    img_url = generate_image(text)
                    download_image(img_url, local_img_path)
                    tweet_it(text, local_img_path)
                else:
                    print("No recent AI message to use for image generation.")
                continue
            
            if new_user_message.lower() == "tweet":
                # If the last message was from the AI, tweet it
                if messages and messages[-1]["role"] == "system":
                    tweet_it(messages[-1]["content"])
                else:
                    print("No recent AI message to tweet.")
                continue
            
            messages.append({"role": "user", "content": new_user_message})
            file.write("You: " + new_user_message + "\n")

            response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)

            # Extracting the model's response
            model_response = response.choices[0].message.content
            messages.append({"role": "system", "content": model_response})

            file.write("AI: " + model_response + "\n")
            print("AI:", model_response)

            links = re.findall(r'http[s]?://\S+', model_response)
            if links:
                print("Links found in the response:", links)
                file.write("Links: " + ', '.join(links) + "\n")

if __name__ == "__main__":
  history_file = './files/conversation_history.json'
  output_file = './files/output.txt'
  
  messages = [{"role": "system", "content": "You are good at writing short paragraph that introduce people to some bizarre events that has happened in the past"},
              {"role": "user", "content": "You will write one single paragraph that describe one true story in a attention grabbing manner, but still keep it easy to read. include informations like time, location, names, and what happened. limit the words to 280 characters."}]
  
  chat_with_openai(messages, output_file, history_file)
