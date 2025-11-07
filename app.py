import streamlit as st
import pandas as pd
from io import BytesIO

# -------------------------------
# Konfigurasi halaman
# -------------------------------
st.set_page_config(page_title="Inventaris Sekolah", layout="wide")

# -------------------------------
# Inisialisasi DataFrame
# -------------------------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Nama Barang", "Jumlah", "Kondisi", "Ruang", "Keterangan"
    ])

# -------------------------------
# Fungsi untuk simpan ke Excel
# -------------------------------
def simpan_ke_excel(df):
    output = BytesIO()
    df.to_excel(output, index=False, sheet_name="Inventaris")
    return output.getvalue()

# -------------------------------
# Tampilan Input Data
# -------------------------------
st.title("📦 Aplikasi Inventaris Sekolah")
st.write("Gunakan aplikasi ini untuk mencatat, mengedit, dan mengelola inventaris per ruang secara langsung, termasuk dari HP.")

with st.expander("➕ Tambah Data Baru", expanded=False):
    with st.form("form_tambah"):
        col1, col2, col3 = st.columns(3)
        nama = col1.text_input("Nama Barang")
        jumlah = col2.number_input("Jumlah", min_value=1, value=1)
        kondisi = col3.selectbox("Kondisi", ["Baik", "Rusak Ringan", "Rusak Berat"])
        ruang = st.selectbox("Ruang", ["Lab DKV", "Lab MPLB", "Lab Informatika", "Ruang Guru", "Perpustakaan", "Kelas"])
        keterangan = st.text_area("Keterangan (opsional)")
        submitted = st.form_submit_button("Tambah Data")

        if submitted:
            new_row = pd.DataFrame({
                "Nama Barang": [nama],
                "Jumlah": [jumlah],
                "Kondisi": [kondisi],
                "Ruang": [ruang],
                "Keterangan": [keterangan]
            })
            st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
            st.success("✅ Data berhasil ditambahkan!")

# -------------------------------
# Tampilan Data
# -------------------------------
st.subheader("📋 Daftar Inventaris")

if st.session_state.data.empty:
    st.info("Belum ada data. Tambahkan data terlebih dahulu.")
else:
    df = st.session_state.data.copy()

    # Pilihan ruang filter
    ruang_pilih = st.selectbox("Filter berdasarkan ruang:", ["Semua"] + df["Ruang"].unique().tolist())

    if ruang_pilih != "Semua":
        df = df[df["Ruang"] == ruang_pilih]

    # Tampilkan tabel data
    st.dataframe(df, use_container_width=True)

    # -------------------------------
    # Fitur Edit Data
    # -------------------------------
    st.markdown("### ✏️ Edit Data")
    index_pilih = st.number_input("Pilih nomor data yang ingin diedit (mulai dari 0):", min_value=0,
                                  max_value=len(df) - 1, step=1)

    if st.button("Tampilkan Data untuk Diedit"):
        data_edit = df.iloc[index_pilih]

        with st.form("form_edit"):
            col1, col2, col3 = st.columns(3)
            nama_edit = col1.text_input("Nama Barang", data_edit["Nama Barang"])
            jumlah_edit = col2.number_input("Jumlah", min_value=1, value=int(data_edit["Jumlah"]))
            kondisi_edit = col3.selectbox("Kondisi", ["Baik", "Rusak Ringan", "Rusak Berat"], index=["Baik", "Rusak Ringan", "Rusak Berat"].index(data_edit["Kondisi"]))
            ruang_edit = st.selectbox("Ruang", ["Lab DKV", "Lab MPLB", "Lab Informatika", "Ruang Guru", "Perpustakaan", "Kelas"], index=["Lab DKV", "Lab MPLB", "Lab Informatika", "Ruang Guru", "Perpustakaan", "Kelas"].index(data_edit["Ruang"]))
            keterangan_edit = st.text_area("Keterangan (opsional)", data_edit["Keterangan"])

            update_btn = st.form_submit_button("💾 Simpan Perubahan")

            if update_btn:
                st.session_state.data.loc[index_pilih] = [nama_edit, jumlah_edit, kondisi_edit, ruang_edit, keterangan_edit]
                st.success("✅ Data berhasil diperbarui!")

    # -------------------------------
    # Fitur Hapus Data
    # -------------------------------
    st.markdown("### 🗑️ Hapus Data")
    hapus_index = st.number_input("Masukkan nomor data yang ingin dihapus:", min_value=0, max_value=len(df) - 1, step=1)
    if st.button("Hapus Data"):
        st.session_state.data = st.session_state.data.drop(hapus_index).reset_index(drop=True)
        st.warning("❌ Data berhasil dihapus.")

    # -------------------------------
    # Tombol Download Excel
    # -------------------------------
    st.markdown("### 💾 Simpan Data ke Excel")
    excel_data = simpan_ke_excel(st.session_state.data)
    st.download_button(
        label="📥 Unduh Excel",
        data=excel_data,
        file_name="Inventaris_Sekolah.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("👨‍💻 Dibuat oleh Tulus Budiono | Versi Revisi: Fitur Edit + Save Excel")
