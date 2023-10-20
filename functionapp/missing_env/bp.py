import azure.functions as func
import logging
import os

missing_env_bp = func.Blueprint()

MY_CONSTANT = os.environ["DOES_NOT_EXIST"]

@missing_env_bp.route(route="missing_env")
def func3(req: func.HttpRequest):
    logging.info("Request received to missing_env_bp")
    return func.HttpResponse(
        "This is from missing_env in the function app",
        status_code=200
    )