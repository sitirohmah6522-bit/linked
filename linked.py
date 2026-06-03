import streamlit as st

class BarangNode:
    def _init_(self, kode, nama, stok):
        self.kode = kode
        self.nama = nama
        self.stok = stok
        self.next = None


class GudangLinkedList:
    def _init_(self):
        self.head = None

    def tambah_barang(self, kode, nama, stok):
        node_baru = BarangNode(kode, nama, stok)

        if self.head is None:
            self.head = node_baru
        else:
            bantu = self.head
            while bantu.next is not None:
                bantu = bantu.next
            bantu.next = node_baru

    def tampilkan_barang(self):
        data = []
        bantu = self.head

        while bantu is not None:
            data.append({
                "Kode Barang": bantu.kode,
                "Nama Barang": bantu.nama,
                "Stok": bantu.stok
            })
            bantu = bantu.next

        return data

    def cari_barang(self, kode):
        bantu = self.head

        while bantu is not None:
            if bantu.kode == kode:
                return bantu
            bantu = bantu.next

        return None

    def hapus_barang(self, kode):
        bantu = self.head

        if bantu is not None and bantu.kode == kode:
            self.head = bantu.next
            return True

        sebelumnya = None
        while bantu is not None:
            if bantu.kode == kode:
                sebelumnya.next = bantu.next
                return True
            sebelumnya = bantu
            bantu = bantu.next

        return False


st.set_page_config(page_title="Linked List Gudang", page_icon="📦")

st.title("📦 Sistem Gudang Menggunakan Linked List")
st.write("Aplikasi ini menggunakan struktur data Single Linked List.")

# RESET object lama yang error
if "gudang" not in st.session_state or not hasattr(st.session_state.gudang, "head"):
    st.session_state.gudang = GudangLinkedList()

tab1, tab2, tab3, tab4 = st.tabs([
    "➕ Tambah Barang",
    "📋 Lihat Barang",
    "🔍 Cari Barang",
    "🗑️ Hapus Barang"
])

with tab1:
    st.subheader("Tambah Data Barang")

    kode = st.text_input("Kode Barang")
    nama = st.text_input("Nama Barang")
    stok = st.number_input("Stok Barang", min_value=0, step=1)

    if st.button("Tambah Barang"):
        if kode and nama:
            st.session_state.gudang.tambah_barang(kode, nama, stok)
            st.success("Barang berhasil ditambahkan!")
        else:
            st.warning("Kode dan nama barang harus diisi.")

with tab2:
    st.subheader("Data Barang Gudang")

    data = st.session_state.gudang.tampilkan_barang()

    if data:
        st.table(data)
    else:
        st.info("Belum ada data barang.")

with tab3:
    st.subheader("Cari Barang")

    kode_cari = st.text_input("Masukkan kode barang yang dicari")

    if st.button("Cari"):
        hasil = st.session_state.gudang.cari_barang(kode_cari)

        if hasil:
            st.success("Barang ditemukan!")
            st.write("Kode:", hasil.kode)
            st.write("Nama:", hasil.nama)
            st.write("Stok:", hasil.stok)
        else:
            st.error("Barang tidak ditemukan.")

with tab4:
    st.subheader("Hapus Barang")

    kode_hapus = st.text_input("Masukkan kode barang yang ingin dihapus")

    if st.button("Hapus"):
        berhasil = st.session_state.gudang.hapus_barang(kode_hapus)

        if berhasil:
            st.success("Barang berhasil dihapus.")
        else:
            st.error("Barang tidak ditemukan.")

if st.button("Reset Data"):
    st.session_state.gudang = GudangLinkedList()
    st.success("Data berhasil direset.")
