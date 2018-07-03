from flask import Flask, jsonify, request, abort, make_response
import sys
import os
import requests

from models import ModelRepository, utility

app = Flask(__name__)
model_repositories = ModelRepository()


class InYourAreaAPI:
    """
    simplify interactions with the InYourArea.co.uk API.
    """
    BASE_URL = "https://itemstore-cache-prod.inyourarea.co.uk/items"

    def article_by_id(self, article_id):
        uri = f"{self.BASE_URL}/articles/{article_id}"

        r = requests.get(uri)
        if r.status_code != 200:
            raise KeyError(f"no article with ID {article_id}.")
        else:
            return r.json()

    def location_by_id(self, location_id):
        uri = f"{self.BASE_URL}/locations/{location_id}"

        r = requests.get(uri)
        if r.status_code != 200:
            raise KeyError(f"no location with ID {location_id}.")
        else:
            return r.json()


in_your_area_api = InYourAreaAPI()


@app.route("/location-filters/predictions", methods=["POST"])
def predict():
    """
    given an article and a list of locations, predicts the relevancy those locations for the article.
    :return:
    """
    article_id = request.json.get("article_id")
    location_ids = request.json.get("location_ids")

    try:
        article = in_your_area_api.article_by_id(article_id)
    except KeyError as e:
        message = e.args[0] if len(e.args) > 0 else "resource not found."
        abort(make_response(jsonify(error=message), 404))

    publisher = utility.clean_publisher(article["publisher"])
    if publisher in model_repositories.list_models():
        model = model_repositories[publisher]
    else:
        abort(make_response(jsonify(error=f"no model available for {article['publisher']}"), 404))

    predictions = {"article_id": article_id, "title": article["item"]["title"],
                   "predictions": [],
                   "publisher": article["publisher"]
                   }

    for location_id in location_ids:
        try:
            location = in_your_area_api.location_by_id(location_id)
        except KeyError as e:
            message = e.args[0] if len(e.args) > 0 else "resource not found."
            predictions["predictions"].append({"id": location_id, "error": message})
        else:
            X = model.process_location(location)
            prediction = model.predict(X)
            is_relevant = bool(prediction[0])

            confidence = model.predict_proba(X)[0]
            print(is_relevant, confidence)
            predictions["predictions"].append(
                {
                    "id": location_id,
                    "name": location["name"],
                    "relevant": is_relevant,
                    "confidence": confidence
                })

    return jsonify(predictions), 200


@app.route("/location-filters/models", methods=["GET"])
def list_models():
    """
    Lists all the publishers available in the current filters repository.
    :return:
    """
    return jsonify(model_repositories.list_models()), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
