import streamlit as st
import mysql.connector
import bcrypt
from koneksi import connect_db

# ========================
# 🔐 Utility: Hash & Verify Password
# ========================
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# ========================
# 🔑 Login Function
# ========================
def login_user(username, password, role):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    if role == "Admin":
        query = "SELECT * FROM admin WHERE username=%s"
    elif role == "Pengelola":
        query = "SELECT * FROM pengelola WHERE username=%s"
    else:
        query = "SELECT * FROM mahasiswa WHERE nim=%s"

    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and verify_password(password, user["password"]):
        return user
    return None

# ========================
# 📝 Register Admin
# ========================
def register_admin(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM admin WHERE username=%s", (username,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return False, "❌ Username Admin sudah terdaftar."

    hashed = hash_password(password)
    try:
        cursor.execute("INSERT INTO admin (username, password) VALUES (%s, %s)", (username, hashed))
        conn.commit()
        return True, "✅ Registrasi Admin berhasil!"
    except Exception as e:
        return False, f"❌ Error: {e}"
    finally:
        cursor.close()
        conn.close()

# ========================
# 📝 Register Pengelola
# ========================
def register_pengelola(username, password, bagian):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pengelola WHERE username=%s", (username,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return False, "❌ Username Pengelola sudah terdaftar."

    hashed = hash_password(password)
    try:
        cursor.execute(
            "INSERT INTO pengelola (username, password, bagian) VALUES (%s, %s, %s)",
            (username, hashed, bagian)
        )
        conn.commit()
        return True, "✅ Registrasi Pengelola berhasil!"
    except Exception as e:
        return False, f"❌ Error: {e}"
    finally:
        cursor.close()
        conn.close()


# ========================
# 📝 Register Mahasiswa
# ========================
def register_mahasiswa(nim, nama, prodi, angkatan, password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM mahasiswa WHERE nim=%s", (nim,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return False, "❌ NIM sudah terdaftar."

    hashed = hash_password(password)
    try:
        cursor.execute(
            "INSERT INTO mahasiswa (nim, nama_mahasiswa, prodi, angkatan, password) VALUES (%s, %s, %s, %s, %s)",
            (nim, nama, prodi, angkatan, hashed)
        )
        conn.commit()
        return True, "✅ Registrasi Mahasiswa berhasil!"
    except Exception as e:
        return False, f"❌ Error: {e}"
    finally:
        cursor.close()
        conn.close()

# ========================
# STREAMLIT UI STARTS HERE
# ========================
if not st.session_state.get("logged_in"):
    st.title("🧑‍🎓 Sistem Kegiatan Mahasiswa")

    # Sidebar menu
    menu = st.sidebar.selectbox("📋 Menu", ["Login", "Register"])

    # Inisialisasi session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None

    # ----------------
    # 🔐 LOGIN
    # ----------------

    if menu == "Login" and not st.session_state.logged_in:
        st.subheader("Login")
        
        role = st.selectbox("Login sebagai:", ["Admin", "Pengelola", "Mahasiswa"])
        username = st.text_input("Username" if role != "Mahasiswa" else "NIM")
        password = st.text_input("Password", type="password")

        if st.button("🔓 Login"):
            user = login_user(username, password, role)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.session_state.role = role

                if role == "Admin":
                    from hal.Admin import Admin
                    st.session_state.admin_id = user["id_admin"]
                    st.session_state.page = "Admin"
                elif role == "Pengelola":
                    from hal.Pengelola import Pengelola
                    st.session_state.pengelola_id = user["id_pengelola"]
                    st.session_state.page = "Pengelola"
                else:
                    from hal.Mahasiswa import Mahasiswa
                    st.session_state.nim = user["nim"]
                    st.session_state.page = "Mahasiswa"

                st.rerun()
            else:
                st.session_state.login_failed = True

        # tampilkan pesan kalau login gagal
        if st.session_state.get("login_failed"):
            st.error("❌ Login gagal. Username/NIM atau password salah.")
            del st.session_state.login_failed



    # ----------------
    # 📝 REGISTRASI
    # ----------------

    elif menu == "Register":
        st.subheader("Registrasi")

        role = st.selectbox("Daftar sebagai:", ["Admin", "Pengelola", "Mahasiswa"])

        if role == "Admin":
            username = st.text_input("Username Admin")
            password = st.text_input("Password", type="password")

            if st.button("📥 Daftar", key="reg_admin"):
                if not username or not password:
                    st.warning("⚠️ Harap isi semua field.")
                else:
                    ok, msg = register_admin(username, password)
                    st.success(msg)

        elif role == "Pengelola":
            username = st.text_input("Username Pengelola")
            password = st.text_input("Password", type="password")
            bagian = st.selectbox("Bagian", ["Olahraga", "Seni", "Akademik", "Teknologi", "Kerohanian"])

            if st.button("📥 Daftar", key="reg_pengelola"):
                if not username or not password or not bagian:
                    st.warning("⚠️ Harap isi semua field.")
                else:
                    ok, msg = register_pengelola(username, password, bagian)
                    st.success(msg)

        elif role == "Mahasiswa":
            nim = st.text_input("NIM")
            nama = st.text_input("Nama Lengkap")
            prodi = st.text_input("Program Studi")
            angkatan = st.text_input("Angkatan (Contoh: 2022)", max_chars=4)
            password = st.text_input("Password", type="password")

            if st.button("📥 Daftar", key="reg_mahasiswa"):
                if not all([nim, nama, prodi, angkatan, password]):
                    st.warning("⚠️ Harap isi semua field.")
                else:
                    ok, msg = register_mahasiswa(nim, nama, prodi, angkatan, password)
                    st.success(msg)

    # ----------------
    # 👋 Setelah Login
    # ----------------
    if st.session_state.logged_in:
        user = st.session_state.user
        role = st.session_state.role

        if role == "Admin":
            greeting_name = user.get("username", "Admin")
        elif role == "Pengelola":
            greeting_name = user.get("username", "Pengelola")
        else:
            greeting_name = user.get("nama_mahasiswa", "Mahasiswa")

        st.write(f"Halo, {greeting_name} 👋")

        if role == "Admin":
            st.subheader("🛠️ Halaman Admin")
            st.write("Fitur: Kelola kegiatan, absensi, sertifikat, dll.")
        elif role == "Pengelola":
            st.subheader("📂 Halaman Pengelola")
            st.write("Fitur: Kelola kegiatan yang ditugaskan, lihat laporan, absensi, dll.")
        else:
            default_password = "123456"
            if bcrypt.checkpw(default_password.encode(), user["password"].encode()):
                st.session_state.force_change_password = True
            else:
                st.session_state.force_change_password = False

if st.session_state.get("logged_in"):
    if st.session_state.get("page") == "Admin":
        from hal.Admin import Admin
        Admin()
    elif st.session_state.get("page") == "Pengelola":
        from hal.Pengelola import Pengelola
        Pengelola()
    elif st.session_state.get("page") == "Mahasiswa":
        from hal.Mahasiswa import Mahasiswa
        Mahasiswa()