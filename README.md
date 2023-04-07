# TakionAPI Incapsula Bypass
This repository showcases the power and versatility of the TakionAPI. It demonstrates how to bypass Incapsula's security restrictions on [eTicketing](https://www.eticketing.co.uk/arsenal/) platforms like Arsenal, as well as any other Incapsula-protected website. Additionally, it shows how to pass the reCAPTCHA challenge presented by Incapsula using the 2captcha service. The goal of this repo is to promote the TakionAPI service and provide an example implementation for clients.

[![Video of an example login](https://i.imgur.com/pjLkl1y.png)](https://youtu.be/EzET_mo7fV4 "Video of an example login")

**Note:** This is a simple example demonstrating the implementation of the APIs. There's no handling for bad responses or invalid credentials. If you plan to use this example for production purposes, it is recommended to enhance the implementation accordingly.

### Features
- TakionAPI bypasses Incapsula's security restrictions effortlessly
- Compatible with any Incapsula-protected website
- Passes reCAPTCHA challenges presented by Incapsula using 2captcha
- Secure and seamless access to eTicketing platforms

### Prerequisites
- Python 3.6 or higher

### Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/eTicketing-Login-Example.git
```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
3. Replace the following placeholders with your credentials:
```python
TAKION_API_KEY = "your_takion_api_key"
TWO_CAPTCHA_KEY = "your_2captcha_key"
USERNAME = "your_eticketing_username"
PASSWORD = "your_eticketing_password"
```

### Usage
Run the `main.py` script:
```bash
python main.py
```


### How It Works
The example implementation demonstrates the following process:
1. Use the Takion API to bypass Incapsula's AntiBot measures and access the website
2. Proceed with the login process
3. Utilize the Takion API along with a solved reCAPTCHA token (in this case, from 2captcha) to bypass Incapsula's captcha challenge
4. Finalize the login process and display the logged-in user's name

### Structure
The repository consists of the following main files:

- `main.py`: The main script that demonstrates the login process using the TakionAPI and TwoCaptcha.
- `takion_api.py`: Contains the TakionAPI class definition for bypassing Incapsula's security restrictions.
- `two_captcha.py`: A simple implementation of the 2captcha APIs.
- `constants.py`: Contains the headers used for the login process.

### Free Trial
To get a free trial of the Takion API service, visit [our Discord server](https://www.glizzykingdreko.live/incapsula).

### Disclaimer
The use of this repository and the TakionAPI is intended for educational purposes and responsible, legitimate use cases. The authors of the repository and the TakionAPI are not responsible for any misuse or damage caused by the use of this software.

### Contact
For any questions or inquiries, please contact us at [our mail](mailto:glizzykingdreko@protonmail.com) or [our Discord server](https://www.glizzykingdreko.live/incapsula).