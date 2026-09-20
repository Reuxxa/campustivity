import streamlit as st
import pandas as pd
import mysql.connector
import bcrypt
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from koneksi import connect_db
from datetime import date
import warnings
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")

def Admin():
    if "user" not in st.session_state or st.session_state.get("role") != "Admin":
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.warning("⚠️ Anda harus login sebagai Admin terlebih dahulu.")
        st.rerun()

    # ========================
    # STREAMLIT UI STARTS HERE
    # ========================

    # Sidebar menu lengkap
    menu = st.sidebar.selectbox("📋 Menu Admin", ["Dashboard", "Kelola Mahasiswa", "Kelola Pengelola", "Keluar"])

    # ----------------
    # 🔐 LOGIN
    # ----------------
    if menu == "Dashboard":
        st.title("📊 Dashboard Admin")
        st.success(f"Halo {st.session_state.user['username']} 👋")

    elif menu == "Kelola Mahasiswa":
        st.title("👨‍🎓 Kelola Mahasiswa")
        if "success_message" in st.session_state:
            st.success(st.session_state.success_message)
            del st.session_state["success_message"]  # hapus supaya tidak ditampilkan terus

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT nim, nama_mahasiswa, prodi, angkatan FROM mahasiswa")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        cursor.close()
        conn.close()

        # 🧾 Form Tambah Mahasiswa
        with st.expander("➕ Tambah Mahasiswa"):
            nim = st.text_input("NIM")
            nama = st.text_input("Nama Lengkap")
            prodi = st.text_input("Program Studi")
            angkatan = st.text_input("Angkatan")

            if st.button("Tambah"):
                if not all([nim, nama, prodi, angkatan]):
                    st.warning("⚠️ Harap isi semua field.")
                else:
                    default_password = "123456"
                    hashed = bcrypt.hashpw(default_password.encode(), bcrypt.gensalt()).decode()

                    conn = connect_db()
                    cursor = conn.cursor()
                    try:
                        cursor.execute(
                            "INSERT INTO mahasiswa (nim, nama_mahasiswa, prodi, angkatan, password) VALUES (%s, %s, %s, %s, %s)",
                            (nim, nama, prodi, angkatan, hashed)
                        )
                        conn.commit()
                        st.session_state["success_message"] = f"✅ Mahasiswa berhasil ditambahkan (password default: 123456)."
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Gagal: {e}")
                    finally:
                        cursor.close()
                        conn.close()

        # 📋 Tampilkan Mahasiswa
        st.subheader("📑 Daftar Mahasiswa")

        if not df.empty:
            header_cols = st.columns([1, 2, 2, 2, 1, 1])
            headers = ["NIM", "Nama", "Prodi", "Angkatan", "Edit", "Delete"]
            for col, header in zip(header_cols, headers):
                col.markdown(f"**{header}**")

            for idx, row in df.iterrows():
                cols = st.columns([1, 2, 2, 2, 1, 1])

                # ❌ NIM tidak bisa diedit
                cols[0].markdown(f"{row['nim']}")

                nama = cols[1].text_input("Nama Lengkap", value=row["nama_mahasiswa"], key=f"nama_{idx}", label_visibility="hidden")
                prodi = cols[2].text_input("Program Studi", value=row["prodi"], key=f"prodi_{idx}", label_visibility="hidden")
                angkatan = cols[3].text_input("Angkatan", value=row["angkatan"], key=f"angkatan_{idx}", label_visibility="hidden")


                # EDIT
                if cols[4].button("🔄", key=f"edit_{idx}"):
                    conn = connect_db()
                    cursor = conn.cursor()
                    try:
                        cursor.execute(
                            "UPDATE mahasiswa SET nama_mahasiswa=%s, prodi=%s, angkatan=%s WHERE nim=%s",
                            (nama, prodi, angkatan, row["nim"])
                        )
                        conn.commit()
                        st.success(f"✅ Data mahasiswa {row['nim']} berhasil diupdate.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Gagal update: {e}")
                    finally:
                        cursor.close()
                        conn.close()

                # DELETE
                if cols[5].button("🗑️", key=f"delete_{idx}"):
                    conn = connect_db()
                    cursor = conn.cursor()
                    try:
                        cursor.execute("DELETE FROM mahasiswa WHERE nim=%s", (row["nim"],))
                        conn.commit()
                        st.session_state["success_message"] = f"🗑️ Mahasiswa {row['nim']} berhasil dihapus."
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Gagal hapus: {e}")
                    finally:
                        cursor.close()
                        conn.close()
        else:
            st.info("❕ Belum ada data mahasiswa.")

    elif menu == "Kelola Pengelola":
        st.title("🧑‍💼 Kelola Pengelola")
        
        if "success_message" in st.session_state:
            st.success(st.session_state.success_message)
            del st.session_state["success_message"]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id_pengelola, username, bagian FROM pengelola")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        cursor.close()
        conn.close()

        # 🧾 Form Tambah Pengelola
        with st.expander("➕ Tambah Pengelola"):
            id_pengelola = st.text_input("ID Pengelola")
            username = st.text_input("Username")
            password = st.text_input("Password (default atau diatur manual)", value="123456", type="password")
            bagian = st.selectbox("Bagian", ["Olahraga", "Seni", "Akademik", "Teknologi"])

            if st.button("Tambah"):
                if not all([id_pengelola, username, password, bagian]):
                    st.warning("⚠️ Harap isi semua field.")
                else:
                    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

                    conn = connect_db()
                    cursor = conn.cursor()
                    try:
                        cursor.execute(
                            "INSERT INTO pengelola (id_pengelola, username, password, bagian) VALUES (%s, %s, %s, %s)",
                            (id_pengelola, username, hashed, bagian)
                        )
                        conn.commit()
                        st.session_state["success_message"] = "✅ Pengelola berhasil ditambahkan."
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Gagal: {e}")
                    finally:
                        cursor.close()
                        conn.close()

        # 📋 Tampilkan Pengelola
        st.subheader("📑 Daftar Pengelola")

        if not df.empty:
            header_cols = st.columns([2, 3, 2, 1, 1])
            headers = ["ID Pengelola", "Username", "Bagian", "Edit", "Delete"]
            for col, header in zip(header_cols, headers):
                col.markdown(f"**{header}**")

            bagian_list = ["Olahraga", "Seni", "Akademik", "Teknologi"]

            for idx, row in df.iterrows():
                cols = st.columns([2, 3, 2, 1, 1])
                
                cols[0].markdown(f"{row['id_pengelola']}")
                username = cols[1].text_input("Username", value=row["username"], key=f"username_{idx}", label_visibility="collapsed")

                selected_bagian = cols[2].selectbox(
                    "Bagian",
                    bagian_list,
                    index=bagian_list.index(row["bagian"]) if row["bagian"] in bagian_list else 0,
                    key=f"bagian_{idx}",
                    label_visibility="collapsed"
                )

                # EDIT
                if cols[3].button("🔄", key=f"edit_{idx}"):
                    conn = connect_db()
                    cursor = conn.cursor()
                    try:
                        cursor.execute(
                            "UPDATE pengelola SET username=%s, bagian=%s WHERE id_pengelola=%s",
                            (username, selected_bagian, row["id_pengelola"])
                        )
                        conn.commit()
                        st.session_state["success_message"] = f"✅ Data pengelola {row['id_pengelola']} berhasil diupdate."
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Gagal update: {e}")
                    finally:
                        cursor.close()
                        conn.close()

                # DELETE
                if cols[4].button("🗑️", key=f"delete_{idx}"):
                    conn = connect_db()
                    cursor = conn.cursor()
                    try:
                        cursor.execute("DELETE FROM pengelola WHERE id_pengelola=%s", (row["id_pengelola"],))
                        conn.commit()
                        st.session_state["success_message"] = f"🗑️ Pengelola {row['id_pengelola']} berhasil dihapus."
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Gagal hapus: {e}")
                    finally:
                        cursor.close()
                        conn.close()
        else:
            st.info("❕ Belum ada data pengelola.")


    elif menu == "Keluar":
        st.session_state.clear()
        st.success("✅ Berhasil logout.")
        st.rerun()