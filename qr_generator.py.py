import qrcode
url=input("enter the url: ").strip()
file_path="C:\\Users\\yusef\\Desktop\\qrcode.png"
qr=qrcode.QRCode()
qr.add_data(url)
img=qr.make_image()
img.save(file_path)
print("QR Code has been created")