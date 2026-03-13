import requests
import os
import shutil
from dotenv import load_dotenv

load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def fetch_tiger_env_assets(query="wild tiger"):
    print(f"[*] Researcher Agent: Mengambil 3 klip harimau yang berbeda...")
    headers = {"Authorization": PEXELS_API_KEY}

    for folder in ["assets/raw_videos", "assets/voiceovers"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder, exist_ok=True)

    url = f"https://api.pexels.com/videos/search?query={query}&per_page=5&orientation=portrait"
    try:
        data = requests.get(url, headers=headers).json()
        for i, v in enumerate(data.get('videos', [])):
            if i >= 3: break
            v_link = v['video_files'][0]['link']
            v_path = f"assets/raw_videos/bg_{i}.mp4"
            with open(v_path, 'wb') as f:
                f.write(requests.get(v_link).content)
            print(f"[+] Klip {i+1} berhasil diunduh.")
    except Exception as e:
        print(f"[!] Gagal unduh klip: {e}")