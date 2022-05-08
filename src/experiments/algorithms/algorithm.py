from typing import Optional, Protocol

from ..datasets import AnnotatedImage
from ..types import Landmarks


class Algorithm(Protocol):
    def fit(self, an_img: AnnotatedImage) -> Optional[Landmarks]:
        ...
