from requests import post
from time import sleep
from json import loads

class TwoCaptcha:
    def __init__(self, captcha_key):
        self.captcha_key = captcha_key
        pass

    def create_task(self, **kwargs) -> str:
        if kwargs.get("gt") and kwargs.get("challenge"):
            task_payload = self.create_task_geetest(**kwargs)
        else:
            task_payload = self.create_task_recaptcha(**kwargs)
        task_request = post("http://2captcha.com/in.php", params=task_payload)
        if "OK" in task_request.text:
            return task_request.text.split("OK|")[1]
        raise Exception("Failed to create task")
    
    def create_task_geetest(
        self, 
        gt: str, 
        challenge: str,
        pageurl: str,
        api_server: str="api.geetest.com"
    ) -> str:
        return {
            'key' : self.captcha_key,
            'method' : 'geetest',
            "gt" : gt,
            "challenge": challenge,
            "api_server" : api_server,
            "pageurl" : pageurl
        }
    
    def create_task_recaptcha(
        self,
        pageurl: str,
        sitekey: str,
    ) -> str:
        return {
            'key' : self.captcha_key,
            'method' : 'userrecaptcha',
            "version" : "v2",
            "pageurl" : pageurl,
            "googlekey" : sitekey
        }

    def get_task_result(self, task_id: str) -> str:
        task_result_payload = {
            'key' : self.captcha_key,
            'action': 'get',
            'id': task_id
        }
        task_result_request = post("http://2captcha.com/res.php", params=task_result_payload)
        while "CAPCHA_NOT_READY" in task_result_request.text:
            sleep(5)
            task_result_request = post("http://2captcha.com/res.php", params=task_result_payload)
        if "OK" in task_result_request.text:
            return task_result_request.text.split("OK|")[1]
        raise Exception("Failed to get task result")
    
    def solve_captcha(self, **kwargs) -> str:
        task_id = self.create_task(**kwargs)
        res = self.get_task_result(task_id)
        if kwargs.get("gt") and kwargs.get("challenge"):
            res = loads(res)
        return res