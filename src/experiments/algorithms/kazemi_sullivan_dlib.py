from typing import Optional

import dlib
import numpy as np

from ..datasets.dataset import AnnotatedImage
from ..types import Landmarks


class LandmarkFitting:
    def __init__(self, predictor_path: str):
        self.predictor = dlib.shape_predictor(predictor_path)
        self.detector = dlib.get_frontal_face_detector()

    def fit(self, a_img: AnnotatedImage) -> Optional[Landmarks]:
        bbox = self.detector(a_img.image, 1)
        if len(bbox) > 0:
            # There should only be at most one face
            shape = self.predictor(a_img.image, bbox[0])
            return np.array([(p.x, p.y) for p in shape.parts()])
        return None
