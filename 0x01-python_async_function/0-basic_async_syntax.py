#!/usr/bin/env python3
"""Module demonstrating basic async syntax"""
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """
    Asynch coroutine that waits for random delay between 0 and max_delay secs.

    Args:
        max_delay (int): The maximum number of seconds to wait. Defaults to 10.

    Returns:
        float: The actual number of seconds waited.
    """
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
