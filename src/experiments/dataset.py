# Provides a way to define a dataset, including:
#   - splitting into manually curated categories
#   - pulling in files from multiple paths
#   - transparently handle different image file types
#   - easily match a given image to it's .pts file

from itertools import chain
from operator import attrgetter, methodcaller
from pathlib import Path
from typing import Any, Iterator, Optional, Set, Union

import numpy as np
import numpy.typing as npt
from funcy import compose, select
from PIL import Image

from .types import Landmarks

PathLike = Union[Path, str]


class AnnotatedImage:
    def __init__(self, img_path: Path):
        self.img_path = img_path
        self.pts_path = img_path.with_suffix(".pts")
        self._points: Optional[Landmarks] = None

    @property
    def name(self) -> str:
        return self.img_path.stem

    @property
    def image(self) -> npt.NDArray[Any]:
        """The image data associated with this annotated image."""
        return np.asarray(Image.open(self.img_path))

    @property
    def points(self) -> Landmarks:
        """The annotations associated with this annotated image."""
        if self._points is None:
            self._points = read_pts(self.pts_path)
        return self._points


class Dataset:
    def __init__(self, basepath: PathLike, set_: Optional[Set[AnnotatedImage]] = None):
        self.basepath = Path(basepath).resolve()
        if set_ is None:
            self._set = self._load()
        else:
            self._set = set_

    def _load(self) -> Set[AnnotatedImage]:
        return set(
            map(
                AnnotatedImage,
                chain(self.basepath.glob("**/*.png"), self.basepath.glob("**/*.jpg")),
            )
        )

    def subdir(self, path: PathLike):
        path = Path(path)
        subpath = self.basepath.joinpath(path)
        return Dataset(
            subpath,
            select(
                compose(
                    methodcaller("is_relative_to", subpath),
                    attrgetter("img_path"),
                ),
                self._set,
            ),
        )

    def subset_file(self, path: PathLike):
        """
        Load subset from a text file containing a list of images. The format is
        one path to an image file per line, relative to the location of the
        list file.
        """
        path = Path(path)
        with path.open() as list_file:
            members = set(
                map(
                    compose(
                        methodcaller("with_suffix", ""),
                        methodcaller("resolve"),
                        path.parent.joinpath,
                        methodcaller("strip"),
                    ),
                    list_file.readlines(),
                )
            )
        return Dataset(
            self.basepath,
            select(
                compose(
                    members,
                    methodcaller("with_suffix", ""),
                    attrgetter("img_path"),
                ),
                self._set,
            ),
        )

    def __iter__(self) -> Iterator[AnnotatedImage]:
        return self._set.__iter__()

    def __len__(self):
        return self._set.__len__()


def read_pts(path: Union[Path, str]) -> Landmarks:
    """Read a file containing landmarks into a Numpy NDArray"""
    with open(path) as file:
        lines = file.readlines()
    assert lines[0].split() == ["version:", "1"], "not a valid PTS file"
    assert lines[1].split() == ["n_points:", "68"], "expected 68 landmark points"
    assert lines[2].strip() == "{", "could not find start of points"
    assert lines[-1].strip() == "}", "could not find end of points"

    res: Landmarks = np.array(
        [[float(x), float(y)] for x, y in [l.split() for l in lines[3:-1]]]
    )
    assert len(res) == 68
    return res
