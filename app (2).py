from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory, flash
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change_this_secret"

# Path to store guest messages
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
MESSAGES_FILE = os.path.join(DATA_DIR, 'messages.json')

# Ensure data dir exists
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(MESSAGES_FILE):
    with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)

# Configuration: edit these values for your wedding
CONFIG = {
    "bride": "Ajeng Nimasuri",
    "groom": "Saka Suryo Baskoro",
    "datetime": "2025-11-15 08:00:00",  # YYYY-MM-DD HH:MM:SS local time (WIB)
    "location_text": "Pendopo Hegar Manah Ranggamekar, Kec. Bogor Selatan, Kota Bogor, Jawa Barat 16136",
    # Replace with your real Google Maps embed URL (from Google Maps -> Share -> Embed a map -> copy iframe src)
    "map_embed_url": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3966.0527146742144!2d106.789!3d-6.252!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2e69ef9dabcde123%3A0x111222333444555!2sPendopo%20Hegar%20Manah!5e0!3m2!1sid!2sid!4v1700000000000",
    "home_address": "Jl. Contoh No.10, Bogor, Jawa Barat, 16136",
    "rekening": {
        "bank": "BCA",
        "atas_nama": "Saka Suryo Baskoro",
        "nomor": "1234567890"
    },
    # Static filenames - place these files in the `static/` folder
    "background_images": ["bg_flowers.jpg", "bg_stage.jpg"],
    "couple_photo": "couple.jpg",
    "music_file": "cinta_terakhirku.mp3"
}

