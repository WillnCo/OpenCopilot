import logging

from flask import Flask, request, jsonify, Response
from routes.workflow.workflow_controller import workflow
from routes._swagger.controller import _swagger
from typing import Any, Tuple
from utils.config import Config
from utils.__sql import sql_db

logging.basicConfig(level=logging.INFO)


app = Flask(__name__)

app.register_blueprint(workflow, url_prefix="/workflow")
app.register_blueprint(_swagger, url_prefix="/swagger_api")


app.config.from_object(Config)
from routes.root_service import handle_request


## TODO: Implement caching for the swagger file content (no need to load it everytime)
@app.route("/handle", methods=["POST", "OPTIONS"])
def handle() -> Response:
    data = request.get_json()
    try:
        response = handle_request(data)
        return jsonify(response)
    except Exception as e:
        return jsonify({"response": str(e)})


@app.errorhandler(500)
def internal_server_error(error: Any) -> Tuple[str, int]:
    # Log the error to the console
    print(error)
    return "Internal Server Error", 500


sql_db.init_app(app)

with app.app_context():
    sql_db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True)
