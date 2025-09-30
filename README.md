# cctv-proxy-auth-bypass

Proxy kecil untuk menambahkan header `Authorization: Basic ...` secara *preemptive* ke snapshot camera yang menolak request non-preemptive.

## Gambaran singkat
Beberapa kamera murah (Esee / V380 / Anyka) hanya menerima preemptive Basic Auth. Mereka menerima `curl -u user:pass` tapi menolak request dari browser atau NVR yang menunggu `401` challenge. Proxy ini menambahkan header Authorization pada request keluar ke kamera, sehingga NVR/AgentDVR dapat mengambil snapshot tanpa 401.

## Files
- `cam.py` → Flask proxy (simple, dev server). Edit `CAMERA_URL` / `AUTH_HEADER` atau set env vars.
- `requirements.txt` → Python dependencies.
- `.gitignore` → standard ignores.

## Cara cepat (nohup, sesuai preferensimu)
1. Copy repository ke server (contoh `/root/waw`).
2. Pasang dependency (opsi APT atau virtualenv):
```bash
# APT (recommended on Debian/OMV)
apt update
apt install -y python3 python3-pip
apt install -y python3-flask python3-requests

# OR using virtualenv (if you prefer)
python3 -m venv /root/waw/venv
source /root/waw/venv/bin/activate
pip install -r requirements.txt
```

3. Jalankan dengan nohup (background):
```bash
cd /root/waw
nohup python3 /root/waw/cam.py > cam.log 2>&1 &
```

4. Cek proses dan log:
```bash
pgrep -f cam.py
tail -f cam.log
```

5. Stop:
```bash
PID=$(pgrep -f cam.py)
kill $PID
# or force
kill -9 $PID
```

## Konfigurasi environment (opsional)
You can override defaults with environment variables before starting:
```bash
export CAMERA_URL="http://192.168.95.123/snapshot.jpg"
export AUTH_HEADER="Basic YWRtaW46YWRtaW4xMjM="
export PORT=8081
nohup python3 cam.py > cam.log 2>&1 &
```

## Catatan
- Flask development server cukup untuk use-case rumahan / lab. For production, consider gunicorn/uvicorn.
- Jangan commit secrets (base64 auth) to public repos. Use GitHub Secrets or environment variables for production usage.
