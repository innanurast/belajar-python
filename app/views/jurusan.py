from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource, fields
from ..utils import db
from ..models.jurusan import Jurusan
from ..logs.log import flasklogger

#namespace digunakan untuk mengelompokkan route yang berkaitan dengan entitas tertentu
#nama namespace digunakan untuk sebagai nama endpoint, nanti jadinya /users
jurusan_ns = Namespace('jurusan', description='Namespace for jurusan')

# .model() digunakan untuk mendefiniskan atribut dari model tersebut
# digunakan untuk melakukan validasi data yang diterima dan memberikan struktur respons
jurusan_model = jurusan_ns.model(
    # mendefinisikan model users dengan atribut kode, nama mk
    'Jurusan', {
        'kode_jurusan': fields.Integer(description = "Ini adalah kode jurusan"),
        'nama_jurusan': fields.String(description = "Ini adalah nama jurusan")
    }
)

@jurusan_ns.route('/') #mendefinisikan route /users/
class UserGetPost(Resource):
    #resource berisi :
    # self : mengakses properti atau metode lain dari kelas resource
    # args : berisi nilai parameter URL misal /users/<int:user_id>, jadi bisa mengambil user_id
    # kwargs : berisi nilai parameter query string, misal terdapat parameter ?=name=Nia, nisa mengambil query name
    # data : berisi json yang di body request

    # .doc() untuk memberikan keterangan di swaggernya 
    @jurusan_ns.marshal_list_with(jurusan_model) 
    # mashal_list_with digunakan untuk mengkonversi banyak objek ke format JSON
    @jurusan_ns.doc(description = "Get all jurusan")
    def get(self):
        """Get All Data Jurusan"""
        try:
            data_jurusan = Jurusan.query.all()
            print("data berhasil : ", data_jurusan)

            flasklogger.info(f"Data jurusan =  {data_jurusan}")
            return data_jurusan, HTTPStatus.OK #menjalankan perintah get prodi jika berhasil
     
        except Exception as e:
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
        
    @jurusan_ns.doc(
        description = "Create New Jurusan"
    )
    @jurusan_ns.expect(jurusan_model)  # menggunakan model "jurusan_model" untuk validasi input di body
    @jurusan_ns.marshal_with(jurusan_model) # untuk mengkonversi satu objek ke format JSON
    def post(self):
        """Get New Data Jurusan"""

        try:
            new_data = request.get_json()
            print(f"data : {new_data}") #ketika sudah dipastikan aman tidak butuh lagi function seperti print input kalau di kava console.log
            
            new_input_data = Jurusan(
                nama_jurusan = new_data.get('nama_jurusan')
            )

            flasklogger.info(f"Data jurusan =  {new_input_data}")
            db.session.add(new_input_data)
            db.session.commit()

            return [], HTTPStatus.CREATED

        except Exception as e:
            print("Error Post : ", e)
            return [], HTTPStatus.BAD_REQUEST

@jurusan_ns.route('/<int:jurusan_id>')
class UserGetPutDelete(Resource):
    @jurusan_ns.doc(
            description = "Get Jurusan data by id", 
            params = {"jurusan_id": "Id user"}
    )
    @jurusan_ns.marshal_list_with(jurusan_model)
    def get(self, jurusan_id):
        """Get Jurusan data by id"""
        try:
            data = Jurusan.query.get_or_404(jurusan_id)

            flasklogger.info(f"Data jurusan =  {data}")
            return data, HTTPStatus.OK

        except Exception as e:
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
        
    @jurusan_ns.marshal_with(jurusan_model)
    @jurusan_ns.expect(jurusan_model)
    @jurusan_ns.doc(
        description = "Update Jurusan by Id",
        params = {
            "jurusan_id" : "An Id a given jurusan for method PUT by id"
        }
    )
    def put(self, jurusan_id):
        """Update Jurusan Data by Id Unique"""
        try:
            data_update = Jurusan.query.get_or_404(jurusan_id)

            data = jurusan_ns.payload

            data_update.nama_jurusan = data['nama_jurusan']

            flasklogger.info(f"Data jurusan =  {data_update}")
            db.session.commit()

            return [], HTTPStatus.OK
        
        except Exception as e:
            print("Error update by id : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    @jurusan_ns.marshal_with(jurusan_model)
    @jurusan_ns.doc(
        description = "Delete by jurusan id",
        params = {
            "jurusan_id" : "An Id a given jurusan for method PUT by id"
        }
    )
    def delete(self, jurusan_id):
        """Delete User Data by Id Unique"""
        try:
            data_delete = Jurusan.query.get_or_404(jurusan_id)
    
            flasklogger.info(f"Data jurusan =  {data_delete}")
            db.session.delete(data_delete)
            db.session.commit()

            return [], HTTPStatus.OK
        
        except Exception as e:
            print("Error delete by id : ", e)
            return [], HTTPStatus.BAD_REQUEST

        
    