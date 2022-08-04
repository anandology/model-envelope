"""Model Envelope
"""
import json
from pathlib import Path
import web
import cloudpickle
import sys
import subprocess

__version__ = "0.2"

db_url = "sqlite:///model.db"
storage_path = "models"

@web.memoize
def get_db():
    return web.database(db_url)

class ModelEnvelope:
    def __init__(self, id, name, description, tags):
        self.id = id
        self.name = name
        self.description = description
        self.tags = tags
        self._query_function = None

    def write_query_function(self, query_function):
        path = Path(storage_path) / str(self.id) / "model.pkl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as f:
            cloudpickle.dump(query_function, f)

    def load_query_function(self):
        path = Path(storage_path) / str(self.id) / "model.pkl"
        with path.open("rb") as f:
            return cloudpickle.load(f)

    def write_artifact(self, filename: str, contents: bytes):
        """Writes an artifact related to the model.
        """
        path = Path(storage_path) / str(self.id) / filename
        with path.open("wb") as f:
            cloudpickle.dump(contents, f)
        print("write", path)

    def _get_artifact_path(self, filename: str) -> Path:
        return Path(storage_path) / str(self.id) / filename

    def save_params(self, params):
        """Saves the params used to create this model.
        """
        with self._get_artifact_path("params.json").open("w") as f:
            json.dump(params, f)

    def get_params(self):
        with self._get_artifact_path("params.json").open() as f:
            return json.load(f)

    def save_environment(self):
        cmd = [sys.executable, "-m", "pip", "freeze"]
        requirements = subprocess.check_output(cmd).decode('ascii').strip().split("\n")
        d = {
            "python_version": list(sys.version_info),
            "requirements": requirements
        }
        with self._get_artifact_path("env.json").open("w") as f:
            json.dump(d, f)

    def get_environment(self):
        with self._get_artifact_path("env.json").open() as f:
            return json.load(f)

    @property
    def query_function(self):
        if self._query_function is None:
            self._query_function = self.load_query_function()
        return self._query_function

    @staticmethod
    def find_all():
        rows = get_db().select("model", order="id desc")
        return [ModelEnvelope(row.id, row.name, row.description, json.loads(row.tags)) for row in rows]

    @staticmethod
    def find(id):
        row = get_db().where("model", id=id).first()
        return ModelEnvelope(row.id, row.name, row.description, json.loads(row.tags))

    @staticmethod
    def new(name, description, tags):
        tags = json.dumps(tags)
        id = get_db().insert("model", name=name, description=description, tags=tags)
        return ModelEnvelope.find(id)

    def __repr__(self):
        return f"<ModelEnvelope#{self.id} {self.name!r}>"

def save_model(query_function, name, description, tags):
    """Saves a model and returns the ModelEnvelope object.
    """
    model = ModelEnvelope.new(name, description, tags)
    model.write_query_function(query_function)
    model.save_environment()
    return model

def get_model(model_id):
    """Returns the ModelEnvelope for given id."""
    return ModelEnvelope.find(model_id)

def list_models(name=None, tags={}):
    models = ModelEnvelope.find_all()
    if name:
        models = [m for m in models if m.name == name]
    for tag_name, tag_value in tags.items():
        models = [m for m in models if m.has_tag(tag_name, tag_value)]
    return models