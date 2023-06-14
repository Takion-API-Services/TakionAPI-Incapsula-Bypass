from typing import Dict, Union, Tuple
from resilient_caller import send_request, RETRY_EVENT
import logging, warnings
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made to host")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TakionAPI:
    def __init__(self, api_key: str) -> None:
        self.api_key, self.challenge_details = api_key, {}
        pass
    
    def handle_good_response(self, response: str, *_) -> Tuple[str, Dict[str, str], Dict[str, str]]:
        data = response.json()
        return data['url'], data['headers'], data['payload']
    
    def handle_good_general_response(self, response: str, *_) -> Tuple[str, Dict[str, str], Dict[str, str]]:
        return response.json()
    
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
            f"https://takionapi.tech/incapsula/sensor/{website}?api_key={self.api_key}",
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
    
    def solve_reese84(self, website: str, session: object, browser_details: Dict[str, str]={}) -> Union[str, bool]:
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
    
    def solve_challenges(self, url: str, proxy: str, browser_details: Dict[str, str]={}) -> Union[str, bool]:
        if browser_details.get("User-Agent") or browser_details.get("sec-ch-ua"):
            logger.debug("Using custom browser details")
        logger.debug(f"Generating challenge data for {url}")
        res = send_request(
            f"https://takionapi.tech/incapsula/all?api_key={self.api_key}",
            method="POST",
            json={
                "url": url,
                "proxy": proxy
            },
            conditions={
                "all": self.handle_good_general_response
            },
            retries=3,
            delay=3,
            verify=False,
            on_retry=lambda tries: logger.debug(f"Retrying solving ({tries})"),
            headers=browser_details,
            timeout=320
        )
        return res
        
    
    def solve_geetest(self, challenge: str, gt: str) -> dict:
        logger.debug(f"Solving geetest challenge: {challenge}")
        res = send_request(
            f"https://takionapi.tech/geetest?api_key={self.api_key}&challenge={challenge}&gt={gt}",
            method="GET",
            conditions={
                "all": self.handle_good_general_response
            },
            retries=3,
            delay=3,
            verify=False,
            on_retry=lambda tries: logger.debug(f"Retrying solving ({tries})"),
        )
        return res
