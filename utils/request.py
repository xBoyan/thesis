import copy

import requests
import time
import shutil
from functools import wraps

from logger import logger
from .exceptions import RequestMethodNotImplemented, ServerError
from .utils import get_checksum

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br"
}


def handler(max_retries=3):
    def wrap(func):
        @wraps(func)
        def request_wrapper(*args, **kwargs):
            exception, result = None, None

            for i in range(max_retries):
                try:
                    logger.debug(f"[{i}] Sending request with parameters: {kwargs}")

                    result = func(*args, **kwargs)

                    _status_code = result.status_code
                    _response = result.text

                except ServerError as e:
                    _status_code = e.status_code
                    _response = e.message
                    exception = e

                logger.debug(f"[{_status_code}] Received response from the server")
                logger.trace(f"------FULL RESPONSE------\n{kwargs}\n{_response}\n------END OF FULL RESPONSE------")

                if not isinstance(exception, ServerError):
                    return result

                delay = kwargs.get("delay", 2)
                time.sleep(delay * 5 if _status_code == 429 else delay)

            raise exception

        return request_wrapper

    return wrap


def download_image(save_path, download_url):
    """
    Downloads image from selected url and saves it under specified path
    :param save_path: absolute path where the image will be saved
    :type save_path: str
    :param download_url: image url
    :type download_url: str
    """
    logger.trace(f"Downloading image from {download_url} and saving it as {save_path}")

    response = requests.get(url=download_url, headers=DEFAULT_HEADERS, stream=True)

    with open(save_path, "wb") as file:
        shutil.copyfileobj(response.raw, file)


@handler(max_retries=3)
def send_request(method, url, **parameters):
    """
    Sends request on specified url
    :param method: request method e.g. GET, POST, PUT
    :type method: str
    :param url: url where request will be sent
    :type url: str
    :param parameters: additional params such as headers, proxies, timeout, etc.
    :type parameters: Any
    :return: request response
    :rtype: requests.Response
    :raises RequestMethodNotImplemented: when not implemented method is used
    :raises ServerError: when server doesn't return response with status code < 400
    """
    headers = parameters.get("headers", DEFAULT_HEADERS)

    if method == "GET":
        response = requests.get(url=url, headers=headers, **parameters)

    elif method == "POST":
        response = requests.post(url=url, headers=headers, **parameters)

    elif method == "PUT":
        response = requests.put(url=url, headers=headers, **parameters)

    else:
        raise RequestMethodNotImplemented(f"Specified {method} method is not implemented")

    if not response.ok:
        raise ServerError(status_code=response.status_code, message=response.text)

    return response
