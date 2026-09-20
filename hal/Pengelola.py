import streamlit as st
import pandas as pd
import mysql.connector
import bcrypt
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from koneksi import connect_db
from datetime import date
import warnings
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")

def Pengelola():
    if "user" not in st.session_state or st.session_state.get("role") != "Pengelola":
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.warning("⚠️ Anda harus login sebagai Pengelola terlebih dahulu.")
        st.rerun()

    # ========================
    # STREAMLIT UI STARTS HERE
    # ========================

    # Sidebar menu lengkap
    menu = st.sidebar.selectbox("📋 Menu Pengelola", ["Dashboard", "Kelola Kegiatan", "Kelola Pendaftaran", "Kelola Absensi", "Kelola Sertifikat", "Kelola Notifikasi", "Keluar"])

    # ----------------
    # 🔐 LOGIN
    # ----------------
    if menu == "Dashboard":
        st.title("📊 Dashboard pengelola")
        st.success(f"Halo {st.session_state.user['username']} 👋")

    elif menu == "Kelola Kegiatan":
        st.title("👨‍🎓 Kelola Kegiatan")
        
        if "success_message" in st.session_state:
            st.success(st.session_state.success_message)
            del st.session_state["success_message"]  

        # 🔄 Ambil Data Kegiatan untuk Pengelola yang Login
        id_pengelola = st.session_state.user["id_pengelola"]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_kegiatan, judul_kegiatan, waktu, tempat, deskripsi
            FROM kegiatan
            WHERE id_pengelola = %s
        """, (id_pengelola,))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        cursor.close()
        conn.close()


        # 🧾 Form Tambah Kegiatan
        with st.expander("➕ Tambah Kegiatan"):
            judulK = st.text_input("Judul Kegiatan")
            waktu = st.date_input("Waktu")
            tempat = st.text_input("Tempat")
            deskripsi = st.text_input("Deskripsi")

            if st.button("Tambah"):
                if not all([judulK, waktu, tempat, deskripsi]):
                    st.warning("⚠️ Harap isi semua field.")
                else:
                    id_pengelola = st.session_state.user["id_pengelola"]  # ambil dari session

                    conn = connect_db()
                    cursor = conn.cursor()
                    try:
                        cursor.execute(
                            "INSERT INTO kegiatan (judul_kegiatan, waktu, tempat, deskripsi, id_pengelola) VALUES (%s, %s, %s, %s, %s)",
                            (judulK, waktu, tempat, deskripsi, id_pengelola)
                        )

                        # Ambil semua mahasiswa untuk dikirimi notifikasi
                        cursor.execute("SELECT nim FROM mahasiswa")
                        mahasiswa_list = cursor.fetchall()

                        judul_notif = "Kegiatan Baru"
                        pesan_notif = f"Ada kegiatan baru: {judulK}. Yuk cek dan daftar sekarang!"
                        tanggal_notif = date.today()

                        # Masukkan notifikasi untuk tiap mahasiswa
                        for (nim,) in mahasiswa_list:
                            cursor.execute(
                                "INSERT INTO notifikasi (nim, judul, pesan, tanggal) VALUES (%s, %s, %s, %s)",
                                (nim, judul_notif, pesan_notif, tanggal_notif)
                            )


                        conn.commit()
                        st.success("✅ Kegiatan berhasil ditambahkan.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Gagal: {e}")
                    finally:
                        cursor.close()
                        conn.close()

        # 📋 Tampilkan Kegiatan
        st.subheader("📑 Daftar Kegiatan")

        if not df.empty:
            header_cols = st.columns([1, 2, 2, 2, 2, 1, 1])
            headers = ["ID", "Judul Kegiatan", "Waktu", "Tempat", "Deskripsi", "Edit", "Delete"]
            for col, header in zip(header_cols, headers):
                col.markdown(f"**{header}**")

            for idx, row in df.iterrows():
                cols = st.columns([1, 2, 2, 2, 2, 1, 1])

                # ❌ ID tidak bisa diedit
                cols[0].markdown(f"{row['id_kegiatan']}")

                judulK = cols[1].text_input("Judul Kegiatan", value=row["judul_kegiatan"], key=f"judulK_{idx}", label_visibility="collapsed")
                waktu = cols[2].text_input("Waktu", value=str(row["waktu"]), key=f"waktu_{idx}", label_visibility="collapsed")
                tempat = cols[3].text_input("Tempat", value=row["tempat"], key=f"tempat_{idx}", label_visibility="collapsed")
                deskripsi = cols[4].text_input("Deskripsi", value=row["deskripsi"], key=f"deskripsi_{idx}", label_visibility="collapsed")

                # ✅ EDIT
                if cols[5].button("🔄", key=f"edit_{idx}"):
                    conn = connect_db()
                    cursor = conn.cursor()
                    try:
                        cursor.execute(
                            "UPDATE kegiatan SET judul_kegiatan=%s, waktu=%s, tempat=%s, deskripsi=%s WHERE id_kegiatan=%s",
                            (judulK, waktu, tempat, deskripsi, row["id_kegiatan"])
                        )
                        conn.commit()
                        st.session_state["success_message"] = f"✅ Data kegiatan berhasil diupdate."
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Gagal update: {e}")
                    finally:
                        cursor.close()
                        conn.close()

                # ✅ DELETE
                if cols[6].button("🗑️", key=f"delete_{idx}"):
                    conn = connect_db()
                    cursor = conn.cursor()
                    try:
                        cursor.execute("DELETE FROM kegiatan WHERE id_kegiatan=%s", (row["id_kegiatan"],))
                        conn.commit()
                        st.session_state["success_message"] = f"✅ Data kegiatan berhasil dihapus."
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Gagal hapus: {e}")
                    finally:
                        cursor.close()
                        conn.close()

        else:
            st.info("❕ Belum ada data kegiatan.")

    elif menu == "Kelola Pendaftaran":
        st.title("📝 Kelola Pendaftaran Kegiatan")
        
        if "success_message" in st.session_state:
            st.success(st.session_state.success_message)
            del st.session_state["success_message"]  

        # 🔄 Ambil Data Pendaftaran
        conn = connect_db()
        cursor = conn.cursor()
        query = """
            SELECT p.id_pendaftaran, m.nama_mahasiswa, k.judul_kegiatan, p.tgl_pendaftaran, p.status
            FROM pendaftaran p
            JOIN mahasiswa m ON p.nim = m.nim
            JOIN kegiatan k ON p.id_kegiatan = k.id_kegiatan
            WHERE k.id_pengelola = %s
        """
        cursor.execute(query, (st.session_state.user["id_pengelola"],))

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        cursor.close()
        conn.close()

        st.subheader("📋 Daftar Pendaftaran")

        if not df.empty:
            header_cols = st.columns([1, 2, 2, 2, 2, 1, 1])
            headers = ["ID", "Nama Mahasiswa", "Kegiatan", "Tgl Daftar", "Status", "Edit", "Hapus"]
            for col, header in zip(header_cols, headers):
                col.markdown(f"**{header}**")

            status_list = ["pending", "terdaftar", "diterima", "ditolak"]

            for idx, row in df.iterrows():
                cols = st.columns([1, 2, 2, 2, 2, 1, 1])
                cols[0].markdown(f"{row['id_pendaftaran']}")
                cols[1].markdown(f"{row['nama_mahasiswa']}")
                cols[2].markdown(f"{row['judul_kegiatan']}")
                cols[3].markdown(str(row['tgl_pendaftaran']))

                # Aman kalau status di DB beda atau baru
                try:
                    selected_index = status_list.index(row["status"].lower())
                except ValueError:
                    selected_index = 0

                status = cols[4].selectbox(
                    "Status",
                    status_list,
                    index=selected_index,
                    key=f"status_{idx}",
                    label_visibility="collapsed"
                )

                # Tombol edit
                if cols[5].button("🔄", key=f"edit_{idx}"):
                    conn = connect_db()
                    cursor = conn.cursor()
                    try:
                        cursor.execute(
                            "UPDATE pendaftaran SET status=%s WHERE id_pendaftaran=%s",
                            (status, row["id_pendaftaran"])
                        )
                        conn.commit()
                        st.session_state["success_message"] = f"Status pendaftaran berhasil diupdate."
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal update: {e}")
                    finally:
                        cursor.close()
                        conn.close()

                # Tombol delete
                if cols[6].button("🗑️", key=f"delete_{idx}"):
                    conn = connect_db()
                    cursor = conn.cursor()
                    try:
                        cursor.execute("DELETE FROM pendaftaran WHERE id_pendaftaran=%s", (row["id_pendaftaran"],))
                        conn.commit()
                        st.session_state["success_message"] = f"Pendaftaran berhasil dihapus."
                        st.success(f"Pendaftaran berhasil dihapus.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal hapus: {e}")
                    finally:
                        cursor.close()
                        conn.close()

        else:
            st.info("📭 Belum ada data pendaftaran.")

    elif menu == "Kelola Absensi":
        st.title("🗓️ Kelola Absensi Kegiatan")
        if "success_message" in st.session_state:
            st.success(st.session_state.success_message)
            del st.session_state["success_message"]

        conn = connect_db()
        cursor = conn.cursor()
        query = """
            SELECT p.id_pendaftaran, m.nama_mahasiswa, k.judul_kegiatan, 
                IFNULL(a.status_kehadiran, 'belum absen') AS status_kehadiran,
                IFNULL(a.id_absensi, 0) AS id_absensi
            FROM pendaftaran p
            JOIN mahasiswa m ON p.nim = m.nim
            JOIN kegiatan k ON p.id_kegiatan = k.id_kegiatan
            LEFT JOIN absensi a ON p.id_pendaftaran = a.id_pendaftaran
            WHERE k.id_pengelola = %s
            ORDER BY k.judul_kegiatan, m.nama_mahasiswa
        """
        cursor.execute(query, (st.session_state.user["id_pengelola"],))

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        cursor.close()
        conn.close()

        st.subheader("📋 Daftar Absensi")

        if not df.empty:
            header_cols = st.columns([1, 3, 3, 2, 1])
            headers = ["ID", "Nama Mahasiswa", "Kegiatan", "Status Absensi", "Simpan"]
            for col, header in zip(header_cols, headers):
                col.markdown(f"**{header}**")

            status_list = ["hadir", "izin", "sakit", "alfa", "belum absen"]

            for idx, row in df.iterrows():
                cols = st.columns([1, 3, 3, 2, 1])
                cols[0].markdown(f"{row['id_pendaftaran']}")
                cols[1].markdown(row['nama_mahasiswa'])
                cols[2].markdown(row['judul_kegiatan'])

                # Aman kalau status_absensi tidak ada di list
                try:
                    selected_index = status_list.index(row["status_kehadiran"].lower())
                except ValueError:
                    selected_index = status_list.index("belum absen")

                status = cols[3].selectbox(
                    "Status Absensi",
                    status_list,
                    index=selected_index,
                    key=f"status_absen_{idx}",
                    label_visibility="collapsed" 
                )

                if cols[4].button("💾", key=f"simpan_absen_{idx}"):
                    conn = connect_db()
                    cursor = conn.cursor()
                    try:
                        if row['id_absensi'] == 0:
                            # Insert baru
                            cursor.execute(
                                """
                                INSERT INTO absensi (id_pendaftaran, tgl_kehadiran, status_kehadiran, id_pengelola)
                                VALUES (%s, CURDATE(), %s, %s)
                                """,
                                (row['id_pendaftaran'], status, st.session_state.pengelola_id)
                            )
                        else:
                            # Update yang sudah ada
                            cursor.execute(
                                """
                                UPDATE absensi
                                SET status_kehadiran=%s, tgl_kehadiran=CURDATE(), id_pengelola=%s
                                WHERE id_absensi=%s
                                """,
                                (status, st.session_state.pengelola_id, row['id_absensi'])
                            )
                        conn.commit()
                        st.session_state["success_message"] = f"Absensi untuk {row['nama_mahasiswa']} berhasil disimpan."
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal simpan absensi: {e}")
                    finally:
                        cursor.close()
                        conn.close()

        else:
            st.info("📭 Belum ada data absensi.")

    elif menu == "Kelola Sertifikat":
        st.title("🎓 Kelola Sertifikat")

        if "success_message" in st.session_state:
            st.success(st.session_state.success_message)
            del st.session_state["success_message"]

        # Ambil data sertifikat
        conn = connect_db()
        cursor = conn.cursor()
        query = """
            SELECT s.id_sertifikat, s.id_pendaftaran, m.nama_mahasiswa, k.judul_kegiatan, s.tgl_terbit, s.status
            FROM sertifikat s
            JOIN pendaftaran p ON s.id_pendaftaran = p.id_pendaftaran
            JOIN mahasiswa m ON p.nim = m.nim
            JOIN kegiatan k ON p.id_kegiatan = k.id_kegiatan
            WHERE k.id_pengelola = %s
        """
        cursor.execute(query, (st.session_state.user["id_pengelola"],))

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        cursor.close()
        conn.close()

        # Form Tambah Sertifikat
        with st.expander("➕ Tambah Sertifikat"):
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id_pendaftaran, m.nama_mahasiswa, k.judul_kegiatan 
                FROM pendaftaran p
                JOIN mahasiswa m ON p.nim = m.nim
                JOIN kegiatan k ON p.id_kegiatan = k.id_kegiatan
            """)
            daftar_pendaftaran = cursor.fetchall()
            cursor.close()
            conn.close()

            pilihan = [f"{row[0]} - {row[1]} - {row[2]}" for row in daftar_pendaftaran]

            if pilihan:
                selected = st.selectbox("Pilih Pendaftaran", ["-- Pilih Pendaftaran --"] + pilihan)

                if selected != "-- Pilih Pendaftaran --":
                    selected_id = int(selected.split(" - ")[0])
                    tgl_terbit = st.date_input("Tanggal Terbit", value=date.today())
                    status = st.selectbox("Status", ["Terbit", "Belum Terbit"])

                    if st.button("Tambah Sertifikat"):
                        conn = connect_db()
                        cursor = conn.cursor()
                        try:
                            cursor.execute("""
                                INSERT INTO sertifikat (id_pendaftaran, tgl_terbit, status)
                                VALUES (%s, %s, %s)
                            """, (selected_id, tgl_terbit, status))
                            conn.commit()
                            st.success("✅ Sertifikat berhasil ditambahkan.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Gagal: {e}")
                        finally:
                            cursor.close()
                            conn.close()
                else:
                    st.info("ℹ️ Silakan pilih pendaftaran terlebih dahulu.")
            else:
                st.warning("⚠️ Belum ada mahasiswa yang mendaftar kegiatan.")


        # Tampilkan Sertifikat
        st.subheader("📜 Daftar Sertifikat")

        if not df.empty:
            header_cols = st.columns([1, 2, 2, 2, 2, 1, 1])
            headers = ["ID", "Mahasiswa", "Kegiatan", "Tanggal Terbit", "Status", "Edit", "Delete"]
            for col, header in zip(header_cols, headers):
                col.markdown(f"**{header}**")

            for idx, row in df.iterrows():
                cols = st.columns([1, 2, 2, 2, 2, 1, 1])
                cols[0].markdown(f"{row['id_sertifikat']}")
                cols[1].markdown(row['nama_mahasiswa'])
                cols[2].markdown(row['judul_kegiatan'])

                tgl_terbit = cols[3].text_input("Tanggal", value=str(row["tgl_terbit"]), key=f"tgl_{idx}", label_visibility="collapsed")
                status = cols[4].selectbox("Status", ["Terbit", "Belum Terbit"], index=0 if row["status"] == "Terbit" else 1, key=f"status_{idx}", label_visibility="collapsed")

                if cols[5].button("🔄", key=f"edit_{idx}"):
                    conn = connect_db()
                    cursor = conn.cursor()
                    try:
                        cursor.execute("""
                            UPDATE sertifikat SET tgl_terbit=%s, status=%s WHERE id_sertifikat=%s
                        """, (tgl_terbit, status, row["id_sertifikat"]))
                        conn.commit()
                        st.session_state["success_message"] = f"✅ Sertifikat berhasil diupdate."
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Gagal update: {e}")
                    finally:
                        cursor.close()
                        conn.close()

                if cols[6].button("🗑️", key=f"delete_{idx}"):
                    conn = connect_db()
                    cursor = conn.cursor()
                    try:
                        cursor.execute("DELETE FROM sertifikat WHERE id_sertifikat=%s", (row["id_sertifikat"],))
                        conn.commit()
                        st.session_state["success_message"] = f"✅ Sertifikat berhasil dihapus."
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Gagal hapus: {e}")
                    finally:
                        cursor.close()
                        conn.close()
        else:
            st.info("❕ Belum ada data sertifikat.")

    elif menu == "Kelola Notifikasi":
        st.title("🔔 Kelola Notifikasi")

        if "success_message" in st.session_state:
            st.success(st.session_state.success_message)
            del st.session_state["success_message"]

        # Form tambah notifikasi manual (opsional)
        with st.expander("➕ Tambah Notifikasi Manual"):
            # Ambil daftar angkatan dan prodi dari DB untuk dropdown
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT angkatan FROM mahasiswa ORDER BY angkatan")
            angkatan_list = [str(row[0]) for row in cursor.fetchall()]
            cursor.execute("SELECT DISTINCT prodi FROM mahasiswa ORDER BY prodi")
            prodi_list = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()

            angkatan_options = ["-- Semua Angkatan --"] + angkatan_list
            prodi_options = ["-- Semua Prodi --"] + prodi_list

            selected_angkatan = st.selectbox("Filter Angkatan (opsional)", angkatan_options)
            selected_prodi = st.selectbox("Filter Prodi (opsional)", prodi_options)

            # Query mahasiswa berdasar filter (jika pilih semua, tidak difilter)
            query = "SELECT nim, nama_mahasiswa FROM mahasiswa WHERE 1=1"
            params = []

            if selected_angkatan != "-- Semua Angkatan --":
                query += " AND angkatan = %s"
                params.append(selected_angkatan)
            if selected_prodi != "-- Semua Prodi --":
                query += " AND prodi = %s"
                params.append(selected_prodi)

            query += " ORDER BY nama_mahasiswa"

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            mahasiswa_list = cursor.fetchall()
            cursor.close()
            conn.close()

            if mahasiswa_list:
                options = [f"{nim} - {nama}" for nim, nama in mahasiswa_list]
                selected_mahasiswa = st.selectbox("Pilih Mahasiswa (NIM - Nama)", options)
                nim = selected_mahasiswa.split(" - ")[0]
            else:
                st.warning("Tidak ada mahasiswa sesuai filter.")
                nim = None

            judul = st.text_input("Judul Notifikasi")
            pesan = st.text_area("Pesan Notifikasi")
            tanggal = st.date_input("Tanggal", value=pd.to_datetime("today"))

            if st.button("Tambah Notifikasi"):
                if not nim:
                    st.warning("Mohon pilih mahasiswa terlebih dahulu.")
                elif not judul or not pesan:
                    st.warning("Judul dan pesan harus diisi.")
                else:
                    conn = connect_db()
                    cursor = conn.cursor()
                    try:
                        cursor.execute("""
                            INSERT INTO notifikasi (nim, judul, pesan, tanggal)
                            VALUES (%s, %s, %s, %s)
                        """, (nim, judul, pesan, tanggal))
                        conn.commit()
                        st.session_state["success_message"] = "Notifikasi berhasil ditambahkan."
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Gagal tambah notifikasi: {e}")
                    finally:
                        cursor.close()
                        conn.close()

        conn = connect_db()
        cursor = conn.cursor()

        # Ambil data notifikasi beserta nama mahasiswa
        cursor.execute("""
            SELECT n.id_notifikasi, n.nim, m.nama_mahasiswa, n.judul, n.pesan, n.tanggal
            FROM notifikasi n
            JOIN mahasiswa m ON n.nim = m.nim
            WHERE n.id_pengelola = %s
            ORDER BY n.tanggal DESC
        """, (st.session_state.user["id_pengelola"],))

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)

        cursor.close()
        conn.close()

        st.subheader("📋 Daftar Notifikasi")

        if not df.empty:
            header_cols = st.columns([1, 2, 3, 5, 2])
            headers = ["ID", "NIM", "Nama Mahasiswa", "Pesan", "Tanggal"]
            for col, header in zip(header_cols, headers):
                col.markdown(f"**{header}**")

            for idx, row in df.iterrows():
                cols = st.columns([1, 2, 3, 5, 2])
                cols[0].markdown(str(row["id_notifikasi"]))
                cols[1].markdown(row["nim"])
                cols[2].markdown(row["nama_mahasiswa"])
                cols[3].markdown(f"**{row['judul']}**\n\n{row['pesan']}")
                cols[4].markdown(row["tanggal"].strftime("%Y-%m-%d"))

        else:
            st.info("📭 Belum ada notifikasi.")



    elif menu == "Keluar":
        st.session_state.clear()
        st.success("✅ Berhasil logout.")
        st.rerun()