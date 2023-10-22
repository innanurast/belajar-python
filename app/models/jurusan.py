from ..utils  import db

class Jurusan(db.Model): #digunakan untuk membuat tabel pada database 
    __tablename__ = 'jurusan'
    kode_jurusan = db.Column(db.Integer(), primary_key=True)
    nama_jurusan = db.Column(db.String(30), nullable=False, unique=True)
    mahasiswas = db.relationship('Mahasiswa', backref='jurusan', lazy=True)

def __repr__(self):
    return f'<jurusan {self.nama_jurusan}>' 