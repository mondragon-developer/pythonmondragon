import qrcode

img = qrcode.make('https://github.com/mondragon-developer/pythonmondragon')
img.save('linkedin_qr.png')