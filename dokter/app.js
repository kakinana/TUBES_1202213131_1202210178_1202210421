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





app.get('/dokter', (req, res) => {
    connection.query('SELECT dokter.idDok, dokter.nama, dokter.spesial, poliklinik.nama_poliklinik FROM dokter INNER JOIN poliklinik ON dokter.idPoli = poliklinik.idPoli', (error, results, fields) => {
        if (error) {
            console.error('Error saat menjalankan query:', error);
            res.status(500).json({ error: 'Terjadi kesalahan saat mengambil data dari server' });
            return;
        }
        
        res.json(results);
    });
});

app.get('/dokter/:id', (req, res) => {
    const dokterId = req.params.id;
    const query = `
        SELECT dokter.idDok, dokter.nama, dokter.spesial, poliklinik.nama_poliklinik 
        FROM dokter 
        INNER JOIN poliklinik ON dokter.idPoli = poliklinik.idPoli
        WHERE dokter.idDok = ?
    `;

    connection.query(query, [dokterId], (error, results, fields) => {
        if (error) {
            console.error('Error saat menjalankan query:', error);
            res.status(500).json({ error: 'Terjadi kesalahan saat mengambil data dari server' });
            return;
        }

        if (results.length === 0) {
            res.status(404).json({ error: 'Dokter tidak ditemukan.' });
            return;
        }

        res.json(results[0]);
    });
});


app.post('/tambahdokter', (req, res) => {
    const { nama, spesial , idpoli } = req.body;

    
    if (!nama || !spesial || !idpoli) {
        res.status(400).json({ error: 'Data harus diisi semua.' });
        return;
    }

    
    connection.query('INSERT INTO dokter (nama, spesial, idPoli) VALUES (?, ?, ?)', [nama, spesial, idpoli], (error, results, fields) => {
        if (error) {
            res.status(500).json({ error: 'Terjadi kesalahan dalam menambahkan data ke database.' });
            return;
        }
        res.json({ message: 'Data Dokter berhasil ditambahkan.' });
    });
});

app.put('/updatedokter/:id_dokter', (req, res) => {
    const idPoliklinik = req.params.id_dokter;
    const { nama, spesial, idPoli } = req.body;

    
    if (!nama || !spesial || !idPoli) {
        res.status(400).json({ error: 'Nama, spesialis, dan idPoli Dokter diperlukan.' });
        return;
    }

    
    connection.query('UPDATE dokter SET nama = ?, spesial = ?, idPoli = ? WHERE idDok = ?', [nama, spesial, idPoli, idPoliklinik], (error, results, fields) => {
        if (error) {
            res.status(500).json({ error: 'Terjadi kesalahan dalam memperbarui data di database.' });
            return;
        }
        
        
        if (results.affectedRows === 0) {
            res.status(404).json({ error: 'Data Dokter tidak ditemukan.' });
            return;
        }

        res.json({ message: 'Data Dokter berhasil diperbarui.' });
    });
});

app.delete('/hapusdokter/:id_dokter', (req, res) => {
    const idPoliklinik = req.params.id_dokter;

    
    connection.query('DELETE FROM dokter WHERE idDok = ?', [idPoliklinik], (error, results, fields) => {
        if (error) {
            res.status(500).json({ error: 'Terjadi kesalahan dalam menghapus data dari database.' });
            return;
        }

       
        if (results.affectedRows === 0) {
            res.status(404).json({ error: 'Data Dokter tidak ditemukan.' });
            return;
        }

        res.json({ message: 'Data Dokter berhasil dihapus.' }); // Mengirimkan pesan sukses
    });
});

app.get('/jadwaldokter', (req, res) => {

    connection.query('SELECT jadwal_dokter.*, dokter.nama FROM jadwal_dokter INNER JOIN dokter ON jadwal_dokter.idDok = dokter.idDok', (error, results, fields) => {
        if (error) {
            res.status(500).json({ error: 'Terjadi kesalahan dalam mengambil data dari database.' });
            return;
        }
        res.json(results);
    });
});

app.get('/jadwaldokter/:id', (req, res) => {
    const jadwalId = req.params.id;
    const query = `
        SELECT jadwal_dokter.*, dokter.nama 
        FROM jadwal_dokter 
        INNER JOIN dokter ON jadwal_dokter.idDok = dokter.idDok
        WHERE jadwal_dokter.idJadwal = ?
    `;

    connection.query(query, [jadwalId], (error, results, fields) => {
        if (error) {
            res.status(500).json({ error: 'Terjadi kesalahan dalam mengambil data dari database.' });
            return;
        }

        if (results.length === 0) {
            res.status(404).json({ error: 'Jadwal dokter tidak ditemukan.' });
            return;
        }

        res.json(results[0]);
    });
});



app.post('/tambahjadwal', (req, res) => {
    const { idDokter, hari , mulai , selesai } = req.body;

    
    if (!idDokter || !hari || !mulai || !selesai) {
        res.status(400).json({ error: 'Data harus diisi semua.' });
        return;
    }

    
    connection.query('INSERT INTO jadwal_dokter (idDok, hari, mulai, selesai) VALUES (?, ?, ?, ?)', [idDokter, hari, mulai , selesai], (error, results, fields) => {
        if (error) {
            res.status(500).json({ error: 'Terjadi kesalahan dalam menambahkan data ke database.' });
            return;
        }
        res.json({ message: 'Data Jadwal berhasil ditambahkan.' });
    });
});

app.put('/updatejadwal/:id_dokter', (req, res) => {
    const idPoliklinik = req.params.id_dokter;
    const { idDokter, hari , mulai , selesai } = req.body;

    
    if (!idDokter || !hari || !mulai || !selesai) {
        res.status(400).json({ error: 'Data harus diisi semua.' });
        return;
    }

    
    connection.query('UPDATE jadwal_dokter SET idDok = ?, hari = ?, mulai = ?, selesai = ? WHERE idJadwal = ?', [idDokter, hari, mulai , selesai, idPoliklinik], (error, results, fields) => {
        if (error) {
            res.status(500).json({ error: 'Terjadi kesalahan dalam memperbarui data di database.' });
            return;
        }
        
        
        if (results.affectedRows === 0) {
            res.status(404).json({ error: 'Data Jadwal tidak ditemukan.' });
            return;
        }

        res.json({ message: 'Data jadwal berhasil diperbarui.' });
    });
});

app.delete('/hapusjadwal/:id_dokter', (req, res) => {
    const idPoliklinik = req.params.id_dokter;

    
    connection.query('DELETE FROM jadwal_dokter WHERE idJadwal = ?', [idPoliklinik], (error, results, fields) => {
        if (error) {
            res.status(500).json({ error: 'Terjadi kesalahan dalam menghapus data dari database.' });
            return;
        }

       
        if (results.affectedRows === 0) {
            res.status(404).json({ error: 'Data Dokter tidak ditemukan.' });
            return;
        }

        res.json({ message: 'Data jadwal berhasil dihapus.' }); // Mengirimkan pesan sukses
    });
});



const PORT = process.env.PORT || 5007;
app.listen(PORT, () => {
    console.log(`Server berjalan di port ${PORT}`);
});