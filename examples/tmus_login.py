'''
Example implementation of the solution on the protected 
TicketMaster US login flow.
'''
from takion_api import TakionAPI

from tls_client import Session
from dotenv import load_dotenv
from os import getenv

load_dotenv()

def ticketmaster_login(
    session: Session, 
    solver: TakionAPI,
    username: str, 
    password: str
) -> None:
    print("Proceeding to login...")
    url = "https://identity.ticketmaster.com/sign-in"
    querystring = {"integratorId":"prd1224.ccpDiscovery","placementId":"discovery","redirectUri":"https://www.ticketmaster.com/"}
    headers = {
        "authority": "identity.ticketmaster.co.uk",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
        "referer": "https://www.ticketmaster.co.uk/",
        "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-site",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    res = session.get(url, headers=headers, params=querystring)
    print("Solving challenge (auth.ticketmaster.com)...")
    solver.solve_reese84("auth.ticketmaster.com", session)
    redirect_url = res.headers['Location'].replace(" ", "%20")
    headers = {
        "authority": "auth.ticketmaster.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
        "referer": "https://www.ticketmaster.co.uk/",
        "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "cross-site",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    res = session.get(redirect_url, headers=headers)
    print("Submitting credentials...")
    url = "https://auth.ticketmaster.com/json/sign-in"
    payload = {
        "email": username,
        "password": password,
        "rememberMe": True,
        "resumePath": res.text.split('resumePath":"')[1].split('"')[0],
        "siteToken": res.text.split("siteToken: '")[1].split("'")[0],
        "pfVal": None,
        "paramsToken": res.text.split('paramsToken":"')[1].split('"')[0],
    }
    headers = {
        "authority": "auth.ticketmaster.com",
        "accept": "*/*",
        "accept-language": "en-gb",
        "content-type": "application/json",
        "origin": "https://auth.ticketmaster.com",
        "referer": "https://auth.ticketmaster.com/as/authorization.oauth2?client_id=35a8d3d0b1f1.web.ticketmaster.uk&response_type=code&scope=openid%20profile%20phone%20email%20tm&redirect_uri=https://identity.ticketmaster.co.uk/exchange&visualPresets=tmeu&lang=en-gb&placementId=mytmlogin&hideLeftPanel=false&integratorId=prd1741.iccp&intSiteToken=tm-uk&deviceId=1oqJw0NjMbW4t7O0vbe5uLi5urM6SRs6f6%2FZ1A&doNotTrack=false",
        "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "tm-client-id": "35a8d3d0b1f1.web.ticketmaster.uk",
        "tm-integrator-id": "prd1741.iccp",
        "tm-placement-id": "mytmlogin",
        "tm-site-token": "tm-uk",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    res = session.post(url, headers=headers, json=payload).json()
    if res.get("message"):
        print(f"Login failed: {res['message']}")
        return
    redirect_url = res['_links']['continueLink']['source']
    headers = {
        "authority": "identity.ticketmaster.co.uk",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
        "referer": "https://auth.ticketmaster.com/",
        "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "cross-site",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    res = session.get(redirect_url, headers=headers)
    redirect = res.headers.get("Location")
    res = session.get(redirect, headers=headers)
    url = f'https://my.ticketmaster.com/user-account/json/profile'
    res = session.get(url, headers=headers)
    print(f"Logged in: {res.json()['email']}")

if __name__ == "__main__":
    ticketmaster_login(
        Session(client_identifier="chome_110"),
        TakionAPI(getenv("TAKION_API_KEY")),
        getenv("TMUS_USERNAME"),
        getenv("TMUS_PASSWORD")
    )