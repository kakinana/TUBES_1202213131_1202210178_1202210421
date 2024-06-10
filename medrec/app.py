from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL

app= Flask(__name__)

app.config['MYSQL_HOST'] = 'tugasduadwbi-tugasduadwbi.a.aivencloud.com'
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_ZDlr9ve2e04PDMAixdK'
app.config['MYSQL_DB'] = 'sekar'
app.config['MYSQL_PORT'] = 22273

mysql = MySQL(app)

@app.route('/medrec', methods=['GET'])
def medrec():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM medrec")
        kolom = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(kolom, row)))
        cursor.close()
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Metode HTTP tidak didukung'}), 405
    
@app.route('/medrec/<int:id>', methods=['GET'])
def get_med_by_id(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM medrec WHERE idPat=%s"
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
    
@app.route('/tambahmedrec', methods = ['POST'])
def add_medrec():
    if request.method =='POST':
        nama = request.json['nama']
        birth = request.json['birth']
        address = request.json['address']
        disease = request.json['disease']
        handling = request.json['handling']
        medic = request.json['medic']
        time = request.json['time']
        nurse = request.json['nurse']
        dokter = request.json['dokter']
        
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO medrec (name_pat,birthdate_pat,address_pat,timestamp,disease,handling,medicine_pat,nurse_name,doctor_name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        val = (nama,birth,address,time,disease,handling,medic,nurse,dokter)
        cursor.execute(sql,val)

        mysql.connection.commit()
        cursor.close()

        return jsonify({'message':'data berhasil masuk'})
    else:
        return jsonify({'error': 'Metode HTTP tidak didukung'}), 405
    
#get untuk id mengetahui data dari id tertentu
@app.route('/detailmedrec',methods =['GET'])
def detailpasien():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM medrec WHERE idPat = %s"
        val = (request.args['id'])
        cursor.execute(sql,val)
        kolom = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(kolom,row)))
        cursor.close()
        
        return jsonify(data)


@app.route('/updatemedrec', methods = ['PUT'])
def edit_medrec():
    if 'id' in request.args:
        data = request.get_json()

        cursor = mysql.connection.cursor()
        sql = "UPDATE medrec SET name_pat = %s, birthdate_pat = %s, address_pat = %s, timestamp = %s, disease =%s, handling =%s ,medicine_pat =%s, nurse_name=%s, doctor_name=%s WHERE idPat = %s"
        val = (data['nama'],data['birth'],data['address'],data['time'],data['disease'],data['handling'],data['medic'],data['nurse'],data['dokter'],request.args['id'])
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()  

        return jsonify({'message': 'data berhasil diubah'})

@app.route('/hapusmedrec', methods=['DELETE'])
def delete_medrec():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM medrec WHERE idPat = %s"
        val = (request.args['id'],) 
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()  

        return jsonify({'message': 'Data berhasil dihapus'}), 200
    #else:
        return jsonify({'error': 'Parameter id tidak ditemukan'}), 400

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5006, debug = False)