import azure.functions as func
import logging

error = 'no error so far'

try:
    from does_not_exists import something # type: ignore
except ImportError as e:
    error = e

properly_handled_bp = func.Blueprint()

@properly_handled_bp.route(route="properly_handled")
def func4(req: func.HttpRequest):
    logging.info("Request received to properly_handled_bp")
    return func.HttpResponse(
        f"This is from properly_handled in the function app, error was properly caught: {error}",
        status_code=400
    )