#!/usr/bin/env python3
"""Module for measuring runtime"""
import time
import asyncio

wait_n = __import__("1-concurrent_coroutines").wait_n


async def measure_time(n: int, max_delay: int) -> float:
    """
    Measure the total execution time for wait_n function.

    Args:
        n (int): The number of coroutines to spawn.
        max_delay (int): The maximum delay for each coroutine.

    Returns:
        float: The average time per coroutine.
    """
    start_time = time.perf_counter()

    asyncio.run(wait_n(n, max_delay))

    end_time = time.perf_counter()

    total_time = end_time - start_time

    return total_time / n
