import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

# Import helper script
from .predict import predict_image_from_url

@app.route(route="classify", auth_level=func.AuthLevel.Function)
def classify(req: func.HttpRequest) -> func.HttpResponse:
    image_url = req.params.get('img')
    logging.info('Image URL received: ' + image_url)

    results = predict_image_from_url(image_url)

    headers = {
        "Content-type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }

    return func.HttpResponse(json.dumps(results), headers = headers)