TEMPLATE = r"""
<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Undangan Pernikahan - {{ bride }} & {{ groom }}</title>
  <style>
    /* Basic reset */
    *{box-sizing:border-box}
    body{margin:0;font-family:Inter, 'Segoe UI', Roboto, Arial;background:#fafafa}

    /* Background layers: flowers + stage */
    .bg-layer{
      position:fixed;inset:0;z-index:-3;background-size:cover;background-position:center;opacity:0.85;
      transition:opacity 0.6s ease;
    }
    .bg-flowers{z-index:-3}
    .bg-stage{z-index:-2;filter:blur(2px);opacity:0.55}

    .overlay{position:relative;min-height:100vh;background:linear-gradient(rgba(0,0,0,0.35), rgba(0,0,0,0.35));display:flex;flex-direction:column;align-items:center;justify-content:flex-start;padding:40px 16px;color:white}

    .card{background:rgba(255,255,255,0.06);backdrop-filter:blur(4px);padding:28px;border-radius:16px;max-width:980px;width:100%;box-shadow:0 8px 30px rgba(0,0,0,0.35)}

    header{text-align:center}
    h1{margin:6px 0;font-size:2.2rem}
    h2{margin:0;font-weight:400;opacity:0.9}

    .couple{display:flex;gap:18px;align-items:center;justify-content:center;margin-top:18px}
    .photo{width:180px;height:180px;border-radius:50%;overflow:hidden;border:6px solid rgba(255,255,255,0.9)}
    .photo img{width:100%;height:100%;object-fit:cover;display:block}

    .info{padding:0 12px;text-align:center}
    .date{font-size:1.05rem;margin-top:12px}

    .countdown{display:flex;gap:12px;justify-content:center;margin-top:18px}
    .countdown .col{min-width:72px;background:rgba(255,255,255,0.06);padding:12px;border-radius:10px}
    .countdown .num{font-size:1.4rem;font-weight:700}

    .grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px}

    .box{background:rgba(255,255,255,0.04);padding:14px;border-radius:12px}
    .box h3{margin:0 0 8px 0}

    .map iframe{width:100%;height:260px;border:0;border-radius:10px}

    .btn{display:inline-block;padding:10px 16px;border-radius:10px;background:#f8c0d3;color:#2b2b2b;text-decoration:none;border:none;cursor:pointer}

    form.add-msg{display:flex;gap:8px;margin-top:10px}
    form.add-msg input[type=text]{flex:1;padding:10px;border-radius:8px;border:1px solid rgba(255,255,255,0.12);background:transparent;color:white}
    form.add-msg button{padding:10px 14px;border-radius:8px;border:none;background:#ffd6a5}

    .messages{max-height:200px;overflow:auto;margin-top:8px}
    .message{background:rgba(0,0,0,0.25);padding:10px;border-radius:8px;margin-bottom:8px}

    footer{margin-top:18px;text-align:center;color:rgba(255,255,255,0.8);font-size:0.9rem}

    @media(max-width:800px){.grid{grid-template-columns:1fr}.couple{flex-direction:column}.photo{width:140px;height:140px}}
  </style>
</head>
<body>
  <!-- Background images (place static/bg_flowers.jpg and static/bg_stage.jpg) -->
  <div class="bg-layer bg-flowers" style="background-image:url('{{ url_for('static', filename=bg1) }}')"></div>
  <div class="bg-layer bg-stage" style="background-image:url('{{ url_for('static', filename=bg2) }}')"></div>

  <div class="overlay">
    <div class="card">
      <header>
        <h2>Undangan Pernikahan</h2>
        <h1>{{ bride }} <span style="opacity:0.8">&amp;</span> {{ groom }}</h1>
        <div class="couple">
          <div class="photo"><img src="{{ url_for('static', filename=couple_photo) }}" alt="Foto pasangan"></div>
        </div>
        <div class="date">{{ event_date_str }}</div>

        <div class="countdown" id="countdown">
          <div class="col"><div class="num" id="days">0</div><div>Hari</div></div>
          <div class="col"><div class="num" id="hours">0</div><div>Jam</div></div>
          <div class="col"><div class="num" id="minutes">0</div><div>Menit</div></div>
          <div class="col"><div class="num" id="seconds">0</div><div>Detik</div></div>
        </div>
      </header>

      <div class="grid">
        <div class="box">
          <h3>Lokasi</h3>
          <p>{{ location_text }}</p>
          <div class="map"><iframe src="{{ map_embed_url }}" allowfullscreen loading="lazy"></iframe></div>
        </div>

        <div class="box">
          <h3>Hadiah & Donasi</h3>
          <p><strong>Rekening</strong><br>{{ rekening.bank }} - {{ rekening.nomor }}<br>a.n. {{ rekening.atas_nama }}</p>

          <h4>Alternatif: Kirim Hadiah ke Alamat Rumah</h4>
          <p>{{ home_address }}</p>
          <button class="btn" onclick="copyHomeAddress()">Salin Alamat Rumah</button>
          <button class="btn" onclick="window.location.href='{{ url_for('send_gift') }}'">Beri Hadiah ke Alamat Rumah</button>

          <hr style="margin:12px 0;border:none;border-top:1px solid rgba(255,255,255,0.06)">
          <h4>Kata - kata Ucapan</h4>

          <form class="add-msg" action="{{ url_for('add_message') }}" method="post">
            <input type="text" name="author" placeholder="Nama (contoh: Bapak/Ibu)" required>
            <input type="text" name="message" placeholder="Ucapan singkat" required>
            <button type="submit">Kirim</button>
          </form>

          <div class="messages">
            {% if messages|length == 0 %}
              <p style="opacity:0.8">Belum ada ucapan. Jadilah yang pertama!</p>
            {% else %}
              {% for m in messages|reverse %}
                <div class="message"><strong>{{ m.author }}</strong><div style="margin-top:6px">{{ m.text }}</div><div style="opacity:0.7;font-size:0.8rem;margin-top:6px">{{ m.time }}</div></div>
              {% endfor %}
            {% endif %}
          </div>

        </div>
      </div>

      <footer>
        <p>Terima kasih sudah hadir dan mendoakan. Powered by Your Wedding</p>
      </footer>
    </div>
  </div>

  <!-- Background music (place static/cinta_terakhirku.mp3) -->
  <audio id="bgmusic" loop>
    <source src="{{ url_for('static', filename=music_file) }}" type="audio/mpeg">
    Your browser does not support the audio element.
  </audio>

  <script>
    // Try to autoplay; many browsers block autoplay with sound. We'll attempt and mute if blocked, and provide instruction.
    const audioEl = document.getElementById('bgmusic');
    function tryPlay() {
      const p = audioEl.play();
      if (p !== undefined) {
        p.then(()=>{
          // playing
        }).catch(()=>{
          // failed to autoplay, try muted play and show user a hint
          audioEl.muted = true;
          audioEl.play().catch(()=>{});
          // show a small notice (flash)
          alert('Autoplay diblokir oleh browser. Klik ikon play pada halaman untuk memutar musik.');
        });
      }
    }
    tryPlay();

    function updateCountdown(){
      const target = new Date("{{ event_iso }}").getTime();
      const now = new Date().getTime();
      let diff = target - now;
      if (diff < 0) diff = 0;
      const days = Math.floor(diff / (1000*60*60*24));
      const hours = Math.floor((diff % (1000*60*60*24)) / (1000*60*60));
      const minutes = Math.floor((diff % (1000*60*60)) / (1000*60));
      const seconds = Math.floor((diff % (1000*60)) / 1000);
      document.getElementById('days').textContent = days;
      document.getElementById('hours').textContent = hours;
      document.getElementById('minutes').textContent = minutes;
      document.getElementById('seconds').textContent = seconds;
    }
    updateCountdown();
    setInterval(updateCountdown, 1000);

    function copyHomeAddress(){
      navigator.clipboard.writeText('{{ home_address }}').then(()=>{
        alert('Alamat rumah disalin ke clipboard. Terima kasih!');
      }).catch(()=>{alert('Tidak dapat menyalin alamat. Silakan salin manual: {{ home_address }}')});
    }
  </script>
</body>
</html>
"""


