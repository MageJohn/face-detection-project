import pathlib
from contextlib import ExitStack
from operator import attrgetter, indexOf, methodcaller
from typing import Optional

import click
from funcy import compact, compose, walk
from matplotlib import pyplot as plt
from matplotlib.backend_tools import ToolBase
from matplotlib.widgets import RadioButtons

from experiments.dataset import Dataset

plt.rcParams["toolbar"] = "toolmanager"


class SubsetMakerUi:
    def __init__(self, dataset: Dataset, subsets: list[pathlib.Path]):
        self.images = sorted(list(dataset), key=attrgetter("img_path"))
        self.subset_choices: list[Optional[int]] = [None] * len(self.images)
        self.cur_image = 0
        self.subsets = subsets

        self.fig = plt.figure()
        subset_axes, self.im_axes = self.fig.subplots(
            ncols=2, gridspec_kw={"width_ratios": (0.2, 0.8), "wspace": 0.02}
        )
        subset_axes.set_aspect("equal")
        self.im_axes.set_xticks([])
        self.im_axes.set_yticks([])

        self.subset_radios = RadioButtons(
            subset_axes, walk(attrgetter("stem"), self.subsets), 0
        )
        self.subset_radios.on_clicked(self.choose_subset)

        self.fig.canvas.manager.toolmanager.add_tool(
            "Prev",
            ControlTool,
            callback=self.prev_image,
            tooltip="Prev",
            image="back",
        )
        self.fig.canvas.manager.toolmanager.add_tool(
            "Next",
            ControlTool,
            callback=self.next_image,
            tooltip="Next",
            image="forward",
        )
        self.fig.canvas.manager.toolmanager.add_tool(
            "Save",
            ControlTool,
            callback=self.write_subsets,
            tooltip="Save the subsets",
            image="filesave",
        )
        self.fig.canvas.manager.toolbar.add_tool("Save", "my_controls")
        self.fig.canvas.manager.toolbar.add_tool("Prev", "my_controls")
        self.fig.canvas.manager.toolbar.add_tool("Next", "my_controls")
        self.fig.canvas.manager.toolmanager.remove_tool("save")
        self.fig.canvas.manager.toolmanager.remove_tool("forward")
        self.fig.canvas.manager.toolmanager.remove_tool("back")

    def run(self):
        self.update()
        plt.show()

    def choose_subset(self, subset_label):
        self.subset_choices[self.cur_image] = indexOf(
            map(methodcaller("get_text"), self.subset_radios.labels), subset_label
        )

    def next_image(self, _event=None):
        if self.cur_image < len(self.images) - 1:
            self.cur_image += 1
            self.update()

    def prev_image(self, _event=None):
        if self.cur_image > 0:
            self.cur_image -= 1
            self.update()

    def update(self):
        self.subset_radios.set_active(self.subset_choices[self.cur_image] or 0)

        self.im_axes.clear()
        self.im_axes.imshow(self.images[self.cur_image].image)
        self.fig.canvas.draw_idle()

    def write_subsets(self):
        for subset, contents in (
            (
                subset,
                (
                    f"{self.images[img_i].img_path.relative_to(subset.parent)}\n"
                    for img_i, choice in enumerate(self.subset_choices)
                    if choice == subs_i
                ),
            )
            for subs_i, subset in enumerate(self.subsets)
        ):
            with subset.open("w") as out:
                out.writelines(contents)


class ControlTool(ToolBase):
    def __init__(self, *args, callback, tooltip, image, **kwargs):
        self.description = tooltip
        self.my_callback = callback
        self.image = image
        super().__init__(*args, **kwargs)

    def trigger(self, *args, **kwargs):
        self.my_callback()


@click.command()
@click.option("-d", "--dataset-path", type=click.Path(path_type=pathlib.Path))
@click.argument("subsets", nargs=-1, type=click.Path(path_type=pathlib.Path))
def main(dataset_path: pathlib.Path, subsets: list[pathlib.Path]):
    dataset = Dataset(dataset_path)
    SubsetMakerUi(dataset, walk(methodcaller("resolve"), subsets)).run()


if __name__ == "__main__":
    main()
