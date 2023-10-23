from flask_restx import Namespace, Resource, fields
from flask import request
from flask import jsonify, json
from http import HTTPStatus
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from ..utils import db
from ..models.mahasiswa import Mahasiswa
from ..logs.log import flasklogger

auth_ns = Namespace('auth', 'Namespace for auth')

# .model() digunakan untuk mendefiniskan atribut dari model tersebut
# digunakan untuk melakukan validasi data yang diterima dan memberikan struktur respons
auth_model = auth_ns.model(
    # mendefinisikan model auth dengan atribut sesuai dengan tabel mahasiswa
    'mahasiswaa', {
        'nama': fields.String(),
        'password': fields.String(),
        'alamat': fields.String(),
        'tanggal_lahir': fields.Date(format='%Y-%m-%d'),
        'email': fields.String(),
        'no_telepon': fields.String(),
        'jurusan_id': fields.Integer()
    }
)

auth_login_model = auth_ns.model(
    # mendefinisikan model users dengan atribut id, username, password
    'mahasiswa_login', {
        'email': fields.String(),
        'password': fields.String(),
    }
)

@auth_ns.route('/SignUp')
class SignUp(Resource):
    @auth_ns.expect(auth_model)
    @auth_ns.doc(
        description = "Sign Up for Mahasiswa"
    )
    def post(self):
        """An sign up for new account"""

        data = request.get_json()
        email = data.get('email')

        # Periksa apakah alamat email sudah ada dalam basis data
        existing_user = Mahasiswa.query.filter_by(email=email).first()

        if existing_user:
            auth_ns.abort(HTTPStatus.BAD_REQUEST, message="Email is already taken.")

        flasklogger.info(f"password original = {data.get('password)')}") # untuk mengetahui informasi password asli
        try:
            data = request.get_json()

            # Jika alamat email belum ada, simpan ke basis data
            new_account = Mahasiswa(
                nama = data.get('nama'),
                alamat = data.get('alamat'),
                tanggal_lahir = data.get('tanggal_lahir'),
                email = data.get('email'),
                no_telepon = data.get('no_telepon'),
                jurusan_id = data.get('jurusan_id'),
                password = generate_password_hash(data.get('password'))
            )

            flasklogger.info(f"Data Account sign up =  {new_account}")
            flasklogger.info(f"password hash =  {new_account.password}")

            db.session.add(new_account)
            db.session.commit()

            return [], HTTPStatus.OK

        except Exception as e:
            print("Error Post : ", e)
            return [], HTTPStatus.BAD_REQUEST

@auth_ns.route("/SignIn")
class SignIn(Resource):
    @auth_ns.expect(auth_login_model)
    @auth_ns.doc(
        description = "Sign In for Mahasiswa"
    )
    def post(self):
        """An sign in for new account"""

        data = request.get_json()
        email = data.get('email')

        # Periksa apakah alamat email ada dalam basis data
        data_mhs = Mahasiswa.query.filter_by(email=email).first()
        if (not data_mhs):
            auth_ns.abort(HTTPStatus.BAD_REQUEST, message="Email is not found.")

         # Periksa apakah password sudah benar
        cek_password = check_password_hash(data_mhs.password, data.get('password'))
        if(cek_password is False):
            auth_ns.abort(HTTPStatus.BAD_REQUEST, message="Incorrect Password.")

        try:
            mhs = Mahasiswa.query.filter_by(email = data.get('email')).first()
            print(f"mhs db : {mhs.email}")
            print(f"mhs db : {mhs.password}")
            check_password = check_password_hash(mhs.password, data.get('password'))

            print(f"check pass : {check_password}")
            flasklogger.info(f"check_password =  {check_password}")

            if mhs and check_password:
                access_token = create_access_token(identity= mhs.email)
                refresh_token = create_refresh_token(identity= mhs.email)

            response = {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

            return response, HTTPStatus.OK

        except Exception as e:
            print("Error Get : ", e)
            return [], HTTPStatus.BAD_REQUEST
   
@auth_ns.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """Refresh JWT token"""

        try:
            email = get_jwt_identity()
            
            access_token = create_access_token(identity= email)

            response = {'access_token': access_token}, HTTPStatus.OK

        except Exception as e:
            print("Error refresh : ", e)
            return [], HTTPStatus.BAD_REQUEST
        