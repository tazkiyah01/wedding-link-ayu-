import streamlit as st
from datetime import datetime
import time
import os

# ================== CONFIG DATA ==================
CONFIG = {
    "bride": "Ajeng Nimasuri",
    "groom": "Saka Suryo Baskoro",
    "date": "2025-11-15 08:00:00",
    "location": "Pendopo Hegar Manah Ranggamekar, Bogor Selatan, Jawa Barat 16136",
    "map_embed": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3966.0527146742144!2d106.789!3d-6.252!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2e69ef9dabcde123%3A0x111222333444555!2sPendopo%20Hegar%20Manah!5e0!3m2!1sid!2sid!4v1700000000000",
    "rekening": {
        "bank": "BCA",
        "atas_nama": "Saka Suryo Baskoro",
        "nomor": "1234567890"
    },
    "alamat_rumah": "Jl. Melati No. 12, Bogor Selatan, Jawa Barat",
}

# =============== STYLING ===============
st.set_page_config(
    page_title="Undangan Pernikahan",
    page_icon="💍",
    layout="centered",
)

page_bg = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("file://{os.path.abspath('static/bg_flowers.jpg')}");
    background-size: cover;
    background-attachment: fixed;
    color: white;
    text-align: center;
}}
h1, h2, h3, h4 {{
    color: white;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
}}
div.block-container {{
    background: rgba(0,0,0,0.6);
    padding: 2rem;
    border-radius: 20px;
}}
button[kind="primary"] {{
    background-color: #f6d365 !important;
    color: black !important;
}}
iframe {{
    border-radius: 15px;
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ================== HEADER ==================
st.title("💖 Undangan Pernikahan 💖")
st.subheader(f"{CONFIG['bride']} & {CONFIG['groom']}")

st.image("static/couple.jpg", width=250, caption="Pasangan Bahagia 💕")

# ================== COUNTDOWN ==================
event_time = datetime.strptime(CONFIG["date"], "%Y-%m-%d %H:%M:%S")
now = datetime.now()
diff = event_time - now
if diff.total_seconds() > 0:
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    st.markdown(f"### ⏳ Menuju Hari Bahagia:")
    st.markdown(f"**{days} Hari {hours} Jam {minutes} Menit {seconds} Detik**")
else:
    st.markdown("### 🥂 Selamat! Hari Bahagia Telah Tiba! 💐")

# ================== DETAIL ACARA ==================
st.markdown("---")
st.markdown(f"📅 **Tanggal & Waktu:** {event_time.strftime('%A, %d %B %Y %H:%M')} WIB")
st.markdown(f"📍 **Lokasi:** {CONFIG['location']}")

st.components.v1.iframe(CONFIG["map_embed"], height=300)

# ================== REKENING HADIAH ==================
st.markdown("---")
st.markdown("🎁 **Rekening Hadiah**")
st.markdown(f"**Bank:** {CONFIG['rekening']['bank']}")
st.markdown(f"**Atas Nama:** {CONFIG['rekening']['atas_nama']}")
st.markdown(f"**Nomor:** `{CONFIG['rekening']['nomor']}`")

# ================== TOMBOL HADIAH ==================
if st.button("🎀 Beri Hadiah ke Alamat Rumah 🎀"):
    st.success(f"Silakan kirim hadiah ke alamat: **{CONFIG['alamat_rumah']}** 💝")
    st.info(f"Atau transfer ke rekening atas nama **{CONFIG['rekening']['atas_nama']}**")

# ================== FORM UCAPAN TAMU ==================
st.markdown("---")
st.markdown("💌 **Kata-Kata Ucapan untuk Mempelai**")

with st.form("ucapan_form"):
    nama = st.text_input("Nama Anda")
    pesan = st.text_area("Tulis ucapan atau doa Anda 💕")
    submitted = st.form_submit_button("Kirim Ucapan")

if submitted and nama and pesan:
    os.makedirs("data", exist_ok=True)
    with open("data/messages.txt", "a", encoding="utf-8") as f:
        f.write(f"{nama}: {pesan}\n")
    st.success("Terima kasih atas ucapan dan doanya 💖")

# ================== MENAMPILKAN UCAPAN ==================
if os.path.exists("data/messages.txt"):
    st.markdown("### 🌷 Doa & Ucapan dari Sahabat 🌷")
    with open("data/messages.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            st.markdown(f"💬 {line.strip()}")

# ================== MUSIK ROMANTIS ==================
st.markdown("---")
st.markdown("🎶 *Musik: Cinta Terakhirku* 🎶")
st.audio("static/cinta_terakhirku.mp3", format="audio/mp3", loop=True)
