import time
from openai import APITimeoutError


def call_openai_with_retry(func, retries=3, delay=2):
    # Executes an OpenAI call with retry logic on timeout.

    # :param func: A callable that performs the OpenAI request
    # :param retries: Number of retry attempts
    # :param delay: Delay (seconds) between retries

    for attempt in range(retries):
        try:
            return func()
        except APITimeoutError:
            if attempt == retries - 1:
                raise
            time.sleep(delay)  # wait before retry
