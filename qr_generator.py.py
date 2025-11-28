import os
from py_compile import main
import qrcode
import requests
from urllib.parse import quote_plus, urlparse
from PIL import Image

def escape_wifi(str)-> str: 
    return str.replace("\\", "\\\\").replace(';', '\\;').replace("'", "\\'").replace('"', '\\"').replace(":", "\\:").replace(",", "\\,")

def build_wifi_payload()-> str: 
    ssid = input("SSID: ").strip()
    auth = input("Encryption (WPA/WEP/none): ").strip().upper()
    password = ""
    if auth != "NONE" and auth != "NOPASS":
        password = input("Password: ").strip()
    hidden = input("Hidden SSID? (yes/no): ").strip().lower()
    t = "WPA" if auth == "WPA" else ("WEP" if auth == "WEP" else "")
    payload = f"WIFI:T:{t};S:{escape_wifi(ssid)};P:{escape_wifi(password)};"
    if hidden in ("yes", "y", "true", "1"):
        payload += "H:true;"
    payload += ";"
    return payload

def build_contact_payload() -> str:
    kind = input("Format (vcard/mecard) [vcard]: ").strip().lower() or "vcard"
    name = input("Full name: ").strip()
    org = input("Organization (optional): ").strip()
    title = input("Title (optional): ").strip()
    phone = input("Phone (optional): ").strip()
    email = input("Email (optional): ").strip()
    address = input("Address (optional): ").strip()

    if kind == "mecard":
        parts = [f"N:{name}"]
        if org: parts.append(f"ORG:{org}")
        if title: parts.append(f"TITLE:{title}")
        if phone: parts.append(f"TEL:{phone}")
        if email: parts.append(f"EMAIL:{email}")
        if address: parts.append(f"ADR:{address}")
        return "MECARD:" + ";".join(parts) + ";;"
    else:
        # vCard 3.0
        v = ["BEGIN:VCARD", "VERSION:3.0", f"FN:{name}"]
        if org: v.append(f"ORG:{org}")
        if title: v.append(f"TITLE:{title}")
        if phone: v.append(f"TEL;TYPE=CELL:{phone}")
        if email: v.append(f"EMAIL;TYPE=INTERNET:{email}")
        if address: v.append(f"ADR;TYPE=HOME:;;{address}")
        v.append("END:VCARD")
        return "\n".join(v)
def build_location_payload() -> str:
    lat = input("Latitude (decimal): ").strip()
    lon = input("Longitude (decimal): ").strip()
    label = input("Label (optional): ").strip()
    payload = f"geo:{lat},{lon}"
    if label:
        payload += f"?q={quote_plus(label)}"
    return payload

def build_audio_payload() -> str:
    source = input("Audio source (URL or local file path): ").strip()
    if source.startswith("http://") or source.startswith("https://"):
        return source
    # convert local path to file URI (clients may not open file URIs)
    absolute = os.path.abspath(source)
    file_uri = "file:///" + absolute.replace("\\", "/")
    return file_uri

def build_location_payload() -> str:
    lat = input("Latitude (decimal): ").strip()
    lon = input("Longitude (decimal): ").strip()
    label = input("Label (optional): ").strip()
    payload = f"geo:{lat},{lon}"
    if label:
        payload += f"?q={quote_plus(label)}"
    return payload

def build_audio_payload() -> str:
    source = input("Audio source (URL or local file path): ").strip()
    if source.startswith("http://") or source.startswith("https://"):
        return source
    # convert local path to file URI (clients may not open file URIs)
    absolute = os.path.abspath(source)
    file_uri = "file:///" + absolute.replace("\\", "/")
    return file_uri

def add_logo_to_img(img: Image.Image, logo_path: str) -> Image.Image:
    try:
        logo = Image.open(logo_path)
        qr_width = img.size[0]
        logo_max_size = qr_width // 3
        resample = getattr(Image, "Resampling", Image).LANCZOS
        logo.thumbnail((logo_max_size, logo_max_size), resample)
        halo_padding = 25
        halo_width = logo.width + (halo_padding * 2)
        halo_height = logo.height + (halo_padding * 2)
        logo_with_halo = Image.new('RGB', (halo_width, halo_height), 'white')
        logo_position = (halo_padding, halo_padding)
        logo_with_halo.paste(logo, logo_position, logo.convert("RGBA") if logo.mode in ("RGBA", "LA") else None)
        pos = ((img.size[0] - halo_width) // 2, (img.size[1] - halo_height) // 2)
        img.paste(logo_with_halo, pos)
        print("✓ Logo added successfully")
    except FileNotFoundError:
        print("⚠ Logo file not found. Creating QR code without logo.")
    except Exception as e:
        print(f"⚠ Error adding logo: {e}. Creating QR code without logo.")
    return img  

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



def main():
    print("Select QR content type:")
    print("1) URL")
    print("2) WiFi")
    print("3) Contact (vCard/MECARD)")
    print("4) Location (geo)")
    print("5) Audio (URL or local file URI)")
    choice = input("Choice [1]: ").strip() or "1"

    payload = ""
    if choice == "1":
        url = input("Enter the URL: ").strip()
        result = urlparse(url)
        if not (result.scheme and result.netloc):
            print("Invalid URL format")
            return
        if result.scheme not in ("http", "https"):
            print("Unsupported URL scheme")
            return
        print("Valid URL format")
        if result.scheme == "https":
            print("✓ URL uses HTTPS")
            if validate_http_url(url):
                print("✓ URL is reachable")
            else:
                print("⚠ URL not reachable or invalid")
                cont = input("Create QR anyway? (yes/no): ").strip().lower()
                if cont != "yes":
                    return
                else: 
                    print("⚠ Warning: URL uses HTTP (NOT SECURE)")
            cont = input("Create QR anyway? (yes/no): ").strip().lower()
            if cont != "yes":
                return
            if validate_http_url(url):
                print("✓ URL is reachable")
        payload = url

    elif choice == "2":
        payload = build_wifi_payload()
        print(f"WiFi payload: {payload}")

    elif choice == "3":
        payload = build_contact_payload()
        print("Contact payload created")

    elif choice == "4":
        payload = build_location_payload()
        print(f"Location payload: {payload}")

    elif choice == "5":
        payload = build_audio_payload()
        print(f"Audio payload: {payload}")

    else:
        print("Invalid choice")
        return
     # Build QR
    QRcode = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )
    QRcode.add_data(payload)
    QRcode.make(fit=True)
    img = QRcode.make_image(fill_color="black", back_color="white").convert('RGB')

    logo_link = input("\nEnter path to logo (or press Enter to skip): ").strip().strip('"').strip("'")
    if logo_link:
        img = add_logo_to_img(img, logo_link)

    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    os.makedirs(desktop, exist_ok=True)
    file_name = input(f"Output filename (default qrcode.png): ").strip() or "qrcode.png"
    file_path = os.path.join(desktop, file_name)
    try:
        img.save(file_path)
        print(f"✓ QR Code has been created at: {file_path}")
    except Exception as e:
        print(f"Failed to save QR code: {e}")
        
    if __name__ == "__main__":
        main()