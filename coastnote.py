import streamlit as st
import pandas as pd
from datetime import date,datetime

# =========================
# PENGATURAN HALAMAN
# =========================
st.set_page_config(
    page_title="COASTNOTE",
    page_icon="🌿",
    layout="wide"
)

# =========================
# DESAIN APLIKASI
# =========================
st.markdown("""
<style>
.stApp {
    background: #F3EFE6;
}

h1, h2, h3 {
    color: #596B50;
}

p, label {
    color: #796B54;
}

[data-testid="stMetric"] {
    background: #FFFCF6;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #E3DDCF;
}

.stButton > button {
    background: #829779;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 22px;
}

.stButton > button:hover {
    background: #687D60;
    color: white;
}

.card {
    background: #FFFCF6;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #E3DDCF;
    margin-bottom: 15px;
}

.hero {
    background: linear-gradient(110deg, #AAB99B, #D2C3A9);
    padding: 30px;
    border-radius: 18px;
    color: #40513C;
}

.hero h2 {
    color: #40513C;
}

.hero p {
    color: #40513C;
}
</style>
""", unsafe_allow_html=True)

# =========================
# JUDUL APLIKASI
# =========================
st.title("🌿 COASTNOTE")
st.caption("COASTAL SURVEY RECORD SYSTEM")

st.markdown("""
<div class="hero">
    <h2>Welcome to COASTNOTE</h2>
    <p>Catat, simpan, dan pantau hasil pengamatan wilayah pesisir.</p>
</div>
""", unsafe_allow_html=True)

st.write(
    "📅 Tanggal hari ini:",
    datetime.now().strftime("%d-%m-%Y")
)

st.divider()

# =========================
# RINGKASAN DATA
# =========================
st.header("📊 Ringkasan Pengamatan")

if "survei" not in st.session_state:
    st.session_state.survei = []

total = len(st.session_state.survei)

lokasi = len(set(
    data["Lokasi"] for data in st.session_state.survei
))

col1, col2, col3 = st.columns(3)

col1.metric("📝 Total Survei", total)
col2.metric("📍 Lokasi Diamati", lokasi)
col3.metric("🌊 Data Tersimpan", total)

st.divider()

# =========================
# FORMULIR SURVEI
# =========================
st.header("📝 Formulir Pengamatan")

with st.form("form_survei"):

    nama_lokasi = st.text_input(
        "Nama lokasi pengamatan",
        placeholder="Contoh: Pantai Sedari"
    )

    tanggal = st.date_input(
        "Tanggal pengamatan",
        value=datetime.now().date()
    )

    col1, col2 = st.columns(2)

    with col1:
        cuaca = st.selectbox(
            "Kondisi cuaca",
            ["Cerah", "Berawan", "Mendung", "Hujan"]
        )

        gelombang = st.selectbox(
            "Kondisi gelombang",
            ["Rendah", "Sedang", "Tinggi"]
        )

    with col2:
        kondisi_pantai = st.selectbox(
            "Kondisi pantai",
            ["Berpasir", "Berlumpur", "Berbatu", "Campuran"]
        )

        vegetasi = st.selectbox(
            "Vegetasi pesisir",
            ["Mangrove", "Pohon kelapa", "Vegetasi pantai lainnya", "Tidak ditemukan"]
        )

    keterangan = st.text_area(
        "Catatan tambahan",
        placeholder="Tuliskan hasil pengamatan..."
    )

    simpan = st.form_submit_button(
        "🌿 Simpan Pengamatan",
        use_container_width=True
    )

    if simpan:
        if nama_lokasi.strip() == "":
            st.warning("Nama lokasi harus diisi terlebih dahulu.")
        else:
            data_baru = {
                "Tanggal": tanggal.strftime("%d-%m-%Y"),
                "Lokasi": nama_lokasi,
                "Cuaca": cuaca,
                "Gelombang": gelombang,
                "Kondisi Pantai": kondisi_pantai,
                "Vegetasi": vegetasi,
                "Catatan": keterangan
            }

            st.session_state.survei.append(data_baru)

            st.success("Pengamatan berhasil disimpan!")

st.divider()

# =========================
# RIWAYAT PENGAMATAN
# =========================
st.header("📋 Riwayat Survei")

if total > 0:
    tabel = pd.DataFrame(st.session_state.survei)

    st.dataframe(
        tabel,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("Belum ada data pengamatan. Silakan isi formulir terlebih dahulu.")

st.divider()

# =========================
# INFORMASI APLIKASI
# =========================
st.header("ℹ️ Tentang COASTNOTE")

st.markdown("""
<div class="card">
    <h3>🌿 Coastal Survey Record System</h3>
    <p>
    COASTNOTE merupakan aplikasi pencatatan hasil survei pesisir
    yang membantu pengguna menyimpan dan melihat kembali
    informasi hasil pengamatan wilayah pantai.
    </p>
    <p>
    Aplikasi ini dapat digunakan untuk mendokumentasikan
    kondisi cuaca, gelombang, karakteristik pantai,
    serta vegetasi pesisir.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style="text-align:center; color:#8A806F;">
COASTNOTE © 2026 | Coastal Survey Record System
</p>
""", unsafe_allow_html=True)

# =========================
# EKSPOR DATA SURVEI
# =========================

st.divider()

st.header("📥 Pusat Data COASTNOTE")

st.markdown("""
<div class="card">
    <h3>🌿 Simpan Hasil Pengamatan</h3>
    <p>
    Data survei yang telah dimasukkan dapat diunduh
    untuk digunakan sebagai dokumentasi dan laporan pengamatan.
    </p>
</div>
""", unsafe_allow_html=True)

if st.session_state.survei:

    data_export = pd.DataFrame(st.session_state.survei)

    file_csv = data_export.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="⬇️ Unduh Data Survei (CSV)",
        data=file_csv,
        file_name="data_survei_coastnote.csv",
        mime="text/csv",
        use_container_width=True
    )

else:
    st.info("Belum ada data survei yang dapat diunduh.")

st.caption("COASTNOTE | Dokumentasi survei wilayah pesisir")

# =========================
# VISUALISASI HASIL SURVEI
# =========================

st.divider()

st.header("📊 Visualisasi Hasil Survei")

