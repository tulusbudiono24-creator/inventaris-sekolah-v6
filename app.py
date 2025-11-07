import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Inventaris Sekolah", layout="wide")

st.title("📘 Aplikasi Inventaris Sekolah")
st.caption("By: Tulus Budiono | SMK KY Ageng Giri")

# ==============================================
# Fungsi Simpan & Load Excel
# ==============================================
def simpan_excel(df, nama_file):
    towrite = BytesIO()
    df.to_excel(towrite, index=False, sheet_name="DataInventaris")
    towrite.seek(0)
    st.download_button(
        label="💾 Download Data Excel",
        data=towrite,
        file_name=f"{nama_file}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def load_data():
    try:
        return pd.read_excel("inventaris_data.xlsx")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Ruang", "Nama Barang", "Jumlah", "Kondisi", "Keterangan"])

def save_data(df):
    df.to_excel("inventaris_data.xlsx", index=False)

# ==============================================
# Muat Data
# ==============================================
df = load_data()

# ==============================================
# Input Data Baru
# ==============================================
st.sidebar.header("➕ Tambah / Edit Data Inventaris")

ruang = st.sidebar.selectbox("Pilih Ruang", sorted(df["Ruang"].unique().tolist() + ["Baru"]), index=len(df["Ruang"].unique().tolist()))
if ruang == "Baru":
    ruang = st.sidebar.text_input("Masukkan Nama Ruang Baru")

nama_barang = st.sidebar.text_input("Nama Barang")
jumlah = st.sidebar.number_input("Jumlah", min_value=1, step=1)
kondisi = st.sidebar.selectbox("Kondisi", ["Baik", "Rusak Ringan", "Rusak Berat"])
keterangan = st.sidebar.text_input("Keterangan (Opsional)")

if st.sidebar.button("💾 Simpan Data"):
    if ruang and nama_barang:
        new_data = pd.DataFrame([[ruang, nama_barang, jumlah, kondisi, keterangan]],
                                columns=df.columns)
        df = pd.concat([df, new_data], ignore_index=True)
        save_data(df)
        st.sidebar.success("✅ Data berhasil disimpan!")
        st.experimental_rerun()
    else:
        st.sidebar.warning("⚠️ Lengkapi semua data dulu!")

# ==============================================
# Tabel Data & Edit Langsung
# ==============================================
st.subheader("📋 Data Inventaris Sekolah")

if len(df) > 0:
    # Tabel editable
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        key="editable_tabel",
    )

    # Tombol simpan perubahan
    if st.button("💾 Simpan Perubahan"):
        save_data(edited_df)
        st.success("✅ Data berhasil diperbarui!")
        st.experimental_rerun()

    # Tombol download Excel
    simpan_excel(edited_df, "Data_Inventaris_Sekolah")

    # Hapus baris tertentu
    with st.expander("🗑️ Hapus Data"):
        index_hapus = st.number_input("Masukkan Nomor Baris yang Ingin Dihapus", min_value=0, max_value=len(df)-1, step=1)
        if st.button("Hapus"):
            df = df.drop(df.index[index_hapus])
            save_data(df)
            st.warning(f"❌ Data baris ke-{index_hapus} telah dihapus.")
            st.experimental_rerun()

else:
    st.info("Belum ada data inventaris. Tambahkan data di sidebar.")

# ==============================================
# Footer
# ==============================================
st.markdown("---")
st.caption("🧰 Dibuat dengan Streamlit | Versi 2025 | Dapat diakses via HP & Laptop")
