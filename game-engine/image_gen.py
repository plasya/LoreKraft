from openai import OpenAI
import requests
import os
import time
import random
import string

def image_gen(prompt):
    # Initialize OpenAI client
    client = OpenAI(api_key="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")
    
    # Generate the image
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    
    # Get the URL of the generated image
    image_url = response['data'][0]['url']
    
    # Create a unique filename based on the current timestamp
    timestamp = int(time.time())
    file_name = f"generated_image_{timestamp}.png"
    
    # Define the file path where the image will be saved
    file_path = os.path.join("static/src", file_name)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Download the image from the URL and save it locally
    image_data = requests.get(image_url).content
    with open(file_path, 'wb') as image_file:
        image_file.write(image_data)
    return "54.67.37.79:8000/"+file_path