if st.session_state.survei:

    data_grafik = pd.DataFrame(st.session_state.survei)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("☀️ Kondisi Cuaca")

        grafik_cuaca = data_grafik["Cuaca"].value_counts()

        st.bar_chart(
            grafik_cuaca,
            color="#829779"
        )

    with col2:
        st.subheader("🌊 Kondisi Gelombang")

        grafik_gelombang = data_grafik["Gelombang"].value_counts()

        st.bar_chart(
            grafik_gelombang,
            color="#B49A7A"
        )

    st.caption(
        "Grafik diperbarui berdasarkan data survei yang tersimpan."
    )

else:
    st.info(
        "Masukkan data pengamatan terlebih dahulu "
        "untuk menampilkan grafik."
    )


   # =========================
# STYLE COASTNOTE
# =========================

st.markdown("""
<style>

.stApp {
    background-color: #F5F3EB;
}

h1, h2, h3 {
    color: #526B52;
}

p, label {
    color: #514B40;
}

div[data-testid="stMetric"] {
    background-color: #E5E9DD;
    padding: 18px;
    border-radius: 12px;
}

.stButton > button {
    background-color: #829779;
    color: white;
    border-radius: 10px;
    border: none;
}

.stButton > button:hover {
    background-color: #657D62;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# =========================
# ANALISIS KONDISI PESISIR
# =========================

st.divider()

st.header("🌿 Analisis Kondisi Pesisir")

if st.session_state.survei:

    data_analisis = pd.DataFrame(st.session_state.survei)

    st.write(
        "Bagian ini menampilkan ringkasan kondisi "
        "lingkungan berdasarkan hasil pengamatan."
    )

    total_data = len(data_analisis)

    st.metric(
        "Total Data Pengamatan",
        total_data
    )

    if "Cuaca" in data_analisis.columns:
        st.subheader("☀️ Ringkasan Cuaca")

        for nama, jumlah in data_analisis["Cuaca"].value_counts().items():
            st.write(f"• {nama}: {jumlah} pengamatan")

    if "Gelombang" in data_analisis.columns:
        st.subheader("🌊 Ringkasan Gelombang")

        for nama, jumlah in data_analisis["Gelombang"].value_counts().items():
            st.write(f"• {nama}: {jumlah} pengamatan")

    st.caption(
        "Analisis ini berdasarkan data yang telah dimasukkan, "
        "bukan hasil pengukuran otomatis."
    )

else:
    st.info("Belum ada data survei untuk dianalisis.")


    # =========================
# INFORMASI LOKASI SURVEI
# =========================

st.divider()

st.header("📍 Informasi Lokasi Survei")

if st.session_state.survei:

    data_lokasi = pd.DataFrame(st.session_state.survei)

    kolom_lokasi = None

    for kolom in ["Lokasi", "Nama Lokasi", "lokasi"]:
        if kolom in data_lokasi.columns:
            kolom_lokasi = kolom
            break

    if kolom_lokasi:

        daftar_lokasi = data_lokasi[kolom_lokasi].dropna()

        if not daftar_lokasi.empty:

            jumlah_lokasi = daftar_lokasi.nunique()

            st.metric(
                "Jumlah Lokasi Diamati",
                jumlah_lokasi
            )

            st.subheader("Daftar Lokasi")

            for lokasi, jumlah in daftar_lokasi.value_counts().items():

                st.write(f"📌 **{lokasi}**")
                st.caption(f"{jumlah} kali pengamatan")

        else:
            st.info("Belum ada informasi lokasi.")

    else:
        st.info(
            "Kolom lokasi belum ditemukan dalam data survei."
        )

else:
    st.info("Masukkan data survei untuk melihat informasi lokasi.")

    # =========================
# PANDUAN PENGAMATAN CUACA
# =========================

st.divider()

st.header("☀️ Pusat Informasi Cuaca")

panduan_cuaca = {
    "Cerah": {
        "ciri": "Langit didominasi warna biru, awan sedikit, dan sinar matahari terlihat langsung.",
        "pengamatan": "Perhatikan intensitas sinar matahari, suhu udara, dan kondisi permukaan pantai.",
        "status": "Cuaca cerah"
    },
    "Berawan": {
        "ciri": "Langit tertutup sebagian oleh awan, tetapi cahaya matahari masih dapat terlihat.",
        "pengamatan": "Amati perubahan tutupan awan dan kemungkinan perubahan cuaca.",
        "status": "Cuaca berawan"
    },
    "Mendung": {
        "ciri": "Langit didominasi awan tebal dan cahaya matahari berkurang.",
        "pengamatan": "Perhatikan kemungkinan hujan dan perubahan kondisi gelombang.",
        "status": "Perlu pemantauan cuaca"
    },
    "Hujan": {
        "ciri": "Terdapat air hujan yang turun di lokasi pengamatan.",
        "pengamatan": "Perhatikan jarak pandang, kondisi permukaan pantai, dan keselamatan kegiatan lapangan.",
        "status": "Waspadai kondisi lapangan"
    }
}

pilihan_cuaca = st.selectbox(
    "Pilih kondisi cuaca untuk melihat panduan:",
    list(panduan_cuaca.keys()),
    key="panduan_cuaca_coastnote"
)

hasil_cuaca = panduan_cuaca[pilihan_cuaca]

st.subheader(f"🌤️ Kondisi: {pilihan_cuaca}")

st.info(hasil_cuaca["ciri"])

st.write("**Hal yang perlu diperhatikan:**")
st.write(hasil_cuaca["pengamatan"])

st.success(hasil_cuaca["status"])

st.caption(
    "Panduan ini merupakan informasi pengamatan visual, "
    "bukan prakiraan cuaca atau pengukuran meteorologi."
)


# =========================
# PANDUAN GELOMBANG LAUT
# =========================

st.divider()

st.header("🌊 Pusat Informasi Gelombang")

panduan_gelombang = {
    "Tenang": {
        "tinggi": "0 – 0,1 meter",
        "ciri": "Permukaan laut relatif datar dengan riak kecil.",
        "dampak": "Pengamatan visual permukaan laut relatif mudah.",
        "peringatan": "Tetap perhatikan arus, pasang surut, dan kondisi sekitar."
    },
    "Rendah": {
        "tinggi": "> 0,1 – 0,5 meter",
        "ciri": "Gelombang kecil mulai terlihat dan permukaan laut sedikit bergelombang.",
        "dampak": "Pergerakan air mulai terlihat lebih jelas.",
        "peringatan": "Perhatikan perubahan gelombang selama pengamatan."
    },
    "Sedang": {
        "tinggi": "> 0,5 – 1,25 meter",
        "ciri": "Gelombang terlihat jelas dan dapat menyebabkan permukaan air berguncang.",
        "dampak": "Pengamatan di dekat air membutuhkan kewaspadaan lebih.",
        "peringatan": "Evaluasi kondisi lapangan sebelum melanjutkan survei."
    },
    "Tinggi": {
        "tinggi": "> 1,25 meter",
        "ciri": "Gelombang relatif besar dan pergerakan permukaan air lebih kuat.",
        "dampak": "Kondisi dapat mengganggu kegiatan pengamatan di pantai.",
        "peringatan": "Hindari aktivitas yang berisiko dan ikuti prosedur keselamatan."
    }
}

pilihan_gelombang = st.selectbox(
    "Pilih kondisi gelombang:",
    list(panduan_gelombang.keys()),
    key="panduan_gelombang_coastnote"
)

hasil_gelombang = panduan_gelombang[pilihan_gelombang]

st.subheader(f"🌊 Gelombang {pilihan_gelombang}")

st.metric(
    "Kisaran Tinggi Gelombang",
    hasil_gelombang["tinggi"]
)

st.write("**Karakteristik:**")
st.info(hasil_gelombang["ciri"])

st.write("**Pengaruh terhadap survei:**")
st.write(hasil_gelombang["dampak"])

st.warning(hasil_gelombang["peringatan"])

st.caption(
    "Kisaran di atas merupakan kategori panduan sederhana, "
    "bukan klasifikasi resmi BMKG. Tinggi gelombang harus "
    "diukur atau diperoleh dari sumber pengamatan yang valid."
)

# ==================================
# COASTNOTE - COASTAL ALERT CENTER
# ==================================

st.divider()

st.header("🚨 COASTAL ALERT CENTER")

st.write(
    "Pusat informasi potensi bahaya berdasarkan "
    "data kondisi pesisir."
)

st.caption(
    "Simulasi penilaian otomatis berdasarkan pilihan pengguna."
)

col1, col2 = st.columns(2)

with col1:
    cuaca_alert = st.selectbox(
        "Kondisi cuaca",
        ["Cerah", "Berawan", "Mendung", "Hujan"],
        key="alert_cuaca"
    )

with col2:
    gelombang_alert = st.selectbox(
        "Kondisi gelombang",
        ["Tenang", "Rendah", "Sedang", "Tinggi"],
        key="alert_gelombang"
    )

angin_alert = st.selectbox(
    "Kondisi angin",
    ["Lemah", "Sedang", "Kuat"],
    key="alert_angin"
)

hujan_lebat = st.checkbox(
    "Terdapat hujan lebat atau cuaca ekstrem"
)

st.divider()

# SISTEM PENILAIAN

skor = 0
alasan = []

if cuaca_alert == "Hujan":
    skor += 1
    alasan.append("Terdapat hujan di lokasi.")

if gelombang_alert == "Sedang":
    skor += 2
    alasan.append("Gelombang sedang perlu diwaspadai.")

elif gelombang_alert == "Tinggi":
    skor += 4
    alasan.append("Gelombang tinggi berpotensi mengganggu aktivitas pesisir.")

if angin_alert == "Sedang":
    skor += 1
    alasan.append("Angin sedang terpantau.")

elif angin_alert == "Kuat":
    skor += 3
    alasan.append("Angin kuat perlu diwaspadai.")

if hujan_lebat:
    skor += 4
    alasan.append("Hujan lebat atau cuaca ekstrem dilaporkan.")

# HASIL ANALISIS

st.subheader("📊 Hasil Analisis")

if gelombang_alert == "Tinggi" or hujan_lebat or (
    angin_alert == "Kuat" and cuaca_alert == "Hujan"
):
    st.error("🔴 STATUS: BAHAYA")

    st.write(
        "Ditemukan indikator kondisi yang berpotensi "
        "membahayakan aktivitas di wilayah pesisir."
    )

    st.warning(
        "Tunda aktivitas lapangan yang berisiko. "
        "Ikuti informasi resmi BMKG dan prosedur keselamatan."
    )

elif skor >= 2:
    st.warning("🟡 STATUS: WASPADA")

    st.write(
        "Terdapat kondisi lingkungan yang perlu "
        "dipantau lebih lanjut."
    )

    st.info(
        "Tingkatkan kewaspadaan dan periksa perubahan "
        "cuaca serta kondisi perairan."
    )

else:
    st.success("🟢 STATUS: TERKENDALI")

    st.write(
        "Belum ditemukan indikator peringatan dari "
        "parameter yang dipilih."
    )

    st.info(
        "Tetap pantau kondisi lingkungan dan informasi "
        "cuaca terbaru."
    )

st.subheader("🔎 Faktor yang Diperhatikan")

if alasan:
    for item in alasan:
        st.write("•", item)
else:
    st.write("Belum ada indikator khusus yang terdeteksi.")

st.caption(
    "Catatan: Ini merupakan prototipe aturan sederhana, "
    "bukan sistem peringatan resmi atau penilaian keselamatan. "
    "Belum menggunakan data BMKG secara langsung."
)


# ==========================================
# FITUR: COASTAL WASTE MONITOR
# ==========================================

st.divider()
st.header("🗑️ COASTAL WASTE MONITOR")
st.write(
    "Fitur pemantauan jenis, jumlah, dan kondisi sampah "
    "yang ditemukan di wilayah pesisir."
)

if "data_sampah_pesisir" not in st.session_state:
    st.session_state.data_sampah_pesisir = []

with st.expander("📝 Input Pengamatan Sampah", expanded=True):

    with st.form("form_monitor_sampah"):

        tanggal_sampah = st.date_input(
            "Tanggal pengamatan",
            value=date.today(),
            key="tanggal_sampah_baru"
        )

        lokasi_sampah = st.text_input(
            "Lokasi pengamatan",
            placeholder="Contoh: Pantai Sedari"
        )

        jenis_sampah = st.selectbox(
            "Jenis sampah yang ditemukan",
            [
                "Plastik",
                "Organik",
                "Kaca dan logam",
                "Jaring atau alat tangkap ikan",
                "Styrofoam",
                "Lainnya"
            ]
        )

        jumlah_sampah = st.number_input(
            "Jumlah sampah yang ditemukan (item)",
            min_value=1,
            step=1
        )

        kondisi_sampah = st.selectbox(
            "Kondisi persebaran sampah",
            [
                "Terkumpul di satu titik",
                "Tersebar di sepanjang pantai",
                "Mengapung di perairan",
                "Terdampar di sekitar mangrove"
            ]
        )

        catatan_sampah = st.text_area(
            "Catatan tambahan",
            placeholder="Tuliskan kondisi lokasi atau temuan lainnya."
        )

        simpan_sampah = st.form_submit_button(
            "Simpan Hasil Pengamatan"
        )

    if simpan_sampah:

        if not lokasi_sampah.strip():
            st.warning("Lokasi pengamatan harus diisi.")

        else:
            st.session_state.data_sampah_pesisir.append({
                "Tanggal": str(tanggal_sampah),
                "Lokasi": lokasi_sampah,
                "Jenis Sampah": jenis_sampah,
                "Jumlah": jumlah_sampah,
                "Persebaran": kondisi_sampah,
                "Catatan": catatan_sampah
            })

            st.success("Pengamatan sampah berhasil disimpan!")


# ==========================================
# ANALISIS DAMPAK SAMPAH
# ==========================================

st.subheader("🔎 Analisis Dampak dan Penanganan")

informasi_sampah = {
    "Plastik": {
        "dampak": "Dapat mencemari perairan, tertelan oleh biota laut, "
                  "dan terurai menjadi mikroplastik.",
        "penanganan": "Pisahkan berdasarkan jenis plastik dan salurkan "
                      "ke fasilitas pengelolaan atau daur ulang."
    },
    "Organik": {
        "dampak": "Penumpukan dapat menimbulkan bau dan mengganggu "
                  "kebersihan lingkungan pesisir.",
        "penanganan": "Pisahkan dari sampah anorganik dan kelola "
                      "sesuai jenis serta kondisinya."
    },
    "Kaca dan logam": {
        "dampak": "Pecahan kaca dan bagian logam dapat melukai "
                  "manusia maupun organisme di sekitar pantai.",
        "penanganan": "Jangan menyentuh benda tajam secara langsung. "
                      "Laporkan kepada petugas untuk penanganan aman."
    },
    "Jaring atau alat tangkap ikan": {
        "dampak": "Jaring yang tertinggal dapat menjerat biota laut "
                  "dan merusak habitat.",
        "penanganan": "Catat lokasi temuan dan laporkan kepada "
                      "petugas atau kelompok penanganan sampah laut."
    },
    "Styrofoam": {
        "dampak": "Mudah pecah menjadi bagian kecil dan dapat "
                  "terbawa arus ke perairan.",
        "penanganan": "Kumpulkan melalui petugas atau fasilitas "
                      "pengelolaan sampah yang sesuai."
    },
    "Lainnya": {
        "dampak": "Dampaknya bergantung pada bahan dan karakteristik "
                  "sampah yang ditemukan.",
        "penanganan": "Identifikasi bahan terlebih dahulu sebelum "
                      "menentukan cara pengelolaannya."
    }
}

pilih_analisis = st.selectbox(
    "Pilih jenis sampah untuk melihat analisis",
    list(informasi_sampah.keys()),
    key="analisis_jenis_sampah"
)

st.write("**Potensi dampak lingkungan:**")
st.info(informasi_sampah[pilih_analisis]["dampak"])

st.write("**Rekomendasi penanganan:**")
st.success(informasi_sampah[pilih_analisis]["penanganan"])


# ==========================================
# RIWAYAT PENGAMATAN SAMPAH
# ==========================================

st.subheader("📋 Riwayat Pengamatan Sampah")

if st.session_state.data_sampah_pesisir:

    data_sampah_df = pd.DataFrame(
        st.session_state.data_sampah_pesisir
    )

    st.dataframe(
        data_sampah_df,
        use_container_width=True
    )

    total_item_sampah = data_sampah_df["Jumlah"].sum()

    st.metric(
        "Total Sampah Tercatat",
        f"{total_item_sampah} item"
    )

    st.download_button(
        "⬇️ Unduh Data Pengamatan Sampah",
        data=data_sampah_df.to_csv(
            index=False
        ).encode("utf-8-sig"),
        file_name="data_sampah_pesisir.csv",
        mime="text/csv"
    )

else:
    st.info(
        "Belum ada data sampah. Silakan lakukan pengamatan "
        "dan simpan hasilnya melalui formulir di atas."
    )


    # ==========================================
# PRIORITAS PENANGANAN SAMPAH PESISIR
# ==========================================

st.divider()
st.header("🚨 PRIORITAS PENANGANAN SAMPAH")

if st.session_state.data_sampah_pesisir:

    df_prioritas = pd.DataFrame(
        st.session_state.data_sampah_pesisir
    )

    st.write(
        "Sistem mengidentifikasi temuan yang perlu "
        "mendapat perhatian berdasarkan jenis sampah."
    )

    jenis_berisiko = [
        "Kaca dan logam",
        "Jaring atau alat tangkap ikan"
    ]

    for _, baris in df_prioritas.iterrows():

        jenis = baris["Jenis Sampah"]
        lokasi = baris["Lokasi"]
        jumlah = baris["Jumlah"]

        if jenis == "Sampah medis atau benda berbahaya":
            st.error(
                f"PRIORITAS KESELAMATAN | {lokasi}\n\n"
                f"Temuan: {jenis} ({jumlah} item)\n\n"
                "Jangan disentuh atau dipindahkan. "
                "Jauhkan orang dari lokasi dan laporkan "
                "kepada petugas berwenang."
            )

        elif jenis in jenis_berisiko:
            st.warning(
                f"PERLU PENANGANAN | {lokasi}\n\n"
                f"Temuan: {jenis} ({jumlah} item)\n\n"
                "Berpotensi membahayakan manusia atau biota. "
                "Catat lokasi dan laporkan kepada petugas "
                "untuk penanganan yang aman."
            )

        elif jumlah >= 50:
            st.info(
                f"PERLU PEMANTAUAN LANJUTAN | {lokasi}\n\n"
                f"Temuan: {jenis} ({jumlah} item)\n\n"
                "Jumlah temuan cukup banyak berdasarkan "
                "catatan ini. Periksa kembali area pengamatan "
                "dan lakukan pendataan lanjutan."
            )

        else:
            st.success(
                f"PEMANTAUAN RUTIN | {lokasi}\n\n"
                f"Temuan: {jenis} ({jumlah} item)\n\n"
                "Masukkan dalam catatan pemantauan rutin."
            )

    st.caption(
        "Prioritas ini merupakan penyaringan awal, bukan "
        "penilaian resmi tingkat pencemaran. Jumlah sampah "
        "perlu mempertimbangkan luas area pengamatan."
    )

else:
    st.info(
        "Belum ada data. Simpan pengamatan sampah terlebih dahulu."
    )


    # ==========================================
# TIDE MONITOR - PEMANTAUAN PASANG SURUT
# ==========================================

st.divider()
st.header("🌊 TIDE MONITOR")
st.write(
    "Pemantauan perubahan tinggi muka air laut "
    "berdasarkan hasil pengamatan pasang surut."
)

if "data_pasang_surut" not in st.session_state:
    st.session_state.data_pasang_surut = []

with st.expander("📝 Input Data Pasang Surut", expanded=True):

    with st.form("form_pasang_surut"):

        tanggal_tide = st.date_input(
            "Tanggal pengamatan",
            value=date.today(),
            key="tanggal_tide"
        )

        waktu_tide = st.time_input(
            "Waktu pengamatan",
            key="waktu_tide"
        )

        lokasi_tide = st.text_input(
            "Lokasi pengamatan",
            placeholder="Contoh: Pantai Sedari",
            key="lokasi_tide"
        )

        tinggi_air = st.number_input(
            "Tinggi muka air laut (meter)",
            min_value=0.0,
            max_value=20.0,
            value=1.0,
            step=0.01
        )

        simpan_tide = st.form_submit_button(
            "Simpan Data Pasang Surut"
        )

    if simpan_tide:

        if not lokasi_tide.strip():
            st.warning("Lokasi pengamatan harus diisi.")

        else:
            st.session_state.data_pasang_surut.append({
                "Tanggal": str(tanggal_tide),
                "Waktu": str(waktu_tide),
                "Lokasi": lokasi_tide,
                "Tinggi Air (m)": tinggi_air
            })

            st.success("Data pasang surut berhasil disimpan!")


# ==========================================
# GRAFIK PASANG SURUT
# ==========================================

st.subheader("📈 Grafik Perubahan Muka Air Laut")

if st.session_state.data_pasang_surut:

    df_tide = pd.DataFrame(
        st.session_state.data_pasang_surut
    )

    df_tide["Waktu Pengamatan"] = pd.to_datetime(
        df_tide["Tanggal"] + " " + df_tide["Waktu"]
    )

    df_tide = df_tide.sort_values("Waktu Pengamatan")

    st.line_chart(
        df_tide.set_index("Waktu Pengamatan")[
            "Tinggi Air (m)"
        ],
        color="#557FA3"
    )

    tertinggi = df_tide.loc[
        df_tide["Tinggi Air (m)"].idxmax()
    ]

    terendah = df_tide.loc[
        df_tide["Tinggi Air (m)"].idxmin()
    ]

    col1, col2 = st.columns(2)

    col1.metric(
        "Muka Air Tertinggi",
        f'{tertinggi["Tinggi Air (m)"]:.2f} m'
    )

    col2.metric(
        "Muka Air Terendah",
        f'{terendah["Tinggi Air (m)"]:.2f} m'
    )

    st.write("**Waktu pengamatan tertinggi:**")
    st.write(
        tertinggi["Waktu Pengamatan"].strftime(
            "%d-%m-%Y %H:%M"
        )
    )

    st.write("**Waktu pengamatan terendah:**")
    st.write(
        terendah["Waktu Pengamatan"].strftime(
            "%d-%m-%Y %H:%M"
        )
    )

    st.subheader("📋 Riwayat Data Pasang Surut")

    st.dataframe(
        df_tide[
            ["Tanggal", "Waktu", "Lokasi", "Tinggi Air (m)"]
        ],
        use_container_width=True
    )

    st.download_button(
        "⬇️ Unduh Data Pasang Surut",
        data=df_tide[
            ["Tanggal", "Waktu", "Lokasi", "Tinggi Air (m)"]
        ].to_csv(index=False).encode("utf-8-sig"),
        file_name="data_pasang_surut.csv",
        mime="text/csv"
    )

else:
    st.info(
        "Belum ada data pasang surut. Masukkan hasil "
        "pengamatan untuk menampilkan grafik."
    )

st.caption(
    "Grafik dibuat berdasarkan data pengamatan yang dimasukkan. "
    "Pengukuran tinggi air harus menggunakan titik acuan "
    "yang konsisten agar dapat dibandingkan."
)


# ==========================================
# ANALISIS PASANG DAN SURUT
# ==========================================

st.divider()
st.header("🌊 ANALISIS KONDISI PASANG SURUT")

if st.session_state.data_pasang_surut:

    df_analisis_tide = pd.DataFrame(
        st.session_state.data_pasang_surut
    )

    df_analisis_tide["Waktu Pengamatan"] = pd.to_datetime(
        df_analisis_tide["Tanggal"] + " " +
        df_analisis_tide["Waktu"]
    )

    df_analisis_tide = df_analisis_tide.sort_values(
        "Waktu Pengamatan"
    )

    tinggi_maksimum = df_analisis_tide[
        "Tinggi Air (m)"
    ].max()

    tinggi_minimum = df_analisis_tide[
        "Tinggi Air (m)"
    ].min()

    selisih_air = tinggi_maksimum - tinggi_minimum

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🌊 Tinggi Pasang Tertinggi",
        f"{tinggi_maksimum:.2f} m"
    )

    col2.metric(
        "🏖️ Tinggi Surut Terendah",
        f"{tinggi_minimum:.2f} m"
    )

    col3.metric(
        "↕️ Rentang Pasang Surut",
        f"{selisih_air:.2f} m"
    )

    st.subheader("📖 Penjelasan Hasil Pengamatan")

    st.write(
        f"""
        Berdasarkan data yang dimasukkan:

        - **Pasang tertinggi:** {tinggi_maksimum:.2f} meter.
        - **Surut terendah:** {tinggi_minimum:.2f} meter.
        - **Rentang perubahan muka air:** {selisih_air:.2f} meter.
        """
    )

    st.info(
        "Nilai tertinggi dan terendah merupakan hasil "
        "pengamatan dalam kumpulan data yang tersimpan. "
        "Nilai tersebut belum tentu mewakili pasang tertinggi "
        "dan surut terendah dalam satu siklus pasang surut."
    )

    st.subheader("🔍 Kondisi Pengamatan Terakhir")

    tinggi_terakhir = df_analisis_tide.iloc[-1][
        "Tinggi Air (m)"
    ]

    if len(df_analisis_tide) >= 2:

        tinggi_sebelumnya = df_analisis_tide.iloc[-2][
            "Tinggi Air (m)"
        ]

        if tinggi_terakhir > tinggi_sebelumnya:
            st.success(
                "MUKA AIR SEDANG NAIK — menunjukkan kecenderungan pasang."
            )

        elif tinggi_terakhir < tinggi_sebelumnya:
            st.warning(
                "MUKA AIR SEDANG TURUN — menunjukkan kecenderungan surut."
            )

        else:
            st.info(
                "MUKA AIR TETAP — belum terlihat perubahan "
                "pada dua pengamatan terakhir."
            )

    else:
        st.info(
            "Masukkan minimal dua data pengamatan "
            "untuk mengetahui kecenderungan pasang atau surut."
        )

else:
    st.info(
        "Masukkan data pasang surut terlebih dahulu "
        "untuk menampilkan analisis."
    )


    # ==========================================
# MANGROVE MONITOR
# ==========================================

st.divider()
st.header("🌱 MANGROVE MONITOR")
st.write(
    "Sistem pencatatan dan pemantauan kondisi ekosistem "
    "mangrove di wilayah pesisir."
)

if "data_mangrove" not in st.session_state:
    st.session_state.data_mangrove = []


# ==========================================
# INPUT PENGAMATAN MANGROVE
# ==========================================

st.subheader("📝 Form Pengamatan Mangrove")

with st.form("form_monitor_mangrove"):

    tanggal_mangrove = st.date_input(
        "Tanggal pengamatan",
        value=date.today(),
        key="tanggal_mangrove_monitor"
    )

    lokasi_mangrove = st.text_input(
        "Lokasi pengamatan",
        placeholder="Contoh: Kawasan mangrove Desa Sedari"
    )

    jenis_mangrove = st.selectbox(
        "Jenis mangrove",
        [
            "Rhizophora sp.",
            "Avicennia sp.",
            "Sonneratia sp.",
            "Bruguiera sp.",
            "Ceriops sp.",
            "Belum diketahui"
        ]
    )

    kondisi_mangrove = st.selectbox(
        "Kondisi vegetasi",
        [
            "Sangat baik",
            "Baik",
            "Sedang",
            "Rusak",
            "Rusak berat"
        ]
    )

    kerapatan = st.selectbox(
        "Kerapatan vegetasi",
        [
            "Rapat",
            "Sedang",
            "Jarang",
            "Sangat jarang"
        ]
    )

    tanda_kerusakan = st.multiselect(
        "Tanda-tanda yang ditemukan",
        [
            "Daun menguning",
            "Daun mengering",
            "Pohon tumbang",
            "Akar terbuka",
            "Batang mengalami kerusakan",
            "Sampah menumpuk",
            "Terjadi pengikisan substrat",
            "Tidak ditemukan kerusakan"
        ]
    )

    kondisi_substrat = st.selectbox(
        "Kondisi substrat",
        [
            "Lumpur",
            "Pasir berlumpur",
            "Pasir",
            "Berlumpur dan banyak sampah",
            "Lainnya"
        ]
    )

    catatan_mangrove = st.text_area(
        "Catatan tambahan",
        placeholder="Tuliskan hasil pengamatan di lapangan."
    )

    simpan_mangrove = st.form_submit_button(
        "Simpan Pengamatan Mangrove"
    )

if simpan_mangrove:

    if not lokasi_mangrove.strip():
        st.warning("Lokasi pengamatan harus diisi.")

    else:

        st.session_state.data_mangrove.append({
            "Tanggal": str(tanggal_mangrove),
            "Lokasi": lokasi_mangrove,
            "Jenis Mangrove": jenis_mangrove,
            "Kondisi Vegetasi": kondisi_mangrove,
            "Kerapatan": kerapatan,
            "Tanda Kerusakan": ", ".join(tanda_kerusakan),
            "Substrat": kondisi_substrat,
            "Catatan": catatan_mangrove
        })

        st.success("Data pengamatan mangrove berhasil disimpan!")


# ==========================================
# ANALISIS KONDISI MANGROVE
# ==========================================

st.divider()
st.subheader("🔎 ANALISIS KONDISI MANGROVE")

analisis_mangrove = {

    "Sangat baik": {
        "dampak": "Vegetasi menunjukkan kondisi yang mendukung "
                  "fungsi perlindungan pantai dan habitat biota.",
        "saran": "Pertahankan kondisi kawasan dan lakukan "
                 "pemantauan secara berkala."
    },

    "Baik": {
        "dampak": "Vegetasi relatif terjaga, tetapi tetap perlu "
                  "diperhatikan kemungkinan gangguan lingkungan.",
        "saran": "Lakukan pemantauan pertumbuhan dan kebersihan kawasan."
    },

    "Sedang": {
        "dampak": "Terdapat indikasi penurunan kondisi vegetasi "
                  "yang perlu diamati lebih lanjut.",
        "saran": "Identifikasi penyebab gangguan dan pantau "
                 "perubahan kondisi vegetasi."
    },

    "Rusak": {
        "dampak": "Fungsi ekosistem mangrove dapat terganggu "
                  "dan perlindungan alami pantai berkurang.",
        "saran": "Lakukan penilaian lapangan untuk menentukan "
                 "penyebab kerusakan dan kebutuhan rehabilitasi."
    },

    "Rusak berat": {
        "dampak": "Kerusakan vegetasi dapat memengaruhi habitat "
                  "biota dan kestabilan kawasan pesisir.",
        "saran": "Prioritaskan kajian kondisi kawasan dan "
                 "penanganan bersama pihak terkait."
    }
}

pilihan_analisis_mangrove = st.selectbox(
    "Pilih kondisi mangrove untuk melihat analisis",
    list(analisis_mangrove.keys()),
    key="pilihan_analisis_mangrove"
)

st.write("**Dampak terhadap ekosistem:**")

st.info(
    analisis_mangrove[pilihan_analisis_mangrove]["dampak"]
)

st.write("**Rekomendasi:**")

st.success(
    analisis_mangrove[pilihan_analisis_mangrove]["saran"]
)


# ==========================================
# FUNGSI EKOLOGIS MANGROVE
# ==========================================

st.divider()
st.subheader("🌿 FUNGSI EKOSISTEM MANGROVE")

fungsi_mangrove = {
    "Pelindung pantai":
        "Mengurangi energi gelombang dan membantu "
        "menstabilkan sedimen di kawasan pesisir.",

    "Habitat biota":
        "Menjadi tempat berlindung, mencari makan, "
        "dan berkembang biak bagi berbagai organisme.",

    "Penyerap karbon":
        "Menyimpan karbon pada biomassa vegetasi "
        "dan sedimen mangrove.",

    "Penyaring alami":
        "Vegetasi dan sedimennya dapat membantu "
        "menahan sebagian material yang terbawa aliran air."
}

for nama_fungsi, penjelasan in fungsi_mangrove.items():

    with st.expander(nama_fungsi):
        st.write(penjelasan)


# ==========================================
# RIWAYAT PENGAMATAN MANGROVE
# ==========================================

st.divider()
st.subheader("📋 RIWAYAT PENGAMATAN MANGROVE")

if st.session_state.data_mangrove:

    df_mangrove = pd.DataFrame(
        st.session_state.data_mangrove
    )

    st.dataframe(
        df_mangrove,
        use_container_width=True
    )

    total_pengamatan = len(df_mangrove)

    st.metric(
        "Total Pengamatan Mangrove",
        total_pengamatan
    )

    st.download_button(
        "⬇️ Unduh Data Mangrove",
        data=df_mangrove.to_csv(
            index=False
        ).encode("utf-8-sig"),
        file_name="data_pengamatan_mangrove.csv",
        mime="text/csv"
    )

else:

    st.info(
        "Belum ada data mangrove. Silakan masukkan "
        "hasil pengamatan terlebih dahulu."
    )

st.caption(
    "Analisis kondisi merupakan penilaian awal berdasarkan "
    "pengamatan visual, bukan hasil inventarisasi atau "
    "penilaian kesehatan mangrove secara ilmiah."
)


# ==========================================
# 🐚 BIOTA PESISIR
# ==========================================

if "data_biota" not in st.session_state:
    st.session_state.data_biota = []

st.markdown("---")
st.header("🐚 BIOTA PESISIR")
st.caption("Pencatatan kondisi dan keberadaan biota di wilayah pesisir.")

with st.expander("📝 Input Pengamatan Biota", expanded=True):
    with st.form("form_biota"):
        tanggal_biota = st.date_input(
            "Tanggal pengamatan",
            value=date.today(),
            key="tanggal_biota"
        )

        lokasi_biota = st.text_input("Lokasi pengamatan")

        jenis_biota = st.selectbox(
            "Jenis biota",
            [
                "Ikan",
                "Kepiting",
                "Kerang",
                "Udang",
                "Bintang laut",
                "Teripang",
                "Burung pantai",
                "Biota mangrove",
                "Lainnya"
            ]
        )

        jumlah_biota = st.number_input(
            "Perkiraan jumlah biota yang terlihat",
            min_value=0,
            step=1
        )

        kondisi_biota = st.selectbox(
            "Kondisi biota",
            [
                "Aktif dan terlihat sehat",
                "Jumlah terlihat sedikit",
                "Ditemukan dalam kondisi lemah",
                "Ditemukan mati",
                "Tidak ditemukan"
            ]
        )

        habitat_biota = st.selectbox(
            "Habitat pengamatan",
            [
                "Perairan pantai",
                "Ekosistem mangrove",
                "Hamparan pasir",
                "Lumpur pesisir",
                "Padang lamun",
                "Lainnya"
            ]
        )

        catatan_biota = st.text_area("Catatan tambahan")

        simpan_biota = st.form_submit_button(
            "Simpan Pengamatan Biota"
        )

        if simpan_biota:
            st.session_state.data_biota.append({
                "Tanggal": str(tanggal_biota),
                "Lokasi": lokasi_biota,
                "Jenis Biota": jenis_biota,
                "Jumlah": jumlah_biota,
                "Kondisi": kondisi_biota,
                "Habitat": habitat_biota,
                "Catatan": catatan_biota
            })

            st.success("Pengamatan biota berhasil disimpan!")

# ANALISIS BIOTA
st.subheader("🔎 Analisis Pengamatan")

if st.session_state.data_biota:
    df_biota = pd.DataFrame(st.session_state.data_biota)

    total_biota = int(df_biota["Jumlah"].sum())
    jenis_tercatat = df_biota["Jenis Biota"].nunique()

    col1, col2 = st.columns(2)

    col1.metric("Total perkiraan biota", total_biota)
    col2.metric("Jenis biota tercatat", jenis_tercatat)

    st.markdown("**Jumlah pengamatan berdasarkan jenis biota**")
    grafik_biota = df_biota.groupby(
        "Jenis Biota"
    )["Jumlah"].sum()

    st.bar_chart(grafik_biota)

    st.markdown("**Catatan kondisi biota**")

    for _, baris in df_biota.iterrows():
        st.write(
            f"**{baris['Jenis Biota']} — {baris['Lokasi']}**"
        )

        if baris["Kondisi"] == "Ditemukan mati":
            st.warning(
                "Perlu pemeriksaan lebih lanjut terhadap kondisi habitat dan kualitas lingkungan."
            )
        elif baris["Kondisi"] == "Jumlah terlihat sedikit":
            st.info(
                "Lakukan pengamatan ulang untuk mengetahui apakah jumlah biota mengalami perubahan."
            )
        elif baris["Kondisi"] == "Ditemukan dalam kondisi lemah":
            st.warning(
                "Catat kondisi lingkungan sekitar dan lakukan pemantauan lanjutan."
            )
        else:
            st.success(
                "Catatan pengamatan tersimpan. Lanjutkan pemantauan secara berkala."
            )

    st.subheader("📋 Riwayat Pengamatan Biota")
    st.dataframe(df_biota, use_container_width=True)

    csv_biota = df_biota.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Unduh Data Biota",
        data=csv_biota,
        file_name="data_biota_pesisir.csv",
        mime="text/csv"
    )

else:
    st.info("Belum ada data pengamatan biota.")


    # ==========================================
# 📊 KESIMPULAN KONDISI PESISIR
# ==========================================

st.markdown("---")
st.header("📊 KESIMPULAN KONDISI PESISIR")

st.write(
    "Ringkasan ini dibuat berdasarkan data pengamatan "
    "yang telah dimasukkan ke dalam COASTNOTE."
)

jumlah_aspek = 0
ringkasan = []

# DATA SAMPAH
if st.session_state.get("data_sampah_pesisir"):
    df_s = pd.DataFrame(st.session_state.data_sampah_pesisir)
    jumlah_aspek += 1
    total_sampah = df_s["Jumlah"].sum()

    ringkasan.append(
        f"**Sampah pesisir:** Tercatat sebanyak "
        f"{total_sampah} sampah berdasarkan seluruh data pengamatan."
    )

# DATA MANGROVE
if st.session_state.get("data_mangrove"):
    df_m = pd.DataFrame(st.session_state.data_mangrove)
    jumlah_aspek += 1
    kondisi = df_m["Kondisi"].value_counts()

    kondisi_dominan = kondisi.index[0]

    ringkasan.append(
        f"**Mangrove:** Kondisi yang paling banyak tercatat "
        f"adalah {kondisi_dominan}."
    )

# DATA PASANG SURUT
if st.session_state.get("data_pasang_surut"):
    df_t = pd.DataFrame(st.session_state.data_pasang_surut)
    jumlah_aspek += 1

    tinggi = pd.to_numeric(
        df_t["Tinggi Air (m)"], errors="coerce"
    ).dropna()

    if not tinggi.empty:
        ringkasan.append(
            f"**Pasang surut:** Tinggi air tertinggi yang tercatat "
            f"{tinggi.max():.2f} m dan terendah "
            f"{tinggi.min():.2f} m."
        )

# DATA BIOTA
if st.session_state.get("data_biota"):
    df_b = pd.DataFrame(st.session_state.data_biota)
    jumlah_aspek += 1

    total_biota = df_b["Jumlah"].sum()
    jenis_biota = df_b["Jenis Biota"].nunique()

    ringkasan.append(
        f"**Biota pesisir:** Tercatat {jenis_biota} jenis biota "
        f"dengan perkiraan jumlah keseluruhan {total_biota}."
    )


# ==========================================
# 📊 KESIMPULAN KONDISI PESISIR
# ==========================================

st.markdown("---")
st.header("📊 KESIMPULAN KONDISI PESISIR")

st.write(
    "Ringkasan ini dibuat berdasarkan data pengamatan "
    "yang telah dimasukkan ke dalam COASTNOTE."
)

jumlah_aspek = 0
ringkasan = []

# DATA SAMPAH
if st.session_state.get("data_sampah_pesisir"):
    df_s = pd.DataFrame(st.session_state.data_sampah_pesisir)
    jumlah_aspek += 1
    total_sampah = df_s["Jumlah"].sum()

    ringkasan.append(
        f"**Sampah pesisir:** Tercatat sebanyak "
        f"{total_sampah} sampah berdasarkan seluruh data pengamatan."
    )

# DATA MANGROVE
if st.session_state.get("data_mangrove"):
    df_m = pd.DataFrame(st.session_state.data_mangrove)
    jumlah_aspek += 1
    kondisi = df_m["Kondisi"].value_counts()

    kondisi_dominan = kondisi.index[0]

    ringkasan.append(
        f"**Mangrove:** Kondisi yang paling banyak tercatat "
        f"adalah {kondisi_dominan}."
    )

# DATA PASANG SURUT
if st.session_state.get("data_pasang_surut"):
    df_t = pd.DataFrame(st.session_state.data_pasang_surut)
    jumlah_aspek += 1

    tinggi = pd.to_numeric(
        df_t["Tinggi Air (m)"], errors="coerce"
    ).dropna()

    if not tinggi.empty:
        ringkasan.append(
            f"**Pasang surut:** Tinggi air tertinggi yang tercatat "
            f"{tinggi.max():.2f} m dan terendah "
            f"{tinggi.min():.2f} m."
        )

# DATA BIOTA
if st.session_state.get("data_biota"):
    df_b = pd.DataFrame(st.session_state.data_biota)
    jumlah_aspek += 1

    total_biota = df_b["Jumlah"].sum()
    jenis_biota = df_b["Jenis Biota"].nunique()

    ringkasan.append(
        f"**Biota pesisir:** Tercatat {jenis_biota} jenis biota "
        f"dengan perkiraan jumlah keseluruhan {total_biota}."
    )

# TAMPILAN KESIMPULAN
if jumlah_aspek > 0:
    st.subheader("Hasil Ringkasan Pengamatan")

    for item in ringkasan:
        st.markdown(f"- {item}")

    st.success(
        f"COASTNOTE telah memiliki data pengamatan "
        f"dari {jumlah_aspek} aspek lingkungan pesisir."
    )

    st.info(
        "Kesimpulan ini merupakan ringkasan data yang dimasukkan, "
        "bukan penilaian resmi kondisi lingkungan pesisir."
    )

else:
    st.warning(
        "Belum tersedia data pengamatan. "
        "Masukkan data pada fitur monitoring terlebih dahulu."
    )

st.caption(
    "COASTNOTE | Catatan dan Monitoring Wilayah Pesisir"
)