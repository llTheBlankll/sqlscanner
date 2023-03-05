import threading

import requests
import validators
import colorama
import termcolor

user_agent: str = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 " \
                  "Safari/537.36"

colorama.init()


class Scanner(threading.Thread):

    def __init__(self, url: str, timeout=30):
        super().__init__()

        self.url = url
        self.result = False
        self.timeout: int = timeout

        if validators.url(url.strip()):
            # Create new session
            self.request_session = requests.Session()

            # Set user agent
            self.request_session.headers = {"User-Agent": user_agent}
        else:
            return

    """
    Returns True if the URL is injectable
    False if not
    """

    def run(self):
        try:
            # Adds ' (single quote) for testing the sql injection
            request = requests.get(self.url + "'", timeout=self.timeout)

            content = request.text
            if request.status_code == 200:
                """
                ...
                
                All detection methods are below
                """
                if "you have an error" in content and "sql syntax" in content and "right syntax" in content:
                    self.result = True
                    return

                if "Warning" in content and "to be resource" in content and "expects" in content and "parameter" in content:
                    self.result = True
                    return

                if self.result:
                    print(f"[{termcolor.colored('+', color='green')}] {self.url}")
                    self.result = True
                    return

                print(f"[{termcolor.colored('-', color='red')}] {self.url}")
        except requests.ConnectTimeout as e:
            pass
        except requests.ConnectionError as e:
            pass
        except TypeError as e:
            pass

    def join(self, **kwargs) -> tuple:
        threading.Thread.join(self)
        return self.url, self.result
