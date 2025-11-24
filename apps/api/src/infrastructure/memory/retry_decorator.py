"""Retry decorator utility."""

import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any

logger = logging.getLogger(__name__)


def retry_on_error(max_retries: int = 3, initial_delay: int = 1, backoff_factor: int = 2) -> Callable:
    """Decorator that retries on error."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
            retries = 0
            delay = initial_delay
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries > max_retries:
                        logger.error(f"Maximum retry count ({max_retries}) reached: {str(e)}")
                        raise
                    logger.warning(f"Operation failed, retrying in {delay} seconds ({retries}/{max_retries}): {str(e)}")
                    time.sleep(delay)
                    delay *= backoff_factor

        return wrapper

    return decorator
