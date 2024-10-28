import csv
from datetime import datetime, timedelta
import os
import matplotlib.pyplot as plt

# Fungsi untuk mencatat data sampah
def catat_sampah(jenis_sampah, berat_sampah, status_sampah):
    jenis_sampah_valid = ["botol", "tutup botol", "kaleng", "botol kaca"]
    while jenis_sampah not in jenis_sampah_valid:
        print("Jenis sampah tidak valid!",)
        jenis_sampah = input("Masukkan jenis sampah: ")
    waktu_sekarang = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = [waktu_sekarang, jenis_sampah, berat_sampah, status_sampah]
    
    file_exists = os.path.isfile('data_sampah.csv') and os.path.getsize('data_sampah.csv') > 0
    with open('data_sampah.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Tanggal', 'Jenis Sampah', 'Berat (kg)', 'Status'])
        writer.writerow(data)
    
    print(f"Data sampah berhasil dicatat: {data}")

# Fungsi untuk melihat laporan harian
def lihat_laporan_harian():
    today = datetime.now().strftime('%Y-%m-%d')
    total_berat = 0
    jenis_sampah_count = {}
    print(f"Laporan Sampah Harian - {today}:")
    
    try:
        with open('data_sampah.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Lewati header
            for row in reader:
                if len(row) != 4:
                    continue
                tanggal, jenis, berat, status = row
                if today in tanggal:
                    print(f"Waktu: {tanggal}, Jenis: {jenis}, Berat: {berat} kg, Status: {status}")
                    total_berat += float(berat)
                    if jenis in jenis_sampah_count:
                        jenis_sampah_count[jenis] += float(berat)
                    else:
                        jenis_sampah_count[jenis] = float(berat)
    except FileNotFoundError:
        print("File 'data_sampah.csv' tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    print(f"Total sampah hari ini: {total_berat:.2f} kg")
    buat_grafik_harian(today)
    buat_pie_chart(jenis_sampah_count)

# Fungsi untuk melihat laporan mingguan
def lihat_laporan_mingguan():
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    total_berat = 0
    jenis_sampah_count = {}
    
    print(f"Laporan Sampah Mingguan - {start_of_week.strftime('%Y-%m-%d')} sampai {today.strftime('%Y-%m-%d')}:")
    
    try:
        with open('data_sampah.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Lewati header
            for row in reader:
                if len(row) != 4:
                    continue
                tanggal, jenis, berat, status = row
                tanggal_obj = datetime.strptime(tanggal, '%Y-%m-%d %H:%M:%S')
                if start_of_week <= tanggal_obj <= today:
                    print(f"Waktu: {tanggal}, Jenis: {jenis}, Berat: {berat} kg, Status: {status}")
                    total_berat += float(berat)
                    if jenis in jenis_sampah_count:
                        jenis_sampah_count[jenis] += float(berat)
                    else:
                        jenis_sampah_count[jenis] = float(berat)
    except FileNotFoundError:
        print("File 'data_sampah.csv' tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    print(f"Total sampah minggu ini: {total_berat:.2f} kg")
    buat_grafik_mingguan(start_of_week, today)
    buat_pie_chart(jenis_sampah_count)

# Fungsi untuk membuat grafik harian
def buat_grafik_harian(today):
    tanggal_list = []
    berat_list = []
    
    try:
        with open('data_sampah.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Lewati header
            for row in reader:
                if len(row) != 4:
                    continue
                tanggal, jenis, berat, status = row
                if today in tanggal:
                    tanggal_list.append(tanggal)
                    berat_list.append(float(berat))
        
        # Membuat grafik
        plt.figure(figsize=(10, 5))
        plt.plot(tanggal_list, berat_list, marker='o', color='b', linestyle='-', label='Berat Sampah Harian')
        plt.xlabel('Waktu')
        plt.ylabel('Berat Sampah (kg)')
        plt.title('Grafik Sampah Harian')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()
        plt.show()
    
    except FileNotFoundError:
        print("File 'data_sampah.csv' tidak ditemukan.")

# Fungsi untuk membuat grafik mingguan
def buat_grafik_mingguan(start_of_week, today):
    tanggal_list = []
    berat_list = []
    
    try:
        with open('data_sampah.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Lewati header
            for row in reader:
                if len(row) != 4:
                    continue
                tanggal, jenis, berat, status = row
                tanggal_obj = datetime.strptime(tanggal, '%Y-%m-%d %H:%M:%S')
                if start_of_week <= tanggal_obj <= today:
                    tanggal_list.append(tanggal)
                    berat_list.append(float(berat))
        
        # Membuat grafik
        plt.figure(figsize=(10, 5))
        plt.plot(tanggal_list, berat_list, marker='o', color='g', linestyle='-', label='Berat Sampah Mingguan')
        plt.xlabel('Waktu')
        plt.ylabel('Berat Sampah (kg)')
        plt.title('Grafik Sampah Mingguan')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()
        plt.show()

    except FileNotFoundError:
        print("File 'data_sampah.csv' tidak ditemukan.")

# Fungsi untuk membuat pie chart jenis sampah
def buat_pie_chart(jenis_sampah_count):
    labels = list(jenis_sampah_count.keys())
    sizes = list(jenis_sampah_count.values())
    
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1fclear%%', startangle=140)
    plt.title('Persentase Jenis Sampah')
    plt.show()

# hapus data
def hapus_data():
    konfirmasi = input("Apakah Anda yakin ingin menghapus semua data? (ya/tidak): ")
    if konfirmasi.lower() == 'ya':
        with open('data_sampah.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Tanggal', 'Jenis Sampah', 'Berat (kg)', 'Status'])
        print("Semua data sampah telah dihapus.")
    else:
        print("Penghapusan data dibatalkan.")

# Menu utama
def menu():
    while True:
        print("\n=== Pencatatan Sampah Harian ===")
        print("1. Catat sampah")
        print("2. Lihat laporan harian")
        print("3. Lihat laporan mingguan")
        print("4. Hapus semua data")
        print("5. Keluar")
        
        pilihan = input("Pilih opsi (1/2/3/4/5): ")
        
        if pilihan == '1':
            try:
                jenis = input("Masukkan jenis sampah:  ")
                berat = float(input("Masukkan berat sampah (kg): "))
                status = input("Masukkan status sampah (misal: bersih, kotor): ")
                catat_sampah(jenis, berat, status)
            except ValueError:
                print("Masukkan angka yang valid untuk berat sampah.")
        elif pilihan == '2':
            lihat_laporan_harian()
        elif pilihan == '3':
            lihat_laporan_mingguan()
        elif pilihan == '4':
            hapus_data()
        elif pilihan == '5':
            print("Terima kasih!")
            break
        else:
            print("Opsi tidak valid, silakan coba lagi.")

# Memulai program
if __name__ == "__main__":
    menu()
