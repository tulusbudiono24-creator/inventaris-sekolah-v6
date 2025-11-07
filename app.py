import streamlit as st
import pandas as pd
from io import BytesIO

# ====== LOGIN SYSTEM ======
st.set_page_config(page_title="Inventaris Sekolah", layout="wide")
st.markdown(
    """
    <style>
    .block-container {padding-top: 1rem;}
    @media (max-width: 768px) {.stButton>button {width: 100%;}}
    </style>
    """,
    unsafe_allow_html=True,
)

# Username dan Password
USER = "tulus"
PASS = "himawari"

# Session state untuk login
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔒 Login Aplikasi Inventaris")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if u == USER and p == PASS:
            st.session_state.login = True
            st.success("Login berhasil!")
            st.rerun()
        else:
            st.error("Username atau password salah!")
    st.stop()

# ====== DATA STORAGE ======
if "ruang_data" not in st.session_state:
    st.session_state.ruang_data = []  # List of dicts
if "barang_data" not in st.session_state:
    st.session_state.barang_data = []  # List of dicts

st.sidebar.title("📋 Menu Inventaris")
menu = st.sidebar.radio("Pilih Menu", ["Input Ruang", "Input Barang", "Lihat Data", "Logout"])

# ====== MENU: INPUT RUANG ======
if menu == "Input Ruang":
    st.header("🏠 Input Ruang dan Penanggung Jawab")
    with st.form("ruang_form"):
        ruang = st.text_input("Nama Ruang")
        pj = st.text_input("Penanggung Jawab")
        submitted = st.form_submit_button("Simpan Ruang")
        if submitted:
            if ruang and pj:
                st.session_state.ruang_data.append({"ruang": ruang, "pj": pj})
                st.success(f"Data ruang '{ruang}' berhasil disimpan!")
            else:
                st.warning("Mohon isi semua kolom!")

    if st.session_state.ruang_data:
        st.subheader("📦 Daftar Ruang")
        df_ruang = pd.DataFrame(st.session_state.ruang_data)
        for i, row in df_ruang.iterrows():
            col1, col2, col3, col4 = st.columns([3, 3, 1, 1])
            col1.write(row["ruang"])
            col2.write(row["pj"])
            if col3.button("✏️ Edit", key=f"edit_ruang_{i}"):
                st.session_state.edit_ruang = i
                st.rerun()
            if col4.button("🗑️ Hapus", key=f"hapus_ruang_{i}"):
                st.session_state.ruang_data.pop(i)
                st.success("Ruang dihapus!")
                st.rerun()

        # Form edit ruang
        if "edit_ruang" in st.session_state:
            idx = st.session_state.edit_ruang
            st.info(f"✏️ Edit Data Ruang ke-{idx}")
            data_edit = st.session_state.ruang_data[idx]
            with st.form("edit_ruang_form"):
                ruang_edit = st.text_input("Nama Ruang", data_edit["ruang"])
                pj_edit = st.text_input("Penanggung Jawab", data_edit["pj"])
                simpan_edit = st.form_submit_button("💾 Simpan Perubahan")
                if simpan_edit:
                    st.session_state.ruang_data[idx] = {"ruang": ruang_edit, "pj": pj_edit}
                    st.success("Data ruang berhasil diperbarui!")
                    del st.session_state["edit_ruang"]
                    st.rerun()

