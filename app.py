from escpos.printer import Usb
from flask import Flask, request, Response
from flask_cors import CORS
import time
import pipsta_image, pipsta_constants
import base64
import io
from PIL import Image
import json

with open('config.json', 'r') as configFile:
    configObject = json.load(configFile)

# Change these to the correct values for your device
# You can find the values on linux using `lsusb`
USB_vendor = 0x0483
USB_product = 0xa19d

# Don't change this, it may break things
API_VERSION = 1

SET_FONT_MODE_3 = b'\x1b!\x00'
SET_LED_MODE = b'\x1bX\x2d'

# Newlines to get print above the tear bar - you may want to change this for your printer
feed_to_bar = '\n\n\n\n'

# If your printer is not a Pipsta/AP1400 SET THIS VALUE TO FALSE, otherwise image printing will be broken and may print large amounts of garbage.
pipsta = configObject["pipsta"]
if configObject["pipsta"] == True:
    print("Pipsta enabled")

# Setup a temporary connection to check we can connect to the printer
usb = Usb(USB_vendor, USB_product, 0, out_ep=0x2)
usb._raw(pipsta_constants.invertedPrinting(False))
usb._raw(pipsta_constants.underline(False))
usb.close()

app = Flask(__name__)
if configObject["CORS"]:
    CORS(app)
def print_multipart(jsonObject, printerObject:Usb):
    if jsonObject["parts"]:
        parts = jsonObject["parts"]
    with open("lastjson.json", "w+t") as lastjson:
        lastjson.write(str(jsonObject))
        lastjson.close()
    for part in parts:
        # Check if the message part is an image or not
        partData = jsonObject[part]
        if partData["type"] == "image":
            printerObject._raw(pipsta_constants.ENTER_SPOOLING)
            printerObject.hw('INIT') 
            # Ensure that the printer is initialised, in case underline or other formatting is left on.
            #printerObject._raw(SET_FONT_MODE_3) # Set the font to 3, TODO: Is this needed? If so, why?
            # If we are using a pipsta use my code
            if pipsta == True:
                # Returns an array of raw data to send, one item per command
                printerObject._raw(pipsta_constants.invertedPrinting(False))
                printerObject._raw(pipsta_constants.underline(False))
                dataToSend = pipsta_image.pipsta_image(base64.b64decode(partData["imagedata"]))
                for command in dataToSend:
                    printerObject._raw(command)
                    time.sleep(0.01)
            else:
                # Assume that standard printing works
                file = io.BytesIO(base64.b64decode(partData["imagedata"]))
                printerObject.image(Image.open(file))
            printerObject._raw(pipsta_constants.EXIT_SPOOLING)
        elif partData["type"] == "text":
            # Reset formatting
            printerObject._raw(pipsta_constants.invertedPrinting(False))
            printerObject._raw(pipsta_constants.underline(False))
            printerObject._raw(pipsta_constants.ENTER_SPOOLING)
            if partData["formatting"] == True:
                if partData['underlined'] == True:
                    printerObject._raw(pipsta_constants.underline(True))
                if partData['inverted'] == True:
                    printerObject._raw(pipsta_constants.invertedPrinting(True))
                printerObject._raw(partData['text'] + "\n")
            else:
                
                print(f"Text printing {partData["text"]}")
                printerObject.text(partData["text"] + "\n")
            printerObject._raw(pipsta_constants.EXIT_SPOOLING)
        elif partData["type"] == "barcode":
            printerObject._raw(pipsta_constants.invertedPrinting(False))
            printerObject._raw(pipsta_constants.underline(False))
            printerObject._raw(pipsta_constants.ENTER_SPOOLING)
            if pipsta == True:
                printerObject._raw(pipsta_constants.barcode(partData["barcode-type"], partData["code"]))
            else:
                printerObject._hw_barcode(partData["code"], partData["barcode-type"])
            printerObject._raw(pipsta_constants.EXIT_SPOOLING)
  
@app.route('/', methods=['GET'])
def root():
    # Send I'm a teapot because why not :p
    return Response("<!DOCTYPE html><html><body><h1>use /webhook to send data :)</h1></body></html>", status=418)
@app.route('/webhook', methods=['POST'])
def respond():
    # Setup connection to printer, creating an object
    usb = Usb(USB_vendor, USB_product, 0, out_ep=0x2)
    # Get the JSON data from the request and print the recieved message *to the screen*
    post_data = request.json
    if post_data["multipart"] == True:
        # Check that an API version was provided
        try:
            post_data["api_version"]
            
        except KeyError:
            print(f"ERR_NO_API_VER: No API Version specified in API call")
            return Response("ERR_NO_API_VER: Please provide an API version", status=400)
        # If the API versions match between the code and request we can attempt to print
        if post_data["api_version"] == API_VERSION:
            # function should print each part in order
            print_multipart(post_data, usb)
            usb.text(feed_to_bar)
            usb._raw(pipsta_constants.EXIT_SPOOLING)
            usb.close()
        else:
            print(f"ERR_API_VER_MISMATCH: Message received was for a different version of this program! This program is compatible with v{API_VERSION}, but the message was v{post_data["api_version"]}")
    else:
        # Catch all exceptions to this rule
        # Print out the recieved message, close the connection, and return a simple HTTP OK response
        usb.text(post_data["msg"] + feed_to_bar)
        usb.close()
    # TODO: Error handling ;)
    return Response("PRINTED", status=200)
