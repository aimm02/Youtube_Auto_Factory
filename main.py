import asyncio
import os
import shutil
from agents.researcher import fetch_tiger_env_assets
from agents.writer import generate_encyclopedic_script
from agents.editor import create_voice, build_long_documentary

async def main():
    TOPIK = "Harimau Benggala"
    print(f"=== ENCYCLOPEDIA FACTORY: {TOPIK} ===")
    
    for folder in ["assets/raw_videos", "assets/voiceovers"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder, exist_ok=True)

    # Agent Researcher
    fetch_tiger_env_assets(f"{TOPIK} wildlife")
    
    # Agent Writer
    script_dict = generate_encyclopedic_script(TOPIK)
    
    # Agent Editor
    audio_paths = []
    for i in range(1, 4):
        key = f"segmen{i}"
        text = script_dict.get(key)
        path = f"assets/voiceovers/seg_{i-1}.mp3"
        await create_voice(text, path)
        audio_paths.append(path)
    
    # Agent Checker
    output = f"assets/final_out/{TOPIK.replace(' ', '_')}_Doc.mp4"
    os.makedirs("assets/final_out", exist_ok=True)
    build_long_documentary(audio_paths, output)

if __name__ == "__main__":
    asyncio.run(main())