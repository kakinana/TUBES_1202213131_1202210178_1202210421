from flask import Flask, render_template, request, redirect, url_for , session
from flask_mysqldb import MySQL
import requests

app = Flask(__name__)
app.secret_key = 'rahasia'

#login
app.config['MYSQL_HOST'] = 'tugasduadwbi-tugasduadwbi.a.aivencloud.com'
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_ZDlr9ve2e04PDMAixdK'
app.config['MYSQL_DB'] = 'admin'
app.config['MYSQL_PORT'] = 22273

mysql = MySQL(app)


#layanan karyawan
def get_karyawan():
    response = requests.get('http://karyawan:5002/karyawan')
    return response.json()

def get_karyawan_id(id):
    url = f'http://karyawan:5002/karyawan/{id}'
    response = requests.get(url)
    return response.json()


#layanan poliklink
def get_poli():
    response = requests.get('http://poli:5001/poliklinik')
    return response.json()

def get_poli_id(id):
    url = f'http://poli:5001/poliklinik/{id}'
    response = requests.get(url)
    return response.json()

# layanan dokter
def get_dokter():
    response = requests.get('http://dokter:5007/dokter')
    return response.json()

def get_dokter_id(id):
    url = f'http://dokter:5007/dokter/{id}'
    response = requests.get(url)
    return response.json()

def get_jadwal():
    response = requests.get('http://dokter:5007/jadwaldokter')
    return response.json()

def get_jadwal_id(id):
    url = f'http://dokter:5007/jadwaldokter/{id}'
    response = requests.get(url)
    return response.json()

#layanan aset dan obat
def get_obat():
    response = requests.get('http://obat:5004/obat')
    return response.json()

def get_obat_id(id):
    url = f'http://obat:5004/obat/{id}'
    response = requests.get(url)
    return response.json()

def get_aset():
    response = requests.get('http://aset:5003/aset')
    return response.json()

def get_aset_id(id):
    url = f'http://aset:5003/aset/{id}'
    response = requests.get(url)
    return response.json()


#layanan pasien
def get_pasien():
    response = requests.get('http://pasien:5005/pasien')
    return response.json()

def get_pasien_id(id):
    url = f'http://pasien:5005/pasien/{id}'
    response = requests.get(url)
    return response.json()

#layanan medrec
def get_medrec():
    response = requests.get('http://medrec:5006/medrec')
    return response.json()

def get_medrec_id(id):
    url = f'http://medrec:5006/medrec/{id}'
    response = requests.get(url)
    return response.json()

#layanan partner

def get_request():
    response = requests.get('http://partner:5100/request')
    return response.json()

def get_request_id(id):
    url = f'http://partner:5100/request/{id}'
    response = requests.get(url)
    return response.json()

##############################################################

#route utama
# @app.route('/')
# def index():
#     return render_template('landing.html')

# @app.route('/adminpage')
# def admin():
#     return render_template('index.html')
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Ambil input dari form
        username = request.form['username']
        password = request.form['password']
        
        # Cek apakah username dan password cocok dengan data di MySQL
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        
        if user:
            # Jika user ditemukan, set session dan arahkan ke halaman beranda
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('beranda'))
        else:
            # Jika tidak, tampilkan pesan error
            error = 'Username atau password salah. Silakan coba lagi.'
            return render_template('login.html', error=error)
    
    # Jika method adalah GET, tampilkan halaman login
    return render_template('login.html')

@app.route('/adminpage')
def beranda():
    if 'logged_in' in session:
        # Jika sudah login, tampilkan halaman beranda
        username = session['username']
        return render_template('index.html', username=username)
    else:
        # Jika belum login, redirect ke halaman login
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Hapus session dan arahkan ke halaman login
    session.clear()
    return redirect(url_for('login'))

#KARYAWAN
@app.route('/karyawan')
def showkaryawan():
    karyawan = get_karyawan()
    return render_template('karyawan.html', karyawan=karyawan)

#geser ke html form tambah 
@app.route('/addkar')
def tambah_karyawan():
    return render_template('addKar.html')
#tambah karyawan
@app.route('/addkaryawan', methods=['POST'])
def karyawan():
    data = request.form
    response = requests.post('http://karyawan:5002/tambahkaryawan', json=data)
    return redirect(url_for('showkaryawan')) 

#geser ke html form edit 
@app.route('/editkar/<int:id>')
def edit_karyawan(id):
    karyawan = get_karyawan_id(id)
    return render_template('editKar.html', id=id, karyawan=karyawan)


#update karyawan
@app.route('/updatekaryawan/<int:id>', methods=['POST'])
def update_karyawan(id):
    data = request.form
    response = requests.put(f'http://karyawan:5002/updatekaryawan?id={id}', json=data)
    return redirect(url_for('showkaryawan'))

