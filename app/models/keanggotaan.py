from ..utils  import db

class Keanggotaan(db.Model): #digunakan untuk membuat tabel pada database 
    __tablename__ = 'keanggotaan'
    id = db.Column(db.Integer(), primary_key=True)
    mahasiswa_id = db.Column(db.Integer, db.ForeignKey('mahasiswa.nim'))
    ukm_id = db.Column(db.Integer, db.ForeignKey('ukm.id_ukm'))
    tanggal_masuk = db.Column(db.Date, nullable=False)

    mahasiswa = db.relationship ('Mahasiswa', backref='keanggotaan')
    ukm = db.relationship ('UKM', backref='keanggotaan')

def __repr__(self):
    return f'<keanggotaan {self.id}>'