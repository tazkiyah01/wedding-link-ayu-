from flask import Flask, render_template_string, url_for

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>The Wedding Of - Ajeng & Saka</title>
  <style>
    body {font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height:1.5; margin:0; padding:0; color:#222}
    .container{max-width:900px;margin:40px auto;padding:20px}
    header{text-align:center;margin-bottom:30px}
    h1{font-size:2.2rem;margin:0}
    .couple{display:flex;gap:24px;align-items:center;justify-content:center;margin:18px 0}
    .card{border-radius:12px;padding:16px;box-shadow:0 8px 24px rgba(0,0,0,0.08)}
    .grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
    .center{text-align:center}
    .countdown{display:flex;gap:12px;justify-content:center;margin:18px 0}
    .countdown .col{min-width:72px}
    a.button{display:inline-block;padding:10px 14px;border-radius:8px;text-decoration:none;border:1px solid #ddd}
    footer{margin-top:30px;text-align:center;color:#666;font-size:0.9rem}
    @media(max-width:600px){.grid{grid-template-columns:1fr}.couple{flex-direction:column}}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>The Wedding Of - Ajeng & Saka</h1>
      <p>Two souls, one promise — to love, hold, and walk together until the last breath</p>
    </header>

    <section class="card">
      <div class="couple">
        <div class="center">
          <h3>Ajeng Nimasuri</h3>
          <p>Putri ke tiga dari<br>Bpk. Siruk Suharno & Ibu. Tri Murti</p>
        </div>
        <div class="center">
          <h3>Saka Suryo Baskoro</h3>
          <p>Putra ke satu dari<br>Bpk. Edwin Iswidagdo & Ibu. Esty Widiastuti</p>
        </div>
      </div>

      <div class="center">
        <p><em>Allah's blessings message — QS. Ar-Rum : 21</em></p>
      </div>

      <hr>

      <div class="grid">
        <div>
          <h4>Date & Time</h4>
          <p>Sabtu, 15 November 2025</p>
          <p><strong>Akad Nikah</strong><br>08:00 WIB - selesai</p>
          <p><strong>Resepsi</strong><br>11:30 WIB - 14:30 WIB</p>
        </div>
        <div>
          <h4>Location</h4>
          <p>Pendopo Hegar Manah Ranggamekar<br>Kec. Bogor Selatan, Kota Bogor, Jawa Barat 16136<br>(Bogor Nirwana Residence / BNR)</p>
          <p><a class="button" href="https://maps.app.goo.gl" target="_blank" rel="noopener">Lihat lokasi</a></p>
        </div>
      </div>

      <hr>

      <div class="center">
        <h4>Counting down</h4>
        <div class="countdown" id="countdown">
          <div class="col">
            <div id="days">0</div>
            <div>hari</div>
          </div>
          <div class="col">
            <div id="hours">0</div>
            <div>jam</div>
          </div>
          <div class="col">
            <div id="minutes">0</div>
            <div>menit</div>
          </div>
          <div class="col">
            <div id="seconds">0</div>
            <div>detik</div>
          </div>
        </div>
      </div>

      <hr>

      <div class="center">
        <h4>Gift</h4>
        <p>Sekarang hadiahmu bisa tersampaikan secara digital — <a href="#" class="button">Kirim hadiah</a></p>
      </div>

      <hr>

      <div>
        <h4>Ucapan & Doa</h4>
        <p>(Tempat untuk menampilkan galang ucapan/komentar tamu — jika ingin dibuatkan form, beri tahu saya.)</p>
      </div>

    </section>

    <footer>
      <p>powered by OUR WEDDING LINK</p>
    </footer>
  </div>

  <script>
    // Countdown to 15 November 2025 00:00 (WIB timezone +07:00)
    const target = new Date('2025-11-15T00:00:00+07:00').getTime();

    function updateCountdown(){
      const now = new Date().getTime();
      let diff = target - now;
      if(diff < 0) diff = 0;
      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((diff % (1000 * 60)) / 1000);

      document.getElementById('days').textContent = days;
      document.getElementById('hours').textContent = hours;
      document.getElementById('minutes').textContent = minutes;
      document.getElementById('seconds').textContent = seconds;
    }

    updateCountdown();
    setInterval(updateCountdown, 1000);
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

if __name__ == '__main__':
    # Jalankan dengan: python app.py
    app.run(host='0.0.0.0', port=5000, debug=True)
