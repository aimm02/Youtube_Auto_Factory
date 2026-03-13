import requests
import json
import re

def generate_encyclopedic_script(animal_topic="Harimau"):
    url = "http://localhost:11434/api/generate"
    
    prompt = (
        f"Bertindaklah sebagai ahli Zoologi. Buat naskah dokumenter mendalam tentang {animal_topic}. "
        "Fokus pada fakta unik, habitat, dan peran ekosistem. Gunakan Bahasa Indonesia baku. "
        "Bagi menjadi 3 segmen panjang. "
        "WAJIB FORMAT JSON: {'segmen1': '...', 'segmen2': '...', 'segmen3': '...'} "
        "Jangan ada tag <think> atau penjelasan teknis."
    )
    
    payload = {"model": "deepseek-r1:1.5b", "prompt": prompt, "stream": False, "format": "json"}
    
    try:
        print(f"[*] Writer Agent: Meriset data ensiklopedia untuk {animal_topic}...")
        response = requests.post(url, json=payload)
        res_text = response.json().get('response', '{}')
        res_text = re.sub(r'<think>.*?</think>', '', res_text, flags=re.DOTALL).strip()
        
        data = json.loads(res_text)
        keys = list(data.keys())
        return {
            "segmen1": str(data.get(keys[0], "")),
            "segmen2": str(data.get(keys[1] if len(keys)>1 else keys[0], "")),
            "segmen3": str(data.get(keys[2] if len(keys)>2 else keys[0], ""))
        }
    except Exception as e:
        print(f"[!] Writer Error: {e}. Menggunakan naskah cadangan.")
        return {
            "segmen1": f"{animal_topic} adalah pemangsa puncak yang memiliki peran krusial dalam menjaga keseimbangan alam liar.",
            "segmen2": f"Dengan kemampuan adaptasi yang luar biasa, {animal_topic} mampu bertahan hidup di lingkungan yang menantang.",
            "segmen3": f"Melindungi habitat {animal_topic} adalah kunci bagi kelestarian keanekaragaman hayati bumi kita."
        }