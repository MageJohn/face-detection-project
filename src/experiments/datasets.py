from functools import reduce
from operator import add
from pathlib import Path
from typing import Iterable, Union

import menpo

from .utils import progress

PathLike = Union[str, Path]

DATASETS_PATH = Path(__file__).parent / ".." / ".." / "Datasets"

testsets: dict[str, Union[str, list[str]]] = {
    "lfpw": "lfpw/testset",
    "300w-indoor": "300w_cropped/01_Indoor",
    "300w-outdoor": "300w_cropped/02_Outdoor",
    "300w": ["300w_cropped/01_Indoor", "300w_cropped/02_Outdoor"],
    "helen": "helen/testset",
    "helen_train": "helen/trainset",
    "afw": "afw",
    "all": [
        "lfpw/testset",
        "300W/01_Indoor",
        "300W/02_Outdoor",
        "afw",
        "helen/testset",
        "helen/trainset",
    ],
}

trainsets = {""}


def process_image_import(image):
    # convert to grayscale
    if image.n_channels == 3:
        image = image.as_greyscale()

    # crop to landmarks with 20% padding
    img = image.crop_to_landmarks_proportion(0.2)

    # rescale image to diagonal 200
    img = img.rescale(200.0 / img.diagonal())

    menpo.landmark.labeller(
        img, "PTS", menpo.landmark.face_ibug_68_to_face_ibug_68_trimesh
    )

    return img


def import_assets(paths: Union[PathLike, Iterable[PathLike]]):
    if isinstance(paths, Path) or isinstance(paths, str):
        paths = [paths]
    label = ",".join((Path(p).stem for p in paths))
    lazylist = reduce(
        add, (menpo.io.import_images(DATASETS_PATH / p) for p in paths)
    ).map(process_image_import)
    return list(
        progress(lazylist, desc=f"Importing {label} assets", leave=False, unit="file")
    )


def import_trainset():
    return import_assets(["lfpw/trainset", "ibug"])


def import_testset(testset_id: str):
    return import_assets(testsets[testset_id])
