import os
import json
from pathlib import Path
from test_drone import init_app
from config import load_conf


def _run_app(app):
    """执行启动服务的操作."""
    if app.extensions.get('run_application') is None:
        app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.debug)
    else:
        app.run_application()


def run(args):
    config = load_conf(args)
    app = init_app(config)
    _run_app(app)
