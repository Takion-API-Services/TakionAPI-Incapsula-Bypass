# TakionAPI Incapsula Bypass
This repository showcases the power and versatility of the TakionAPI. It demonstrates how to bypass Incapsula's security restrictions on some Incapsula-protected website using `reese84` or `___utmvc` cookies.
Additionally, it shows how to pass the WAF `GeeTest` challenge presented by Incapsula our solving service [Ticketmaster](https://ticketmaster.co.uk/) websites. 
The goal of this repo is to promote the TakionAPI service and provide an example implementation for clients.

[![Video of an example login](https://i.imgur.com/pjLkl1y.png)](https://youtu.be/EzET_mo7fV4 "Video of an example login")

**Note:** This is a simple example demonstrating the implementation of the APIs. There's no handling for bad responses or invalid credentials. If you plan to use this example for production purposes, it is recommended to enhance the implementation accordingly.

### Features
- TakionAPI bypasses Incapsula's security restrictions effortlessly such as `reese84` and `___utmvc` cookies
- Compatible with any Incapsula-protected website
- Bypasses **Geetest** challenges on Ticketmaster websites using our API
- Secure and seamless access to Ticketmaster platforms and endoints

### Prerequisites
- Python 3.6 or higher

### Installation
1. Clone the repository:
```bash
git clone https://github.com/Takion-API-Services/TakionAPI-Incapsula-Bypass

```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
1. Add your credentials to the .env file:
```python
TAKION_API_KEY="your_takion_api_key" # Required

# Optional for examples/tmus_login.py (US) and examples/tmeu_login.py (UK)
TMUS_USERNAME="xxxxxxx@xxxxx.com"
TMUS_PASSWORD="xxxxxxx"

# Optional for examples/tmeu_login.py (NL)
TMNL_USERNAME="xxxxxxx@xxxxx.com"
TMNL_PASSWORD="xxxxxxx"

PROXY="" # Optional for ___utmvc cookie in examples/utmvc.py
```

### Usage
Change the `TAKION_API_KEY` in the `.env` file to your Takion API key. If you don't have one, you can get a free trial from [our Discord server](https://https://takionapi.tech/incapsula).

Change the directory to the examples folder:
```bash
cd examples
```

Run the `<script_name>.py` you want to test:
```bash
python protected_endpoint.py
```

### Structure
The repository consists of the following main files:

- `examples/constants.py`: Contains the headers used for the login process.
- `examples/protected_endpoint.py`: This script uses our apis to bypass the reese84 challenge in order to access a protected endpoint of Ticketmaster US.
- `examples/takion_api.py`: Contains the TakionAPI class definition for bypassing Incapsula's security restrictions using the TakionAPI.
- `examples/tmeu_login.py`: This script uses our apis to bypass the reese84 and WAF GeeTest challenges in order to login on Ticketmaster UK and NL.
- `examples/tmus_login.py`: This script uses our apis to bypass the reese84 in order to login on Ticketmaster US.
- `examples/utmvc.py`: This script uses our apis to bypass the **___utmvc** challenge in order to access a protected website. It will handle (if needed) the **reese84** challenge and the **WAF GeeTest** challenge, in order to access the website, you'll need to provide a proxy in the `.env` file.
- `.env`: A file where you should store your API keys and eTicketing credentials as environment variables.

### Free Trial
To get a free trial of the Takion API service, visit [our Discord server](https://takionapi.tech/incapsula).

### Conclusion
For more information and an example implementation of a simple Incapsula bypass without the need for captcha solving, please refer to the [official TakionAPI documentation](https://docs.takionapi.tech) or [our Discord server](https://https://takionapi.tech/incapsula).

### Disclaimer
The use of this repository and the TakionAPI is intended for educational purposes and responsible, legitimate use cases. The authors of the repository and the TakionAPI are not responsible for any misuse or damage caused by the use of this software.

### Contact
For any questions or inquiries, please contact us at [our mail](mailto:glizzykingdreko@protonmail.com) or [our Discord server](https://https://takionapi.tech/incapsula).
