import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        # Coba koneksi ke TiDB Cloud Database
        connection = mysql.connector.connect(
            host='gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
            port=4000,
            user='3w7FvA6qK4YqS8b.root',
            password='LKSFCgi4QLf8GPUq',
            database='sistemkegiatan'
        )
        return connection
    except Error as e:
        # Fallback ke localhost jika offline / lokal
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='sistemkegiatan'
            )
            return connection
        except Error:
            print(f"Error saat koneksi ke MySQL: {e}")
            return None