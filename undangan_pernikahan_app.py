# app.py
# Digital Wedding Invitation using Streamlit
# Features:
# - Display names and wedding date
# - Automatic countdown to wedding (client-side JavaScript)
# - Location with Google Maps embed (replace with your embed link)
# - Photo gallery for couple (upload or place images in /static and reference)
# - Wishes / messages section
# - Bank account number and shipping address for gifts
# - Background floral on every page
# - Play a romantic song (replace with your file or a legal URL)

import streamlit as st
from datetime import datetime
import base64
import textwrap

st.set_page_config(page_title="Undangan Pernikahan", layout="centered")

# ----------------------
# === CONFIGURATION ===
# Ganti nilai-nilai di bawah ini dengan data pasangan Anda
BRIDE_NAME = "Nama Mempelai Wanita"
GROOM_NAME = "Nama Mempelai Pria"
WEDDING_DATE = "2026-02-14 10:00:00"  # format: YYYY-MM-DD HH:MM:SS (Waktu acara)
LOCATION_NAME = "Gedung Contoh / Masjid / Gereja"
MAP_EMBED_URL = "https://www.google.com/maps/embed?pb=REPLACE_WITH_YOUR_EMBED"
BANK_DETAILS = "Bank ABC - 1234567890 (Nama Pemilik)"
SHIPPING_ADDRESS = "Jalan Contoh No.123, Kecamatan, Kota, Provinsi, Kode Pos"
MUSIC_FILE = "path_to_song.mp3"  # letakkan file mp3 di folder 'static' atau gunakan URL yang legal

# Optional: paths to couple photos (you can also use Streamlit file_uploader to let user upload)
COUPLE_PHOTOS = ["static/couple1.jpg", "static/couple2.jpg"]

# ----------------------
# === Helper CSS & SVG background ===
# We'll use an inline SVG floral pattern encoded as data URI so pages keep a consistent floral background.
floral_svg = '''<svg xmlns='http://www.w3.org/2000/svg' width='800' height='600'>
  <defs>
    <pattern id='p' width='200' height='200' patternUnits='userSpaceOnUse'>
      <rect width='200' height='200' fill='%23fffaf6'/>
      <g transform='scale(0.9)'>
        <circle cx='40' cy='40' r='6' fill='%23f8c7d1' opacity='0.9'/>
        <circle cx='80' cy='70' r='4' fill='%23ffdede' opacity='0.9'/>
        <path d='M160 120c-10-15-40-10-50 6' stroke='%23f6b9c7' stroke-width='2' fill='none' opacity='0.6'/>
        <path d='M20 160c8-12 28-18 40-8' stroke='%23fce9f0' stroke-width='3' fill='none' opacity='0.5'/>
      </g>
    </pattern>
  </defs>
  <rect width='100%' height='100%' fill='url(%23p)' />
</svg>'''

floral_data_uri = 'data:image/svg+xml;utf8,' + floral_svg.replace('\n', '')

page_style = f"""
<style>
    .main-bg {{
        background-image: url("{floral_data_uri}");
        background-size: cover;
        background-attachment: fixed;
    }}
    .card {{
        background: rgba(255,255,255,0.85);
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    }}
    .title {{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 6px;
    }}
    .subtitle {{
        font-size: 16px;
        color: #555;
        margin-bottom: 12px;
    }}
    .countdown {{
        font-size: 28px;
        font-weight: 600;
        margin: 6px 0;
    }}
    .small {{font-size:14px;color:#333}}
</style>
"""

# Apply background style (we insert a wrapper div around Streamlit content using HTML injection)
st.markdown(page_style, unsafe_allow_html=True)

# Top-level layout container
st.markdown("<div class='main-bg' style='padding:30px;'>", unsafe_allow_html=True)

# Sidebar for page navigation
page = st.sidebar.radio("Menu", ["Beranda", "Lokasi", "Galeri", "Ucapan & Hadiah"])

