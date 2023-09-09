# webhook-escpos
Print out messages recieved via a webhook on a connected ESC/POS compatible printer - which are usually thermal receipt printers

## Requirements
[Flask](https://flask.palletsprojects.com/en) - to recieve webhook requests

[python-escpos](https://python-escpos.readthedocs.io/en/latest/) - to communicate with ESC/POS compatible printers

## Tested On
Pipsta - a rebadged Able Systems ap1400 designed for rasperry pis
Used it with another printer? Make an issue or a pull request!

## Setup
Simply install the required modules from pip and change the usb product and manafacturer IDs to the correct values for your device - full guide coming soon™
