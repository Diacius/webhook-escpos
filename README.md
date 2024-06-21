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
Currently image and barcode printing is limited to the Pipsta/AP1400, this will be fixed soon.

## Running
You _can_ run it with the flask development server like this and it will work fine, but you probably shouldn't do this for production:
`python3 -m flask run -h **your.devices.ip.address**` (you need to include -h to allow requests from your local network)

Allowing access to the internet is **not recommended**, my code isn't perfect and the flask development shouldn't be used in production!
Furthermore, CORS is currently enabled for all connections to the API, you will want to change thsi before using the API, you have been warned!

## Printer support

**_ To put the code into Pipsta/AP1400 mode, change the variable at the top _**

| Feature             | AP1400 | Others |
|---------------------|--------|--------|
| Singlepart messages |✅      |✅     |
| Formatted Text      |✅      |✅     |
| Image printing      |✅      |✅     |
| Barcode printing    |✅      |✅     |

## Single part messages
To send a single part message to the printer make a post request to `http://<Your device's IP address>:5000/webhook` with a json body with a `msg` key like this:
```
POST /webhook HTTP/1.1
Host: 192.168.x.x:5000
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 19
Origin: http://192.168.x.x:5000

{
    "msg": "hi"
}
```
## Multipart messages

**_ Multipart messages are now stable, but please let me know if you find any problems_**
Multipart messages are a new feature being actively developed, however, if you use version 1 of the API, it should work perfectly, feel free to make an issue if you find any bugs.

An example JSON payload is this:
```json
{
    "multipart": true,
    "api_version": 1,
    "parts": ["image1", "text1", "text2", "barcode1"],
    "image1": {"type": "image", "imagedata": "iVBORw0KGgoAAAANSUhEUgAAAYAAAAA/AQMAAADT4o3oAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAGUExURQAAAP///6XZn90AAAAJcEhZcwAADsMAAA7DAcdvqGQAAAORSURBVEjH5Za9btRAEMfHcaJDCZJzEoh0puYJKKI4hREvEGpegQaJIopX4kVSokuRR7jlHUBpV6ILjZGIOEU+D/Ox693zXRIQJatEsTf739/Mf/bDgNgCvMV72w0iNFf6TIJzgD16ms03j+4v0TUIVR4EHQAjvkAxjHnVJILjDE2FcAZBsGDB7sxEwTVUCQCABD0cQeMFLfg2CREDlPgrCCiAfXqHw3WBD5JzKvFbIgAQQnUHgUeUaFYFHZxS52YB51SMBM19hFYI0KwIOsqBCFeDS2yUr4PjECKBXKLsehKQi7nUoa5rLUVdc8UtwHYTCSjsDg5I0INUmmYxu7NLsl8qboU1EHDGKamgCwK0FP9SMWjEjkhAM20k7gml13hBW6g7HKfZk1HDeLSV/jMnQSC0E4kdIKMe8Tsh2FKty8mPQFjwzOIVDa1GBKf4RyxICL2aG/xZJxxkFERC8IKq1551wktatSmBurapHqUXJAQWEOEUEgK5tICtOS1UJfSzMeEx9COCg2c8ka4iBwmh5Ry2sx4aGAg0iZMn3oyVCC74dTYLhOKCBAmhQJst1RGuA9fkpD6hnJ406CZaKCK8x0gwhZtLVU0ZaiKt9ASmc5wQrIbSUplptPEE3wqZXQiJgAhQWd4G9FOMBYFwBIh9JDQWdhqKwE5WBLRGPcFSJch9JVC9SAAvCMKm3H5KCIuU4FYIspZ4Mt0cI4I5zG6egidwgZ2u1lbOJ3POb1ufKMZIyBxAIPT++NDJyIxTKsPJa6wVqTlkFlLCrZHXRT5arZGQ20hAKsK+7DgVpGsp5mCCwMgivZXz1ROqTQSzkgPbTxN1mkO1RkhzMGEbzDcRJkkOeRCEoJfTfRWUkZAPOVAIkaBTtv6eMPECW/jEiOCgGHawP/6dP8XtZCUkn8PP43IQ+CmdJ7hNBFoNCUGntEGQrQsO6WRSAltk8hVCCxsJphgEVj8HQg4t1MMdlGlxzBlfdIPA6T3dgv5d6GUxInygbSp9mYyc7lf4Y6p2dTAcTZ1fYDT4XRCAvx547PVcoRBWRxcIFTxPCF0Q+Bbfuuyr5MAnH/1K30fUsyiaz6+e0G8ZJXCfP2autAIpwYa3JW2TigWfqS/DaLdbJSwCgZMTwXcSFIlg1LrauyRfBrpJLB/ueGeb4SCoOl/N5j4B/osApTjxS+ABwU54fvMngsEubQ8LltNp81eCUfsPBYi/AREiYK1CRJO2AAAAAElFTkSuQmCC"},
    "text1": {"type": "text", "formatting": false, "text": "This text is unformatted"},
    "text2": {"type": "text", "formatting": true, "underlined": true, "inverted": true, "text": "This text is underlined"},
    "barcode1": {"type": "barcode", "barcode-type": "UPC-A", "code": "12345678910"}
}
```
The key `multipart`, when set to true, signifies a multipart, if the message is multipart, the api_version must be set, and be 1 or higher.

The key `parts` should be a list of all the parts of the message, _in the order you want them printed._
There should be a key corresponding to every item in the `parts` list.

An image key is made up of two parts `type` which should be set to `image` so that the program so that the correct code is selected, and `image` which should be the raw bytes of the image file, encoded as base64. [Any image file that can be opened by Pillow is supported.](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html), currently image printing will only work properly with an AP1400

A barcode key has the `"type": "barcode"` property and the `barcode-type` property which should be one of:
- UPC-A
- UPC-E
- EAN-13
- EAN-8
- Code 39
- Int2 of 5
- Code 128A
- Code 128B
- Code 128C
- Code 93
And a `code` key which can be numeric or alphanumeric depending on the barcode type

A text key can be formatted or unformatted. A formatted key can be `underlined` or `inverted` (upside down). If the `formatted` key is `false` then the text will print normally. Both formatted and unformatted text will wrap onto the nextline

### Formatting

You may add the following types of formatting to your messages:
- Underlines
- Inverted Text

## Tested On
Pipsta - a rebadged Able Systems ap1400 designed for Raspberry Pis

Used it with another printer? Make an issue or a pull request!
