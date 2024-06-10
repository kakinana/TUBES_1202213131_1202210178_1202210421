from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL

app= Flask(__name__)

app.config['MYSQL_HOST'] = 'tugasduadwbi-tugasduadwbi.a.aivencloud.com'
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_ZDlr9ve2e04PDMAixdK'
app.config['MYSQL_DB'] = 'sekar'
app.config['MYSQL_PORT'] = 22273

mysql = MySQL(app)

@app.route('/pasien', methods=['GET'])
def get_pasien():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM pasien")
        kolom = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(kolom, row)))
        cursor.close()
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Metode HTTP tidak didukung'}), 405

@app.route('/pasien/<int:id>', methods=['GET'])
def get_pat_by_id(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM pasien WHERE idPat=%s"
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
    
@app.route('/tambahpasien', methods = ['POST'])
def add_pasien():
    if request.method =='POST':
        nama = request.json['nama']
        birth = request.json['birth']
        address = request.json['address']
        blood = request.json['blood']

        cursor = mysql.connection.cursor()
        sql = "INSERT INTO pasien (name_pat,birthdate_pat,address_pat,bloodtype_pat) VALUES (%s,%s,%s,%s)"
        val = (nama,birth,address,blood)
        cursor.execute(sql,val)
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message':'Data pasien berhasil masuk'}), 200
    else:
        return jsonify({'error': 'Metode HTTP tidak didukung'}), 405
    

#@app.route('/detailpasien',methods =['GET'])
#def detailpasien():
    #if 'id' in request.args:
        #cursor = mysql.connection.cursor()
        #sql = "SELECT * FROM pasien WHERE idPat = %s"
        #val = (request.args['id'])
        #cursor.execute(sql,val)
        #kolom = [i[0] for i in cursor.description]
        #data = []
        #for row in cursor.fetchall():
            #data.append(dict(zip(kolom,row)))

        
        #return jsonify(data)
        #cursor.close()


@app.route('/updatepasien', methods = ['PUT'])
def edit_pasien():
    if 'id' in request.args:
        data = request.get_json()

        cursor = mysql.connection.cursor()
        sql = "UPDATE pasien SET name_pat = %s, birthdate_pat = %s, address_pat = %s, bloodtype_pat = %s WHERE idPat = %s"
        val = (data['nama'],data['birth'],data['address'],data['blood'],request.args['id'])
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()  

        return jsonify({'message': 'data pasien berhasil diubah'})
    
@app.route('/hapuspasien', methods=['DELETE'])
def delete_pasien():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM pasien WHERE idPat = %s"
        val = (request.args['id'],)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()  

        return jsonify({'message': 'Data pasien berhasil dihapus'})#, 200
    #else:
        #return jsonify({'error': 'Parameter id tidak ditemukan'}), 400

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5005, debug = False)