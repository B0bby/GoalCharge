import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from flask.ext.script import Manager, Server
from GoalCharge import app

manager = Manager(app)

# Turn on debugger and reloader
manager.add_command("runserver", Server(
    use_debugger = False,
    use_reloader = True,
    host = '0.0.0.0'
    )
)

if __name__ == "__main__":
    manager.run()
