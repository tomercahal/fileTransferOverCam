# File Transfer Over Camera

A Python application that enables secure file transfer between devices using QR codes and camera capture.

## Features

- 📁 **Any File Type**: Transfer any file (text, images, documents, etc.)
- 📱 **QR Code Protocol**: Chunked file transfer using QR codes
- 📹 **Camera Integration**: Uses device camera for QR code scanning
- ✅ **Automatic Acknowledgment**: Built-in approval system for reliable transfer
- 🔄 **Automated Flow**: No manual intervention required during transfer
- 🎯 **Progress Tracking**: Real-time transfer progress indicators

## Installation

```bash
# Clone or download the project
git clone https://github.com/tomercahal/fileTransferOverCam.git
cd fileTransferOverCam

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py receiver  # On receiving device
python main.py sender    # On sending device
```

## Requirements

- **Python 3.8+**
- **Camera/Webcam** on both devices
- **Dependencies** (auto-installed):
  - `qrcode[pil]` - QR code generation
  - `opencv-python` - Camera capture and QR detection
  - `Pillow` - Image processing
  - `tkinter` - GUI (included with Python)

## Usage

### Quick Start

1. **On Receiving Device:**
   ```bash
   python main.py receiver
   ```
   - Application opens and waits for transfer
   - Point camera at sender's QR codes

2. **On Sending Device:**
   ```bash
   python main.py sender
   ```
   - Select file to transfer
   - QR codes are displayed automatically
   - Point receiver's camera at the QR codes

### Transfer Process

1. Sender displays QR code with file metadata
2. Receiver scans and shows approval QR
3. Sender detects approval and shows first data chunk
4. Process repeats until all chunks transferred
5. File automatically saved on receiver

## File Structure

```
file-transfer-over-cam/
├── main.py              # Entry point - choose sender/receiver mode
├── sender.py            # Sender functionality - file selection & QR display
├── reciver.py           # Receiver functionality - scanning & file reconstruction
├── camera_handler.py    # Camera operations - capture & QR detection
├── protocol_utils.py    # Protocol logic - chunking, serialization, validation
├── requirements.txt     # Python dependencies
├── setup.py            # Package configuration
└── README.md           # This file
```

## Protocol Details

- **Chunking**: Large files split into manageable chunks (100 bytes default)
- **Encoding**: JSON payloads with base64-encoded binary data
- **Acknowledgment**: Each chunk requires approval before proceeding
- **Error Handling**: Duplicate chunk detection and invalid data filtering

## Troubleshooting

### Camera Issues
- Ensure camera permissions are granted
- Check if camera is being used by another application
- Try different camera indices if multiple cameras available

### QR Code Detection
- Ensure good lighting conditions
- Hold camera steady and at appropriate distance
- Clean camera lens if blurry

### Installation Issues
```bash
# If dependencies fail to install, try:
pip install --user -r requirements.txt

# Or reinstall:
pip install --force-reinstall -r requirements.txt

# Check Python version (requires 3.8+):
python --version
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## Author

Created for Computer Networks Workshop Final Project.