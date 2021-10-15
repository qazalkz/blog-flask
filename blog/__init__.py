from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
from flask_bcrypt import Bcrypt
from flask_uploads import configure_uploads, IMAGES, UploadSet
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '927b20c8683bcb65dafb69be8b956ba9953569f345dbb5451bf01cb9d1bd0303'
app.config['UPLOADED_IMAGES_DEST'] = 'static/images'



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../blog.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
images = UploadSet('images', IMAGES)
configure_uploads(app, images)
login_manager= LoginManager(app)

from blog import routes