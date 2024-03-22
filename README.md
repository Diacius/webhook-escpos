# webhook-escpos
Print out messages recieved via a webhook on a connected ESC/POS compatible printer - which are usually thermal receipt printers

## Requirements
[Flask](https://flask.palletsprojects.com/en) - to recieve webhook requests

[python-escpos](https://python-escpos.readthedocs.io/en/latest/) - to communicate with ESC/POS compatible printers

## Setup
1. Download app.py or clone the repository
2. Install the required python modules from pip: `flask` and `python-escpos`
3. Change the USB vendor and product IDs at the top of the code so that the program can connect to the printer **if your printer uses serial than you will need to change part of the code - instructions are in a seperate file**

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
## Tested On
Pipsta - a rebadged Able Systems ap1400 designed for Raspberry Pis

Used it with another printer? Make an issue or a pull request!
