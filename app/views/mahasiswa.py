from http import HTTPStatus
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from ..utils import db
from ..models.mahasiswa import Mahasiswa
from ..models.jurusan import Jurusan
from ..logs.log import flasklogger

#namespace digunakan untuk mengelompokkan route yang berkaitan dengan entitas tertentu
#nama namespace digunakan untuk sebagai nama endpoint, nanti jadinya /users
mahasiswa_ns = Namespace('mahasiswa', description='Namespace for mahasiswa')

# .model() digunakan untuk mendefiniskan atribut dari model tersebut
# digunakan untuk melakukan validasi data yang diterima dan memberikan struktur respons
mahasiswa_input_model = mahasiswa_ns.model(
    # mendefinisikan model users dengan atribut kode, nama mk
    'Mahasiswa', {
        'nama': fields.String(description = "Ini adalah nama mahasiswa"),
        'password': fields.String(description = "Ini adalah password "),
        'alamat': fields.String(description = "Ini adalah alamat mahasiswa"),
        'tanggal_lahir': fields.Date(format='%Y-%m-%d', description = "Ini adalah tanggal lahirs"),
        'email': fields.String(description = "Ini adalah email"),
        'no_telepon': fields.String(description = "Ini adalah no telepon"),
        'jurusan_id': fields.Integer(description = "Ini adalah jurusan")
    }
)

jurusan_model = mahasiswa_ns.model(
    # mendefinisikan model users dengan atribut kode, nama mk
    'Jurusan', {
        'kode_jurusan': fields.Integer(description = "Ini adalah kode jurusan"),
        'nama_jurusan': fields.String(description = "Ini adalah nama jurusan")
    }
)

mahasiswa_get_model = mahasiswa_ns.model(
    # mendefinisikan model users dengan atribut kode, nama mk
    'mhs', {
        'nim': fields.Integer(description = "Ini adalah nim "),
        'nama': fields.String(description = "Ini adalah nama mahasiswa"),
        'password': fields.String(description = "Ini adalah password "),
        'alamat': fields.String(description = "Ini adalah alamat mahasiswa"),
        'tanggal_lahir': fields.Date(format='%Y-%m-%d', description = "Ini adalah tanggal lahirs"),
        'email': fields.String(description = "Ini adalah email"),
        'no_telepon': fields.String(description = "Ini adalah no telepon"),
        'jurusan': fields.Nested(jurusan_model, description = "Ini adalah jurusan")
    }
)