# ====== MENU: INPUT BARANG ======
elif menu == "Input Barang":
    st.header("🧰 Input Barang Berdasarkan Ruang & Penanggung Jawab")

    if not st.session_state.ruang_data:
        st.warning("Tambahkan ruang terlebih dahulu sebelum menginput barang.")
        st.stop()

    ruang_pilihan = [r["ruang"] for r in st.session_state.ruang_data]
    ruang_dipilih = st.selectbox("Pilih Ruang", ruang_pilihan)
    pj_dipilih = [r["pj"] for r in st.session_state.ruang_data if r["ruang"] == ruang_dipilih][0]

    with st.form("barang_form"):
        nama_barang = st.text_input("Nama Barang")
        jumlah = st.number_input("Jumlah", min_value=1, step=1)
        kondisi = st.selectbox("Kondisi", ["Baik", "Rusak", "Perlu Perbaikan"])
        tahun = st.number_input("Tahun Pembelian", min_value=2000, max_value=2100, step=1)
        simpan = st.form_submit_button("Simpan Barang")

        if simpan:
            if nama_barang:
                st.session_state.barang_data.append({
                    "ruang": ruang_dipilih,
                    "penanggung_jawab": pj_dipilih,
                    "barang": nama_barang,
                    "jumlah": jumlah,
                    "kondisi": kondisi,
                    "tahun": tahun
                })
                st.success("Barang berhasil disimpan!")
            else:
                st.warning("Nama barang wajib diisi!")

    if st.session_state.barang_data:
        st.subheader("📋 Data Barang")
        df_barang = pd.DataFrame(st.session_state.barang_data)
        for i, row in df_barang.iterrows():
            col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 2, 2, 1, 2, 1, 1])
            col1.write(row["barang"])
            col2.write(row["ruang"])
            col3.write(row["penanggung_jawab"])
            col4.write(row["jumlah"])
            col5.write(row["kondisi"])
            if col6.button("✏️", key=f"edit_barang_{i}"):
                st.session_state.edit_barang = i
                st.rerun()
            if col7.button("🗑️", key=f"hapus_barang_{i}"):
                st.session_state.barang_data.pop(i)
                st.success("Barang dihapus!")
                st.rerun()

        # Form edit barang
        if "edit_barang" in st.session_state:
            idx = st.session_state.edit_barang
            st.info(f"✏️ Edit Data Barang ke-{idx}")
            data_edit = st.session_state.barang_data[idx]
            with st.form("edit_barang_form"):
                ruang_edit = st.selectbox("Ruang", ruang_pilihan, index=ruang_pilihan.index(data_edit["ruang"]))
                pj_edit = [r["pj"] for r in st.session_state.ruang_data if r["ruang"] == ruang_edit][0]
                nama_edit = st.text_input("Nama Barang", data_edit["barang"])
                jumlah_edit = st.number_input("Jumlah", min_value=1, value=int(data_edit["jumlah"]))
                kondisi_edit = st.selectbox("Kondisi", ["Baik", "Rusak", "Perlu Perbaikan"],
                                            index=["Baik", "Rusak", "Perlu Perbaikan"].index(data_edit["kondisi"]))
                tahun_edit = st.number_input("Tahun Pembelian", min_value=2000, max_value=2100, value=int(data_edit["tahun"]))
                simpan_edit = st.form_submit_button("💾 Simpan Perubahan")
                if simpan_edit:
                    st.session_state.barang_data[idx] = {
                        "ruang": ruang_edit,
                        "penanggung_jawab": pj_edit,
                        "barang": nama_edit,
                        "jumlah": jumlah_edit,
                        "kondisi": kondisi_edit,
                        "tahun": tahun_edit
                    }
                    st.success("Data barang berhasil diperbarui!")
                    del st.session_state["edit_barang"]
                    st.rerun()

# ====== MENU: LIHAT DATA ======
elif menu == "Lihat Data":
    st.header("📊 Laporan Data Inventaris per Ruang")

    if not st.session_state.barang_data:
        st.info("Belum ada data barang.")
        st.stop()

    ruang_pilihan = sorted(set([b["ruang"] for b in st.session_state.barang_data]))
    ruang_dipilih = st.selectbox("Pilih Ruang", ruang_pilihan)

    df = pd.DataFrame([b for b in st.session_state.barang_data if b["ruang"] == ruang_dipilih])
    st.dataframe(df, use_container_width=True)

    towrite = BytesIO()
    df.to_excel(towrite, index=False, sheet_name=f"Data_{ruang_dipilih}")
    towrite.seek(0)

    st.download_button(
        label="💾 Simpan ke Excel",
        data=towrite,
        file_name=f"Inventaris_{ruang_dipilih}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ====== LOGOUT ======
elif menu == "Logout":
    st.session_state.login = False
    st.success("Logout berhasil!")
    st.rerun()
