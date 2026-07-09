# ============================================================
# db_fxns2.py - DATABASE FUNCTIONS
# ============================================================
"""
File ini berisi fungsi-fungsi untuk manajemen database SQLite
pada aplikasi ToDo List.
"""

import sqlite3
from pathlib import Path

# ============================================================
# KONFIGURASI DATABASE
# ============================================================

# Dapatkan path absolut dari file ini
# CURRENT_DIR = Path(__file__).resolve().parent          # Utils/
# PROJECT_DIR = CURRENT_DIR.resolve().parent             # Projects_Streamlit/
# DB_DIR = PROJECT_DIR / "Database"                      # Projects_Streamlit/Database/
# DB_PATH = DB_DIR / "data2.db"                          # Projects_Streamlit/Database/data2.db
#"DB_Dir=path('Database/data2.db')

# Buat folder Database jika belum ada
#"DB_DIR.mkdir(parents=True, exist_ok=True)

# Koneksi ke database
#conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
#c = conn.cursor()

from pathlib import Path

# ✅ Cara 1: sederhana - relative path
DB_PATH = Path("data.db")

# ✅ Cara 2: Dari lokasi file ini (lebih aman)
# DB_PATH = Path(__file__).resolve().parent.parent / "Database" / "data2.db"

# Buat folder Database jika belum ada
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Koneksi ke database
conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
c = conn.cursor()


# ============================================================
# FUNGSI DATABASE
# ============================================================

def create_table():
    """Membuat tabel taskstable jika belum ada"""
    c.execute('CREATE TABLE IF NOT EXISTS taskstable(task TEXT, task_status TEXT, task_due_date DATE)')


def add_data(task, task_status, task_due_date):
    """
    Menambahkan data tugas baru (CREATE)
    
    Parameters:
    -----------
    task : str
        Nama tugas
    task_status : str
        Status tugas (ToDo/Doing/Done)
    task_due_date : date
        Tanggal deadline
    """
    c.execute('INSERT INTO taskstable(task, task_status, task_due_date) VALUES (?,?,?)', 
              (task, task_status, task_due_date))
    conn.commit()


def view_all_data():
    """
    Mengambil semua data tugas (READ)
    
    Returns:
    --------
    list : List of tuples (task, task_status, task_due_date)
    """
    c.execute('SELECT * FROM taskstable')
    data = c.fetchall()
    return data


def view_all_task_names():
    """
    Mengambil daftar tugas unik (untuk dropdown)
    
    Returns:
    --------
    list : List of tuples (task,)
    """
    c.execute('SELECT DISTINCT task FROM taskstable')
    data = c.fetchall()
    return data


def get_task(task):
    """
    Mengambil data tugas spesifik berdasarkan nama
    
    Parameters:
    -----------
    task : str
        Nama tugas yang dicari
    
    Returns:
    --------
    list : List of tuples dengan data tugas
    """
    c.execute('SELECT * FROM taskstable WHERE task=?', (task,))
    data = c.fetchall()
    return data


def get_task_by_status(task_status):
    """
    Mengambil data tugas berdasarkan status
    
    Parameters:
    -----------
    task_status : str
        Status tugas (ToDo/Doing/Done)
    
    Returns:
    --------
    list : List of tuples dengan data tugas
    """
    c.execute('SELECT * FROM taskstable WHERE task_status=?', (task_status,))
    data = c.fetchall()
    return data


def edit_task_data(new_task, new_task_status, new_task_date, 
                   task, task_status, task_due_date):
    """
    Mengupdate data tugas (UPDATE)
    
    Parameters:
    -----------
    new_task : str
        Task baru
    new_task_status : str
        Status baru
    new_task_date : date
        Tanggal baru
    task : str
        Task lama (untuk WHERE)
    task_status : str
        Status lama (untuk WHERE)
    task_due_date : date
        Tanggal lama (untuk WHERE)
    """
    c.execute("""UPDATE taskstable 
                 SET task=?, task_status=?, task_due_date=? 
                 WHERE task=? and task_status=? and task_due_date=?""", 
              (new_task, new_task_status, new_task_date, 
               task, task_status, task_due_date))
    conn.commit()
    data = c.fetchall()
    return data


def delete_data(task):
    """
    Menghapus data tugas (DELETE)
    
    Parameters:
    -----------
    task : str
        Nama tugas yang akan dihapus
    """
    c.execute('DELETE FROM taskstable WHERE task=?', (task,))
    conn.commit()


def get_task_count():
    """
    Mendapatkan jumlah tugas yang tersimpan
    
    Returns:
    --------
    int : Jumlah tugas
    """
    c.execute('SELECT COUNT(*) FROM taskstable')
    count = c.fetchone()[0]
    return count


def get_status_count(status):
    """
    Mendapatkan jumlah tugas berdasarkan status
    
    Parameters:
    -----------
    status : str
        Status tugas
    
    Returns:
    --------
    int : Jumlah tugas dengan status tersebut
    """
    c.execute('SELECT COUNT(*) FROM taskstable WHERE task_status=?', (status,))
    count = c.fetchone()[0]
    return count


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TESTING db_fxns2.py")
    print("=" * 60)
    
    print(f"\n📁 Database path: {DB_PATH}")
    print(f"📁 Database exists: {DB_PATH.exists()}")
    
    # Test create table
    print("\n1. Creating table...")
    create_table()
    print("✅ Table created/checked")
    
    # Test count
    count = get_task_count()
    print(f"Total tasks: {count}")
    
    print("\n✅ All tests completed!")