def read_messages():
    try:
        with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def write_messages(msgs):
    with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(msgs, f, ensure_ascii=False, indent=2)


@app.route('/')
def index():
    # Prepare template context
    event_dt = datetime.strptime(CONFIG['datetime'], "%Y-%m-%d %H:%M:%S")
    event_iso = event_dt.isoformat()  # JS-friendly
    context = {
        'bride': CONFIG['bride'],
        'groom': CONFIG['groom'],
        'event_date_str': event_dt.strftime('%A, %d %B %Y %H:%M'),
        'event_iso': event_iso,
        'location_text': CONFIG['location_text'],
        'map_embed_url': CONFIG['map_embed_url'],
        'rekening': CONFIG['rekening'],
        'home_address': CONFIG['home_address'],
        'bg1': CONFIG['background_images'][0],
        'bg2': CONFIG['background_images'][1],
        'couple_photo': CONFIG['couple_photo'],
        'music_file': CONFIG['music_file'],
        'messages': read_messages()
    }
    return render_template_string(TEMPLATE, **context)


@app.route('/add_message', methods=['POST'])
def add_message():
    author = request.form.get('author', '').strip()
    text = request.form.get('message', '').strip()
    if not author or not text:
        flash('Nama dan pesan harus diisi', 'error')
        return redirect(url_for('index'))
    msgs = read_messages()
    msgs.append({'author': author, 'text': text, 'time': datetime.now().strftime('%Y-%m-%d %H:%M')})
    write_messages(msgs)
    flash('Ucapan berhasil dikirim — terima kasih!', 'success')
    return redirect(url_for('index'))


@app.route('/send_gift')
def send_gift():
    # Simple page that thanks user and shows the home address to send gift to
    return render_template_string('''
    <!doctype html>
    <html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Beri Hadiah</title></head>
    <body style="font-family:Inter,Arial;display:flex;align-items:center;justify-content:center;height:100vh;background:#f7f7f7">
      <div style="background:white;padding:24px;border-radius:12px;max-width:520px;text-align:center;box-shadow:0 10px 30px rgba(0,0,0,0.08)">
        <h2>Terima kasih ingin memberikan hadiah 🎁</h2>
        <p>Silakan kirim hadiah (paket/perabot) ke alamat berikut:</p>
        <p style="font-weight:700">{{ addr }}</p>
        <p>Atau gunakan nomor rekening berikut untuk transfer:</p>
        <p style="font-weight:700">{{ bank }} — {{ rek }} (a.n. {{ nama }})</p>
        <p style="margin-top:18px"><a href="/" style="text-decoration:none;padding:10px 14px;background:#ffd6a5;border-radius:8px;color:#000">Kembali ke undangan</a></p>
      </div>
    </body></html>
    ''', addr=CONFIG['home_address'], bank=CONFIG['rekening']['bank'], rek=CONFIG['rekening']['nomor'], nama=CONFIG['rekening']['atas_nama'])


# Static files are served by Flask automatically from the 'static' folder.

if __name__ == '__main__':
    # Run with: python app.py
    app.run(host='0.0.0.0', port=5000, debug=True)
