from ..utils  import db

class UKM(db.Model): #digunakan untuk membuat tabel pada database 
    __tablename__ = 'ukm'
    id_ukm = db.Column(db.Integer(), primary_key=True)
    nama_ukm = db.Column(db.String(50), nullable=False, unique=True)
    deskripsi = db.Column(db.String(255), nullable=True)

    mahasiswas = db.relationship('Mahasiswa', secondary='keanggotaan', backref='ukm')
def __repr__(self):
    return f'<ukm {self.nama_ukm}>' 