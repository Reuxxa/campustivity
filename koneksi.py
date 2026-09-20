import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',       
            user='root',            
            password='',            
            database='sistemkegiatan'  
        )
        return connection
    except Error as e:
        print(f"Error saat koneksi ke MySQL: {e}")
        return None