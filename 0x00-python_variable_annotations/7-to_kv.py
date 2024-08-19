#!/usr/bin/env python3
"""Module for complex types - sting and int/float to tuple"""
from typing import Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """Complex types - string and int/float to tuple"""
    return (k, v**2)
