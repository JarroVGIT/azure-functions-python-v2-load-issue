import azure.functions as func
import logging
# The following imports have no error.
from normal_blueprint.bp import normal_bp
from properly_handled.bp import properly_handled_bp

app = func.FunctionApp()

@app.route(route='from_root')
def main(req: func.HttpRequest):
    logging.info("Request received to root")
    return func.HttpResponse(
        "This is from the root of the function app",
        status_code=200
    )

app.register_blueprint(normal_bp)
app.register_blueprint(properly_handled_bp)

## The following lines are commented out because they cause the function app to fail to start

from import_error.bp import import_error_bp
app.register_blueprint(import_error_bp)

# from missing_env.bp import missing_env_bp
# app.register_blueprint(missing_env_bp)