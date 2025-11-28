# QR Code Generator with URL Validation

A Python application that generates QR codes for valid and reachable URLs. The program validates both the URL structure and accessibility before creating the QR code.

## Features

- URL Structure Validation: Checks if the URL has proper format (scheme and domain)
- URL Reachability Check: Verifies that the URL actually exists and is accessible
- QR Code Generation: Creates a QR code image only for valid, reachable URLs
- Error Handling: Provides clear feedback for invalid or unreachable URLs

## Requirements

- Python 3.x
- qrcode library
- requests library

## Installation

1. Clone this repository:
```bash
git clone https://github.com/YoussefAbdelkawy/qr_code_generator.git
cd qr_code_generator
```

2. Install required dependencies:
```bash
pip install qrcode requests
```

## Usage

1. Run the script:
```bash
python qr_generator.py.py
```

2. Enter a URL when prompted:
```
enter the url: https://www.example.com
```

3. The program will:
   - Validate the URL format
   - Check if the URL is reachable
   - Generate a QR code if the URL is valid and accessible
   - Save the QR code as `qrcode.png` on your Desktop

## How It Works

1. URL Format Validation: Uses `urllib.parse` to check if the URL has a valid scheme (http/https) and domain
2. Reachability Check: Sends an HTTP GET request to verify the URL exists and returns a 200 status code
3. QR Code Generation: Creates a QR code image that can be scanned to access the URL

## Example Output

### Valid and Reachable URL:
```
enter the url: https://www.google.com
Valid URL format
URL is valid and reachable
QR Code has been created
```

### Invalid URL Format:
```
enter the url: not a url
Invalid URL format
```

### Valid Format but Unreachable:
```
enter the url: https://fakeurlfortesting12345.net
Valid URL format
URL is not reachable or invalid
```

## Output Location

The generated QR code is saved to:
```
C:\Users\yusef\Desktop\qrcode.png
```

Note: You can modify the `file_path` variable in the code to change the output location.

## Error Handling

The program handles the following scenarios:
- Invalid URL structure (missing scheme or domain)
- Unreachable URLs (connection errors, timeouts)
- HTTP errors (non-200 status codes)

## License

This project is open source and available for educational purposes.

## Author

Youssef Abdelkawy
