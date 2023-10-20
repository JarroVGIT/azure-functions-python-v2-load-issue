import azure.functions as func
import logging

normal_bp = func.Blueprint()

@normal_bp.route(route="normal_bp")
def func1(req: func.HttpRequest):
    logging.info("Request received to normal_bp")
    return func.HttpResponse(
        "This is from normal bp in the function app",
        status_code=200
    )