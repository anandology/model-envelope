# model-envelope
POC implementation of Model Envelope by Stitchfix

## Setup

Install dependencies:

```
$ pip install -r requirements.txt
```

Setup the sqlite database.

```
$ sqlite3 model.db < schema.sql
```

## Usage

```
import model_envelope as me

# save a model
m = me.save_model(predict_function,
    name="pengins-classification,
    description="Classification of pengins",
    tags={
        "dataset": "pengins",
        "model-flavor": "prod",
        "classifier": "DecisionTree"
    })

# attach params
m.save_params({"random_state": 100, "max_depth": 2})

# attach any other metadata
m.save_metadata({"algo": "sklearn.tree.DecisionTreeClassifier"})

# List all models
models = me.list_models()

# List all models matching some tag
models = me.list_models(tags={"dataset": "pengins"})

# Read params, metadata and environment
m = models[0]
print(m)
print("Params", m.get_params())
print("Metadata", m.get_metadata())
print("Environment", m.get_environment())
```

## Serve a Model

To serve a model:

```
$ python serve-model.py model-id
...
```

Once the model is served, you can post the data to `/model` endpoint.

```
$ curl -H 'content-type: application/json' -d '{"bill_length_mm": 39.1, "bill_depth_mm": 18.7, "flipper_length_mm": 181, "body_mass_g": 3750}' http://localhost:8000/model
{"result": "Adelie"}
```