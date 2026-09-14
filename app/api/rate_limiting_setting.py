import os
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    enabled=os.getenv('TESTING', "false").lower() != 'true' # We want the limiter to be ignored while testing
)