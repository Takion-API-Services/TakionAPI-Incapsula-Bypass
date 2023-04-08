from takion_api import TakionAPI
from two_captcha import TwoCaptcha
from costants import DEFAULT_HEADERS, WEB_IDENTITY_HEADERS, \
    QUEUE_HEADERS, ETICKETING_HEADERS

from json import dumps
from bs4 import BeautifulSoup
from tls_client import Session
from urllib.parse import unquote
from dotenv import load_dotenv
from os import getenv

load_dotenv()

def eticketing_login(
    session: Session, 
    solver: TakionAPI, 
    captcha: TwoCaptcha, 
    username: str, 
    password: str
) -> None:
    print("Proceeding to login...")
    initial_cookie = solver.solve_challenge("www.eticketing.co.uk", session)
    print("Solved incapsula challenge!")

    # Get login page
    url = "https://www.eticketing.co.uk/arsenal/Authentication/Login"
    res = session.get(url, headers=DEFAULT_HEADERS)

    # Solve captcha
    cookie = solver.solve_challenge("www.eticketing.co.uk", session)
    captcha_response = captcha.solve_captcha(
        pageurl="https://www.eticketing.co.uk/",
        sitekey="6LeiYKwZAAAAAPtwKo56Ad4RqtR5eyBjfxlGGZqP",
    )
    payload = dumps({
        "data": cookie,
        "payload": captcha_response,
        "provider": "recaptcha",
        "token": initial_cookie
    })
    response = session.post(
        solver.challenge_details['url'], 
        data=payload, 
        headers=solver.challenge_details['headers']
    )
    session.cookies.set("reese84", response.json()["token"])
    print("Solved incapsula captcha!")


    # Get login page again
    res = session.get(url, headers=DEFAULT_HEADERS)

    # Follow redirects
    redirect = BeautifulSoup(res.text, "html.parser").find("a").get("href").replace('&amp;', '&')
    res = session.get(redirect, headers=WEB_IDENTITY_HEADERS, data=payload)
    res = session.get(res.headers['Location'], headers=WEB_IDENTITY_HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')
    return_url = soup.find('input', {'id': 'ReturnUrl'})['value'].replace(' ', '+').replace("&amp;", "&")
    
    # Login post
    print("Proceeding to login...")
    url = "https://web-identity.tmtickets.co.uk/uk_arsenal/Account/Login"
    querystring = {"ReturnUrl":return_url}
    payload = {
        "ReturnUrl":return_url,
        "Username": username,
        "Password": password,
        "button": "login",
        "__RequestVerificationToken": soup.find('input', {'name': '__RequestVerificationToken'})['value']
    }
    headers = {
        "authority": "web-identity.tmtickets.co.uk",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "null",
        "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    res = session.post(url, headers=headers, params=querystring, data=payload)
    
    # Follow redirects
    res = session.get(f"https://web-identity.tmtickets.co.uk{res.headers['Location']}", headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    form = soup.find('form')
    url = form['action']
    payload = {i['name']: i['value'] for i in form.find_all('input')}
    res = session.post(url, headers=ETICKETING_HEADERS, data=payload)
    redirect = BeautifulSoup(res.text, "html.parser").find("a").get("href").replace('&amp;', '&')
    res = session.get(f"https://www.eticketing.co.uk{redirect}", headers=ETICKETING_HEADERS)
    res = session.get(res.headers['Location'], headers=QUEUE_HEADERS)
    href = unquote(res.text.split("decodeURIComponent('")[1].split("'")[0])
    url = f"https://ticketmastersportuk.queue-it.net{href}"
    res = session.get(url, headers=QUEUE_HEADERS)
    res = session.get(res.headers['Location'], headers=ETICKETING_HEADERS)
    res = session.get(res.headers['Location'], headers=ETICKETING_HEADERS)
    res = session.get(f"https://www.eticketing.co.uk{res.headers['Location']}", headers=ETICKETING_HEADERS)

    name = BeautifulSoup(res.text, "html.parser").find("span", {"class": "myaccount__user"}).text
    print(f"Logged in -> {name}")

if __name__ == "__main__":
    eticketing_login(
        Session(client_identifier="chome_110"),
        TakionAPI(getenv("TAKION_API_KEY")),
        TwoCaptcha(getenv("TWO_CAPTCHA_KEY")),
        getenv("ETICKETING_USERNAME"),
        getenv("ETICKETING_PASSWORD")
    )