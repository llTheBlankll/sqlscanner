import threading

import requests
import validators

user_agent: str = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 " \
                  "Safari/537.36"


class Scanner(threading.Thread):

    def __init__(self, url: str):
        super().__init__()

        self.url = url

        # Create new session
        self.request_session = requests.Session()

        # Set user agent
        self.request_session.headers = {"User-Agent": user_agent}

        self.result: bool = False
    """
    Returns True if the URL is injectable
    False if not
    """

    def run(self):
        try:
            request = requests.get(self.url + "'", timeout=10)  # Adds ' (single quote) for testing the sql injection

            content = request.text
            if request.status_code == 200:
                """
                ...
                
                All detection methods are below
                """
                if "you have an error" in content and "sql syntax" in content and "right syntax" in content:
                    self.result = True

                if "Warning" in content and "to be resource" in content and "expects" in content and "parameter" in content:
                    self.result = True

                if self.result:
                    print(f"{self.url} is VULNERABLE")
                    self.result = False

                print(f"{self.url} is NOT VULNERABLE")
                self.result = False
        except requests.ConnectTimeout as e:
            print("Connection Timeout: %s" % e)
        except requests.ConnectionError as e:
            print("Connection Error: %s" % e)
        except TypeError as e:
            print("Type Error: %s " % e)
        except Exception as e:
            print(e)
            pass

    def join(self, **kwargs) -> tuple:
        threading.Thread.join(self)
        return self.url, self.result
