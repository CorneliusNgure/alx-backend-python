#!/usr/bin/env python3
""" Module that creates task for a function"""
import asyncio

wait_random = __import__("0-basic_async_syntax").wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """
    Schedules the wait_random coroutine.

    Args:
        max_delay (int): The maximum delay to pass to wait_random.

    Returns:
        asyncio.Task: Task object of the wait_random coroutine.
    """
    task = asyncio.create_task(wait_random(max_delay))

    return task
