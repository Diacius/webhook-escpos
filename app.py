from escpos.printer import Usb
usb = Usb(0x0483, 0xa19d, 0, out_ep=0x2)
feed_to_bar = '\n\n\n\n'

usb.close()

from flask import Flask, request, Response
import json
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def respond():
    usb = Usb(0x0483, 0xa19d, 0, out_ep=0x2)
    post_data = request.json
    print(post_data["msg"])
    usb.text(post_data["msg"] + feed_to_bar)
    usb.close()
    return Response("PRINTED", status=200)
