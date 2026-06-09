import streamlit as st
from datetime import datetime

class BarangNode:
    def __init__(self, kode, nama, kategori, stok, harga):
        self.kode = kode
        self.nama = nama
        self.kategori = kategori
        self.stok = stok
        self.harga = harga
        self.next = None


class GudangLinkedList:
    def __init__(self):
        self.head = None
        self.riwayat = []

    def tambah_riwayat(self, aktivitas):
        waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.riwayat.append({"Waktu": waktu, "Aktivitas": aktivitas})

    def tambah_barang(self, kode, nama, kategori, stok, harga):
        node_baru = BarangNode(kode, nama, kategori, stok, harga)

        if self.head is None:
            self.head = node_baru
        else:
            bantu = self.head
            while bantu.next is not None:
                bantu = bantu.next
            bantu.next = node_baru

        self.tambah_riwayat(f"Menambahkan barang {nama} sebanyak {stok}")

    def tampilkan_barang(self):
        data = []
        bantu = self.head

        while bantu is not None:
            data.append({
                "Kode Barang": bantu.kode,
                "Nama Barang": bantu.nama,
                "Kategori": bantu.kategori,
                "Stok": bantu.stok,
                "Harga": bantu.harga,
                "Total Nilai": bantu.stok * bantu.harga
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

    def cari_by_kode(self, kode):
        bantu = self.head

        while bantu is not None:
            if bantu.kode == kode:
                return bantu
            bantu = bantu.next

        return None

    def tambah_stok(self, kode, jumlah):
        barang = self.cari_by_kode(kode)

        if barang:
            barang.stok += jumlah
            self.tambah_riwayat(f"Stok {barang.nama} bertambah {jumlah}")
            return True

        return False

    def kurangi_stok(self, kode, jumlah):
        barang = self.cari_by_kode(kode)

        if barang:
            if barang.stok >= jumlah:
                barang.stok -= jumlah
                self.tambah_riwayat(f"Stok {barang.nama} berkurang {jumlah}")
                return "berhasil"
            else:
                return "stok_kurang"

        return "tidak_ditemukan"

    def edit_barang(self, kode, nama_baru, kategori_baru, stok_baru, harga_baru):
        barang = self.cari_by_kode(kode)

        if barang:
            barang.nama = nama_baru
            barang.kategori = kategori_baru
            barang.stok = stok_baru
            barang.harga = harga_baru
            self.tambah_riwayat(f"Data barang {kode} berhasil diedit")
            return True

        return False

    def hapus_barang(self, kode):
        bantu = self.head

        if bantu is not None and bantu.kode == kode:
            self.tambah_riwayat(f"Barang {bantu.nama} dihapus")
            self.head = bantu.next
            return True

        sebelumnya = None
        while bantu is not None:
            if bantu.kode == kode:
                self.tambah_riwayat(f"Barang {bantu.nama} dihapus")
                sebelumnya.next = bantu.next
                return True
            sebelumnya = bantu
            bantu = bantu.next

        return False

    def stok_menipis(self):
        data = []
        bantu = self.head

        while bantu is not None:
            if bantu.stok <= 5:
                data.append({
                    "Kode Barang": bantu.kode,
                    "Nama Barang": bantu.nama,
                    "Stok": bantu.stok
                })
            bantu = bantu.next

        return data

    def statistik_gudang(self):
        total_barang = 0
        total_stok = 0
        total_nilai = 0
        stok_terbanyak = None
        stok_tersedikit = None

        bantu = self.head

        while bantu is not None:
            total_barang += 1
            total_stok += bantu.stok
            total_nilai += bantu.stok * bantu.harga

            if stok_terbanyak is None or bantu.stok > stok_terbanyak.stok:
                stok_terbanyak = bantu

            if stok_tersedikit is None or bantu.stok < stok_tersedikit.stok:
                stok_tersedikit = bantu

            bantu = bantu.next

        return total_barang, total_stok, total_nilai, stok_terbanyak, stok_tersedikit


st.set_page_config(page_title="Sistem Gudang Retail", page_icon="📦")

st.title("📦 Sistem Gudang Retail Menggunakan Single Linked List")
st.write("Aplikasi ini memiliki fitur tambah barang, tambah stok, kurangi stok, edit barang, kategori, notifikasi stok menipis, riwayat transaksi, statistik, harga, dan total nilai gudang.")

if "gudang" not in st.session_state or not hasattr(st.session_state.gudang, "head"):
    st.session_state.gudang = GudangLinkedList()

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "➕ Tambah Barang",
    "📋 Lihat Barang",
    "🔍 Cari Cepat",
    "📥 Tambah Stok",
    "➖ Kurangi Stok",
    "✏️ Edit Barang",
    "⚠️ Stok Menipis",
    "📊 Statistik",
    "🕒 Riwayat"
])

