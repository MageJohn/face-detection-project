from itertools import zip_longest
from sys import exit

import click

from .datasets import import_testset, import_trainset
from .io import ModelManager, ResultsManager
from .models import models


@click.group
def cli():
    ...


@cli.command()
def list_models():

    print(f"{'id':<8} label")
    print(f"{'':-<8} {'':-<8}")
    for id, spec in models.items():
        print(f"{id:<8} {spec['label']}")


@cli.command()
@click.option(
    "-i",
    "--id",
    "ids",
    multiple=True,
    help="id of the model to build. if unspecified, all models are built.",
)
@click.option(
    "-r",
    "--rebuild/--no-rebuild",
    help="if specified, rebuild and overwrite any exisiting models",
)
def build_model(ids, rebuild):
    """
    Build a model and store it for later use.
    """
    from menpofit.builder import compute_reference_shape

    from .experiments import train_aam

    if len(ids) == 0:
        to_build = list(models.keys())
    else:
        to_build = [id for id in ids if id in models]

    model_manager = ModelManager()

    if not rebuild:
        for id in to_build.copy():
            if model_manager.model_exists(id):
                print(f"Model {id} already exists. Skipping.")
                to_build.remove(id)

    if len(to_build) == 0:
        print("No models to build. Exiting.")
        exit(0)

    trainset = import_trainset()
    reference_shape = compute_reference_shape(
        [im.landmarks["face_ibug_68_trimesh"] for im in trainset],
        diagonal=150,
    )

    for id in to_build:
        kwargs = models[id]["train_kwargs"]
        kwargs["label"] = models[id]["label"]
        trained = train_aam(
            models[id]["feature"],
            trainset,
            reference_shape,
            **kwargs,
        )
        model_manager.save_model(id, trained)


@cli.command()
@click.option(
    "-i",
    "--id",
    "ids",
    multiple=True,
    help="id of the model to test. Can be specified multiple times. If unspecified, defaults to all models.",
)
@click.option(
    "-t", "--testset", "testset_id", help="testset id to use", default="300w_indoor"
)
@click.option(
    "-r",
    "--rerun/--no-rerun",
    help="Whether or not to re-run a test and overwrite results.",
)
def run_tests(ids, testset_id, rerun):
    from .experiments import build_fitter, run_test

    to_test = (
        list(models.keys()) if len(ids) == 0 else [id for id in models if id in ids]
    )
    model_mgr = ModelManager()
    results_mgr = ResultsManager()

    for id in to_test.copy():
        if not model_mgr.model_exists(id):
            print(f"Model {id} has not been built. Skipping")
            to_test.remove(id)

    if not rerun:
        for id in to_test.copy():
            if results_mgr.results_exist(id, testset_id):
                print(
                    f"Results for model {id} and testset {testset_id} already exist. Skipping."
                )
                to_test.remove(id)

    if len(to_test) == 0:
        print("No models to test. Exiting.")
        exit(0)

    testset = import_testset(testset_id)

    for id in to_test:
        model = model_mgr.load_model(id)
        fitter = build_fitter(model)
        results = run_test(fitter, testset, label=models[id]["label"])
        results_mgr.save_results(results, id, testset_id)


@cli.command()
def list_results():
    """List the results that have been previously computed and saved."""
    results_mgr = ResultsManager()
    print("\n".join(results_mgr.results_list()))


@cli.command()
@click.argument(
    "result_names",
    nargs=-1,
)
@click.option(
    "-l",
    "--label",
    "labels",
    multiple=True,
    help="""Label a result. 

    Can be used multiple times. Results and labels are paired up by index, so
    the nth result name is paired with the nth use of this flag.
    """,
)
def plot_results(result_names, labels):
    """Plot the results with names RESULT_NAMES. If non are specified, defaults to all.

    For valid options for RESULT_NAMES, see the output of the list-results command.
    """
    result_mgr = ResultsManager()

    existing_results = result_mgr.results_list()

    if len(result_names) == 0:
        result_names = existing_results.copy()
    else:
        for name in result_names:
            if name not in existing_results:
                print(f"No result with name '{name}'. Skipping")
                result_names.remove(name)

    if len(result_names) == 0:
        print("No results to plot. Exiting.")
        exit(0)

    import matplotlib.pyplot as plt

    from .experiments import process_results

    for label, name in zip_longest(labels, result_names):
        if name is None:
            break
        result = result_mgr.load_results(name)
        label = name if label is None else label
        plt.plot(*process_results(result), label=label)
    plt.legend()
    plt.show()
