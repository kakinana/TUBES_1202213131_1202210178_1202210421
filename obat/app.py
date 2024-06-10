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

@app.route('/obat', methods=['GET'])
def get_obat():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM obat")
        kolom = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(kolom, row)))
        cursor.close()
        
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Metode HTTP tidak didukung'}), 405

@app.route('/obat/<int:id>', methods=['GET'])
def get_obat_by_id(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM obat WHERE idObat=%s"
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

@app.route('/tambahobat', methods = ['POST'])
def add_obat():
    if request.method =='POST':
        nama = request.json['nama']
        tipe = request.json['tipe']
        jenis = request.json['jenis']
        stok = request.json['stok']

        cursor = mysql.connection.cursor()
        sql = "INSERT INTO obat (nama, tipe, jenis, stok) VALUES (%s, %s, %s, %s)"
        val = (nama, tipe, jenis, stok)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Data obat berhasil masuk'}), 200
    else:
        return jsonify({'error': 'Metode HTTP tidak didukung'}), 405
    
@app.route('/hapusobat', methods=['DELETE'])
def delete_obat():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM obat WHERE idObat = %s"
        val = (request.args['id'],) 
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()  

        return jsonify({'message': 'Data obat berhasil dihapus'})#, 200
    #else:
        #return jsonify({'error': 'Parameter id tidak ditemukan'}), 400

@app.route('/updateobat', methods=['PUT'])
def edit_obat():
    if 'id' in request.args:
        data = request.get_json()

        cursor = mysql.connection.cursor()
        sql = "UPDATE obat SET nama = %s, tipe = %s, jenis = %s, stok = %s WHERE idObat = %s"
        val = (data['nama'],data['tipe'],data['jenis'],data['stok'],request.args['id'])
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()  

        return jsonify({'message': 'data obat berhasil diubah'})
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug = False)