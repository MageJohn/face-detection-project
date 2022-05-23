from operator import methodcaller
from pathlib import Path

import menpo
from funcy import walk

DATA_PATH = Path(__file__).parent / ".." / "data"


class ModelManager:
    def __init__(self):
        self.path = DATA_PATH / "models"
        self.path.mkdir(parents=True, exist_ok=True)

    def save_model(self, id, model):
        menpo.io.export_pickle(model, self._id_to_path(id), overwrite=True, protocol=4)

    def load_model(self, id):
        return menpo.io.import_pickle(self._id_to_path(id))

    def model_exists(self, id):
        return self._id_to_path(id).is_file()

    def _id_to_path(self, id):
        return self.path / f"{id}.pkl.gz"


class ResultsManager:
    def __init__(self):
        self.path = DATA_PATH / "results"
        self.path.mkdir(parents=True, exist_ok=True)

    def save_results(self, results, model_id, testset_id):
        menpo.io.export_pickle(
            walk(methodcaller("to_result", pass_image=False), results),
            self._ids_to_path(model_id, testset_id),
            overwrite=True,
            protocol=4,
        )

    def results_exist(self, model_id, testset_id):
        return self._ids_to_path(model_id, testset_id).is_file()

    def load_results(self, name):
        return menpo.io.import_pickle(self._name_to_path(name))

    def load_all_results(self):
        return list(map(self.load_results, self.results_list()))

    def results_list(self):
        return sorted(
            [
                p.name[: -len(".pkl.gz")]
                for p in self.path.iterdir()
                if p.suffixes == [".pkl", ".gz"]
            ]
        )

    def _name_to_path(self, name):
        return self.path / f"{name}.pkl.gz"

    def _ids_to_path(self, model_id, testset_id):
        return self._name_to_path(f"{model_id}_{testset_id}_results")
