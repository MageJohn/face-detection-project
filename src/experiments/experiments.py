#!/usr/bin/python
import numpy as np
from menpofit.aam import (AlternatingInverseCompositional, HolisticAAM,
                          LucasKanadeAAMFitter)

from .utils import progress


def train_aam(
    feature,
    trainset,
    reference_shape,
    label=None,
    batch_size=None,
    max_appearance_components=100,
    max_shape_components=15,
):
    if label is not None:
        print(f"Building {label} AAM")
    max_appearance_components = (
        max_appearance_components
        if batch_size is None or type(max_appearance_components) is int
        else None
    )
    return HolisticAAM(
        trainset,
        group="face_ibug_68_trimesh",
        reference_shape=reference_shape,
        batch_size=batch_size,
        diagonal=150,
        scales=1,
        holistic_features=feature,
        verbose=True,
        max_appearance_components=max_appearance_components,
        max_shape_components=max_shape_components,
    )


def build_fitter(aam):
    return LucasKanadeAAMFitter(
        aam,
        lk_algorithm_cls=AlternatingInverseCompositional,
    )


def run_test(fitter, testset, label="fitting"):
    return list(
        progress(
            (
                fitter.fit_from_bb(
                    testim,
                    testim.landmarks["PTS"].bounding_box(),
                    gt_shape=testim.landmarks["PTS"],
                    max_iters=50,
                )
                for testim in testset
            ),
            desc=f"Running {label} test",
            total=len(testset),
        )
    )


def process_results(results):
    errors = np.fromiter(
        (res.final_error() for res in results), float, count=len(results)
    )
    step = 1e-4
    sampling = np.arange(0, 1, step)
    cumm_err = np.zeros_like(sampling)
    for e in errors:
        if e < sampling[-1]:
            cumm_err[int(e // step) + 1] += 1
    cumm_err /= errors.size
    np.cumsum(cumm_err, out=cumm_err)

    return (sampling, cumm_err)
