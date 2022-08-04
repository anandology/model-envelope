"""Model Envelope
"""
import json
from pathlib import Path
import web
import cloudpickle

__version__ = "0.1"

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

    @property
    def query_function(self):
        if self._query_function is None:
            self._query_function = self.load_query_function()
        return self._query_function

    @staticmethod
    def find_all():
        rows = get_db().select("model")
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
    return model

def list_models(name=None, tags={}):
    models = ModelEnvelope.find_all()
    if name:
        models = [m for m in models if m.name == name]
    for tag_name, tag_value in tags.items():
        models = [m for m in models if m.has_tag(tag_name, tag_value)]
    return models