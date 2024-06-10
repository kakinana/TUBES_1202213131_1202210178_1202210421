# Gunakan image Node.js yang telah disediakan oleh Docker Hub
FROM node:14-slim

# Set direktori kerja di dalam container
WORKDIR /app

# Salin file package.json dan package-lock.json ke dalam direktori kerja
COPY package*.json ./

# Install dependensi yang diperlukan
RUN npm install

# Salin semua file aplikasi ke dalam direktori kerja
COPY . .

EXPOSE 5001

# Perintah untuk menjalankan aplikasi ketika container dimulai
CMD ["node", "app.js"]
