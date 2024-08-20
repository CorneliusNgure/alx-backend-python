#!/usr/bin/env python3
"""Executing multiple routines at the same time with asynch"""
import asyncio
from typing import List

task_wait_random = __import__("3-tasks").task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    Asynch routine that spawns wait_random n times with specified max_delay.

    Args:
        n (int): The number of times to spawn wait_random.
        max_delay (int): The max delay passed to each wait_random invocation.

    Returns:
        list[float]: A list of delay times in ascending order.
    """
    tasks = [task_wait_random(max_delay) for _ in range(n)]

    delays = [await task for task in asyncio.as_completed(tasks)]

    return sorted(delays)