with tab1:
    st.subheader("Tambah Data Barang")

    kode = st.text_input("Kode Barang")
    nama = st.text_input("Nama Barang")
    kategori = st.selectbox("Kategori Barang", ["Makanan", "Minuman", "Snack", "Sembako", "Peralatan", "Lainnya"])
    stok = st.number_input("Stok Barang", min_value=0, step=1)
    harga = st.number_input("Harga Barang", min_value=0, step=500)

    if st.button("Tambah Barang"):
        if kode and nama:
            st.session_state.gudang.tambah_barang(kode, nama, kategori, stok, harga)
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
            data_hasil = []
            for barang in hasil:
                data_hasil.append({
                    "Kode Barang": barang.kode,
                    "Nama Barang": barang.nama,
                    "Kategori": barang.kategori,
                    "Stok": barang.stok,
                    "Harga": barang.harga,
                    "Total Nilai": barang.stok * barang.harga
                })

            st.success("Barang ditemukan!")
            st.table(data_hasil)
        else:
            st.error("Barang tidak ditemukan.")
    elif kata_kunci:
        st.warning("Masukkan minimal 3 huruf.")


with tab4:
    st.subheader("Tambah Stok Barang")

    kode_tambah = st.text_input("Kode barang yang stoknya ingin ditambah")
    jumlah_tambah = st.number_input("Jumlah stok masuk", min_value=1, step=1)

    if st.button("Tambah Stok"):
        berhasil = st.session_state.gudang.tambah_stok(kode_tambah, jumlah_tambah)

        if berhasil:
            st.success("Stok barang berhasil ditambahkan.")
        else:
            st.error("Barang tidak ditemukan.")


with tab5:
    st.subheader("Kurangi Stok Barang")
    st.write("Digunakan saat barang keluar atau terjual.")

    kode_kurang = st.text_input("Kode barang yang stoknya ingin dikurangi")
    jumlah_kurang = st.number_input("Jumlah stok keluar", min_value=1, step=1)

    if st.button("Kurangi Stok"):
        hasil = st.session_state.gudang.kurangi_stok(kode_kurang, jumlah_kurang)

        if hasil == "berhasil":
            st.success("Stok barang berhasil dikurangi.")
        elif hasil == "stok_kurang":
            st.warning("Stok tidak mencukupi.")
        else:
            st.error("Barang tidak ditemukan.")


with tab6:
    st.subheader("Edit Data Barang")

    kode_edit = st.text_input("Masukkan kode barang yang ingin diedit")
    barang_edit = st.session_state.gudang.cari_by_kode(kode_edit)

    if barang_edit:
        nama_baru = st.text_input("Nama Baru", value=barang_edit.nama)
        kategori_baru = st.selectbox(
            "Kategori Baru",
            ["Makanan", "Minuman", "Snack", "Sembako", "Peralatan", "Lainnya"],
            index=["Makanan", "Minuman", "Snack", "Sembako", "Peralatan", "Lainnya"].index(barang_edit.kategori)
        )
