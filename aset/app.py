from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
#from datetime import datetime


app = Flask(__name__)

#MySQLconfig
app.config['MYSQL_HOST'] = 'tugasduadwbi-tugasduadwbi.a.aivencloud.com'
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_ZDlr9ve2e04PDMAixdK'
app.config['MYSQL_DB'] = 'widhya'
app.config['MYSQL_PORT'] = 22273

mysql = MySQL(app)


@app.route('/aset', methods=['GET'])
def asset():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM aset")
        kolom = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(kolom, row)))
        cursor.close()
        return jsonify(data), 200
    else:
        return jsonify ({'error' : 'Method HTTP tidak didukung'}), 405

@app.route('/aset/<int:id>', methods=['GET'])
def get_asset_by_id(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM aset WHERE idAset=%s"
        cursor.execute(query, (id,))
        
        asset = cursor.fetchone()
        
        if asset:
            kolom = [i[0] for i in cursor.description]
            asset_data = dict(zip(kolom, asset))
            cursor.close()
            return jsonify(asset_data), 200
        else:
            cursor.close()
            return jsonify({'error': 'Aset tidak ditemukan'}), 404
    else:
        return jsonify({'error': 'Metode HTTP tidak didukung'}), 405
   
@app.route('/tambahaset', methods=['POST'])
def tambah_aset():
    if request.method =='POST':
        nama = request.json['nama']
        tipe = request.json['tipe']
        merek = request.json['merek']
        lokasi = request.json['lokasi']
        stok = request.json['stok']

        cursor = mysql.connection.cursor()
        sql = "INSERT INTO aset (nama, tipe, merek, lokasi, stok) VALUES (%s, %s, %s, %s, %s)"
        val = (nama, tipe, merek, lokasi, stok)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Data berhasil masuk'}), 200
    else:
        return jsonify({'error': 'Metode HTTP tidak didukung'}), 405
    
@app.route('/hapusaset', methods=['DELETE'])
def deleteaset():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM aset WHERE idAset = %s"
        val = (request.args['id'],) 
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()  

        return jsonify({'message': 'Data berhasil dihapus'})#, 200
    #else:
        return jsonify({'error': 'Parameter id tidak ditemukan'}), 400

@app.route('/updateaset', methods=['PUT'])
def editaset():
    if 'id' in request.args:
        data = request.get_json()

        cursor = mysql.connection.cursor()
        sql = "UPDATE aset SET nama = %s, tipe = %s, merek = %s, lokasi = %s, stok = %s WHERE idAset = %s"
        val = (data['nama'],data['tipe'],data['merek'],data['lokasi'],data['stok'],request.args['id'])
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()  

        return jsonify({'message': 'data berhasil diubah'})
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug = False)