import sqlite3
from datetime import datetime
import shutil

# Membuat koneksi ke database
conn = sqlite3.connect('toko_kelontong.db')
cursor = conn.cursor()

# Membuat tabel jika belum ada
cursor.execute('''CREATE TABLE IF NOT EXISTS Produk (
    ID_Produk INTEGER PRIMARY KEY AUTOINCREMENT,
    Nama_Produk TEXT,
    Harga INTEGER,
    Stok INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Pelanggan (
    ID_Pelanggan INTEGER PRIMARY KEY AUTOINCREMENT,
    Nama_Pelanggan TEXT,
    Alamat TEXT,
    No_Telepon TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Penjualan (
    ID_Penjualan INTEGER PRIMARY KEY AUTOINCREMENT,
    ID_Produk INTEGER,
    ID_Pelanggan INTEGER,
    Jumlah INTEGER,
    Total_Harga INTEGER,
    Tanggal DATE,
    FOREIGN KEY(ID_Produk) REFERENCES Produk(ID_Produk),
    FOREIGN KEY(ID_Pelanggan) REFERENCES Pelanggan(ID_Pelanggan)
)''')

conn.commit()

# Fungsi untuk memastikan input integer yang valid
def get_valid_int(prompt, positive_only=False):
    while True:
        try:
            value = int(input(prompt))
            if positive_only and value <= 0:
                print("Value must be a positive number.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Fungsi backup database
def backup_database():
    shutil.copy('toko_kelontong.db', 'toko_kelontong_backup.db')
    print("Database successfully backed up.")

# Fungsi restore database
def restore_database():
    shutil.copy('toko_kelontong_backup.db', 'toko_kelontong.db')
    print("Database successfully restored.")

# Fungsi laporan penjualan harian
def laporan_penjualan_harian():
    tanggal = input("Masukkan tanggal (YYYY-MM-DD): ")
    cursor.execute('''
        SELECT SUM(Total_Harga) FROM Penjualan WHERE Tanggal = ?
    ''', (tanggal,))
    total = cursor.fetchone()[0]
    if total:
        print(f"Total Penjualan pada {tanggal}: Rp{total}")
    else:
        print("Tidak ada penjualan pada tanggal tersebut.")

# Fungsi CRUD untuk Tabel Produk
def tambah_produk():
    nama = input("Masukkan Nama Produk: ")
    harga = get_valid_int("Masukkan Harga Produk: ")
    stok = get_valid_int("Masukkan Stok Produk: ", positive_only=True)
    cursor.execute("INSERT INTO Produk (Nama_Produk, Harga, Stok) VALUES (?, ?, ?)", (nama, harga, stok))
    conn.commit()
    print("Produk berhasil ditambahkan.")

def lihat_produk():
    cursor.execute("SELECT * FROM Produk")
    data = cursor.fetchall()
    print(f"{'ID':<5} {'Nama Produk':<20} {'Harga':<10} {'Stok':<5}")
    for produk in data:
        print(f"{produk[0]:<5} {produk[1]:<20} {produk[2]:<10} {produk[3]:<5}")

def edit_produk():
    lihat_produk()
    id_produk = get_valid_int("Masukkan ID Produk yang akan diedit: ")
    nama = input("Masukkan Nama Baru: ")
    harga = get_valid_int("Masukkan Harga Baru: ")
    stok = get_valid_int("Masukkan Stok Baru: ", positive_only=True)
    cursor.execute("UPDATE Produk SET Nama_Produk = ?, Harga = ?, Stok = ? WHERE ID_Produk = ?", (nama, harga, stok, id_produk))
    conn.commit()
    print("Produk berhasil diperbarui.")

def hapus_produk():
    lihat_produk()
    id_produk = get_valid_int("Masukkan ID Produk yang akan dihapus: ")
    cursor.execute("DELETE FROM Produk WHERE ID_Produk = ?", (id_produk,))
    conn.commit()
    print("Produk berhasil dihapus.")

# Fungsi CRUD untuk Tabel Pelanggan
def tambah_pelanggan():
    nama = input("Masukkan Nama Pelanggan: ")
    alamat = input("Masukkan Alamat Pelanggan: ")
    no_telepon = input("Masukkan No Telepon Pelanggan: ")
    cursor.execute("INSERT INTO Pelanggan (Nama_Pelanggan, Alamat, No_Telepon) VALUES (?, ?, ?)", (nama, alamat, no_telepon))
    conn.commit()
    print("Pelanggan berhasil ditambahkan.")

def lihat_pelanggan():
    cursor.execute("SELECT * FROM Pelanggan")
    data = cursor.fetchall()
    print(f"{'ID':<5} {'Nama Pelanggan':<20} {'Alamat':<30} {'No Telepon':<15}")
    for pelanggan in data:
        print(f"{pelanggan[0]:<5} {pelanggan[1]:<20} {pelanggan[2]:<30} {pelanggan[3]:<15}")

def edit_pelanggan():
    lihat_pelanggan()
    id_pelanggan = get_valid_int("Masukkan ID Pelanggan yang akan diedit: ")
    nama = input("Masukkan Nama Baru: ")
    alamat = input("Masukkan Alamat Baru: ")
    no_telepon = input("Masukkan No Telepon Baru: ")
    cursor.execute("UPDATE Pelanggan SET Nama_Pelanggan = ?, Alamat = ?, No_Telepon = ? WHERE ID_Pelanggan = ?", 
                   (nama, alamat, no_telepon, id_pelanggan))
    conn.commit()
    print("Pelanggan berhasil diperbarui.")

def hapus_pelanggan():
    lihat_pelanggan()
    id_pelanggan = get_valid_int("Masukkan ID Pelanggan yang akan dihapus: ")
    cursor.execute("DELETE FROM Pelanggan WHERE ID_Pelanggan = ?", (id_pelanggan,))
    conn.commit()
    print("Pelanggan berhasil dihapus.")

# Fungsi CRUD untuk Tabel Penjualan
def tambah_penjualan():
    lihat_produk()
    lihat_pelanggan()
    id_produk = get_valid_int("Masukkan ID Produk: ")
    id_pelanggan = get_valid_int("Masukkan ID Pelanggan: ")
    jumlah = get_valid_int("Masukkan Jumlah Produk: ", positive_only=True)
    cursor.execute("SELECT Harga, Stok FROM Produk WHERE ID_Produk = ?", (id_produk,))
    produk = cursor.fetchone()
    if produk and produk[1] >= jumlah:
        total_harga = produk[0] * jumlah
        cursor.execute("INSERT INTO Penjualan (ID_Produk, ID_Pelanggan, Jumlah, Total_Harga, Tanggal) VALUES (?, ?, ?, ?, ?)", 
                       (id_produk, id_pelanggan, jumlah, total_harga, datetime.now().date()))
        cursor.execute("UPDATE Produk SET Stok = Stok - ? WHERE ID_Produk = ?", (jumlah, id_produk))
        conn.commit()
        print("Penjualan berhasil ditambahkan.")
    else:
        print("Stok tidak mencukupi.")

def lihat_penjualan():
    cursor.execute('''SELECT p.ID_Penjualan, pr.Nama_Produk, pel.Nama_Pelanggan, p.Jumlah, p.Total_Harga, p.Tanggal 
                      FROM Penjualan p
                      JOIN Produk pr ON p.ID_Produk = pr.ID_Produk
                      JOIN Pelanggan pel ON p.ID_Pelanggan = pel.ID_Pelanggan''')
    data = cursor.fetchall()
    print(f"{'ID':<5} {'Nama Produk':<20} {'Nama Pelanggan':<20} {'Jumlah':<6} {'Total Harga':<12} {'Tanggal':<12}")
    for penjualan in data:
        print(f"{penjualan[0]:<5} {penjualan[1]:<20} {penjualan[2]:<20} {penjualan[3]:<6} {penjualan[4]:<12} {penjualan[5]:<12}")

def hapus_penjualan():
    lihat_penjualan()
    id_penjualan = get_valid_int("Masukkan ID Penjualan yang akan dihapus: ")
    cursor.execute("SELECT ID_Produk, Jumlah FROM Penjualan WHERE ID_Penjualan = ?", (id_penjualan,))
    penjualan = cursor.fetchone()
    if penjualan:
        cursor.execute("UPDATE Produk SET Stok = Stok + ? WHERE ID_Produk = ?", (penjualan[1], penjualan[0]))
        cursor.execute("DELETE FROM Penjualan WHERE ID_Penjualan = ?", (id_penjualan,))
        conn.commit()
        print("Penjualan berhasil dihapus dan stok diperbarui.")
    else:
        print("ID Penjualan tidak ditemukan.")

# Menu Utama
def menu():
    while True:
        print("\n=== Sistem Pengelolaan Toko Kelontong ===")
        print("1. Kelola Produk")
        print("2. Kelola Pelanggan")
        print("3. Kelola Penjualan")
        print("4. Laporan Penjualan")
        print("5. Backup Database")
        print("6. Restore Database")
        print("7. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            submenu_produk()
        elif pilihan == '2':
            submenu_pelanggan()
        elif pilihan == '3':
            submenu_penjualan()
        elif pilihan == '4':
            laporan_penjualan_harian()
        elif pilihan == '5':
            backup_database()
        elif pilihan == '6':
            restore_database()
        elif pilihan == '7':
            print("Terima kasih telah menggunakan aplikasi.")
            break
        else:
            print("Pilihan tidak valid.")

# Submenu Produk
def submenu_produk():
    while True:
        print("\n=== Kelola Produk ===")
        print("1. Tambah Produk")
        print("2. Lihat Produk")
        print("3. Edit Produk")
        print("4. Hapus Produk")
        print("5. Kembali ke Menu Utama")
        pilihan = input("Pilih menu: ")
        
        if pilihan == '1':
            tambah_produk()
        elif pilihan == '2':
            lihat_produk()
        elif pilihan == '3':
            edit_produk()
        elif pilihan == '4':
            hapus_produk()
        elif pilihan == '5':
            break
        else:
            print("Pilihan tidak valid.")

# Submenu Pelanggan
def submenu_pelanggan():
    while True:
        print("\n=== Kelola Pelanggan ===")
        print("1. Tambah Pelanggan")
        print("2. Lihat Pelanggan")
        print("3. Edit Pelanggan")
        print("4. Hapus Pelanggan")
        print("5. Kembali ke Menu Utama")
        pilihan = input("Pilih menu: ")
        
        if pilihan == '1':
            tambah_pelanggan()
        elif pilihan == '2':
            lihat_pelanggan()
        elif pilihan == '3':
            edit_pelanggan()
        elif pilihan == '4':
            hapus_pelanggan()
        elif pilihan == '5':
            break
        else:
            print("Pilihan tidak valid.")

# Submenu Penjualan
def submenu_penjualan():
    while True:
        print("\n=== Kelola Penjualan ===")
        print("1. Tambah Penjualan")
        print("2. Lihat Penjualan")
        print("3. Hapus Penjualan")
        print("4. Kembali ke Menu Utama")
        pilihan = input("Pilih menu: ")
        
        if pilihan == '1':
            tambah_penjualan()
        elif pilihan == '2':
            lihat_penjualan()
        elif pilihan == '3':
            hapus_penjualan()
        elif pilihan == '4':
            break
        else:
            print("Pilihan tidak valid.")

# Menjalankan Program
menu()