#!/usr/bin/env python3
""" Module for first element that's unknown """
from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Function documentation"""
    if lst:
        return lst[0]
    else:
        return None
