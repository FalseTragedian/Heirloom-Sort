Heirloom-Sort.py

Authors: Geoff Bell (FalseTragedian), Alex Bridges (alexbridges97), Ryan David Simpson (ryansimpsonn)

A Python script to use Mistral AI to sort a given directory of images into subdirectories.

This is a final project for an "Intro to Artificial Intelligence" class. Don't expect long-term, professional support.

Takes input of a directory name, offers a list of pre-engineered prompts or the option to create your own, and sorts images within the directory into folders using AI identification.

By default it targets the current working directory. Recommend copying your pictures to a new directory for testing purposes, don't run this on the original pictures. It should work but I claim no liability if something goes wrong.

The prompt designs are still a work in progress. If you would like to create your own prompt, remember to give precise and clear instructions like you're speaking to a child who is also a robot. :)

Installation:

In addition to the latest version of Python, the following Python packages are prerequisites: (Enter these in the command line.)

pip install pillow

pip install mistralai

pip install llama-index-multi-modal-llms-mistralai

To use this program you need to bring your own Mistral API key.
1. Go to console.mistral.ai
2. Login or create an account
3. Choose "Billing" from the menu on the left and choose your access plan - this script was designed around the limitations of the free "Experiment" plan so you don't need a paid plan.
4. Choose "API Keys" from the menu on the left
5. Click "Create new key".
6. Click "Create key" in the pop-up.
7. Copy the key it generates for you.
8. The first time the script is run, it will prompt you to enter the key. It will then save it as a text file named "api_key.txt" in the same directory. Alternately, you can create this file (containing ONLY the key) yourself.
