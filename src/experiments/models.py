from functools import partial

import menpo

models = {
    "raw": {
        "label": "Intensity values",
        "feature": menpo.feature.no_op,
        "train_kwargs": {},
    },
    "dsift": {
        "label": "DSIFT",
        "feature": menpo.feature.fast_dsift,
        "train_kwargs": {},
    },
    "daisy": {
        "label": "DAISY",
        "feature": partial(
            menpo.feature.daisy,
            radius=5,
            histograms=4,
            orientations=4,
        ),
        "train_kwargs": {"batch_size": 100},
    },
    "hog": {
        "label": "HOG",
        "feature": partial(
            menpo.feature.hog, mode="dense", num_bins=9, block_size=2, cell_size=8
        ),
        "train_kwargs": {"batch_size": 100},
    },
    "igo": {
        "label": "IGO",
        "feature": partial(menpo.feature.igo, double_angles=False),
        "train_kwargs": {},
    },
}
