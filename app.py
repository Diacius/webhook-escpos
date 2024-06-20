# Change these to the correct values for your device
# You can find the values on linux using `lsusb`
USB_vendor = 0x0483
USB_product = 0xa19d
# Newlines to get print above the tear bar - you may want to change this for your printer
feed_to_bar = '\n\n\n\n'

#TODO: Make this work based of a config file?
multipartEnabled = True

from escpos.printer import Usb
# Setup a temporary connection to check we can connect to the printer
usb = Usb(USB_vendor, USB_product, 0, out_ep=0x2)
usb.close()

from flask import Flask, request, Response
import json
import pipsta_image, pipsta_constants
import base64
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def decode_multipart(jsonObject):
    print("Raw JSON "+ jsonObject)
    if jsonObject["parts"]:
        parts = jsonObject["parts"]
    for part in parts:
        # Check if the message part is an image or not
        if jsonObject[part][type] == "image":
            usb.hw('INIT') # Ensure that the printer is initialised, in case underline or other formatting is left on.
            usb._raw(SET_FONT_MODE_3) # Set the font to 3, TODO: Is this needed? If so, why?
            pipsta_image.pipsta_image(base64.b64decode(jsonObject[part]["rawdata"]))
            
            
  
def respond():
    # Setup connection to printer
    usb = Usb(USB_vendor, USB_product, 0, out_ep=0x2)
    # Get the JSON data from the request and print the recieved message *to the screen*
    post_data = request.json
    if post_data["multipart"] == True:
        # decode_multipart should return the raw payload needed as an arrray
        parts = decode_multipart(post_data)
    else:
        print(post_data["msg"])
        # Print out the recieved message, close the connection, and return a simple HTTP OK response
        usb.text(post_data["msg"] + feed_to_bar)
        usb.close()
    # TODO: Error handling ;)
    return Response("PRINTED", status=200)
