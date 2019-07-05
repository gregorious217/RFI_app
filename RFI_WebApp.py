from app import app
from app.models import User, Rfi, Team


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Rfi': Rfi}