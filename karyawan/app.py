from flask import Flask, jsonify, request , render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'tugasduadwbi-tugasduadwbi.a.aivencloud.com'
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_ZDlr9ve2e04PDMAixdK'
app.config['MYSQL_DB'] = 'poli'
app.config['MYSQL_PORT'] = 22273  

 
mysql = MySQL(app)



@app.route('/karyawan', methods=['GET'])
def get_karyawan():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM karyawan")
        kolom = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(kolom,row)))
        cursor.close()
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Metode HTTP tidak didukung'}), 405

@app.route('/karyawan/<int:id>', methods=['GET'])
def get_karyawan_by_id(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM karyawan WHERE idPegawai=%s"
        cursor.execute(query, (id,))
        
        karyawan = cursor.fetchone()
        
        if karyawan:
            kolom = [i[0] for i in cursor.description]
            karyawan_data = dict(zip(kolom, karyawan))
            cursor.close()
            return jsonify(karyawan_data), 200
        else:
            cursor.close()
            return jsonify({'error': 'Karyawan tidak ditemukan'}), 404
    else:
        return jsonify({'error': 'Metode HTTP tidak didukung'}), 405





@app.route('/tambahkaryawan', methods=['POST'])
def tambah_karyawan():
    if request.method == 'POST':
        nama = request.json['nama']
        jabatan = request.json['jabatan']
        departemen = request.json['departemen']
        gaji = request.json['gaji']
        alamat = request.json['alamat']
        telpon = request.json['telepon']
        tanggal = request.json['tanggal']

        cursor = mysql.connection.cursor()
        sql = "INSERT INTO karyawan (nama, jabatan, departemen, gaji, alamat, telepon, tanggalMasuk) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (nama, jabatan, departemen, gaji, alamat, telpon, tanggal)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Data karyawan berhasil ditambahkan'}), 200
    else:
        return jsonify({'error': 'Metode HTTP tidak didukung'}), 405


@app.route('/hapuskaryawan', methods=['DELETE'])
def deletekaryawan():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM karyawan WHERE idPegawai = %s"
        val = (request.args['id'],)  
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'data berhasil dihapus'})


@app.route('/updatekaryawan',methods=['PUT'])
def editkaryawan():
    if 'id' in request.args:
        data = request.get_json()

        cursor = mysql.connection.cursor()
        sql = "UPDATE karyawan SET nama = %s, jabatan = %s, departemen = %s, gaji = %s, alamat = %s, telepon =%s , tanggalMasuk =%s WHERE idPegawai = %s"
        val = (data['nama'],data['jabatan'],data['departemen'],data['gaji'],data['alamat'],data['telepon'],data['tanggal'],request.args['id'])
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()  

        return jsonify({'message': 'data berhasil diubah'})

    

    




if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False,port=5002)