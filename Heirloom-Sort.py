'''
Heirloom-Sort.py
Authors: Geoff Bell, Ryan David Simpson, Alex Bridges

Work-in-progress. When complete, this will allow users to sort uncategorized,
unlabeled images into directories based on various criteria, by using Mistral
AI image recognition.
Currently, it just puts each picture into a folder named for a brief
description of the picture's content.
'''

#Import packages.
import os
import PIL
from PIL import Image
from llama_index.multi_modal_llms.mistralai import MistralAIMultiModal
from pathlib import Path
import base64
from mistralai import Mistral
from time import sleep

#Taken from the Mistral documentation
def encode_image(image_path):
    '''This function takes a local filesystem path to an image as input, and
    converts the image to a base64-encoded binary stream.
    This is the format used to upload the image to the LLM.
    Input: image_path: A string or path-like object containing the full path
        to the image file.
    Returns: The image data encoded with base64.
    '''
    #Encode the image to base64.
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
    '''This function saves an already loaded image to a new location
    and filename.
    If a file with the new name already exists, it will add a '0' to the
    new filename and recursively call itself.
    Inputs: savePath: a String or Path-like object containing the full path
            to the directory where the file should be placed.
            filename: The new filename under which to save the file.
            image: pillow Image object containing the image data.
    Returns: none.
    '''
    #Check if file with that name already exists
    if not os.path.exists(savePath + filename):
        #Save the file
        image.save(fp = savePath + filename)
        #Tell the user what's going on
        print("Saving: " + savePath + filename)
    else:
        #Split off the file extension from the file
        filenox, ext = os.path.splitext(filename)
        #Insert a zero at the end of the filename and reassemble
        filename = filenox + '0' + ext
        #Recursive call
        saveRename(savePath, filename, image)

#Changed this to accept user specifiable prompt. -- Alex Bridges
def getChatResponse(prompt = "Describe this image in 1 to 3 words.", image = None):
    '''This should be edited to take multiple prompts for different uses.
    For now, it only uses the single prompt.
    '''
    #First we encode the image.
    base64_image = encode_image(image)
    #This is also from Mistral docs.
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
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
    #This is to prevent rate errors from the Mistral serer.
    sleep(2)

    # Return response as a string
    return str(chat_response.choices[0].message.content)

def sortImage(path = '.', filename = '0.png', deleteOriginalFiles = 'N', userPrompt = 'Describe this image in 1-3 words.'):
    '''This should be edited to take multiple prompts for different uses.
    '''
    try:
        #Report which file we're opening
        print(path + filename)
        #Open the file
        image = Image.open(path + filename)
        #Call Mistral, ask it to identify the image content
        newFolder = getChatResponse(userPrompt, path + filename)
        #Use that response to create a new save path for the image
        savePath = (path + newFolder + '\\')
        #Check if the new folder already exists
        if not os.path.exists(savePath):
            #If not, create it
            os.makedirs(savePath)
        #Function call to save the file in the new location
        saveRename(savePath, filename, image)
        #Close the image to cleanup memory
        image.close()
        if deleteOriginalFiles.upper() == 'Y':
            #Deletes original file if user selects that option.
            print("Deleting original file: " + path + filename)
            os.remove(path + filename)
    except PIL.UnidentifiedImageError:
        #This should trigger if a non-image file is encountered
        print('File is not an image, skipping.')
    except Exception as e:
        #General exception handling: 
        image = None
        print('Exception in sortImage: ' + str(e))

#Check if a text file named "api_key.txt" exists in the same directory from which the script was launched.
if os.path.exists(os.getcwd() + '/api_key.txt'):
    #If so, open the file and read it as the key.
    keyFile = open('api_key.txt', 'r')
    mistralKey = keyFile.read()
else:
    #If not, take the key as a manual input.
    mistralKey = input('Please copy and paste Mistral AI API key here:')
    #Then create the text file and write the key to it.
    keyFile = open('api_key.txt', 'w')
    keyFile.write(mistralKey)
#Store the key in OS environment variables (I don't know why but this is volatile).
os.environ['MISTRAL_API_KEY'] = mistralKey
#Open the Mistral client with the API key.
client = Mistral(api_key = mistralKey)
#Close the text file.
keyFile.close()

# User interface that accepts custom category and packages that into a prompt to be fed to Mistral. -- Alex Bridges
category = input('Please select a method of sorting: \n1. By location \n2. By number of people present \n3. By activity \n4. Custom category\n')
userPrompt = ""
if category == '1' or "location" in category.lower():
    userPrompt = "Fit this image into one of these categories based on the location depicted; either Indoor or, if outdoor, specify the general location without using the word 'outdoor' (i.e. City, Park, Beach, Mountains, etc.). Do not include any other text in your response."
elif category == '2' or "number" in category.lower():
    userPrompt = "Fit this image into one of these categories based on the number of people present in the foreground: 0 people, 1-3 people, 4-6 people, 7+ people. Do not include any other text in your response."
elif category == '3' or "activity" in category.lower():
    userPrompt = "Fit this image into a category based on the activity taking place: some examples include: Vacation, Party, Sports, School, etc. Do not include any other text in your response."
else:
    userPrompt = "Describe this imaged based on "
    userPrompt += input('Enter a custom category:')
    userPrompt += " in 1 to 3 words."

#Placeholder. Final version should take an input for the folder to target. DONE -- Alex Bridges
#Maybe default to '.' so the script can be dropped straight into the folder.
path = str(os.getcwd() + '\\')
customFileDestination = input('Would you like to specify a custom file of images to be sorted? If so, type Y and press enter. \nOtherwise, type N or leave blank to default to the current working directory.\n')
if customFileDestination.upper() == 'Y':
    path = input('Enter the file path:')

#Needed: an option to delete the original files. DONE - Alex Bridges
#Needed: a list of different sorting categories. To include "Custom prompt". DONE -- Alex Bridges

deleteOriginalFiles = input('Would you like to delete the original files? If so, type Y and press enter. \nOtherwise, type N and press enter.\n')

#Main loop here.
#Creates a list of files in the target directory.
#Moved file deletion steps to sortImage(). --Geoff Bell
fileList = os.listdir(path)
#Iterates through each item in the list.
for filename in fileList:
    #Checks if the file is a directory. If so, skips it.
    if os.path.isfile(path + filename):
        #Copies the file to a new folder.
        sortImage(path, filename, deleteOriginalFiles.upper(), userPrompt)

print('Directory ' + path + ' finished.')
print('Program will close in 10 seconds. Goodbye.')
sleep(10)
