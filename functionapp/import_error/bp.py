import azure.functions as func
import logging

from does_not_exists import something # type: ignore

import_error_bp = func.Blueprint()

@import_error_bp.route(route="import_error")
def func2(req: func.HttpRequest):
    logging.info("Request received to import_error_bp")
    return func.HttpResponse(
        "This is from import_error in the function app",
        status_code=200
    )