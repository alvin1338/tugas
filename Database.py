import sqlite3

def home():
    print("==" * 8)
    print("1. Matkul")
    print("2. Kelas")
    pilihan = int(input("Masukkan pilihan: "))
    print("==" * 8)

    if pilihan == 1:
        halaman_matkul () 
    elif pilihan == 2:
        halaman_kelas ()
    else:
        print("Tidak ada pilihan")
        home()  

def tambah_matkul():
    conn = sqlite3.connect('matkul.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS matkul
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, nama_matkul TEXT, nama_dosen TEXT)''')

  
    nama_matkul = input("Masukkan nama matkul: ")
    nama_dosen  = input("Masukkan nama dosen: ")

    cursor.execute("INSERT INTO matkul (nama_matkul, nama_dosen) VALUES (?, ?)", (nama_matkul, nama_dosen))

    conn.commit()
    conn.close()

    halaman_matkul()

def lihat_matkul():
    conn = sqlite3.connect('matkul.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM matkul")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()

    halaman_matkul()

def edit_matkul():
    conn = sqlite3.connect('matkul.db')
    cursor = conn.cursor()

    print("Data sebelum pembaruan:")
    cursor.execute("SELECT * FROM matkul")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    id_matkul = int(input("Masukkan ID Matkul yang ingin di edit: "))
    nama_matkul_baru = input("Masukkan Nama Matkul baru: ")
    nama_dosen_baru = input("Masukkan Nama Dosen baru: ")

    cursor.execute("UPDATE matkul SET nama_matkul = ?, nama_dosen = ? WHERE id = ?", 
                   (nama_matkul_baru, nama_dosen_baru, id_matkul))

    conn.commit()
    conn.close()

    print("\nData setelah pembaruan:")
    lihat_matkul()

def hapus_matkul():
    conn = sqlite3.connect('matkul.db')
    cursor = conn.cursor()

    print("Data sebelum penghapusan:")
    cursor.execute("SELECT * FROM matkul")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    id_matkul = int(input("Masukkan ID Matkul yang ingin dihapus: "))

    cursor.execute("DELETE FROM matkul WHERE id = ?", (id_matkul,))

    conn.commit()
    conn.close()

    print("\nData setelah penghapusan:")
    lihat_matkul()

def halaman_matkul():
    while True:
        print("Halaman Matkul")
        print("1. Tambah data matkul baru")
        print("2. Lihat data matkul")
        print("3. Edit data matkul")
        print("4. Hapus data matkul")
        print("5. Menu Utama")
        pilihan = int(input("Masukkan pilihan: "))
        
        if pilihan == 1:
            tambah_matkul()
        elif pilihan == 2:
            lihat_matkul()
        elif pilihan == 3:
            edit_matkul()
        elif pilihan == 4:
            hapus_matkul()
        elif pilihan == 5:
            home()  
            break
        else:
            print("Pilihan tidak valid, coba lagi.")

def tambah_kelas():
    conn = sqlite3.connect('kelas.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS kelas
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, kode_kelas TEXT, ruang_kelas TEXT)''')

    kode_kelas = input("Masukkan kode kelas: ")
    ruang_kelas  = input("Masukkan ruang kelas: ")

    cursor.execute("INSERT INTO kelas (kode_kelas, ruang_kelas) VALUES (?, ?)", (kode_kelas, ruang_kelas))

    conn.commit()
    conn.close()

    halaman_kelas()

def lihat_kelas():
    conn = sqlite3.connect('kelas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kelas")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()

    halaman_kelas()

def edit_kelas():
    conn = sqlite3.connect('kelas.db')
    cursor = conn.cursor()
    print("Data sebelum pembaruan:")
    cursor.execute("SELECT * FROM kelas")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    id_kelas = int(input("Masukkan ID kelas yang ingin di edit: "))
    kode_kelas_baru = input("Masukkan Nama kode kelas baru: ")
    ruang_kelas_baru = input("Masukkan Nama ruang kelas baru: ")

    cursor.execute("UPDATE kelas SET kode_kelas = ?, ruang_kelas = ? WHERE id = ?", 
                   (kode_kelas_baru, ruang_kelas_baru, id_kelas))
    conn.commit()
    conn.close()

    print("\nData setelah pembaruan:")
    lihat_kelas()

def hapus_kelas():
    conn = sqlite3.connect('kelas.db')
    cursor = conn.cursor()

    print("kode sebelum penghapusan:")
    cursor.execute("SELECT * FROM kelas")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    
    id_kelas = int(input("Masukkan ID kelas yang ingin dihapus: "))
    cursor.execute("DELETE FROM kelas WHERE id = ?", (id_kelas,))
    conn.commit()
    conn.close()

    print("\nData setelah penghapusan:")
    lihat_kelas()
 
def halaman_kelas():
    while True:
        print("Halaman kelas")
        print("1. Tambah kode kelas baru")
        print("2. Lihat kode kelas")
        print("3. Edit kode kelas")
        print("4. Hapus kode kelas")
        print("5. Menu Utama")
        pilihan = int(input("Masukkan pilihan: "))
        
        if pilihan == 1:
            tambah_kelas()
        elif pilihan == 2:
            lihat_kelas()
        elif pilihan == 3:
            edit_kelas()
        elif pilihan == 4:
            hapus_kelas()
        elif pilihan == 5:
            home() 
            break
        else:
            print("Pilihan tidak valid, coba lagi.")

home()