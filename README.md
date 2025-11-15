# QR Code Generator with Custom Logo

A Python-based QR code generator with SSL validation, security checks, and custom logo support.

## Features

- ✅ URL Validation: Validates URL format before generating QR code
- 🔒 SSL Certificate Verification: Checks HTTPS certificates for security
- 🎨 Custom Logo Support: Add your own logo to the center of QR codes
- ⚠️ Security Warnings: Alerts for HTTP (non-secure) URLs and invalid SSL certificates
- 🖼️ High Error Correction: Uses ERROR_CORRECT_H (30% error tolerance) for reliable scanning
- 📱 Optimized for Scanning: Large QR codes (box_size=15) for easy mobile scanning

## Requirements
```bash
pip install qrcode[pil] requests Pillow
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YoussefAbdelkawy/qr_code_generator.git
cd qr_code_generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script:
```bash
python qr_generator.py
```

### Step-by-Step Guide

1. **Enter URL**: Input the URL you want to convert to a QR code
```
enter the url: https://example.com
```

2. **Security Check**: The script will validate:
   - URL format
   - HTTPS usage
   - SSL certificate validity
   - URL reachability

3. **Add Logo (Optional)**: Provide the path to your logo image
```
Enter the path to your logo (or press Enter to skip): C:\path\to\logo.png
```
   - Supports: PNG, JPG, JPEG, WebP
   - Logo will be automatically resized and centered
   - White halo added around logo for better contrast

4. **QR Code Generated**: The QR code will be saved to your Desktop
```
✓ QR Code has been created at: C:\Users\yousef\Desktop\qrcode.png
```

## Examples

### Basic QR Code (No Logo)
```
enter the url: https://github.com
✓ URL uses HTTPS
✓ SSL certificate is valid and trusted
✓ URL is valid and reachable

Enter the path to your logo (or press Enter to skip): [press Enter]

✓ QR Code has been created at: C:\Users\yousef\Desktop\qrcode.png
```

### QR Code with Logo
```
enter the url: https://mywebsite.com
✓ URL uses HTTPS
✓ SSL certificate is valid and trusted
✓ URL is valid and reachable

Enter the path to your logo (or press Enter to skip): C:\logos\company_logo.png
✓ Logo added successfully
✓ QR Code has been created at: C:\Users\yousef\Desktop\qrcode.png
```

### HTTP Warning (Insecure URL)
```
enter the url: http://example.com
⚠ Warning: URL uses HTTP (NOT SECURE)
Do you still want to create a QR code? (yes/no): yes
URL is valid and reachable
...
```

## Technical Specifications

- **Error Correction Level**: H (High) - 30% of codewords can be restored
- **Box Size**: 15 pixels per module (larger for better scanning)
- **Border**: 4 modules (standard QR code quiet zone)
- **Logo Coverage**: ~33% of QR code area (within error correction tolerance)
- **Logo Halo Padding**: 25 pixels white border around logo
- **Output Format**: PNG (RGB)

## Security Features

1. **URL Validation**: Checks for valid URL structure
2. **SSL Verification**: Validates HTTPS certificates
3. **Status Code Check**: Ensures URL is reachable (200 OK)
4. **User Warnings**: Alerts for:
   - HTTP (non-encrypted) URLs
   - Invalid/expired SSL certificates
   - Unreachable URLs
5. **User Consent**: Asks permission before creating QR codes for insecure URLs

## File Structure
```
qr_code_generator/
├── qr_generator.py      # Main script
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

## Troubleshooting

### Logo not appearing
- Ensure logo path is correct (remove quotes if copy-pasted from Windows)
- Logo file must be a valid image format (PNG, JPG, etc.)
- Check file permissions

### QR code unscannable
- Logo might be too large (reduce `logo_max_size` to `qr_width // 5`)
- Increase `box_size` for larger QR codes
- Ensure good contrast between QR code and background

### SSL Certificate Error
- URL may have invalid/expired SSL certificate
- Choose "yes" to proceed anyway (not recommended for production use)

## Customization

### Change QR Code Size
```python
box_size=15,  # Increase for larger QR codes (e.g., 20)
```

### Change Logo Size
```python
logo_max_size = qr_width // 5  # Smaller logo (was // 3)
```

### Change Output Location
```python
file_path = "C:\\your\\custom\\path\\qrcode.png"
```

### Change Halo Padding
```python
halo_padding = 20  # Smaller gap (was 25)
```

## License

MIT License - Feel free to use and modify!

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## Author

Youssef Abdelkawy
- GitHub: [@YoussefAbdelkawy](https://github.com/YoussefAbdelkawy)

## Acknowledgments

- [qrcode](https://github.com/lincolnloop/python-qrcode) - Python QR Code library
- [Pillow](https://python-pillow.org/) - Python Imaging Library
- [requests](https://requests.readthedocs.io/) - HTTP library

## Version History

- **v1.0.0** (2024-11-15)
  - Initial release
  - SSL validation
  - Custom logo support
  - High error correction
