# Paramount

`Paramount` is a Python project that allows you to control smart devices (like lights and sockets) using hand gestures. Devices are configured via the Tuya API, and hand gestures are recognized via MediaPipe and OpenCV.

### Installation

1. Clone the repository to your local machine.
2. Set up the environment and install dependencies using `pipenv`:

   ```bash
   pipenv shell
   pipenv install
   ```

3. Setup your account on the Tuya Developer Platform and add your devices. You can follow the instructions [here](./docs/Tuya.IoT.API.Setup.v2.pdf).
4. Set up the devices with `tinytuya` using the wizard:

   ```bash
   python -m tinytuya wizard
   ```

   Follow the instructions to configure your smart devices.

5. Save all the `json` files generated from the wizard (such as device configuration files) in the `./data` directory.

### Usage

After setting up the devices, you can use the system to control the smart devices with hand gestures.

1. To start the program:

   ```bash
   python main.py
   ```

2. **How it works**:
   - Devices are ordered according to their position in the `devices.json` file located in the `./data` directory.
   - Use hand gestures to control the devices:
     - Point with your fingers to form numbers ("1", "2", etc.) to switch devices on or off.
     - A full open palm turns all devices **on**.
     - A closed fist turns all devices **off**.
     - To confirm an action, make a thumbs-up gesture within **2 seconds**.

### Libraries Used

Here are the key libraries used in this project and their purposes:

- `requests`: For making HTTP requests, potentially used to interact with external APIs.
- `tinytuya`: A Python library to control Tuya-based smart devices (like lights, plugs, and more).
- `cryptography` and `pycryptodome`: For secure cryptographic functions, likely used for encryption and decryption of communication with smart devices.
- `pyaes`: For AES encryption, a specific form of encryption that could be needed by Tuya devices.
- `mediapipe`: Used to detect and recognize hand gestures using machine learning models.
- `opencv-python`: OpenCV is used for image and video processing, particularly for capturing and processing hand gestures through a camera.
- `python-dotenv`: Used to load environment variables from a `.env` file for securely storing sensitive information such as API keys and device credentials.

### Environment Setup

Make sure you are using Python version `3.12` as defined in the `Pipfile`:

```toml
[requires]
python_version = "3.12"
```

### License

MIT License
