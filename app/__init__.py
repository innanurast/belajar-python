from flask import Flask
from flask_migrate import Migrate
from .config.config import config_dict
from flask_restx import Api
from flask_jwt_extended import JWTManager

from .views.jurusan import jurusan_ns
from .views.mahasiswa import mahasiswa_ns
from .views.ukm import ukm_ns
from .views.keanggotaan import anggota_ns

from .utils import db
# from flask_sqlalchemy import SQLAlchemy
from .models import jurusan
from .models import mahasiswa
from .models import ukm
from .models import keanggotaan
from .logs.log import flasklogger

def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    api = Api(
        app,
        doc='/tugasApi',
        title="REST API FLASK",
        description="Tugas Membuat REST API dengan Flask"
    )

    api.add_namespace(jurusan_ns)
    api.add_namespace(mahasiswa_ns)
    api.add_namespace(ukm_ns)
    api.add_namespace(anggota_ns)

    migrate = Migrate(app, db)

    jwt = JWTManager(app)
    
    flasklogger.debug('Initial run API flask')

    return app