from pyzbar import pyzbar
from urllib.parse import urlparse, parse_qs
import urllib
import cv2
import pyautogui
import pyotp
import json
import sys
from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton

image = pyautogui.screenshot()
barcodes = pyzbar.decode(image)
new_auths = False
if barcodes:
    print(barcodes[0].data.decode("utf-8"))
    o = urlparse(barcodes[0].data.decode("utf-8"))
    if o.scheme == 'otpauth':
        new_auths = True
        print(f"Label: {urllib.parse.unquote(o.path)[1:]}")
        qs = parse_qs(o.query)
        print(f"Secret: {qs['secret'][0]}")
        if "issuer" in qs:
            issuer = qs['issuer']
        else:
            issuer = None
        

auths = json.load("2fa-secrets.json")
if new_auths:
    auths.append({'label': barcodes[0].data.decode("utf-8"), 'secret': qs['secret'][0], 'issuer': issuer})
with open("2fa-secrets.json", 'w') as f:
    json.dump(auths)

class AutoQR(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("AutoQR")
        for i in auths:
            totp = pyotp.TOTP(i["secret"])
            


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())