# Common header card
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='title'>{BRIDE_NAME}  &amp;  {GROOM_NAME}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>Kami mengundang Anda untuk hadir pada hari bahagia kami</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# === Page: Beranda ===
if page == "Beranda":
    st.markdown("<div class='card' style='margin-top:14px;'>", unsafe_allow_html=True)
    st.markdown("<h3>Hitung Mundur Menuju Hari H</h3>", unsafe_allow_html=True)

    # JavaScript countdown (client-side) so it updates live without server loops
    # It also shows the wedding date in a readable format
    wedding_dt = datetime.fromisoformat(WEDDING_DATE)
    wedding_iso = wedding_dt.isoformat()

    countdown_html = f"""
    <div id='countdown' class='countdown'></div>
    <div class='small'>Acara: {wedding_dt.strftime('%A, %d %B %Y %H:%M')}</div>
    <script>
    const target = new Date('{wedding_iso}');
    function updateCountdown() {{
      const now = new Date();
      let diff = target - now;
      if (diff < 0) {{ document.getElementById('countdown').innerText = 'Sudah Berlangsung!'; return; }}
      const days = Math.floor(diff / (1000*60*60*24));
      diff -= days*(1000*60*60*24);
      const hrs = Math.floor(diff / (1000*60*60));
      diff -= hrs*(1000*60*60);
      const mins = Math.floor(diff / (1000*60));
      diff -= mins*(1000);
      const secs = Math.floor(diff/1000);
      document.getElementById('countdown').innerText = days + ' hari ' + hrs + ' jam ' + mins + ' mnt ' + secs + ' dtk';
    }}
    updateCountdown();
    setInterval(updateCountdown, 1000);
    </script>
    """

    st.components.v1.html(countdown_html, height=120)

    st.markdown("<hr/>", unsafe_allow_html=True)

    # Couple images
    cols = st.columns([1,1])
    try:
        cols[0].image(COUPLE_PHOTOS[0], caption=BRIDE_NAME, use_column_width=True)
    except Exception:
        cols[0].write("Upload foto mempelai di folder /static atau gunakan fitur unggah di halaman Galeri")
    try:
        cols[1].image(COUPLE_PHOTOS[1], caption=GROOM_NAME, use_column_width=True)
    except Exception:
        cols[1].write("")

    st.markdown("</div>", unsafe_allow_html=True)

    # Music player (use Streamlit's audio if file is available)
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h4>Musik Romantis</h4>", unsafe_allow_html=True)
    try:
        # If the developer placed the file in the static folder, you can open and play it
        with open(MUSIC_FILE, 'rb') as f:
            audio_bytes = f.read()
            st.audio(audio_bytes, format='audio/mp3')
            st.write("Jika autoplay diblokir oleh browser, tekan tombol play.")
    except Exception:
        st.write("Tidak menemukan file musik. Letakkan file .mp3 di path yang ditentukan atau gunakan URL legal pada variable MUSIC_FILE.")
    st.markdown("</div>", unsafe_allow_html=True)

# === Page: Lokasi ===
elif page == "Lokasi":
    st.markdown("<div class='card' style='margin-top:14px;'>", unsafe_allow_html=True)
    st.markdown(f"<h3>Lokasi Acara: {LOCATION_NAME}</h3>", unsafe_allow_html=True)
    st.markdown("<p>Silakan lihat peta di bawah untuk petunjuk lokasi.</p>", unsafe_allow_html=True)
    # Embed Google Maps iframe (user should replace MAP_EMBED_URL with their embed link)
    iframe_html = f"<iframe src='{MAP_EMBED_URL}' width='100%' height='400' style='border:0;' allowfullscreen='' loading='lazy'></iframe>"
    st.components.v1.html(iframe_html, height=420)
    st.markdown("</div>", unsafe_allow_html=True)

# === Page: Galeri ===
elif page == "Galeri":
    st.markdown("<div class='card' style='margin-top:14px;'>", unsafe_allow_html=True)
    st.markdown("<h3>Galeri Foto</h3>", unsafe_allow_html=True)
    st.write("Anda dapat mengunggah foto pasangan di bawah ini (akan muncul setelah unggah).")
    uploaded = st.file_uploader("Unggah foto (jpg/png)", type=['png','jpg','jpeg'], accept_multiple_files=True)
    if uploaded:
        cols = st.columns(3)
        for i, file in enumerate(uploaded):
            cols[i%3].image(file, use_column_width=True)
    else:
        st.write("Belum ada foto terunggah. Anda juga bisa menaruh foto ke folder ./static dan mengisi COUPLE_PHOTOS di file app.py")
    st.markdown("</div>", unsafe_allow_html=True)

# === Page: Ucapan & Hadiah ===
elif page == "Ucapan & Hadiah":
    st.markdown("<div class='card' style='margin-top:14px;'>", unsafe_allow_html=True)
    st.markdown("<h3>Ucapan</h3>", unsafe_allow_html=True)
    st.write("Tulis ucapan Anda untuk mempelai:")
    message = st.text_area("Ucapan singkat", "Selamat menempuh hidup baru...")
    if st.button("Kirim Ucapan"):
        st.success("Ucapan terkirim! Terima kasih.")

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("<h3>Hadiah & Donasi</h3>", unsafe_allow_html=True)
    st.markdown(f"**Nomor Rekening / Transfer:** {BANK_DETAILS}")
    st.markdown(f"**Alamat Pengiriman Hadiah:** {SHIPPING_ADDRESS}")
    st.markdown("<p>Jika ingin mengirim hadiah fisik, gunakan alamat di atas. Untuk transfer, gunakan nomor rekening yang tertera dan kirimkan bukti via chat/WA ke nomor yang Anda berikan kepada tamu.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Closing wrapper div
st.markdown("</div>", unsafe_allow_html=True)

# =====================
# Notes for the user (non-sensitive): how to run
# Save this file as app.py in a project folder. Create a folder named 'static' next to it and place photos and the mp3 there.
# Install dependencies: pip install streamlit
# Run: streamlit run app.py



