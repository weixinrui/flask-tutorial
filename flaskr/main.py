from flaskr.create_app import init_log
from flaskr.create_app import create_app

def main():
    sys_log = init_log()
    app = create_app()
    return app