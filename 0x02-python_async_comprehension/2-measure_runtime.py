#!/usr/bin/env python3
"""Measures the runtime for 4 parrallel comprehensions"""

import asyncio
import time
from typing import List

async_comprehension = __import__("1-async_comprehension").async_comprehension


async def measure_runtime() -> float:
    """
    Coroutine that measures the total runtime of
     executing async_comprehension four times in parallel.

    Returns:
        float: Total runtime in seconds.
    """
    start_time = time.perf_counter()

    await asyncio.gather(*(async_comprehension() for _ in range(4)))

    end_time = time.perf_counter()

    return end_time - start_time
