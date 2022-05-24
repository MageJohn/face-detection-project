from itertools import starmap
from pathlib import Path

import menpo
from more_itertools import side_effect

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

    @staticmethod
    def _clean_result(res):
        res._image = None

    def save_results(self, results, model_id: str, testset_id: str) -> None:
        menpo.io.export_pickle(
            list(side_effect(self._clean_result, results)),
            self._ids_to_path(model_id, testset_id),
            overwrite=True,
            protocol=4,
        )

    def results_exist(self, model_id: str, testset_id: str) -> bool:
        return self._ids_to_path(model_id, testset_id).is_file()

    def load_results(self, model_id: str, testset_id: str):
        return menpo.io.import_pickle(self._ids_to_path(model_id, testset_id))

    def load_all_results(self):
        return list(starmap(self.load_results, self.results_list()))

    def results_list(self) -> list[tuple[str, str]]:
        return sorted(
            [
                self._path_to_ids(p)
                for p in self.path.iterdir()
                if p.suffixes == [".pkl", ".gz"]
            ]
        )

    def _name_to_path(self, name: str) -> Path:
        return self.path / f"{name}.pkl.gz"

    def _ids_to_path(self, model_id: str, testset_id: str) -> Path:
        return self._name_to_path(f"{model_id}_{testset_id}_results")

    @staticmethod
    def _path_to_ids(path: Path) -> tuple[str, str]:
        parts = ResultsManager._stem(path).split("_")
        return (parts[0], parts[1])

    @staticmethod
    def _stem(path: Path) -> str:
        return path.name[: -len("_results.pkl.gz")]
