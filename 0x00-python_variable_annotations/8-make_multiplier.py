#!/usr/bin/env python3
"""Complex types - functions"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Function that accepts a function as an argument"""
    def mult(x: float) -> float:
        """Returns argument times multiplier"""
        return x * multiplier
    return mult
