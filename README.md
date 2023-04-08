# TakionAPI Incapsula Bypass
This repository showcases the power and versatility of the TakionAPI. It demonstrates how to bypass Incapsula's security restrictions on [eTicketing](https://www.eticketing.co.uk/arsenal/) platforms like Arsenal, as well as any other Incapsula-protected website. Additionally, it shows how to pass the reCAPTCHA challenge presented by Incapsula using the 2captcha service and how to bypass the Geetest challenge on [Ticketmaster](https://ticketmaster.co.uk/) websites. The goal of this repo is to promote the TakionAPI service and provide an example implementation for clients.

[![Video of an example login](https://i.imgur.com/pjLkl1y.png)](https://youtu.be/EzET_mo7fV4 "Video of an example login")

**Note:** This is a simple example demonstrating the implementation of the APIs. There's no handling for bad responses or invalid credentials. If you plan to use this example for production purposes, it is recommended to enhance the implementation accordingly.

### Features
- TakionAPI bypasses Incapsula's security restrictions effortlessly
- Compatible with any Incapsula-protected website
- Passes reCAPTCHA challenges presented by Incapsula using 2captcha
- Bypasses Geetest challenges on Ticketmaster websites
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
1. Add your credentials to the .env file:
```python
TAKION_API_KEY="your_takion_api_key"
TWO_CAPTCHA_KEY="your_2captcha_key"
ETICKETING_USERNAME="your_eticketing_username"
ETICKETING_PASSWORD="your_eticketing_password"
```

### Usage
Run the `eticketing.py` script to test the Incapsula + reCAPTCHA challenge:
```bash
python eticketing.py
```
Run the `ticketmaster.py` script to test the Incapsula + Geetest challenge on Ticketmaster websites:
```bash
python eticketing.py
```


### How It Works
The example implementation demonstrates the following processes:

1. `eticketing.py`: Bypasses Incapsula's AntiBot measures and reCAPTCHA challenges on the eTicketing platform.
   - Use the Takion API to bypass Incapsula's security restrictions and access the website
   - Proceed with the login process
   - Utilize the Takion API along with a solved reCAPTCHA token (in this case, from 2captcha) to bypass Incapsula's captcha challenge
   - Finalize the login process and display the logged-in user's name

2. `ticketmaster.py`: Bypasses Incapsula's AntiBot measures and Geetest challenges on Ticketmaster websites (ticketmaster.co.uk and ticketmaster.nl).
   - Force the Geetest challenge to show up
   - Use the Takion API to bypass Incapsula's security restrictions
   - Solve the Geetest challenge using 2captcha

### Structure
The repository consists of the following main files:

- `eticketing.py`: The script that demonstrates the login process on the eTicketing platform using the TakionAPI and TwoCaptcha.
- `ticketmaster.py`: The script that tests the  Geetest challenge on ticketmaster.co.uk and ticketmaster.nl using the TakionAPI and TwoCaptcha.
- `takion_api.py`: Contains the TakionAPI class definition for bypassing Incapsula's security restrictions.
- `two_captcha.py`: A simple implementation of the 2captcha APIs.
- `constants.py`: Contains the headers used for the login process.
- `.env`: A file where you should store your API keys and eTicketing credentials as environment variables.

### Free Trial
To get a free trial of the Takion API service, visit [our Discord server](https://www.glizzykingdreko.live/incapsula).

### Conclusion
This repository showcases the power and versatility of the TakionAPI in bypassing Incapsula's security restrictions in addition to reCAPTCHA and Geetest challenges. For more information and an example implementation of a simple Incapsula bypass without the need for captcha solving, please refer to the [official TakionAPI documentation](https://docs.glizzykingdreko.live).

### Disclaimer
The use of this repository and the TakionAPI is intended for educational purposes and responsible, legitimate use cases. The authors of the repository and the TakionAPI are not responsible for any misuse or damage caused by the use of this software.

### Contact
For any questions or inquiries, please contact us at [our mail](mailto:glizzykingdreko@protonmail.com) or [our Discord server](https://www.glizzykingdreko.live/incapsula).
