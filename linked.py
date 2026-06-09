import streamlit as st

class BarangNode:
    def __init__(self, kode, nama, stok):
        self.kode = kode
        self.nama = nama
        self.stok = stok
        self.next = None


class GudangLinkedList:
    def __init__(self):
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

    def cari_barang(self, kata_kunci):
        hasil = []
        bantu = self.head

        while bantu is not None:
            if (
                bantu.kode.lower().startswith(kata_kunci.lower()) or
                bantu.nama.lower().startswith(kata_kunci.lower())
            ):
                hasil.append(bantu)
            bantu = bantu.next

        return hasil

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

    def kurangi_stok(self, kode, jumlah):
        bantu = self.head

        while bantu is not None:
            if bantu.kode == kode:
                if bantu.stok >= jumlah:
                    bantu.stok -= jumlah
                    return "berhasil"
                else:
                    return "stok_kurang"
            bantu = bantu.next

        return "tidak_ditemukan"


st.set_page_config(page_title="Linked List Gudang Retail", page_icon="📦")

st.title("📦 Sistem Gudang Retail Menggunakan Linked List")
st.write("Aplikasi gudang sederhana dengan fitur tambah, lihat, cari cepat, hapus, dan pengurangan stok barang.")

if "gudang" not in st.session_state or not hasattr(st.session_state.gudang, "head"):
    st.session_state.gudang = GudangLinkedList()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "➕ Tambah Barang",
    "📋 Lihat Barang",
    "🔍 Cari Cepat",
    "➖ Kurangi Stok",
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
    st.subheader("Cari Cepat Barang")
    st.write("Masukkan minimal 3 huruf pertama dari kode atau nama barang.")

    kata_kunci = st.text_input("Masukkan 3 huruf pertama")

    if len(kata_kunci) >= 3:
        hasil = st.session_state.gudang.cari_barang(kata_kunci)

        if hasil:
            st.success("Barang ditemukan!")

            data_hasil = []
            for barang in hasil:
                data_hasil.append({
                    "Kode Barang": barang.kode,
                    "Nama Barang": barang.nama,
                    "Stok": barang.stok
                })

            st.table(data_hasil)
        else:
            st.error("Barang tidak ditemukan.")
    elif kata_kunci:
        st.warning("Masukkan minimal 3 huruf.")


with tab4:
    st.subheader("Pengurangan Stok Barang")
    st.write("Fitur ini digunakan saat barang keluar atau terjual.")

    kode_kurang = st.text_input("Kode barang yang stoknya dikurangi")
    jumlah_kurang = st.number_input("Jumlah pengurangan stok", min_value=1, step=1)

    if st.button("Kurangi Stok"):
        hasil = st.session_state.gudang.kurangi_stok(kode_kurang, jumlah_kurang)

        if hasil == "berhasil":
            st.success("Stok barang berhasil dikurangi.")
        elif hasil == "stok_kurang":
            st.warning("Stok tidak mencukupi.")
        else:
            st.error("Barang tidak ditemukan.")


with tab5:
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
