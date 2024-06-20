# webhook-escpos
Print out messages recieved via HTTP POST (webhook) on a connected ESC/POS compatible printer - which are usually thermal receipt printers.

## Requirements
[Flask](https://flask.palletsprojects.com/en) - to recieve webhook requests

[python-escpos](https://python-escpos.readthedocs.io/en/latest/) - to communicate with ESC/POS compatible printers

## Setup
1. Download app.py or clone the repository
2. Install the required python modules from pip: `flask` and `python-escpos`
3. Change the USB vendor and product IDs at the top of the code so that the program can connect to the printer **if your printer uses serial than you will need to change part of the code - instructions are in a seperate file**

## Use Cases
This works with Uptime Kuma, and can be setup as a notification, so your printer can print out status reports.


## Running
You _can_ run it with the flask development server like this and it will work fine, but you probably shouldn't do this for production:
`python3 -m flask run -h **your.devices.ip.address**` (you need to include -h to allow requests from your local network)

Allowing access to the internet is probably unwise, my code probably isn't incredible and I have no idea how secure the flask development server is!

To send messages to the printer make a post request to `http://192.168.x.x:5000/webhook` with a json body with a `msg` key like this:
```
POST /webhook HTTP/1.1
Host: 192.168.1.34:5000
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 19
Origin: http://192.168.1.34:5000
Pragma: no-cache
Cache-Control: no-cache

{
    "msg": "hi"
}
```
## Multipart messages

**_This feature is a WORK IN PROGRESS, the format of multipart messages is very likely to change for the time being_**
Multipart messages are a new feature being actively developed, an example JSON payload is this:
```json
{
    "multipart": true,
    "parts": ["image1", "text1", "text2"],
    "image1": {"type": "image", "rawdata": "iVBORw0KGgoAAAANSUhEUgAAAYAAAAA/AQMAAADT4o3oAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAGUExURQAAAP///6XZn90AAAAJcEhZcwAADsMAAA7DAcdvqGQAAAORSURBVEjH5Za9btRAEMfHcaJDCZJzEoh0puYJKKI4hREvEGpegQaJIopX4kVSokuRR7jlHUBpV6ILjZGIOEU+D/Ox693zXRIQJatEsTf739/Mf/bDgNgCvMV72w0iNFf6TIJzgD16ms03j+4v0TUIVR4EHQAjvkAxjHnVJILjDE2FcAZBsGDB7sxEwTVUCQCABD0cQeMFLfg2CREDlPgrCCiAfXqHw3WBD5JzKvFbIgAQQnUHgUeUaFYFHZxS52YB51SMBM19hFYI0KwIOsqBCFeDS2yUr4PjECKBXKLsehKQi7nUoa5rLUVdc8UtwHYTCSjsDg5I0INUmmYxu7NLsl8qboU1EHDGKamgCwK0FP9SMWjEjkhAM20k7gml13hBW6g7HKfZk1HDeLSV/jMnQSC0E4kdIKMe8Tsh2FKty8mPQFjwzOIVDa1GBKf4RyxICL2aG/xZJxxkFERC8IKq1551wktatSmBurapHqUXJAQWEOEUEgK5tICtOS1UJfSzMeEx9COCg2c8ka4iBwmh5Ry2sx4aGAg0iZMn3oyVCC74dTYLhOKCBAmhQJst1RGuA9fkpD6hnJ406CZaKCK8x0gwhZtLVU0ZaiKt9ASmc5wQrIbSUplptPEE3wqZXQiJgAhQWd4G9FOMBYFwBIh9JDQWdhqKwE5WBLRGPcFSJch9JVC9SAAvCMKm3H5KCIuU4FYIspZ4Mt0cI4I5zG6egidwgZ2u1lbOJ3POb1ufKMZIyBxAIPT++NDJyIxTKsPJa6wVqTlkFlLCrZHXRT5arZGQ20hAKsK+7DgVpGsp5mCCwMgivZXz1ROqTQSzkgPbTxN1mkO1RkhzMGEbzDcRJkkOeRCEoJfTfRWUkZAPOVAIkaBTtv6eMPECW/jEiOCgGHawP/6dP8XtZCUkn8PP43IQ+CmdJ7hNBFoNCUGntEGQrQsO6WRSAltk8hVCCxsJphgEVj8HQg4t1MMdlGlxzBlfdIPA6T3dgv5d6GUxInygbSp9mYyc7lf4Y6p2dTAcTZ1fYDT4XRCAvx547PVcoRBWRxcIFTxPCF0Q+Bbfuuyr5MAnH/1K30fUsyiaz6+e0G8ZJXCfP2autAIpwYa3JW2TigWfqS/DaLdbJSwCgZMTwXcSFIlg1LrauyRfBrpJLB/ueGeb4SCoOl/N5j4B/osApTjxS+ABwU54fvMngsEubQ8LltNp81eCUfsPBYi/AREiYK1CRJO2AAAAAElFTkSuQmCC"},
    "text1": {"type": "text", "formatting": false, "text": "This text is unformatted"},
    "text2": {"type": "text", "formatting": true, "underline": true, "text": "This text is underlined"}
}
```
multipart must be set to true, and parts should be an array, listing the keys of all parts of the message.

imagex is an image payload, which should be encoded as base64
textx is a text payload which can be unformatted, or formatted.

## Tested On
Pipsta - a rebadged Able Systems ap1400 designed for Raspberry Pis

Used it with another printer? Make an issue or a pull request!
