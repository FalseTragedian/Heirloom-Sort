"""
Heirloom-Sort.py
Authors: Geoff Bell, Ryan David Simpson, Alex Bridges

Work-in-progress. When complete, this will allow users to sort uncategorized,
unlabeled images into directories based on various criteria, by using Mistral
AI image recognition.
Currently, it just puts each picture into a folder named for a brief
description of the picture's content.
"""

#Import packages.
import os
from PIL import Image
from llama_index.multi_modal_llms.mistralai import MistralAIMultiModal
from pathlib import Path
import base64
from mistralai import Mistral
from time import sleep

#Taken from the Mistral documentation
def encode_image(image_path):
    """This function takes a local filesystem path to an image as input, and converts the image to a base64-encoded binary stream.
    This is the format used to upload the image to the LLM.
    Input: image_path: A string or path-like object containing the full path to the image file.
    Returns: The image data encoded with base64.
    """
    print('Encoding to base64...')
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:  # Added general exception handling
        print(f"Error: {e}")
        return None

def saveRename(savePath = '.', filename = '0.png', image = None):

    if not os.path.exists(savePath + filename):
        image.save(fp = savePath + filename)
        print("Saving: " + savePath + filename)
    else:
        filenox, ext = os.path.splitext(filename)
        filename = filenox + '0' + ext
        saveRename(savePath, filename, image)

def getChatResponse(image = None):
    base64_image = encode_image(image)
    #This is also from Mistral docs.
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Describe this image in 1 to 3 words."
                },
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}" 
                }
            ]
        }
    ]

    # Get the chat response
    chat_response = client.chat.complete(
        model='pixtral-12b-2409',
        messages=messages
    )
    sleep(2)

    # Return response as a string
    return str(chat_response.choices[0].message.content)

def sortImage(path = '.', filename = '0.png'):
    try:
        print(path + filename)
        image = Image.open(path + filename)
        newFolder = getChatResponse(path + filename)
        savePath = (path + newFolder + '\\')
        if not os.path.exists(savePath):
            os.makedirs(savePath)
        saveRename(savePath, filename, image)
    except Exception as e:
        image = None
        print('Exception in sortImage: ' + str(e))


path = 'C:\\Temp\\Pictures\\'

mistralKey = input('Please copy and paste Mistral AI API key here:')
os.environ['MISTRAL_API_KEY'] = mistralKey
client = Mistral(api_key = mistralKey)

fileList = os.listdir(path)
for filename in fileList:
    if os.path.isfile(path + filename):
        sortImage(path, filename)

print('Finished.')
