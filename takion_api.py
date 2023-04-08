from typing import List, Dict, Any, Union, Optional, Tuple, TypeVar, Generic, Callable, Type, cast, overload
from requests import get, post, session
from resilient_caller import send_request, RETRY_EVENT
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
disable_warnings(InsecureRequestWarning)

class TakionAPI:
    def __init__(self, api_key: str) -> None:
        self.api_key, self.challenge_details = api_key, {}
        pass
    
    def handle_good_response(self, response: str, *_) -> Tuple[str, Dict[str, str], Dict[str, str]]:
        data = response.json()
        return data['url'], data['headers'], data['payload']
    
    def handle_response(self, response: str, *_) -> Union[Tuple[str, Dict[str, str], Dict[str, str]], RETRY_EVENT]:
        logger.debug(f"Got response: {response.status_code} / {response.json().get('message', 'No errors')}")
        if response.status_code == 200:
            return self.handle_good_response(response)
        logger.error(f"Failed to solve challenge: {response.status_code} / {response.json()['message']}")
        return RETRY_EVENT

    def gen_challenge_data(
        self, 
        website: str,
        browser_details: Dict[str, str]={}
    ) -> Union[Tuple[str, Dict[str, str], Dict[str, str]], Tuple[None, None, None]]:
        if browser_details.get("User-Agent") or browser_details.get("sec-ch-ua"):
            logger.debug("Using custom browser details")
        logger.debug(f"Generating challenge data for {website}")
        res = send_request(
            f"http://127.0.0.1:4777/incapsula/sensor/{website}?api_key={self.api_key}",
            method="GET",
            conditions={
                "all": self.handle_response
            },
            retries=3,
            delay=3,
            verify=False,
            on_retry=lambda tries: logger.debug(f"Retrying solving ({tries})"),
            headers=browser_details
        )
        return res
    
    def solve_challenge(self, website: str, session: object, browser_details: Dict[str, str]={}) -> Union[str, bool]:
        details = self.gen_challenge_data(website, browser_details)

        if details is None:
            logger.error("Failed to solve challenge")
            return False
        
        challenge_url, challenge_headers, challenge_payload = \
            details
        self.challenge_details = {
            "url": challenge_url,
            "headers": challenge_headers
        }

        # Send challenge
        response = session.post(challenge_url, headers=challenge_headers, data=challenge_payload).json()
        reese = response["token"]

        # Set cookie
        session.cookies.set("reese84", reese)
        return reese
