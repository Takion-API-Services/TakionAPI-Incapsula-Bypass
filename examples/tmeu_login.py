'''
Example implementation of the solution on the protected 
TicketMaster EU login flow.
'''
from takion_api import TakionAPI
from examples.costants import DEFAULT_HEADERS, ESPF_HEADERS

from json import dumps
from tls_client import Session
from dotenv import load_dotenv
from os import getenv

load_dotenv()

def ticketmaster_test(
    session: Session, 
    solver: TakionAPI, 
    domain: str="ticketmaster.co.uk"
) -> None:
    # Define headers for ticketmaster
    DEFAULT_HEADERS['authority'] = f"www.{domain}"
    ESPF_HEADERS['authority'] = f"epsf.{domain}"
    ESPF_HEADERS['referer'] = f"https://www.{domain}/"
    ESPF_HEADERS['origin'] = f"https://{domain}"
    ESPF_HEADERS['requesting-host'] = domain

    
    # Trigger challenge
    print(f"({domain}) Forcing incapsula challenge...")
    session.cookies.set("reese84", "trigger_challenge")
    response = session.get(f"https://www.{domain}/", headers=DEFAULT_HEADERS)
    
    # Check response
    print(f"Response status code: {response.status_code}")
    if not (response.status_code == 403 and 'Get Your Identity Verified' in response.text): return
    
    # Solve challenge
    print("Challenge triggered, solving...")
    initial_cookie = solver.solve_reese84(domain, session)
    print("Solved incapsula challenge!")

    # Ticketmaster uses geetest, we need to load it from this url
    res = session.get(
        f"https://epsf.{domain}/vamigood", 
        headers=ESPF_HEADERS
    ).text

    # Parse challenge details
    gt = res.split('gt: "')[1].split('"')[0]
    challenge = res.split('challenge: "')[1].split('"')[0]
    print("Solving geetest challenge...")
    captcha_response = solver.solve_geetest(
        gt=gt,
        challenge=challenge
    )
    print("Solved geetest challenge!")
    gee_reese_parsed = res.split('solvedCaptcha({')[1].split('data: "')[1].split('"')[0]
    reese_parsed = res.split('protectionSubmitCaptcha("geetest", payload, timeoutMs,')[1].split('"')[1].split('"')[0]
    payload = dumps({
        "data": reese_parsed,
        "payload": {
            "geetest_challenge": challenge,
            "geetest_seccode": captcha_response['geetest_validate'],
            "geetest_validate": captcha_response['geetest_seccode'],
            "data": gee_reese_parsed
        },
        "provider":"geetest",
        "token" :initial_cookie
    })

    # Send challenge response
    response = session.post(
        solver.challenge_details['url'], 
        data=payload,
        headers=solver.challenge_details['headers']
    )
    print("Solved geetest challenge!")
    cookie = response.json()['token']
    session.cookies.set("reese84", cookie)

    # Get main page again
    response = session.get(f"https://www.{domain}/", headers=DEFAULT_HEADERS)
    print(f"({domain}) Response status code: {response.status_code}")

def tm_nl_login(
    session: Session, 
    username: str,
    password: str,
    domain: str="ticketmaster.nl",
) -> None:
    url = f"https://identity.{domain}/login"
    payload = {
        "username": username,
        "password": password,
    }
    headers = {
        "authority": f"identity.{domain}",
        "accept": "*/*",
        "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "origin": f"https://www.{domain}",
        "referer": f"https://www.{domain}/",
        "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    res = session.post(url, headers=headers, json=payload)
    if res.status_code == 200:
        print(f"Logged in as -> {res.json()['firstName']}")
    else:
        print(f"Login failed! -> {res.json()['error_description']}")

def tm_uk_login(
    session: Session, 
    solver: TakionAPI,
    username: str,
    password: str
) -> None:
    url = "https://identity.ticketmaster.co.uk/sign-in"
    querystring = {"doNotTrack":"false","integratorId":"prd1741.iccp","lang":"en-gb","placementId":"mytmlogin","redirectUri":"https://www.ticketmaster.co.uk/"}
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
    url = "https://auth.ticketmaster.com/json/sign-in"
    payload = {
        "email": username,
        "password":  password,
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
    takion_api_key = getenv("TAKION_API_KEY")
    session = Session(client_identifier="chome_110")
    solver = TakionAPI(takion_api_key)
    ticketmaster_test(
        session,
        solver,
        domain="ticketmaster.co.uk"
    )
    if getenv("TMUS_USERNAME") and getenv("TMUS_PASSWORD"):
        tm_uk_login(session, solver, getenv("TMUS_USERNAME"), getenv("TMUS_PASSWORD"))
    
    session = Session(client_identifier="chome_110")
    ticketmaster_test(
        session,
        TakionAPI(takion_api_key),
        domain="ticketmaster.nl"
    )
    if getenv("TMNL_USERNAME") and getenv("TMNL_PASSWORD"):
        tm_nl_login(session, getenv("TMNL_USERNAME"), getenv("TMNL_PASSWORD"))