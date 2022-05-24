#!/usr/bin/python
import menpo.landmark
import numpy as np
from menpofit.aam import (AlternatingInverseCompositional, HolisticAAM,
                          LucasKanadeAAMFitter)
from menpofit.builder import compute_reference_shape
from menpofit.error import euclidean_bb_normalised_error
from menpofit.result import Result

from .utils import progress


def train_aam(
    feature,
    trainset,
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
    reference_shape = (
        compute_reference_shape(
            [im.landmarks["face_ibug_68_trimesh"] for im in trainset], None
        )
        if batch_size is not None
        else None
    )

    return HolisticAAM(
        trainset,
        group="face_ibug_68_trimesh",
        reference_shape=reference_shape,
        batch_size=batch_size,
        scales=1,
        holistic_features=feature,
        verbose=True,
        max_appearance_components=max_appearance_components,
        max_shape_components=max_shape_components,
    )


def build_fitter(aam, n_appearance=None, n_shape=None):
    return LucasKanadeAAMFitter(
        aam,
        lk_algorithm_cls=AlternatingInverseCompositional,
        n_appearance=n_appearance,
        n_shape=n_shape,
    )


def run_test(fitter, testset, label="fitting"):
    return list(
        progress(
            (
                fitter.fit_from_bb(
                    testim,
                    testim.landmarks["PTS"].bounding_box(),
                    gt_shape=testim.landmarks["PTS"],
                    max_iters=250,
                )
                for testim in testset
            ),
            desc=f"Running {label} test",
            total=len(testset),
        )
    )


def extract_errors(results, compute_error=euclidean_bb_normalised_error):
    return np.fromiter(
        (res.final_error(compute_error) for res in results), float, count=len(results)
    )


def process_results(results, compute_error=euclidean_bb_normalised_error):
    errors = extract_errors(results, compute_error)
    step = 1e-4
    sampling = np.arange(0, 1, step)
    cumm_err = np.zeros_like(sampling)
    for e in errors:
        if e < sampling[-1]:
            cumm_err[int(e // step) + 1] += 1
    cumm_err /= errors.size
    np.cumsum(cumm_err, out=cumm_err)

    return (sampling, cumm_err)


def result_to_lmark_subset(result, subset):
    subset_func = getattr(menpo.landmark, f"face_ibug_68_to_face_ibug_{subset}")
    return [
        Result(
            subset_func(res.final_shape),
            image=res.image,
            initial_shape=subset_func(res.initial_shape),
            gt_shape=subset_func(res.gt_shape),
        )
        for res in result
    ]
