const express = require('express')
const app = express()
const bodyParser = require('body-parser');


app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

const mysql = require('mysql');


const connection = mysql.createConnection({
    host: 'tugasduadwbi-tugasduadwbi.a.aivencloud.com',
    port: '22273',
    user: 'avnadmin',
    password: 'AVNS_ZDlr9ve2e04PDMAixdK',
    database: 'poli'
});

connection.connect((err) => {
    if (err) throw err;
    
});



app.get('/poliklinik', (req, res) => {
    connection.query('SELECT * FROM poliklinik', (error, results, fields) => {
        if (error) {
            res.status(500).json({ error: 'Terjadi kesalahan dalam mengambil data dari database.' });
            return;
        }
        res.json(results); 
    });
});

app.get('/poliklinik/:id_poliklinik', (req, res) => {
    const idPoliklinik = req.params.id_poliklinik;

    
    connection.query('SELECT * FROM poliklinik WHERE idPoli = ?', [idPoliklinik], (error, results, fields) => {
        if (error) {
            res.status(500).json({ error: 'Terjadi kesalahan dalam mengambil data dari database.' });
            return;
        }

        
        if (results.length === 0) {
            res.status(404).json({ error: 'Data poliklinik tidak ditemukan.' });
            return;
        }

        res.json(results[0]); 
    });
});


app.post('/tambahpoliklinik', (req, res) => {
    const { nama, lokasi , deskripsi } = req.body;

    
    if (!nama || !lokasi || !deskripsi) {
        res.status(400).json({ error: 'Data harus diisi semua.' });
        return;
    }

    
    connection.query('INSERT INTO poliklinik (Nama_Poliklinik, Deskripsi, Lokasi) VALUES (?, ?, ?)', [nama, deskripsi, lokasi], (error, results, fields) => {
        if (error) {
            res.status(500).json({ error: 'Terjadi kesalahan dalam menambahkan data ke database.' });
            return;
        }
        res.json({ message: 'Data poliklinik berhasil ditambahkan.' });
    });
});

app.put('/updatepoliklinik/:id_poliklinik', (req, res) => {
    const idPoliklinik = req.params.id_poliklinik;
    const { nama, lokasi, deskripsi } = req.body;

    
    if (!nama || !lokasi || !deskripsi) {
        res.status(400).json({ error: 'Nama, lokasi, dan deskripsi poliklinik diperlukan.' });
        return;
    }

    
    connection.query('UPDATE poliklinik SET Nama_Poliklinik = ?, Deskripsi = ?, Lokasi = ? WHERE idPoli = ?', [nama, deskripsi, lokasi, idPoliklinik], (error, results, fields) => {
        if (error) {
            res.status(500).json({ error: 'Terjadi kesalahan dalam memperbarui data di database.' });
            return;
        }
        
        
        if (results.affectedRows === 0) {
            res.status(404).json({ error: 'Data poliklinik tidak ditemukan.' });
            return;
        }

        res.json({ message: 'Data poliklinik berhasil diperbarui.' });
    });
});


app.delete('/hapuspoliklinik/:id_poliklinik', (req, res) => {
    const idPoliklinik = req.params.id_poliklinik;

    
    connection.query('DELETE FROM poliklinik WHERE idPoli = ?', [idPoliklinik], (error, results, fields) => {
        if (error) {
            res.status(500).json({ error: 'Terjadi kesalahan dalam menghapus data dari database.' });
            return;
        }

       
        if (results.affectedRows === 0) {
            res.status(404).json({ error: 'Data poliklinik tidak ditemukan.' });
            return;
        }

        res.json({ message: 'Data poliklinik berhasil dihapus.' }); // Mengirimkan pesan sukses
    });
});





const PORT = process.env.PORT || 5001;
app.listen(PORT, () => {
    console.log(`Server berjalan di port ${PORT}`);
});
