import threading

import requests
import validators

user_agent: str = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"


class Scanner(threading.Thread):

    def __init__(self, url: str):
        super().__init__()

        # Check if the URL is valid.
        if validators.url(url):
            self.url = url

            # Create new session
            self.request_session = requests.Session()

            # Set user agent
            self.request_session.headers = {"User-Agent": user_agent}
        else:
            raise validators.ValidationFailure("Invalid URL %s " % url)

    """
    Returns True if the URL is injectable
    False if not
    """

    def scan(self) -> bool:
        try:
            request = requests.get(self.url + "'")  # Adds ' (single quote) for testing the sql injection

            content = request.text
            if request.status_code == 200:
                """
                ...
                
                All detection methods are below
                """
                if "you have an error" in content and "sql syntax" in content and "right syntax" in content:
                    return True

                if "Warning" in content and "to be resource" in content and "expects" in content and "parameter" in content:
                    return True

                return False
        except requests.ConnectTimeout as e:
            print("Connection Timeout: %s" % e)
        except requests.ConnectionError as e:
            print("Connection Error: %s" % e)
        except TypeError as e:
            print("Type Error: %s " % e)