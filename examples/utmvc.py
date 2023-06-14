'''
Example implementation of the solution on a protected website using ___utmvc, 
reese84 and WAF GeeTest challenge
'''
from takion_api import TakionAPI

from tls_client import Session
from resilenter_caller import update_session_proxy
from dotenv import load_dotenv
from os import getenv

load_dotenv()

# Define protected url and headers
protected_url = "https://premier.hkticketing.com"
headers = {
    "Host": "premier.hkticketing.com",
    "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="112", "Google Chrome";v="112"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
    "sec-fetch-dest": "document",
    "accept-language": "en-GB,en;q=0.9"
}


def is_incapsula_blocked(res) -> bool:
    return ('Request unsuccessful. Incapsula incident ID' in res.text or '_Incapsula_Resource' in res.text) and \
        (res.headers.get('Cache-Control') == 'no-cache, no-store' or res.headers.get('Connection') == 'close')


def send_request_with_solving(
    api_key: str = getenv("TAKION_API_KEY"),
    proxy: str = getenv("PROXY")
) -> None:
    '''
    Send request to protected url after solving the challenge
    '''
    # Create a new session
    session = Session(client_identifier="chrome_112")

    if not proxy or proxy == "":
        print("No proxy provided")
        return
    update_session_proxy(session, proxy)

    # If u want, you can select a specific browser/OS/chrome version to solve the challenge
    # just pass "Usear-Agent" and "sec-ch-ua" headers to the session
    # (not required)
    solving_browser = {
        "User-Agent": headers["user-agent"],
        "sec-ch-ua": headers["sec-ch-ua"]
    }

    incapsula_blocked = True
    while incapsula_blocked:
        print("Solving the challenge(s)...")
        response = TakionAPI(
            api_key=api_key,
        ).solve_challenges(
            url=protected_url,
            proxy=proxy,
            browser_details=solving_browser
        )
        if response.get("status") == "banned":
            print("Proxy banned")
            break
        if response.get("cookies"):
            for cookie in response["cookies"]:
                session.cookies.set(cookie["name"], cookie["value"])
        if response.get("solved_challenges"):
            for challenge in response["solved_challenges"]:
                print(f"Solved challenge: {challenge}")

        # Sending request to protected url 
        print("Sending request to protected url...")
        res = session.get(protected_url, headers=headers)
        incapsula_blocked = is_incapsula_blocked(res)
        print("Incapsula blocked the request" if incapsula_blocked else "Incapsula didn't block the request")


if __name__ == "__main__":
    send_request_with_solving()