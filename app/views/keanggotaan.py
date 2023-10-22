from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource, fields
from ..utils import db
from ..models.keanggotaan import Keanggotaan

from datetime import datetime
from ..logs.log import flasklogger

#namespace digunakan untuk mengelompokkan route yang berkaitan dengan entitas tertentu
#nama namespace digunakan untuk sebagai nama endpoint, nanti jadinya /users
anggota_ns = Namespace('keanggotaan', description='Namespace for keanggotaan')

# .model() digunakan untuk mendefiniskan atribut dari model tersebut
# digunakan untuk melakukan validasi data yang diterima dan memberikan struktur respons

anggota_input_model = anggota_ns.model(
    'Keanggotaan', {
        'mahasiswa_id': fields.Integer(),
        'ukm_id': fields.Integer(),
        'tanggal_masuk': fields.Date(format='%Y-%m-%d')
    }
)

mahasiswa_model = anggota_ns.model(
    'Mahasiswa', {
        'nim': fields.Integer(description = "Ini adalah nim "),
        'nama': fields.String(description = "Ini adalah nama mahasiswa"),
        'password': fields.String(description = "Ini adalah password "),
        'alamat': fields.String(description = "Ini adalah alamat mahasiswa"),
        'tanggal_lahir': fields.Date(format='%Y-%m-%d', description = "Ini adalah tanggal lahirs"),
        'email': fields.String(description = "Ini adalah email"),
        'no_telepon': fields.String(description = "Ini adalah no telepon"),
        'jurusan_id': fields.Integer(description = "Ini adalah jurusan")
    }
)

ukm_model = anggota_ns.model(
    # mendefinisikan model ukm dengan atribut id, nama ukm, dan deskripsi
    'UKM', {
        'id_ukm': fields.Integer(description = "Ini adalah kode UKM"),
        'nama_ukm': fields.String(description = "Ini adalah nama UKM"),
        'deskripsi': fields.String(description = "Ini adalah deskripsi UKM")
    }
)

anggota_get_model = anggota_ns.model(
    'anggotaan', {
        'id': fields.Integer(description = "Ini adalah data id anggota"),
        'tanggal_masuk': fields.Date(format ='%Y-%m-%d', description = "Ini adalah tanggal masuk"),
        'mahasiswa': fields.Nested(mahasiswa_model,description = "Ini adalah data id dari relasi mahasiswa"), #penamaan tidak boleh sama dengan data lain
        'ukm': fields.Nested(ukm_model,description = "Ini adalah deskripsi UKM") # ukm_id diganti dnegan ukm
    }
)

@anggota_ns.route('/') #mendefinisikan route /users/
class AnggotaGetPost(Resource):
    @anggota_ns.marshal_list_with(anggota_get_model) 
    # mashal_list_with digunakan untuk mengkonversi banyak objek ke format JSON
    @anggota_ns.doc(description = "Get all keanggotaan")
    def get(self):
        """Get All Data Keanggotaan UKM"""
        try:
            data_anggota = Keanggotaan.query.all()
            print("data berhasil : ", data_anggota)

            flasklogger.info(f"Data keanggotaan =  {data_anggota}")
            return data_anggota, HTTPStatus.OK #menjalankan perintah get prodi jika berhasil
     
        except Exception as e:
            print(str(e))
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
        
    @anggota_ns.doc(
        description = "Create New Keanggotaan UKM"
    )
    @anggota_ns.expect(anggota_input_model)  # menggunakan model "anggota_model" untuk validasi input di body
    @anggota_ns.marshal_with(anggota_input_model) # untuk mengkonversi satu objek ke format JSON
    def post(self):
        """Get New Data Keanggotaan UKM"""

        try:
            #get_json() adalah metode request yang menguraikan data dalam badan permintaan sebagai JSON. 
            #Jika data dalam badan permintaan adalah JSON yang valid, metode ini akan mengembalikan objek Python yang sesuai. 
            #Jika data tersebut bukan JSON yang valid, maka akan muncul sebuah pengecualian.

            new_data = request.get_json() 
            print(f"data : {new_data}") #ketika sudah dipastikan aman tidak butuh lagi function seperti print input kalau di kava console.log
            
            new_input_data = Keanggotaan(
                mahasiswa_id = new_data.get('mahasiswa_id'),
                ukm_id = new_data.get('ukm_id'),
                tanggal_masuk = new_data.get('tanggal_masuk')
            )

            flasklogger.info(f"Data keanggotaan =  {new_input_data}")
            db.session.add(new_input_data)
            db.session.commit()

            return [], HTTPStatus.CREATED

        except Exception as e:
            print("Error Post : ", e)
            print(str(e))
            return [], HTTPStatus.BAD_REQUEST

@anggota_ns.route('/<int:id_anggota>')
class AnggotaGetPutDelete(Resource):
    @anggota_ns.doc(
            description = "Get Keanggotaan UKM data by id", 
            params = {"id_anggota": "Id Anggota"}
    )
    @anggota_ns.marshal_list_with(anggota_get_model)
    def get(self, id_anggota):
        """Get Keanggotaan data by id"""
        try:
            data = Keanggotaan.query.get_or_404(id_anggota)

            flasklogger.info(f"Data keanggotaan =  {data}")
            return data, HTTPStatus.OK

        except Exception as e:
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
        
    @anggota_ns.marshal_with(anggota_input_model)
    @anggota_ns.expect(anggota_input_model)
    @anggota_ns.doc(
        description = "Update Keanggotaan by Id",
        params = {
            "id_anggota" : "An Id a given Keanggotaan for method PUT by id"
        }
    )
    def put(self, id_anggota):
        """Update Keanggotaan Data by Id Unique"""
        try:
            data_update = Keanggotaan.query.get_or_404(id_anggota)
            data = request.get_json(force=True)

            data_update.mahasiswa_id = data['mahasiswa_id'],
            data_update.ukm_id = data['ukm_id'],
            data_update.tanggal_masuk = data['tanggal_masuk'],

            flasklogger.info(f"Data keanggotaan =  {data_update}")
            db.session.commit()

            return [], HTTPStatus.OK
        
        except Exception as e:
            print("Error update by id : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    @anggota_ns.marshal_with(anggota_input_model)
    @anggota_ns.doc(
        description = "Delete by Keanggotaan id",
        params = {
            "id_anggota" : "An Id a given Keanggotaan for method PUT by id"
        }
    )
    def delete(self, id_anggota):
        """Delete UKM Data by Id Unique"""
        try:
            data_delete = Keanggotaan.query.get_or_404(id_anggota)
    
            flasklogger.info(f"Data keanggotaan =  {data_delete}")
            db.session.delete(data_delete)
            db.session.commit()

            return [], HTTPStatus.OK
        
        except Exception as e:
            print("Error delete by id : ", e)
            return [], HTTPStatus.BAD_REQUEST

        
    