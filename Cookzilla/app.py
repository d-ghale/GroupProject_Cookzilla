from flask import Flask

UPLOAD_FOLDER_RECIPE = 'static/uploads/recipe'
UPLOAD_FOLDER_REVIEW = 'static/uploads/review'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER_RECIPE'] = UPLOAD_FOLDER_RECIPE
app.config['UPLOAD_FOLDER_REVIEW'] = UPLOAD_FOLDER_REVIEW

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
