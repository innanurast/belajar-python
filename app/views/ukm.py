from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource, fields
from ..utils import db
from ..models.ukm import UKM
from ..logs.log import flasklogger

#namespace digunakan untuk mengelompokkan route yang berkaitan dengan entitas tertentu
#nama namespace digunakan untuk sebagai nama endpoint, nanti jadinya /users
ukm_ns = Namespace('ukm', description='Namespace for unit kegiatan mahasiswa')

# .model() digunakan untuk mendefiniskan atribut dari model tersebut
# digunakan untuk melakukan validasi data yang diterima dan memberikan struktur respons
ukm_model = ukm_ns.model(
    # mendefinisikan model ukm dengan atribut id, nama ukm, dan deskripsi
    'UKM', {
        'id_ukm': fields.Integer(description = "Ini adalah kode UKM"),
        'nama_ukm': fields.String(description = "Ini adalah nama UKM"),
        'deskripsi': fields.String(description = "Ini adalah deskripsi UKM")
    }
)

@ukm_ns.route('/') #mendefinisikan route /users/
class UkmGetPost(Resource):
    @ukm_ns.marshal_list_with(ukm_model) 
    # mashal_list_with digunakan untuk mengkonversi banyak objek ke format JSON
    @ukm_ns.doc(description = "Get all ukm")
    def get(self):
        """Get All Data UKM"""
        try:
            data_ukm = UKM.query.all()
            print("data berhasil : ", data_ukm)

            flasklogger.info(f"Data UKM =  {data_ukm}")
            return data_ukm, HTTPStatus.OK #menjalankan perintah get prodi jika berhasil
     
        except Exception as e:
            print(str(e))
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
        
        
    @ukm_ns.doc(
        description = "Create New UKM"
    )
    @ukm_ns.expect(ukm_model)  # menggunakan model "ukm_model" untuk validasi input di body
    @ukm_ns.marshal_with(ukm_model) # untuk mengkonversi satu objek ke format JSON
    def post(self):
        """Get New Data UKM"""

        try:
            new_data = request.get_json()
            print(f"data : {new_data}") #ketika sudah dipastikan aman tidak butuh lagi function seperti print input kalau di kava console.log
            
            new_input_data = UKM(
                nama_ukm = new_data.get('nama_ukm'),
                deskripsi = new_data.get('deskripsi')
            )

            flasklogger.info(f"Data UKM =  {new_input_data}")
            db.session.add(new_input_data)
            db.session.commit()

            return [], HTTPStatus.CREATED

        except Exception as e:
            print("Error Post : ", e)
            return [], HTTPStatus.BAD_REQUEST

@ukm_ns.route('/<int:id_ukm>')
class UserGetPutDelete(Resource):
    @ukm_ns.doc(
            description = "Get UKM data by id", 
            params = {"id_ukm": "Id UKM"}
    )
    @ukm_ns.marshal_list_with(ukm_model)
    def get(self, id_ukm):
        """Get UKM data by id"""
        try:
            data = UKM.query.get_or_404(id_ukm)

            flasklogger.info(f"Data UKM =  {data}")
            return data, HTTPStatus.OK

        except Exception as e:
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
        
    @ukm_ns.marshal_with(ukm_model)
    @ukm_ns.expect(ukm_model)
    @ukm_ns.doc(
        description = "Update UKM by Id",
        params = {
            "id_ukm" : "An Id a given UKM for method PUT by id"
        }
    )
    def put(self, id_ukm):
        """Update UKM Data by Id Unique"""
        try:
            data_update = UKM.query.get_or_404(id_ukm)

            data = ukm_ns.payload

            data_update.nama_ukm = data['nama_ukm'],
            data_update.deskripsi = data['deskripsi']

            flasklogger.info(f"Data update UKM =  {data_update}")
            db.session.commit()

            return [], HTTPStatus.OK
        
        except Exception as e:
            print("Error update by id : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    @ukm_ns.marshal_with(ukm_model)
    @ukm_ns.doc(
        description = "Delete by UKM id",
        params = {
            "id_ukm" : "An Id a given UKM for method PUT by id"
        }
    )
    def delete(self, id_ukm):
        """Delete UKM Data by Id Unique"""
        try:
            data_delete = UKM.query.get_or_404(id_ukm)
    
            flasklogger.info(f"Data delete UKM =  {data_delete}")
            db.session.delete(data_delete)
            db.session.commit()

            return [], HTTPStatus.OK
        
        except Exception as e:
            print("Error delete by id : ", e)
            return [], HTTPStatus.BAD_REQUEST

        
    