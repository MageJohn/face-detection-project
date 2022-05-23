from pathlib import Path

import menpo

from .utils import progress

DATASETS_PATH = Path(__file__).parent / ".." / ".." / "Datasets"

testsets = {
    "lfpw": "lfpw/testset",
    "300w_indoor": "300W/01_Indoor",
    "300w_outdoor": "300W/02_Outdoor",
}


def process_image_import(image):
    # convert to grayscale
    if image.n_channels == 3:
        image = image.as_greyscale()

    # crop to landmarks with 20% padding
    img = image.crop_to_landmarks_proportion(0.2)

    # rescale image if its diagonal is bigger than 400 pixels
    if img.diagonal() > 400:
        img = img.rescale(400.0 / img.diagonal())

    menpo.landmark.labeller(
        img, "PTS", menpo.landmark.face_ibug_68_to_face_ibug_68_trimesh
    )

    return img


def import_assets(path, label=None):
    label = "" if label is None else label + " "
    return list(
        progress(
            menpo.io.import_images(path).map(process_image_import),
            desc=f"Importing {label}assets",
            leave=False,
        )
    )


def import_trainset():
    return import_assets(
        DATASETS_PATH / "lfpw" / "trainset", "lfpw training"
    ) + import_assets(DATASETS_PATH / "ibug", "ibug training")


def import_testset(testset_id: str):
    return import_assets(DATASETS_PATH / testsets[testset_id], "testing")
