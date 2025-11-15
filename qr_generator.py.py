import qrcode
import requests
from urllib.parse import urlparse
from PIL import Image

url = input("enter the url: ").strip()
result = urlparse(url)

if result.scheme and result.netloc:
    print("Valid URL format")
else:
    print("Invalid URL format")
    exit()

if result.scheme == "https":
    print("✓ URL uses HTTPS")
    try:
        response = requests.get(url, timeout=5, verify=True)
        print("✓ SSL certificate is valid and trusted")

        if response.status_code == 200:
            print("✓ URL is valid and reachable")
        else:
            print(f"⚠ URL exists but returned status code: {response.status_code}")
            exit()

    except requests.exceptions.SSLError:
        print("✗ SSL certificate is invalid, expired, or not trusted")
        print("This URL may not be secure!")
        choice = input("Do you still want to create a QR code? (yes/no): ").strip().lower()
        if choice != "yes":
            print("QR code creation cancelled for security reasons")
            exit()

    except requests.exceptions.RequestException:
        print("URL is not reachable or invalid")
        exit()

elif result.scheme == "http":
    print("⚠ Warning: URL uses HTTP (NOT SECURE)")
    choice = input("Do you still want to create a QR code? (yes/no): ").strip().lower()
    if choice != "yes":
        print("QR code creation cancelled for security reasons")
        exit()

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print("URL is valid and reachable")
        else:
            print(f"URL exists but returned status code: {response.status_code}")
            exit()
    except requests.exceptions.RequestException:
        print("URL is not reachable or invalid")
        exit()


logo_link = input("\nEnter the path to your logo (or press Enter to skip): ").strip()
logo_link = logo_link.strip('"').strip("'")


QRcode = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=15,
    border=4,
)
QRcode.add_data(url)
QRcode.make(fit=True)
img = QRcode.make_image(fill_color="black", back_color="white").convert('RGB')


if logo_link:
    try:
        logo = Image.open(logo_link)

        qr_width = img.size[0]
        logo_max_size = qr_width // 3  #

        logo.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)

        halo_padding = 25
        halo_width = logo.width + (halo_padding * 2)
        halo_height = logo.height + (halo_padding * 2)
        logo_with_halo = Image.new('RGB', (halo_width, halo_height), 'white')
        logo_position = (halo_padding, halo_padding)
        logo_with_halo.paste(logo, logo_position)

        pos = ((img.size[0] - halo_width) // 2,
               (img.size[1] - halo_height) // 2)
        img.paste(logo_with_halo, pos)
        print("✓ Logo added successfully")
    except FileNotFoundError:
        print("⚠ Logo file not found. Creating QR code without logo.")
    except Exception as e:
        print(f"⚠ Error adding logo: {e}. Creating QR code without logo.")

# Save the final QR code (with or without logo)
file_path = "C:\\Users\\yusef\\Desktop\\qrcode.png"
img.save(file_path)
print(f"✓ QR Code has been created at: {file_path}")