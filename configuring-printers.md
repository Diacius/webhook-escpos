# Configuring your printer
The module that this project uses to communicate to printers - escpos-python - supports USB, Serial and Network connections to printers.
Although this project uses USB connections by default, it is very easy to set it up to use a different connection type.
Referring to this page for the escpos-python module documentation will help you with this: [https://python-escpos.readthedocs.io/en/latest/user/usage.html](https://python-escpos.readthedocs.io/en/latest/user/usage.html#usb-printer)
(you can navigate to the section for the type of connection you are using.)

If this guidance is not enough and you're still not sure what to do, the documentation above goes into more depth, simply replace each `printer = Usb()` with the correct details for your prinnter
## USB
1. Find your devices vendor and product ids using `lsusb`
2. Edit 2 variables at the top of the file `USB_vendor`, and `USB_product`. If lsusb says the device is `1234:5678`, then `USB_vendor` is `1234` and `USB_product` is `5678`
## Serial
## Network
