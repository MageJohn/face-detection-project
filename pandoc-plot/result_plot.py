import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import experiments as exp

mpl.rcParams["axes.titley"] = -0.18


def result_plot(testset_id: str, xlim: tuple[float, float] = (0, 0.05), ax=None):
    if ax is None:
        ax = plt.gca()

    resmgr = exp.ResultsManager()
    for model_id in exp.models:
        results = resmgr.load_results(model_id, testset_id)
        sampling, cumm_err = exp.process_results(results)
        ax.plot(sampling, cumm_err, label=exp.models[model_id]["label"])

    xsize = abs(xlim[0] - xlim[1])
    xpad = xsize * 0.05
    xstep = xsize / 5
    ax.set_xlim(xlim[0] - xpad, xlim[1] + xpad)
    ax.set_xticks(np.arange(xlim[0], xlim[1] + xstep, step=xstep))

    ax.set_yticks(np.arange(0, 1.1, step=0.1))
