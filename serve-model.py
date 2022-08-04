"""Serves a model as an API.

USAGE:

    $ python serve-model.py 2
"""
import argparse
import json
import model_envelope as me
from flask import Flask, request, jsonify

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("model_id")
    return p.parse_args()

args = parse_args()
model = me.get_model(args.model_id)

print(f"Serving {model} ...")

app = Flask(__name__)

@app.route("/model", methods=["POST"])
def serve():
    args = request.get_json()
    result = model.query_function(**args)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run()