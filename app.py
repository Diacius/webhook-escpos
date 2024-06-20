# Change these to the correct values for your device
# You can find the values on linux using `lsusb`
USB_vendor = 0x0483
USB_product = 0xa19d
SET_FONT_MODE_3 = b'\x1b!\x00'
SET_LED_MODE = b'\x1bX\x2d'
FEED_PAST_CUTTER = b'\n' * 5
SELECT_SDL_GRAPHICS = b'\x1b*\x08'
USB_BUSY = 66
# Newlines to get print above the tear bar - you may want to change this for your printer
feed_to_bar = '\n\n\n\n'

#TODO: Make this work based of a config file?
multipartEnabled = True

from escpos.printer import Usb
# Setup a temporary connection to check we can connect to the printer
usb = Usb(USB_vendor, USB_product, 0, out_ep=0x2)
usb.close()

from flask import Flask, request, Response
import time
import pipsta_image, pipsta_constants
import base64
app = Flask(__name__)
def print_multipart(jsonObject, printerObject:Usb):
    printerObject._raw(pipsta_constants.ENTER_SPOOLING)
    if jsonObject["parts"]:
        parts = jsonObject["parts"]
    for part in parts:
        # Check if the message part is an image or not
        partData = jsonObject[part]
        if partData["type"] == "image":
            printerObject.hw('INIT') # Ensure that the printer is initialised, in case underline or other formatting is left on.
            printerObject._raw(SET_FONT_MODE_3) # Set the font to 3, TODO: Is this needed? If so, why?
            # Returns an array of raw data to send, one item per command
            dataToSend = pipsta_image.pipsta_image(base64.b64decode(partData["rawdata"]))
            for command in dataToSend:
                printerObject._raw(command)
                time.sleep(0.01)
        if partData["type"] == "text":
            if partData["formatting"] == True:
                #print("Sorry, formatting is currently not implemented, printing without formatting")
                if partData['underline']:
                    printerObject._raw(pipsta_constants.underline(True))
                if partData['inverted']:
                    printerObject._raw(pipsta_constants.invertedPrinting(True))
                printerObject.text(partData['text'] + "\n")
                printerObject._raw(pipsta_constants.invertedPrinting(False))
                printerObject._raw(pipsta_constants.underline(False))
            else:
                printerObject._raw(pipsta_constants.invertedPrinting(False))
                printerObject._raw(pipsta_constants.underline(False))
                print(f"Text printing {partData["text"]}")
                printerObject.text(partData["text"] + "\n")
    printerObject._raw(pipsta_constants.EXIT_SPOOLING)    
  
@app.route('/', methods=['GET'])
def root():
    return Response("<!DOCTYPE html><html><body><h1>use /webhook to send data :)</h1></body></html>", status=418)
@app.route('/webhook', methods=['POST'])
def respond():
    # Setup connection to printer
    usb = Usb(USB_vendor, USB_product, 0, out_ep=0x2)
    # Get the JSON data from the request and print the recieved message *to the screen*
    post_data = request.json
    if post_data["multipart"] == True:
        # function should print each part in order
        print_multipart(post_data, usb)
        usb.text(feed_to_bar)
        usb.close()
    else:
        print(post_data["msg"])
        # Print out the recieved message, close the connection, and return a simple HTTP OK response
        usb.text(post_data["msg"] + feed_to_bar)
        usb.close()
    # TODO: Error handling ;)
    return Response("PRINTED", status=200)
