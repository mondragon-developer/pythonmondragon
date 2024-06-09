import qrcode

img = qrcode.make('https://www.linkedin.com/in/josemondragonit/')
img.save('linkedin_qr.png')