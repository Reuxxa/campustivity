import streamlit as st
import pandas as pd
import mysql.connector
import bcrypt
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from koneksi import connect_db
import warnings
import datetime

warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")

def Mahasiswa():
    if "user" not in st.session_state or st.session_state.get("role") != "Mahasiswa":
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.warning("⚠️ Anda harus login sebagai Mahasiswa terlebih dahulu.")
        st.rerun()

    def hash_password(password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    if st.session_state.get("force_change_password"):
        st.warning("⚠️ Password Anda masih default. Demi keamanan, silakan ubah sekarang.")

        with st.expander("🔒 Ubah Password"):
            new_pass = st.text_input("Password Baru", type="password")
            confirm_pass = st.text_input("Konfirmasi Password", type="password")

            if st.button("Ubah Password"):
                if not new_pass or not confirm_pass:
                    st.error("❌ Harap isi semua kolom.")
                elif new_pass != confirm_pass:
                    st.error("❌ Password tidak cocok.")
                else:
                    hashed = hash_password(new_pass)
                    conn = connect_db()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE mahasiswa SET password=%s WHERE nim=%s", (hashed, st.session_state.user["nim"]))
                    conn.commit()
                    cursor.close()
                    conn.close()

                    st.session_state.force_change_password = False
                    st.success("✅ Password berhasil diubah.")
                    st.rerun()


    # ========================
    # STREAMLIT UI STARTS HERE
    # ========================

    # Sidebar menu lengkap
    menu = st.sidebar.selectbox("📋 Menu Mahasiswa", ["Dashboard", "Pendaftaran Kegiatan", "Riwayat Kegiatan", "Absensi", "Sertifikat", "Notifikasi", "Keluar"])

    # ----------------
    # 🔐 LOGIN
    # ----------------
    if menu == "Dashboard":
        st.title("📊 Dashboard Mahasiswa")
        st.success(f"Halo {st.session_state.user['nama_mahasiswa']} 👋")
        st.write("Selamat datang di sistem kegiatan mahasiswa. Silakan jelajahi fitur yang tersedia.")

    elif menu == "Pendaftaran Kegiatan":
        st.title("📝 Pendaftaran Kegiatan")
        if "success_message" in st.session_state:
            st.success(st.session_state.success_message)
            del st.session_state["success_message"]

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT id_kegiatan, judul_kegiatan, waktu, tempat, deskripsi FROM kegiatan")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)

        nim = st.session_state.user["nim"]

        st.subheader("📋 Daftar Kegiatan Tersedia")

        if not df.empty:
            header_cols = st.columns([1, 2, 2, 2, 3, 3, 2])
            headers = ["ID", "Judul", "Waktu", "Tempat", "Deskripsi","Status","Aksi"]
            for col, header in zip(header_cols, headers):
                col.markdown(f"**{header}**")

            for idx, row in df.iterrows():
                cols = st.columns([1, 2, 2, 2, 3, 3, 2])
                cols[0].markdown(f"{row['id_kegiatan']}")
                cols[1].markdown(row['judul_kegiatan'])
                cols[2].markdown(row['waktu'].strftime("%d-%m-%Y %H:%M"))
                cols[3].markdown(row['tempat'])
                cols[4].markdown(row['deskripsi'])

                cursor.execute("SELECT COUNT(*) FROM pendaftaran WHERE nim=%s AND id_kegiatan=%s", (nim, row['id_kegiatan']))
                sudah_daftar = cursor.fetchone()[0] > 0

                # Status kolom
                with cols[5]:
                    if sudah_daftar:
                        st.markdown("<span style='color: green;'>Telah Mendaftar</span>", unsafe_allow_html=True)
                    else:
                        st.markdown("<span style='color: red;'>Belum Mendaftar</span>", unsafe_allow_html=True)

                # Tombol aksi
                with cols[6]:
                    if sudah_daftar:
                        if st.button("Batal", key=f"batal_{row['id_kegiatan']}"):
                            try:
                                cursor.execute("DELETE FROM pendaftaran WHERE nim=%s AND id_kegiatan=%s", (nim, row['id_kegiatan']))
                                conn.commit()
                                st.session_state["success_message"] = f"🗑️ Pendaftaran kegiatan {row['judul_kegiatan']} dibatalkan."
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Gagal membatalkan pendaftaran: {e}")
                    else:
                        if st.button("Daftar", key=f"daftar_{row['id_kegiatan']}"):
                            try:
                                tgl_daftar = datetime.date.today()
                                status = ""
                                cursor.execute(
                                    "INSERT INTO pendaftaran (nim, id_kegiatan, tgl_pendaftaran, status) VALUES (%s, %s, %s, %s)",
                                    (nim, row["id_kegiatan"], tgl_daftar, status)
                                )
                                conn.commit()
                                st.session_state["success_message"] = f"✅ Berhasil mendaftar kegiatan {row['judul_kegiatan']}"
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Gagal mendaftar: {e}")

        else:
            st.info("📭 Belum ada kegiatan tersedia.")

        cursor.close()
        conn.close()


    elif menu == "Riwayat Kegiatan":
        st.title("📜 Riwayat Kegiatan")

        conn = connect_db()
        cursor = conn.cursor()

        nim = st.session_state.user["nim"]

        cursor.execute("""
            SELECT k.id_kegiatan, k.judul_kegiatan, k.waktu, k.tempat, k.deskripsi, p.status, p.tgl_pendaftaran
            FROM pendaftaran p
            JOIN kegiatan k ON p.id_kegiatan = k.id_kegiatan
            WHERE p.nim = %s
            ORDER BY p.tgl_pendaftaran DESC
        """, (nim,))
        rows = cursor.fetchall()
        columns = ["ID", "Judul", "Waktu", "Tempat", "Deskripsi", "Status", "Tgl Daftar"]
        df = pd.DataFrame(rows, columns=columns)

        st.subheader("📋 Daftar Riwayat Kegiatan")

        if not df.empty:
            header_cols = st.columns([1, 2, 2, 2, 3, 2, 2])
            for col, header in zip(header_cols, columns):
                col.markdown(f"**{header}**")

            for idx, row in df.iterrows():
                cols = st.columns([1, 2, 2, 2, 3, 2, 2])
                cols[0].markdown(str(row["ID"]))
                cols[1].markdown(row["Judul"])
                cols[2].markdown(row["Waktu"].strftime("%d-%m-%Y %H:%M"))
                cols[3].markdown(row["Tempat"])
                cols[4].markdown(row["Deskripsi"])
                cols[5].markdown(f"`{row['Status']}`")
                cols[6].markdown(row["Tgl Daftar"].strftime("%d-%m-%Y"))
        else:
            st.info("📭 Belum ada riwayat kegiatan.")

        cursor.close()
        conn.close()

    elif menu == "Absensi":
        st.title("📶 Riwayat Absensi Kegiatan")

        conn = connect_db()
        cursor = conn.cursor()

        nim = st.session_state.user["nim"]

        cursor.execute("""
            SELECT 
                k.id_kegiatan,
                k.judul_kegiatan,
                a.tgl_kehadiran,
                a.status_kehadiran
            FROM absensi a
            JOIN pendaftaran p ON a.id_pendaftaran = p.id_pendaftaran
            JOIN kegiatan k ON p.id_kegiatan = k.id_kegiatan
            WHERE p.nim = %s
            ORDER BY a.tgl_kehadiran DESC
        """, (nim,))
        rows = cursor.fetchall()
        columns = ["ID Kegiatan", "Judul Kegiatan", "Tanggal", "Status"]
        df = pd.DataFrame(rows, columns=columns)

        st.subheader("📋 Daftar Absensi")

        if not df.empty:
            header_cols = st.columns([1.5, 2.5, 2, 1.5, 3])
            for col, header in zip(header_cols, columns):
                col.markdown(f"**{header}**")

            for _, row in df.iterrows():
                cols = st.columns([1.5, 2.5, 2, 1.5, 3])
                cols[0].markdown(str(row["ID Kegiatan"]))
                cols[1].markdown(row["Judul Kegiatan"])
                cols[2].markdown(row["Tanggal"].strftime("%d-%m-%Y"))
                cols[3].markdown(f"`{row['Status']}`")
        else:
            st.info("📭 Belum ada data absensi.")

        cursor.close()
        conn.close()

    elif menu == "Sertifikat":
        st.title("🎓 Riwayat Sertifikat Kegiatan")

        conn = connect_db()
        cursor = conn.cursor()

        nim = st.session_state.user["nim"]

        cursor.execute("""
            SELECT 
                s.id_sertifikat,
                k.judul_kegiatan,
                s.tgl_terbit,
                s.status
            FROM sertifikat s
            JOIN pendaftaran p ON s.id_pendaftaran = p.id_pendaftaran
            JOIN kegiatan k ON p.id_kegiatan = k.id_kegiatan
            WHERE p.nim = %s
            ORDER BY s.tgl_terbit DESC
        """, (nim,))

        rows = cursor.fetchall()

        columns = ["ID Sertifikat", "Judul Kegiatan", "Tanggal Terbit", "Status"]
        df = pd.DataFrame(rows, columns=columns)

        st.subheader("📋 Daftar Sertifikat")

        if not df.empty:
            header_cols = st.columns([1, 3, 2, 2])
            for col, header in zip(header_cols, columns):
                col.markdown(f"**{header}**")

            for _, row in df.iterrows():
                cols = st.columns([1, 3, 2, 2])
                cols[0].markdown(str(row["ID Sertifikat"]))
                cols[1].markdown(row["Judul Kegiatan"])
                cols[2].markdown(row["Tanggal Terbit"].strftime("%d-%m-%Y") if pd.notnull(row["Tanggal Terbit"]) else "-")
                cols[3].markdown(f"`{row['Status']}`" if row["Status"] else "-")
        else:
            st.info("📭 Belum ada data sertifikat.")

        cursor.close()
        conn.close()

    elif menu == "Notifikasi":
        st.title("🔔 Notifikasi")

        # Gunakan session_state.user["nim"] sesuai struktur login kamu
        nim_mahasiswa = st.session_state.user["nim"]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_notifikasi, judul, pesan, tanggal
            FROM notifikasi
            WHERE nim = %s
            ORDER BY tanggal DESC
            LIMIT 20
        """, (nim_mahasiswa,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if rows:
            for notif in rows:
                st.markdown(f"### {notif[1]}")  # judul
                st.markdown(f"_{notif[3].strftime('%Y-%m-%d')}_")  # tanggal
                st.write(notif[2])  # pesan
                st.markdown("---")
        else:
            st.info("📭 Belum ada notifikasi.")

    elif menu == "Keluar":
        st.session_state.clear()
        st.success("✅ Berhasil logout.")
        st.rerun()