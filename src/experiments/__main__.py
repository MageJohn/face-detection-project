#!/usr/bin/python

from itertools import pairwise, starmap
from typing import Any, Callable, Iterable, List, Optional, Tuple

import dlib
import numpy as np
from nptyping import NDArray, Number, Shape

from .algorithms.algorithm import Algorithm
from .algorithms.kazemi_sullivan_dlib import LandmarkFitting as KSD
from .dataset import Dataset
from .types import Landmarks
from .utils import circle, progress, rms_error, rms_error_51


def render_landmarks(
    win, lmarks: Landmarks, color: Tuple[int, int, int] = (0, 255, 0)
) -> None:
    parts: List[Iterable] = [
        lmarks[0:17],  # boundary:
        lmarks[17:22],  # left eyebrow:
        lmarks[22:27],  # right eyebrow:
        lmarks[27:31],  # nose bridge:
        lmarks[31:36],  # nose base:
        circle(lmarks[36:42]),  # left eye:
        circle(lmarks[42:48]),  # right eye:
        circle(lmarks[48:60]),  # outer mouth:
        circle(lmarks[60:68]),  # inner mouth:
    ]
    dlib_point: Callable[[NDArray[Shape["2, 1"], Number]], Any] = (
        dlib.point if isinstance(lmarks.dtype, np.integer) else dlib.dpoint
    )
    for part in parts:
        win.add_overlay(
            list(starmap(dlib.line, pairwise(map(dlib_point, part)))),
            dlib.rgb_pixel(*color),
        )


def run_demo(algorithm: Algorithm, dataset: Dataset):
    win = dlib.image_window()
    for a_img in dataset:
        win.clear_overlay()
        win.set_image(a_img.image)
        render_landmarks(win, a_img.points, (255, 0, 0))

        fitted_points = algorithm.fit(a_img)
        if fitted_points is not None:
            error = rms_error(fitted_points, a_img.points)
            error_51 = rms_error_51(fitted_points, a_img.points)
            render_landmarks(win, fitted_points)
        else:
            error = float("inf")
            error_51 = float("inf")
        print(
            f"Fitted image {a_img.img_path}. RMS (68) = {error}, RMS (51) = {error_51}"
        )
        dlib.hit_enter_to_continue()


def run_experiment(algorithm: Algorithm, dataset: Dataset) -> List[Optional[Landmarks]]:
    return list(progress(map(algorithm.fit, dataset), len(dataset)))


def main() -> None:
    all_data = Dataset("../Datasets")
    algorithm = KSD(
        "../Implementations/Kazemi and Sullivan/shape_predictor_68_face_landmarks.dat"
    )
    run_experiment(algorithm, all_data.subdir("300w_cropped"))


if __name__ == "__main__":
    main()
