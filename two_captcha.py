from requests import post
from time import sleep

class TwoCaptcha:
    def __init__(self, captcha_key):
        self.captcha_key = captcha_key
        pass

    def create_task(self) -> str:
        task_payload = {
            'key' : self.captcha_key,
            'method' : 'userrecaptcha',
            "version" : "v2",
            "pageurl" : "https://www.eticketing.co.uk/",
            "googlekey" : "6LeiYKwZAAAAAPtwKo56Ad4RqtR5eyBjfxlGGZqP",
        }
        
        task_request = post("http://2captcha.com/in.php", params=task_payload)

        if "OK" in task_request.text:
            return task_request.text.split("OK|")[1]
        raise Exception("Failed to create task")
    
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
    
    def solve_captcha(self) -> str:
        task_id = self.create_task()
        return self.get_task_result(task_id)