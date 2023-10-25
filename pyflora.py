from app import create_app, db
from app.models import User, Pot, Sensor, Reading, Plant, Value, Gauge

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Pot': Pot, 'Sensor': Sensor, 'Reading': Reading, 'Plant': Plant, 'Value': Value, 'Gauge': Gauge}