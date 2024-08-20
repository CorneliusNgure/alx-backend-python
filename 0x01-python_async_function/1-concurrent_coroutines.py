#!/usr/bin/env python3
"""Executing multiple routines at the same time with asynch"""
import asyncio
from typing import List

wait_random = __import__("0-basic_async_syntax").wait_random


async def wait_n(n: int, max_delay: int) -> list[float]:
    """
    Asynch routine that spawns wait_random n times with specified max_delay.

    Args:
        n (int): The number of times to spawn wait_random.
        max_delay (int): The max delay passed to each wait_random invocation.

    Returns:
        list[float]: A list of delay times in ascending order.
    """
    coroutines = [wait_random(max_delay) for _ in range(n)]

    delays = await asyncio.gather(*coroutines)

    return sorted(delays)
