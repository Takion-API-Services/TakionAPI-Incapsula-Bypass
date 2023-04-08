
from takion_api import TakionAPI
from two_captcha import TwoCaptcha
from costants import DEFAULT_HEADERS, ESPF_HEADERS

from json import dumps
from tls_client import Session
from dotenv import load_dotenv
from os import getenv

load_dotenv()

def ticketmaster_test(
    session: Session, 
    solver: TakionAPI, 
    captcha: TwoCaptcha,
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
    initial_cookie = solver.solve_challenge(domain, session)
    print("Solved incapsula challenge!")

    # Ticketmaster uses geetest, we need to load it from this url
    res = session.get(
        f"https://epsf.{domain}/vamigood", 
        headers=ESPF_HEADERS
    ).text

    # Parse challenge details
    gt = res.split('gt: "')[1].split('"')[0]
    challenge = res.split('challenge: "')[1].split('"')[0]
    captcha_response = captcha.solve_captcha(
        pageurl=f"https://www.{domain}/",
        gt=gt,
        challenge=challenge
    )
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
    
if __name__ == "__main__":
    takion_api_key = getenv("TAKION_API_KEY")
    two_captcha_key = getenv("TWO_CAPTCHA_KEY")
    ticketmaster_test(
        Session(client_identifier="chome_110"),
        TakionAPI(takion_api_key),
        TwoCaptcha(two_captcha_key),
        domain="ticketmaster.co.uk"
    )
    ticketmaster_test(
        Session(client_identifier="chome_110"),
        TakionAPI(takion_api_key),
        TwoCaptcha(two_captcha_key),
        domain="ticketmaster.nl"
    )
    # Please note that 2Captcha takes a lot
    # of time to solving geetest challenges!