import qrcode
import requests
from urllib.parse import urlparse

url=input("enter the url: ").strip()
result = urlparse(url)
if result.scheme and result.netloc:
    print("Valid URL format")
else:
    print("Invalid URL format")
    exit()
try:
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        print("URL is valid and reachable")
    else:
        print(f"URL exists but returned status code: {response.status_code}")
except requests.exceptions.RequestException:
    print("URL is not reachable or invalid")
file_path="C:\\Users\\yusef\\Desktop\\qrcode.png"
qr=qrcode.QRCode()
qr.add_data(url)
img=qr.make_image()
img.save(file_path)
print("QR Code has been created")