from flask import Flask
app = Flask(__name__)
app.secret_key = "ChooseAKeyOrLeaveThisAlone"

# from flask.app.controllers import controllerNameHere (maybe not needed?)
# No need to touch this page unless you want to change the secret key.