#delete karyawan
@app.route('/deletekaryawan/<int:id>')
def delete(id):
    response = requests.delete(f'http://karyawan:5002/hapuskaryawan?id={id}')
    return redirect(url_for('showkaryawan'))

##############################################################

#POLIKLINIK
@app.route('/poliklinik')
def showpoli():
    pol = get_poli()
    return render_template('poliklinik.html',pol=pol)

#geser ke html form tambah 
@app.route('/addpol')
def tambah_poli():
    return render_template('addPoli.html')
#tambah poliklinik
@app.route('/addpoli', methods=['POST'])
def poli():
    data = request.form
    response = requests.post('http://poli:5001/tambahpoliklinik', json=data)
    return redirect(url_for('showpoli')) 

#geser ke html form edit 
@app.route('/editpoli/<int:id>')
def edit_poli(id):
    poliklinik = get_poli_id(id)
    return render_template('editPoli.html', id=id, poliklinik=poliklinik)
#update poliklinik
@app.route('/updatepoli/<int:id>', methods=['POST'])
def update_poli(id):
    data = request.form
    response = requests.put(f'http://poli:5001/updatepoliklinik/{id}', json=data)
    return redirect(url_for('showpoli'))

#delete poliklinik
@app.route('/deletepoli/<int:id>')
def delete_poli(id):
    response = requests.delete(f'http://poli:5001/hapuspoliklinik/{id}')
    return redirect(url_for('showpoli'))
#############################################################

@app.route('/dokter')
def showdokter():
    dokter = get_dokter()
    return render_template('dokter.html',dokter=dokter)
# Geser ke html tambah

@app.route('/adddok')
def tambah_dokter():
    return render_template('addDokter.html')
#Tambah Dokter
@app.route('/tambahdokter', methods=['POST'])
def dokter():
    data = request.form
    response = requests.post('http://dokter:5007/tambahdokter', json=data)
    return redirect(url_for('showdokter')) 
#update dokter
#geser ke html form edit 
@app.route('/editdokter/<int:id>')
def edit_dokter(id):
    dokter = get_dokter_id(id)
    return render_template('editDokter.html', id=id, dokter=dokter)

@app.route('/updatedokter/<int:id>', methods=['POST'])
def update_dokter(id):
    data = request.form
    response = requests.put(f'http://dokter:5007/updatedokter/{id}', json=data)
    return redirect(url_for('showdokter'))
#delete 
@app.route('/deletedokter/<int:id>')
def delete_dokter(id):
    response = requests.delete(f'http://dokter:5007/hapusdokter/{id}')
    return redirect(url_for('showdokter'))
#JADWAL

@app.route('/jadwal')
def showjadwal():
    jad = get_jadwal()
    return render_template('jadwal.html',jad=jad)

#tambah jadwal
@app.route('/addjad')
def tambah_jadwal():
    return render_template('addJadwal.html')
#Tambah jadwal
@app.route('/tambahjadwal', methods=['POST'])
def jadwal():
    data = request.form
    response = requests.post('http://dokter:5007/tambahjadwal', json=data)
    return redirect(url_for('showjadwal'))

@app.route('/editjadwal/<int:id>', methods=['GET', 'POST'])
def edit_jadwal(id):
    jadwal = get_jadwal_id(id)  
    return render_template('editJadwal.html', id=id, jadwal=jadwal)


@app.route('/updatejadwal/<int:id>', methods=['POST'])
def update_jadwal(id):
    data = request.form
    response = requests.put(f'http://dokter:5007/updatejadwal/{id}', json=data)
    return redirect(url_for('showjadwal'))
#Delete
@app.route('/deletejadwal/<int:id>')
def delete_jadwal(id):
    response = requests.delete(f'http://dokter:5007/hapusjadwal/{id}')
    return redirect(url_for('showjadwal'))

##############################################################

#OBAT
@app.route('/obat')
def showobat():
    obaat = get_obat()
    return render_template('obat.html', obaat=obaat)

#geser ke html form tambah 
@app.route('/adddrug')
def tambah_obat():
    return render_template('addObat.html')
#tambah obat
@app.route('/addobat', methods=['POST'])
def obat():
    data = request.form
    response = requests.post('http://obat:5004//tambahobat', json=data)
    return redirect(url_for('showobat')) 

#geser ke html form edit 
@app.route('/editobat/<int:id>')
def edit_obat(id):
    obat = get_obat_id(id)
    return render_template('editObat.html', id=id, obat=obat)
#update obat
@app.route('/updateobat/<int:id>', methods=['POST'])
def update_obat(id):
    data = request.form
    response = requests.put(f'http://obat:5004/updateobat?id={id}', json=data)
    return redirect(url_for('showobat'))