@mahasiswa_ns.route('/') #mendefinisikan route /users/
class MhsGetPost(Resource):
    #resource berisi :
    # self : mengakses properti atau metode lain dari kelas resource
    # args : berisi nilai parameter URL misal /users/<int:user_id>, jadi bisa mengambil user_id
    # kwargs : berisi nilai parameter query string, misal terdapat parameter ?=name=Nia, nisa mengambil query name
    # data : berisi json yang di body request

    # .doc() untuk memberikan keterangan di swaggernya 
    @mahasiswa_ns.marshal_list_with(mahasiswa_get_model) 
    # mashal_list_with digunakan untuk mengkonversi banyak objek ke format JSON
    @mahasiswa_ns.doc(description = "Get all mahasiswa")
    def get(self):
        """Get All Data Mahasiswa"""
        try:
            data_mhs = Mahasiswa.query.all()
            print("data berhasil : ", data_mhs)
            flasklogger.info(f"Data mahasiswa =  {data_mhs}")

            # message = "Data mahasiswa berhasil ditemukan."  # Pesan sukses
            # return jsonify({"data_mhs": data_mhs, "message": message}), HTTPStatus.OK
            return data_mhs, HTTPStatus.OK #menjalankan perintah get prodi jika berhasil
     
        except Exception as e:
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
    
    @mahasiswa_ns.doc(
        description = "Create New Mahasiswa"
    )
    @mahasiswa_ns.expect(mahasiswa_input_model)  # menggunakan model "mahasiswa_model" untuk validasi input di body
    @mahasiswa_ns.marshal_with(mahasiswa_input_model) # untuk mengkonversi satu objek ke format JSON
    def post(self):
        """Get New Data Mahasiswa"""

        data = request.get_json()
        email = data.get('email')
        no_tlp = data.get('no_telepon')
        data_jurusan = data.get('jurusan_id')

        # Periksa apakah alamat email, no tlp sudah ada dalam basis data
        existing_mhs = Mahasiswa.query.filter_by(email=email).first()
        existing_tlp = Mahasiswa.query.filter_by(no_telepon=no_tlp).first()

        # Periksa apakah data jurusan ada dalam basis data
        major = Jurusan.query.filter_by(jurusan_id=data_jurusan).first()


        if existing_mhs:
            mahasiswa_ns.abort(HTTPStatus.BAD_REQUEST, message="Email is already taken.")
        
         if existing_tlp:
            mahasiswa_ns.abort(HTTPStatus.BAD_REQUEST, message="No telepon is already taken.")

        if (not major):
            mahasiswa_ns.abort(HTTPStatus.BAD_REQUEST, message="data jurusan is not found.")

        try:
            new_mhs = request.get_json()
            print(f"data : {new_mhs}") #ketika sudah dipastikan aman tidak butuh lagi function seperti print input kalau di kava console.log
            
            new_input_mhs = Mahasiswa(
                nama = new_mhs.get('nama'),
                password = new_mhs.get('password'),
                alamat = new_mhs.get('alamat'),
                tanggal_lahir = new_mhs.get('tanggal_lahir'),
                email = new_mhs.get('email'),
                no_telepon = new_mhs.get('no_telepon'),
                jurusan_id = new_mhs.get('jurusan_id'),
            )

            flasklogger.info(f"Data mahasiswa =  {new_input_mhs}")
            db.session.add(new_input_mhs)
            db.session.commit()

            return [], HTTPStatus.CREATED

        except Exception as e:
            print("Error Post : ", e)
            return [], HTTPStatus.BAD_REQUEST


@mahasiswa_ns.route('/<int:mhs_id>')
class MhsGetPutDelete(Resource):
    @mahasiswa_ns.doc(
            description = "Get mahasiswa data by id", 
            params = {"mhs_id": "Id mhs"}
    )
    @mahasiswa_ns.marshal_list_with(mahasiswa_get_model)
    def get(self, mhs_id):
        """Get mahasiswa data by id"""
        try:
            data = Mahasiswa.query.get_or_404(mhs_id)

            flasklogger.info(f"Data mahasiswa =  {data}")
            return data, HTTPStatus.OK

        except Exception as e:
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
        
    @mahasiswa_ns.marshal_with(mahasiswa_input_model)
    @mahasiswa_ns.expect(mahasiswa_input_model)
    @mahasiswa_ns.doc(
        description = "Update Mahasiswa by Id",
        params = {
            "mhs_id" : "An Id a given mahasiswa for method PUT by id"
        }
    )
    def put(self, mhs_id):
        """Update Mahasiswa Data by Id Unique"""
        try:
            data_update = Mahasiswa.query.get_or_404(mhs_id)

            data = request.get_json(force=True)

            data_update.nama = data['nama'],
            data_update.password = data['password'],
            data_update.alamat = data['alamat'],
            data_update.tanggal_lahir = data['tanggal_lahir'],
            data_update.email = data['email'],
            data_update.no_telepon = data['no_telepon'],
            data_update.jurusan_id = data['jurusan_id'],

            flasklogger.info(f"Data mahasiswa =  {data_update}")
            db.session.commit()

            return [], HTTPStatus.OK
        
        except Exception as e:
            print("Error update by id : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    @mahasiswa_ns.marshal_with(mahasiswa_input_model)
    @mahasiswa_ns.doc(
        description = "Delete by mahasiswa id",
        params = {
            "mhs_id" : "An Id a given mahasiswa for method PUT by id"
        }
    )
    def delete(self, mhs_id):
        """Delete User Data by Id Unique"""
        try:
            data_delete = Mahasiswa.query.get_or_404(mhs_id)
    
            flasklogger.info(f"Data mahasiswa =  {data_delete}")
            db.session.delete(data_delete)
            db.session.commit()

            return [], HTTPStatus.OK
        
        except Exception as e:
            print("Error delete by id : ", e)
            return [], HTTPStatus.BAD_REQUEST

        
    