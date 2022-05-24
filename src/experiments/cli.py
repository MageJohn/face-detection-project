import csv
from sys import exit
from typing import Optional

import click

from .datasets import import_testset, import_trainset, testsets
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

    for id in to_build:
        kwargs = models[id]["train_kwargs"]
        kwargs["label"] = models[id]["label"]
        trained = train_aam(
            models[id]["feature"],
            trainset,
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
    print("\n".join(map(", ".join, results_mgr.results_list())))


@cli.command()
@click.option(
    "-t",
    "--testset",
    "testset_id",
    help="Testset id for which to plot results",
    required=True,
)
@click.option(
    "-m",
    "--model",
    "model_ids",
    help="Model id for which to plot results. "
    "Can be specified multiple times. "
    "If unspecified, defaults to all models",
    multiple=True,
)
@click.option(
    "--point-subset", type=click.Choice(("49", "51", "65", "66", "68")), default=None
)
def plot_results(model_ids: list[str], testset_id: str, point_subset: Optional[str]):
    """Plot the results with names RESULT_NAMES. If non are specified, defaults to all.

    For valid options for RESULT_NAMES, see the output of the list-results command.
    """
    if point_subset == "68":
        point_subset = None
    result_mgr = ResultsManager()

    existing_results = result_mgr.results_list()
    if len(model_ids) == 0:
        mid_set = set(models.keys())
    else:
        mid_set = set(model_ids)

    result_names = [
        res for res in existing_results if res[0] in mid_set and res[1] == testset_id
    ]

    if len(result_names) == 0:
        print("No results to plot. Exiting.")
        exit(0)

    import matplotlib.pyplot as plt

    from .experiments import process_results, result_to_lmark_subset

    for mid, tid in result_names:
        result = result_mgr.load_results(mid, tid)
        if point_subset is not None:
            result = result_to_lmark_subset(result, point_subset)
        label = models[mid]["label"]
        plt.plot(*process_results(result), label=label)
    plt.legend()
    plt.show()


@cli.command()
@click.option(
    "-t",
    "--testset",
    "testset_ids",
    help="Testset id for which results will be used",
    multiple=True,
)
@click.option(
    "-m",
    "--model",
    "model_ids",
    help="Model id for which results will be used. "
    "Can be specified multiple times. "
    "If unspecified, defaults to all models.",
    multiple=True,
)
@click.option(
    "--point-subset", type=click.Choice(("49", "51", "65", "66", "68")), default=None
)
@click.argument("output", type=click.File("w"), default="-")
def stats_table(
    model_ids: list[str], testset_ids: list[str], point_subset: Optional[str], output
):
    """Produce a CSV table from the results.

    For valid options for RESULT_NAMES, see the output of the list-results command.
    """
    if point_subset == "68":
        point_subset = None
    result_mgr = ResultsManager()

    existing_results = result_mgr.results_list()
    if len(model_ids) == 0:
        mid_set = set(models.keys())
    else:
        mid_set = set(model_ids)

    tid_set = set(testsets.keys()) if len(testset_ids) == 0 else set(testset_ids)

    result_names = [
        res for res in existing_results if res[0] in mid_set and res[1] in tid_set
    ]

    if len(result_names) == 0:
        print("No results to plot. Exiting.")
        exit(0)

    import numpy as np

    from .experiments import extract_errors, result_to_lmark_subset

    header = ["Testset", "Image feature", "Mean error", "Median error"]
    rows: list[list[str]] = []
    for mid, tid in result_names:
        result = result_mgr.load_results(mid, tid)
        if point_subset is not None:
            result = result_to_lmark_subset(result, point_subset)
        errors = extract_errors(result)
        rows.append(
            [
                tid,
                models[mid]["label"],
                f"{np.mean(errors):.2}",
                f"{np.median(errors):.2}",
            ]
        )
    rows.sort()
    rows.insert(0, header)

    csv.writer(output).writerows(rows)