#delete obat
@app.route('/deleteobat/<int:id>')
def delete_obat(id):
    response = requests.delete(f'http://obat:5004/hapusobat?id={id}')
    return redirect(url_for('showobat'))

##############################################################

#ASET
@app.route('/aset')
def showaset():
    aset = get_aset()
    return render_template('aset.html', aset=aset)

#geser ke html form tambah 
@app.route('/addasset')
def tambah_aset():
    return render_template('addAset.html')
#tambah aset
@app.route('/addAset', methods=['POST'])
def aset():
    data = request.form
    response = requests.post('http://aset:5003/tambahaset', json=data)
    return redirect(url_for('showaset')) 

#geser ke html form edit 
@app.route('/editaset/<int:id>')
def edit_aset(id):
    aset = get_aset_id(id)
    return render_template('editAset.html', id=id, aset=aset)
#update aset
@app.route('/updateaset/<int:id>', methods=['POST'])
def update_aset(id):
    data = request.form
    response = requests.put(f'http://aset:5003/updateaset?id={id}', json=data)
    return redirect(url_for('showaset'))

#delete aset
@app.route('/deleteaset/<int:id>')
def delete_aset(id):
    response = requests.delete(f'http://aset:5003/hapusaset?id={id}')
    return redirect(url_for('showaset'))

##############################################################

#PASIEN
@app.route('/pasien')
def showpasien():
    pas = get_pasien()
    return render_template('pasien.html', pas=pas)

#geser ke html form tambah 
@app.route('/addpatient')
def tambah_pasien():
    return render_template('addPat.html')
#tambah pasien
@app.route('/addpasien', methods=['POST'])
def pasien():
    data = request.form
    response = requests.post('http://pasien:5005/tambahpasien', json=data)
    return redirect(url_for('showpasien')) 

#geser ke html form edit 
@app.route('/editpasien/<int:id>')
def edit_pasien(id):
    pasien = get_pasien_id(id)
    return render_template('editPat.html', id=id, pasien=pasien)
#update pasien
@app.route('/updatepasien/<int:id>', methods=['POST'])
def update_pasien(id):
    data = request.form
    response = requests.put(f'http://pasien:5005/updatepasien?id={id}', json=data)
    return redirect(url_for('showpasien'))

#delete pasien
@app.route('/deletepasien/<int:id>')
def delete_pasien(id):
    response = requests.delete(f'http://pasien:5005/hapuspasien?id={id}')
    return redirect(url_for('showpasien'))

##############################################################

#MEDREC
@app.route('/medrec')
def showmedrec():
    medic = get_medrec()
    return render_template('medrec.html', medic=medic)

#geser ke html form tambah 
@app.route('/addmed')
def tambah_medrec():
    return render_template('addMedrec.html')
#tambah medrec
@app.route('/addmedic', methods=['POST'])
def medrec():
    data = request.form
    response = requests.post('http://medrec:5006/tambahmedrec', json=data)
    return redirect(url_for('showmedrec')) 

#geser ke html form edit 
@app.route('/editmedrec/<int:id>')
def edit_medrec(id):
    medrec = get_medrec_id(id)
    return render_template('editMedrec.html', id=id, medrec=medrec)
#update medrec
@app.route('/updatemedrec/<int:id>', methods=['POST'])
def update_medrec(id):
    data = request.form
    response = requests.put(f'http://medrec:5006/updatemedrec?id={id}', json=data)
    return redirect(url_for('showmedrec'))

#delete medrec
@app.route('/deletemedrec/<int:id>')
def delete_medrec(id):
    response = requests.delete(f'http://medrec:5006/hapusmedrec?id={id}')
    return redirect(url_for('showmedrec'))

##############################################################

@app.route('/request')
def showpartner():
    req = get_request()
    return render_template('partner.html', req=req)

@app.route('/addreq')
def req():
    return render_template('addReq.html')

@app.route('/addrequest', methods=['POST'])
def addreq():
    data = request.form
    response = requests.post('http://partner:5100/tambahrequest', json=data)
    return redirect(url_for('showpartner'))

@app.route('/editrequest/<int:id>')
def edit_request(id):
    req = get_request_id(id)
    return render_template('editReq.html', id=id, req=req)

@app.route('/updaterequest/<int:id>', methods=['POST'])
def update_request(id):
    data = request.form
    response = requests.put(f'http://partner:5100/updaterequest?id={id}', json=data)
    return redirect(url_for('showpartner'))

@app.route('/deleterequest/<int:id>')
def delete_request(id):
    response = requests.delete(f'http://partner:5100/hapusrequest?id={id}')
    return redirect(url_for('showpartner'))


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000) 