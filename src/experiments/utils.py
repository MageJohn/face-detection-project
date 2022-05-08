from itertools import cycle
from math import sqrt
from typing import Iterable, Iterator, TypeVar

import numpy as np

from .types import Landmarks


def interocular(lmarks: Landmarks) -> float:
    """Calculate the distance between the outer points of the eye."""
    return sqrt(
        (lmarks[36, 0] - lmarks[45, 0]) ** 2 + (lmarks[36, 1] - lmarks[45, 1]) ** 2
    )


def rms_error_51(fitted: Landmarks, truth: Landmarks):
    return np.sqrt(np.square(fitted[17:] - truth[17:]).sum(axis=1)).sum() / (
        interocular(truth) * len(truth[17:])
    )


def rms_error(fitted: Landmarks, truth: Landmarks) -> float:
    """
    Calculate the root mean squared error between a set of fitted and ground truth landmarks.

    Follows the method used by Sagonas et al. (2016).
    """
    return np.sqrt(np.square(fitted - truth).sum(axis=1)).sum() / (
        interocular(truth) * len(truth)
    )


T = TypeVar("T")


def circle(iterable: Iterable[T]) -> Iterator[T]:
    it = iter(iterable)
    try:
        first = next(it)
    except StopIteration:
        return
    yield first
    for el in it:
        yield el
    yield first


def progress(iterable: Iterable[T], length: int) -> Iterator[T]:
    spinner = iter(cycle(["|", "/", "-", "\\"]))
    count = 0
    for el in iterable:
        count += 1
        print(f"\r{next(spinner)} {count}/{length}", end="")
        yield el
    print()
