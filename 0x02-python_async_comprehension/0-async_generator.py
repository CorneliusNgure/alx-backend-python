#!/usr/bin/env python3
"""Async generator"""
from typing import AsyncGenerator
import asyncio
import random


async def async_generator() -> AsyncGenerator[float, None]:
    """
    Coroutine that loops 10 times asynchronously,
    yields a random number between 0 and 10.
    """
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
