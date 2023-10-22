from ..utils  import db
from ..models import keanggotaan

class Mahasiswa(db.Model): #digunakan untuk membaut tabel pada database 
    __tablename__ = 'mahasiswa'
    nim = db.Column(db.Integer(), primary_key=True)
    nama = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, unique=True)
    alamat = db.Column(db.String(255), nullable=False)
    tanggal_lahir = db.Column(db.Date, nullable=False) 
    email = db.Column(db.String(50), nullable=False, unique=True)
    no_telepon = db.Column(db.String(50), nullable=False, unique=True)
    jurusan_id = db.Column(db.Integer(), db.ForeignKey('jurusan.kode_jurusan'), nullable=False) #jurusan.id (tabel jurusan dengan id untuk relasi)
    
    jurusans = db.relationship ('Jurusan', backref='mahasiswa')
    ukms = db.relationship('UKM', secondary='keanggotaan', backref='mahasiswa')

def __repr__(self):
    return f'<mahasiswa {self.nama}>' 